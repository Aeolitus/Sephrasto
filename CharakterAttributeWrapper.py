# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:21:49 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterAttribute
from PyQt5 import QtWidgets, QtCore

class AttrWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
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
        self.updateAttribute()
        self.loadAttribute()
        
    def updateAttribute(self):
        Wolke.Char.attribute['KO'].wert = self.uiAttr.spinKO.value()
        Wolke.Char.attribute['KO'].aktualisieren()
        Wolke.Char.attribute['MU'].wert = self.uiAttr.spinMU.value()
        Wolke.Char.attribute['MU'].aktualisieren()
        Wolke.Char.attribute['GE'].wert = self.uiAttr.spinGE.value()
        Wolke.Char.attribute['GE'].aktualisieren()
        Wolke.Char.attribute['KK'].wert = self.uiAttr.spinKK.value()
        Wolke.Char.attribute['KK'].aktualisieren()
        Wolke.Char.attribute['IN'].wert = self.uiAttr.spinIN.value()
        Wolke.Char.attribute['IN'].aktualisieren()
        Wolke.Char.attribute['KL'].wert = self.uiAttr.spinKL.value()
        Wolke.Char.attribute['KL'].aktualisieren()
        Wolke.Char.attribute['CH'].wert = self.uiAttr.spinCH.value()
        Wolke.Char.attribute['CH'].aktualisieren()
        Wolke.Char.attribute['FF'].wert = self.uiAttr.spinFF.value()
        Wolke.Char.attribute['FF'].aktualisieren()
        Wolke.Char.asp.wert = self.uiAttr.spinAsP.value()
        Wolke.Char.kap.wert = self.uiAttr.spinKaP.value()
        Wolke.Char.aktualisieren()
        self.modified.emit()
        
    def loadAttribute(self):
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