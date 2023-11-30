# -*- coding: utf-8 -*-
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden
from VoraussetzungenListe import VoraussetzungenListe, VoraussetzungException

class DatenbankElementEditorBase():
    def __init__(self):
        self.validator = { "Name" : True } #modules can add their own keys

    def setupAndShow(self, datenbank, ui, elementType, element, readonly):
        self.datenbank = datenbank
        self.elementTable = datenbank.tablesByType[elementType]
        if element is None:
            element = elementType()
        self.elementPicked = element
        self.readonly = readonly
        self.dialog = QtWidgets.QDialog()
        self.dialog.accept = lambda: self.accept()
        self.ui = ui
        self.ui.setupUi(self.dialog)
        self.onSetupUi()

        if readonly:
            self.ui.warning.setText("Gelöschte und überschriebene Elemente können nicht verändert werden.")
            self.ui.warning.setVisible(True)
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)

        self.dialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)
        
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setText("Speichern")
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Abbrechen")

        settingName = "WindowSize-DB" + elementType.__name__
        if not settingName in Wolke.Settings:
            Wolke.Settings[settingName] = [461, 522]
        windowSize = Wolke.Settings[settingName]
        self.dialog.resize(windowSize[0], windowSize[1])

        self.load(element)

        self.dialog.show()
        ret = self.dialog.exec()

        Wolke.Settings[settingName] = [self.dialog.size().width(), self.dialog.size().height()]

        if ret == QtWidgets.QDialog.Accepted:
            self.element = elementType()
            self.update(self.element)
            self.element.finalize(self.datenbank)
            if self.element.deepequals(element):
                self.element = None
        else:
            self.element = None

    # to be overridden by subclasses
    def onSetupUi(self):
        pass

    def load(self, element):
        self.ui.leName.setText(element.name)
        self.ui.leName.textChanged.connect(self.nameChanged)
        self.nameChanged()

    def update(self, element):
        element.name = self.ui.leName.text()

    def accept(self):
        self.dialog.done(QtWidgets.QDialog.Accepted)

    # eventhandlers
    def nameChanged(self):
        name = self.ui.leName.text()
        if name == "":
            self.ui.leName.setToolTip("Name darf nicht leer sein.")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
            self.validator["Name"] = False
        elif name != self.elementPicked.name and name in self.elementTable:
            self.ui.leName.setToolTip("Name existiert bereits.")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
            self.validator["Name"] = False
        else:
            self.ui.leName.setToolTip("")
            self.ui.leName.setStyleSheet("")
            self.validator["Name"] = True
        self.updateSaveButtonState()
    
    def updateSaveButtonState(self):
        if self.readonly:
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
            return

        for valid in self.validator.values():
            if not valid:
                self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
                return

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)

class BeschreibungEditor:
    def __init__(self, editor, propertyName = "text", textEditName = "teBeschreibung", previewName = "tbBeschreibung", listifyPreview = False):
        self.editor = editor
        self.textEditName = textEditName
        self.previewName = previewName
        self.propertyName = propertyName
        self.listifyPreview = listifyPreview

    def load(self, element):
        textEdit = getattr(self.editor.ui, self.textEditName)
        textEdit.setPlainText(getattr(element, self.propertyName))
        textEdit.textChanged.connect(self.beschreibungTextChanged)
        self.beschreibungTextChanged()

    def update(self, element):
        textEdit = getattr(self.editor.ui, self.textEditName)
        setattr(element, self.propertyName, textEdit.toPlainText())

    def beschreibungTextChanged(self):
        textEdit = getattr(self.editor.ui, self.textEditName)
        if self.previewName is not None:
            previewEdit = getattr(self.editor.ui, self.previewName)
            text = textEdit.toPlainText()
            if self.listifyPreview and ("\n" in text and not "<ul" in text and not "<ol" in text):
                text = "<ul><li>" + text.replace("\n", "</li><li>") + "</li></ul>"
            previewEdit.setText(Hilfsmethoden.fixHtml(text))

class VoraussetzungenEditor:
    def __init__(self, editor):
        self.editor = editor
        self.editor.validator["Voraussetzungen"] = True

    def load(self, element):
        self.editor.ui.teVoraussetzungen.setPlainText(element.voraussetzungen.text)
        self.editor.ui.teVoraussetzungen.textChanged.connect(self.voraussetzungenTextChanged)
        self.voraussetzungenTextChanged()

    def update(self, element):
        try:
            element.voraussetzungen.compile(self.editor.ui.teVoraussetzungen.toPlainText(), self.editor.datenbank)
        except VoraussetzungException as e:
            element.voraussetzungen = []

    def voraussetzungenTextChanged(self):
        try:
            VoraussetzungenListe().compile(self.editor.ui.teVoraussetzungen.toPlainText(), self.editor.datenbank)
            self.editor.ui.teVoraussetzungen.setStyleSheet("")
            self.editor.ui.teVoraussetzungen.setToolTip("")
            self.editor.validator["Voraussetzungen"] = True
        except VoraussetzungException as e:
            self.editor.ui.teVoraussetzungen.setStyleSheet("border: 1px solid red;")
            self.editor.ui.teVoraussetzungen.setToolTip(str(e))
            self.editor.validator["Voraussetzungen"] = False
        self.editor.updateSaveButtonState()

class ScriptEditor:
    def __init__(self, editor, propertyName):
        self.editor = editor
        self.propertyName = propertyName
        self.widget = None
        self.editor.validator[self.propertyName] = True

    def load(self, element):
        lineEditName = "le" + self.propertyName[0].upper() + self.propertyName[1:]
        textEditName = "te" + self.propertyName[0].upper() + self.propertyName[1:]
        if hasattr(self.editor.ui, lineEditName):
            self.widget = getattr(self.editor.ui, lineEditName)
            self.widget.setText(getattr(element, self.propertyName))
        elif hasattr(self.editor.ui, textEditName):
            self.widget = getattr(self.editor.ui, textEditName)
            self.widget.setPlainText(getattr(element, self.propertyName))
        self.widget.textChanged.connect(self.scriptTextChanged)
        self.scriptTextChanged()

    def update(self, element):
        text = self.widget.text() if isinstance(self.widget, QtWidgets.QLineEdit) else self.widget.toPlainText()
        setattr(element, self.propertyName, text)

    def scriptTextChanged(self):
        try:
            text = self.widget.text() if isinstance(self.widget, QtWidgets.QLineEdit) else self.widget.toPlainText()
            compile(text, self.propertyName, "exec")
            self.widget.setStyleSheet("")
            self.widget.setToolTip("")
            self.editor.validator[self.propertyName] = True
        except SyntaxError as e:
            self.widget.setStyleSheet("border: 1px solid red;")
            if isinstance(self.widget, QtWidgets.QLineEdit):
                self.widget.setToolTip(f"{e.msg} (at position {e.offset})")
            else:
                self.widget.setToolTip(f"{e.msg} (at line {e.lineno} position {e.offset})")
            self.editor.validator[self.propertyName] = False
        self.editor.updateSaveButtonState()