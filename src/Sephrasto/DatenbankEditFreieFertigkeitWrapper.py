# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:33:21 2018

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, VoraussetzungenEditor
from Hilfsmethoden import Hilfsmethoden
import UI.DatenbankEditFreieFertigkeit
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Core.FreieFertigkeit import FreieFertigkeitDefinition
from Datenbank import Datenbank

class DatenbankEditFreieFertigkeitWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, element = None):
        super().__init__(datenbank, UI.DatenbankEditFreieFertigkeit.Ui_dialog(), FreieFertigkeitDefinition, element)
        self.voraussetzungenEditor = VoraussetzungenEditor(self)

    def onSetupUi(self):
        super().onSetupUi()

        ui = self.ui
        self.registerInput(ui.leName, ui.labelName)
        self.registerInput(ui.comboKategorie, ui.labelKategorie)
        self.registerInput(ui.teVoraussetzungen, ui.labelVoraussetzungen)

    def load(self, fertigkeit):
        super().load(fertigkeit)
        self.voraussetzungenEditor.load(fertigkeit)
        self.ui.comboKategorie.addItems(self.datenbank.einstellungen["FreieFertigkeiten: Kategorien"].wert.keyList)
        self.ui.comboKategorie.setCurrentIndex(fertigkeit.kategorie)

    def update(self, fertigkeit):
        super().update(fertigkeit)
        self.voraussetzungenEditor.update(fertigkeit)
        fertigkeit.kategorie = self.ui.comboKategorie.currentIndex()