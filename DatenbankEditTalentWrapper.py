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
        
        self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(talent.voraussetzungen, None))
        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)
        self.voraussetzungenEditStyleSheet = self.ui.voraussetzungenEdit.styleSheet()

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

    def voraussetzungenTextChanged(self):
        try:
            Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), self.datenbank)
            self.ui.voraussetzungenEdit.setStyleSheet(self.voraussetzungenEditStyleSheet)
            self.ui.voraussetzungenEdit.setToolTip("")
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        except VoraussetzungException as e:
            self.ui.voraussetzungenEdit.setStyleSheet("border: 1px solid red;")
            self.ui.voraussetzungenEdit.setToolTip(str(e))
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)