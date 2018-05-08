# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:52 2018

@author: Aeolitus
"""
from Wolke import Wolke
import Einstellungen
from PyQt5 import QtWidgets, QtCore
import os.path
import yaml
import logging

class EinstellungenWrapper():    
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QDialog()
        self.ui = Einstellungen.Ui_SettingsWindow()
        self.ui.setupUi(self.form)
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.checkCheatsheet.setChecked(Wolke.Settings['Cheatsheet'])
        self.ui.comboBogen.setCurrentText(Wolke.Settings['Bogen'])
        
        if Wolke.Settings['Pfad-Chars'] == '':
            self.resetCharPath()
        else:
            self.ui.editChar.setText(Wolke.Settings['Pfad-Chars'])
        
        if Wolke.Settings['Pfad-Regeln'] == '':
            self.resetRulePath()
        else:
            self.ui.editRegeln.setText(Wolke.Settings['Pfad-Regeln'])

        optionsList = ['Keine']            
        if os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            for file in os.listdir(Wolke.Settings['Pfad-Regeln']):
                if file.lower().endswith('.xml'):
                    optionsList.append(file)
        self.ui.comboRegelbasis.clear()
        self.ui.comboRegelbasis.addItems(optionsList)
        if Wolke.Settings['Datenbank'] in optionsList:
            self.ui.comboRegelbasis.setCurrentText(Wolke.Settings['Datenbank'])
            
        self.ui.checkPDFOpen.setChecked(Wolke.Settings['PDF-Open'])
        
        self.ui.comboLogging.setCurrentIndex(Wolke.Settings['Logging'])
            
        self.ui.buttonChar.clicked.connect(self.setCharPath)
        self.ui.buttonRegeln.clicked.connect(self.setRulePath)
        self.ui.resetChar.clicked.connect(self.resetCharPath)
        self.ui.resetRegeln.clicked.connect(self.resetRulePath)
        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            if not os.path.isdir(os.path.join(os.path.expanduser('~'),'Sephrasto')):
                os.mkdir(os.path.join(os.path.expanduser('~'),'Sephrasto'))
                os.mkdir(os.path.join(os.path.expanduser('~'),'Sephrasto', 'Charaktere'))
                os.mkdir(os.path.join(os.path.expanduser('~'),'Sephrasto', 'Regeln'))
            
            Wolke.Settings['Bogen'] = self.ui.comboBogen.currentText()
            db = self.ui.comboRegelbasis.currentText()
            if db == 'Keine':
                Wolke.Settings['Datenbank'] = 'datenbank_user.xml'
            else:
                Wolke.Settings['Datenbank'] = db
            Wolke.Settings['Cheatsheet'] = self.ui.checkCheatsheet.isChecked()
            if os.path.isdir(self.ui.editChar.text()):
                Wolke.Settings['Pfad-Chars'] = self.ui.editChar.text()
            else:
                Wolke.Settings['Pfad-Chars'] = ''
            if os.path.isdir(self.ui.editRegeln.text()):
                Wolke.Settings['Pfad-Regeln'] = self.ui.editRegeln.text()
            else:
                Wolke.Settings['Pfad-Regeln'] = ''
                
            Wolke.Settings['Logging'] = self.ui.comboLogging.currentIndex()
            loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
            logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])
            
            Wolke.Settings['PDF-Open'] = self.ui.checkPDFOpen.isChecked()
            
            SettingsPath = os.path.join(os.path.expanduser('~'),'Sephrasto', 
                                        'Sephrasto.ini')
            with open(SettingsPath, 'w') as outfile:
                yaml.dump(Wolke.Settings, outfile)
    
    
    def setCharPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Charaktere aus!",
          Wolke.Settings['Pfad-Chars'],
          QtWidgets.QFileDialog.ShowDirsOnly)
        if os.path.isdir(path):
            Wolke.Settings['Pfad-Chars'] = path
            self.ui.editChar.setText(path)
            
    def setRulePath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Regeln aus!",
          Wolke.Settings['Pfad-Regeln'],
          QtWidgets.QFileDialog.ShowDirsOnly)
        if os.path.isdir(path):
            Wolke.Settings['Pfad-Regeln'] = path
            self.ui.editRegeln.setText(path)
            
    def resetCharPath(self):
        p = os.path.expanduser('~')
        p = os.path.join(p, 'Sephrasto', 'Charaktere')
        Wolke.Settings['Pfad-Chars'] = p
        self.ui.editChar.setText(p)
        
    def resetRulePath(self):
        p = os.path.expanduser('~')
        p = os.path.join(p, 'Sephrasto', 'Regeln')
        Wolke.Settings['Pfad-Regeln'] = p
        self.ui.editRegeln.setText(p)
        
        