# -*- coding: utf-8 -*-
from Core.AbgeleiteterWert import AbgeleiteterWertDefinition
import UI.DatenbankEditAbgeleiteterWert
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, ScriptEditor
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditAbgeleiteterWertWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, abgeleiteterWert = None, readonly = False):
        super().__init__()
        self.beschreibungEditor = BeschreibungEditor(self)
        self.scriptEditor = ScriptEditor(self, "script")
        self.finalscriptEditor = ScriptEditor(self, "finalscript")
        self.setupAndShow(datenbank, UI.DatenbankEditAbgeleiteterWert.Ui_dialog(), AbgeleiteterWertDefinition, abgeleiteterWert, readonly)

    def load(self, abgeleiteterWert):
        super().load(abgeleiteterWert)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.ui.leAnzeigeName.setText(abgeleiteterWert.anzeigename)
        self.ui.checkShow.setChecked(abgeleiteterWert.anzeigen)
        self.beschreibungEditor.load(abgeleiteterWert)
        self.ui.leFormel.setText(abgeleiteterWert.formel)
        self.ui.spinSortOrder.setValue(abgeleiteterWert.sortorder)
        self.scriptEditor.load(abgeleiteterWert)
        self.finalscriptEditor.load(abgeleiteterWert)

    def update(self, abgeleiteterWert):
        super().update(abgeleiteterWert)
        abgeleiteterWert.anzeigename = self.ui.leAnzeigeName.text()
        abgeleiteterWert.anzeigen = self.ui.checkShow.isChecked()
        self.beschreibungEditor.update(abgeleiteterWert)
        abgeleiteterWert.formel = self.ui.leFormel.text()
        abgeleiteterWert.sortorder = int(self.ui.spinSortOrder.value())
        self.scriptEditor.update(abgeleiteterWert)
        self.finalscriptEditor.update(abgeleiteterWert)