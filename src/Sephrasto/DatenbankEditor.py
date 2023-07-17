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
import os
from EinstellungenWrapper import EinstellungenWrapper
from Wolke import Wolke
from copy import copy
import logging
from EventBus import EventBus
from HilfeWrapper import HilfeWrapper
from Hilfsmethoden import Hilfsmethoden
from QtUtils.RichTextButton import RichTextToolButton
from CharakterAssistent.WizardWrapper import WizardWrapper
from functools import partial

class DatenbankTypWrapper:
    def __init__(self, dataType, editorType, isDeletable):
        self.dataType = dataType
        self.editorType = editorType
        self.isDeletable = isDeletable
        self.isAddable = isDeletable
        self.showSubtype = hasattr(dataType, "typname")
        self.showDetails = hasattr(dataType, "details")

    def add(self, datenbank):
        return self.edit(datenbank, self.dataType())

    def edit(self, datenbank, inp, readonly = False):
        filterName = self.dataType.__name__.lower()
        editorType = EventBus.applyFilter("dbe_class_" + filterName + "_wrapper", self.editorType)
        editor = self.editorType(datenbank, inp, readonly)
        return editor.element

class DBESortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nameFilter = ""
        self.statusFilters = []

    def setFilters(self, nameFilter, statusFilters):
        self.nameFilter = nameFilter.lower()
        self.statusFilters = statusFilters
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        model = self.sourceModel()
        statusIndex = model.index(sourceRow, 0, sourceParent)
        status = model.data(statusIndex)
        nameIndex = model.index(sourceRow, 1, sourceParent)
        name = model.data(nameIndex).lower()
        return self.nameFilter in name and status in self.statusFilters

