# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 15:58:13 2017

@author: Lennart
"""

from Wolke import Wolke
import CharakterEP
from PyQt5 import QtWidgets, QtCore
import logging

class EPWrapper(QtCore.QObject):
    '''
    Wrapper class for the EP Reference GUI. Contains methods for updating
    the GUI elements to the current values.
    '''
    modified = QtCore.pyqtSignal()

    def __init__(self):
        ''' Initialize the GUI and set signals for the spinners'''
        super().__init__()
        logging.debug("Initializing EPWrapper...")
        self.formEP = QtWidgets.QWidget()
        self.uiEP = CharakterEP.Ui_Form()
        self.uiEP.setupUi(self.formEP)
        self.load()

    def update(self):
        pass

    def load(self):
        ''' Load all values and derived values '''
        totalVal = 0
        if Wolke.Char.EPtotal > 0:
            totalVal = Wolke.Char.EPtotal
        else:
            totalVal = Wolke.Char.EPspent
        if totalVal == 0:
            totalVal = 1

        self.uiEP.spinAttributeSpent.setValue(Wolke.Char.EP_Attribute)
        self.uiEP.spinAttributePercent.setValue(round(
                Wolke.Char.EP_Attribute / totalVal * 100))

        self.uiEP.spinVorteileSpent.setValue(Wolke.Char.EP_Vorteile)
        self.uiEP.spinVorteilePercent.setValue(round(
                Wolke.Char.EP_Vorteile / totalVal * 100))

        total = (Wolke.Char.EP_Fertigkeiten +
                 Wolke.Char.EP_Fertigkeiten_Talente +
                 Wolke.Char.EP_FreieFertigkeiten)

        self.uiEP.spinProfanSpent.setValue(total)
        self.uiEP.spinProfanPercent.setValue(round(total / totalVal * 100))

        self.uiEP.spinFertigkeitenSpent.setValue(Wolke.Char.EP_Fertigkeiten)
        self.uiEP.spinFertigkeitenPercent.setValue(round(
                Wolke.Char.EP_Fertigkeiten / max(total, 1) * 100))

        self.uiEP.spinTalenteSpent.setValue(Wolke.Char.EP_Fertigkeiten_Talente)
        self.uiEP.spinTalentePercent.setValue(round(
                Wolke.Char.EP_Fertigkeiten_Talente / max(total, 1) * 100))

        self.uiEP.spinFreieSpent.setValue(Wolke.Char.EP_FreieFertigkeiten)
        self.uiEP.spinFreiePercent.setValue(round(
                Wolke.Char.EP_FreieFertigkeiten / max(total, 1) * 100))

        if Wolke.Char.EP_Uebernatuerlich + \
                Wolke.Char.EP_Uebernatuerlich_Talente > 0:

            self.uiEP.spinUebernatuerlichSpent.show()
            self.uiEP.spinUebernatuerlichPercent.show()
            self.uiEP.spinUeberFertigkeitenSpent.show()
            self.uiEP.spinUeberFertigkeitenPercent.show()
            self.uiEP.spinUeberTalenteSpent.show()
            self.uiEP.spinUeberTalentePercent.show()
            self.uiEP.labelUeber1.show()
            self.uiEP.labelUeber2.show()
            self.uiEP.labelUeber3.show()

            total = (Wolke.Char.EP_Uebernatuerlich +
                     Wolke.Char.EP_Uebernatuerlich_Talente)

            self.uiEP.spinUebernatuerlichSpent.setValue(total)
            self.uiEP.spinUebernatuerlichPercent.setValue(round(
                    total / totalVal * 100))

            self.uiEP.spinUeberFertigkeitenSpent.setValue(
                    Wolke.Char.EP_Uebernatuerlich)
            self.uiEP.spinUeberFertigkeitenPercent.setValue(round(
                Wolke.Char.EP_Uebernatuerlich / max(total, 1) * 100))

            self.uiEP.spinUeberTalenteSpent.setValue(
                    Wolke.Char.EP_Uebernatuerlich_Talente)
            self.uiEP.spinUeberTalentePercent.setValue(round(
                Wolke.Char.EP_Uebernatuerlich_Talente / max(total, 1) * 100))

        else:

            self.uiEP.spinUebernatuerlichSpent.hide()
            self.uiEP.spinUebernatuerlichPercent.hide()
            self.uiEP.spinUeberFertigkeitenSpent.hide()
            self.uiEP.spinUeberFertigkeitenPercent.hide()
            self.uiEP.spinUeberTalenteSpent.hide()
            self.uiEP.spinUeberTalentePercent.hide()
            self.uiEP.labelUeber1.hide()
            self.uiEP.labelUeber2.hide()
            self.uiEP.labelUeber3.hide()
