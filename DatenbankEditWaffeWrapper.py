# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Objekte
import DatenbankEditWaffe
from PyQt5 import QtWidgets, QtCore

class DatenbankEditWaffeWrapper(object):
    def __init__(self, datenbank, waffe=None):
        super().__init__()
        self.db = datenbank
        if waffe is None:
            waffe = Objekte.Nahkampfwaffe()
        self.waffePicked = waffe
        waffeDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditWaffe.Ui_talentDialog()
        self.ui.setupUi(waffeDialog)
        
        if not waffe.isUserAdded:
            self.ui.warning.setVisible(True)

        waffeDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.nameEdit.setText(waffe.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()

        if type(waffe) == Objekte.Fernkampfwaffe:
            self.ui.comboTyp.setCurrentIndex(1)
        else:
            self.ui.comboTyp.setCurrentIndex(0)
        self.ui.comboTyp.currentIndexChanged[int].connect(self.switchType)
        self.ui.textEigenschaften.setPlainText(", ".join(waffe.eigenschaften))
        self.ui.spinHaerte.setValue(waffe.haerte)
        self.ui.spinW6.setValue(waffe.W6)
        self.ui.spinPlus.setValue(waffe.plus)
        self.ui.spinRW1.setValue(waffe.rw)
        if type(waffe) == Objekte.Fernkampfwaffe:
            self.switchType(1)
            self.ui.spinWMLZ.setValue(waffe.lz)
        else:
            self.switchType(0)
            self.ui.spinWMLZ.setValue(waffe.wm)
        if waffe.fertigkeit != '':
            try: 
                self.ui.comboFert.setCurrentText(waffe.fertigkeit)
                fff = waffe.fertigkeit
            except:
                pass
        else:
            fff = self.ui.comboFert.currentText()
        self.switchTals(fff)
        self.ui.comboFert.currentTextChanged.connect(self.switchTals)
        if waffe.talent != '':
            try:
                self.ui.comboTalent.setCurrentText(waffe.talent)
            except:
                pass
        self.ui.checkBeid.setChecked(waffe.beid != 0)
        self.ui.checkParry.setChecked(waffe.pari != 0)
        self.ui.checkReiter.setChecked(waffe.reit != 0)
        self.ui.checkSchild.setChecked(waffe.schi != 0)
        self.ui.checkKraft.setChecked(waffe.kraf != 0)
        self.ui.checkSchnell.setChecked(waffe.schn != 0)
        
        waffeDialog.show()
        ret = waffeDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            if self.ui.comboTyp.currentIndex() == 0:
                self.waffe = Objekte.Nahkampfwaffe()
                self.waffe.wm = int(self.ui.spinWMLZ.value())
            else:
                self.waffe = Objekte.Fernkampfwaffe()
                self.waffe.lz = int(self.ui.spinWMLZ.value())
            self.waffe.rw = int(self.ui.spinRW1.value())
            self.waffe.W6 = int(self.ui.spinW6.value())
            self.waffe.plus = int(self.ui.spinPlus.value())
            self.waffe.haerte = int(self.ui.spinHaerte.value())
            eigenschaftStr = self.ui.textEigenschaften.toPlainText()
            if eigenschaftStr:
                self.waffe.eigenschaften = list(map(str.strip, eigenschaftStr.split(",")))
            self.waffe.name = self.ui.nameEdit.text()
            self.waffe.fertigkeit = self.ui.comboFert.currentText()
            self.waffe.talent = self.ui.comboTalent.currentText()
            self.waffe.beid = int(self.ui.checkBeid.isChecked())
            self.waffe.pari = int(self.ui.checkParry.isChecked())
            self.waffe.reit = int(self.ui.checkReiter.isChecked())
            self.waffe.schi = int(self.ui.checkSchild.isChecked())
            self.waffe.kraf = int(self.ui.checkKraft.isChecked())
            self.waffe.schn = int(self.ui.checkSchnell.isChecked())
        else:
            self.waffe = None
            
    def switchType(self, melee):
        if melee == 0:
            self.ui.spinWMLZ.setMinimum(-9)
            self.ui.labelWMLZ.setText("Waffenmodifikator")
        else:
            self.ui.spinWMLZ.setMinimum(1)
            self.ui.labelWMLZ.setText("Ladezeit")
            
    def switchTals(self, ff):
        self.ui.comboTalent.setCurrentIndex(0)
        self.ui.comboTalent.clear()
        for tal in self.db.talente:
            if ff in self.db.talente[tal].fertigkeiten:
                self.ui.comboTalent.addItem(tal)

    def nameChanged(self):
        name = self.ui.nameEdit.text()
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        elif name != self.waffePicked.name and name in self.db.waffen:
            self.ui.nameEdit.setToolTip("Name existiert bereits.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        else:
            self.ui.nameEdit.setToolTip("")
            self.ui.nameEdit.setStyleSheet("")
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)