# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 15:58:13 2017

@author: Lennart
"""

from Wolke import Wolke
import UI.CharakterInfo
from PyQt5 import QtWidgets, QtCore, QtGui
import logging
from EinstellungenWrapper import EinstellungenWrapper
import os

class FocusWatcher(QtCore.QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obje, even):
        if type(even) == QtGui.QFocusEvent:
            if not obje.hasFocus():
                self.callback()
        return False

class InfoWrapper(QtCore.QObject):
    '''
    Wrapper class for the EP Reference GUI. Contains methods for updating
    the GUI elements to the current values.
    '''
    modified = QtCore.pyqtSignal()

    def __init__(self):
        ''' Initialize the GUI and set signals for the spinners'''
        super().__init__()
        logging.debug("Initializing InfoWrapper...")
        self.formEP = QtWidgets.QWidget()
        self.ui = UI.CharakterInfo.Ui_Form()
        self.ui.setupUi(self.formEP)

        font = QtGui.QFont(Wolke.Settings["FontHeading"], Wolke.Settings["FontHeadingSize"])
        font.setBold(True)
        self.ui.labelNotiz.setFont(font)
        self.ui.labelNotiz.setStyleSheet("color: " + Wolke.HeadingColor + ";}")
        self.ui.labelEP.setFont(font)
        self.ui.labelEP.setStyleSheet("color: " + Wolke.HeadingColor + ";}")
        self.ui.labelEinstellungen.setFont(font)
        self.ui.labelEinstellungen.setStyleSheet("color: " + Wolke.HeadingColor + ";}")
        self.ui.labelReload.setVisible(False)

        self.ui.comboHausregeln.addItems(EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"]))
        self.ui.checkFinanzen.setToolTip("Die Finanzen spielen nur bei einem neuen Charakter eine Rolle und können nach dem ersten Abenteuer ausgeblendet werden.")
        self.ui.checkFinanzen.stateChanged.connect(self.einstellungenChanged)
        self.ui.checkUeberPDF.stateChanged.connect(self.einstellungenChanged)
        self.ui.checkUeberPDF.setToolTip("Sephrasto übernimmt automatisch alle übernatürlichen Fertigkeiten in den Charakterbogen, deren FW mindestens 1 beträgt \n"\
        "und für welche du mindestens ein Talent aktiviert hast.\n"\
        "Wenn du diese Option aktivierst, zeigt Sephrasto eine PDF-Spalte bei den übernatürlichen Fertigkeiten an.\n"\
        "Mit dieser kannst du selbst entscheiden, welche Fertigkeiten in den Charakterbogen übernommen werden sollen.")
        self.ui.checkRegeln.stateChanged.connect(self.einstellungenChanged)
        self.ui.comboHausregeln.currentIndexChanged.connect(self.einstellungenChanged)

        boegen = [os.path.basename(os.path.splitext(bogen)[0]) for bogen in Wolke.Charakterbögen]
        for bogen in boegen:
            if bogen == "Standard Charakterbogen":
                self.ui.comboCharsheet.insertItem(0, bogen)
            elif bogen == "Langer Charakterbogen":
                self.ui.comboCharsheet.insertItem(0, bogen)
            else:
                self.ui.comboCharsheet.addItem(bogen)
        if not (Wolke.Char.charakterbogen in boegen):
            Wolke.Char.charakterbogen = self.ui.comboCharsheet.itemText(0)
        self.ui.comboCharsheet.currentIndexChanged.connect(self.einstellungenChanged)
        self.ui.comboRegelnGroesse.currentIndexChanged.connect(self.einstellungenChanged)

        self.focusWatcher = FocusWatcher(self.notizChanged)
        self.ui.teNotiz.installEventFilter(self.focusWatcher)

        self.initialHausregeln = Wolke.Char.hausregeln

        self.initialDetails = False
        for bogen in Wolke.Charakterbögen:
            if Wolke.Char.charakterbogen == os.path.basename(os.path.splitext(bogen)[0]):
                self.initialDetails = Wolke.Charakterbögen[bogen].beschreibungDetails
                break

        self.currentlyLoading = False

    def update(self):
        pass

    def einstellungenChanged(self):
        if self.currentlyLoading:
            return
        Wolke.Char.finanzenAnzeigen = self.ui.checkFinanzen.isChecked()
        Wolke.Char.ueberPDFAnzeigen = self.ui.checkUeberPDF.isChecked()
        Wolke.Char.regelnAnhaengen = self.ui.checkRegeln.isChecked()
        Wolke.Char.regelnGroesse = self.ui.comboRegelnGroesse.currentIndex()
        Wolke.Char.hausregeln = self.ui.comboHausregeln.currentText() if self.ui.comboHausregeln.currentText() != "Keine" else None
        Wolke.Char.charakterbogen = self.ui.comboCharsheet.currentText()

        details = False
        for bogen in Wolke.Charakterbögen:
            if Wolke.Char.charakterbogen == os.path.basename(os.path.splitext(bogen)[0]):
                details = Wolke.Charakterbögen[bogen].beschreibungDetails
                break

        self.ui.labelReload.setVisible(Wolke.Char.hausregeln != self.initialHausregeln or self.initialDetails != details)

        self.modified.emit()

    def load(self):
        self.currentlyLoading = True
        self.ui.teNotiz.setPlainText(Wolke.Char.notiz)

        self.ui.checkFinanzen.setChecked(Wolke.Char.finanzenAnzeigen)
        self.ui.checkUeberPDF.setChecked(Wolke.Char.ueberPDFAnzeigen)
        self.ui.checkRegeln.setChecked(Wolke.Char.regelnAnhaengen)
        self.ui.comboRegelnGroesse.setCurrentIndex(Wolke.Char.regelnGroesse)
        self.ui.comboHausregeln.setCurrentText(Wolke.Char.hausregeln or "Keine")
        self.ui.comboCharsheet.setCurrentText(Wolke.Char.charakterbogen)

        ''' Load all values and derived values '''
        totalVal = 0
        if Wolke.Char.EPtotal > 0:
            totalVal = Wolke.Char.EPtotal
        else:
            totalVal = Wolke.Char.EPspent
        if totalVal == 0:
            totalVal = 1

        self.ui.spinAttributeSpent.setValue(Wolke.Char.EP_Attribute)
        self.ui.spinAttributePercent.setValue(round(Wolke.Char.EP_Attribute / totalVal * 100))

        self.ui.spinVorteileSpent.setValue(Wolke.Char.EP_Vorteile)
        self.ui.spinVorteilePercent.setValue(round(Wolke.Char.EP_Vorteile / totalVal * 100))

        total = Wolke.Char.EP_Fertigkeiten + Wolke.Char.EP_Fertigkeiten_Talente + Wolke.Char.EP_FreieFertigkeiten

        self.ui.spinProfanSpent.setValue(total)
        self.ui.spinProfanPercent.setValue(round(total / totalVal * 100))

        self.ui.spinFertigkeitenSpent.setValue(Wolke.Char.EP_Fertigkeiten)
        self.ui.spinFertigkeitenPercent.setValue(round(Wolke.Char.EP_Fertigkeiten / max(total, 1) * 100))

        self.ui.spinTalenteSpent.setValue(Wolke.Char.EP_Fertigkeiten_Talente)
        self.ui.spinTalentePercent.setValue(round(Wolke.Char.EP_Fertigkeiten_Talente / max(total, 1) * 100))

        self.ui.spinFreieSpent.setValue(Wolke.Char.EP_FreieFertigkeiten)
        self.ui.spinFreiePercent.setValue(round(Wolke.Char.EP_FreieFertigkeiten / max(total, 1) * 100))

        if Wolke.Char.EP_Uebernatuerlich + Wolke.Char.EP_Uebernatuerlich_Talente > 0:
            self.ui.spinUebernatuerlichSpent.show()
            self.ui.spinUebernatuerlichPercent.show()
            self.ui.spinUeberFertigkeitenSpent.show()
            self.ui.spinUeberFertigkeitenPercent.show()
            self.ui.spinUeberTalenteSpent.show()
            self.ui.spinUeberTalentePercent.show()
            self.ui.labelUeber1.show()
            self.ui.labelUeber2.show()
            self.ui.labelUeber3.show()

            total = Wolke.Char.EP_Uebernatuerlich + Wolke.Char.EP_Uebernatuerlich_Talente

            self.ui.spinUebernatuerlichSpent.setValue(total)
            self.ui.spinUebernatuerlichPercent.setValue(round(total / totalVal * 100))

            self.ui.spinUeberFertigkeitenSpent.setValue(Wolke.Char.EP_Uebernatuerlich)
            self.ui.spinUeberFertigkeitenPercent.setValue(round(Wolke.Char.EP_Uebernatuerlich / max(total, 1) * 100))

            self.ui.spinUeberTalenteSpent.setValue(Wolke.Char.EP_Uebernatuerlich_Talente)
            self.ui.spinUeberTalentePercent.setValue(round(Wolke.Char.EP_Uebernatuerlich_Talente / max(total, 1) * 100))
        else:
            self.ui.spinUebernatuerlichSpent.hide()
            self.ui.spinUebernatuerlichPercent.hide()
            self.ui.spinUeberFertigkeitenSpent.hide()
            self.ui.spinUeberFertigkeitenPercent.hide()
            self.ui.spinUeberTalenteSpent.hide()
            self.ui.spinUeberTalentePercent.hide()
            self.ui.labelUeber1.hide()
            self.ui.labelUeber2.hide()
            self.ui.labelUeber3.hide()

        self.currentlyLoading = False

    def notizChanged(self):
        if self.currentlyLoading:
            return
        
        if Wolke.Char.notiz != self.ui.teNotiz.toPlainText():
            Wolke.Char.notiz = self.ui.teNotiz.toPlainText()
            self.modified.emit()