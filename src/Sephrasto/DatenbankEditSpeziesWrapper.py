# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, ScriptEditor
from Core.Spezies import Spezies
import UI.DatenbankEditSpezies
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar
from ScriptPickerWrapper import ScriptPickerWrapper, ScriptContext
from EventBus import EventBus

class DatenbankEditSpeziesWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, spezies=None):
        super().__init__(datenbank, UI.DatenbankEditSpezies.Ui_dialog(), Spezies, spezies)
        self.beschreibungEditor = BeschreibungEditor(self)
        self.scriptEditor = ScriptEditor(self, lineLimit=2)

    def onSetupUi(self):
        super().onSetupUi()
        
        ui = self.ui
        self.registerInput(ui.leName, ui.labelName)
        self.registerInput(ui.teBeschreibung, ui.labelBeschreibung)
        self.registerInput(ui.teScript, ui.labelScript)

        self.ui.buttonPickScript.setText("\uf121")
        self.ui.buttonPickScript.clicked.connect(self.openScriptPicker)

    def load(self, spezies):
        super().load(spezies)
        self.htmlToolbar = HtmlToolbar(self.ui.teBeschreibung)
        self.ui.tab.layout().insertWidget(0, self.htmlToolbar)
        self.beschreibungEditor.load(spezies)
        self.scriptEditor.load(spezies)

    def update(self, spezies):
        super().update(spezies)
        self.beschreibungEditor.update(spezies)
        self.scriptEditor.update(spezies)

    def openScriptPicker(self):
        pickerClass = EventBus.applyFilter("class_scriptpicker_wrapper", ScriptPickerWrapper)
        picker = pickerClass(self.datenbank, self.ui.teScript.toPlainText(), ScriptContext.Charakter)
        if picker.script != None:
            self.ui.teScript.setPlainText(picker.script)