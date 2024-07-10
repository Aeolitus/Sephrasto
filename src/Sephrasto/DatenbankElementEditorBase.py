# -*- coding: utf-8 -*-
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden
from VoraussetzungenListe import VoraussetzungenListe, VoraussetzungException
from RestrictedPython import compile_restricted

class DatenbankElementEditorBase():
    def __init__(self, datenbank, ui, elementType, element, readonly):
        self.datenbank = datenbank
        self.elementTable = datenbank.tablesByType[elementType]
        self.elementType = elementType
        if element is None:
            element = elementType()
        self.elementPicked = element
        self.readonly = readonly
        self.validator = { "Name" : True } #modules can add their own keys
        self.ui = ui

    def setupAsWidget(self):
        self.form = QtWidgets.QWidget()     
        self.ui.setupUi(self.form)
        self.onSetupUi()               
        self.load(self.elementPicked)

    def setupAsDialogAndShow(self):
        self.form = QtWidgets.QDialog()
        self.form.accept = lambda: self.accept()
        self.ui.setupUi(self.form)
        
        self.ui.warning = QtWidgets.QLabel()
        self.ui.warning.setProperty("class", "warning")
        
        assert isinstance(self.form.layout(), QtWidgets.QBoxLayout), "database element editors must have a QBoxLayout"

        self.form.layout().insertWidget(0, self.ui.warning)
        
        self.ui.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        self.ui.buttonBox.setCenterButtons(True)
        self.ui.buttonBox.accepted.connect(self.form.accept)
        self.ui.buttonBox.rejected.connect(self.form.reject)
        self.form.layout().addWidget(self.ui.buttonBox)

        self.onSetupUi()

        if self.readonly:
            self.ui.warning.setText("Gelöschte und überschriebene Elemente können nicht verändert werden.")
            self.ui.warning.setVisible(True)
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        else:
            self.ui.warning.setVisible(False)

        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)
        
        settingName = "WindowSize-DB" + self.elementType.__name__
        if not settingName in Wolke.Settings:
            Wolke.Settings[settingName] = [461, 522]
        windowSize = Wolke.Settings[settingName]
        self.form.resize(windowSize[0], windowSize[1])
        
        self.load(self.elementPicked)
        
        self.form.show()
        ret = self.form.exec()
        
        Wolke.Settings[settingName] = [self.form.size().width(), self.form.size().height()]
        
        if ret == QtWidgets.QDialog.Accepted:
            self.element = self.elementType()
            self.update(self.element)
            self.element.finalize(self.datenbank)
            if self.element.deepequals(self.elementPicked):
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
        self.form.done(QtWidgets.QDialog.Accepted)

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
        if not hasattr(self.ui, "buttonBox"):
            return;

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
    def __init__(self, editor, propertyName="script", textEditName = "teScript", lineLimit = 0, mode = "exec"):
        self.editor = editor
        self.propertyName = propertyName
        self.textEditName = textEditName
        self.widget = None
        self.editor.validator[self.propertyName] = True
        self.lineLimit = lineLimit
        self.mode = mode

    def load(self, element):
        textEdit = getattr(self.editor.ui, self.textEditName)
        textEdit.setPlainText(getattr(element, self.propertyName))
        if self.lineLimit > 0:
            line = QtWidgets.QLineEdit()
            textEdit.setFixedHeight(self.lineLimit * line.sizeHint().height())
            line.deleteLater()
        self.toolTip = textEdit.toolTip()
        textEdit.textChanged.connect(self.scriptTextChanged)
        self.scriptTextChanged()

    def update(self, element):
        textEdit = getattr(self.editor.ui, self.textEditName)
        setattr(element, self.propertyName, textEdit.toPlainText())

    def scriptTextChanged(self):
        textEdit = getattr(self.editor.ui, self.textEditName)
        if self.mode == "eval" and "\n" in textEdit.toPlainText():
            textEdit.setStyleSheet("border: 1px solid red;")
            textEdit.setToolTip("Dieses Script muss einen Ausdruck in einer einzelnen Zeile enthalten.")
            self.editor.validator[self.propertyName] = False
        else:
            try:
                compile_restricted(textEdit.toPlainText() or "0", self.propertyName, self.mode)
                textEdit.setStyleSheet("")
                textEdit.setToolTip(self.toolTip)
                self.editor.validator[self.propertyName] = True
            except SyntaxError as e:
                textEdit.setStyleSheet("border: 1px solid red;")
                textEdit.setToolTip("\n".join(e.msg))
                self.editor.validator[self.propertyName] = False
        self.editor.updateSaveButtonState()