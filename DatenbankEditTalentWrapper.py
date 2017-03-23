# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:04:21 2017

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden
import DatenbankEditTalent
from PyQt5 import QtWidgets

class DatenbankEditTalentWrapper(object):
    def __init__(self, talent=None):
        super().__init__()
        if talent is None:
            talent = Fertigkeiten.Talent()
        talentDialog = QtWidgets.QDialog()
        ui = DatenbankEditTalent.Ui_talentDialog()
        ui.setupUi(talentDialog)
        ui.nameEdit.setText(talent.name)
        if talent.verbilligt:
            ui.buttonVerbilligt.setChecked(True)
        elif talent.kosten is not 0 and talent.kosten is not -1:
            ui.buttonSpezial.setChecked(True)
            ui.comboKosten.setCurrentText(str(talent.kosten) + " EP")
        else:
            ui.buttonRegulaer.setChecked(True)
        ui.fertigkeitenEdit.setText(Hilfsmethoden.FertArray2Str(talent.fertigkeiten, None))
        ui.voraussetzungenEdit.setText(Hilfsmethoden.VorArray2Str(talent.voraussetzungen, None))
        ui.textEdit.setPlainText(talent.text)
        talentDialog.show()
        ret = talentDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.talent = Fertigkeiten.Talent()
            self.talent.name = ui.nameEdit.text()
            self.talent.fertigkeiten = Hilfsmethoden.FertStr2Array(ui.fertigkeitenEdit.text(),None)
            self.talent.voraussetzungen = Hilfsmethoden.VorStr2Array(ui.voraussetzungenEdit.text(),None)
            self.talent.text = ui.textEdit.toPlainText()
            self.talent.kosten = -1
            if ui.buttonSpezial.isChecked():
                self.talent.kosten = int(ui.comboKosten.currentText()[:2])
                if self.talent.kosten not in [0,20,40,60,80]:
                    self.talent.kosten = int(ui.comboKosten.currentText()[:3])
            elif ui.buttonVerbilligt.isChecked():
                self.talent.verbilligt = 1
        else:
            self.talent = None
