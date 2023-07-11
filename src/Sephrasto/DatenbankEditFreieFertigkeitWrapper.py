# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:33:21 2018

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, VoraussetzungenEditor
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import UI.DatenbankEditFreieFertigkeit
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Core.FreieFertigkeit import FreieFertigkeitDefinition
from Datenbank import Datenbank

class DatenbankEditFreieFertigkeitWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, element = None, readonly = False):
        super().__init__()
        self.voraussetzungenEditor = VoraussetzungenEditor(self)
        self.setupAndShow(datenbank, UI.DatenbankEditFreieFertigkeit.Ui_dialog(), FreieFertigkeitDefinition, element, readonly)

    def load(self, fertigkeit):
        super().load(fertigkeit)
        self.voraussetzungenEditor.load(fertigkeit)
        ffTypen = self.datenbank.einstellungen["FreieFertigkeiten: Typen"].wert
        self.ui.comboTyp.addItems(ffTypen)
        self.ui.comboTyp.setCurrentText(fertigkeit.kategorie)

    def update(self, fertigkeit):
        super().update(fertigkeit)
        self.voraussetzungenEditor.update(fertigkeit)
        fertigkeit.kategorie = self.ui.comboTyp.currentText()