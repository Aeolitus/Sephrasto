# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, ScriptEditor
from Core.Waffeneigenschaft import Waffeneigenschaft
import UI.DatenbankEditWaffeneigenschaft
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar

class DatenbankEditWaffeneigenschaftWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, waffeneigenschaft=None, readonly = False):
        super().__init__()
        self.beschreibungEditor = BeschreibungEditor(self)
        self.scriptEditor = ScriptEditor(self, "script")
        self.setupAndShow(datenbank, UI.DatenbankEditWaffeneigenschaft.Ui_dialog(), Waffeneigenschaft, waffeneigenschaft, readonly)

    def load(self, waffeneigenschaft):
        super().load(waffeneigenschaft)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.beschreibungEditor.load(waffeneigenschaft)
        self.ui.spinScriptPrio.setValue(waffeneigenschaft.scriptPrio)
        self.scriptEditor.load(waffeneigenschaft)

    def update(self, waffeneigenschaft):
        super().update(waffeneigenschaft)
        self.beschreibungEditor.update(waffeneigenschaft)
        waffeneigenschaft.scriptPrio = self.ui.spinScriptPrio.value()
        self.scriptEditor.update(waffeneigenschaft)