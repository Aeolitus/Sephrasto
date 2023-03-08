# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:33:39 2017

@author: Aeolitus
"""
from PySide6 import QtWidgets, QtCore
import UI.DatenbankSelectType

class DatenbankSelectTypeWrapper(object):
    def __init__(self, dbTypes):
        super().__init__()
        Dialog = QtWidgets.QDialog()
        ui = UI.DatenbankSelectType.Ui_Dialog()
        ui.setupUi(Dialog)

        types = []
        for dbType in sorted(dbTypes):
            if dbType == "Einstellung":
                continue
            types.append(dbType)
        types = sorted(types)

        buttons = []
        for dbType in types:
            button = QtWidgets.QRadioButton()
            button.setText(dbType)
            buttons.append(button)
            ui.buttonLayout.addWidget(button)

        buttons[0].setChecked(True)

        Dialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        Dialog.show()
        ret = Dialog.exec()
        self.entryType = None
        if ret == QtWidgets.QDialog.Accepted:
            for button in buttons:
                if button.isChecked():
                    self.entryType = button.text()
                    break
        
        