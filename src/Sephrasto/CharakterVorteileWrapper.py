# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:21:03 2017

@author: Aeolitus
"""
from Wolke import Wolke
import UI.CharakterVorteile
import CharakterMinderpaktWrapper
from PySide6 import QtWidgets, QtCore, QtGui
import logging
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden
from QtUtils.Section import Section
from QtUtils.AutoResizingTextBrowser import AutoResizingTextBrowser, TextEditAutoResizer
from QtUtils.TreeExpansionHelper import TreeExpansionHelper
from functools import partial
from Core.Vorteil import Vorteil
from VoraussetzungenListe import VoraussetzungenListe
from Hilfsmethoden import SortedCategoryToListDict
from QtUtils.RichTextButton import RichTextToolButton
from ScriptPickerWrapper import ScriptPickerWrapper
import copy

class CharakterVorteileWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self, supportedCategories = []):
        super().__init__()
        logging.debug("Initializing VorteileWrapper...")
        self.rowMargin = Hilfsmethoden.emToPixels(1)
        line = QtWidgets.QLineEdit()
        self.rowHeight = line.sizeHint().height()
        line.deleteLater()

        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterVorteile.Ui_Form()
        self.ui.setupUi(self.form)

        font = QtWidgets.QApplication.instance().font()
        self.ui.treeWidget.setProperty("class", "treeVorteile")
        self.ui.treeWidget.itemSelectionChanged.connect(self.vortClicked)
        self.ui.treeWidget.itemChanged.connect(self.itemChangeHandler)
        self.ui.treeWidget.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.ui.treeWidget.header().setSectionResizeMode(1,QtWidgets.QHeaderView.Fixed)
        self.ui.treeWidget.header().resizeSection(1, Hilfsmethoden.emToPixels(10))
        self.ui.treeWidget.header().setSectionResizeMode(2,QtWidgets.QHeaderView.Fixed)
        self.ui.treeWidget.header().resizeSection(2, Hilfsmethoden.emToPixels(3))

        self.expansionHelper = TreeExpansionHelper(self.ui.treeWidget, self.ui.buttonExpandToggle)

        self.autoResizeHelper = TextEditAutoResizer(self.ui.plainText)

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        if len(Wolke.Char.vorteile) > 0:
            self.currentVort = Wolke.Char.vorteile.__iter__().__next__()
        else:
            self.currentVort = Wolke.DB.vorteile.__iter__().__next__()

        self.itemWidgets = {}
        self.qvSlots = {}
        self.qvTexts = {}
        self.qvSections = {}

        # Set supported Vorteil Kategorien - all by default. This increases the reusability and might be useful for plugins.
        self.supportedCategories = supportedCategories
        if len(self.supportedCategories) == 0:
            for i in range(len(Wolke.DB.einstellungen["Vorteile: Kategorien"].wert)):
                self.supportedCategories.append(i)
        self.initVorteile()

        self.ui.labelFilter.setText("\uf002")
        self.ui.nameFilterEdit.setFocus()
        self.ui.nameFilterEdit.textChanged.connect(self.load)     
        self.shortcutSearch = QtGui.QAction()
        self.shortcutSearch.setShortcut("Ctrl+F")
        self.shortcutSearch.triggered.connect(self.ui.nameFilterEdit.setFocus)
        self.ui.nameFilterEdit.addAction(self.shortcutSearch)
        self.shortcutClearSearch = QtGui.QAction()
        self.shortcutClearSearch.setShortcut("Esc")
        self.shortcutClearSearch.triggered.connect(lambda: self.ui.nameFilterEdit.setText("") if self.ui.nameFilterEdit.hasFocus() else None)
        self.ui.nameFilterEdit.addAction(self.shortcutClearSearch)

        self.buttonFilterText = "<span style='" + Wolke.FontAwesomeCSS + f"'>\uf0b0</span>&nbsp;&nbsp;Filter"
        self.ui.buttonFilter = RichTextToolButton(None, self.buttonFilterText)
        self.ui.buttonFilter.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.ui.horizontalLayout.addWidget(self.ui.buttonFilter)
        self.filterMenu = QtWidgets.QMenu()
        action = self.filterMenu.addAction("Filter zurücksetzen")
        action.setVisible(False)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.resetFilter)

        action = self.filterMenu.addAction("Gekauft")
        action.setCheckable(True)
        action.setChecked(True)
        action.setShortcut("Ctrl+G")
        action.triggered.connect(self.load)

        action = self.filterMenu.addAction("Nicht gekauft")
        action.setCheckable(True)
        action.setChecked(True)
        action.setShortcut("Ctrl+N")
        action.triggered.connect(self.load)

        action = self.filterMenu.addAction("Voraussetzungen nicht erfüllt")
        action.setCheckable(True)
        action.setChecked(False)
        action.setShortcut(QtCore.QCoreApplication.tr("Ctrl+V"))
        action.triggered.connect(self.load)
        self.ui.buttonFilter.setMenu(self.filterMenu)

    def resetFilter(self):
        for action in self.filterMenu.actions():
            action.blockSignals(True)

        self.filterMenu.actions()[1].setChecked(True)
        self.filterMenu.actions()[2].setChecked(True)
        self.filterMenu.actions()[3].setChecked(False)

        for action in self.filterMenu.actions():
            action.blockSignals(False)
        self.load()

    def kosten(self, vorteil):
        if isinstance(vorteil, Vorteil):
            return vorteil.kosten
        else:
            return EventBus.applyFilter("vorteil_kosten", vorteil.kosten, { "charakter" : Wolke.Char, "vorteil" : vorteil.name })

    def initVorteile(self):
        self.ui.treeWidget.blockSignals(True)

        vorteileByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Vorteile: Kategorien"].wert)
        vorteileByKategorie.setCategoryFilter(self.supportedCategories)
        for vorteil in Wolke.DB.vorteile.values():
            vorteileByKategorie.append(vorteil.kategorie, vorteil.name)
        vorteileByKategorie.sortValues()

        for kategorie, vorteile in vorteileByKategorie.items():
            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            parent.setText(0, kategorie)
            parent.setText(1,"")
            parent.setExpanded(True)
            parent.setSizeHint(0, QtCore.QSize(0, self.rowHeight + self.rowMargin))
            font = parent.font(0)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            font.setPointSize(Wolke.FontHeadingSizeL3)
            parent.setFont(0, font)

            for el in vorteile:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, el)
                child.setSizeHint(0, QtCore.QSize(0, self.rowHeight + self.rowMargin))

                vorteil = Wolke.DB.vorteile[el]
                if el in Wolke.Char.vorteile:
                    vorteil = Wolke.Char.vorteile[el]
                    child.setCheckState(0, QtCore.Qt.Checked)

                if vorteil.variableKosten:
                    spin = QtWidgets.QSpinBox()
                    spin.setMinimum(-9999)
                    spin.setSuffix(" EP")
                    spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
                    spin.setMaximum(9999)
                    spin.setValue(self.kosten(vorteil))
                    spin.setReadOnly("Minderpakt" in Wolke.Char.vorteile and vorteil.name == Wolke.Char.vorteile["Minderpakt"].kommentar)
                    spin.setSingleStep(20)
                    self.itemWidgets[el] = spin
                    spin.valueChanged.connect(partial(self.spinnerChanged, name=vorteil.name))
                    self.ui.treeWidget.setItemWidget(child,1,spin)
                else:
                    child.setText(1, str(self.kosten(vorteil)) + " EP")

                favoriteButton = QtWidgets.QPushButton()
                font = favoriteButton.font()
                font.setHintingPreference(QtGui.QFont.PreferNoHinting)
                favoriteButton.setFont(font)
                favoriteButton.setText("\uf005")
                favoriteButton.setFlat(True)
                favoriteButton.clicked.connect(partial(self.markFavorite, name=vorteil.name))
                self.itemWidgets[el+"Favorite"] = favoriteButton
                self.updateFavoriteButton(el)
                self.ui.treeWidget.setItemWidget(child, 2, favoriteButton)

                if child.checkState(0) == QtCore.Qt.Checked:
                    self.handleAddSubwidgets(el, child)

        self.ui.treeWidget.blockSignals(False)

    def markFavorite(self, name):
        if name in Wolke.Char.vorteilFavoriten:
            Wolke.Char.vorteilFavoriten.remove(name)
        else:
            Wolke.Char.vorteilFavoriten.append(name)
        self.updateFavoriteButton(name)

    def updateFavoriteButton(self, name):
        # The full/empty star icons are unfortunatelly different fontawesome fonts
        button = self.itemWidgets[name+"Favorite"]
        if name in Wolke.Char.vorteilFavoriten:
            button.setProperty("class", "icon")
            button.setToolTip("Klicke, damit der Vorteil nicht mehr als Favorit markiert wird.")
        else:
            button.setProperty("class", "iconRegular")
            button.setToolTip("Klicke, damit der Vorteil als Favorit markiert wird.\nFavoriten werden unabhängig von den Filter-Einstellungen angezeigt.")

        button.style().unpolish(button)
        button.style().polish(button)
        
    def load(self):
        numFilters = sum([1 for a in self.filterMenu.actions()[1:] if a.isChecked()])

        if numFilters == 0:
            showPurchased = True
            showUnpurchased = True
            showUnvailable = True
            self.ui.buttonFilter.setText(self.buttonFilterText)
        else:
            showPurchased = self.filterMenu.actions()[1].isChecked()
            showUnpurchased = self.filterMenu.actions()[2].isChecked()
            showUnvailable = self.filterMenu.actions()[3].isChecked()
            self.ui.buttonFilter.setText(f"{self.buttonFilterText} <span style='color: {Wolke.ValidColor};'>({numFilters})</span>")
        self.filterMenu.actions()[0].setVisible(not(showPurchased and showUnpurchased and not showUnvailable))

        self.ui.treeWidget.blockSignals(True)

        vorteileByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Vorteile: Kategorien"].wert)
        vorteileByKategorie.setCategoryFilter(self.supportedCategories)
        for vorteil in Wolke.DB.vorteile.values():
            if vorteil.name in Wolke.Char.vorteile:
                vorteil = Wolke.Char.vorteile[vorteil.name]

            if Wolke.Char.voraussetzungenPrüfen(vorteil):
                vorteileByKategorie.append(vorteil.kategorie, vorteil.name)

        i = -1
        for vorteile in vorteileByKategorie.values():
            i += 1
            itm = self.ui.treeWidget.topLevelItem(i)
            if type(itm) != QtWidgets.QTreeWidgetItem:
                continue
            if itm == 0: 
                continue

            hasVisibleItems = False
            for j in range(itm.childCount()):
                chi = itm.child(j)
                if type(chi) != QtWidgets.QTreeWidgetItem:
                    continue
                vorteil = Wolke.DB.vorteile[chi.text(0)]

                isFiltered = self.ui.nameFilterEdit.text() != "" and \
                    (not self.ui.nameFilterEdit.text().lower() in vorteil.name.lower()) and \
                    (not self.ui.nameFilterEdit.text().lower() in itm.text(0).lower())

                if vorteil.name in Wolke.Char.vorteile:
                    vorteil = Wolke.Char.vorteile[vorteil.name]
                    chi.setCheckState(0, QtCore.Qt.Checked)
                    self.handleAddSubwidgets(vorteil.name, chi)
                    chi.setHidden(isFiltered or not showPurchased)
                else:
                    chi.setCheckState(0, QtCore.Qt.Unchecked)
                    # remove potential subwidgets (call doesnt do anything if it doesnt exist)
                    chi.takeChild(0)
                    # restore potential widget changes by minderpakt
                    if vorteil.name in self.itemWidgets:
                        self.itemWidgets[vorteil.name].setReadOnly(False)
                    chi.setHidden(isFiltered or not showUnpurchased)

                if vorteil.variableKosten:
                    self.itemWidgets[vorteil.name].setValue(self.kosten(vorteil))
                else:
                    chi.setText(1, str(self.kosten(vorteil)) + " EP")

                if vorteil.name not in vorteile:
                    if showUnvailable:
                        chi.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                        chi.setCheckState(0,QtCore.Qt.Unchecked)
                        chi.setForeground(0, QtGui.QBrush(QtGui.QColor(Wolke.ErrorColor)))
                        chi.setHidden(isFiltered)
                    else:
                        chi.setHidden(True)
                    Wolke.Char.removeVorteil(vorteil.name)
                else:
                    chi.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    chi.setForeground(0, QtGui.QBrush())

                if vorteil.name in Wolke.Char.vorteilFavoriten:
                    chi.setHidden(False)

                if not chi.isHidden():
                    hasVisibleItems = True

            itm.setHidden(not hasVisibleItems)

        self.updateInfo()
        self.ui.treeWidget.blockSignals(False)
        
    def update(self):
        pass

    def spinnerChanged(self, value, name):
        if name in Wolke.Char.vorteile and Wolke.Char.vorteile[name].variableKosten:
            Wolke.Char.vorteile[name].kosten = self.itemWidgets[name].value()
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

    def kommentarChanged(self, text, name):
        vorteil = Wolke.Char.vorteile[name]
        vorteil.kommentar = text
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()
        
    def editorScriptChanged(self, name, widget):
        vorteil = Wolke.Char.vorteile[name]      
        vorteil.editorScript = widget.toPlainText()
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

        if vorteil.editorScriptFault:
            widget.setProperty("error", True)
            widget.setToolTip(vorteil.editorScriptFault)
        else:
            widget.setProperty("error", False)
            widget.setToolTip("")
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def openScriptPicker(self, scriptEdit):
        pickerClass = EventBus.applyFilter("class_scriptpicker_wrapper", ScriptPickerWrapper)
        picker = pickerClass(Wolke.DB, scriptEdit.toPlainText())
        if picker.script != None:
            scriptEdit.setPlainText(picker.script)

    def handleAddSubwidgets(self, name, parent):
        if parent.childCount() > 0 or name not in Wolke.Char.vorteile:
            return
        vorteil = Wolke.Char.vorteile[name]

        if not (vorteil.kommentarErlauben or vorteil.editorScriptErlauben):
            return

        layout = QtWidgets.QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setFormAlignment(QtCore.Qt.AlignVCenter)
        rowHeight = 0
        if vorteil.kommentarErlauben:
            text = QtWidgets.QLineEdit(vorteil.kommentar)
            text.setReadOnly(name == "Minderpakt")
            text.setFixedHeight(self.rowHeight)
            layout.addRow("Kommentar", text)
            text.textChanged.connect(partial(self.kommentarChanged, name=name))
            rowHeight += self.rowHeight

        if vorteil.editorScriptErlauben:
            childLayout = QtWidgets.QHBoxLayout()
            text = QtWidgets.QPlainTextEdit(vorteil.editorScript)
            text.setFixedHeight(2 * self.rowHeight)
            text.textChanged.connect(partial(self.editorScriptChanged, name=name, widget=text))
            if vorteil.editorScriptFault:
                text.setProperty("error", True)
                text.style().unpolish(text)
                text.style().polish(text)
                text.setToolTip(vorteil.editorScriptFault)

            button = QtWidgets.QPushButton()
            button.setProperty("class", "iconSmall")
            button.setText("\uf121")
            font = button.font()
            font.setHintingPreference(QtGui.QFont.PreferNoHinting)
            button.setFont(font)
            button.setToolTip("Scripteditor öffnen")
            button.clicked.connect(partial(self.openScriptPicker, scriptEdit=text))
            childLayout.addWidget(text)
            childLayout.addWidget(button)
            layout.addRow("Script", childLayout)

            if rowHeight != 0:
                rowHeight += layout.verticalSpacing()
            rowHeight += 2 * self.rowHeight

        w = QtWidgets.QWidget()
        w.setLayout(layout)
        child = QtWidgets.QTreeWidgetItem(parent)

        child.setSizeHint(0, QtCore.QSize(0, rowHeight + self.rowMargin))
        self.ui.treeWidget.setItemWidget(child,0,w)
        parent.setExpanded(True)

    def handleAddMinderpakt(self, name, item):
        if name != "Minderpakt":
            return None
        mpWrapper = CharakterMinderpaktWrapper.CharakterMinderpaktWrapper()
        if mpWrapper.minderpakt is None:
            Wolke.Char.removeVorteil(name)
            return None

        if mpWrapper.minderpakt not in Wolke.Char.vorteile:
            if not self.checkConsequences(mpWrapper.minderpakt, True, True):
                Wolke.Char.removeVorteil(name)
                return None

            minderpakt = Wolke.Char.vorteile["Minderpakt"]
            minderpakt.kommentar = mpWrapper.minderpakt
            minderpakt.voraussetzungen = VoraussetzungenListe().compile("Vorteil " + minderpakt.kommentar, Wolke.DB)
            vorteil = Wolke.Char.addVorteil(minderpakt.kommentar)
            vorteil.voraussetzungen = VoraussetzungenListe().compile("Vorteil Minderpakt", Wolke.DB)
            vorteil.kosten = 20
           
            minderpaktWidget = self.ui.treeWidget.findItems(vorteil.name, QtCore.Qt.MatchRecursive)[0]

            if vorteil.name in self.itemWidgets:
                self.itemWidgets[vorteil.name].setReadOnly(True)
                self.itemWidgets[vorteil.name].setValue(20)
            else:
                minderpaktWidget.setText(1, "20 EP")
            return minderpaktWidget
        return None
    
    def itemChangeHandler(self, item, column):
        # Block Signals to make sure we dont repeat infinitely
        self.ui.treeWidget.blockSignals(True)
        name = item.text(0)
        self.currentVort = name
        self.updateInfo()
        cs = item.checkState(0)
        manualUpdate = None

        if cs == QtCore.Qt.Checked and name not in Wolke.Char.vorteile and name != "":
            if self.checkConsequences(name, True):
                Wolke.Char.addVorteil(name)
                manualUpdate = self.handleAddMinderpakt(name, item)
                self.handleAddSubwidgets(name, item)   
        elif cs != QtCore.Qt.Checked and name in Wolke.Char.vorteile:
            if self.checkConsequences(name, False):
                Wolke.Char.removeVorteil(name)

        self.modified.emit()
        self.load()
        self.ui.treeWidget.blockSignals(False)

        if manualUpdate:
           self.itemChangeHandler(manualUpdate, 0)
    
    def vortClicked(self):
        for el in self.ui.treeWidget.selectedItems():
            if el.text(0) in Wolke.DB.einstellungen["Vorteile: Kategorien"].wert:
                continue
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()

    def updateInfo(self):
        if self.currentVort != "":
            vorteil = Wolke.DB.vorteile[self.currentVort]
            if self.currentVort in Wolke.Char.vorteile:
                vorteil = Wolke.Char.vorteile[self.currentVort]
            self.ui.labelVorteil.setText(vorteil.name)
            self.ui.labelTyp.setText(vorteil.kategorieName(Wolke.DB))
            self.ui.labelNachkauf.setText(vorteil.nachkauf)
            voraussetzungen = vorteil.voraussetzungen.anzeigetext(Wolke.DB)
            self.ui.labelVoraussetzungen.setText(voraussetzungen)

            text = vorteil.text
            if vorteil.bedingungen:
                text = f"<i>Bedingungen</i>: {vorteil.bedingungen}\n\n" + text

            if vorteil.info:
                text += f"\n\n<b>Sephrasto</b>: {vorteil.info}"
            self.ui.plainText.setText(Hilfsmethoden.fixHtml(text))

            kosten = self.kosten(vorteil)
            if self.currentVort in Wolke.Char.vorteile:
                kosten = Wolke.Char.vorteile[self.currentVort].kosten
            self.ui.labelKosten.setText(str(kosten) + " EP")

            # delete old querverweise ui elements
            for qv in self.qvSlots:
                self.qvTexts[qv].sizeChanged.disconnect(self.qvSlots[qv]) #leaks otherwise
            self.qvSlots = {}
            self.qvTexts = {}
            self.qvSections = {}

            for i in reversed(range(self.ui.vlQuerverweise.count())):
                widget = self.ui.vlQuerverweise.itemAt(i).widget()
                widget.setParent(None)
                del widget

            # build new querverweise ui elements
            if len(vorteil.querverweise) > 0:
                header = QtWidgets.QLabel()
                header.setText("Querverweise:")
                self.ui.vlQuerverweise.addWidget(header)

            for qv in vorteil.querverweiseResolved:
                section = Section(qv)
                self.qvSections[qv] = section
                contentLayout = QtWidgets.QVBoxLayout()
                contentLayout.setContentsMargins(0, 0, 0, 0)
                qvText = AutoResizingTextBrowser()
                self.qvTexts[qv] = qvText
                qvText.setText(Hilfsmethoden.fixHtml(vorteil.querverweiseResolved[qv]))
                self.qvSlots[qv] = partial(self.updateSectionHeight, qv=qv)
                qvText.sizeChanged.connect(self.qvSlots[qv])
                contentLayout.addWidget(qvText)
                section.setContentLayout(contentLayout)
                self.ui.vlQuerverweise.addWidget(section)

    def updateSectionHeight(self, width, height, qv):
        self.qvSections[qv].updateHeight(height, True)


    def checkConsequences(self, vorteil, add = True, minderpakt = False):
        vorteile = copy.copy(Wolke.Char.vorteile)
        if add:
            vorteile[vorteil] = Vorteil(Wolke.DB.vorteile[vorteil], Wolke.Char)
            if minderpakt:
                vorteile[vorteil].voraussetzungen = VoraussetzungenListe().compile("Vorteil Minderpakt", Wolke.DB)
        else:
            vorteile.pop(vorteil)

        vorteile, talente = Wolke.Char.findUnerfüllteVoraussetzungen(vorteile=vorteile)
        if vorteile or talente:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Question)
            messageBox.setWindowTitle(vorteil + " " + ("kaufen" if add else "entfernen"))
            messageBox.setText("Wenn du " + vorteil + " " + ("kaufst" if add else "entfernst") + ", verlierst du:")

            vorteile = vorteile + talente[:3]
            talente = talente[3:]
            if len(talente) > 0:
                vorteile.append("... und " + str(len(talente)) + " weitere Talente")

            vorteile.append("\nBist du sicher?")
            messageBox.setInformativeText("\n".join(vorteile))
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
            result = messageBox.exec()
            return result == QtWidgets.QMessageBox.Yes
        return True