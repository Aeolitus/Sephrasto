# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:52 2018

@author: Aeolitus
"""
from Wolke import Wolke
from Wolke import CharakterbogenInfo
import UI.Einstellungen
from PySide6 import QtWidgets, QtCore, QtGui
import os.path
import yaml
import logging
import sys
import platform
import PathHelper
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
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Abbrechen")
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
        self.ui.comboFormular.setCurrentIndex(Wolke.Settings['Formular-Editierbarkeit'])

        self.ui.editChar.setText(Wolke.Settings['Pfad-Chars'])
        self.ui.editRegeln.setText(Wolke.Settings['Pfad-Regeln'])
        self.ui.editPlugins.setText(Wolke.Settings['Pfad-Plugins'])
        self.ui.editCharakterboegen.setText(Wolke.Settings['Pfad-Charakterbögen'])

        self.pluginCheckboxes = []
        self.updatePluginCheckboxes(plugins)
        self.updateComboRegelbasis()
            
        self.ui.checkPDFOpen.setChecked(Wolke.Settings['PDF-Open'])
        self.ui.checkUpdate.setChecked(not Wolke.Settings['UpdateCheck_Disable'])
        self.ui.comboLogging.setCurrentIndex(Wolke.Settings['Logging'])

        # Offer custom themes
        for theme in Wolke.Themes.keys():
            self.ui.comboTheme.addItem(theme)
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

        self.ui.buttonCharakterboegen.clicked.connect(self.setCharakterboegenPath)
        self.ui.buttonCharakterboegen.setText('\uf07c')

        self.ui.resetChar.clicked.connect(self.resetCharPath)
        self.ui.resetChar.setText('\uf2ea')

        self.ui.resetRegeln.clicked.connect(self.resetRulePath)
        self.ui.resetRegeln.setText('\uf2ea')

        self.ui.resetPlugins.clicked.connect(self.resetPluginsPath)
        self.ui.resetPlugins.setText('\uf2ea')

        self.ui.resetCharakterboegen.clicked.connect(self.resetCharakterboegenPath)
        self.ui.resetCharakterboegen.setText('\uf2ea')

        self.ui.resetFontDefault.clicked.connect(self.resetFonts)
        self.ui.resetFontDefault.setText('\uf2ea')

        # the dpi setting doesn't do anything on macOS, hide the option
        if platform.system() == "Darwin":  
            self.ui.label_13.setVisible(False)
            self.ui.checkDPI.setVisible(False)

        self.ui.checkDPI.setChecked(Wolke.Settings['DPI-Skalierung'])

        self.ui.resetFontOS.clicked.connect(lambda: self.resetFonts(True))
        self.ui.resetFontOS.setText('\uf390')

        windowSize = Wolke.Settings["WindowSize-Einstellungen"]
        self.form.resize(windowSize[0], windowSize[1])

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()

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
            Wolke.Settings['Formular-Editierbarkeit'] = self.ui.comboFormular.currentIndex()

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

            if self.ui.editCharakterboegen.text() != Wolke.Settings['Pfad-Charakterbögen']:
                if os.path.isdir(self.ui.editCharakterboegen.text()):
                    Wolke.Settings['Pfad-Charakterbögen'] = self.ui.editCharakterboegen.text()
                else:
                    Wolke.Settings['Pfad-Charakterbögen'] = ''
                needRestart = True # TODO: reload char sheets so a restart isnt necessary

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

            if Wolke.Settings['DPI-Skalierung'] != self.ui.checkDPI.isChecked():
                Wolke.Settings['DPI-Skalierung'] = self.ui.checkDPI.isChecked()
                needRestart = True

            EinstellungenWrapper.save()

            if needRestart:
                messageBox = QtWidgets.QMessageBox()
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setWindowTitle("Sephrasto neustarten?")
                messageBox.setText("Sephrasto muss bei Änderungen an Plugin- oder Theme-Einstellungen neugestartet werden.")
                messageBox.addButton("Neustarten", QtWidgets.QMessageBox.YesRole)
                messageBox.addButton("Später", QtWidgets.QMessageBox.RejectRole)
                messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
                result = messageBox.exec()
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
    def createSettingsFolder():
        res = PathHelper.getSettingsFolder()
        if not os.path.isdir(res):
            if not PathHelper.createFolder(res):
                messagebox = QtWidgets.QMessageBox()
                messagebox.setWindowTitle("Fehler!")
                messagebox.setText("Konnte den Sephrasto Ordner in deinem lokalen Einstellungsverzeichnis nicht erstellen (" + res + "). Bitte stelle sicher, dass Sephrasto die nötigen Schreibrechte hat und dein Antivirus Programm den Zugriff nicht blockiert. Sephrasto wird sonst nicht richtig funktionieren.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messagebox.exec()
        return res

    @staticmethod
    def createUserFolder(basePath):
        if os.path.isdir(basePath):
            return
        if not PathHelper.createFolder(basePath):
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Fehler!")
            messagebox.setText("Konnte den Sephrasto Ordner in deinem Nutzerverzeichnis nicht erstellen (" + basePath + "). Bitte stelle sicher, dass Sephrasto die nötigen Schreibrechte hat und dein Antivirus Programm den Zugriff nicht blockiert. Sephrasto wird sonst nicht richtig funktionieren.")
            messagebox.setIcon(QtWidgets.QMessageBox.Critical)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec_()


    @staticmethod
    def loadPreQt():
        # Do not use any PySide/Qt stuff here, the QApplication isn't initialized yet when this function is called
        # We do a 2-step initialization to read in some settings that we require before the QApp (like DPI)
        settingsFolder = PathHelper.getSettingsFolder()
        settingsPath = os.path.join(settingsFolder, 'Sephrasto.ini')
        if not os.path.isfile(settingsPath):
            return
        with open(settingsPath,'r') as infile:
            tmpSet = yaml.safe_load(infile)
            if tmpSet is None:
                return
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

    @staticmethod
    def loadPostQt():
        #Here we are allowed to use Qt for messageboxes etc.
        EinstellungenWrapper.createSettingsFolder()

        #Init defaults
        folders = [('Pfad-Chars', 'Charaktere'),
                   ('Pfad-Regeln', 'Regeln'),
                   ('Pfad-Plugins', 'Plugins'),
                   ('Pfad-Charakterbögen', 'Charakterbögen')]

        missingFolders = []
        for configName, folderName in folders:
            if Wolke.Settings[configName] and not os.path.isdir(Wolke.Settings[configName]):
                missingFolders.append(folderName)

            if not Wolke.Settings[configName] or not os.path.isdir(Wolke.Settings[configName]):
                Wolke.Settings[configName] = os.path.join(PathHelper.getDefaultUserFolder(), folderName)
                EinstellungenWrapper.createUserFolder(Wolke.Settings[configName])

        if len(missingFolders) > 0:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Fehlende Ordner")
            messagebox.setText("Die folgenden Ordner existieren nicht mehr und wurden auf den Standardpfad zurückgesetzt: " + ", ".join(missingFolders))
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec()

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

                if "Info" in tmpSet:
                    cbi.info = tmpSet["Info"]
                if "ÜberSeite" in tmpSet:
                    cbi.überSeite = tmpSet["ÜberSeite"]
                if "ÜberFertigkeitenZuProfan" in tmpSet:
                    cbi.überFertigkeitenZuProfan = tmpSet["ÜberFertigkeitenZuProfan"]
                if "ÜberVorteileZuKampf" in tmpSet:
                    cbi.überVorteileZuKampf = tmpSet["ÜberVorteileZuKampf"]
                if "MaxVorteileProFeld" in tmpSet:
                    cbi.maxVorteileProFeld = tmpSet["MaxVorteileProFeld"]
                if "MaxKampfVorteileProFeld" in tmpSet:
                    cbi.maxKampfVorteileProFeld = tmpSet["MaxKampfVorteileProFeld"]
                if "MaxÜberVorteileProFeld" in tmpSet:
                    cbi.maxÜberVorteileProFeld = tmpSet["MaxÜberVorteileProFeld"]
                if "MaxFreieProFeld" in tmpSet:
                    cbi.maxFreieProFeld = tmpSet["MaxFreieProFeld"]
                if "ExtraÜberSeiten" in tmpSet:
                    cbi.extraÜberSeiten = tmpSet["ExtraÜberSeiten"]
                if "BeschreibungDetails" in tmpSet:
                    cbi.beschreibungDetails = tmpSet["BeschreibungDetails"]
                if "Bild" in tmpSet:
                    for v in tmpSet["Bild"]:
                        cbi.bild.append(v)
                regelAnhang = os.path.splitext(filePath)[0] + "_Regeln.pdf"
                if os.path.isfile(regelAnhang):
                    cbi.regelanhangPfad = regelAnhang
                    regelAnhangHintergrund = os.path.splitext(filePath)[0] + "_Hintergrund.pdf"
                    if os.path.isfile(regelAnhangHintergrund):
                        cbi.regelanhangHintergrundPfad = regelAnhangHintergrund
                    else:
                        cbi.regelanhangHintergrundPfad = None
                Wolke.Charakterbögen[filePath] = cbi

        #Init themes
        Wolke.Themes = EinstellungenWrapper.getThemes()

    @staticmethod
    def save():
        settingsFolder = EinstellungenWrapper.createSettingsFolder()
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
            else:
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

        self.ui.gbPlugins.setVisible(len(self.pluginCheckboxes) > 0)

    @staticmethod
    def getDatenbanken(path):
        optionsList = ['Keine']            
        if os.path.isdir(path):
            for file in PathHelper.listdir(path):
                if file.lower().endswith('.xml'):
                    optionsList.append(file)
        return optionsList

    @staticmethod
    def getCharakterbögen():
        result = []
        for file in PathHelper.listdir(os.path.join("Data", "Charakterbögen")):
            if not file.endswith(".pdf"):
                continue

            if not os.path.isfile(os.path.join("Data", "Charakterbögen", os.path.splitext(file)[0] + ".ini")):
                continue
            result.append(os.path.join("Data", "Charakterbögen", file))

        for file in PathHelper.listdir(Wolke.Settings['Pfad-Charakterbögen']):
            if not file.endswith(".pdf"):
                continue

            if not os.path.isfile(os.path.join(Wolke.Settings['Pfad-Charakterbögen'], os.path.splitext(file)[0] + ".ini")):
                continue
            result.append(os.path.join(Wolke.Settings['Pfad-Charakterbögen'], file))
        return result

    @staticmethod
    def getThemes():
        result = {}

        files = [os.path.join("Data", "Themes", f) for f in PathHelper.listdir(os.path.join("Data", "Themes"))]
        userTheme = os.path.join(PathHelper.getSettingsFolder(), "Mein Theme.ini")
        if os.path.isfile(userTheme):
            files.append(userTheme)

        for filePath in files:
            if not filePath.endswith(".ini"):
                continue
            with open(filePath,'r', encoding='utf8') as file:
                result[os.path.splitext(os.path.basename(filePath))[0]] = yaml.safe_load(file)

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

    def setCharakterboegenPath(self):
        p = QtWidgets.QFileDialog.getExistingDirectory(None,
          "Wähle einen Speicherort für Charakterbögen aus!",
          self.ui.editCharakterboegen.text(),
          QtWidgets.QFileDialog.ShowDirsOnly)
        if p:
            p = os.path.realpath(p)
            if os.path.isdir(p):
                self.ui.editCharakterboegen.setText(p)

    def resetCharPath(self):
        p = os.path.join(PathHelper.getDefaultUserFolder(), 'Charaktere')
        self.ui.editChar.setText(p)
        
    def resetRulePath(self):
        p = os.path.join(PathHelper.getDefaultUserFolder(), 'Regeln')
        self.ui.editRegeln.setText(p)
        self.updateComboRegelbasis()
        
    def resetPluginsPath(self):
        p = os.path.join(PathHelper.getDefaultUserFolder(), 'Plugins')
        self.ui.editPlugins.setText(p)
        self.updatePluginCheckboxes(PluginLoader.getPlugins(p))

    def resetCharakterboegenPath(self):
        p = os.path.join(PathHelper.getDefaultUserFolder(), 'Charakterbögen')
        self.ui.editCharakterboegen.setText(p)

    def resetFonts(self, systemFont = False):
        self.ui.comboTheme.setCurrentText("Ilaris")
        if systemFont:
            self.ui.comboFont.setCurrentText(Wolke.DefaultOSFont)
        else:
            self.ui.comboFont.setCurrentText("Crimson Pro")
        self.ui.spinAppFontSize.setValue(Wolke.DefaultOSFontSize)
        self.ui.comboFontHeading.setCurrentText("Aniron")
        self.ui.spinAppFontHeadingSize.setValue(Wolke.DefaultOSFontSize -1)