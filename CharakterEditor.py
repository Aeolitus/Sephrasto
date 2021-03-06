# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 22:36:35 2017

@author: Aeolitus
"""

from PyQt5 import QtWidgets, QtCore
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
import logging

class Editor(object):
    '''
    Main class for the character editing window. Mostly puts together the
    different parts of the GUI and handles the communication inbetween.
    '''
    def __init__(self, savePathUpdatedCallback, CharacterName=""):
        super().__init__()
        Wolke.DB = Datenbank.Datenbank()
        self.pdfMeister = pdfM.pdfMeister()
        self.savepath = CharacterName
        self.changed = False
        self.savePathUpdatedCallback = savePathUpdatedCallback
        if Wolke.DB.loaded:
            self.noDatabase = False
            self.finishInit()
        else:
            self.noDatabase = True
        
    def finishInit(self):
        Wolke.Char = Charakter.Char() 
        if self.savepath != "":
            Wolke.Char.xmlLesen(self.savepath)
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
        
        self.BeschrWrapper.modified.connect(self.onModified)
        self.AttrWrapper.modified.connect(self.onModified)
        self.FertWrapper.modified.connect(self.onModified)
        self.FreiWrapper.modified.connect(self.onModified)
        self.UebernatuerlichWrapper.modified.connect(self.onModified)
        self.EquipWrapper.modified.connect(self.onModified)
        self.VortWrapper.modified.connect(self.onModified)
        self.ItmWrapper.modified.connect(self.onModified)
        self.EPWrapper.modified.connect(self.onModified)
        
        self.ui.tabs.currentChanged.connect(self.reloadAll)
        self.ui.buttonSave.clicked.connect(self.saveButton)
        self.ui.buttonQuicksave.clicked.connect(self.quicksaveButton)
        self.ui.buttonSavePDF.clicked.connect(self.pdfButton)
        self.ui.spinEP.valueChanged.connect(self.epChanged)
        self.ui.checkReq.stateChanged.connect(self.reqChanged)
        
        self.reloadAll()

        self.formMain.closeEvent = self.closeEvent
        
    def cancelDueToPendingChanges(self, action):
        if self.changed:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle(action)
            messagebox.setText("Sollen die ausstehenden Änderungen gespeichert werden?")
            messagebox.setIcon(QtWidgets.QMessageBox.Question)
            messagebox.addButton(QtWidgets.QPushButton("Ja"), QtWidgets.QMessageBox.YesRole)
            messagebox.addButton(QtWidgets.QPushButton("Nein"), QtWidgets.QMessageBox.NoRole)
            messagebox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.RejectRole)
            result = messagebox.exec_()
            if result == 0:
                self.quicksaveButton()
            elif result == 2:
                return True
        return False

    def closeEvent(self,event):
        self.formMain.setFocus() #make sure editingfinished is called on potential line edits in focus
        if self.cancelDueToPendingChanges("Beenden"):
            event.ignore()
        else:
            Wolke.Reqs = True

    def reqChanged(self):
        Wolke.Reqs = self.ui.checkReq.isChecked()
        epBefore = Wolke.Char.EPspent
        Wolke.Char.aktualisieren()
        self.reloadAll()
        self.updateEP()
        if epBefore != Wolke.Char.EPspent:
            self.changed = True
    
    def onModified(self):
        self.changed = True
        self.updateEP()

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
        self.onModified()
    
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
        self.ItmWrapper.updateItems()
        self.EPWrapper.updateEP()
        self.updateEP()
        self.ignoreModified = False
        
    def saveButton(self):
        if self.savepath != "":
            startDir = self.savepath
        elif os.path.isdir(Wolke.Settings['Pfad-Chars']):
            startDir = os.path.join(Wolke.Settings['Pfad-Chars'], Wolke.Char.name)
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Charakter speichern...",startDir,"XML-Datei (*.xml)")
        if spath == "":
            return
        if ".xml" not in spath:
            spath = spath + ".xml"
            
        if spath.endswith("datenbank.xml"):
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Speichern des Charakters fehlgeschlagen!")
            infoBox.setInformativeText("Ich empfehle, die Regelbasis nicht mit einem Charakter zu überschreiben. \
Versuchs doch bitte nochmal mit einer anderen Zieldatei.")
            infoBox.setWindowTitle("Charakter speichern fehlgeschlagen.")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
            return
        self.savepath = spath
        self.savePathUpdatedCallback()
        self.quicksaveButton()
            
    def quicksaveButton(self):
        self.updateAll()
        if self.savepath == "":
            self.saveButton()
        else:
            try:
                Wolke.Char.xmlSchreiben(self.savepath)
            except Exception as e:
                logging.error("Sephrasto Fehlercode " + str(Wolke.Fehlercode) + ". Exception: " + str(e))
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
        self.changed = False
            
    def pdfButton(self):
        self.updateAll()
        
        result = -1

        check = QtWidgets.QCheckBox("Regelübersicht anhängen")
        if Wolke.Settings['Bogen'] == 'Frag immer nach':
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Charakterbogen wählen")
            messagebox.setText("Welcher Charakterbogen soll genutzt werden?")
            messagebox.setIcon(QtWidgets.QMessageBox.Question)

            check.setCheckState(QtCore.Qt.Unchecked)
            messagebox.setCheckBox(check)
            messagebox.addButton(QtWidgets.QPushButton("  Standard Ilaris-Charakterbogen  "), QtWidgets.QMessageBox.AcceptRole)
            messagebox.addButton(QtWidgets.QPushButton("  Lange Version von Gatsu  "), QtWidgets.QMessageBox.AcceptRole)
            messagebox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.RejectRole)
            result = messagebox.exec_()
        if result == 0 or Wolke.Settings['Bogen'] == 'Standard Ilaris-Charakterbogen':
            self.pdfMeister.setCharakterbogenKurz()
        elif result == 1 or Wolke.Settings['Bogen'] == 'Die lange Version von Gatsu':
            self.pdfMeister.setCharakterbogenLang()
        else:
            return

        # Check if there is a base Charakterbogen.pdf:
        if not os.path.isfile(self.pdfMeister.CharakterBogen.filePath):
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Fehler!")
            messagebox.setText("Konnte " + self.pdfMeister.CharakterBogen.filePath + " nicht im Installationsordner finden")
            messagebox.setIcon(QtWidgets.QMessageBox.Critical)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec_()
            return
        
        if os.path.isfile(self.savepath):
            startDir = os.path.dirname(self.savepath)
        elif os.path.isdir(Wolke.Settings['Pfad-Chars']):
            startDir = Wolke.Settings['Pfad-Chars']
        else:
            startDir = ""

        startDir = os.path.join(startDir, Wolke.Char.name or os.path.splitext(os.path.basename(self.savepath))[0])
            
        # Let the user choose a saving location and name
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Charakterbogen erstellen...",startDir,"PDF-Datei (*.pdf)")
        if spath == "":
            return
        if ".pdf" not in spath:
            spath = spath + ".pdf"
            
        try:
            if Wolke.Settings['Cheatsheet'] or check.checkState() == QtCore.Qt.Checked:
                printRules = True
            else:
                printRules = False
            self.pdfMeister.pdfErstellen(spath, printRules)
        except Exception as e:
            logging.error("Sephrasto Fehlercode " + str(Wolke.Fehlercode) + ". Exception: " + str(e))
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