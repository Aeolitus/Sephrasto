# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Objekte
import DatenbankEditRuestung
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from PyQt5 import QtWidgets, QtCore
import Definitionen

class DatenbankEditRuestungWrapper(object):
    def __init__(self, datenbank, ruestung=None, readonly=False):
        super().__init__()
        self.db = datenbank
        if ruestung is None:
            ruestung = Objekte.Ruestung()
        self.ruestungPicked = ruestung
        self.readonly = readonly
        ruestungDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditRuestung.Ui_talentDialog()
        self.ui.setupUi(ruestungDialog)
        
        if not ruestung.isUserAdded:
            if readonly:
                self.ui.warning.setText("Gelöschte Elemente können nicht verändert werden.")
            self.ui.warning.setVisible(True)

        ruestungDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.nameValid = True
        self.ui.leName.setText(ruestung.name)
        self.ui.leName.textChanged.connect(self.nameChanged)
        self.nameChanged()

        self.ui.sbBeine.valueChanged.connect(self.rsChanged)
        self.ui.sbSchwert.valueChanged.connect(self.rsChanged)
        self.ui.sbSchild.valueChanged.connect(self.rsChanged)
        self.ui.sbBauch.valueChanged.connect(self.rsChanged)
        self.ui.sbBrust.valueChanged.connect(self.rsChanged)
        self.ui.sbKopf.valueChanged.connect(self.rsChanged)

        self.ui.cbTyp.addItems(datenbank.einstellungen["RüstungsTypen"].toTextList())
        self.ui.cbTyp.setCurrentIndex(ruestung.typ)
        self.ui.cbSystem.setCurrentIndex(ruestung.system)
        self.ui.sbBeine.setValue(ruestung.rs[0])
        self.ui.sbSchwert.setValue(ruestung.rs[1])
        self.ui.sbSchild.setValue(ruestung.rs[2])
        self.ui.sbBauch.setValue(ruestung.rs[3])
        self.ui.sbBrust.setValue(ruestung.rs[4])
        self.ui.sbKopf.setValue(ruestung.rs[5])
        self.ui.teBeschreibung.setPlainText(ruestung.text)
        
        ruestungDialog.adjustSize()
        ruestungDialog.show()
        ret = ruestungDialog.exec_()

        if ret == QtWidgets.QDialog.Accepted:
            self.ruestung = Objekte.Ruestung()
            self.ruestung.name = self.ui.leName.text()
            self.ruestung.typ = self.ui.cbTyp.currentIndex()
            self.ruestung.system = self.ui.cbSystem.currentIndex()
            self.ruestung.rs[0] = int(self.ui.sbBeine.value())
            self.ruestung.rs[1] = int(self.ui.sbSchwert.value())
            self.ruestung.rs[2] = int(self.ui.sbSchild.value())
            self.ruestung.rs[3] = int(self.ui.sbBauch.value())
            self.ruestung.rs[4] = int(self.ui.sbBrust.value())
            self.ruestung.rs[5] = int(self.ui.sbKopf.value())
            self.ruestung.text = self.ui.teBeschreibung.toPlainText()
            self.ruestung.isUserAdded = False
            if self.ruestung == self.ruestungPicked:
                self.ruestung = None
            else:
                self.ruestung.isUserAdded = True
        else:
            self.ruestung = None

    def rsChanged(self):
        self.ui.lblRS.setText(str(round((self.ui.sbBeine.value() + self.ui.sbSchwert.value() + self.ui.sbSchild.value() + self.ui.sbBauch.value() + self.ui.sbBrust.value() + self.ui.sbKopf.value()) / 6, 2)))

    def nameChanged(self):
        name = self.ui.leName.text()
        self.nameValid = False
        if name == "":
            self.ui.leName.setToolTip("Name darf nicht leer sein.")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
        elif name != self.ruestungPicked.name and name in self.db.rüstungen:
            self.ui.leName.setToolTip("Name existiert bereits.")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
        else:
            self.ui.leName.setToolTip("")
            self.ui.leName.setStyleSheet("")
            self.nameValid = True
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(not self.readonly and self.nameValid)