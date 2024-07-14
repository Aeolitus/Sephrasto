# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase
import UI.DatenbankEditWaffe
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from PySide6 import QtWidgets, QtCore
from QtUtils.TextTagCompleter import TextTagCompleter
from Core.Fertigkeit import KampffertigkeitTyp
from Core.Waffe import WaffeDefinition
from Wolke import Wolke
from functools import partial
from Datenbank import Datenbank

class DatenbankEditWaffeWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, waffe=None):
        super().__init__(datenbank, UI.DatenbankEditWaffe.Ui_dialog(), WaffeDefinition, waffe)
        self.validator["Waffeneigenschaften"] = True

    def load(self, waffe):
        super().load(waffe)
        self.ui.comboTyp.setCurrentIndex(1 if waffe.fernkampf else 0)
        self.ui.comboTyp.currentIndexChanged[int].connect(self.switchType)

        self.eigenschaftenCompleter = TextTagCompleter(self.ui.teEigenschaften, self.datenbank.waffeneigenschaften.keys())
        self.ui.teEigenschaften.setPlainText(", ".join(waffe.eigenschaften))
        self.ui.teEigenschaften.textChanged.connect(self.eigenschaftenChanged)
        self.eigenschaftenChanged()

        self.ui.spinHaerte.setValue(waffe.härte)
        self.ui.spinWuerfel.setValue(waffe.würfel)
        self.ui.comboWuerfelSeiten.setCurrentText("W" + str(waffe.würfelSeiten))
        self.ui.spinPlus.setValue(waffe.plus)
        self.ui.spinRW1.setValue(waffe.rw)
        self.ui.spinWM.setValue(waffe.wm)
        if waffe.fernkampf:
            self.switchType(1)
            self.ui.spinLZ.setValue(waffe.lz)
        else:
            self.switchType(0)

        for fert in self.datenbank.fertigkeiten.values():
            if fert.kampffertigkeit == KampffertigkeitTyp.Keine:
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
        for kampfstil in self.datenbank.findKampfstile():
            checkbox = QtWidgets.QCheckBox(kampfstil)
            checkbox.stateChanged.connect(partial(self.kampfstilChanged, kampfstil=kampfstil))
            if kampfstil in waffe.kampfstile:
                checkbox.setChecked(True)
            self.ui.layoutKampfstile.addWidget(checkbox, row, col)
            if col == 0:
                col +=1
            else:
                row += 1
                col = 0

    def update(self, waffe):
        super().update(waffe)
        if self.ui.comboTyp.currentIndex() == 1:
            waffe.fernkampf = True
            waffe.lz = int(self.ui.spinLZ.value())
        waffe.rw = int(self.ui.spinRW1.value())
        waffe.würfel = int(self.ui.spinWuerfel.value())
        waffe.würfelSeiten = int(self.ui.comboWuerfelSeiten.currentText()[1:])
        waffe.plus = int(self.ui.spinPlus.value())
        waffe.wm = int(self.ui.spinWM.value())
        waffe.härte = int(self.ui.spinHaerte.value())
        eigenschaftStr = self.ui.teEigenschaften.toPlainText()
        if eigenschaftStr:
            waffe.eigenschaften = list(map(str.strip, eigenschaftStr.strip().rstrip(',').split(",")))
        waffe.fertigkeit = self.ui.comboFert.currentText()
        waffe.talent = self.ui.comboTalent.currentText()
        waffe.kampfstile = sorted(self.kampfstile)

    def kampfstilChanged(self, state, kampfstil):
        if state == 0:
            self.kampfstile.remove(kampfstil)
        else:
            self.kampfstile.append(kampfstil)

    def switchType(self, index):
        self.ui.labelLZ.setVisible(index == 1)
        self.ui.spinLZ.setVisible(index == 1)
            
    def switchTals(self, ff):
        self.ui.comboTalent.setCurrentIndex(0)
        self.ui.comboTalent.clear()
        for tal in self.datenbank.talente:
            if ff in self.datenbank.talente[tal].fertigkeiten:
                self.ui.comboTalent.addItem(tal)

    def nameChanged(self):
        super().nameChanged()
        name = self.ui.leName.text()
        if not self.validator["Name"] and name != self.elementPicked.name and name in self.datenbank.waffen:
            self.ui.leName.setToolTip(f"Name existiert bereits.\nFalls du eine Variante der gleichen Waffe erstellen möchtest, verwende am besten das Namenschema '{name} ({self.ui.comboTalent.currentText()})', '{name} (NK)' oder '{name} (FK)'")

    def eigenschaftenChanged(self):
        eigenschaftStr = self.ui.teEigenschaften.toPlainText()
        if eigenschaftStr:
            eigenschaften = list(map(str.strip, eigenschaftStr.strip().rstrip(',').split(",")))
            for el in eigenschaften:
                try:
                    Hilfsmethoden.VerifyWaffeneigenschaft(el, self.datenbank)
                except WaffeneigenschaftException as e:
                    self.ui.teEigenschaften.setToolTip(str(e))
                    self.ui.teEigenschaften.setStyleSheet("border: 1px solid red;")
                    self.validator["Waffeneigenschaften"] = False
                    self.updateSaveButtonState()
                    return

        self.ui.teEigenschaften.setToolTip("")
        self.ui.teEigenschaften.setStyleSheet("")
        self.validator["Waffeneigenschaften"] = True
        self.updateSaveButtonState()