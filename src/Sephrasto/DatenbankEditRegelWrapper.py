# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:33:21 2018

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import UI.DatenbankEditRegel
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
import re

class DatenbankEditRegelWrapper(object):
    def __init__(self, datenbank, regel=None, readonly=False):
        super().__init__()
        self.datenbank = datenbank
        if regel is None:
            regel = Fertigkeiten.Regel()
        self.regelPicked = regel
        self.nameValid = True
        self.readonly = readonly
        self.voraussetzungenValid = True
        self.regelDialog = QtWidgets.QDialog()
        self.regelDialog.accept = lambda: self.accept()
        self.ui = UI.DatenbankEditRegel.Ui_regelDialog()
        self.ui.setupUi(self.regelDialog)

        if not regel.isUserAdded:
            if readonly:
                self.ui.warning.setText("Gelöschte Elemente können nicht verändert werden.")
            self.ui.warning.setVisible(True)

        self.regelDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setText("Speichern")
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Abbrechen")
        
        windowSize = Wolke.Settings["WindowSize-DBRegel"]
        self.regelDialog.resize(windowSize[0], windowSize[1])

        self.ui.nameEdit.setText(regel.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()
        self.ui.probeEdit.setText(regel.probe)
        self.ui.comboTyp.clear()
        self.ui.comboTyp.addItems(datenbank.einstellungen["Regeln: Typen"].toTextList())
        self.ui.comboTyp.setCurrentIndex(regel.typ)
        
        self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(regel.voraussetzungen, None))
        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)

        self.ui.textEdit.setPlainText(regel.text)
        self.regelDialog.show()
        ret = self.regelDialog.exec()

        Wolke.Settings["WindowSize-DBRegel"] = [self.regelDialog.size().width(), self.regelDialog.size().height()]

        if ret == QtWidgets.QDialog.Accepted:
            self.regel = Fertigkeiten.Regel()
            self.regel.name = self.ui.nameEdit.text()
            self.regel.probe = self.ui.probeEdit.text()
            self.regel.typ = self.ui.comboTyp.currentIndex()
            self.regel.voraussetzungen = Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), datenbank)
            self.regel.text = self.ui.textEdit.toPlainText()

            self.regel.isUserAdded = False
            if self.regel == self.regelPicked:
                self.regel = None
            else:
                self.regel.isUserAdded = True
        else:
            self.regel = None

    def nameChanged(self):
        name = self.ui.nameEdit.text()
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        elif name != self.regelPicked.name and name in self.datenbank.regeln:
            self.ui.nameEdit.setToolTip("Name existiert bereits.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        else:
            self.ui.nameEdit.setToolTip("")
            self.ui.nameEdit.setStyleSheet("")
            self.nameValid = True
        self.updateSaveButtonState()

    def voraussetzungenTextChanged(self):
        try:
            Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), self.datenbank)
            self.ui.voraussetzungenEdit.setStyleSheet("")
            self.ui.voraussetzungenEdit.setToolTip("")
            self.voraussetzungenValid = True
        except VoraussetzungException as e:
            self.ui.voraussetzungenEdit.setStyleSheet("border: 1px solid red;")
            self.ui.voraussetzungenEdit.setToolTip(str(e))
            self.voraussetzungenValid = False
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(not self.readonly and self.nameValid and self.voraussetzungenValid)

    def accept(self):
        text = self.ui.textEdit.toPlainText()
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
                self.ui.textEdit.setPlainText(text)
                return

        self.regelDialog.done(QtWidgets.QDialog.Accepted)