# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:33:39 2017

@author: Aeolitus
"""
from PyQt5 import QtWidgets, QtCore
import UI.DatenbankSelectType

class DatenbankSelectTypeWrapper(object):
    def __init__(self, dbTypes):
        super().__init__()
        Dialog = QtWidgets.QDialog()
        ui = UI.DatenbankSelectType.Ui_Dialog()
        ui.setupUi(Dialog)

        # Todo: Should probably just rename them properly but it would require a db migration...
        displayNames = {
            "Manöver / Modifikation" : "Manöver / Modifikation / Regel",
            "Fertigkeit" : "Fertigkeit (profan)",
            "Übernatürliche Fertigkeit" : "Fertigkeit (übernatürlich)"
        }
        displayNames_inverse = {v: k for k, v in displayNames.items()}

        types = []
        for dbType in sorted(dbTypes):
            if dbType == "Einstellung":
                continue
            if dbType in displayNames:
                types.append(displayNames[dbType])
            else:
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
        ret = Dialog.exec_()
        self.entryType = None
        if ret == QtWidgets.QDialog.Accepted:
            for button in buttons:
                if button.isChecked():
                    self.entryType = button.text()
                    if self.entryType in displayNames_inverse:
                        self.entryType = displayNames_inverse[self.entryType]
                    break
        
        