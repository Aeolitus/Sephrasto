# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Fertigkeiten
import DatenbankEditVorteil
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
from PyQt5 import QtWidgets, QtCore

class DatenbankEditVorteilWrapper(object):
    def __init__(self, datenbank, vorteil=None):
        super().__init__()
        self.datenbank = datenbank
        if vorteil is None:
            vorteil = Fertigkeiten.Vorteil()
        self.vorteilPicked = vorteil
        self.nameValid = True
        self.voraussetzungenValid = True
        vorteilDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditVorteil.Ui_talentDialog()
        self.ui.setupUi(vorteilDialog)
        
        if not vorteil.isUserAdded:
            self.ui.warning.setVisible(True)

        vorteilDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.nameEdit.setText(vorteil.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()
        self.ui.kostenEdit.setValue(vorteil.kosten)
        self.ui.comboNachkauf.setCurrentText(vorteil.nachkauf)
        self.ui.comboTyp.setCurrentIndex(vorteil.typ)

        self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(vorteil.voraussetzungen, None))
        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)

        self.ui.textEdit.setPlainText(vorteil.text)
        self.ui.checkVariable.setChecked(vorteil.variable!=-1)

        self.ui.scriptPrioEdit.setValue(vorteil.scriptPrio)

        scriptPrioDoc = [
            "Die Skript-Priorität legt die Reihenfolge der Auswertung fest. 0 ist Standard, negative Werte werden davor,",
            "positive Werte danach ausgewertet. Dies ist relevant, falls bspw. die INI verdoppelt werden soll nachdem",
            "Kampfreflexe eingerechnet wurde. In diesem Fall sollte die Skript-Priorität höher als die von Kampfreflexe sein."
        ]

        self.ui.scriptPrioEdit.setToolTip("\n".join(scriptPrioDoc))

        self.ui.scriptEdit.setText("; ".join(vorteil.script))

        scriptDocs = [
            "API:",
            "'get' Funktionen liefern den entsprechenden Wert zurück, die 'set' Funktionen setzen den Wert auf den übergebenen Ganzzahl-Parameter,",
            "und die 'modify' Funktionen verändern den gewünschten Wert um den übergebenen Ganzzahl-Parameter. Ausnahmen sind in spitzen Klammern aufgeführt.",
            "Skripte werden in Python geschrieben, wobei mehrere Funktionsaufrufe durch ein Semikolon getrennt werden.",
            "Das folgende Beispiel senkt die Wundschwelle um das Durchhaltevermögen +2: modifyWS(-(getDH() + 2))",
            "Die folgenden Funktionen stehen neben Python-Builtins wie 'round' zur Verfügung:",
            "AsP: getAsPBasis, setAsPBasis, modifyAsPBasis, getAsPMod, setAsPMod, modifyAsPMod",
            "KaP: getKaPBasis, setKaPBasis, modifyKaPBasis, getKaPMod, setKaPMod, modifyKaPMod",
            "SchiP: getSchiPMax, setSchiPMax, modifySchiPMax",
            "WS: getWSBasis, getWS, setWS, modifyWS",
            "MR: getMRBasis, getMR, setMR, modifyMR",
            "GS: getGSBasis, getGS, setGS, modifyGS",
            "DH: getDH, setDH, modifyDH",
            "Schadensbonus: getSchadensbonusBasis, getSchadensbonus, setSchadensbonus, modifySchadensbonus",
            "INI: getINIBasis, getINI, setINI, modifyINI",
            "RS: getRSMod, setRSMod, modifyRSMod",
            "BE: getBEBasis, getBEMod, setBEMod, modifyBEMod",
            "Kampfstile:",
            "  getKampfstil <Parameter: Kampfstil-Name. Return: Gibt ein Objekt zurück mit den folgenden Feldern: AT, VT, TP, RW, WM_LZ>",
            "                Beispiel: getKampfstil('Reiterkampf').TP",
            "  setKampfstil/modifyKampfstil <Parameter: Kampfstil-Name, AT, VT, TP, RW, WM_LZ>",
            "                Beispiel: modifyKampfstil('Reiterkampf', 1, 1, 1, 0, 0)",
            "  setKampfstilBEIgnore <Parameter: Kampfstil-Name, Fertigkeit-Name, Talent-Name>",
            "                Beispiel: setKampfstilBEIgnore('Reiterkampf', 'Athletik', 'Reiten'>",
            "Attribute: getAttribut <Parameter: Attribut-Name. Return: Wert des Attributes>",
            "                Beispiel: getAttribut('KO')",
            "Sonstiges: addWaffeneigenschaft <Parameter: WaffenName, Eigenschaft>",
            "                Beispiel: addWaffeneigenschaft('Waffenlos', 'Kopflastig')"
        ]

        self.ui.scriptEdit.setToolTip("\n".join(scriptDocs))

        vorteilDialog.show()
        ret = vorteilDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.vorteil = Fertigkeiten.Vorteil()
            self.vorteil.name = self.ui.nameEdit.text()
            self.vorteil.kosten = self.ui.kostenEdit.value()
            self.vorteil.nachkauf = self.ui.comboNachkauf.currentText()
            self.vorteil.voraussetzungen = Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), datenbank)
            self.vorteil.typ = self.ui.comboTyp.currentIndex()
            if self.ui.checkVariable.isChecked():
                self.vorteil.variable = 1
            else:
                self.vorteil.variable = -1
            self.vorteil.text = self.ui.textEdit.toPlainText()
            
            self.vorteil.scriptPrio = self.ui.scriptPrioEdit.value()
            self.vorteil.script = list(map(str.strip, self.ui.scriptEdit.text().split(";")))

            self.vorteil.isUserAdded = False
            if self.vorteil == self.vorteilPicked:
                self.vorteil = None
            else:
                self.vorteil.isUserAdded = True
        else:
            self.vorteil = None
           
    def nameChanged(self):
        name = self.ui.nameEdit.text()
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        elif name != self.vorteilPicked.name and name in self.datenbank.vorteile:
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
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.nameValid and self.voraussetzungenValid)