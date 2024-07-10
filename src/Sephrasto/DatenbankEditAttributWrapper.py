# -*- coding: utf-8 -*-
from Core.Attribut import AttributDefinition
import UI.DatenbankEditAttribut
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditAttributWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, element = None, readonly = False):
        super().__init__(datenbank, UI.DatenbankEditAttribut.Ui_dialog(), AttributDefinition, element, readonly)
        self.beschreibungEditor = BeschreibungEditor(self)

    def load(self, attribut):
        super().load(attribut)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.ui.leAnzeigeName.setText(attribut.anzeigename)
        self.beschreibungEditor.load(attribut)
        self.ui.teBeschreibung.setPlainText(attribut.text)
        self.ui.spinSF.setValue(attribut.steigerungsfaktor)
        self.ui.spinSortOrder.setValue(attribut.sortorder)

    def update(self, attribut):
        super().update(attribut)
        attribut.anzeigename = self.ui.leAnzeigeName.text()
        self.beschreibungEditor.update(attribut)
        attribut.steigerungsfaktor = int(self.ui.spinSF.value())
        attribut.sortorder = int(self.ui.spinSortOrder.value())

    def nameChanged(self):
        super().nameChanged()
        name = self.ui.leName.text()
        if self.validator["Name"] and len(name) != 2:
            self.ui.leName.setToolTip("Attributsnamen müssen aus exakt zwei Zeichen bestehen.") # need to adjust VoraussetzungenListe to remove this
            self.ui.leName.setStyleSheet("border: 1px solid red;")
            self.validator["Name"] = False
            self.updateSaveButtonState()
