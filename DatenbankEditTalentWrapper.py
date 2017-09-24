# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:04:21 2017

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden
import DatenbankEditTalent
from PyQt5 import QtWidgets, QtCore

class DatenbankEditTalentWrapper(object):
    def __init__(self, talent=None):
        super().__init__()
        if talent is None:
            talent = Fertigkeiten.Talent()
        talentDialog = QtWidgets.QDialog()
        ui = DatenbankEditTalent.Ui_talentDialog()
        ui.setupUi(talentDialog)
        
        talentDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        ui.nameEdit.setText(talent.name)
        if talent.verbilligt:
            ui.buttonVerbilligt.setChecked(True)
        elif talent.kosten is not 0 and talent.kosten is not -1:
            ui.buttonSpezial.setChecked(True)
            ui.spinKosten.setValue(talent.kosten)
        else:
            ui.buttonRegulaer.setChecked(True)
        if talent.variable:
            ui.checkVariable.setChecked(True)
        else:
            ui.checkVariable.setChecked(False)
        ui.fertigkeitenEdit.setText(Hilfsmethoden.FertArray2Str(talent.fertigkeiten, None))
        ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(talent.voraussetzungen, None))
        ui.textEdit.setPlainText(talent.text)
        talentDialog.show()
        ret = talentDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.talent = Fertigkeiten.Talent()
            self.talent.name = ui.nameEdit.text()
            self.talent.fertigkeiten = Hilfsmethoden.FertStr2Array(ui.fertigkeitenEdit.text(),None)
            self.talent.voraussetzungen = Hilfsmethoden.VorStr2Array(ui.voraussetzungenEdit.toPlainText(),None)
            self.talent.text = ui.textEdit.toPlainText()
            self.talent.kosten = -1
            if ui.checkVariable.isChecked():
                self.talent.variable = 1
            else:
                self.talent.variable = -1
            if ui.buttonSpezial.isChecked():
                self.talent.kosten = ui.spinKosten.value()
            elif ui.buttonVerbilligt.isChecked():
                self.talent.verbilligt = 1
        else:
            self.talent = None
