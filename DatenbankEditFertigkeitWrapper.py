# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:21:32 2017

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import DatenbankEditFertigkeit
from PyQt5 import QtWidgets, QtCore

class DatenbankEditFertigkeitWrapper(object):
    def __init__(self, datenbank, fertigkeit=None, ueber=False):
        super().__init__()
        self.datenbank = datenbank
        if fertigkeit is None:
            fertigkeit = Fertigkeiten.Fertigkeit()
        fertDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditFertigkeit.Ui_talentDialog()
        self.ui.setupUi(fertDialog)
        
        if not fertigkeit.isUserAdded:
            self.ui.warning.setVisible(True)
        
        fertDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.nameEdit.setText(fertigkeit.name)
        self.ui.steigerungsfaktorEdit.setValue(fertigkeit.steigerungsfaktor)
        self.ui.comboAttribut1.setCurrentText(fertigkeit.attribute[0])
        self.ui.comboAttribut2.setCurrentText(fertigkeit.attribute[1])
        self.ui.comboAttribut3.setCurrentText(fertigkeit.attribute[2])
        if ueber:
            self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen, None))
            self.ui.radioUebernatuerlich.setChecked(True)
            self.ui.radioProfan.setCheckable(False)
            self.ui.checkKampffertigkeit.setCheckable(False)
        else:
            self.ui.voraussetzungenEdit.setPlainText(" - ")
            self.ui.voraussetzungenEdit.setReadOnly(True)
            self.ui.radioProfan.setChecked(True)
            self.ui.radioUebernatuerlich.setCheckable(False)
            if fertigkeit.kampffertigkeit == 1:
                self.ui.checkKampffertigkeit.setChecked(True)

        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)
        self.voraussetzungenEditStyleSheet = self.ui.voraussetzungenEdit.styleSheet()

        self.ui.textEdit.setPlainText(fertigkeit.text)
        fertDialog.show()
        ret = fertDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.fertigkeit = Fertigkeiten.Fertigkeit()
            self.fertigkeit.name = self.ui.nameEdit.text()
            self.fertigkeit.steigerungsfaktor = int(self.ui.steigerungsfaktorEdit.value())
            if self.ui.radioProfan.isChecked():
                if self.ui.checkKampffertigkeit.isChecked():
                    self.fertigkeit.kampffertigkeit = 1;
            else:
                self.fertigkeit.voraussetzungen = Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), datenbank)
            self.fertigkeit.attribute = [self.ui.comboAttribut1.currentText(), 
                             self.ui.comboAttribut2.currentText(),
                             self.ui.comboAttribut3.currentText()]
            self.fertigkeit.text = self.ui.textEdit.toPlainText()
        else:
            self.fertigkeit = None
        
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