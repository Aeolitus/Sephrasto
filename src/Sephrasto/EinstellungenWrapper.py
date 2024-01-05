# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:09:52 2018

@author: Aeolitus
"""
from Wolke import Wolke
from Charakterbogen import Charakterbogen
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
from functools import partial
import Version
from PluginRepository import PluginRepo
import shutil

class PluginDataUI:
    def __init__(self, pd, sephrastoVersion = Version._sephrasto_version):
        self.pd = pd
        self.repoPd = pd
        self.installed = False
        self.installable = False
        self.updatable = False
        self.downgradable = False
        self.sephrastoVersion = sephrastoVersion

    @property
    def name(self): return self.pd.name

    @property
    def version(self): return self.pd.version

class EinstellungenWrapper():    
    def __init__(self, activePlugins):
        self.needRestart = False
        self.activePlugins = activePlugins
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
        
        for i in range(self.ui.tabWidget.tabBar().count()):
            self.ui.tabWidget.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))
        self.ui.tabWidget.setStyleSheet('QTabBar { font-size: ' + str(Wolke.Settings["FontHeadingSize"]) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')

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
        self.ui.spinRulesFontSize.setValue(Wolke.Settings['Cheatsheet-Fontsize'])
        self.ui.checkFormular.setChecked(Wolke.Settings['Formular-Editierbarkeit'])

        self.ui.editChar.setText(Wolke.Settings['Pfad-Chars'])
        self.ui.editRegeln.setText(Wolke.Settings['Pfad-Regeln'])
        self.ui.editPlugins.setText(Wolke.Settings['Pfad-Plugins'])
        self.ui.editCharakterboegen.setText(Wolke.Settings['Pfad-Charakterbögen'])

        self.updateComboRegelbasis()
            
        self.ui.checkPDFOpen.setChecked(Wolke.Settings['PDF-Open'])
        self.ui.checkUpdate.setChecked(not Wolke.Settings['UpdateCheck_Disable'])
        self.ui.comboLogging.setCurrentIndex(Wolke.Settings['Logging'])

        self.ui.spinCharListCols.setValue(Wolke.Settings['CharListCols'])
        self.ui.spinCharListRows.setValue(Wolke.Settings['CharListRows'])

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

        self.ui.buttonLogOpen.clicked.connect(self.openLogLocation)
        self.ui.buttonLogOpen.setText('\uf07c')

        # the dpi setting doesn't do anything on macOS, hide the option
        if platform.system() == "Darwin":  
            self.ui.labelDPI.setVisible(False)
            self.ui.checkDPI.setVisible(False)

        self.ui.checkDPI.setChecked(Wolke.Settings['DPI-Skalierung'])

        self.ui.resetFontOS.clicked.connect(lambda: self.resetFonts(True))
        self.ui.resetFontOS.setText('\uf390')

        self.ui.buttonSettings.setText('\uf013')
        self.ui.buttonSettings.setVisible(False)
        self.ui.buttonInstall.setVisible(False)
        self.ui.buttonUpdate.setVisible(False)
        self.ui.buttonDowngrade.setVisible(False)
        self.ui.buttonDelete.setVisible(False)
        self.ui.buttonSettings.clicked.connect(self.openPluginSettings)
        self.ui.buttonDelete.clicked.connect(lambda: self.deletePlugin(self.getSelectedPlugin()))
        self.ui.buttonInstall.clicked.connect(lambda: self.installPlugin(self.getSelectedPlugin()))
        self.ui.buttonUpdate.clicked.connect(lambda: self.updatePlugin(self.getSelectedPlugin()))
        self.ui.buttonDowngrade.clicked.connect(lambda: self.updatePlugin(self.getSelectedPlugin()))
        self.ui.tbPluginInfo.setOpenExternalLinks(True)
        self.ui.tablePlugins.currentItemChanged.connect(self.onPluginSelected)
        self.ui.tablePlugins.currentCellChanged.connect(self.onPluginSelected)
        self.ui.tablePlugins.cellClicked.connect(self.onPluginSelected) 
        self.ui.tablePlugins.verticalHeader().setVisible(False)
        self.ui.tablePlugins.setColumnCount(3)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        item.setText("Plugin")
        self.ui.tablePlugins.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("Version")
        self.ui.tablePlugins.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tablePlugins.setHorizontalHeaderItem(2, item)

        header = self.ui.tablePlugins.horizontalHeader()
        header.setMinimumSectionSize(0)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.ui.tablePlugins.setColumnWidth(1, Hilfsmethoden.emToPixels(10))
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        self.ui.tablePlugins.setColumnWidth(2, Hilfsmethoden.emToPixels(3))

        self.pluginDataUIs = []
        self.pluginUiReady = False
        self.pluginUiMutex = QtCore.QMutex()
        self.pluginRepos = []
        for repo in Wolke.Settings['Plugin-Repos']:
            self.pluginRepos.append(PluginRepo(repo["name"], repo["url"]))
        for repo in self.pluginRepos:
            repo.ready.connect(self.onPluginRepoReady)
            repo.loadingProgress.connect(self.onPluginLoadingProgress)
            repo.update()

        windowSize = Wolke.Settings["WindowSize-Einstellungen"]
        self.form.resize(windowSize[0], windowSize[1])

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()

        Wolke.Settings["WindowSize-Einstellungen"] = [self.form.size().width(), self.form.size().height()]

        if self.ret == QtWidgets.QDialog.Accepted:
            Wolke.Settings['Bogen'] = self.ui.comboBogen.currentText()
            db = self.ui.comboRegelbasis.currentText()
            if db == 'Keine':
                Wolke.Settings['Datenbank'] = None
            else:
                Wolke.Settings['Datenbank'] = db
            
            Wolke.Settings['Charakter-Assistent'] = self.ui.checkWizard.isChecked()
            Wolke.Settings['Cheatsheet'] = self.ui.checkCheatsheet.isChecked()
            Wolke.Settings['Cheatsheet-Fontsize'] = self.ui.spinRulesFontSize.value()
            Wolke.Settings['Formular-Editierbarkeit'] = self.ui.checkFormular.isChecked()

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
                self.needRestart = True

            if self.ui.editCharakterboegen.text() != Wolke.Settings['Pfad-Charakterbögen']:
                if os.path.isdir(self.ui.editCharakterboegen.text()):
                    Wolke.Settings['Pfad-Charakterbögen'] = self.ui.editCharakterboegen.text()
                else:
                    Wolke.Settings['Pfad-Charakterbögen'] = ''
                self.needRestart = True # TODO: reload char sheets so a restart isnt necessary
              
            Wolke.Settings['UpdateCheck_Disable'] = not self.ui.checkUpdate.isChecked()
            Wolke.Settings['Logging'] = self.ui.comboLogging.currentIndex()
            if Wolke.CmdArgs.loglevel is None:
                loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
                logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])
            
            Wolke.Settings['PDF-Open'] = self.ui.checkPDFOpen.isChecked()

            if Wolke.Settings['CharListCols'] != self.ui.spinCharListCols.value():
                Wolke.Settings['CharListCols'] = self.ui.spinCharListCols.value()
                self.needRestart = True

            if Wolke.Settings['CharListRows'] != self.ui.spinCharListRows.value():
                Wolke.Settings['CharListRows'] = self.ui.spinCharListRows.value()
                self.needRestart = True

            if Wolke.Settings['Theme'] != self.ui.comboTheme.currentText():
                Wolke.Settings['Theme'] = self.ui.comboTheme.currentText()
                self.needRestart = True

            if Wolke.Settings['Font'] != self.ui.comboFont.currentText():
                Wolke.Settings['Font'] = self.ui.comboFont.currentText()
                self.needRestart = True

            if Wolke.Settings['FontSize'] != self.ui.spinAppFontSize.value():
                Wolke.Settings['FontSize'] = self.ui.spinAppFontSize.value()
                self.needRestart = True

            if Wolke.Settings['FontHeading'] != self.ui.comboFontHeading.currentText():
                Wolke.Settings['FontHeading'] = self.ui.comboFontHeading.currentText()
                self.needRestart = True

            if Wolke.Settings['FontHeadingSize'] != self.ui.spinAppFontHeadingSize.value():
                Wolke.Settings['FontHeadingSize'] = self.ui.spinAppFontHeadingSize.value()
                self.needRestart = True

            if Wolke.Settings['DPI-Skalierung'] != self.ui.checkDPI.isChecked():
                Wolke.Settings['DPI-Skalierung'] = self.ui.checkDPI.isChecked()
                self.needRestart = True

            EinstellungenWrapper.save()

            if self.needRestart:
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
   
    def getSelectedPlugin(self):
        row = self.ui.tablePlugins.currentRow()
        if row >= len(self.pluginDataUIs):
            return None
        return self.pluginDataUIs[row]

    def refreshPluginTable(self):
        if not self.pluginUiReady:
            return
        self.pluginUiReady = False
        row = self.ui.tablePlugins.currentRow()
        self.onPluginRepoReady()
        if row >= self.ui.tablePlugins.rowCount():
            row = 0
        self.ui.tablePlugins.selectRow(row)

    def openPluginSettings(self):
        pdui = self.getSelectedPlugin()
        if pdui is None:
            return
        pdui.pd.showSettings()

    def installDependencies(self, pdui):
        toInstall = []
        toUpdate = []
        missing = []
        for dep in pdui.pd.dependencies:
            resolved = None
            for el in self.pluginDataUIs:
                if el.name == dep["name"]:
                    resolved = el
                    break
            if resolved is None or Version.isHigher(resolved.repoPd.version, dep["version"]):
                missing.append(dep)
                continue
            if resolved.installable:
                toInstall.append(resolved)
                continue
            if resolved.installed and (Version.isEqual(resolved.pd.version, dep["version"]) or Version.isLower(resolved.pd.version, dep["version"])):
                continue
            if resolved.updatable:
                toUpdate.append(resolved)
        if len(toInstall) == 0 and len(toUpdate) == 0 and len(missing) == 0:
            return True
        text = []
        if len(toInstall) > 0:
            text.append("Installiere:\n-" + "\n- ".join([f"{pdui.pd.anzeigename} {Version.toString(pdui.version)}" for pdui in toInstall]))
        if len(toUpdate) > 0:
            text.append("Aktualisiere:\n-" + "\n- ".join([f"{pdui.pd.anzeigename} {Version.toString(pdui.repoPd.version)}" for pdui in toUpdate]))
        if len(missing) > 0:
            text.append(f"Nicht auffindbar:\n-" +
                        "\n- ".join([f"{dep['name']} {Version.toString(dep['version'])}" for dep in missing]))
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information if len(missing) == 0 else QtWidgets.QMessageBox.Warning)
        messageBox.setWindowTitle(pdui.pd.anzeigename + " Installation")
        messageBox.setText(pdui.pd.anzeigename + " benötigt weitere Plugins!")
        messageBox.setInformativeText("\n\n".join(text))
        messageBox.addButton("Fortfahren", QtWidgets.QMessageBox.YesRole)
        messageBox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
        result = messageBox.exec()
        if result == 1:
            return False
        for el in toInstall:
            self.installPlugin(el)
        for el in toUpdate:
            self.updatePlugin(el)
        return True

    def installPlugin(self, pdui):
        if pdui is None or not pdui.installable:
            return
        if not self.installDependencies(pdui):
            return
        srcPath = os.path.join(pdui.pd.path, pdui.pd.name)
        dstPath = os.path.join(self.ui.editPlugins.text(), pdui.pd.name)
        shutil.copytree(srcPath, dstPath, dirs_exist_ok=True)
        self.needRestart = True
        self.refreshPluginTable()

    def updatePlugin(self, pdui):
        if pdui is None or not (pdui.updatable or pdui.downgradable):
            return
        if not self.installDependencies(pdui):
            return
        srcPath = os.path.join(pdui.repoPd.path, pdui.repoPd.name)
        dstPath = os.path.join(pdui.pd.path, pdui.pd.name)
        shutil.copytree(srcPath, dstPath, dirs_exist_ok=True) 
        self.needRestart = True
        self.refreshPluginTable()

    def deletePlugin(self, pdui):
        if pdui is None or not pdui.installed:
            return

        if pdui.pd == pdui.repoPd:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle(pdui.pd.anzeigename + " löschen")
            messageBox.setText(f"{pdui.pd.anzeigename} ist in keinem Repository auffindbar, sodass du es nach dem Löschen nicht mehr wiederherstellen kannst.\n\nMit dem Löschen fortfahren?")
            messageBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            messageBox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            result = messageBox.exec()
            if result == 1:
                return

        dependants = []
        for el in self.pluginDataUIs:
            if not el.installed:
                continue
            for dep in el.pd.dependencies:
                if pdui.name == dep["name"]:
                    dependants.append(el.pd.anzeigename)
                    break
        if len(dependants) > 0:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle(pdui.pd.anzeigename + " löschen")
            messageBox.setText(f"Die folgenden Plugins benötigen {pdui.pd.anzeigename} für eine fehlerfreie Funktion: {', '.join(dependants)}.\n\nMit dem Löschen fortfahren?")
            messageBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            messageBox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            result = messageBox.exec()
            if result == 1:
                return

        srcPath = os.path.join(pdui.pd.path, pdui.pd.name)
        shutil.rmtree(srcPath)
        self.needRestart = True
        self.refreshPluginTable()

    def onPluginSelected(self):
        pdui = self.getSelectedPlugin()
        if pdui is None:
            self.ui.buttonSettings.setVisible(False)
            self.ui.buttonInstall.setVisible(False)
            self.ui.buttonUpdate.setVisible(False)
            self.ui.buttonDowngrade.setVisible(False)
            self.ui.buttonDelete.setVisible(False)
            return
      
        self.ui.buttonSettings.setVisible(pdui.installed and pdui.pd.hasSettings)
        if pdui.pd.isLoaded():
            self.ui.buttonSettings.setToolTip("")
            self.ui.buttonSettings.setEnabled(True)
        else:
            self.ui.buttonSettings.setToolTip("Starte Sephrasto neu, um Einstellungen vornehmen zu können")
            self.ui.buttonSettings.setEnabled(False)

        self.ui.buttonInstall.setVisible(pdui.installable)
        self.ui.buttonUpdate.setVisible(pdui.updatable)
        self.ui.buttonDowngrade.setVisible(pdui.downgradable)
        self.ui.buttonDelete.setVisible(pdui.installed)

        
        text = f"<p><b>{pdui.pd.anzeigename}</b><br><i>von {pdui.pd.autor}</i></p>{pdui.pd.beschreibung}"
        dependencies = ", ".join(dep["name"] for dep in pdui.pd.dependencies)
        if dependencies:        
            text += f"<p><i>Verwendet:</i> {dependencies}</p>"

        self.ui.tbPluginInfo.setText(Hilfsmethoden.fixHtml(text))

    def onPluginLoadingProgress(self):
        progress = min(repo.progress for repo in self.pluginRepos)
        self.ui.progressBar.setValue(int(progress*100))

    def onPluginRepoReady(self):
        self.pluginUiMutex.lock()
        if self.pluginUiReady:
            self.pluginUiMutex.unlock()
            return
        for repo in self.pluginRepos:
            if not repo.isReady:
                self.pluginUiMutex.unlock()
                return
        self.ui.progressBar.hide()
        self.pluginUiReady = True
        self.pluginUiMutex.unlock()

        installedPluginDataUIs = {}
        pluginDataUIs = {}

        for pd in PluginLoader.getPlugins(self.ui.editPlugins.text()):
            for pdLoaded in self.activePlugins:
                if pd.name == pdLoaded.name and pd.path == pdLoaded.path and pd.version == pdLoaded.version:
                    pd = pdLoaded
                    break  
            pdui = PluginDataUI(pd)
            pdui.installed = True
            pluginDataUIs[pd.name] = pdui
            installedPluginDataUIs[pd.name] = pdui

        for repo in self.pluginRepos:
            for pd in repo.pluginData:
                if pd.name in installedPluginDataUIs:
                    installedPdui = installedPluginDataUIs[pd.name]
                    installedPdui.repoPd = pd
                    installedPdui.sephrastoVersion = repo.sephrastoVersion
                    if Version.isHigher(installedPdui.version, pd.version):
                        installedPdui.updatable = True
                    elif Version.isLower(installedPdui.version, pd.version):
                        installedPdui.downgradable = True
                    continue
                pluginDataUIs[pd.name] = PluginDataUI(pd, repo.sephrastoVersion)
                pluginDataUIs[pd.name].installable = True

        self.pluginDataUIs = sorted(pluginDataUIs.values(), key=lambda pdui: Hilfsmethoden.unicodeCaseInsensitive(pdui.name))

        self.ui.tablePlugins.clearContents()
        self.ui.tablePlugins.setRowCount(0)
        for pdui in self.pluginDataUIs:
            row = self.ui.tablePlugins.rowCount()
            self.ui.tablePlugins.insertRow(row)

            item = QtWidgets.QTableWidgetItem(pdui.pd.anzeigename)
            self.ui.tablePlugins.setItem(row, 0, item)

            label = QtWidgets.QLabel()
            label.setStyleSheet("width: 100%;");
            label.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            anzeigeversion = Version.toString(pdui.version)

            if pdui.downgradable:
                warnIcon = "&nbsp;&nbsp;<span style='" + Wolke.FontAwesomeCSS + "'>\uf071</span>"
                anzeigeversion += warnIcon
                sephrastoVersion = ".".join([str(v) for v in pdui.sephrastoVersion[:3]])
                label.setToolTip("Das Plugin wurde für eine neuere Sephrasto-Version entwickelt.\n"\
                    "Vielleicht macht das nichts, aber es kann auch sein, dass es nicht richtig funktionieren wird.\n"\
                    f"Es steht eine ältere Version für Sephrasto {sephrastoVersion} zur Verfügung, ein Downgrade wird empfohlen.")
            elif Version.isClientHigher(pdui.sephrastoVersion):
                warnIcon = "&nbsp;&nbsp;<span style='" + Wolke.FontAwesomeCSS + "'>\uf071</span>"
                anzeigeversion += warnIcon
                sephrastoVersion = ".".join([str(v) for v in pdui.sephrastoVersion[:3]])
                label.setToolTip(f"Das Plugin wurde für das ältere Sephrasto {sephrastoVersion} entwickelt.\n"\
                    "Vielleicht macht das nichts, aber es kann auch sein, dass es nicht richtig funktionieren wird.")

            label.setText(anzeigeversion)
            self.ui.tablePlugins.setCellWidget(row, 1, label)

            label = QtWidgets.QLabel()
            label.setStyleSheet("width: 100%;");
            label.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            label.setProperty("class", "icon")

            if pdui.updatable:
                label.setText("\uf0aa")   
                anzeigeversion = ".".join([str(v) for v in pdui.repoPd.version]).strip(".0")
                label.setToolTip("Neue Version verfügbar: " + anzeigeversion)
            elif pdui.downgradable:
                label.setText("\uf0ab")   
                anzeigeversion = ".".join([str(v) for v in pdui.repoPd.version]).strip(".0")
                label.setToolTip("Downgrade auf ältere Version empfohlen: " + anzeigeversion)
            elif pdui.installed:
                label.setText("\uf00c")
            elif pdui.installable:
                label.setText("\uf65e")
            self.ui.tablePlugins.setCellWidget(row, 2, label)


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
        settingsPath = Wolke.CmdArgs.settingsfile
        if settingsPath is None:
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
            if Wolke.Settings['Version'] == 2:
                if Wolke.Settings['Cheatsheet-Fontsize'] == 0:
                    Wolke.Settings['Cheatsheet-Fontsize'] = 8
                elif Wolke.Settings['Cheatsheet-Fontsize'] == 1:
                    Wolke.Settings['Cheatsheet-Fontsize'] = 10
                elif Wolke.Settings['Cheatsheet-Fontsize'] == 2:
                    Wolke.Settings['Cheatsheet-Fontsize'] = 12
                Wolke.Settings['Formular-Editierbarkeit'] = Wolke.Settings['Formular-Editierbarkeit'] != "2"
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

        if len(missingFolders) > 0:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle("Fehlende Ordner")
            messageBox.setText("Die folgenden Ordner existieren nicht mehr. Sollen sie auf den Standardpfad zurückgesetzt werden?")
            messageBox.setInformativeText(", ".join(missingFolders))
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.addButton("Zurücksetzen", QtWidgets.QMessageBox.YesRole)
            messageBox.addButton("Sephrasto beenden", QtWidgets.QMessageBox.RejectRole)
            if messageBox.exec() == 1:
                sys.exit()

        for configName, folderName in folders:
            if not Wolke.Settings[configName] or not os.path.isdir(Wolke.Settings[configName]):
                Wolke.Settings[configName] = os.path.join(PathHelper.getDefaultUserFolder(), folderName)
                EinstellungenWrapper.createUserFolder(Wolke.Settings[configName])

        #Init charsheets
        for filePath in EinstellungenWrapper.getCharakterbögen():
            cb = Charakterbogen()
            if cb.load(filePath):
                Wolke.Charakterbögen[cb.name] = cb

        #Init themes
        Wolke.Themes = EinstellungenWrapper.getThemes()

    @staticmethod
    def save():
        settingsPath = Wolke.CmdArgs.settingsfile
        if settingsPath is None:
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
                Wolke.Settings[setting] = settings[setting]
                foundMissingSetting = True
        if foundMissingSetting:
            EinstellungenWrapper.save()

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
            if not file.endswith(".ini"):
                continue
            result.append(os.path.join("Data", "Charakterbögen", file))

        for file in PathHelper.listdir(Wolke.Settings['Pfad-Charakterbögen']):
            if not file.endswith(".ini"):
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
                self.refreshPluginTable()

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
        self.refreshPluginTable()

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

    def openLogLocation(self):
        Hilfsmethoden.openFile(os.getcwd())