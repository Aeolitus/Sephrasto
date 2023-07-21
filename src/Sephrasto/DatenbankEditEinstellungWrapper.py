from DatenbankElementEditorBase import DatenbankElementEditorBase, ScriptEditor
import UI.DatenbankEditEinstellung
from Core.DatenbankEinstellung import DatenbankEinstellung
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank

class DatenbankEditEinstellungWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, element, readonly=False):
        super().__init__()
        if element.typ in ["Exec", "Eval"]:
            self.scriptEditor = ScriptEditor(self, "text")
        elif element.typ == "TextDict":
            self.validator["Text"] = True
        self.setupAndShow(datenbank, UI.DatenbankEditEinstellung.Ui_dialog(), DatenbankEinstellung, element, readonly)

    def load(self, einstellung):
        self.ui.labelName.setText(einstellung.name)
        self.ui.labelBeschreibung.setText(einstellung.beschreibung)
        self.ui.checkText.setVisible(einstellung.typ == 'Bool')
        self.ui.spinText.setVisible(einstellung.typ == 'Int')
        self.ui.dspinText.setVisible(einstellung.typ == 'Float')
        self.ui.teText.setVisible(einstellung.typ in ['Text', 'TextList', 'IntList', 'TextDict', 'Eval', 'Exec'])
        if einstellung.typ == 'Int':
            self.ui.spinText.setValue(int(einstellung.text))
        elif einstellung.typ == 'Float':
            self.ui.dspinText.setValue(float(einstellung.text))
        elif einstellung.typ == 'Bool':
            self.ui.checkText.setChecked(einstellung.text.lower() == "true" or einstellung.text == '1')
        elif einstellung.typ in ["Exec", "Eval"]:
            self.scriptEditor.load(einstellung)
            self.dialog.layout().removeItem(self.ui.verticalSpacer)
        elif einstellung.typ == "TextDict":
            self.ui.teText.textChanged.connect(self.dictChanged)
            self.ui.teText.setPlainText(einstellung.text)
            self.dialog.layout().removeItem(self.ui.verticalSpacer)         
        else:
            self.ui.teText.setPlainText(einstellung.text)
            self.dialog.layout().removeItem(self.ui.verticalSpacer)

    def update(self, einstellung):
        einstellung.name = self.ui.labelName.text()
        einstellung.typ = self.elementPicked.typ
        einstellung.beschreibung = self.elementPicked.beschreibung
        einstellung.separator = self.elementPicked.separator
        einstellung.strip = self.elementPicked.strip
        if einstellung.typ == 'Int':
            einstellung.text = str(self.ui.spinText.value())
        elif einstellung.typ == 'Float':
            einstellung.text = str(self.ui.dspinText.value())
        elif einstellung.typ == 'Bool':
            einstellung.text = str(self.ui.checkText.isChecked())
        elif einstellung.typ in ["Exec", "Eval"]:
            self.scriptEditor.update(einstellung)
        else:
            einstellung.text = self.ui.teText.toPlainText()

    def dictChanged(self):
        text = self.ui.teText.toPlainText()
        allLinesValid = True
        for line in text.split(self.elementPicked.separator):
            if not "=" in line:
                allLinesValid = False
                break

        if text and not allLinesValid:
            self.ui.teText.setToolTip("Jeder Eintrag muss ein '=' enthalten.")
            self.ui.teText.setStyleSheet("border: 1px solid red;")
            self.validator["Text"] = False
            self.updateSaveButtonState()
        else:
            self.ui.teText.setToolTip("")
            self.ui.teText.setStyleSheet("")
            self.validator["Text"] = True
            self.updateSaveButtonState()