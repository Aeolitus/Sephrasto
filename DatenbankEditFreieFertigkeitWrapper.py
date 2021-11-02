# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:33:21 2018

@author: Aeolitus
"""
from PyQt5 import QtCore, QtWidgets

import DatenbankEditFreieFertigkeit
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException


class DatenbankEditFreieFertigkeitWrapper(object):
    def __init__(self, datenbank, fert=None, readonly=False):
        super().__init__()
        self.datenbank = datenbank
        if fert is None:
            fert = Fertigkeiten.FreieFertigkeitDB()
        self.freieFertigkeitPicked = fert
        self.nameValid = True
        self.readonly = readonly
        self.voraussetzungenValid = True
        ffDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditFreieFertigkeit.Ui_ffDialog()
        self.ui.setupUi(ffDialog)

        if not fert.isUserAdded:
            if readonly:
                self.ui.warning.setText(
                    "Gelöschte Elemente können nicht verändert werden."
                )
            self.ui.warning.setVisible(True)

        ffDialog.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        self.ui.leName.setText(fert.name)
        self.ui.leName.textChanged.connect(self.nameChanged)
        self.nameChanged()
        self.ui.leKategorie.setText(fert.kategorie)
        self.ui.teVoraussetzungen.setPlainText(
            Hilfsmethoden.VorArray2Str(fert.voraussetzungen, None)
        )
        self.ui.teVoraussetzungen.textChanged.connect(self.voraussetzungenTextChanged)

        ffDialog.show()
        ret = ffDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.freieFertigkeit = Fertigkeiten.FreieFertigkeitDB()
            self.freieFertigkeit.name = self.ui.leName.text()
            self.freieFertigkeit.kategorie = self.ui.leKategorie.text()
            self.freieFertigkeit.voraussetzungen = Hilfsmethoden.VorStr2Array(
                self.ui.teVoraussetzungen.toPlainText(), datenbank
            )

            self.freieFertigkeit.isUserAdded = False
            if self.freieFertigkeit == self.freieFertigkeitPicked:
                self.freieFertigkeit = None
            else:
                self.freieFertigkeit.isUserAdded = True
        else:
            self.freieFertigkeit = None

    def nameChanged(self):
        name = self.ui.leName.text()
        if name == "":
            self.ui.leName.setToolTip("Name darf nicht leer sein.")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        elif (
            name != self.freieFertigkeitPicked.name
            and name in self.datenbank.freieFertigkeiten
        ):
            self.ui.leName.setToolTip("Name existiert bereits.")
            self.ui.leName.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        else:
            self.ui.leName.setToolTip("")
            self.ui.leName.setStyleSheet("")
            self.nameValid = True
        self.updateSaveButtonState()

    def voraussetzungenTextChanged(self):
        try:
            Hilfsmethoden.VorStr2Array(
                self.ui.teVoraussetzungen.toPlainText(), self.datenbank
            )
            self.ui.teVoraussetzungen.setStyleSheet("")
            self.ui.teVoraussetzungen.setToolTip("")
            self.voraussetzungenValid = True
        except VoraussetzungException as e:
            self.ui.teVoraussetzungen.setStyleSheet("border: 1px solid red;")
            self.ui.teVoraussetzungen.setToolTip(str(e))
            self.voraussetzungenValid = False
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(
            not self.readonly and self.nameValid and self.voraussetzungenValid
        )
