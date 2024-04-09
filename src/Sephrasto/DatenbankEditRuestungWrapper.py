# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor
from Core.Ruestung import RuestungDefinition
import UI.DatenbankEditRuestung
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditRuestungWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, rüstung=None, readonly=False):
        super().__init__()
        self.beschreibungEditor = BeschreibungEditor(self)
        self.setupAndShow(datenbank, UI.DatenbankEditRuestung.Ui_dialog(), RuestungDefinition, rüstung, readonly)

    def load(self, rüstung):
        super().load(rüstung)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.beschreibungEditor.load(rüstung)
        self.ui.spinBeine.valueChanged.connect(self.rsChanged)
        self.ui.spinSchwert.valueChanged.connect(self.rsChanged)
        self.ui.spinSchild.valueChanged.connect(self.rsChanged)
        self.ui.spinBauch.valueChanged.connect(self.rsChanged)
        self.ui.spinBrust.valueChanged.connect(self.rsChanged)
        self.ui.spinKopf.valueChanged.connect(self.rsChanged)

        self.ui.comboTyp.addItems(self.datenbank.einstellungen["Rüstungen: Kategorien"].wert.keyList)
        self.ui.comboTyp.setCurrentIndex(rüstung.kategorie)
        self.ui.comboSystem.setCurrentIndex(rüstung.system)
        self.ui.spinBeine.setValue(rüstung.rs[0])
        self.ui.spinSchwert.setValue(rüstung.rs[1])
        self.ui.spinSchild.setValue(rüstung.rs[2])
        self.ui.spinBauch.setValue(rüstung.rs[3])
        self.ui.spinBrust.setValue(rüstung.rs[4])
        self.ui.spinKopf.setValue(rüstung.rs[5])

    def update(self, rüstung):
        super().update(rüstung)
        self.beschreibungEditor.update(rüstung)   
        rüstung.kategorie = self.ui.comboTyp.currentIndex()
        rüstung.system = self.ui.comboSystem.currentIndex()
        rüstung.rs[0] = int(self.ui.spinBeine.value())
        rüstung.rs[1] = int(self.ui.spinSchwert.value())
        rüstung.rs[2] = int(self.ui.spinSchild.value())
        rüstung.rs[3] = int(self.ui.spinBauch.value())
        rüstung.rs[4] = int(self.ui.spinBrust.value())
        rüstung.rs[5] = int(self.ui.spinKopf.value())

    def rsChanged(self):
        self.ui.labelRS.setText(str(round((self.ui.spinBeine.value() + self.ui.spinSchwert.value() + self.ui.spinSchild.value() + self.ui.spinBauch.value() + self.ui.spinBrust.value() + self.ui.spinKopf.value()) / 6, 2)))