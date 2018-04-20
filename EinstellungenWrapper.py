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
            p = os.path.expanduser('~')
            p = os.path.join(p, 'Sephrasto', 'Charaktere')
            Wolke.Settings['Pfad-Chars'] = p
            self.ui.editChar.setText(p)
        else:
            self.ui.editChar.setText(Wolke.Settings['Pfad-Chars'])
        
        if Wolke.Settings['Pfad-Regeln'] == '':
            p = os.path.expanduser('~')
            p = os.path.join(p, 'Sephrasto', 'Regeln')
            Wolke.Settings['Pfad-Regeln'] = p
            self.ui.editRegeln.setText(p)
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
        
        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
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
                
            with open('Sephrasto.ini', 'w') as outfile:
                yaml.dump(Wolke.Settings, outfile)
    
    
          