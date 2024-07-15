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
from ScriptPickerWrapper import ScriptPickerWrapper, ScriptContext
from EventBus import EventBus

class DatenbankEditWaffeneigenschaftWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, waffeneigenschaft=None):
        super().__init__(datenbank, UI.DatenbankEditWaffeneigenschaft.Ui_dialog(), Waffeneigenschaft, waffeneigenschaft)
        self.beschreibungEditor = BeschreibungEditor(self)
        self.scriptEditor = ScriptEditor(self, lineLimit=2)

    def onSetupUi(self):
        super().onSetupUi()
        
        ui = self.ui
        self.registerInput(ui.leName, ui.labelName)
        self.registerInput(ui.teBeschreibung, ui.labelBeschreibung)
        self.registerInput(ui.teScript, ui.labelScript)
        self.registerInput(ui.spinScriptPrio, ui.labelScript)

        self.ui.buttonPickScript.setText("\uf121")
        self.ui.buttonPickScript.clicked.connect(self.openScriptPicker)

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

    def openScriptPicker(self):
        pickerClass = EventBus.applyFilter("class_scriptpicker_wrapper", ScriptPickerWrapper)
        picker = pickerClass(self.datenbank, self.ui.teScript.toPlainText(), ScriptContext.Waffeneigenschaften)
        if picker.script != None:
            self.ui.teScript.setPlainText(picker.script)