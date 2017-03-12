# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 22:36:35 2017

@author: Aeolitus
"""

from PyQt5 import QtCore, QtWidgets, QtGui
import CharakterMain
import CharakterBeschreibungWrapper
import CharakterAttributeWrapper
import CharakterEquipmentWrapper
import CharakterFertigkeitenWrapper
import CharakterUeberWrapper
import sys
import Charakter
import Datenbank
import Wolke

class Editor(object):
    def __init__(self, Character=None):
        super().__init__()
        if Character is not None:
            Wolke.Char = Character
        else:
            Wolke.Char = Charakter.Char()
        Wolke.DB = Datenbank.Datenbank()
        
    def setupMainForm(self):
        self.formMain = QtWidgets.QWidget()
        self.ui = CharakterMain.Ui_formMain()
        self.ui.setupUi(self.formMain)
        self.ui.tabs.removeTab(0)
        self.ui.tabs.removeTab(0)
        
        self.updateEP()
        
        self.BeschrWrapper = CharakterBeschreibungWrapper.BeschrWrapper()
        self.AttrWrapper = CharakterAttributeWrapper.AttrWrapper()
        self.FertWrapper = CharakterFertigkeitenWrapper.FertWrapper()
        self.UeberWrapper = CharakterUeberWrapper.UeberWrapper()
        self.EquipWrapper = CharakterEquipmentWrapper.EquipWrapper()
        
        self.ui.tabs.addTab(self.BeschrWrapper.formBeschr, "Beschreibung")
        self.ui.tabs.addTab(self.AttrWrapper.formAttr, "Attribute")
        self.ui.tabs.addTab(self.FertWrapper.formFert, "Fertigkeiten")
        self.ui.tabs.addTab(self.UeberWrapper.formUeber, "Übernatürliches")
        self.ui.tabs.addTab(self.EquipWrapper.formEq, "Waffen und Rüstung")    
        
        self.ui.buttonSave.clicked.connect(self.EquipWrapper.updateEquipment)
        self.ui.buttonSavePDF.clicked.connect(self.EquipWrapper.loadEquipment)
        self.ui.spinEP.valueChanged.connect(self.epChanged)
        
        
        self.formMain.show()
        
    def updateEP(self):
        self.ui.spinEP.setValue(Wolke.Char.EPtotal)
        Wolke.Char.aktualisieren()
        self.ui.spinRemaining.setValue(Wolke.Char.EPtotal-Wolke.Char.EPspent)
        if Wolke.Char.EPtotal < Wolke.Char.EPspent:
            self.ui.spinRemaining.setStyleSheet("QSpinBox { background-color: rgb(200,50,50) }")
        else:
            self.ui.spinRemaining.setStyleSheet("QSpinBox { background-color: white }")
    
    def epChanged(self):
        Wolke.Char.EPtotal = self.ui.spinEP.value()
        self.updateEP()
    
if __name__ == "__main__":
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    ed = Editor()
    ed.setupMainForm()
    sys.exit(app.exec_())            
    