# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:52 2018

@author: Aeolitus
"""
from Wolke import Wolke
import UI.Einstellungen
from PyQt5 import QtWidgets, QtCore
import os.path
import yaml
import logging
import sys
from Hilfsmethoden import Hilfsmethoden

class EinstellungenWrapper():    
    def __init__(self, plugins):
        super().__init__()

        self.plugins = plugins
        self.form = QtWidgets.QDialog()
        self.ui = UI.Einstellungen.Ui_SettingsWindow()
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
        self.updatePluginCheckboxes(self.plugins)
        self.updateComboRegelbasis()
            
        self.ui.checkPDFOpen.setChecked(Wolke.Settings['PDF-Open'])
        
        self.ui.checkUpdate.setChecked(not Wolke.Settings['UpdateCheck_Disable'])
        self.ui.comboLogging.setCurrentIndex(Wolke.Settings['Logging'])
        self.ui.comboTheme.setCurrentText(Wolke.Settings['Theme'])
            
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
            needRestart = False

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

            if self.ui.editPlugins.text() != Wolke.Settings['Pfad-Plugins']:
                if os.path.isdir(self.ui.editPlugins.text()):
                    Wolke.Settings['Pfad-Plugins'] = self.ui.editPlugins.text()
                else:
                    Wolke.Settings['Pfad-Plugins'] = ''
                needRestart = True

            for checkbox in self.pluginCheckboxes:
                if checkbox.isChecked() and (checkbox.text() in Wolke.Settings['Deaktivierte-Plugins']):
                    Wolke.Settings['Deaktivierte-Plugins'].remove(checkbox.text())
                    needRestart = True
                elif not checkbox.isChecked() and not (checkbox.text() in Wolke.Settings['Deaktivierte-Plugins']):
                    Wolke.Settings['Deaktivierte-Plugins'].append(checkbox.text())
                    needRestart = True
              
            Wolke.Settings['UpdateCheck_Disable'] = not self.ui.checkUpdate.isChecked()
            Wolke.Settings['Logging'] = self.ui.comboLogging.currentIndex()
            loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
            logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])
            
            Wolke.Settings['PDF-Open'] = self.ui.checkPDFOpen.isChecked()

            if Wolke.Settings['Theme'] != self.ui.comboTheme.currentText():
                Wolke.Settings['Theme'] = self.ui.comboTheme.currentText()
                needRestart = True

            EinstellungenWrapper.save()

            if needRestart:
                messageBox = QtWidgets.QMessageBox()
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setWindowTitle("Sephrasto neustarten?")
                messageBox.setText("Sephrasto muss bei Änderungen an Plugin- oder Theme-Einstellungen neugestartet werden.")
                messageBox.addButton(QtWidgets.QPushButton("Neustarten"), QtWidgets.QMessageBox.YesRole)
                messageBox.addButton(QtWidgets.QPushButton("Später"), QtWidgets.QMessageBox.RejectRole)
                messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
                result = messageBox.exec_()
                if result == 0:
                    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

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

    def updatePluginCheckboxes(self, plugins):
        self.pluginCheckboxes = []
        for i in reversed(range(self.ui.gbPlugins.layout().count())): 
            self.ui.gbPlugins.layout().itemAt(i).widget().setParent(None)

        officialPlugins = [p for p in plugins if p.isOfficial]
        if len(officialPlugins) > 0:
            self.ui.gbPlugins.layout().addWidget(QtWidgets.QLabel("Offizielle Plugins:"))
        for pluginData in officialPlugins:
            check = QtWidgets.QCheckBox(pluginData.name)
            if pluginData.description:
                check.setToolTip(pluginData.description)

            if not (pluginData.name in Wolke.Settings['Deaktivierte-Plugins']):
                check.setChecked(True)
            self.ui.gbPlugins.layout().addWidget(check)
            self.pluginCheckboxes.append(check)

        userPlugins = [p for p in plugins if not p.isOfficial]
        if len(userPlugins) > 0:
            self.ui.gbPlugins.layout().addWidget(QtWidgets.QLabel("Nutzer-Plugins:"))
        for pluginData in userPlugins:
            check = QtWidgets.QCheckBox(pluginData.name)
            if pluginData.description:
                check.setToolTip(pluginData.description)

            if not (pluginData.name in Wolke.Settings['Deaktivierte-Plugins']):
                check.setChecked(True)
            self.ui.gbPlugins.layout().addWidget(check)
            self.pluginCheckboxes.append(check)

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
            self.updatePluginCheckboxes([p for p in self.plugins if p.isOfficial])

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
        self.updatePluginCheckboxes([p for p in self.plugins if p.isOfficial])