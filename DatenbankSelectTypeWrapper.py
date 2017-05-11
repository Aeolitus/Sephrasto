# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:33:39 2017

@author: Aeolitus
"""
from PyQt5 import QtWidgets
import DatenbankSelectType

class DatenbankSelectTypeWrapper(object):
    def __init__(self):
        super().__init__()
        Dialog = QtWidgets.QDialog()
        ui = DatenbankSelectType.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        ret = Dialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            if ui.buttonTalent.isChecked():
                self.entryType = "Talent"
            elif ui.buttonVorteil.isChecked():
                self.entryType = "Vorteil"
            elif ui.buttonFertigkeit.isChecked():
                self.entryType = "Fertigkeit"
            elif ui.buttonUebernatuerlich.isChecked():
                self.entryType = "Übernatürliche Fertigkeit"
            else:
                self.entryType = "Waffe"
        else: 
            self.entryType = None
        
        