class DatenbankEditor(object):
    def __init__(self, plugins, onCloseCB):
        super().__init__()
        self.plugins = plugins
        self.onCloseCB = onCloseCB
        self.databaseTypes = {}
        self.datenbank = Datenbank(Wolke.Settings['Datenbank'])
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
            "Hilfe" : self.ui.menuHilfe
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

        self.ui.buttonStatusFilter = RichTextToolButton(None, 2*"&nbsp;" + "<span style='" + Wolke.FontAwesomeCSS + f"'>\uf0b0</span>&nbsp;&nbsp;Status-Filter" + 4*"&nbsp;")
        self.ui.buttonStatusFilter.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.ui.horizontalLayout_3.addWidget(self.ui.buttonStatusFilter)
        self.statusFilterMenu = QtWidgets.QMenu()
        for el in ["Alle", "Neu", "Geändert", "RAW", "Gelöscht"]:
            action = self.statusFilterMenu.addAction(el)
            action.setCheckable(True)
            action.setChecked(True)
            if el != "Alle":
                action.triggered.connect(self.updateFilter)

        self.statusFilterMenu.actions()[0].triggered.connect(self.filterAllToggled)
        self.ui.buttonStatusFilter.setMenu(self.statusFilterMenu)

        # Menu actions
        self.ui.actionOeffnen.triggered.connect(lambda: self.loadDatenbank())
        self.ui.actionZusaetzlichOeffnen.triggered.connect(lambda: self.loadDatenbank(True))
        self.ui.actionZusaetzlichOeffnen.setEnabled(self.datenbank.hausregelDatei is not None)
        self.ui.actionSpeichern.triggered.connect(self.quicksaveDatenbank)
        self.ui.actionSpeichern_unter.triggered.connect(self.saveDatenbank)
        self.ui.actionSchliessen.triggered.connect(self.closeDatenbank)
        self.ui.actionBeenden.triggered.connect(lambda: self.form.close())

        self.ui.actionFehlerliste.triggered.connect(self.showErrorLog)
        self.wizardWrapper = WizardWrapper()
        self.wizardActions = []
        for baukastenFolder in self.wizardWrapper.baukastenFolders:
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

        self.ui.buttonQuicksave.clicked.connect(self.quicksaveDatenbank)
        self.ui.buttonQuicksave.setText("\uf0c7")

        self.ui.buttonEditieren.clicked.connect(self.editSelected)
        self.ui.buttonEditieren.setEnabled(False)
        self.ui.buttonEditieren.setText("\uf044")

        self.ui.buttonDuplizieren.clicked.connect(self.duplicateSelected)
        self.ui.buttonDuplizieren.setEnabled(False)
        self.ui.buttonDuplizieren.setText("\uf24d")

        self.ui.buttonLoeschen.clicked.connect(self.deleteSelected)
        self.ui.buttonLoeschen.setEnabled(False)
        self.ui.buttonLoeschen.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
        self.ui.buttonLoeschen.setText("\uf2ed")

        self.ui.buttonHinzufuegen.clicked.connect(self.hinzufuegen)
        self.ui.buttonHinzufuegen.setText("\u002b")

        self.ui.buttonWiederherstellen.clicked.connect(self.wiederherstellen)
        self.ui.buttonWiederherstellen.setText("\uf829")

        self.ui.buttonRAW.clicked.connect(self.vanillaAnsehen)
        self.ui.buttonRAW.setText("\uf02d")

        self.ui.checkDetails.stateChanged.connect(self.onDetailsClicked)

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

        for dbType in sorted(self.databaseTypes, key = lambda t: t.displayName):
            self.databaseTypesByIndex.append(dbType)
            tableView = QtWidgets.QTableView()
            self.lists.append(tableView)
            model = QtGui.QStandardItemModel(tableView)
            self.models.append(model)

            filterProxy = DBESortFilterProxyModel()
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

    def onDetailsClicked(self):
        dbType = self.databaseTypesByIndex[self.ui.tabWidget.currentIndex()]
        typeWrapper = self.databaseTypes[dbType]
        if typeWrapper.showDetails:
            self.updateGUI()

    def filterAllToggled(self):
        checked = self.statusFilterMenu.actions()[0].isChecked()
        for a in self.statusFilterMenu.actions()[1:]:
            a.blockSignals(True)
            a.setChecked(checked)
            a.blockSignals(False)
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
        self.ui.buttonHinzufuegen.setEnabled(self.databaseTypes[dbType].isAddable)
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
            messagebox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            messagebox.addButton("Nein", QtWidgets.QMessageBox.NoRole)
            messagebox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            result = messagebox.exec()
            if result == 0:
                self.quicksaveDatenbank()
            elif result == 2:
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
        statusses = []
        if self.statusFilterMenu.actions()[1].isChecked():
            statusses.append("+")
        if self.statusFilterMenu.actions()[2].isChecked():
            statusses.append("\uf044")
        if self.statusFilterMenu.actions()[3].isChecked():
            statusses.append("\uf02d")
        if self.statusFilterMenu.actions()[4].isChecked():
            statusses.append("\uf068")
        if len(statusses) < 4:
            allAction = self.statusFilterMenu.actions()[0]
            allAction.blockSignals(True)
            allAction.setChecked(False)
            allAction.blockSignals(False)
    
        filter = self.filters[self.ui.tabWidget.currentIndex()]
        filter.setFilters(self.ui.nameFilterEdit.text(), statusses)

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
        if typeWrapper.showSubtype:
            headerLabels.append("Typ")
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
            iconItem.setFont(Wolke.FontAwesomeFont)
            iconItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if self.datenbank.isRemoved(element):
                iconItem.setText("\uf068")
                iconItem.setForeground(QtGui.QBrush(QtCore.Qt.red))
                iconItem.setToolTip("<b>Gelöschtes</b> RAW Element.")
            elif self.datenbank.isNew(element):
                iconItem.setText("\u002b")
                iconItem.setForeground(QtGui.QBrush(QtCore.Qt.darkGreen))
                iconItem.setToolTip("<b>Neues</b> Element.")
            elif self.datenbank.isChanged(element):
                iconItem.setText('\uf044')
                iconItem.setForeground(QtGui.QBrush(QtCore.Qt.blue))
                iconItem.setToolTip("<b>Geändertes</b> RAW Element. Wenn du es löschst, erhältst du die Möglichkeit, die RAW-Daten wiederherzustellen. Unten rechts hast du über den RAW-Button die Möglichkeit diese anzusehen.")
            elif not self.datenbank.isOverriddenByOther(element):
                iconItem.setText("\uf02d")
                iconItem.setToolTip("<b>RAW</b> Element. Regeln wie sie im Buch stehen.")
            row.append(iconItem)

            nameItem = QtGui.QStandardItem(element.name)     
            nameItem.setData(element, QtCore.Qt.UserRole)
            nameItem.setEditable(False)
            row.append(nameItem)

            if typeWrapper.showSubtype:
                subTypeText = element.typname(self.datenbank)
                subTypeItem = QtGui.QStandardItem(subTypeText or "n/a")
                subTypeItem.setEditable(False)
                row.append(subTypeItem)

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
                messageBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
                messageBox.addButton("Nein", QtWidgets.QMessageBox.RejectRole)
                if messageBox.exec() == 1:
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
                    messageBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
                    messageBox.addButton("Nein", QtWidgets.QMessageBox.RejectRole)
                    autorestore = messageBox.exec() == 0
                if autorestore:
                    restoredElement = self.datenbank.referenceDB[element.__class__][element.name]
                    restoredElement.finalize(self.datenbank) #might not have been called if it was overriden
                    table[restoredElement.name] = restoredElement

            databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
                              
    def saveDatenbank(self):
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
            infoBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            infoBox.addButton("Anderer Pfad", QtWidgets.QMessageBox.NoRole)
            infoBox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            result = infoBox.exec()
            if result == 1:
                self.saveDatenbank()
                return
            elif result == 2:
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
            self.saveDatenbank()
            return

        self.savepath = spath
        self.quicksaveDatenbank()
        self.updateWindowTitleAndCloseButton()

        if isInRulesPath and Wolke.Settings['Datenbank'] != os.path.basename(spath):
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Question)
            infoBox.setText("Sollen die neuen Hausregeln in den Einstellungen aktiv gesetzt werden?")
            infoBox.setWindowTitle("Hausregeln aktiv setzen")
            infoBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            infoBox.addButton("Nein", QtWidgets.QMessageBox.NoRole)
            result = infoBox.exec()
            if result == 0:
                Wolke.Settings['Datenbank'] = os.path.basename(spath)
                EinstellungenWrapper.save()
        
    def quicksaveDatenbank(self):
        if not self.savepath:
            self.saveDatenbank()
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
            self.datenbank.hausregelDatei = self.savepath
            self.datenbank.xmlSchreiben()
            self.changed = False
    
    def closeDatenbank(self):
        if self.cancelDueToPendingChanges("Datenbank schließen"):
            return
        self.datenbank.hausregelDatei = None
        self.savepath = None
        self.datenbank.xmlLaden()
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.changed = False
        self.ui.actionZusaetzlichOeffnen.setEnabled(False)

        if hasattr(self, "errorLogWindow"):
            self.errorLogWindow.refresh()

    RememberConflictResult = -1

    def loadDatenbank(self, additiv = False):
        if self.cancelDueToPendingChanges("Andere Datenbank laden"):
            return

        if not additiv:
            self.datenbank.hausregelDatei = None

        if self.datenbank.hausregelDatei is not None:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Es sind bereits Hausregeln geladen. Wenn du zusätzlich noch andere Hausregeln lädst, werden beide zusammengefasst!\n" +
                            "Wenn in beiden Hausregeln die gleichen Datenbank-Elemente geändert wurden, wirst du dich zwischen einer Version entscheiden müssen - Sephrasto wird dir dabei helfen. " +
                            "Du kannst dies ohne Risiko ausprobieren: Die zusammengefassten Hausregeln werden erst gespeichert, wenn du den Speichern-Button drückst.\n" +
                            "In jedem Fall solltest du hinterher aber überprüfen, ob alle geänderten Elemente noch intakt sind. " +
                            "Beispielsweise könnten die zusätzlichen Hausregeln einen Vorteil gelöscht haben, der in den aktuellen Hausregeln irgendwo als Voraussetzung gelistet ist.")
            infoBox.setWindowTitle("Mehrere Hausregeln laden")
            infoBox.addButton("Abbrechen", QtWidgets.QMessageBox.NoRole)
            infoBox.addButton("Verstanden!", QtWidgets.QMessageBox.YesRole)
            result = infoBox.exec()
            if result != 1:
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

        def showConflict(typ, old, new):
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Question)
            infoBox.setText(typ.displayName + " " + old.name + " wurde sowohl in den bestehenden, als auch in den neu geladenen Hausregeln geändert. Welche Version möchtest du beibehalten?")
            infoBox.setWindowTitle("Zusätzliche Hausregeln laden: Konflikt")

            infoBox.addButton("Aktuell ansehen", QtWidgets.QMessageBox.YesRole)
            infoBox.addButton("Neu ansehen", QtWidgets.QMessageBox.YesRole)
            infoBox.addButton("Aktuell auswählen", QtWidgets.QMessageBox.YesRole)
            infoBox.addButton("Neu auswählen", QtWidgets.QMessageBox.YesRole)
            check = QtWidgets.QCheckBox("Alle weiteren Konflikte gleich behandeln.")
            infoBox.setCheckBox(check)
            return (infoBox.exec(), infoBox.checkBox().isChecked())

        def conflictCB(typ, old, new):
            result = -1
            if DatenbankEditor.RememberConflictResult != -1:
                result = DatenbankEditor.RememberConflictResult

            while result < 2: 
                result, checked = showConflict(typ, old, new)
                if result < 2 and typ in self.databaseTypes:
                    databaseType = self.databaseTypes[typ]
                    databaseType.edit(self.datenbank, old if result == 0 else new, True)
                elif result >= 2 and checked:
                    DatenbankEditor.RememberConflictResult = result

            return old if result == 2 else new

        if self.datenbank.hausregelDatei is not None:
            DatenbankEditor.RememberConflictResult = -1
            self.datenbank.xmlLadenAdditiv(spath, conflictCB)
            DatenbankEditor.RememberConflictResult = -1
        else:
            self.savepath = spath
            self.datenbank.hausregelDatei = spath
            self.datenbank.xmlLaden()

        if len(self.datenbank.loadingErrors) > 0:
            self.showErrorLog()
        
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.checkMissingPlugins()
        self.changed = False
        self.ui.actionZusaetzlichOeffnen.setEnabled(self.datenbank.hausregelDatei is not None)

    def showErrorLog(self):
        if not hasattr(self, "errorLogWindow"):
            self.errorLogWindow = DatenbankErrorLogWrapper.DatenbankErrorLogWrapper(self.datenbank, lambda element: self.edit(element))
        else:
            self.errorLogWindow.refresh()
            self.errorLogWindow.form.show()
            self.errorLogWindow.form.activateWindow()

    def showCharakterAssistentErrorLog(self, baukasten):
        if not hasattr(self, "charakterAssistentErrorLog"):
            self.charakterAssistentErrorLog = HilfeWrapper(None, False)
            self.charakterAssistentErrorLog.form.show()
        else:
            self.charakterAssistentErrorLog.form.show()
            self.charakterAssistentErrorLog.form.activateWindow()

        self.charakterAssistentErrorLog.setTitle("Charakter Assistent Fehler (" + os.path.basename(baukasten) + ")")
        errors = "<br>".join(self.wizardWrapper.verify(self.datenbank, baukasten))
        if errors:
            self.charakterAssistentErrorLog.setText(errors)
        else:
            self.charakterAssistentErrorLog.setText("<b>Keine Fehler gefunden!</b>")

    def showEditorHelp(self):
        if not hasattr(self, "editorHelpWindow"):
            self.editorHelpWindow = HilfeWrapper("DatenbankEditor.md", False)
            self.editorHelpWindow.form.show()
        else:
            self.editorHelpWindow.form.show()
            self.editorHelpWindow.form.activateWindow()

    def showScriptHelp(self):
        if not hasattr(self, "scriptHelpWindow"):
            self.scriptHelpWindow = HilfeWrapper("ScriptAPI.md", False)
        else:
            self.scriptHelpWindow.form.show()
            self.scriptHelpWindow.form.activateWindow()