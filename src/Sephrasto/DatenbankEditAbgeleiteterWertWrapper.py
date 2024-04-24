# -*- coding: utf-8 -*-
from Core.AbgeleiteterWert import AbgeleiteterWertDefinition
import UI.DatenbankEditAbgeleiteterWert
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor, ScriptEditor
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar
from ScriptPickerWrapper import ScriptPickerWrapper
from EventBus import EventBus

class DatenbankEditAbgeleiteterWertWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, abgeleiteterWert = None, readonly = False):
        super().__init__()
        self.beschreibungEditor = BeschreibungEditor(self)
        self.scriptEditor = ScriptEditor(self, mode="eval")
        self.finalscriptEditor = ScriptEditor(self, "finalscript", "teFinalscript", mode="eval")
        self.setupAndShow(datenbank, UI.DatenbankEditAbgeleiteterWert.Ui_dialog(), AbgeleiteterWertDefinition, abgeleiteterWert, readonly)
            
    def onSetupUi(self):
        super().onSetupUi()
        self.ui.buttonPickScript.setText("\uf121")
        self.ui.buttonPickScript.clicked.connect(lambda: self.openScriptPicker(self.ui.teScript))

        self.ui.buttonPickFinalscript.setText("\uf121")
        self.ui.buttonPickFinalscript.clicked.connect(lambda: self.openScriptPicker(self.ui.teFinalscript))

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

    def openScriptPicker(self, editor):
        pickerClass = EventBus.applyFilter("class_scriptpicker_wrapper", ScriptPickerWrapper)
        picker = pickerClass(self.datenbank, editor.toPlainText(), mode="eval")
        if picker.script != None:
            editor.setPlainText(picker.script)