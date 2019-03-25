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
import sys

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
        self.comboBogenIndexChanged()
        self.ui.comboFontSize.setCurrentIndex(Wolke.Settings['Cheatsheet-Fontsize'])

        if Wolke.Settings['Pfad-Chars'] == '':
            self.resetCharPath()
        else:
            self.ui.editChar.setText(Wolke.Settings['Pfad-Chars'])
        
        if Wolke.Settings['Pfad-Regeln'] == '':
            self.resetRulePath()
        else:
            self.ui.editRegeln.setText(Wolke.Settings['Pfad-Regeln'])

        self.ui.editExportPlugin.setText(Wolke.Settings['Pfad-Export-Plugin'])

        self.updateComboRegelbasis()
            
        self.ui.checkPDFOpen.setChecked(Wolke.Settings['PDF-Open'])
        
        self.ui.comboLogging.setCurrentIndex(Wolke.Settings['Logging'])
            
        self.ui.buttonChar.clicked.connect(self.setCharPath)
        self.ui.buttonRegeln.clicked.connect(self.setRulePath)
        self.ui.buttonExportPlugin.clicked.connect(self.setExportPluginPath)
        self.ui.resetChar.clicked.connect(self.resetCharPath)
        self.ui.resetRegeln.clicked.connect(self.resetRulePath)
        self.ui.resetExportPlugin.clicked.connect(self.resetExportPluginPath)
        self.ui.comboBogen.currentIndexChanged.connect(self.comboBogenIndexChanged)

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            userFolder = os.path.expanduser('~')
            if sys.platform.startswith("win"):
                import ctypes.wintypes
                CSIDL_PERSONAL = 5       # My Documents
                SHGFP_TYPE_CURRENT = 0   # Get current, not default value
                buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
                userFolder = buf.value or userFolder

            sephrastoFolder = os.path.join(userFolder,'Sephrasto')
            if not os.path.isdir(sephrastoFolder):
                os.mkdir(sephrastoFolder)
                os.mkdir(os.path.join(sephrastoFolder, 'Charaktere'))
                os.mkdir(os.path.join(sephrastoFolder, 'Regeln'))
            
            Wolke.Settings['Bogen'] = self.ui.comboBogen.currentText()
            db = self.ui.comboRegelbasis.currentText()
            if db == 'Keine':
                Wolke.Settings['Datenbank'] = None
            else:
                Wolke.Settings['Datenbank'] = db
            Wolke.Settings['Cheatsheet'] = self.ui.checkCheatsheet.isChecked()
            Wolke.Settings['Cheatsheet-Fontsize'] = self.ui.comboFontSize.currentIndex()

            if os.path.isdir(self.ui.editChar.text()):
                Wolke.Settings['Pfad-Chars'] = self.ui.editChar.text()
            else:
                Wolke.Settings['Pfad-Chars'] = ''
            if os.path.isdir(self.ui.editRegeln.text()):
                Wolke.Settings['Pfad-Regeln'] = self.ui.editRegeln.text()
            else:
                Wolke.Settings['Pfad-Regeln'] = ''

            if os.path.isfile(self.ui.editExportPlugin.text()):
                Wolke.Settings['Pfad-Export-Plugin'] = self.ui.editExportPlugin.text()
            else:
                Wolke.Settings['Pfad-Export-Plugin'] = ''
                
            Wolke.Settings['Logging'] = self.ui.comboLogging.currentIndex()
            loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
            logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])
            
            Wolke.Settings['PDF-Open'] = self.ui.checkPDFOpen.isChecked()
            
            SettingsPath = os.path.join(os.path.expanduser('~'),'Sephrasto', 
                                        'Sephrasto.ini')
            with open(SettingsPath, 'w') as outfile:
                yaml.dump(Wolke.Settings, outfile)

    def comboBogenIndexChanged(self):
        self.ui.checkCheatsheet.setEnabled(self.ui.comboBogen.currentIndex() != 0)
        if not self.ui.checkCheatsheet.isEnabled():
            self.ui.checkCheatsheet.setChecked(False)

    def updateComboRegelbasis(self):
        optionsList = ['Keine']            
        if os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            for file in os.listdir(Wolke.Settings['Pfad-Regeln']):
                if file.lower().endswith('.xml'):
                    optionsList.append(file)
        self.ui.comboRegelbasis.clear()
        self.ui.comboRegelbasis.addItems(optionsList)
        if Wolke.Settings['Datenbank'] in optionsList:
            self.ui.comboRegelbasis.setCurrentText(Wolke.Settings['Datenbank'])

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
            self.updateComboRegelbasis()

    def setExportPluginPath(self):
        path = QtWidgets.QFileDialog.getOpenFileName(None,
          "Wähle einen Speicherort für das Export-Plugin aus!",
          Wolke.Settings['Pfad-Export-Plugin'], 'Python scripts (*.py)', None,
          QtWidgets.QFileDialog.ShowDirsOnly)
        if os.path.isfile(path[0]):
            Wolke.Settings['Pfad-Export-Plugin'] = path[0]
            self.ui.editExportPlugin.setText(path[0])
            
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
        
    def resetExportPluginPath(self):
        Wolke.Settings['Pfad-Export-Plugin'] = ''
        self.ui.editExportPlugin.setText('')
        