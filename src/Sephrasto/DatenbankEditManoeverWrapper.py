# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:33:21 2018

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import UI.DatenbankEditManoever
from PyQt5 import QtWidgets, QtCore
from Wolke import Wolke

class DatenbankEditManoeverWrapper(object):
    def __init__(self, datenbank, man=None, readonly=False):
        super().__init__()
        self.datenbank = datenbank
        if man is None:
            man = Fertigkeiten.Manoever()
        self.manöverPicked = man
        self.nameValid = True
        self.readonly = readonly
        self.voraussetzungenValid = True
        self.manDialog = QtWidgets.QDialog()
        self.ui = UI.DatenbankEditManoever.Ui_manDialog()
        self.ui.setupUi(self.manDialog)

        if not man.isUserAdded:
            if readonly:
                self.ui.warning.setText("Gelöschte Elemente können nicht verändert werden.")
            self.ui.warning.setVisible(True)

        self.manDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        windowSize = Wolke.Settings["WindowSize-DBManoever"]
        self.manDialog.resize(windowSize[0], windowSize[1])

        self.ui.nameEdit.setText(man.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()
        self.ui.probeEdit.setText(man.probe)
        self.ui.gegenEdit.setText(man.gegenprobe)
        self.ui.comboTyp.clear()
        self.ui.comboTyp.addItems(datenbank.einstellungen["Manöver: Typen"].toTextList())
        self.ui.comboTyp.setCurrentIndex(man.typ)
        
        self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(man.voraussetzungen, None))
        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)

        self.ui.textEdit.setPlainText(man.text)
        self.manDialog.show()
        ret = self.manDialog.exec_()

        Wolke.Settings["WindowSize-DBManoever"] = [self.manDialog.size().width(), self.manDialog.size().height()]

        if ret == QtWidgets.QDialog.Accepted:
            self.man = Fertigkeiten.Manoever()
            self.man.name = self.ui.nameEdit.text()
            self.man.probe = self.ui.probeEdit.text()
            self.man.gegenprobe = self.ui.gegenEdit.text()
            self.man.typ = self.ui.comboTyp.currentIndex()
            self.man.voraussetzungen = Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), datenbank)
            self.man.text = self.ui.textEdit.toPlainText()

            self.man.isUserAdded = False
            if self.man == self.manöverPicked:
                self.man = None
            else:
                self.man.isUserAdded = True
        else:
            self.man = None

    def nameChanged(self):
        name = self.ui.nameEdit.text()
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        elif name != self.manöverPicked.name and name in self.datenbank.manöver:
            self.ui.nameEdit.setToolTip("Name existiert bereits.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        else:
            self.ui.nameEdit.setToolTip("")
            self.ui.nameEdit.setStyleSheet("")
            self.nameValid = True
        self.updateSaveButtonState()

    def voraussetzungenTextChanged(self):
        try:
            Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), self.datenbank)
            self.ui.voraussetzungenEdit.setStyleSheet("")
            self.ui.voraussetzungenEdit.setToolTip("")
            self.voraussetzungenValid = True
        except VoraussetzungException as e:
            self.ui.voraussetzungenEdit.setStyleSheet("border: 1px solid red;")
            self.ui.voraussetzungenEdit.setToolTip(str(e))
            self.voraussetzungenValid = False
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(not self.readonly and self.nameValid and self.voraussetzungenValid)