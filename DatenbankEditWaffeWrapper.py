# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Objekte
import DatenbankEditWaffe
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
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
        
        self.eigenschaftenValid = True
        self.nameValid = True
        self.ui.nameEdit.setText(waffe.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()

        if type(waffe) == Objekte.Fernkampfwaffe:
            self.ui.comboTyp.setCurrentIndex(1)
        else:
            self.ui.comboTyp.setCurrentIndex(0)
        self.ui.comboTyp.currentIndexChanged[int].connect(self.switchType)
        self.ui.textEigenschaften.setPlainText(", ".join(waffe.eigenschaften))
        self.ui.textEigenschaften.textChanged.connect(self.eigenschaftenChanged)
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

        for fert in datenbank.fertigkeiten.values():
            if fert.kampffertigkeit == 0:
                continue
            self.ui.comboFert.addItem(fert.name)

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

        col = 0
        row = 0
        self.kampfstile = []
        for kampfstil in datenbank.findKampfstile():
            checkbox = QtWidgets.QCheckBox(kampfstil)
            checkbox.stateChanged.connect(lambda state, kampfstil=kampfstil : self.kampfstilChanged(kampfstil, state))
            if kampfstil in waffe.kampfstile:
                checkbox.setChecked(True)
            self.ui.layoutKampfstile.addWidget(checkbox, row, col)
            if col == 0:
                col +=1
            else:
                row += 1
                col = 0
        
        waffeDialog.adjustSize()

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
            self.waffe.kampfstile = self.kampfstile

            self.waffe.isUserAdded = False
            if self.waffe == self.waffePicked:
                self.waffe = None
            else:
                self.waffe.isUserAdded = True
        else:
            self.waffe = None

    def kampfstilChanged(self, kampfstil, state):
        if state == 0:
            self.kampfstile.remove(kampfstil)
        else:
            self.kampfstile.append(kampfstil)

    def switchType(self, melee):
        if melee == 0:
            self.ui.spinWMLZ.setMinimum(-9)
            self.ui.labelWMLZ.setText("Waffenmodifikator")
        else:
            self.ui.spinWMLZ.setMinimum(0)
            self.ui.labelWMLZ.setText("Ladezeit")
            
    def switchTals(self, ff):
        self.ui.comboTalent.setCurrentIndex(0)
        self.ui.comboTalent.clear()
        for tal in self.db.talente:
            if ff in self.db.talente[tal].fertigkeiten:
                self.ui.comboTalent.addItem(tal)

    def nameChanged(self):
        name = self.ui.nameEdit.text()
        self.nameValid = False
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
        elif name != self.waffePicked.name and name in self.db.waffen:
            self.ui.nameEdit.setToolTip("Name existiert bereits.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
        else:
            self.ui.nameEdit.setToolTip("")
            self.ui.nameEdit.setStyleSheet("")
            self.nameValid = True
        self.updateSaveButtonState()

    def eigenschaftenChanged(self):
        eigenschaftStr = self.ui.textEigenschaften.toPlainText()
        if eigenschaftStr:
            eigenschaften = list(map(str.strip, eigenschaftStr.split(",")))
            for el in eigenschaften:
                try:
                    Hilfsmethoden.VerifyWaffeneigenschaft(el, self.db)
                except WaffeneigenschaftException as e:
                    self.ui.textEigenschaften.setToolTip(str(e))
                    self.ui.textEigenschaften.setStyleSheet("border: 1px solid red;")
                    self.eigenschaftenValid = False
                    self.updateSaveButtonState()
                    return

        self.ui.textEigenschaften.setToolTip("")
        self.ui.textEigenschaften.setStyleSheet("")
        self.eigenschaftenValid = True
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.nameValid and self.eigenschaftenValid)