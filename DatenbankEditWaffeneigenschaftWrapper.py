# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Objekte
import DatenbankEditWaffeneigenschaft
from PyQt5 import QtWidgets, QtCore

class DatenbankEditWaffeneigenschaftWrapper(object):
    def __init__(self, datenbank, waffeneigenschaft=None):
        super().__init__()
        self.datenbank = datenbank
        if waffeneigenschaft is None:
            waffeneigenschaft = Objekte.Waffeneigenschaft()
        self.waffeneigenschaftPicked = waffeneigenschaft
        self.nameValid = True
        waffeneigenschaftDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditWaffeneigenschaft.Ui_waffeneigenschaftDialog()
        self.ui.setupUi(waffeneigenschaftDialog)
        
        if not waffeneigenschaft.isUserAdded:
            self.ui.warning.setVisible(True)

        waffeneigenschaftDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.nameEdit.setText(waffeneigenschaft.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()

        self.ui.textEdit.setPlainText(waffeneigenschaft.text)
        self.ui.scriptPrioEdit.setValue(waffeneigenschaft.scriptPrio)

        scriptPrioDoc = [
            "Die Skript-Priorität legt die Reihenfolge der Auswertung fest. 0 ist Standard, negative Werte werden davor,",
            "positive Werte danach ausgewertet. Dies ist relevant, falls bspw. die INI verdoppelt werden soll nachdem",
            "Kampfreflexe eingerechnet wurde. In diesem Fall sollte die Skript-Priorität höher als die von Kampfreflexe sein."
        ]

        self.ui.scriptPrioEdit.setToolTip("\n".join(scriptPrioDoc))

        self.ui.scriptEdit.setText(waffeneigenschaft.script)

        scriptDocs = [
            "API:",
            "'get' Funktionen liefern den entsprechenden Wert zurück, die 'set' Funktionen setzen den Wert auf den übergebenen Ganzzahl-Parameter,",
            "und die 'modify' Funktionen verändern den gewünschten Wert um den übergebenen Ganzzahl-Parameter. Ausnahmen sind in spitzen Klammern aufgeführt.",
            "Skripte werden in Python geschrieben, wobei alles in eine Zeile geschrieben werden muss. Bei komplexeren Vorhaben am besten einen 'one-lined python converter' nutzen.",
            "Das folgende Beispiel senkt die Wundschwelle um das Durchhaltevermögen +2: modifyWS(-(getDH() + 2))",
            "Die folgenden Funktionen stehen neben Python-Builtins wie 'round' zur Verfügung:",
            "Parameter dieser Waffeneigenschaft als string erhalten: getEigenschaftParam <Parameter: Parameternummer>. Parameter müssen mit Semikolon getrennt werden.",
            "Waffen mit dieser Waffeneigenschaft modifizieren: modifyWaffeAT, modifyWaffeVT, modifyWaffeTPW6, modifyWaffeTPPlus",
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
            "Sonstiges: addWaffeneigenschaft <Parameter: TalentName, Eigenschaft>",
            "                Beispiel: addWaffeneigenschaft('Waffenlos', 'Kopflastig')"
        ]

        self.ui.scriptEdit.setToolTip("\n".join(scriptDocs))

        waffeneigenschaftDialog.show()
        ret = waffeneigenschaftDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.waffeneigenschaft = Objekte.Waffeneigenschaft()
            self.waffeneigenschaft.name = self.ui.nameEdit.text()
            self.waffeneigenschaft.text = self.ui.textEdit.toPlainText()

            self.waffeneigenschaft.scriptPrio = self.ui.scriptPrioEdit.value()
            self.waffeneigenschaft.script = str.strip(self.ui.scriptEdit.text())

            self.waffeneigenschaft.isUserAdded = False
            if self.waffeneigenschaft == self.waffeneigenschaftPicked:
                self.waffeneigenschaft = None
            else:
                self.waffeneigenschaft.isUserAdded = True
        else:
            self.waffeneigenschaft = None
           
    def nameChanged(self):
        name = self.ui.nameEdit.text()
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        elif name != self.waffeneigenschaftPicked.name and name in self.datenbank.waffeneigenschaften:
            self.ui.nameEdit.setToolTip("Name existiert bereits.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        else:
            self.ui.nameEdit.setToolTip("")
            self.ui.nameEdit.setStyleSheet("")
            self.nameValid = True
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.nameValid)