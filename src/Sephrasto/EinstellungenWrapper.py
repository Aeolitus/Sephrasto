# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:52 2018

@author: Aeolitus
"""
from Wolke import Wolke
import UI.Einstellungen
from PyQt5 import QtWidgets, QtCore, QtGui
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

        boegen = [os.path.basename(os.path.splitext(bogen)[0]) for bogen in EinstellungenWrapper.getCharakterbögen()]
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

        self.fontFamilies = QtGui.QFontDatabase().families()
        self.ui.comboFont.addItems(self.fontFamilies)
        self.ui.comboFont.setCurrentText(QtWidgets.QApplication.instance().font().family())
        self.ui.spinAppFontSize.setValue(Wolke.Settings['FontSize'])

        self.ui.comboFontHeading.addItems(self.fontFamilies)
        if Wolke.Settings['FontHeading'] in self.fontFamilies:
            self.ui.comboFontHeading.setCurrentText(Wolke.Settings['FontHeading'])
        else:
            self.ui.comboFontHeading.setCurrentText(QtWidgets.QApplication.instance().font().family())
        self.ui.spinAppFontHeadingSize.setValue(Wolke.Settings['FontHeadingSize'])
            
        font = QtGui.QFont("Font Awesome 6 Free Solid", 9, QtGui.QFont.Black)
        self.ui.buttonChar.clicked.connect(self.setCharPath)
        self.ui.buttonChar.setFont(font)
        self.ui.buttonChar.setText('\uf07c')

        self.ui.buttonRegeln.clicked.connect(self.setRulePath)
        self.ui.buttonRegeln.setFont(font)
        self.ui.buttonRegeln.setText('\uf07c')

        self.ui.buttonPlugins.clicked.connect(self.setPluginsPath)
        self.ui.buttonPlugins.setFont(font)
        self.ui.buttonPlugins.setText('\uf07c')

        self.ui.resetChar.clicked.connect(self.resetCharPath)
        self.ui.resetChar.setFont(font)
        self.ui.resetChar.setText('\uf2ea')

        self.ui.resetRegeln.clicked.connect(self.resetRulePath)
        self.ui.resetRegeln.setFont(font)
        self.ui.resetRegeln.setText('\uf2ea')

        self.ui.resetPlugins.clicked.connect(self.resetPluginsPath)
        self.ui.resetPlugins.setFont(font)
        self.ui.resetPlugins.setText('\uf2ea')

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
                    if os.path.splitext(sys.executable)[0].endswith("Sephrasto"):
                        os.execl(sys.executable, *sys.argv)
                    else:
                        os.execl(sys.executable, sys.argv[0], *sys.argv)

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
        if not Wolke.Settings['Pfad-Chars']:
            Wolke.Settings['Pfad-Chars'] = os.path.join(settingsFolder, 'Charaktere')
        if not Wolke.Settings['Pfad-Regeln']:
            Wolke.Settings['Pfad-Regeln'] = os.path.join(settingsFolder, 'Regeln')
        if not Wolke.Settings['Pfad-Plugins']:
            Wolke.Settings['Pfad-Plugins'] = os.path.join(settingsFolder, 'Plugins')
        if not Wolke.Settings['Pfad-Charakterbögen']:
            Wolke.Settings['Pfad-Charakterbögen'] = os.path.join(settingsFolder, 'Charakterbögen')

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
        
        layout = self.ui.gbPluginsOfficial.layout()
        for i in reversed(range(layout.count())): 
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().setParent(None)
            layout.removeItem(layout.itemAt(i))
        officialPlugins = [p for p in plugins if p.isOfficial]
        for pluginData in officialPlugins:
            check = QtWidgets.QCheckBox(pluginData.name)
            if pluginData.description:
                check.setToolTip(pluginData.description)

            if not (pluginData.name in Wolke.Settings['Deaktivierte-Plugins']):
                check.setChecked(True)
            layout.addWidget(check)
            self.pluginCheckboxes.append(check)
        layout.addStretch()

        layout = self.ui.gbPluginsUser.layout()
        for i in reversed(range(layout.count())): 
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().setParent(None)
            layout.removeItem(layout.itemAt(i))
        userPlugins = [p for p in plugins if not p.isOfficial]
        for pluginData in userPlugins:
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