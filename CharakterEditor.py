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
import CharakterNotizWrapper
import Charakter
import Datenbank
from Wolke import Wolke
import os.path
import pdfMeister as pdfM
from pdfMeister import CharakterbogenInfo
import logging
from EventBus import EventBus

class Tab():
    def __init__(self, order, wrapper, form, name):
        self.order = order
        self.wrapper = wrapper
        self.form = form
        self.name = name

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
        
        EventBus.doAction("charakter_geladen", { "neu" : self.savepath == "", "filepath" : self.savepath })
        self.ignoreModified = False
        
    def setupMainForm(self, plugins):      
        self.ui.progressBar.setVisible(False)
        self.updateEP()

        self.BeschrWrapper = EventBus.applyFilter("class_beschreibung_wrapper", CharakterBeschreibungWrapper.BeschrWrapper)()
        self.AttrWrapper = EventBus.applyFilter("class_attribute_wrapper", CharakterAttributeWrapper.AttrWrapper)()
        self.FertWrapper = EventBus.applyFilter("class_fertigkeiten_wrapper", CharakterFertigkeitenWrapper.FertigkeitenWrapper)()
        self.FreiWrapper = EventBus.applyFilter("class_freiefertigkeiten_wrapper", CharakterFreieFertWrapper.CharakterFreieFertWrapper)()
        self.UebernatuerlichWrapper = EventBus.applyFilter("class_uebernatuerlichefertigkeiten_wrapper", CharakterUebernatuerlichWrapper.UebernatuerlichWrapper)()
        self.EquipWrapper = EventBus.applyFilter("class_ausruestung_wrapper", CharakterEquipmentWrapper.EquipWrapper)()
        self.VortWrapper = EventBus.applyFilter("class_vorteile_wrapper", CharakterVorteileWrapper.CharakterVorteileWrapper)()
        self.ItmWrapper = EventBus.applyFilter("class_items_wrapper", CharakterItemsWrapper.CharakterItemsWrapper)()
        self.EPWrapper = EventBus.applyFilter("class_ep_wrapper", CharakterEPWrapper.EPWrapper)()
        self.NotizWrapper = EventBus.applyFilter("class_notiz_wrapper", CharakterNotizWrapper.CharakterNotizWrapper)()
        
        tabs = []
        tabs.append(Tab(10, self.BeschrWrapper, self.BeschrWrapper.formBeschr, "Beschreibung"))
        tabs.append(Tab(30, self.AttrWrapper, self.AttrWrapper.formAttr, "Attribute"))
        tabs.append(Tab(40, self.VortWrapper, self.VortWrapper.formVor, "Vorteile"))
        tabs.append(Tab(50, self.FertWrapper, self.FertWrapper.formFert, "Fertigkeiten"))
        tabs.append(Tab(60, self.FreiWrapper, self.FreiWrapper.formFert, "Freie Fertigkeiten"))
        tabs.append(Tab(70, self.UebernatuerlichWrapper, self.UebernatuerlichWrapper.formFert, "Übernatürliches"))
        tabs.append(Tab(80, self.EquipWrapper, self.EquipWrapper.formEq, "Ausrüstung"))   
        tabs.append(Tab(90, self.ItmWrapper, self.ItmWrapper.formIt, "Inventar"))
        tabs.append(Tab(100, self.EPWrapper, self.EPWrapper.formEP, "EP-Verteilung"))
        tabs.append(Tab(110, self.NotizWrapper, self.NotizWrapper.form, "Notiz"))

        for plugin in [p.plugin for p in plugins]:
            if hasattr(plugin, "createCharakterTabs"):
                for tab in plugin.createCharakterTabs():
                   tabs.append(tab)

            if hasattr(plugin, "createCharakterButtons"):
                for button in plugin.createCharakterButtons():
                    self.ui.horizontalLayout_3.addWidget(button)
        
        self.tabs = sorted(tabs, key=lambda tab: tab.order)
        for tab in self.tabs:
            self.ui.tabs.addTab(tab.form, tab.name)
            if hasattr(tab.wrapper, "modified"):
                tab.wrapper.modified.connect(self.onModified)
        
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
                self.ui.spinRemaining.setStyleSheet("")
            self.ui.spinSpent.setStyleSheet("")
            self.ui.spinSpent.setValue(Wolke.Char.EPspent)
    
    def epChanged(self):
        Wolke.Char.EPtotal = self.ui.spinEP.value()
        self.onModified()
    
    def reloadAll(self):
        for tab in self.tabs:
            if hasattr(tab.wrapper, "load"):
                tab.wrapper.load()

        self.updateEP()
        self.ui.tabs.setTabVisible(self.ui.tabs.indexOf(self.UebernatuerlichWrapper.formFert), len(Wolke.Char.übernatürlicheFertigkeiten) > 0)
        
    def updateAll(self):
        self.ignoreModified = True
        for tab in self.tabs:
            if hasattr(tab.wrapper, "update"):
                tab.wrapper.update()

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

    def showProgressBar(self, show):
        self.ui.tabs.setEnabled(not show)
        self.ui.spinEP.setEnabled(not show)
        self.ui.spinRemaining.setEnabled(not show)
        self.ui.spinSpent.setEnabled(not show)
        self.ui.checkReq.setEnabled(not show)
        self.ui.buttonQuicksave.setVisible(not show)
        self.ui.buttonSave.setVisible(not show)
        self.ui.buttonSavePDF.setVisible(not show)
        self.ui.progressBar.setVisible(show)
      
    def pdfMeisterProgressCallback(self, progress):
        self.ui.progressBar.setValue(progress)

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

        charakterBogen = None
        if result == 0 or Wolke.Settings['Bogen'] == 'Standard Ilaris-Charakterbogen':
            charakterBogen = CharakterbogenInfo(filePath="Charakterbogen.pdf", maxVorteile = 8, maxFreie = 12, maxFertigkeiten = 2, seitenProfan = 2, kurzbogenHack=True)
        elif result == 1 or Wolke.Settings['Bogen'] == 'Die lange Version von Gatsu':
            charakterBogen = CharakterbogenInfo(filePath="Charakterbogen_lang.pdf", maxVorteile = 24, maxFreie = 28, maxFertigkeiten = 28, seitenProfan = 3, kurzbogenHack=False)
        else:
            return

        self.pdfMeister.setCharakterbogen(EventBus.applyFilter("set_charakterbogen", charakterBogen))

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

            self.showProgressBar(True)
            self.pdfMeister.pdfErstellen(spath, printRules, self.pdfMeisterProgressCallback)
            self.showProgressBar(False)
        except Exception as e:
            logging.error("Sephrasto Fehlercode " + str(Wolke.Fehlercode) + ". Exception: " + str(e))
            self.showProgressBar(False)
            self.ui.tabs.setEnabled(True)
            self.ui.buttonQuicksave.setVisible(True)
            self.ui.buttonSave.setVisible(True)
            self.ui.buttonSavePDF.setVisible(True)
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