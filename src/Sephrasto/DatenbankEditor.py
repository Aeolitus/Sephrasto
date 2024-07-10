# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:29:39 2017

@author: Aeolitus
"""
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Core.DatenbankEinstellung import DatenbankEinstellung
from Core.Attribut import AttributDefinition
from Core.AbgeleiteterWert import AbgeleiteterWertDefinition
from Core.Energie import EnergieDefinition
from Core.Fertigkeit import FertigkeitDefinition, UeberFertigkeitDefinition
from Core.FreieFertigkeit import FreieFertigkeitDefinition
from Core.Regel import Regel
from Core.Ruestung import RuestungDefinition
from Core.Talent import TalentDefinition
from Core.Vorteil import VorteilDefinition
from Core.Waffe import WaffeDefinition
from Core.Waffeneigenschaft import Waffeneigenschaft
from Core.DatenbankEinstellung import DatenbankEinstellung
from Datenbank import Datenbank
import UI.DatenbankMain
import DatenbankEditFertigkeitWrapper
import DatenbankEditFreieFertigkeitWrapper
import DatenbankEditTalentWrapper
import DatenbankEditVorteilWrapper
import DatenbankEditWaffeneigenschaftWrapper
import DatenbankEditWaffeWrapper
import DatenbankEditRuestungWrapper
import DatenbankEditRegelWrapper
import DatenbankEditEinstellungWrapper
import DatenbankEditAttributWrapper
import DatenbankEditAbgeleiteterWertWrapper
import DatenbankEditEnergieWrapper
import DatenbankErrorLogWrapper
import DatenbankMergeDialogWrapper
import os
from EinstellungenWrapper import EinstellungenWrapper
from Wolke import Wolke
from copy import copy
import logging
from EventBus import EventBus
from WebEngineWrapper import WebEngineWrapper
from Hilfsmethoden import Hilfsmethoden
from QtUtils.RichTextButton import RichTextToolButton
from CharakterAssistent.WizardWrapper import WizardWrapper
from functools import partial
import fnmatch
from Migrationen import Migrationen

class DatenbankTypWrapper:
    def __init__(self, dataType, editorType, isDeletable):
        self.dataType = dataType
        self.editorType = editorType
        self.isDeletable = isDeletable
        self.isAddable = isDeletable
        self.showCategory = hasattr(dataType, "kategorieName")
        self.showDetails = hasattr(dataType, "details")

    def add(self, datenbank):
        return self.edit(datenbank, self.dataType())

    def edit(self, datenbank, inp, readonly = False):
        filterName = self.dataType.__name__.lower()
        editorType = EventBus.applyFilter("dbe_class_" + filterName + "_wrapper", self.editorType)
        editor = editorType(datenbank, inp, readonly)
        editor.setupAsDialogAndShow()
        return editor.element
    
    def display(self, datenbank, inp, readonly = False):
        filterName = self.dataType.__name__.lower()
        editorType = EventBus.applyFilter("dbe_class_" + filterName + "_wrapper", self.editorType)
        editor = editorType(datenbank, inp, readonly)
        editor.setupAsWidget()
        return editor      

class DBESortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, datenbank, parent=None):
        super().__init__(parent)
        self.datenbank = datenbank
        self.nameFilter = ""
        self.fullText = False
        self.statusFilters = []

    def lessThan(self, leftIndex, rightIndex):
        model = self.sourceModel()
        left = model.data(leftIndex)
        right = model.data(rightIndex)
        return Hilfsmethoden.unicodeCaseInsensitive(left) < Hilfsmethoden.unicodeCaseInsensitive(right)

    def setFilters(self, nameFilter, statusFilters, fullText = False):
        self.nameFilter = nameFilter.lower()
        if not self.nameFilter.startswith("*"):
            self.nameFilter = "*" + self.nameFilter
        if not self.nameFilter.endswith("*"):
            self.nameFilter += "*"

        self.statusFilters = statusFilters
        self.fullText = fullText
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        model = self.sourceModel()
        statusIndex = model.index(sourceRow, 0, sourceParent)
        status = model.data(statusIndex)
        nameIndex = model.index(sourceRow, 1, sourceParent)
        element = model.data(nameIndex, QtCore.Qt.UserRole)
        if not self.fullText:
            return fnmatch.fnmatchcase(element.name.lower(), self.nameFilter) and status in self.statusFilters
        else:
            return (fnmatch.fnmatchcase(element.name.lower(), self.nameFilter) or fnmatch.fnmatchcase(element.details(self.datenbank).lower(), self.nameFilter)) and status in self.statusFilters

class DatenbankEditor(object):
    def __init__(self, plugins, onCloseCB):
        super().__init__()
        self.plugins = plugins
        self.onCloseCB = onCloseCB
        self.databaseTypes = {}
        self.datenbank = Datenbank()
        self.datenbank.loadFile(hausregeln = Wolke.Settings['Datenbank'])
        self.showDatabaseMigrationUpdatesPopup()
        self.savepath = self.datenbank.hausregelDatei
        self.changed = False
        self.windowTitleDefault = ""
        self.checkMissingPlugins()

    def getDatabaseChangingPlugins(self):
        enabledPlugins = []
        for pluginData in self.plugins:
            if pluginData.plugin is not None and hasattr(pluginData.plugin, "changesDatabase") and pluginData.plugin.changesDatabase():
                enabledPlugins.append(pluginData.name)
        return enabledPlugins

    def checkMissingPlugins(self):
        enabledPlugins = self.getDatabaseChangingPlugins()       
        missingPlugins = set(self.datenbank.enabledPlugins) - set(enabledPlugins)
        if len(missingPlugins) > 0:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setWindowTitle("Plugin fehlt!")
            infoBox.setText("Die Datenbank wurde mit einem oder mehreren Plugins erstellt, die sie beeinflussen. "\
            "Nicht alle davon sind aktiv, daher können beim Speichern Daten dieser Plugins verloren gehen:\n\n" + ", ".join(missingPlugins))
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()

        self.datenbank.enabledPlugins = enabledPlugins
    
    def setupGUI(self):
        windowSize = Wolke.Settings["WindowSize-Datenbank"]
        self.form.resize(windowSize[0], windowSize[1])

        self.menus = {
            "Datei" : self.ui.menuDatei,
            "Analysieren" : self.ui.menuAnalysieren,
            "Export" : self.ui.menuExport,
            "Hilfe" : self.ui.menuHilfe,
        }

        def addMenuItem(menu, action):
            if menu not in self.menus:
                self.menus[menu] = QtWidgets.QMenu(self.ui.menubar)
                self.menus[menu].setTitle(menu)
                self.ui.menubar.addAction(self.menus[menu].menuAction())
            self.menus[menu].addAction(action)
        EventBus.doAction("dbe_menuitems_erstellen", { "addMenuItemCB" : addMenuItem })

        # GUI Mods
        self.ui.labelFilterName.setText("\uf002")
        self.ui.nameFilterEdit.textChanged.connect(self.updateFilter)
        self.ui.checkFullText.stateChanged.connect(self.updateFilter)

        self.shortcutSearch = QtGui.QAction()
        self.shortcutSearch.setShortcut("Ctrl+F")
        self.shortcutSearch.triggered.connect(self.ui.nameFilterEdit.setFocus)
        self.ui.nameFilterEdit.addAction(self.shortcutSearch)
        self.shortcutClearSearch = QtGui.QAction()
        self.shortcutClearSearch.setShortcut("Esc")
        self.shortcutClearSearch.triggered.connect(lambda: self.ui.nameFilterEdit.setText("") if self.ui.nameFilterEdit.hasFocus() else None)
        self.ui.nameFilterEdit.addAction(self.shortcutClearSearch)

        self.buttonStatusFilterText = "<span style='" + Wolke.FontAwesomeCSS + f"'>\uf0b0</span>&nbsp;&nbsp;Status-Filter"
        self.ui.buttonStatusFilter = RichTextToolButton(None, self.buttonStatusFilterText)
        self.ui.buttonStatusFilter.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.ui.horizontalLayout_3.addWidget(self.ui.buttonStatusFilter)
        self.statusFilterMenu = QtWidgets.QMenu()

        action = self.statusFilterMenu.addAction("Filter zurücksetzen")
        #action.setData("\uf068")
        action.setShortcut("Ctrl+R")
        action.setVisible(False)
        action.triggered.connect(self.resetFilter)

        action = self.statusFilterMenu.addAction("Hinzugefügt")
        action.setData("+")
        action.setCheckable(True)
        action.setShortcut("Ctrl+H")
        action.triggered.connect(self.updateFilter)

        action = self.statusFilterMenu.addAction("Verändert")
        action.setData("\uf044")
        action.setCheckable(True)
        action.setShortcut("Ctrl+V")
        action.triggered.connect(self.updateFilter)

        action = self.statusFilterMenu.addAction("Unverändert")
        action.setData("\uf02d")
        action.setCheckable(True)
        action.setShortcut("Ctrl+U")
        action.triggered.connect(self.updateFilter)

        action = self.statusFilterMenu.addAction("Gelöscht")
        action.setData("\uf068")
        action.setCheckable(True)
        action.setShortcut("Ctrl+G")
        action.triggered.connect(self.updateFilter)

        self.ui.buttonStatusFilter.setMenu(self.statusFilterMenu)

        # Menu actions
        self.ui.actionOeffnen.triggered.connect(lambda: self.loadDatenbank())
        self.ui.actionZusaetzlichOeffnen.triggered.connect(lambda: self.loadDatenbank(True))
        self.ui.actionZusaetzlichOeffnen.setEnabled(self.datenbank.hausregelDatei is not None)
        self.ui.actionSpeichern.triggered.connect(self.quicksaveDatenbank)
        self.ui.actionSpeichern_unter.triggered.connect(self.saveDatenbank)
        self.ui.actionDBMergen.triggered.connect(lambda: self.saveDatenbank(True))
        self.ui.actionSchliessen.triggered.connect(self.closeDatenbank)
        self.ui.actionReload.triggered.connect(self.reloadDatenbank)
        self.ui.actionBeenden.triggered.connect(lambda: self.form.close())

        self.ui.actionFehlerliste.triggered.connect(self.showErrorLog)
        self.wizardActions = []
        for baukastenFolder in WizardWrapper.getBaukastenFolders():
            action = QtGui.QAction("Charakter Assistent: " + os.path.basename(baukastenFolder))
            action.triggered.connect(partial(self.showCharakterAssistentErrorLog, baukasten=baukastenFolder))
            self.ui.menuAnalysieren.addAction(action)
            self.wizardActions.append(action)

        self.ui.actionCharakterAssistent.triggered.connect(self.showCharakterAssistentErrorLog)

        self.ui.actionDatenbank_Editor.triggered.connect(self.showEditorHelp)
        self.ui.actionScript_API.triggered.connect(self.showScriptHelp)

        # Edit buttons
        self.ui.buttonOpen.clicked.connect(self.loadDatenbank)
        self.ui.buttonOpen.setText("\uf07c")
        self.setButtonShortcut(self.ui.buttonOpen, "Ctrl+O")

        self.ui.buttonQuicksave.clicked.connect(self.quicksaveDatenbank)
        self.ui.buttonQuicksave.setText("\uf0c7")
        self.setButtonShortcut(self.ui.buttonQuicksave, "Ctrl+S")

        self.ui.buttonEditieren.clicked.connect(self.editSelected)
        self.ui.buttonEditieren.setEnabled(False)
        self.ui.buttonEditieren.setText("\uf044")
        self.setButtonShortcut(self.ui.buttonEditieren, "Return")

        self.ui.buttonDuplizieren.clicked.connect(self.duplicateSelected)
        self.ui.buttonDuplizieren.setEnabled(False)
        self.ui.buttonDuplizieren.setText("\uf24d")
        self.setButtonShortcut(self.ui.buttonDuplizieren, "Ctrl+D")

        self.ui.buttonLoeschen.clicked.connect(self.deleteSelected)
        self.ui.buttonLoeschen.setEnabled(False)
        self.ui.buttonLoeschen.setText("\uf2ed")
        self.setButtonShortcut(self.ui.buttonLoeschen, "Del")

        self.ui.buttonNeu.clicked.connect(self.hinzufuegen)
        self.ui.buttonNeu.setText("\u002b")
        self.setButtonShortcut(self.ui.buttonNeu, "Ctrl+N")

        self.ui.buttonWiederherstellen.clicked.connect(self.wiederherstellen)
        self.ui.buttonWiederherstellen.setText("\uf829")
        self.setButtonShortcut(self.ui.buttonWiederherstellen, "Ctrl+W")

        self.ui.buttonRAW.clicked.connect(self.vanillaAnsehen)
        self.ui.buttonRAW.setText("\uf02d")
        self.setButtonShortcut(self.ui.buttonRAW, "Ctrl+R")

        self.ui.checkDetails.stateChanged.connect(self.onDetailsClicked)

        # Add shortcuts for tab cycling
        # QTabWidget has this builtin but it only works in certain conditions, probably some focus issue
        self.shortcutNextTab = QtGui.QAction() 
        self.shortcutNextTab.setShortcut("Ctrl+Tab")
        self.shortcutNextTab.triggered.connect(self.nextTab)
        self.ui.tabWidget.addAction(self.shortcutNextTab)

        self.shortcutPrevTab = QtGui.QAction()
        self.shortcutPrevTab.setShortcut("Ctrl+Shift+Tab")
        self.shortcutPrevTab.triggered.connect(self.previousTab)
        self.ui.tabWidget.addAction(self.shortcutPrevTab)

        self.databaseTypes = {}
        self.databaseTypes[AbgeleiteterWertDefinition] = DatenbankTypWrapper(AbgeleiteterWertDefinition, DatenbankEditAbgeleiteterWertWrapper.DatenbankEditAbgeleiteterWertWrapper, True)
        self.databaseTypes[AttributDefinition] = DatenbankTypWrapper(AttributDefinition, DatenbankEditAttributWrapper.DatenbankEditAttributWrapper, True)
        self.databaseTypes[DatenbankEinstellung] = DatenbankTypWrapper(DatenbankEinstellung, DatenbankEditEinstellungWrapper.DatenbankEditEinstellungWrapper, False)
        self.databaseTypes[EnergieDefinition] = DatenbankTypWrapper(EnergieDefinition, DatenbankEditEnergieWrapper.DatenbankEditEnergieWrapper, True)
        self.databaseTypes[FertigkeitDefinition] = DatenbankTypWrapper(FertigkeitDefinition, DatenbankEditFertigkeitWrapper.DatenbankEditProfaneFertigkeitWrapper, True)
        self.databaseTypes[UeberFertigkeitDefinition] = DatenbankTypWrapper(UeberFertigkeitDefinition, DatenbankEditFertigkeitWrapper.DatenbankEditUebernatürlicheFertigkeitWrapper, True)
        self.databaseTypes[FreieFertigkeitDefinition] = DatenbankTypWrapper(FreieFertigkeitDefinition, DatenbankEditFreieFertigkeitWrapper.DatenbankEditFreieFertigkeitWrapper, True)
        self.databaseTypes[Regel] = DatenbankTypWrapper(Regel, DatenbankEditRegelWrapper.DatenbankEditRegelWrapper, True)
        self.databaseTypes[RuestungDefinition] = DatenbankTypWrapper(RuestungDefinition, DatenbankEditRuestungWrapper.DatenbankEditRuestungWrapper, True)
        self.databaseTypes[TalentDefinition] = DatenbankTypWrapper(TalentDefinition, DatenbankEditTalentWrapper.DatenbankEditTalentWrapper, True)
        self.databaseTypes[VorteilDefinition] = DatenbankTypWrapper(VorteilDefinition, DatenbankEditVorteilWrapper.DatenbankEditVorteilWrapper, True)
        self.databaseTypes[WaffeDefinition] = DatenbankTypWrapper(WaffeDefinition, DatenbankEditWaffeWrapper.DatenbankEditWaffeWrapper, True)
        self.databaseTypes[Waffeneigenschaft] = DatenbankTypWrapper(Waffeneigenschaft, DatenbankEditWaffeneigenschaftWrapper.DatenbankEditWaffeneigenschaftWrapper, True)
        self.databaseTypes = EventBus.applyFilter("datenbank_editor_typen", self.databaseTypes)

        self.ui.tabWidget.setStyleSheet(f"QTabBar::tab {{ max-height: {max(Hilfsmethoden.emToPixels(4.5), 40)}px; }}")
        tabIndex = 0
        self.lists = []
        self.models = []
        self.filters = []
        self.databaseTypesByIndex = []
        self.tabLabels = []

        for dbType in sorted(self.databaseTypes, key = lambda t: Hilfsmethoden.unicodeCaseInsensitive(t.displayName)):
            self.databaseTypesByIndex.append(dbType)
            tableView = QtWidgets.QTableView()
            self.lists.append(tableView)
            model = QtGui.QStandardItemModel(tableView)
            self.models.append(model)

            filterProxy = DBESortFilterProxyModel(self.datenbank)
            self.filters.append(filterProxy)
            filterProxy.setSourceModel(model)

            tableView.setModel(filterProxy)
            tableView.doubleClicked["QModelIndex"].connect(self.editSelected)
            tableView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            tableView.selectionModel().selectionChanged.connect(self.listSelectionChanged)         
            tableView.setAlternatingRowColors(True)
            tableView.setShowGrid(False)
            tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            tableView.setSortingEnabled(True)
            tableView.sortByColumn(1, QtCore.Qt.AscendingOrder);
            tableView.verticalHeader().setVisible(False)
            setting = 'ColumnWidth-DBName' + dbType.__name__
            if setting not in Wolke.Settings:
                Wolke.Settings[setting] = 250
            tableView.horizontalHeader().sectionResized.connect(lambda col, old, new, setting=setting: Wolke.Settings.update({setting : new}) if col == 1 else None)
            setting = 'ColumnWidth-DBTyp' + dbType.__name__
            if setting not in Wolke.Settings:
                Wolke.Settings[setting] = 150
            tableView.horizontalHeader().sectionResized.connect(lambda col, old, new, setting=setting: Wolke.Settings.update({setting : new}) if col == 2 else None)

            # Hack: we are setting the tab name to empty and add a label as tab button. A Proper solution would be to subclass the tab widget.
            self.ui.tabWidget.insertTab(tabIndex, tableView, "")
            tabLabel = QtWidgets.QLabel(dbType.displayName)
            self.tabLabels.append(tabLabel)
            self.ui.tabWidget.tabBar().setTabButton(tabIndex, QtWidgets.QTabBar.ButtonPosition.LeftSide, tabLabel)
            tabIndex += 1

        self.ui.tabWidget.currentChanged.connect(self.currentTabChanged)

        self.form.closeEvent = self.closeEvent
        self.windowTitleDefault = self.form.windowTitle()

        self.updateFilter()
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()

        if len(self.datenbank.loadingErrors) > 0:
            QtCore.QTimer.singleShot(0, self.showErrorLog)

    def setButtonShortcut(self, button, shortcutStr):
        button.setShortcut(shortcutStr)
        button.setToolTip(button.toolTip() + " (" + button.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")

    def nextTab(self):
        index = self.ui.tabWidget.currentIndex() + 1
        if index >= self.ui.tabWidget.count():
            index = 0
        while not self.ui.tabWidget.isTabVisible(index):
            index += 1
            if index >= self.ui.tabWidget.count():
                index = 0

        self.ui.tabWidget.setCurrentIndex(index)

    def previousTab(self):
        index = self.ui.tabWidget.currentIndex() - 1
        if index < 0:
            index = self.ui.tabWidget.count() - 1
        while not self.ui.tabWidget.isTabVisible(index):
            index -= 1
            if index < 0:
                index = self.ui.tabWidget.count()-1

        self.ui.tabWidget.setCurrentIndex(index)

    def onDetailsClicked(self):
        dbType = self.databaseTypesByIndex[self.ui.tabWidget.currentIndex()]
        typeWrapper = self.databaseTypes[dbType]
        if typeWrapper.showDetails:
            self.updateGUI()

    def resetFilter(self):
        for action in self.statusFilterMenu.actions()[1:]:
            action.blockSignals(True)
            action.setChecked(False)
            action.blockSignals(False)
        self.updateFilter()

    def currentTabChanged(self):
        self.updateFilter()
        self.updateGUI() 

    def listSelectionChanged(self):
        dbType = self.databaseTypesByIndex[self.ui.tabWidget.currentIndex()]
        tableView = self.lists[self.ui.tabWidget.currentIndex()]
        model = self.models[self.ui.tabWidget.currentIndex()]
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        indexes = tableView.selectedIndexes()
        self.ui.buttonNeu.setEnabled(self.databaseTypes[dbType].isAddable)
        if not indexes:
            self.ui.buttonEditieren.setEnabled(False)
            self.ui.buttonLoeschen.setEnabled(False)
            self.ui.buttonLoeschen.setVisible(True)
            self.ui.buttonWiederherstellen.setVisible(False)
            self.ui.buttonDuplizieren.setEnabled(False)
            self.ui.buttonRAW.setVisible(False)
            return

        self.ui.buttonEditieren.setEnabled(True)

        deletable = True
        restorable = True
        duplicatable = True
        userAdded = True
        changed = True
        for idx in indexes:
            element = model.itemFromIndex(filter.mapToSource(idx)).data(QtCore.Qt.UserRole)
            if element is None:
                continue
            if not self.databaseTypes[element.__class__].isDeletable:
                deletable = False
            if not self.databaseTypes[element.__class__].isAddable:
                duplicatable = False

            if self.datenbank.isRemoved(element):
                deletable = False
                duplicatable = False
                userAdded = False
                changed = False
            elif self.datenbank.isOverriddenByOther(element):
                deletable = False
                duplicatable = False
                userAdded = False
                changed = False
            else:
                restorable = False
                if not self.datenbank.isChangedOrNew(element):
                    userAdded = False
                if not self.datenbank.isChanged(element):
                    changed = False

        self.ui.buttonLoeschen.setVisible(not restorable or deletable or userAdded)
        self.ui.buttonLoeschen.setEnabled(deletable or userAdded)
        self.ui.buttonWiederherstellen.setVisible(restorable)
        self.ui.buttonWiederherstellen.setVisible(restorable)
        self.ui.buttonDuplizieren.setEnabled(duplicatable)
        self.ui.buttonRAW.setVisible(changed)

    def cancelDueToPendingChanges(self, action):
        if self.changed:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle(action)
            messagebox.setText("Sollen die ausstehenden Änderungen gespeichert werden?")
            messagebox.setIcon(QtWidgets.QMessageBox.Question)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            result = messagebox.exec()
            if result == QtWidgets.QMessageBox.Yes:
                self.quicksaveDatenbank()
            elif result == QtWidgets.QMessageBox.Cancel:
                return True
        return False

    def closeEvent(self,event):
        if self.cancelDueToPendingChanges("Beenden"):
            event.ignore()
        else:
            Wolke.Settings["WindowSize-Datenbank"] = [self.form.size().width(), self.form.size().height()]
            if hasattr(self, "errorLogWindow"):
                self.errorLogWindow.form.close()
                self.errorLogWindow = None
            if hasattr(self, "editorHelpWindow"):
                self.editorHelpWindow.form.close()
                self.editorHelpWindow = None
            if hasattr(self, "scriptHelpWindow"):
                self.scriptHelpWindow.form.close()
                self.scriptHelpWindow = None
            self.onCloseCB()

    def onDatabaseChange(self):
        self.changed = True
        self.updateGUI()
    
    def updateWindowTitleAndCloseButton(self):
        splitpath = self.savepath and os.path.split(self.savepath) or ["keine Hausregeln geladen"]
        self.form.setWindowTitle(self.windowTitleDefault + " (" + splitpath[-1] + ")")
        self.ui.actionSchliessen.setEnabled(self.savepath != "" or self.changed)

    def updateFilter(self):
        statusses = [a.data() for a in self.statusFilterMenu.actions()[1:] if a.isChecked()]
        if len(statusses) > 0:
            self.ui.buttonStatusFilter.setText(f"{self.buttonStatusFilterText} <span style='color: green;'>({len(statusses)})</span>")
            self.statusFilterMenu.actions()[0].setVisible(True)
        else:
            statusses = [a.data() for a in self.statusFilterMenu.actions()[1:]]
            self.ui.buttonStatusFilter.setText(self.buttonStatusFilterText)
            self.statusFilterMenu.actions()[0].setVisible(False)

        filter = self.filters[self.ui.tabWidget.currentIndex()]
        filter.setFilters(self.ui.nameFilterEdit.text(), statusses, fullText=self.ui.checkFullText.isChecked())
        self.updateResultsLabel(filter)

    def updateResultsLabel(self, filter):
        self.ui.labelNumResults.setText(f"{filter.rowCount()}/{filter.sourceModel().rowCount()} Ergebnisse")

    def updateGUI(self):
        dbType = self.databaseTypesByIndex[self.ui.tabWidget.currentIndex()]
        tableView = self.lists[self.ui.tabWidget.currentIndex()]
        model = self.models[self.ui.tabWidget.currentIndex()]
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        prevScrollPos = tableView.verticalScrollBar().value()
        prevSelected = tableView.selectionModel().selectedIndexes()

        if self.ui.checkDetails.isChecked():
            tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        else:
            tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            tableView.verticalHeader().setDefaultSectionSize(Hilfsmethoden.emToPixels(3.4))
        
        tableView.selectionModel().blockSignals(True)
        prevSortCol = tableView.horizontalHeader().sortIndicatorSection()
        prevSortOrder = tableView.horizontalHeader().sortIndicatorOrder()
        model.clear()

        typeWrapper = self.databaseTypes[dbType]
        headerLabels = ["", "Name"]
        setColWidth = False
        if typeWrapper.showCategory:
            headerLabels.append("Kategorie")
            setColWidth = True
        if typeWrapper.showDetails:
            headerLabels.append("Details")
        model.setHorizontalHeaderLabels(headerLabels)
        tableView.setColumnWidth(0, Hilfsmethoden.emToPixels(2.5))
        tableView.setColumnWidth(1, Wolke.Settings['ColumnWidth-DBName' + dbType.__name__])
        if setColWidth:
            tableView.setColumnWidth(2, Wolke.Settings['ColumnWidth-DBTyp' + dbType.__name__])
        tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        tableView.horizontalHeader().setSectionResizeMode(len(headerLabels)-1, QtWidgets.QHeaderView.Stretch)
        tableView.sortByColumn(prevSortCol, prevSortOrder);

        table = list(self.datenbank.tablesByType[dbType].values())
        table.extend([self.datenbank.referenceDB[dbType][el] for el in self.datenbank.getRemoved(dbType)])
        for element in table:
            row = []
            iconItem = QtGui.QStandardItem()
            iconItem.setEditable(False)
            iconItem.setFont(Wolke.FontAwesomeFont)
            iconItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if self.datenbank.isRemoved(element):
                iconItem.setText("\uf068")
                iconItem.setForeground(QtGui.QBrush(QtCore.Qt.red))
                iconItem.setToolTip("<b>Gelöschtes</b> Original-Element.")
            elif self.datenbank.isNew(element):
                iconItem.setText("\u002b")
                iconItem.setForeground(QtGui.QBrush(QtCore.Qt.darkGreen))
                iconItem.setToolTip("<b>Hinzugefügtes</b> Element.")
            elif self.datenbank.isChanged(element):
                iconItem.setText('\uf044')
                iconItem.setForeground(QtGui.QBrush(QtCore.Qt.blue))
                iconItem.setToolTip("<b>Verändertes</b> Original-Element. Wenn du es löschst, erhältst du die Möglichkeit, die Original-Daten wiederherzustellen. Unten rechts hast du über den Original-Button die Möglichkeit diese anzusehen.")
            elif not self.datenbank.isOverriddenByOther(element):
                iconItem.setText("\uf02d")
                iconItem.setToolTip("<b>Unverändertes</b> Original-Element. Regeln wie sie im Buch stehen.")
            row.append(iconItem)

            nameItem = QtGui.QStandardItem(element.name)     
            nameItem.setData(element, QtCore.Qt.UserRole)
            nameItem.setEditable(False)
            row.append(nameItem)

            if typeWrapper.showCategory:
                kategorieText = element.kategorieName(self.datenbank)
                kategorieItem = QtGui.QStandardItem(kategorieText or "n/a")
                kategorieItem.setEditable(False)
                row.append(kategorieItem)

            if typeWrapper.showDetails:
                text = element.details(self.datenbank)
                if not self.ui.checkDetails.isChecked():
                    text = text.split("\n")[0]
                detailsItem = QtGui.QStandardItem(text)
                detailsItem.setEditable(False)
                row.append(detailsItem)

            model.appendRow(row)

        for itemIndex in prevSelected:
            row = itemIndex.row()
            tableView.selectionModel().select(filter.index(row, 0), QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        QtCore.QTimer.singleShot(0, lambda view=tableView, scrollPos=prevScrollPos: view.verticalScrollBar().setValue(scrollPos))

        tableView.selectionModel().blockSignals(False)
        self.listSelectionChanged()
        self.updateResultsLabel(filter)
               
    def wiederherstellen(self):
        model = self.models[self.ui.tabWidget.currentIndex()]
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        tableView = self.lists[self.ui.tabWidget.currentIndex()]

        for itm in tableView.selectedIndexes():
            element = model.itemFromIndex(filter.mapToSource(itm)).data(QtCore.Qt.UserRole)
            if element is None:
                continue
            table = self.datenbank.tablesByType[element.__class__]
            if element.name in table:
                messageBox = QtWidgets.QMessageBox()
                messageBox.setIcon(QtWidgets.QMessageBox.Question)
                messageBox.setWindowTitle("Geändertes Element zurücksetzen?")
                messageBox.setText(f"Bist du sicher, dass du die Original-Daten von {element.name} wiederherstellen möchtest? Damit gehen alle von dir gemachten Anderungen verloren.")   
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if messageBox.exec() == QtWidgets.QMessageBox.No:
                    continue
            elif not self.datenbank.isRemoved(element):
                continue
            table[element.name] = self.datenbank.referenceDB[element.__class__][element.name]

        self.onDatabaseChange();

    def vanillaAnsehen(self):
        model = self.models[self.ui.tabWidget.currentIndex()]
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        tableView = self.lists[self.ui.tabWidget.currentIndex()]

        for itm in tableView.selectedIndexes():
            element = model.itemFromIndex(filter.mapToSource(itm)).data(QtCore.Qt.UserRole)
            if element is None:
                continue
            if not self.datenbank.isChanged(element):
                continue
            table = self.datenbank.referenceDB[element.__class__]
            self.edit(table[element.name], True)
    
    def hinzufuegen(self):
        '''
        Lässt den Nutzer einen neuen Eintrag in die Datenbank einfügen.
        Öffnet zunächst den DatenbankSelectType-Dialog, welcher den 
        Nutzer fragt, was für ein Eintrag angelegt werden soll. 
        Akzeptiert der Nutzer, wird seiner Auswahl nach ein Dialog zum
        Erstellen des Eintrages geöffnet.
        '''
        dbType = self.databaseTypesByIndex[self.ui.tabWidget.currentIndex()]   
        val = self.databaseTypes[dbType].add(self.datenbank)
        if val is not None:
            self.datenbank.tablesByType[dbType][val.name] = val
            self.onDatabaseChange()

    def editSelected(self):
        tableView = self.lists[self.ui.tabWidget.currentIndex()]
        model = self.models[self.ui.tabWidget.currentIndex()]
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        databaseChanged = False
        for itm in tableView.selectedIndexes(): 
            element = model.itemFromIndex(filter.mapToSource(itm)).data(QtCore.Qt.UserRole)
            if element is None:
                continue
            if self.edit(element, True):
                databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()

    def edit(self, element, surpressChanges = False):
        if element is None:
            return False
        readonly = False
        if self.datenbank.isRemoved(element) or self.datenbank.isOverriddenByOther(element):
            readonly = True
        ret = self.databaseTypes[element.__class__].edit(self.datenbank, element, readonly)
        if ret is None:
            return False
        table = self.datenbank.tablesByType[element.__class__]
        if ret.name != element.name:
            table.pop(element.name)
        table[ret.name] = ret
        if not surpressChanges:
            self.onDatabaseChange()
        return True

    def duplicate(self, table, name):
        item = table[name]
        clone = copy(item)
        while clone.name in table:
            clone.name = clone.name + " (Kopie)"
        table[clone.name] = clone

    def duplicateSelected(self):
        tableView = self.lists[self.ui.tabWidget.currentIndex()]
        model = self.models[self.ui.tabWidget.currentIndex()]
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        databaseChanged = False
        for itm in tableView.selectedIndexes():
            element = model.itemFromIndex(filter.mapToSource(itm)).data(QtCore.Qt.UserRole)
            if element is None:
                continue
            table = self.datenbank.tablesByType[element.__class__]
            self.duplicate(table, element.name)
            databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
                                
    def deleteSelected(self):
        tableView = self.lists[self.ui.tabWidget.currentIndex()]
        model = self.models[self.ui.tabWidget.currentIndex()]
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        databaseChanged = False
        for itm in tableView.selectedIndexes():
            item = model.itemFromIndex(filter.mapToSource(itm))
            element = item.data(QtCore.Qt.UserRole)
            if element is None:
                continue
            table = self.datenbank.tablesByType[element.__class__]
            wasChanged = self.datenbank.isChanged(element)
            table.pop(element.name)
            if self.datenbank.isRemoved(element):
                autorestore = not self.databaseTypes[element.__class__].isDeletable
                if not autorestore and wasChanged:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setIcon(QtWidgets.QMessageBox.Question)
                    messageBox.setWindowTitle("Original-Daten wiederherstellen?")
                    messageBox.setText(f"Möchtest du die Original-Daten von {element.name} nach dem Löschen deiner Änderungen wiederherstellen?")            
                    messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    autorestore = messageBox.exec() == QtWidgets.QMessageBox.Yes
                if autorestore:
                    restoredElement = self.datenbank.referenceDB[element.__class__][element.name]
                    restoredElement.finalize(self.datenbank) #might not have been called if it was overriden
                    table[restoredElement.name] = restoredElement

            databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
 
    def saveDatenbank(self, merge = False):
        if os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            startDir = Wolke.Settings['Pfad-Regeln']
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Hausregeln speichern...",startDir,"XML-Datei (*.xml)")
        if spath == "":
            return
        spath = os.path.realpath(spath)
        if not spath.endswith(".xml"):
            spath = spath + ".xml"

        isInRulesPath = os.path.dirname(spath) == Wolke.Settings['Pfad-Regeln']
        if not isInRulesPath:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Question)
            infoBox.setText("Der Charakter-Editor kann nur Datenbanken aus dem in den Einstellungen gesetzten Pfad laden, sicher dass du die Datenbank hierhin speichern möchtest?")
            infoBox.setWindowTitle("Hausregeln speichern")
            yesButton = infoBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            otherButton = infoBox.addButton("Anderer Pfad", QtWidgets.QMessageBox.NoRole)
            cancelButton = infoBox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            infoBox.exec()
            if infoBox.clickedButton() == otherButton:
                self.saveDatenbank(merge)
                return
            elif infoBox.clickedButton() == cancelButton:
                return

        refDatabaseFile = os.getcwd() + os.path.normpath("/Data/datenbank.xml")
        if spath == refDatabaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Überschreiben der zentralen Datenbank verhindert!")
            infoBox.setInformativeText("Bitte schreibe deine eigenen Regeln nicht mit in die zentrale datenbank.xml - \
diese wird bei vielen Updates von Sephrasto verändert, wodurch du deine Regeln \
verlieren würdest. Stattdessen kannst du sie als separate Datei abspeichern und in den Einstellungen selektieren. \
Sie wird dann automatisch beim Programmstart mit geladen. Änderungen darin überschreiben \
die datenbank.xml, aber bleiben bei Updates erhalten!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()
            self.saveDatenbank(merge)
            return

        tmp = self.savepath
        self.savepath = spath
        self.quicksaveDatenbank(merge)
        if merge:
            self.savepath = tmp

        self.updateWindowTitleAndCloseButton()

        if not merge and isInRulesPath and Wolke.Settings['Datenbank'] != os.path.basename(spath):
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Question)
            infoBox.setText("Sollen die neuen Hausregeln in den Einstellungen aktiv gesetzt werden?")
            infoBox.setWindowTitle("Hausregeln aktiv setzen")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            result = infoBox.exec()
            if result == QtWidgets.QMessageBox.Yes:
                Wolke.Settings['Datenbank'] = os.path.basename(spath)
                EinstellungenWrapper.save()
        
    def quicksaveDatenbank(self, merge = False):
        prevText = self.ui.buttonQuicksave.text()
        prevShortcut = self.ui.buttonQuicksave.shortcut()
        self.ui.buttonQuicksave.setText("\uf254")
        QtWidgets.QApplication.processEvents()

        if not self.savepath:
            self.saveDatenbank(merge)
            self.ui.buttonQuicksave.setText(prevText)
            self.ui.buttonQuicksave.setShortcut(prevShortcut)
            return

        refDatabaseFile = os.getcwd() + os.path.normpath("/Data/datenbank.xml")
        if self.savepath == refDatabaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Überschreiben der zentralen Datenbank verhindert!")
            infoBox.setInformativeText("Bitte schreibe deine eigenen Regeln nicht mit in die zentrale datenbank.xml - \
diese wird bei vielen Updates von Sephrasto verändert, wodurch du deine Regeln \
verlieren würdest. Stattdessen kannst du sie als separate Datei abspeichern und in den Einstellungen selektieren. \
Sie wird dann automatisch beim Programmstart mit geladen. Änderungen darin überschreiben \
die datenbank.xml, aber bleiben bei Updates erhalten!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()
        else:
            # plugins may change their changesDatabase-flag depending on database settings, so update the enabled plugins here
            self.datenbank.enabledPlugins = self.getDatabaseChangingPlugins()
            self.datenbank.saveFile(self.savepath, merge)
            self.changed = False

        self.ui.buttonQuicksave.setText(prevText)
        self.ui.buttonQuicksave.setShortcut(prevShortcut)
    
    def closeDatenbank(self):
        if self.cancelDueToPendingChanges("Datenbank schließen"):
            return
        self.savepath = None
        self.datenbank.loadFile(hausregeln = None)
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.changed = False
        self.ui.actionZusaetzlichOeffnen.setEnabled(False)

        if hasattr(self, "errorLogWindow"):
            self.errorLogWindow.refresh()

    def reloadDatenbank(self):
        if self.cancelDueToPendingChanges("Datenbank schließen"):
            return
        self.datenbank.loadFile(hausregeln = self.datenbank.hausregelDatei)
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.changed = False

        if hasattr(self, "errorLogWindow"):
            self.errorLogWindow.refresh()

    def loadDatenbank(self, additiv = False):
        if self.cancelDueToPendingChanges("Andere Datenbank laden"):
            return

        if additiv and self.datenbank.hausregelDatei is not None:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Es sind bereits Hausregeln geladen. Wenn du zusätzlich noch andere Hausregeln lädst, werden beide zusammengefasst!\n" +
                            "Wenn in beiden Hausregeln die gleichen Datenbank-Elemente geändert wurden, wirst du dich zwischen einer Version entscheiden müssen - Sephrasto wird dir dabei helfen. " +
                            "Du kannst dies ohne Risiko ausprobieren: Die zusammengefassten Hausregeln werden erst gespeichert, wenn du den Speichern-Button drückst.\n" +
                            "In jedem Fall solltest du hinterher aber überprüfen, ob alle geänderten Elemente noch intakt sind. " +
                            "Beispielsweise könnten die zusätzlichen Hausregeln einen Vorteil gelöscht haben, der in den aktuellen Hausregeln irgendwo als Voraussetzung gelistet ist.")
            infoBox.setWindowTitle("Mehrere Hausregeln laden")
            cancelButton = infoBox.addButton("Abbrechen", QtWidgets.QMessageBox.NoRole)
            okButton = infoBox.addButton("Verstanden!", QtWidgets.QMessageBox.YesRole)
            infoBox.exec()
            if infoBox.clickedButton() == cancelButton:
                return

        if os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            startDir = Wolke.Settings['Pfad-Regeln']
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Hausregeln laden...",startDir,"XML-Datei (*.xml)")
        if not spath:
            return
        spath = os.path.realpath(spath)
        databaseFile = os.getcwd() + os.path.normpath("/Data/datenbank.xml")
        if spath == databaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Diese Funktion dient dem Laden einer Hausregel-Datenbank. Die zentrale Sephrasto-Datenbank 'database.xml' wird sowieso immer geladen!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()
            self.loadDatenbank(additiv)
            return

        if spath == self.datenbank.hausregelDatei:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Diese Hausregeln sind bereits geladen!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()
            self.loadDatenbank(additiv)
            return

        def conflictCB(typ, old, new):
            dialog = DatenbankMergeDialogWrapper.DatenbankMergeDialogWrapper(self.databaseTypes[typ], self.datenbank, old, new)
            return dialog.element

        if additiv:
            if not self.datenbank.loadFileAdditional(spath, conflictCB):
                self.showInvalidDatabasePopup(spath)
        else:
            if self.datenbank.loadFile(hausregeln=spath):
                self.savepath = spath
            else:
                self.savepath = None
                self.showInvalidDatabasePopup(spath)

        self.showDatabaseMigrationUpdatesPopup()

        if len(self.datenbank.loadingErrors) > 0:
            self.showErrorLog()
        
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.checkMissingPlugins()
        self.changed = False
        self.ui.actionZusaetzlichOeffnen.setEnabled(self.datenbank.hausregelDatei is not None)

    def showDatabaseMigrationUpdatesPopup(self):
        if len(Migrationen.hausregelUpdates) == 0:
            return
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowTitle("Hausregeln wurden aktualisiert")
        messageBox.setText(Migrationen.hausregelUpdates[0])
        if len(Migrationen.hausregelUpdates) > 1:
            messageBox.setInformativeText("Weitere Informationen:\n- " + "\n- ".join(Migrationen.hausregelUpdates[1:]))
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
        messageBox.exec()

    def showInvalidDatabasePopup(self, file):
        messagebox = QtWidgets.QMessageBox()
        messagebox.setWindowTitle("Fehler!")
        messagebox.setText(file + " ist keine valide Datenbank-Datei!")
        messagebox.setIcon(QtWidgets.QMessageBox.Critical)  
        messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messagebox.exec()

    def showErrorLog(self):
        if not hasattr(self, "errorLogWindow"):
            self.errorLogWindow = DatenbankErrorLogWrapper.DatenbankErrorLogWrapper(self.datenbank, lambda element: self.edit(element))
        else:
            self.errorLogWindow.refresh()
            self.errorLogWindow.form.show()
            self.errorLogWindow.form.activateWindow()

    def showCharakterAssistentErrorLog(self, baukasten):
        if not hasattr(self, "charakterAssistentErrorLog"):
            self.charakterAssistentErrorLog = WebEngineWrapper("Charakter Assistent Fehlerliste")
            self.charakterAssistentErrorLog.form.show()
        else:
            self.charakterAssistentErrorLog.form.show()
            self.charakterAssistentErrorLog.form.activateWindow()

        errors = "<br>".join(WizardWrapper.verify(self.datenbank, baukasten))
        if errors:
            self.charakterAssistentErrorLog.setHtml(errors)
        else:
            self.charakterAssistentErrorLog.setHtml("<b>Keine Fehler gefunden!</b>")

    def showEditorHelp(self):
        if not hasattr(self, "editorHelpWindow"):
            self.editorHelpWindow = WebEngineWrapper("Hilfe", "./Doc/datenbankeditor.html", Wolke.MkDocsCSS)
            self.editorHelpWindow.form.show()
        else:
            self.editorHelpWindow.form.show()
            self.editorHelpWindow.form.activateWindow()

    def showScriptHelp(self):
        if not hasattr(self, "scriptHelpWindow"):
            self.scriptHelpWindow = WebEngineWrapper("Hilfe", "./Doc/script_api.html", Wolke.MkDocsCSS)
            self.scriptHelpWindow.form.show()
        else:
            self.scriptHelpWindow.form.show()
            self.scriptHelpWindow.form.activateWindow()