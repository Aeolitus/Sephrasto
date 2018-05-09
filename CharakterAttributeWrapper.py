# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:21:49 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterAttribute
from PyQt5 import QtWidgets, QtCore
import logging

class AttrWrapper(QtCore.QObject):
    ''' 
    Wrapper class for the Attribute setting GUI. Contains methods for updating
    the GUI elements to the current values and for changing the current values
    to the values set by the user. 
    '''
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        ''' Initialize the GUI and set signals for the spinners'''
        super().__init__()
        logging.debug("Initializing AttrWrapper...")
        self.formAttr = QtWidgets.QWidget()
        self.uiAttr = CharakterAttribute.Ui_formAttribute()
        self.uiAttr.setupUi(self.formAttr)
        self.loadAttribute()
        #Signals
        self.uiAttr.spinAsP.valueChanged.connect(self.updateAttribute)
        self.uiAttr.spinKaP.valueChanged.connect(self.updateAttribute)
        self.uiAttr.spinKO.valueChanged.connect(self.refresh)
        self.uiAttr.spinMU.valueChanged.connect(self.refresh)
        self.uiAttr.spinIN.valueChanged.connect(self.refresh)
        self.uiAttr.spinGE.valueChanged.connect(self.refresh)
        self.uiAttr.spinKK.valueChanged.connect(self.refresh)
        self.uiAttr.spinFF.valueChanged.connect(self.refresh)
        self.uiAttr.spinKL.valueChanged.connect(self.refresh)
        self.uiAttr.spinCH.valueChanged.connect(self.refresh)
        
    def refresh(self):
        ''' The calculation of values is done by the Attribut objects, so we 
        first update them with the current value, and then set the PW's. '''
        self.updateAttribute()
        self.loadAttribute()
        
    def updateAttribute(self):
        ''' Set and refresh all Attributes '''
        changed = False
        if Wolke.Char.attribute['KO'].wert != self.uiAttr.spinKO.value():
            Wolke.Char.attribute['KO'].wert = self.uiAttr.spinKO.value()
            Wolke.Char.attribute['KO'].aktualisieren()
            changed = True

        if Wolke.Char.attribute['MU'].wert != self.uiAttr.spinMU.value():
            Wolke.Char.attribute['MU'].wert = self.uiAttr.spinMU.value()
            Wolke.Char.attribute['MU'].aktualisieren()
            changed = True

        if Wolke.Char.attribute['GE'].wert != self.uiAttr.spinGE.value():
            Wolke.Char.attribute['GE'].wert = self.uiAttr.spinGE.value()
            Wolke.Char.attribute['GE'].aktualisieren()
            changed = True

        if Wolke.Char.attribute['KK'].wert != self.uiAttr.spinKK.value():
            Wolke.Char.attribute['KK'].wert = self.uiAttr.spinKK.value()
            Wolke.Char.attribute['KK'].aktualisieren()
            changed = True

        if Wolke.Char.attribute['IN'].wert != self.uiAttr.spinIN.value():
            Wolke.Char.attribute['IN'].wert = self.uiAttr.spinIN.value()
            Wolke.Char.attribute['IN'].aktualisieren()
            changed = True

        if Wolke.Char.attribute['KL'].wert != self.uiAttr.spinKL.value():
            Wolke.Char.attribute['KL'].wert = self.uiAttr.spinKL.value()
            Wolke.Char.attribute['KL'].aktualisieren()
            changed = True

        if Wolke.Char.attribute['CH'].wert != self.uiAttr.spinCH.value():
            Wolke.Char.attribute['CH'].wert = self.uiAttr.spinCH.value()
            Wolke.Char.attribute['CH'].aktualisieren()
            changed = True

        if Wolke.Char.attribute['FF'].wert != self.uiAttr.spinFF.value():
            Wolke.Char.attribute['FF'].wert = self.uiAttr.spinFF.value()
            Wolke.Char.attribute['FF'].aktualisieren()
            changed = True

        if Wolke.Char.asp.wert != self.uiAttr.spinAsP.value():
            Wolke.Char.asp.wert = self.uiAttr.spinAsP.value()
            changed = True

        if Wolke.Char.kap.wert != self.uiAttr.spinKaP.value():
            Wolke.Char.kap.wert = self.uiAttr.spinKaP.value()
            changed = True

        if changed:
            Wolke.Char.aktualisieren()
            self.modified.emit()
        
    def loadAttribute(self):
        ''' Load all values and derived values '''
        self.uiAttr.spinKO.setValue(Wolke.Char.attribute['KO'].wert)
        self.uiAttr.pwKO.setValue(Wolke.Char.attribute['KO'].wert*2)
        self.uiAttr.spinMU.setValue(Wolke.Char.attribute['MU'].wert)
        self.uiAttr.pwMU.setValue(Wolke.Char.attribute['MU'].wert*2)
        self.uiAttr.spinGE.setValue(Wolke.Char.attribute['GE'].wert)
        self.uiAttr.pwGE.setValue(Wolke.Char.attribute['GE'].wert*2)
        self.uiAttr.spinKK.setValue(Wolke.Char.attribute['KK'].wert)
        self.uiAttr.pwKK.setValue(Wolke.Char.attribute['KK'].wert*2)
        self.uiAttr.spinIN.setValue(Wolke.Char.attribute['IN'].wert)
        self.uiAttr.pwIN.setValue(Wolke.Char.attribute['IN'].wert*2)
        self.uiAttr.spinKL.setValue(Wolke.Char.attribute['KL'].wert)
        self.uiAttr.pwKL.setValue(Wolke.Char.attribute['KL'].wert*2)
        self.uiAttr.spinCH.setValue(Wolke.Char.attribute['CH'].wert)
        self.uiAttr.pwCH.setValue(Wolke.Char.attribute['CH'].wert*2)
        self.uiAttr.spinFF.setValue(Wolke.Char.attribute['FF'].wert)
        self.uiAttr.pwFF.setValue(Wolke.Char.attribute['FF'].wert*2)
        self.uiAttr.abWS.setValue(Wolke.Char.ws)
        self.uiAttr.abGS.setValue(Wolke.Char.gs)
        self.uiAttr.abIN.setValue(Wolke.Char.ini)
        self.uiAttr.abMR.setValue(Wolke.Char.mr)
        self.uiAttr.abSB.setValue(Wolke.Char.schadensbonus)
        if "Zauberer I" in Wolke.Char.vorteile:
            self.uiAttr.spinAsP.setEnabled(True)
            self.uiAttr.spinAsP.setValue(Wolke.Char.asp.wert)
        else:
            self.uiAttr.spinAsP.setValue(0)
            self.uiAttr.spinAsP.setEnabled(False)
        if "Geweiht I" in Wolke.Char.vorteile:
            self.uiAttr.spinKaP.setEnabled(True)
            self.uiAttr.spinKaP.setValue(Wolke.Char.kap.wert)
        else:
            self.uiAttr.spinKaP.setValue(0)
            self.uiAttr.spinKaP.setEnabled(False)