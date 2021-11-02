# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:33:39 2017

@author: Aeolitus
"""
from PyQt5 import QtCore, QtWidgets

import DatenbankSelectType


class DatenbankSelectTypeWrapper(object):
    def __init__(self):
        super().__init__()
        Dialog = QtWidgets.QDialog()
        ui = DatenbankSelectType.Ui_Dialog()
        ui.setupUi(Dialog)

        Dialog.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        Dialog.show()
        ret = Dialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            # entryType should correspond with the names in DatenbankEdit::initDatabaseTypes
            if ui.buttonTalent.isChecked():
                self.entryType = "Talent"
            elif ui.buttonVorteil.isChecked():
                self.entryType = "Vorteil"
            elif ui.buttonFertigkeit.isChecked():
                self.entryType = "Fertigkeit"
            elif ui.buttonUebernatuerlich.isChecked():
                self.entryType = "Übernatürliche Fertigkeit"
            elif ui.buttonFreieFertigkeit.isChecked():
                self.entryType = "Freie Fertigkeit"
            elif ui.buttonManoever.isChecked():
                self.entryType = "Manöver / Modifikation"
            elif ui.buttonWaffeneigenschaft.isChecked():
                self.entryType = "Waffeneigenschaft"
            elif ui.buttonWaffe.isChecked():
                self.entryType = "Waffe"
            else:
                self.entryType = "Rüstung"
        else:
            self.entryType = None
