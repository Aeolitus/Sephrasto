# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, VoraussetzungenEditor, ScriptEditor
from Core.Vorteil import VorteilDefinition, VorteilLinkKategorie
import UI.DatenbankEditVorteil
from Hilfsmethoden import Hilfsmethoden
from PySide6 import QtWidgets, QtCore, QtGui
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar
from ScriptPickerWrapper import ScriptPickerWrapper
from EventBus import EventBus

class DatenbankEditVorteilWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, vorteil=None):
        super().__init__(datenbank, UI.DatenbankEditVorteil.Ui_dialog(), VorteilDefinition, vorteil)
        self.validator["Querverweise"] = True
        self.beschreibungEditor = BeschreibungEditor(self)
        self.beschreibungRegelanhangEditor = BeschreibungEditor(self, "cheatsheetBeschreibung", "teCheatsheet", "tbCheatsheet", True)
        self.beschreibungBedingungenEditor = BeschreibungEditor(self, "bedingungen", "teBedingungen", "tbBedingungen")
        self.beschreibungInfoEditor = BeschreibungEditor(self, "info", "teInfo", "tbInfo")
        self.voraussetzungenEditor = VoraussetzungenEditor(self)
        self.scriptEditor = ScriptEditor(self, lineLimit=2)

    def onSetupUi(self):
        super().onSetupUi()
        self.ui.buttonPickScript.setText("\uf121")
        self.ui.buttonPickScript.clicked.connect(self.openScriptPicker)

    def load(self, vorteil):
        super().load(vorteil)
        self.htmlToolbar1 = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar1)
        self.htmlToolbar2 = HtmlToolbar(self.ui.teCheatsheet)
        self.ui.tab_2.layout().insertWidget(0, self.htmlToolbar2)
        self.htmlToolbar3 = HtmlToolbar(self.ui.teBedingungen)
        self.ui.tab_4.layout().insertWidget(0, self.htmlToolbar3)
        self.htmlToolbar4 = HtmlToolbar(self.ui.teInfo)
        self.ui.tab_5.layout().insertWidget(0, self.htmlToolbar4)

        self.voraussetzungenEditor.load(vorteil)
        self.beschreibungEditor.load(vorteil)
        self.beschreibungRegelanhangEditor.load(vorteil)
        self.beschreibungBedingungenEditor.load(vorteil)
        self.beschreibungInfoEditor.load(vorteil)

        self.ui.spinKosten.setValue(vorteil.kosten)
        self.ui.comboNachkauf.setCurrentText(vorteil.nachkauf)

        self.ui.comboTyp.addItems(self.datenbank.einstellungen["Vorteile: Kategorien"].wert.keyList)
        self.ui.comboTyp.setCurrentIndex(vorteil.kategorie)

        self.ui.checkVariable.setChecked(vorteil.variableKosten)
        self.ui.checkKommentar.setChecked(vorteil.kommentarErlauben)
        self.ui.checkScript.setChecked(vorteil.editorScriptErlauben)
        self.ui.checkVariable.clicked.connect(self.variableKostenChanged)
        self.variableKostenChanged()

        self.ui.checkCheatsheet.setChecked(vorteil.cheatsheetAuflisten)

        # Querverweise
        self.ui.buttonVerweisAdd.setText('\u002b')
        self.ui.buttonVerweisAdd.clicked.connect(self.addVerweis)
        self.ui.buttonVerweisDelete.setText('\uf2ed')
        self.ui.buttonVerweisDelete.clicked.connect(self.deleteVerweis)
        self.ui.buttonVerweisUp.setText('\uf106')
        self.ui.buttonVerweisUp.clicked.connect(self.moveVerweisUp)
        self.ui.buttonVerweisDown.setText('\uf078')
        self.ui.buttonVerweisDown.clicked.connect(self.moveVerweisDown)

        items = []
        for qv in vorteil.querverweise:
            splitted = qv.split(":")
            if len(splitted) == 1:
                items.append(splitted[0].strip())
            else:
                items.append(splitted[0].strip() + ": " + splitted[1].strip())

        self.ui.listVerweise.addItems(items)
        self.ui.listVerweise.model().rowsInserted.connect(self.querverweiseChanged)
        self.ui.listVerweise.model().rowsRemoved.connect(self.querverweiseChanged)
        self.querverweiseChanged()
        self.ui.comboVerweisTyp.currentIndexChanged.connect(self.verweisKategorieChanged)
        self.verweisKategorieChanged()

        # Verknüpfung
        self.ui.comboLinkKategorie.setCurrentIndex(vorteil.linkKategorie)
        self.ui.comboLinkKategorie.currentIndexChanged.connect(self.linkKategorieChanged)
        self.linkKategorieChanged()
        if vorteil.linkKategorie != VorteilLinkKategorie.NichtVerknüpfen:
            self.ui.comboLinkElement.setCurrentText(vorteil.linkElement)

        self.ui.spinScriptPrio.setValue(vorteil.scriptPrio)
        self.scriptEditor.load(vorteil)

        # Beschreibung Tabfarben
        self.ui.teBedingungen.textChanged.connect(self.updateBedingungenTabColor)
        self.updateBedingungenTabColor()

        self.ui.teCheatsheet.textChanged.connect(self.updateCheatsheetTabColor)
        self.updateCheatsheetTabColor()

        self.ui.teInfo.textChanged.connect(self.updateInfoTabColor)
        self.updateInfoTabColor()

        self.ui.comboVorschau.currentIndexChanged.connect(self.updateVorschau)
        self.updateVorschau()

    def update(self, vorteil):
        super().update(vorteil)
        self.voraussetzungenEditor.update(vorteil)
        self.beschreibungEditor.update(vorteil)
        self.beschreibungRegelanhangEditor.update(vorteil)
        self.beschreibungBedingungenEditor.update(vorteil)
        self.beschreibungInfoEditor.update(vorteil)
        vorteil.kosten = self.ui.spinKosten.value()
        vorteil.nachkauf = self.ui.comboNachkauf.currentText()
        vorteil.kategorie = self.ui.comboTyp.currentIndex()
        vorteil.variableKosten = self.ui.checkVariable.isChecked()
        vorteil.kommentarErlauben = self.ui.checkKommentar.isChecked()
        vorteil.editorScriptErlauben = self.ui.checkScript.isChecked()
        vorteil.scriptPrio = self.ui.spinScriptPrio.value()
        self.scriptEditor.update(vorteil)
        vorteil.cheatsheetAuflisten = self.ui.checkCheatsheet.isChecked()
        items = []
        for i in range(self.ui.listVerweise.count()):
            item = self.ui.listVerweise.item(i).text()
            splitted = item.split(":")
            if len(splitted) == 1:
                items.append(splitted[0].strip())
            else:
                items.append(splitted[0].strip() + ":" + splitted[1].strip())
        vorteil.querverweise = items
        vorteil.linkKategorie = self.ui.comboLinkKategorie.currentIndex()
        vorteil.linkElement = self.ui.comboLinkElement.currentText()

    def verweisKategorieChanged(self):
        self.ui.comboVerweis.clear()
        if self.ui.comboVerweisTyp.currentIndex() == 0: #regel
            self.ui.comboVerweis.addItems(sorted(self.datenbank.regeln.keys(), key=Hilfsmethoden.unicodeCaseInsensitive))
        elif self.ui.comboVerweisTyp.currentIndex() == 1: #talent
            self.ui.comboVerweis.addItems(sorted(self.datenbank.talente.keys(), key=Hilfsmethoden.unicodeCaseInsensitive))
        elif self.ui.comboVerweisTyp.currentIndex() == 2: #vorteil
            self.ui.comboVerweis.addItems(sorted([el for el in self.datenbank.vorteile if el != self.ui.leName.text()], key=Hilfsmethoden.unicodeCaseInsensitive))
        elif self.ui.comboVerweisTyp.currentIndex() == 3: #waffeneigenschaft
            self.ui.comboVerweis.addItems(sorted(self.datenbank.waffeneigenschaften.keys(), key=Hilfsmethoden.unicodeCaseInsensitive))
        elif self.ui.comboVerweisTyp.currentIndex() == 4: #abgeleiteter wert
            self.ui.comboVerweis.addItems(sorted(self.datenbank.abgeleiteteWerte.keys(), key=Hilfsmethoden.unicodeCaseInsensitive))
        elif self.ui.comboVerweisTyp.currentIndex() == 5: #statusse
            self.ui.comboVerweis.addItem("Statusse")
        elif self.ui.comboVerweisTyp.currentIndex() == 6: #finanzen
            self.ui.comboVerweis.addItem("Finanzen")

    def addVerweis(self):
        if self.ui.comboVerweisTyp.currentText() in ["Statusse", "Finanzen"]:
            self.ui.listVerweise.addItem(self.ui.comboVerweisTyp.currentText())
        else:
            self.ui.listVerweise.addItem(self.ui.comboVerweisTyp.currentText() + " : " + self.ui.comboVerweis.currentText())

    def deleteVerweis(self):
        self.ui.listVerweise.takeItem(self.ui.listVerweise.currentRow())

    def moveVerweisUp(self):
        currentRow = self.ui.listVerweise.currentRow()
        currentItem = self.ui.listVerweise.takeItem(currentRow)
        self.ui.listVerweise.insertItem(currentRow - 1, currentItem)
        self.ui.listVerweise.setCurrentRow(currentRow - 1)

    def moveVerweisDown(self):
        currentRow = self.ui.listVerweise.currentRow()
        currentItem = self.ui.listVerweise.takeItem(currentRow)
        self.ui.listVerweise.insertItem(currentRow + 1, currentItem)
        self.ui.listVerweise.setCurrentRow(currentRow + 1)

    def updateTabColor(self, text, index):
        if text:
            self.ui.tabWidget.tabBar().setTabTextColor(index, QtCore.Qt.darkGreen)
        else:
            palette = QtWidgets.QApplication.instance().palette()
            palette.setCurrentColorGroup(QtGui.QPalette.Disabled)
            self.ui.tabWidget.tabBar().setTabTextColor(index, palette.buttonText().color())

    def updateBedingungenTabColor(self):
        self.updateTabColor(self.ui.teBedingungen.toPlainText(), 1)

    def updateCheatsheetTabColor(self):
        self.updateTabColor(self.ui.teCheatsheet.toPlainText(), 2)

    def updateInfoTabColor(self):
        self.updateTabColor(self.ui.teInfo.toPlainText(), 3)
            
    def updateVorschau(self):
        self.ui.tbBeschreibung.setVisible(self.ui.comboVorschau.currentIndex() == 0)
        self.ui.tbBedingungen.setVisible(self.ui.comboVorschau.currentIndex() == 1)
        self.ui.tbCheatsheet.setVisible(self.ui.comboVorschau.currentIndex() == 2)
        self.ui.tbInfo.setVisible(self.ui.comboVorschau.currentIndex() == 3)
           
    def linkKategorieChanged(self):
        self.ui.comboLinkElement.clear()
        if self.ui.comboLinkKategorie.currentIndex() == VorteilLinkKategorie.Regel:
            self.ui.comboLinkElement.addItems(sorted(self.datenbank.regeln.keys(), key=Hilfsmethoden.unicodeCaseInsensitive))
        elif self.ui.comboLinkKategorie.currentIndex() == VorteilLinkKategorie.ÜberTalent:
            self.ui.comboLinkElement.addItems(sorted([el for el in self.datenbank.talente if self.datenbank.talente[el].spezialTalent], key=Hilfsmethoden.unicodeCaseInsensitive))
        elif self.ui.comboLinkKategorie.currentIndex() == VorteilLinkKategorie.Vorteil:
            self.ui.comboLinkElement.addItems(sorted([el for el in self.datenbank.vorteile if el != self.ui.leName.text()], key=Hilfsmethoden.unicodeCaseInsensitive))

    def variableKostenChanged(self):
        if self.ui.checkVariable.isChecked():
            self.ui.checkKommentar.setChecked(self.ui.checkVariable.isChecked())
        self.ui.checkKommentar.setEnabled(not self.ui.checkVariable.isChecked())

    def nameChanged(self):
        super().nameChanged()
        name = self.ui.leName.text()
        if self.validator["Name"] and Hilfsmethoden.containsWildcard(name):
            self.ui.leName.setToolTip("Name enthält ein nicht erlaubtes Zeichen: *?[]")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
            self.validator["Name"] = False
            self.updateSaveButtonState()

    def querverweiseChanged(self):
        rowHeight = max(self.ui.listVerweise.sizeHintForRow(0), 28) # can be -1
        contentHeight = rowHeight * max(self.ui.listVerweise.count(), 3) + 2 * self.ui.listVerweise.frameWidth()
        self.ui.listVerweise.setFixedHeight(contentHeight)

        error = ""
        for i in range(self.ui.listVerweise.count()):
            item = self.ui.listVerweise.item(i).text()
            splitted = item.split(":")
            if len(splitted) != 2:
                continue
            typ = splitted[0].strip()
            name = splitted[1].strip()

            if typ == "Regel":
                if name not in self.datenbank.regeln:
                    error = f"Kann Regel {name} nicht in der Datenbank finden."
                    break
            elif typ == "Vorteil":
                if name not in self.datenbank.vorteile:
                    error = f"Kann Vorteil {name} nicht in der Datenbank finden."
                    break
            elif typ == "Talent":
                if name not in self.datenbank.talente:
                    error = f"Kann Talent {name} nicht in der Datenbank finden."
                    break
            elif typ == "Waffeneigenschaft":
                if name not in self.datenbank.waffeneigenschaften:
                    error = f"Kann Waffeneigenschaft {name} nicht in der Datenbank finden."
                    break
            elif typ == "Abgeleiteter Wert":
                if name not in self.datenbank.abgeleiteteWerte:
                    error = f"Kann Abgeleiteten Wert {name} nicht in der Datenbank finden."
                    break

        if error:
            self.ui.listVerweise.setStyleSheet("border: 1px solid red;")
            self.ui.listVerweise.setToolTip(error)
            self.validator["Querverweise"] = False
        else:
            self.ui.listVerweise.setStyleSheet("")
            self.ui.listVerweise.setToolTip("")
            self.validator["Querverweise"] = True

        self.updateSaveButtonState()

    def openScriptPicker(self):
        pickerClass = EventBus.applyFilter("class_scriptpicker_wrapper", ScriptPickerWrapper)
        picker = pickerClass(self.datenbank, self.ui.teScript.toPlainText())
        if picker.script != None:
            self.ui.teScript.setPlainText(picker.script)