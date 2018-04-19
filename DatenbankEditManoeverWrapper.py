# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:33:21 2018

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden
import DatenbankEditManoever
from PyQt5 import QtWidgets, QtCore

class DatenbankEditManoeverWrapper(object):
    def __init__(self, man=None):
        super().__init__()
        if man is None:
            man = Fertigkeiten.Manoever()
        manDialog = QtWidgets.QDialog()
        ui = DatenbankEditManoever.Ui_manDialog()
        ui.setupUi(manDialog)
        
        manDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        ui.nameEdit.setText(man.name)
        ui.probeEdit.setText(man.probe)
        ui.gegenEdit.setText(man.gegenprobe)
        ui.comboTyp.setCurrentIndex(man.typ)
        ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(man.voraussetzungen, None))
        ui.textEdit.setPlainText(man.text)
        manDialog.show()
        ret = manDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.man = Fertigkeiten.Manoever()
            self.man.name = ui.nameEdit.text()
            self.man.probe = ui.probeEdit.text()
            self.man.gegenprobe = ui.gegenEdit.text()
            self.man.typ = ui.comboTyp.currentIndex()
            self.man.voraussetzungen = Hilfsmethoden.VorStr2Array(ui.voraussetzungenEdit.toPlainText(),None)
            self.man.text = ui.textEdit.toPlainText()
        else:
            self.man = None
