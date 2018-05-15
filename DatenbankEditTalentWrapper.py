# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:04:21 2017

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import DatenbankEditTalent
from PyQt5 import QtWidgets, QtCore

class DatenbankEditTalentWrapper(object):
    def __init__(self, datenbank, talent=None):
        super().__init__()
        self.datenbank = datenbank
        if talent is None:
            talent = Fertigkeiten.Talent()
        self.talentPicked = talent
        self.nameValid = True
        self.voraussetzungenValid = True
        self.fertigkeitenValid = True
        talentDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditTalent.Ui_talentDialog()
        self.ui.setupUi(talentDialog)

        if not talent.isUserAdded:
            self.ui.warning.setVisible(True)

        talentDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.nameEdit.setText(talent.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()
        if talent.verbilligt:
            self.ui.buttonVerbilligt.setChecked(True)
        elif talent.kosten is not 0 and talent.kosten is not -1:
            self.ui.buttonSpezial.setChecked(True)
            self.ui.spinKosten.setValue(talent.kosten)
        else:
            self.ui.buttonRegulaer.setChecked(True)
        if talent.variable != -1:
            self.ui.checkVariable.setChecked(True)
        else:
            self.ui.checkVariable.setChecked(False)
        self.ui.fertigkeitenEdit.setText(Hilfsmethoden.FertArray2Str(talent.fertigkeiten, None))
        self.ui.fertigkeitenEdit.textChanged.connect(self.fertigkeitenTextChanged)
        
        self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(talent.voraussetzungen, None))
        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)

        self.ui.textEdit.setPlainText(talent.text)
        talentDialog.show()
        ret = talentDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.talent = Fertigkeiten.Talent()
            self.talent.name = self.ui.nameEdit.text()
            self.talent.fertigkeiten = Hilfsmethoden.FertStr2Array(self.ui.fertigkeitenEdit.text(),None)
            self.talent.voraussetzungen = Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), datenbank)
            self.talent.text = self.ui.textEdit.toPlainText()
            self.talent.kosten = -1
            if self.ui.checkVariable.isChecked():
                self.talent.variable = 1
            else:
                self.talent.variable = -1
            if self.ui.buttonSpezial.isChecked():
                self.talent.kosten = self.ui.spinKosten.value()
            elif self.ui.buttonVerbilligt.isChecked():
                self.talent.verbilligt = 1
        else:
            self.talent = None

    def nameChanged(self):
        name = self.ui.nameEdit.text()
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        elif name != self.talentPicked.name and name in self.datenbank.talente:
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

    def fertigkeitenTextChanged(self):
        fertigkeiten = Hilfsmethoden.FertStr2Array(self.ui.fertigkeitenEdit.text(),None)
        self.fertigkeitenValid = True
        for fertigkeit in fertigkeiten:
            if not fertigkeit in self.datenbank.fertigkeiten and not fertigkeit in self.datenbank.übernatürlicheFertigkeiten:
                self.ui.fertigkeitenEdit.setStyleSheet("border: 1px solid red;")
                self.ui.fertigkeitenEdit.setToolTip("Unbekannte Fertigkeit '" + fertigkeit + "'")
                self.fertigkeitenValid = False
                break
        if self.fertigkeitenValid:
            self.ui.fertigkeitenEdit.setStyleSheet("")
            self.ui.fertigkeitenEdit.setToolTip("")
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.nameValid and self.voraussetzungenValid and self.fertigkeitenValid)