# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:04:21 2017

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, VoraussetzungenEditor
from Hilfsmethoden import Hilfsmethoden
import UI.DatenbankEditTalent
from PySide6 import QtWidgets, QtCore, QtGui
from QtUtils.TextTagCompleter import TextTagCompleter
from Wolke import Wolke
import re
from Core.Talent import TalentDefinition
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditTalentWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, talent=None):
        super().__init__(datenbank, UI.DatenbankEditTalent.Ui_dialog(), TalentDefinition, talent)
        self.beschreibungEditor = BeschreibungEditor(self, "textSerialized")
        self.beschreibungInfoEditor = BeschreibungEditor(self, "info", "teInfo", "tbInfo")
        self.voraussetzungenEditor = VoraussetzungenEditor(self)
        self.validator["Fertigkeiten"] = True

    def onSetupUi(self):
        super().onSetupUi()

        ui = self.ui
        self.registerInput(ui.leName, ui.labelName)
        self.registerInput(ui.comboKategorie, ui.labelKategorie)
        self.registerInput(ui.checkVerbilligt, ui.labelKategorie)
        self.registerInput(ui.spinKosten, ui.labelKategorie)
        self.registerInput(ui.checkVariable, ui.labelVariable)
        self.registerInput(ui.checkKommentar, ui.labelKommentar)
        self.registerInput(ui.checkCheatsheet, ui.labelCheatsheet)
        self.registerInput(ui.leFertigkeiten, ui.labelFertigkeiten)
        self.registerInput(ui.teVoraussetzungen, ui.labelVoraussetzungen)
        self.registerInput(ui.teBeschreibung, ui.labelBeschreibung)
        self.registerInput(ui.teInfo, ui.labelBeschreibung)
        self.registerInput(ui.comboSeite, ui.labelSeite)
        self.registerInput(ui.spinSeite, ui.labelSeite)

    def load(self, talent):
        super().load(talent)
        self.htmlToolbar1 = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar1)
        self.htmlToolbar2 = HtmlToolbar(self.ui.teInfo)
        self.ui.tab_3.layout().insertWidget(0, self.htmlToolbar2)
        self.voraussetzungenEditor.load(talent)
        self.beschreibungEditor.load(talent)
        self.beschreibungInfoEditor.load(talent)

        self.ui.comboKategorie.addItems(self.datenbank.einstellungen["Talente: Kategorien"].wert.keyList)
        self.ui.comboKategorie.setCurrentIndex(talent.kategorie)
        self.ui.comboKategorie.currentIndexChanged.connect(self.kostenChanged)
        self.ui.spinKosten.setValue(talent.kosten)
        self.ui.checkCheatsheet.setChecked(talent.cheatsheetAuflisten)
        self.ui.checkVerbilligt.setChecked(talent.verbilligt)
        self.ui.checkVariable.setChecked(talent.variableKosten)
        self.ui.checkKommentar.setChecked(talent.kommentarErlauben)

        self.fertigkeitenCompleter = TextTagCompleter(self.ui.leFertigkeiten, [])
        self.ui.leFertigkeiten.setText(Hilfsmethoden.FertArray2Str(talent.fertigkeiten, None))
        self.ui.leFertigkeiten.textChanged.connect(self.fertigkeitenTextChanged)
        
        self.kostenChanged()

        self.ui.checkVariable.clicked.connect(self.variableKostenCheckChanged)
        self.variableKostenCheckChanged()

        bücher = self.datenbank.einstellungen["Referenzbücher"].wert
        if (len(bücher) > 0):
            self.ui.comboSeite.addItems(bücher)
            self.ui.comboSeite.setCurrentIndex(talent.referenzBuch)
        self.ui.spinSeite.setValue(talent.referenzSeite)

        self.ui.teInfo.textChanged.connect(self.updateInfoTabColor)
        self.updateInfoTabColor()

        self.ui.comboVorschau.currentIndexChanged.connect(self.updateVorschau)
        self.updateVorschau()

    def updateInfoTabColor(self):
        if self.ui.teInfo.toPlainText():
            self.ui.tabWidget.tabBar().setTabTextColor(1, QtCore.Qt.darkGreen)
        else:
            palette = QtWidgets.QApplication.instance().palette()
            palette.setCurrentColorGroup(QtGui.QPalette.Disabled)
            self.ui.tabWidget.tabBar().setTabTextColor(1, palette.buttonText().color())

    def updateVorschau(self):
        self.ui.tbBeschreibung.setVisible(self.ui.comboVorschau.currentIndex() == 0)
        self.ui.tbInfo.setVisible(self.ui.comboVorschau.currentIndex() == 1)

    def update(self, talent):
        super().update(talent)
        self.voraussetzungenEditor.update(talent)
        self.beschreibungEditor.update(talent)
        self.beschreibungInfoEditor.update(talent)
        talent.kategorie = self.ui.comboKategorie.currentIndex()
        talent.kommentarErlauben = self.ui.checkKommentar.isChecked()
        talent.variableKosten = self.ui.checkVariable.isChecked()
        talent.kosten = self.ui.spinKosten.value()
        talent.verbilligt = self.ui.checkVerbilligt.isChecked()
        talent.fertigkeiten = Hilfsmethoden.FertStr2Array(self.ui.leFertigkeiten.text(),None)
        talent.cheatsheetAuflisten = self.ui.checkCheatsheet.isChecked()
        talent.referenzBuch = self.ui.comboSeite.currentIndex()
        talent.referenzSeite = self.ui.spinSeite.value()

    def kostenChanged(self):
        isSpezial = self.ui.comboKategorie.currentIndex() > 0
        self.ui.spinKosten.setVisible(isSpezial)
        self.ui.checkVerbilligt.setVisible(not isSpezial)
        
        wasEnabled = self.ui.checkCheatsheet.isEnabled()
        self.ui.checkCheatsheet.setEnabled(isSpezial)
        if not wasEnabled and isSpezial:
            self.ui.checkCheatsheet.setChecked(True)
        elif not isSpezial:
            self.ui.checkCheatsheet.setChecked(False)

        if isSpezial:
            self.fertigkeitenCompleter.setTags([f for f in self.datenbank.übernatürlicheFertigkeiten.keys()])
        else:
            self.fertigkeitenCompleter.setTags([f for f in self.datenbank.fertigkeiten.keys()])
        self.fertigkeitenTextChanged()

    def variableKostenCheckChanged(self):
        if self.ui.checkVariable.isChecked():
            self.ui.checkKommentar.setChecked(self.ui.checkVariable.isChecked())
        self.ui.checkKommentar.setEnabled(not self.ui.checkVariable.isChecked())

    def nameChanged(self):
        super().nameChanged()
        name = self.ui.leName.text()
        fertigkeiten = Hilfsmethoden.FertStr2Array(self.ui.leFertigkeiten.text(),None)
        if not self.validator["Name"] and name != self.elementPicked.name and name in self.datenbank.talente:
            self.ui.leName.setToolTip(f"Name existiert bereits.\nVerwende am besten das Namensschema 'Fertigkeit: {name}'.")
        elif self.validator["Name"] and "Gebräuche" in fertigkeiten and not name.startswith("Gebräuche: "):
            self.ui.leName.setToolTip("Talentnamen für die Fertigkeit Gebräuche müssen mit 'Gebräuche: ' anfangen.")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
            self.validator["Name"] = False
            self.updateSaveButtonState()

    def fertigkeitenTextChanged(self):
        fertigkeiten = Hilfsmethoden.FertStr2Array(self.ui.leFertigkeiten.text(),None)
        self.validator["Fertigkeiten"] = True
        for fertigkeit in fertigkeiten:
            isSpezial = self.ui.comboKategorie.currentIndex() > 0
            if isSpezial:
                if not fertigkeit in self.datenbank.übernatürlicheFertigkeiten:
                    self.ui.leFertigkeiten.setStyleSheet("border: 1px solid red;")
                    self.ui.leFertigkeiten.setToolTip("Unbekannte übernatürliche Fertigkeit '" + fertigkeit + "'. Spezialtalente müssen übernatürlichen Fertigkeiten zugewiesen werden.")
                    self.validator["Fertigkeiten"] = False
                    break
            else:
                if not fertigkeit in self.datenbank.fertigkeiten:
                    self.ui.leFertigkeiten.setStyleSheet("border: 1px solid red;")
                    self.ui.leFertigkeiten.setToolTip("Unbekannte profane Fertigkeit '" + fertigkeit + "'. Reguläre Talente müssen profanen Fertigkeiten zugewiesen werden.")
                    self.validator["Fertigkeiten"] = False
                    break

        if self.validator["Fertigkeiten"]:
            self.ui.leFertigkeiten.setStyleSheet("")
            self.ui.leFertigkeiten.setToolTip("")
        self.nameChanged()

    def accept(self):
        text = self.ui.teBeschreibung.toPlainText()
        example = ""
        bold = ["Mächtige Magie:", "Mächtige Liturgie:", "Mächtige Anrufung:", "Probenschwierigkeit:", "Modifikationen:", "Vorbereitungszeit:",
                "Ziel:", "Reichweite:", "Wirkungsdauer:", "Kosten:", "Fertigkeiten:", "Erlernen:", "Anmerkung:", "Fertigkeit Eis:",
                "Fertigkeit Erz:", "Fertigkeit Feuer:", "Fertigkeit Humus:", "Fertigkeit Luft:", "Fertigkeit Wasser:"]
        boldPattern = re.compile("(?<!<b>)(" + "|".join(bold) + ")(?!</b>)")
        italic = ["Konterprobe", "Aufrechterhalten", "Ballistischer", "Ballistische", "Erfrieren", "Niederschmettern", "Nachbrennen", "Fesseln", "Zurückstoßen", "Ertränken", "Konzentration", "Objektritual", "Objektrituale"]
        italicPattern = re.compile("(?<!<i>)(" + "|".join(italic) + ")(?!</i>)")
        illusionPattern = re.compile("(?<!<i>)Illusion \((Sicht|Gehör|Geruch|Geschmack|Tast)")

        match = boldPattern.search(text)
        if match:
            example = "\"" + match.group(0)[:-1] + "\", normalerweise fett"
        if not match:
            match = italicPattern.search(text)
            if match:
                example = "\"" + match.group(0) + "\", normalerweise kursiv"
        if not match:
            match = illusionPattern.search(text)
            if match:
                example = "Illusion, normalerweise kursiv"

        if match:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle("Formatierung der Beschreibung anpassen?")
            messageBox.setText("Die Beschreibung enthält Schlüsselwörter (z. B. " + example + "), die nicht wie üblich formatiert sind. Soll Sephrasto den Text automatisch anpassen?")
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            result = messageBox.exec()
            if result == QtWidgets.QMessageBox.Yes:
                text = boldPattern.sub(lambda m: "<b>" + m.group(0) + "</b>", text)
                text = italicPattern.sub(lambda m: "<i>" + m.group(0) + "</i>", text)
                text = illusionPattern.sub(lambda m: m.group(0).replace("Illusion", "<i>Illusion</i>"), text)
                self.ui.teBeschreibung.setPlainText(text)
                return

        super().accept()