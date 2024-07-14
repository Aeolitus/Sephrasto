# -*- coding: utf-8 -*-
from Core.Energie import EnergieDefinition
import UI.DatenbankEditEnergie
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, VoraussetzungenEditor
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditEnergieWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, energie = None):
        super().__init__(datenbank, UI.DatenbankEditEnergie.Ui_dialog(), EnergieDefinition, energie)
        self.beschreibungEditor = BeschreibungEditor(self)
        self.voraussetzungenEditor = VoraussetzungenEditor(self)

    def load(self, energie):
        super().load(energie)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.voraussetzungenEditor.load(energie)
        self.ui.leAnzeigeName.setText(energie.anzeigename)
        self.beschreibungEditor.load(energie)
        self.ui.spinSF.setValue(energie.steigerungsfaktor)
        self.ui.spinSortOrder.setValue(energie.sortorder)

    def update(self, energie):
        super().update(energie)
        self.voraussetzungenEditor.update(energie)
        energie.anzeigename = self.ui.leAnzeigeName.text()
        self.beschreibungEditor.update(energie)
        energie.steigerungsfaktor = int(self.ui.spinSF.value())
        energie.sortorder = int(self.ui.spinSortOrder.value())