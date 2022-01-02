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
from PluginLoader import PluginLoader
from Hilfsmethoden import Hilfsmethoden

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

        self.settingsFolder = EinstellungenWrapper.getSettingsFolder()
        self.ui.editChar.setText(Wolke.Settings['Pfad-Chars'])
        self.ui.editRegeln.setText(Wolke.Settings['Pfad-Regeln'])
        self.ui.editPlugins.setText(Wolke.Settings['Pfad-Plugins'])

        self.pluginCheckboxes = []
        self.updatePluginCheckboxes()
        self.updateComboRegelbasis()
            
        self.ui.checkPDFOpen.setChecked(Wolke.Settings['PDF-Open'])
        
        self.ui.comboLogging.setCurrentIndex(Wolke.Settings['Logging'])
            
        self.ui.buttonChar.clicked.connect(self.setCharPath)
        self.ui.buttonRegeln.clicked.connect(self.setRulePath)
        self.ui.buttonPlugins.clicked.connect(self.setPluginsPath)
        self.ui.resetChar.clicked.connect(self.resetCharPath)
        self.ui.resetRegeln.clicked.connect(self.resetRulePath)
        self.ui.resetPlugins.clicked.connect(self.resetPluginsPath)
        self.ui.comboBogen.currentIndexChanged.connect(self.comboBogenIndexChanged)

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
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

            if os.path.isdir(self.ui.editPlugins.text()):
                Wolke.Settings['Pfad-Plugins'] = self.ui.editPlugins.text()
            else:
                Wolke.Settings['Pfad-Plugins'] = ''

            for checkbox in self.pluginCheckboxes:
                if checkbox.isChecked() and (checkbox.text() in Wolke.Settings['Deaktivierte-Plugins']):
                    Wolke.Settings['Deaktivierte-Plugins'].remove(checkbox.text())
                elif not checkbox.isChecked() and not (checkbox.text() in Wolke.Settings['Deaktivierte-Plugins']):
                    Wolke.Settings['Deaktivierte-Plugins'].append(checkbox.text())
                
            Wolke.Settings['Logging'] = self.ui.comboLogging.currentIndex()
            loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
            logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])
            
            Wolke.Settings['PDF-Open'] = self.ui.checkPDFOpen.isChecked()
            
            EinstellungenWrapper.save()

    @staticmethod
    def getSettingsFolder():
        userFolder = os.path.expanduser('~')
        if sys.platform.startswith("win"):
            import ctypes.wintypes
            CSIDL_PERSONAL = 5       # My Documents
            SHGFP_TYPE_CURRENT = 0   # Get current, not default value
            buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            userFolder = buf.value or userFolder
        return os.path.join(userFolder,'Sephrasto')

    @staticmethod
    def createUserFolders(basePath):
        if not os.path.isdir(basePath):
            try:
                os.mkdir(basePath)
                if not os.path.isdir(os.path.join(basePath, 'Charaktere')):
                    os.mkdir(os.path.join(basePath, 'Charaktere'))
                if not os.path.isdir(os.path.join(basePath, 'Regeln')):
                    os.mkdir(os.path.join(basePath, 'Regeln'))
                if not os.path.isdir(os.path.join(basePath, 'Plugins')):
                    os.mkdir(os.path.join(basePath, 'Plugins'))
            except:
                messagebox = QtWidgets.QMessageBox()
                messagebox.setWindowTitle("Fehler!")
                messagebox.setText("Konnte den Sephrasto Ordner in deinem Nutzerverzeichnis nicht erstellen (" + basePath + "). Bitte stelle sicher, dass Sephrasto die nötigen Schreibrechte hat und dein Antivirus Programm den Zugriff nicht blockiert. Sephrasto wird sonst nicht richtig funktionieren.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messagebox.exec_()

    @staticmethod
    def load():
        settingsFolder = EinstellungenWrapper.getSettingsFolder()
        EinstellungenWrapper.createUserFolders(settingsFolder)
        settingsPath = os.path.join(settingsFolder, 'Sephrasto.ini')
        if os.path.isfile(settingsPath):
            with open(settingsPath,'r') as infile:
                tmpSet = yaml.safe_load(infile)
                for el in tmpSet:
                    Wolke.Settings[el] = tmpSet[el]
                if not 'Version' in tmpSet:
                    Wolke.Settings['Version'] = 0

                #Settings migration code goes here, dont forget to increment the base version in Wolke.py too
                if Wolke.Settings['Version'] == 0:
                    if not 'CharakterBeschreibungExt' in Wolke.Settings['Deaktivierte-Plugins']:
                        Wolke.Settings['Deaktivierte-Plugins'].append('CharakterBeschreibungExt')
                    Wolke.Settings['Version'] += 1
        
        #Init defaults
        if not Wolke.Settings['Pfad-Chars']:
            Wolke.Settings['Pfad-Chars'] = os.path.join(settingsFolder, 'Charaktere')
        if not Wolke.Settings['Pfad-Regeln']:
            Wolke.Settings['Pfad-Regeln'] = os.path.join(settingsFolder, 'Regeln')
        if not Wolke.Settings['Pfad-Plugins']:
            Wolke.Settings['Pfad-Plugins'] = os.path.join(settingsFolder, 'Plugins')

    @staticmethod
    def save():
        settingsFolder = EinstellungenWrapper.getSettingsFolder()
        EinstellungenWrapper.createUserFolders(settingsFolder)

        settingsPath = os.path.join(settingsFolder, 'Sephrasto.ini')
        with open(settingsPath, 'w') as outfile:
            yaml.dump(Wolke.Settings, outfile)

    def updatePluginCheckboxes(self):
        self.pluginCheckboxes = []
        for i in reversed(range(self.ui.vlPlugins.count())): 
            self.ui.vlPlugins.itemAt(i).widget().setParent(None)

        pluginNames = PluginLoader.getPlugins("Plugins")
        if len(pluginNames) > 0:
            self.ui.vlPlugins.addWidget(QtWidgets.QLabel("Offizielle Plugins:"))
        for pluginName in pluginNames:
            check = QtWidgets.QCheckBox(pluginName)
            if not (pluginName in Wolke.Settings['Deaktivierte-Plugins']):
                check.setChecked(True)
            self.ui.vlPlugins.addWidget(check)
            self.pluginCheckboxes.append(check)

        pluginNames = PluginLoader.getPlugins(self.ui.editPlugins.text())
        if len(pluginNames) > 0:
            self.ui.vlPlugins.addWidget(QtWidgets.QLabel("Nutzer-Plugins:"))
        for pluginName in pluginNames:
            check = QtWidgets.QCheckBox(pluginName)
            if not (pluginName in Wolke.Settings['Deaktivierte-Plugins']):
                check.setChecked(True)
            self.ui.vlPlugins.addWidget(check)
            self.pluginCheckboxes.append(check)

        if len(pluginNames) > 0:
            self.ui.vlPlugins.addWidget(QtWidgets.QLabel("(De-)Aktivieren erfordert einen Neustart!"))

    def comboBogenIndexChanged(self):
        self.ui.checkCheatsheet.setEnabled(self.ui.comboBogen.currentIndex() != 0)
        if not self.ui.checkCheatsheet.isEnabled():
            self.ui.checkCheatsheet.setChecked(False)

    def updateComboRegelbasis(self):
        optionsList = ['Keine']            
        if os.path.isdir(self.ui.editRegeln.text()):
            for file in Hilfsmethoden.listdir(self.ui.editRegeln.text()):
                if file.lower().endswith('.xml'):
                    optionsList.append(file)
        self.ui.comboRegelbasis.clear()
        self.ui.comboRegelbasis.addItems(optionsList)
        if Wolke.Settings['Datenbank'] in optionsList:
            self.ui.comboRegelbasis.setCurrentText(Wolke.Settings['Datenbank'])

    def setCharPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Charaktere aus!",
          self.ui.editChar.text(),
          QtWidgets.QFileDialog.ShowDirsOnly)
        path = os.path.realpath(path)
        if os.path.isdir(path):
            self.ui.editChar.setText(path)
            
    def setRulePath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Regeln aus!",
          self.ui.editRegeln.text(),
          QtWidgets.QFileDialog.ShowDirsOnly)
        path = os.path.realpath(path)
        if os.path.isdir(path):
            self.ui.editRegeln.setText(path)
            self.updateComboRegelbasis()

    def setPluginsPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Plugins aus!",
          self.ui.editPlugins.text(),
          QtWidgets.QFileDialog.ShowDirsOnly)
        path = os.path.realpath(path)
        if os.path.isdir(path):
            self.ui.editPlugins.setText(path)
            self.updatePluginCheckboxes()
            
    def resetCharPath(self):
        p = os.path.join(self.settingsFolder, 'Charaktere')
        self.ui.editChar.setText(p)
        
    def resetRulePath(self):
        p = os.path.join(self.settingsFolder, 'Regeln')
        self.ui.editRegeln.setText(p)
        self.updateComboRegelbasis()
        
    def resetPluginsPath(self):
        p = os.path.join(self.settingsFolder, 'Plugins')
        self.ui.editPlugins.setText(p)
        self.updatePluginCheckboxes()
        