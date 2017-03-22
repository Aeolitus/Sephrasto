# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 22:36:35 2017

@author: Aeolitus
"""

from PyQt5 import QtCore, QtWidgets
import CharakterMain
import CharakterBeschreibungWrapper
import CharakterAttributeWrapper
import CharakterEquipmentWrapper
import CharakterFertigkeitenWrapper
import CharakterUebernatuerlichWrapper
import CharakterFreieFertWrapper
import CharakterVorteileWrapper
import CharakterItemsWrapper
import sys
import Charakter
import Datenbank
from Wolke import Wolke

class Editor(object):
    def __init__(self, Character=None):
        super().__init__()
        Wolke.DB = Datenbank.Datenbank()
        if Character is not None:
            Wolke.Char = Character
        else:
            Wolke.Char = Charakter.Char() 
            #TODO: Remove
            Wolke.Char.xmlLesen("Franz.xml")
        Wolke.Char.aktualisieren() # A bit later because it needs access to itself
        
        self.ignoreModified = False
        
        
    def setupMainForm(self):
        self.formMain = QtWidgets.QWidget()
        self.ui = CharakterMain.Ui_formMain()
        self.ui.setupUi(self.formMain)
        self.ui.tabs.removeTab(0)
        self.ui.tabs.removeTab(0)
        
        self.updateEP()
        
        self.BeschrWrapper = CharakterBeschreibungWrapper.BeschrWrapper()
        self.AttrWrapper = CharakterAttributeWrapper.AttrWrapper()
        self.FertWrapper = CharakterFertigkeitenWrapper.FertigkeitenWrapper()
        self.FreiWrapper = CharakterFreieFertWrapper.CharakterFreieFertWrapper()
        self.UebernatuerlichWrapper = CharakterUebernatuerlichWrapper.UebernatuerlichWrapper()
        self.EquipWrapper = CharakterEquipmentWrapper.EquipWrapper()
        self.VortWrapper = CharakterVorteileWrapper.CharakterVorteileWrapper()
        self.ItmWrapper = CharakterItemsWrapper.CharakterItemsWrapper()
        
        self.ui.tabs.addTab(self.BeschrWrapper.formBeschr, "Beschreibung")
        self.ui.tabs.addTab(self.AttrWrapper.formAttr, "Attribute")
        self.ui.tabs.addTab(self.VortWrapper.formVor, "Vorteile")
        self.ui.tabs.addTab(self.FertWrapper.formFert, "Fertigkeiten")
        self.ui.tabs.addTab(self.FreiWrapper.formFert, "Freie Fertigkeiten")
        self.ui.tabs.addTab(self.UebernatuerlichWrapper.formFert, "Übernatürliches")
        self.ui.tabs.addTab(self.EquipWrapper.formEq, "Ausrüstung")    
        self.ui.tabs.addTab(self.ItmWrapper.formIt, "Inventar")
        
        self.BeschrWrapper.modified.connect(self.updateEP)
        self.AttrWrapper.modified.connect(self.updateEP)
        self.FertWrapper.modified.connect(self.updateEP)
        self.FreiWrapper.modified.connect(self.updateEP)
        self.UebernatuerlichWrapper.modified.connect(self.updateEP)
        self.EquipWrapper.modified.connect(self.updateEP)
        self.VortWrapper.modified.connect(self.updateEP)
        self.ItmWrapper.modified.connect(self.updateEP)
        
        self.ui.tabs.currentChanged.connect(self.reloadAll)
        self.ui.buttonSave.clicked.connect(self.saveButton)
        self.ui.buttonSavePDF.clicked.connect(self.pdfButton)
        self.ui.spinEP.valueChanged.connect(self.epChanged)
        self.formMain.show()
        
    def updateEP(self):
        try:
            if not self.ignoreModified:
                self.ui.spinEP.setValue(Wolke.Char.EPtotal)
                Wolke.Char.aktualisieren()
                self.ui.spinRemaining.setValue(Wolke.Char.EPtotal-Wolke.Char.EPspent)
                if Wolke.Char.EPtotal < Wolke.Char.EPspent:
                    self.ui.spinRemaining.setStyleSheet("QSpinBox { background-color: rgb(200,50,50) }")
                else:
                    self.ui.spinRemaining.setStyleSheet("QSpinBox { background-color: white }")
        except:
            print("Error thrown in CharakterEditor->updateEP")
    
    def epChanged(self):
        Wolke.Char.EPtotal = self.ui.spinEP.value()
        self.updateEP()
    
    def reloadAll(self):
        self.BeschrWrapper.loadBeschreibung()
        self.AttrWrapper.loadAttribute()
        self.EquipWrapper.loadEquipment()
        self.FertWrapper.loadFertigkeiten()
        self.FreiWrapper.loadFreie()
        self.UebernatuerlichWrapper.loadFertigkeiten()
        self.VortWrapper.loadVorteile()
        self.ItmWrapper.loadItems()
        
    def updateAll(self):
        self.ignoreModified = True
        self.BeschrWrapper.updateBeschreibung()
        self.AttrWrapper.updateAttribute()
        self.EquipWrapper.updateEquipment()
        self.FertWrapper.updateFertigkeiten()
        self.FreiWrapper.updateFreie()
        self.UebernatuerlichWrapper.updateFertigkeiten()
        self.VortWrapper.updateVorteile()
        self.ItmWrapper.updateFreie()
        self.updateEP()
        self.ignoreModified = False
        
    def saveButton(self):
        self.updateAll()
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Charakter speichern...","","XML-Datei (*.xml)")
        if ".xml" not in spath:
            spath = spath + ".xml"
        try:
            Wolke.Char.xmlSchreiben(spath)
        except: 
            pass #TODO: Error Handling
    
    def pdfButton(self):
        #TODO: Implement
        pass
    
if __name__ == "__main__":
    #try:
        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        ed = Editor()
        ed.setupMainForm()
        app.exec_() 
    #except:
     #   print("Error manhandled.")
    