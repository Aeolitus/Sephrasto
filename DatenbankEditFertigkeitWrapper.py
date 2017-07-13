# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:21:32 2017

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden
import DatenbankEditFertigkeit
from PyQt5 import QtWidgets, QtCore

class DatenbankEditFertigkeitWrapper(object):
    def __init__(self, fertigkeit=None, ueber=False):
        super().__init__()
        if fertigkeit is None:
            fertigkeit = Fertigkeiten.Fertigkeit()
        fertDialog = QtWidgets.QDialog()
        ui = DatenbankEditFertigkeit.Ui_talentDialog()
        ui.setupUi(fertDialog)
        
        fertDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        ui.nameEdit.setText(fertigkeit.name)
        ui.steigerungsfaktorEdit.setValue(fertigkeit.steigerungsfaktor)
        ui.comboAttribut1.setCurrentText(fertigkeit.attribute[0])
        ui.comboAttribut2.setCurrentText(fertigkeit.attribute[1])
        ui.comboAttribut3.setCurrentText(fertigkeit.attribute[2])
        if ueber:
            ui.voraussetzungenEdit.setText(Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen, None))
            ui.radioUebernatuerlich.setChecked(True)
            ui.radioProfan.setCheckable(False)
            ui.checkKampffertigkeit.setCheckable(False)
        else:
            ui.voraussetzungenEdit.setText(" - ")
            ui.voraussetzungenEdit.setReadOnly(True)
            ui.radioProfan.setChecked(True)
            ui.radioUebernatuerlich.setCheckable(False)
            if fertigkeit.kampffertigkeit == 1:
                ui.checkKampffertigkeit.setChecked(True)
        ui.textEdit.setPlainText(fertigkeit.text)
        fertDialog.show()
        ret = fertDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.fertigkeit = Fertigkeiten.Fertigkeit()
            self.fertigkeit.name = ui.nameEdit.text()
            self.fertigkeit.steigerungsfaktor = int(ui.steigerungsfaktorEdit.value())
            if ui.radioProfan.isChecked():
                if ui.checkKampffertigkeit.isChecked():
                    self.fertigkeit.kampffertigkeit = 1;
            else:
                self.fertigkeit.voraussetzungen = Hilfsmethoden.VorStr2Array(ui.voraussetzungenEdit.text(),None)
            self.fertigkeit.attribute = [ui.comboAttribut1.currentText(), 
                             ui.comboAttribut2.currentText(),
                             ui.comboAttribut3.currentText()]
            self.fertigkeit.text = ui.textEdit.toPlainText()
        else:
            self.fertigkeit = None
        