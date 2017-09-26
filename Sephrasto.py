#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:30:34 2017

@author: Aeolitus
"""
from PyQt5 import QtWidgets, QtCore
import sys
import MainWindow
import CharakterEditor
import DatenbankEdit
import CharakterMain
import DatenbankMain
from Wolke import Wolke

class MainWindowWrapper(object):
    '''
    Main Class responsible for running the entire application. 
    Just shows three buttons and handles the execution of the individual subparts.
    '''
    def __init__(self):
        '''
        Initializes the GUI and connects the buttons.
        '''
        self._version_ = "v0.4.0"
        super().__init__()
            
        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        #self.app.setStyleSheet("*[readOnly=\"true\"] { background-color: #F5F5F5 } QAbstractScrollArea #scrollAreaWidgetContents { background-color: #FFFFFF }")
        self.app.setStyleSheet("""
        *[readOnly=\"true\"] 
        { 
            background-color: #FFFFFF;
            border: none
        } 
        QAbstractScrollArea #scrollAreaWidgetContents 
        { 
            background-color: #FFFFFF 
        }
        """)
        self.Form = QtWidgets.QWidget()
        self.ui = MainWindow.Ui_Form()
        self.ui.setupUi(self.Form)
        self.ui.buttonNew.clicked.connect(self.createNew)
        self.ui.buttonEdit.clicked.connect(self.editExisting)
        self.ui.buttonRules.clicked.connect(self.editRuleset)
        self.ui.labelVersion.setText(self._version_ + " - by Aeolitus ")
        self.Form.show()
        sys.exit(self.app.exec_())
        
    def createNew(self):
        '''
        Creates a new CharakterEditor which is empty and shows it.
        If the folder this script is in does not contain a datenbank.xml or
        regelbasis.xml, it prompts the user for a valid one first. If either 
        of the xml files cannot be parsed properly, it will display an infobox
        and exit.
        '''
        self.ed = CharakterEditor.Editor()
        if self.ed.noDatabase:
            spathDB, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Regelbasis wählen... ","","XML-Datei (*.xml)")
            if ".xml" not in spathDB:
                spathDB = spathDB + ".xml"
            Wolke.DB.datei = spathDB
            try:
                Wolke.DB.xmlLaden()
                self.ed.finishInit("")
            except:
                infoBox = QtWidgets.QMessageBox()
                infoBox.setIcon(QtWidgets.QMessageBox.Information)
                infoBox.setText("Regelbasis öffnen fehlgeschlagen")
                infoBox.setInformativeText("Die XML-Datei konnte nicht gelesen werden. Ist sie mit dieser Version von Sephrasto kompatibel?")
                infoBox.setWindowTitle("Fehlerhafte Datei")
                infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
                infoBox.exec_()
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        self.ed.formMain.show()
        
    def editExisting(self):
        '''
        Creates a CharakterEditor for an existing character and shows it.
        If the folder this script is in does not contain a datenbank.xml or
        regelbasis.xml, it prompts the user for a valid one first. If either 
        of the xml files cannot be parsed properly, it will display an infobox
        and exit.
        '''
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Charakter laden...","","XML-Datei (*.xml)")
        if spath == "":
            return
        if ".xml" not in spath:
            spath = spath + ".xml"
        try:
            self.ed = CharakterEditor.Editor(spath)
        except:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Charakterdatei öffnen fehlgeschlagen")
            infoBox.setInformativeText("Die XML-Datei konnte nicht gelesen werden. Ist sie mit dieser Version von Sephrasto kompatibel?")
            infoBox.setWindowTitle("Fehlerhafte Datei")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
        else:
            if self.ed.noDatabase:
                spathDB, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Regelbasis wählen... ","","XML-Datei (*.xml)")
                if ".xml" not in spathDB:
                    spathDB = spathDB + ".xml"
                Wolke.DB.datei = spathDB
                try:
                    Wolke.DB.xmlLaden()
                    self.ed.finishInit(spath)
                except:
                    infoBox = QtWidgets.QMessageBox()
                    infoBox.setIcon(QtWidgets.QMessageBox.Information)
                    infoBox.setText("Regelbasis öffnen fehlgeschlagen")
                    infoBox.setInformativeText("Die XML-Datei konnte nicht gelesen werden. Ist sie mit dieser Version von Sephrasto kompatibel?")
                    infoBox.setWindowTitle("Fehlerhafte Datei")
                    infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
                    infoBox.exec_()
            self.ed.formMain = QtWidgets.QWidget()
            self.ed.ui = CharakterMain.Ui_formMain()
            self.ed.ui.setupUi(self.ed.formMain)
            self.ed.ui.tabs.removeTab(0)
            self.ed.ui.tabs.removeTab(0)
            self.ed.setupMainForm()
            self.ed.formMain.show()
        
    def editRuleset(self):
        '''
        Creates the DatenbankEdit Form and shows it. If the folder contains a 
        datenbank.xml, it shows that; alternatively, if there is a file called
        regelbasis.xml, that one will be shown. Otherwise, the rulebase remains
        empty at first.
        '''
        self.D = DatenbankEdit.DatenbankEdit()
        self.D.Form = QtWidgets.QWidget()
        self.D.ui = DatenbankMain.Ui_Form()
        self.D.ui.setupUi(self.D.Form)
        self.D.setupGUI()
        self.D.Form.show()
        
if __name__ == "__main__":
    itm = MainWindowWrapper()