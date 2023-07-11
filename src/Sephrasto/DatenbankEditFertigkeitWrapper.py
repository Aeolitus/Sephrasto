# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:21:32 2017

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, VoraussetzungenEditor
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import UI.DatenbankEditFertigkeit
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Core.Fertigkeit import FertigkeitDefinition, UeberFertigkeitDefinition
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditFertigkeitWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, ueber, fertigkeit=None, readonly=False):
        super().__init__()
        self.beschreibungEditor = BeschreibungEditor(self)
        self.voraussetzungenEditor = VoraussetzungenEditor(self)
        self.fertigkeitUeber = ueber
        type = UeberFertigkeitDefinition if ueber else FertigkeitDefinition
        self.setupAndShow(datenbank, UI.DatenbankEditFertigkeit.Ui_dialog(), type, fertigkeit, readonly)

    def load(self, fertigkeit):
        super().load(fertigkeit)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.voraussetzungenEditor.load(fertigkeit)
        self.beschreibungEditor.load(fertigkeit) 
        self.ui.spinSF.setValue(fertigkeit.steigerungsfaktor)

        attribute = [a.name for a in sorted(self.datenbank.attribute.values(), key=lambda value: value.sortorder)]
        self.ui.comboAttribut1.addItems(attribute)
        self.ui.comboAttribut2.addItems(attribute)
        self.ui.comboAttribut3.addItems(attribute)

        self.ui.comboAttribut1.setCurrentText(fertigkeit.attribute[0])
        self.ui.comboAttribut2.setCurrentText(fertigkeit.attribute[1])
        self.ui.comboAttribut3.setCurrentText(fertigkeit.attribute[2])

        if self.fertigkeitUeber:
            self.ui.labelKampffertigkeit.setVisible(False)
            self.ui.comboKampffertigkeit.setVisible(False)
            self.ui.checkGruppieren.setChecked(fertigkeit.talenteGruppieren)
            fertigkeitsTypen = self.datenbank.einstellungen["Fertigkeiten: Typen übernatürlich"].wert
        else:
            self.ui.labelGruppieren.setVisible(False)
            self.ui.checkGruppieren.setVisible(False)
            self.ui.comboKampffertigkeit.setCurrentIndex(fertigkeit.kampffertigkeit)
            fertigkeitsTypen = self.datenbank.einstellungen["Fertigkeiten: Typen profan"].wert

        self.ui.comboTyp.addItems(fertigkeitsTypen)
        typ = max(fertigkeit.typ, 0)
        self.ui.comboTyp.setCurrentIndex(typ)

    def update(self, fertigkeit):
        super().update(fertigkeit)
        self.voraussetzungenEditor.update(fertigkeit)
        self.beschreibungEditor.update(fertigkeit)
        fertigkeit.steigerungsfaktor = int(self.ui.spinSF.value())
        fertigkeit.attribute = [self.ui.comboAttribut1.currentText(), 
                       self.ui.comboAttribut2.currentText(),
                       self.ui.comboAttribut3.currentText()]    
        fertigkeit.typ = self.ui.comboTyp.currentIndex()

        if self.fertigkeitUeber:
            fertigkeit.talenteGruppieren = self.ui.checkGruppieren.isChecked()
        else:
            fertigkeit.kampffertigkeit = self.ui.comboKampffertigkeit.currentIndex()

class DatenbankEditProfaneFertigkeitWrapper(DatenbankEditFertigkeitWrapper):
    def __init__(self, datenbank, fertigkeit=None, readonly=False):
        super().__init__(datenbank, False, fertigkeit, readonly)

class DatenbankEditUebernatürlicheFertigkeitWrapper(DatenbankEditFertigkeitWrapper):
    def __init__(self, datenbank, fertigkeit=None, readonly=False):
        super().__init__(datenbank, True, fertigkeit, readonly)

