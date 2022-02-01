import UI.DatenbankEditEinstellung
import Datenbank
from DatenbankEinstellung import DatenbankEinstellung
from PyQt5 import QtWidgets, QtCore

class DatenbankEditEinstellungWrapper(object):
    def __init__(self, datenbank, einstellung=None, readonly=False):
        super().__init__()
        self.datenbank = datenbank
        if einstellung is None:
            einstellung = DatenbankEinstellung()
        self.einstellungPicked = einstellung
        self.readonly = readonly
        deDialog = QtWidgets.QDialog()
        self.ui = UI.DatenbankEditEinstellung.Ui_deDialog()
        self.ui.setupUi(deDialog)

        if not einstellung.isUserAdded:
            if readonly:
                self.ui.warning.setText("Gelöschte Elemente können nicht verändert werden.")
            self.ui.warning.setVisible(True)

        deDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.labelName.setText(einstellung.name)
        self.ui.labelBeschreibung.setText(einstellung.beschreibung)
        
        self.ui.checkWert.setVisible(einstellung.typ == 'Bool')
        self.ui.spinWert.setVisible(einstellung.typ == 'Int')
        self.ui.dspinWert.setVisible(einstellung.typ == 'Float')
        self.ui.teWert.setVisible(einstellung.typ == 'Text')
        if einstellung.typ == 'Int':
            self.ui.spinWert.setValue(einstellung.toInt())
        elif einstellung.typ == 'Float':
            self.ui.dspinWert.setValue(einstellung.toFloat())
        elif einstellung.typ == 'Bool':
            self.ui.checkWert.setChecked(einstellung.toBool())
        else:
            self.ui.teWert.setPlainText(einstellung.toText())
        deDialog.adjustSize()

        self.updateSaveButtonState()
        deDialog.show()
        ret = deDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.einstellung = Datenbank.DatenbankEinstellung()
            self.einstellung.name = self.ui.labelName.text()
            self.einstellung.typ = self.einstellungPicked.typ
            self.einstellung.beschreibung = self.einstellungPicked.beschreibung
            if einstellung.typ == 'Int':
                self.einstellung.wert = str(self.ui.spinWert.value())
            elif einstellung.typ == 'Float':
                self.einstellung.wert = str(self.ui.dspinWert.value())
            elif einstellung.typ == 'Bool':
                self.einstellung.wert = str(self.ui.checkWert.isChecked())
            else:
                self.einstellung.wert = self.ui.teWert.toPlainText()

            self.einstellung.isUserAdded = False
            if self.einstellung == self.einstellungPicked:
                self.einstellung = None
            else:
                self.einstellung.isUserAdded = True
        else:
            self.einstellung = None

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(not self.readonly)