# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:33:21 2018

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, VoraussetzungenEditor
from Hilfsmethoden import Hilfsmethoden
import UI.DatenbankEditRegel
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
import re
from Core.Regel import Regel
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditRegelWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, regel=None, readonly=False):
        super().__init__()
        self.beschreibungEditor = BeschreibungEditor(self)
        self.voraussetzungenEditor = VoraussetzungenEditor(self)
        self.setupAndShow(datenbank, UI.DatenbankEditRegel.Ui_dialog(), Regel, regel, readonly)

    def load(self, regel):
        super().load(regel)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.voraussetzungenEditor.load(regel)
        self.beschreibungEditor.load(regel)
        self.ui.leProbe.setText(regel.probe)
        self.ui.comboTyp.clear()
        self.ui.comboTyp.addItems(self.datenbank.einstellungen["Regeln: Typen"].wert)
        self.ui.comboTyp.setCurrentIndex(regel.typ)

    def update(self, regel):
        super().update(regel)
        self.voraussetzungenEditor.update(regel)
        self.beschreibungEditor.update(regel)    
        regel.probe = self.ui.leProbe.text()
        regel.typ = self.ui.comboTyp.currentIndex()

    def nameChanged(self):
        super().nameChanged()
        name = self.ui.leName.text()
        if not self.validator["Name"] and name != self.elementPicked.name and name in self.datenbank.regeln:
            self.ui.leName.setToolTip(f"Name existiert bereits.\nVerwende am besten das Namensschema '{name} (M)', '{name} (L)',  '{name} (D)', '{name} (NK)' oder '{name} (FK)'.")

    def accept(self):
        text = self.ui.teBeschreibung.toPlainText()
        example = ""
        italic = ["Gegenprobe:", "Wirkung:", "Voraussetzung:", "Voraussetzungen:", "Besonderheit:", "Besonderheiten:", "Anmerkung:", "Anmerkungen:",
                  "Hohe Qualität:", "Probenschwierigkeit:", "Modifikationen:", "Dauer:", "Werkzeuge:", "Verbrauchsmaterialien:", "Haltbarkeit:",
                  "Talent:", "Talente:", "Unterstützung:"]
        italicPattern = re.compile("(?<!<i>)(" + "|".join(italic) + ")(?!</i>)")
        
        match = italicPattern.search(text)
        if match:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle("Formatierung der Beschreibung anpassen?")
            example = "\"" + match.group(0)[:-1] + "\", normalerweise kursiv"
            messageBox.setText("Die Beschreibung enthält Schlüsselwörter (z. B. " + example + "), die nicht wie üblich formatiert sind. Soll Sephrasto den Text automatisch anpassen?")
            messageBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            messageBox.addButton("Nein", QtWidgets.QMessageBox.RejectRole)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            result = messageBox.exec()
            if result == 0:
                text = italicPattern.sub(lambda m: "<i>" + m.group(0) + "</i>", text)
                self.ui.teBeschreibung.setPlainText(text)
                return

        super().accept()