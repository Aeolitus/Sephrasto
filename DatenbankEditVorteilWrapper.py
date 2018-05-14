# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Fertigkeiten
import DatenbankEditVorteil
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
from PyQt5 import QtWidgets, QtCore

class DatenbankEditVorteilWrapper(object):
    def __init__(self, datenbank, vorteil=None):
        super().__init__()
        self.datenbank = datenbank
        if vorteil is None:
            vorteil = Fertigkeiten.Vorteil()
        vorteilDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditVorteil.Ui_talentDialog()
        self.ui.setupUi(vorteilDialog)
        
        if not vorteil.isUserAdded:
            self.ui.warning.setVisible(True)

        vorteilDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.nameEdit.setText(vorteil.name)
        self.ui.kostenEdit.setValue(vorteil.kosten)
        self.ui.comboNachkauf.setCurrentText(vorteil.nachkauf)
        self.ui.comboTyp.setCurrentIndex(vorteil.typ)

        self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(vorteil.voraussetzungen, None))
        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)
        self.voraussetzungenEditStyleSheet = self.ui.voraussetzungenEdit.styleSheet()

        self.ui.textEdit.setPlainText(vorteil.text)
        self.ui.checkVariable.setChecked(vorteil.variable!=-1)
        vorteilDialog.show()
        ret = vorteilDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.vorteil = Fertigkeiten.Vorteil()
            self.vorteil.name = self.ui.nameEdit.text()
            self.vorteil.kosten = self.ui.kostenEdit.value()
            self.vorteil.nachkauf = self.ui.comboNachkauf.currentText()
            self.vorteil.voraussetzungen = Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), datenbank)
            self.vorteil.typ = self.ui.comboTyp.currentIndex()
            if self.ui.checkVariable.isChecked():
                self.vorteil.variable = 1
            else:
                self.vorteil.variable = -1
            self.vorteil.text = self.ui.textEdit.toPlainText()
        else:
            self.vorteil = None
            
    def voraussetzungenTextChanged(self):
        try:
            Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), self.datenbank)
            self.ui.voraussetzungenEdit.setStyleSheet(self.voraussetzungenEditStyleSheet)
            self.ui.voraussetzungenEdit.setToolTip("")
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        except VoraussetzungException as e:
            self.ui.voraussetzungenEdit.setStyleSheet("border: 1px solid red;")
            self.ui.voraussetzungenEdit.setToolTip(str(e))
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)