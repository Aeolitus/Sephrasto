# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 22:36:35 2017

@author: Aeolitus
"""

from PyQt5 import QtWidgets
import CharakterBeschreibungWrapper
import CharakterAttributeWrapper
import CharakterEquipmentWrapper
import CharakterFertigkeitenWrapper
import CharakterUebernatuerlichWrapper
import CharakterFreieFertWrapper
import CharakterVorteileWrapper
import CharakterItemsWrapper
import CharakterEPWrapper
import Charakter
import Datenbank
from Wolke import Wolke
import os.path
import pdfMeister as pdfM


class Editor(object):
    '''
    Main class for the character editing window. Mostly puts together the
    different parts of the GUI and handles the communication inbetween.
    '''
    def __init__(self, CharacterName=""):
        super().__init__()
        Wolke.DB = Datenbank.Datenbank()
        self.pdfMeister = pdfM.pdfMeister()
        if Wolke.DB.root is not None:
            self.noDatabase = False
            self.finishInit(CharacterName)
        else:
            self.noDatabase = True
        
    def finishInit(self, CharacterName):
        Wolke.Char = Charakter.Char() 
        if CharacterName != "":
            Wolke.Char.xmlLesen(CharacterName)
        Wolke.Char.aktualisieren() # A bit later because it needs access to itself
        
        self.ignoreModified = False
        
    def setupMainForm(self):      
        self.updateEP()
        
        self.BeschrWrapper = CharakterBeschreibungWrapper.BeschrWrapper()
        self.AttrWrapper = CharakterAttributeWrapper.AttrWrapper()
        self.FertWrapper = CharakterFertigkeitenWrapper.FertigkeitenWrapper()
        self.FreiWrapper = CharakterFreieFertWrapper.CharakterFreieFertWrapper()
        self.UebernatuerlichWrapper = CharakterUebernatuerlichWrapper.UebernatuerlichWrapper()
        self.EquipWrapper = CharakterEquipmentWrapper.EquipWrapper()
        self.VortWrapper = CharakterVorteileWrapper.CharakterVorteileWrapper()
        self.ItmWrapper = CharakterItemsWrapper.CharakterItemsWrapper()
        self.EPWrapper = CharakterEPWrapper.EPWrapper()
        
        self.ui.tabs.addTab(self.BeschrWrapper.formBeschr, "    Beschreibung    ")
        self.ui.tabs.addTab(self.AttrWrapper.formAttr, "    Attribute    ")
        self.ui.tabs.addTab(self.VortWrapper.formVor, "    Vorteile    ")
        self.ui.tabs.addTab(self.FertWrapper.formFert, "    Fertigkeiten    ")
        self.ui.tabs.addTab(self.FreiWrapper.formFert, "    Freie Fertigkeiten    ")
        self.ui.tabs.addTab(self.UebernatuerlichWrapper.formFert, "    Übernatürliches    ")
        self.ui.tabs.addTab(self.EquipWrapper.formEq, "    Ausrüstung    ")    
        self.ui.tabs.addTab(self.ItmWrapper.formIt, "    Inventar    ")
        self.ui.tabs.addTab(self.EPWrapper.formEP, "    EP-Verteilung    ")
        
        self.BeschrWrapper.modified.connect(self.updateEP)
        self.AttrWrapper.modified.connect(self.updateEP)
        self.FertWrapper.modified.connect(self.updateEP)
        self.FreiWrapper.modified.connect(self.updateEP)
        self.UebernatuerlichWrapper.modified.connect(self.updateEP)
        self.EquipWrapper.modified.connect(self.updateEP)
        self.VortWrapper.modified.connect(self.updateEP)
        self.ItmWrapper.modified.connect(self.updateEP)
        self.EPWrapper.modified.connect(self.updateEP)
        
        self.ui.tabs.currentChanged.connect(self.reloadAll)
        self.ui.buttonSave.clicked.connect(self.saveButton)
        self.ui.buttonSavePDF.clicked.connect(self.pdfButton)
        self.ui.spinEP.valueChanged.connect(self.epChanged)
        self.ui.checkReq.stateChanged.connect(self.reqChanged)
        
        self.reloadAll()
        
    def reqChanged(self):
        Wolke.Reqs = self.ui.checkReq.isChecked()
        Wolke.Char.aktualisieren()
        self.reloadAll()
        
    def updateEP(self):
        if not self.ignoreModified:
            self.ui.spinEP.setValue(Wolke.Char.EPtotal)
            Wolke.Char.aktualisieren()
            self.ui.spinRemaining.setValue(Wolke.Char.EPtotal-Wolke.Char.EPspent)
            if Wolke.Char.EPtotal < Wolke.Char.EPspent:
                self.ui.spinRemaining.setStyleSheet("QSpinBox { background-color: rgb(200,50,50) }")
            else:
                self.ui.spinRemaining.setStyleSheet("QSpinBox { background-color: #FFFFFF}")
            self.ui.spinSpent.setStyleSheet("QSpinBox { background-color: #FFFFFF}")
            self.ui.spinSpent.setValue(Wolke.Char.EPspent)
    
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
        self.EPWrapper.loadEP()
        
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
        self.EPWrapper.updateEP()
        self.updateEP()
        self.ignoreModified = False
        
    def saveButton(self):
        self.updateAll()
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Charakter speichern...","","XML-Datei (*.xml)")
        if spath == "":
            return
        if ".xml" not in spath:
            spath = spath + ".xml"
        try:
            Wolke.Char.xmlSchreiben(spath)
        except:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Speichern des Charakters fehlgeschlagen!")
            infoBox.setInformativeText("Beim Speichern des Charakters ist ein Fehler aufgetreten!\n\
Fehlercode: " + str(Wolke.Fehlercode) + "\n\
Fehlermeldung: " + Wolke.ErrorCode[Wolke.Fehlercode] + "\n")
            infoBox.setWindowTitle("Charakter speichern fehlgeschlagen.")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
    
    def pdfButton(self):
        self.updateAll()
        # Check if there is a base Charakterbogen.pdf:
        if not os.path.isfile(self.pdfMeister.CharakterBogen):
            spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Leeren Charakterbogen auswählen...","","PDF-Datei (*.pdf)")
            if spath == "":
                return
            if ".pdf" not in spath:
                spath = spath + ".pdf"
            self.pdfMeister.CharakterBogen = spath
        
        # Let the user choose a saving location and name
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Charakterbogen erstellen...","","PDF-Datei (*.pdf)")
        if spath == "":
            return
        if ".pdf" not in spath:
            spath = spath + ".pdf"
            
        try:
            self.pdfMeister.pdfErstellen(spath)
        except:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("PDF-Erstellung fehlgeschlagen!")
            infoBox.setInformativeText("Beim Erstellen des Charakterbogens ist ein Fehler aufgetreten.\n\
Fehlercode: " + str(Wolke.Fehlercode) + "\n\
Fehlermeldung: " + Wolke.ErrorCode[Wolke.Fehlercode] + "\n")
            infoBox.setWindowTitle("PDF-Erstellung fehlgeschlagen.")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()