# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:52 2018

@author: Aeolitus
"""
from Wolke import Wolke
from Wolke import CharakterbogenInfo
import UI.Einstellungen
from PyQt5 import QtWidgets, QtCore, QtGui
import os.path
import yaml
import logging
import sys
import platform
from Hilfsmethoden import Hilfsmethoden
from PluginLoader import PluginLoader

class EinstellungenWrapper():    
    def __init__(self, plugins):
        super().__init__()

        self.form = QtWidgets.QDialog()
        self.ui = UI.Einstellungen.Ui_SettingsWindow()
        self.ui.setupUi(self.form)
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.ui.checkCheatsheet.setChecked(Wolke.Settings['Cheatsheet'])

        boegen = [os.path.basename(os.path.splitext(bogen)[0]) for bogen in Wolke.Charakterbögen]
        for bogen in boegen:
            if bogen == "Standard Charakterbogen":
                self.ui.comboBogen.insertItem(0, bogen)
            elif bogen == "Langer Charakterbogen":
                self.ui.comboBogen.insertItem(0, bogen)
            else:
                self.ui.comboBogen.addItem(bogen)
        if not (Wolke.Settings['Bogen'] in boegen):
            Wolke.Settings['Bogen'] = self.ui.comboBogen.itemText(0)
        self.ui.comboBogen.setCurrentText(Wolke.Settings['Bogen'])
        self.ui.checkWizard.setChecked(Wolke.Settings['Charakter-Assistent'])
        self.ui.comboFontSize.setCurrentIndex(Wolke.Settings['Cheatsheet-Fontsize'])

        self.settingsFolder = EinstellungenWrapper.getSettingsFolder()
        self.ui.editChar.setText(Wolke.Settings['Pfad-Chars'])
        self.ui.editRegeln.setText(Wolke.Settings['Pfad-Regeln'])
        self.ui.editPlugins.setText(Wolke.Settings['Pfad-Plugins'])

        self.pluginCheckboxes = []
        self.updatePluginCheckboxes(plugins)
        self.updateComboRegelbasis()
            
        self.ui.checkPDFOpen.setChecked(Wolke.Settings['PDF-Open'])
        self.ui.checkUpdate.setChecked(not Wolke.Settings['UpdateCheck_Disable'])
        self.ui.comboLogging.setCurrentIndex(Wolke.Settings['Logging'])
        self.ui.comboTheme.setCurrentText(Wolke.Settings['Theme'])

        self.fontFamilies = QtGui.QFontDatabase().families()
        self.ui.comboFont.addItems(self.fontFamilies)
        if Wolke.Settings['Font'] in self.fontFamilies:
            self.ui.comboFont.setCurrentText(Wolke.Settings['Font'])
        else:
            self.ui.comboFont.setCurrentText(Wolke.DefaultOSFont)
        self.ui.spinAppFontSize.setValue(Wolke.Settings['FontSize'])

        self.ui.comboFontHeading.addItems(self.fontFamilies)
        if Wolke.Settings['FontHeading'] in self.fontFamilies:
            self.ui.comboFontHeading.setCurrentText(Wolke.Settings['FontHeading'])
        else:
            self.ui.comboFontHeading.setCurrentText(Wolke.DefaultOSFont)
        self.ui.spinAppFontHeadingSize.setValue(Wolke.Settings['FontHeadingSize'])
            
        self.ui.buttonChar.clicked.connect(self.setCharPath)
        self.ui.buttonChar.setText('\uf07c')

        self.ui.buttonRegeln.clicked.connect(self.setRulePath)
        self.ui.buttonRegeln.setText('\uf07c')

        self.ui.buttonPlugins.clicked.connect(self.setPluginsPath)
        self.ui.buttonPlugins.setText('\uf07c')

        self.ui.resetChar.clicked.connect(self.resetCharPath)
        self.ui.resetChar.setText('\uf2ea')

        self.ui.resetRegeln.clicked.connect(self.resetRulePath)
        self.ui.resetRegeln.setText('\uf2ea')

        self.ui.resetPlugins.clicked.connect(self.resetPluginsPath)
        self.ui.resetPlugins.setText('\uf2ea')

        self.ui.resetFontDefault.clicked.connect(self.resetFonts)
        self.ui.resetFontDefault.setText('\uf2ea')

        self.ui.resetFontOS.clicked.connect(lambda: self.resetFonts(True))
        system = platform.system()
        if system == 'Windows':
            self.ui.resetFontOS.setText('\uf17a')
        elif system == 'Linux':
            self.ui.resetFontOS.setText('\uf17c')
        elif system == 'Darwin':
            self.ui.resetFontOS.setText('\uf5d1')
        else:
            self.ui.resetFontOS.setText('\ue4e5')

        windowSize = Wolke.Settings["WindowSize-Einstellungen"]
        self.form.resize(windowSize[0], windowSize[1])

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec_()

        Wolke.Settings["WindowSize-Einstellungen"] = [self.form.size().width(), self.form.size().height()]

        if self.ret == QtWidgets.QDialog.Accepted:
            needRestart = False

            Wolke.Settings['Bogen'] = self.ui.comboBogen.currentText()
            db = self.ui.comboRegelbasis.currentText()
            if db == 'Keine':
                Wolke.Settings['Datenbank'] = None
            else:
                Wolke.Settings['Datenbank'] = db
            
            Wolke.Settings['Charakter-Assistent'] = self.ui.checkWizard.isChecked()
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

            if Wolke.Settings['Font'] != self.ui.comboFont.currentText():
                Wolke.Settings['Font'] = self.ui.comboFont.currentText()
                needRestart = True

            if Wolke.Settings['FontSize'] != self.ui.spinAppFontSize.value():
                Wolke.Settings['FontSize'] = self.ui.spinAppFontSize.value()
                needRestart = True

            if Wolke.Settings['FontHeading'] != self.ui.comboFontHeading.currentText():
                Wolke.Settings['FontHeading'] = self.ui.comboFontHeading.currentText()
                needRestart = True

            if Wolke.Settings['FontHeadingSize'] != self.ui.spinAppFontHeadingSize.value():
                Wolke.Settings['FontHeadingSize'] = self.ui.spinAppFontHeadingSize.value()
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
                    EinstellungenWrapper.restartSephrasto()
    
    @staticmethod
    def restartSephrasto():
        os.chdir(EinstellungenWrapper.oldWorkingDir)
        if os.path.splitext(sys.executable)[0].endswith("Sephrasto"):
            os.execl(sys.executable, *sys.argv)
        else:
            os.execl(sys.executable, sys.argv[0], *sys.argv)

    @staticmethod
    def getSettingsFolder():
        userFolder = os.path.expanduser('~')
        system = platform.system()
        if system == 'Windows':
            import ctypes.wintypes
            CSIDL_PERSONAL = 5       # My Documents
            SHGFP_TYPE_CURRENT = 0   # Get current, not default value
            buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            userFolder = buf.value or userFolder
            return os.path.join(userFolder,'Sephrasto')
        elif system == 'Linux':
            if os.path.isdir(os.path.join(userFolder,'.sephrasto')):
                return os.path.join(userFolder,'.sephrasto') # allow users to rename the folder to a hidden folder
            else:
                return os.path.join(userFolder,'sephrasto')
        elif system == 'Darwin':
            return os.path.join(userFolder, 'Documents', 'Sephrasto') # the documents folder is language-independent on macos
        else:
            return os.path.join(userFolder,'Sephrasto')

    @staticmethod
    def createUserFolders(basePath):
        if not os.path.isdir(basePath):
            try:
                os.mkdir(basePath)
            except:
                messagebox = QtWidgets.QMessageBox()
                messagebox.setWindowTitle("Fehler!")
                messagebox.setText("Konnte den Sephrasto Ordner in deinem Nutzerverzeichnis nicht erstellen (" + basePath + "). Bitte stelle sicher, dass Sephrasto die nötigen Schreibrechte hat und dein Antivirus Programm den Zugriff nicht blockiert. Sephrasto wird sonst nicht richtig funktionieren.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messagebox.exec_()

        folders = ['Charaktere', 'Regeln', 'Plugins', 'Charakterbögen']
        for folder in folders:
            if not os.path.isdir(os.path.join(basePath, folder)):
                os.mkdir(os.path.join(basePath, folder))

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
                if Wolke.Settings['Version'] == 1:
                    if Wolke.Settings['Bogen'] == "Standard Ilaris-Charakterbogen" or Wolke.Settings['Bogen'] == "Frag immer nach":
                        Wolke.Settings['Bogen'] = "Standard Charakterbogen"
                    elif Wolke.Settings['Bogen'] == "Die lange Version von Gatsu":
                        Wolke.Settings['Bogen'] = "Langer Charakterbogen"
                    Wolke.Settings['Font'] = "Crimson Pro"
                    Wolke.Settings['FontSize'] = 9
                    Wolke.Settings['Theme'] = "Ilaris"
                    Wolke.Settings['Version'] += 1

        #Init defaults
        if not Wolke.Settings['Font'] or not Wolke.Settings['FontSize'] or not Wolke.Settings['FontHeading'] or not Wolke.Settings['FontHeadingSize'] or not Wolke.Settings['IconSize']:
            EinstellungenWrapper.useDefaultFont()
        
        if not Wolke.Settings['Pfad-Chars'] or not os.path.isdir(Wolke.Settings['Pfad-Chars']):
            Wolke.Settings['Pfad-Chars'] = os.path.join(settingsFolder, 'Charaktere')
        if not Wolke.Settings['Pfad-Regeln'] or not os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            Wolke.Settings['Pfad-Regeln'] = os.path.join(settingsFolder, 'Regeln')
        if not Wolke.Settings['Pfad-Plugins'] or not os.path.isdir(Wolke.Settings['Pfad-Plugins']):
            Wolke.Settings['Pfad-Plugins'] = os.path.join(settingsFolder, 'Plugins')
        if not Wolke.Settings['Pfad-Charakterbögen'] or not os.path.isdir(Wolke.Settings['Pfad-Charakterbögen']):
            Wolke.Settings['Pfad-Charakterbögen'] = os.path.join(settingsFolder, 'Charakterbögen')

        #Init charsheets
        for filePath in EinstellungenWrapper.getCharakterbögen():
            inifile = os.path.splitext(filePath)[0] + ".ini"
            if not os.path.isfile(inifile):
                continue
            with open(inifile,'r', encoding='utf8') as file:
                tmpSet = yaml.safe_load(file)
                cbi  = CharakterbogenInfo()
                cbi.filePath = filePath
                cbi.maxVorteile = tmpSet["MaxVorteile"]
                cbi.maxKampfVorteile = tmpSet["MaxKampfVorteile"]
                cbi.maxÜberVorteile = tmpSet["MaxÜbernatürlicheVorteile"]
                cbi.maxFreie = tmpSet["MaxFreieFertigkeiten"]
                cbi.maxFertigkeiten = tmpSet["MaxFertigkeiten"]
                cbi.maxÜberFertigkeiten = tmpSet["MaxÜbernatürlicheFertigkeiten"]
                cbi.maxÜberTalente = tmpSet["MaxÜbernatürlicheTalente"]
                cbi.seitenProfan = tmpSet["SeitenProfan"]
                cbi.kurzbogenHack = tmpSet["KurzerBogenHack"] if "KurzerBogenHack" in tmpSet else False
                cbi.beschreibungDetails = tmpSet["BeschreibungDetails"]
                cbi.bild = tmpSet["Bild"]
                cbi.bildOffset = tmpSet["BildOffset"] if "BildOffset" in tmpSet else [0, 0]
                Wolke.Charakterbögen[filePath] = cbi

    @staticmethod
    def save():
        settingsFolder = EinstellungenWrapper.getSettingsFolder()
        EinstellungenWrapper.createUserFolders(settingsFolder)

        settingsPath = os.path.join(settingsFolder, 'Sephrasto.ini')
        with open(settingsPath, 'w') as outfile:
            yaml.dump(Wolke.Settings, outfile)

    # Plugins can use this function to add their own settings
    # The setting can afterwards be accessed via Wolke.Settings["setting name"]
    @staticmethod
    def addSettings(settings):
        foundMissingSetting = False
        for setting in settings:
            if not setting in Wolke.Settings:
                Wolke.Settings[setting] = ""
                foundMissingSetting = True
        if foundMissingSetting:
            EinstellungenWrapper.save()

    def updatePluginCheckboxes(self, plugins):
        self.pluginCheckboxes = []

        layout = self.ui.gbPlugins.layout()
        for i in reversed(range(layout.count())): 
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().setParent(None)
            layout.removeItem(layout.itemAt(i))

        for pluginData in plugins:
            check = QtWidgets.QCheckBox(pluginData.name)
            if pluginData.description:
                check.setToolTip(pluginData.description)

            if not (pluginData.name in Wolke.Settings['Deaktivierte-Plugins']):
                check.setChecked(True)
            layout.addWidget(check)
            self.pluginCheckboxes.append(check)
        layout.addStretch()

    @staticmethod
    def getDatenbanken(path):
        optionsList = ['Keine']            
        if os.path.isdir(path):
            for file in Hilfsmethoden.listdir(path):
                if file.lower().endswith('.xml'):
                    optionsList.append(file)
        return optionsList

    @staticmethod
    def getCharakterbögen():
        result = []
        for file in Hilfsmethoden.listdir(os.path.join("Data", "Charakterbögen")):
            if not file.endswith(".pdf"):
                continue

            if not os.path.isfile(os.path.join("Data", "Charakterbögen", os.path.splitext(file)[0] + ".ini")):
                continue
            result.append(os.path.join("Data", "Charakterbögen", file))

        for file in Hilfsmethoden.listdir(Wolke.Settings['Pfad-Charakterbögen']):
            if not file.endswith(".pdf"):
                continue

            if not os.path.isfile(os.path.join(Wolke.Settings['Pfad-Charakterbögen'], os.path.splitext(file)[0] + ".ini")):
                continue
            result.append(os.path.join(Wolke.Settings['Pfad-Charakterbögen'], file))
        return result

    def updateComboRegelbasis(self):
        optionsList = EinstellungenWrapper.getDatenbanken(self.ui.editRegeln.text())
        self.ui.comboRegelbasis.clear()
        self.ui.comboRegelbasis.addItems(optionsList)
        if Wolke.Settings['Datenbank'] in optionsList:
            self.ui.comboRegelbasis.setCurrentText(Wolke.Settings['Datenbank'])

    def setCharPath(self):
        p = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Charaktere aus!",
          self.ui.editChar.text(),
          QtWidgets.QFileDialog.ShowDirsOnly)
        if p:
            p = os.path.realpath(p)
            if os.path.isdir(p):
                self.ui.editChar.setText(p)
            
    def setRulePath(self):
        p = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Regeln aus!",
          self.ui.editRegeln.text(),
          QtWidgets.QFileDialog.ShowDirsOnly)
        if p:
            p = os.path.realpath(p)
            if os.path.isdir(p):
                self.ui.editRegeln.setText(p)
                self.updateComboRegelbasis()

    def setPluginsPath(self):
        p = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Plugins aus!",
          self.ui.editPlugins.text(),
          QtWidgets.QFileDialog.ShowDirsOnly)
        if p:
            p = os.path.realpath(p)
            if os.path.isdir(p):
                self.ui.editPlugins.setText(p)
                self.updatePluginCheckboxes(PluginLoader.getPlugins(p))

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
        self.updatePluginCheckboxes(PluginLoader.getPlugins(p))

    def resetFonts(self, systemFont = False):
        self.ui.comboTheme.setCurrentText("Ilaris")
        if systemFont:
            self.ui.comboFont.setCurrentText(Wolke.DefaultOSFont)
        else:
            self.ui.comboFont.setCurrentText("Crimson Pro")
        self.ui.spinAppFontSize.setValue(Wolke.DefaultOSFontSize)
        self.ui.comboFontHeading.setCurrentText("Aniron")
        self.ui.spinAppFontHeadingSize.setValue(Wolke.DefaultOSFontSize -1)

    @staticmethod
    def useSystemFont():
        Wolke.Settings['Font'] = Wolke.DefaultOSFont
        Wolke.Settings['FontSize'] = Wolke.DefaultOSFontSize
        Wolke.Settings['FontHeading'] = "Aniron"
        Wolke.Settings['FontHeadingSize'] = Wolke.DefaultOSFontSize -1
        Wolke.Settings['IconSize'] = min(max(9, Wolke.Settings['FontSize']), 12)

    @staticmethod
    def useDefaultFont():
        Wolke.Settings['Font'] = "Crimson Pro"
        Wolke.Settings['FontSize'] = Wolke.DefaultOSFontSize
        Wolke.Settings['FontHeading'] = "Aniron"
        Wolke.Settings['FontHeadingSize'] = Wolke.DefaultOSFontSize -1
        Wolke.Settings['IconSize'] = min(max(9, Wolke.Settings['FontSize']), 12)