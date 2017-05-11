# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Objekte
import DatenbankEditWaffe
from PyQt5 import QtWidgets

class DatenbankEditWaffeWrapper(object):
    def __init__(self, waffe=None):
        super().__init__()
        if waffe is None:
            waffe = Objekte.Nahkampfwaffe()
        waffeDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditWaffe.Ui_talentDialog()
        self.ui.setupUi(waffeDialog)
        self.ui.nameEdit.setText(waffe.name)
        if type(waffe) == Objekte.Fernkampfwaffe:
            self.ui.comboTyp.setCurrentIndex(1)
        else:
            self.ui.comboTyp.setCurrentIndex(0)
        self.ui.comboTyp.currentIndexChanged[int].connect(self.switchType)
        self.ui.textEigenschaften.setPlainText(waffe.eigenschaften)
        self.ui.spinHaerte.setValue(waffe.haerte)
        self.ui.spinW6.setValue(waffe.W6)
        self.ui.spinPlus.setValue(waffe.plus)
        if type(waffe) == Objekte.Fernkampfwaffe:
            self.switchType(1)
            self.ui.spinRW1.setValue(waffe.rwnah)
            self.ui.spinRW2.setValue(waffe.rwfern)
            self.ui.spinWMLZ.setValue(waffe.lz)
        else:
            self.switchType(0)
            self.ui.spinRW1.setValue(waffe.rw)
            self.ui.spinWMLZ.setValue(waffe.wm)
        waffeDialog.show()
        ret = waffeDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            if self.ui.comboTyp.currentIndex() == 0:
                self.waffe = Objekte.Nahkampfwaffe()
                self.waffe.rw = int(self.ui.spinRW1.value())
                self.waffe.wm = int(self.ui.spinWMLZ.value())
            else:
                self.waffe = Objekte.Fernkampfwaffe()
                self.waffe.rwnah = int(self.ui.spinRW1.value())
                self.waffe.rwfern = int(self.ui.spinRW2.value())
                self.waffe.lz = int(self.ui.spinWMLZ.value())
            self.waffe.W6 = int(self.ui.spinW6.value())
            self.waffe.plus = int(self.ui.spinPlus.value())
            self.waffe.haerte = int(self.ui.spinHaerte.value())
            self.waffe.eigenschaften = self.ui.textEigenschaften.toPlainText()
            self.waffe.name = self.ui.nameEdit.text()
        else:
            self.waffe = None
            
    def switchType(self, melee):
        if melee == 0:
            self.ui.labelRW.hide()
            self.ui.spinRW2.hide()
            self.ui.spinWMLZ.setMinimum(-9)
            self.ui.labelWMLZ.setText("Waffenmodifikator")
        else:
            self.ui.labelRW.show()
            self.ui.spinRW2.show()
            self.ui.spinWMLZ.setMinimum(1)
            self.ui.labelWMLZ.setText("Ladezeit")