# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 22:36:35 2017

@author: Aeolitus
"""

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import CharakterBeschreibungWrapper
import CharakterBeschreibungDetailsWrapper
import CharakterAttributeWrapper
import CharakterEquipmentWrapper
import CharakterFertigkeitenWrapper
import CharakterUebernatuerlichWrapper
import CharakterFreieFertWrapper
import CharakterVorteileWrapper
import CharakterInfoWrapper
import Charakter
import Datenbank
from Wolke import Wolke
import os.path
import PdfExporter
import logging
from EventBus import EventBus
from shutil import which
from EinstellungenWrapper import EinstellungenWrapper
from CharakterAssistent import WizardWrapper
from UI import Wizard
import platform

class Tab():
    def __init__(self, order, wrapper, form, name):
        self.order = order
        self.wrapper = wrapper
        self.form = form
        self.name = name

class Editor(object):
    '''
    Main class for the character editing window. Mostly puts together the
    different parts of the GUI and handles the communication inbetween.
    '''
    def __init__(self, plugins, savePathUpdatedCallback, CharacterName=""):
        super().__init__()
        self.plugins = plugins
        self.savepath = CharacterName

        hausregeln = Wolke.Settings['Datenbank']
        if self.savepath:
            tmp = Charakter.Char.xmlHausregelnLesen(self.savepath)
            if tmp is None:
                hausregeln = ""
            elif tmp in EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"]):
                hausregeln = tmp if tmp != "Keine" else ""

        Wolke.DB = Datenbank.Datenbank(hausregeln)
        self.pdfExporter = PdfExporter.PdfExporter()

        self.changed = False
        self.savePathUpdatedCallback = savePathUpdatedCallback
        if Wolke.DB.loaded:
            self.noDatabase = False
            self.finishInit()
        else:
            self.noDatabase = True
        
    def finishInit(self):
        Wolke.Char = Charakter.Char()

        if self.savepath:
            Wolke.Char.xmlLesen(self.savepath)
        else:
            self.showCharacterWizard()

        enabledPlugins = []
        for pluginData in self.plugins:
            if pluginData.plugin is not None and hasattr(pluginData.plugin, "changesCharacter") and pluginData.plugin.changesCharacter():
                enabledPlugins.append(pluginData.name)
        
        missingPlugins = set(Wolke.Char.enabledPlugins) - set(enabledPlugins)
        if len(missingPlugins) > 0:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setWindowTitle("Plugin fehlt!")
            infoBox.setText("Der Charakter wurde mit einem oder mehreren Plugins erstellt, die seine Werte beeinflussen. "\
            "Nicht alle davon sind aktiv, daher können beim Speichern Daten dieser Plugins verloren gehen:\n\n" + ", ".join(missingPlugins))
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()

        Wolke.Char.enabledPlugins = enabledPlugins

        Wolke.Char.aktualisieren() # A bit later because it needs access to itself
        
    def wheelEvent(self, ev):
        if ev.type() == QtCore.QEvent.Wheel:
            if not self.ui.scrollArea.hasFocus():
                ev.ignore()

    def setupMainForm(self):
        windowSize = Wolke.Settings["WindowSize-Charakter"]
        self.form.resize(windowSize[0], windowSize[1])

        self.ui.scrollArea.wheelEvent = self.wheelEvent

        self.ui.progressBar.setVisible(False)
        self.updateEP()

        tabs = []

        details = False
        for bogen in Wolke.Charakterbögen:
            if Wolke.Char.charakterbogen == os.path.basename(os.path.splitext(bogen)[0]):
                details = Wolke.Charakterbögen[bogen].beschreibungDetails
                break

        if details:
            beschrWrapper = EventBus.applyFilter("class_beschreibungdetails_wrapper", CharakterBeschreibungDetailsWrapper.CharakterBeschreibungDetailsWrapper)
            if beschrWrapper:
                self.beschrWrapper = beschrWrapper()
                tabs.append(Tab(10, self.beschrWrapper, self.beschrWrapper.form, "Beschreibung"))
        else:
            beschrWrapper = EventBus.applyFilter("class_beschreibung_wrapper", CharakterBeschreibungWrapper.BeschrWrapper)
            if beschrWrapper:
                self.beschrWrapper = beschrWrapper()
                tabs.append(Tab(10, self.beschrWrapper, self.beschrWrapper.form, "Beschreibung"))

        attrWrapper = EventBus.applyFilter("class_attribute_wrapper", CharakterAttributeWrapper.AttrWrapper)
        if attrWrapper:
            self.attrWrapper = attrWrapper()
            tabs.append(Tab(20, self.attrWrapper, self.attrWrapper.form, "Attribute"))

        vortWrapper = EventBus.applyFilter("class_vorteile_wrapper", CharakterVorteileWrapper.CharakterVorteileWrapper)
        if vortWrapper:
            self.vortWrapper = vortWrapper()
            tabs.append(Tab(30, self.vortWrapper, self.vortWrapper.form, "Vorteile"))

        fertWrapper = EventBus.applyFilter("class_fertigkeiten_wrapper", CharakterFertigkeitenWrapper.FertigkeitenWrapper)
        if fertWrapper:
            self.fertWrapper = fertWrapper()
            tabs.append(Tab(40, self.fertWrapper, self.fertWrapper.form, "Fertigkeiten"))

        equipWrapper = EventBus.applyFilter("class_ausruestung_wrapper", CharakterEquipmentWrapper.EquipWrapper)
        if equipWrapper:
            self.equipWrapper = equipWrapper()
            tabs.append(Tab(50, self.equipWrapper, self.equipWrapper.form, "Ausrüstung"))   

        infoWrapper = EventBus.applyFilter("class_info_wrapper", CharakterInfoWrapper.InfoWrapper)
        if infoWrapper:
            self.infoWrapper = infoWrapper()
            tabs.append(Tab(70, self.infoWrapper, self.infoWrapper.form, "Info"))

        for pd in self.plugins:
            if pd.plugin is None:
                continue

            if hasattr(pd.plugin, "createCharakterTabs"):
                for tab in pd.plugin.createCharakterTabs():
                   tabs.append(tab)

            if hasattr(pd.plugin, "createCharakterButtons"):
                for button in pd.plugin.createCharakterButtons():
                    self.ui.horizontalLayout_2.addWidget(button)

        self.tabs = sorted(tabs, key=lambda tab: tab.order)
        for tab in self.tabs:
            self.ui.tabs.addTab(tab.form, tab.name)
            if hasattr(tab.wrapper, "modified"):
                tab.wrapper.modified.connect(self.onModified)

        for i in range(self.ui.tabs.tabBar().count()):
            self.ui.tabs.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))

        self.ui.tabs.setStyleSheet('QTabBar { font-weight: bold; font-size: ' + str(Wolke.FontHeadingSizeL1) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')
        self.ui.tabs.currentChanged.connect(lambda idx : self.reload(idx))
        self.ui.buttonSave.clicked.connect(self.saveButton)
        self.ui.buttonQuicksave.clicked.connect(self.quicksaveButton)
        self.ui.buttonSavePDF.clicked.connect(self.pdfButton)
        self.ui.spinEP.valueChanged.connect(self.epChanged)

        self.reload(self.ui.tabs.currentIndex())

        self.form.closeEvent = self.closeEvent
        
    def cancelDueToPendingChanges(self, action):
        if self.changed:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle(action)
            messagebox.setText("Sollen die ausstehenden Änderungen gespeichert werden?")
            messagebox.setIcon(QtWidgets.QMessageBox.Question)
            messagebox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            messagebox.addButton("Nein", QtWidgets.QMessageBox.NoRole)
            messagebox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            result = messagebox.exec()
            if result == 0:
                self.quicksaveButton()
            elif result == 2:
                return True
        return False

    def closeEvent(self,event):
        self.form.setFocus() #make sure editingfinished is called on potential line edits in focus
        if self.cancelDueToPendingChanges("Beenden"):
            event.ignore()
        else:
            Wolke.Settings["WindowSize-Charakter"] = [self.form.size().width(), self.form.size().height()]
    
    def onModified(self):
        self.changed = True
        Wolke.Char.aktualisieren()
        self.updateEP()

    def updateEP(self):
        self.ui.spinEP.setValue(Wolke.Char.EPtotal)
        self.ui.spinRemaining.setValue(Wolke.Char.EPtotal-Wolke.Char.EPspent)
        if Wolke.Char.EPtotal < Wolke.Char.EPspent:
            self.ui.spinRemaining.setStyleSheet("QSpinBox { color: white; background-color: rgb(200,50,50) }")
        else:
            self.ui.spinRemaining.setStyleSheet("")
        self.ui.spinSpent.setStyleSheet("")
        self.ui.spinSpent.setValue(Wolke.Char.EPspent)
    
    def epChanged(self):
        Wolke.Char.EPtotal = self.ui.spinEP.value()
        self.onModified()

    def reloadByName(self, name):
        for tab in self.tabs:
            if tab.name == name:
                if hasattr(tab.wrapper, "load"):
                    tab.wrapper.load()
                return

    def reload(self, idx):
        tab = self.tabs[idx]
        if hasattr(tab.wrapper, "load"):
            tab.wrapper.load()

    def saveButton(self):
        if self.savepath != "":
            startDir = self.savepath
        elif os.path.isdir(Wolke.Settings['Pfad-Chars']):
            startDir = os.path.join(Wolke.Settings['Pfad-Chars'], Wolke.Char.name)
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Charakter speichern...",startDir,"XML-Datei (*.xml)")
        if spath == "":
            return
        if ".xml" not in spath:
            spath = spath + ".xml"
            
        if spath.endswith("datenbank.xml"):
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Speichern des Charakters fehlgeschlagen!")
            infoBox.setInformativeText("Ich empfehle, die Regelbasis nicht mit einem Charakter zu überschreiben. \
Versuchs doch bitte nochmal mit einer anderen Zieldatei.")
            infoBox.setWindowTitle("Charakter speichern fehlgeschlagen.")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()
            return
        self.savepath = spath
        self.savePathUpdatedCallback()
        self.quicksaveButton()
            
    def quicksaveButton(self):
        if self.savepath == "":
            self.saveButton()
        else:
            Wolke.Char.xmlSchreiben(self.savepath)

        self.changed = False


    def showCharacterWizard(self):
        if not Wolke.Settings['Charakter-Assistent']:
            return

        self.wizardEd = WizardWrapper.WizardWrapper()
        self.wizardEd.form = QtWidgets.QDialog()
        self.wizardEd.form .setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)

        self.wizardEd.ui = Wizard.Ui_formMain()
        self.wizardEd.ui.setupUi(self.wizardEd.form)
        self.wizardEd.setupMainForm()
        self.wizardEd.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.wizardEd.form.show()
        self.wizardEd.form.exec()

    def showProgressBar(self, show):
        if show:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        else:
            QApplication.restoreOverrideCursor()

        self.ui.tabs.setEnabled(not show)
        self.ui.spinEP.setEnabled(not show)
        self.ui.spinRemaining.setEnabled(not show)
        self.ui.spinSpent.setEnabled(not show)
        for i in range(7, self.ui.horizontalLayout_2.count()): 
            self.ui.horizontalLayout_2.itemAt(i).widget().setVisible(not show)
        self.ui.progressBar.setVisible(show)
      
    def pdfExporterProgressCallback(self, progress):
        self.ui.progressBar.setValue(progress)

    def pdfButton(self):
        if which("pdftk") is None:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("PDFtk ist nicht installiert!")
            message = "Sephrasto benötigt PDFtk für den PDF-Export. Hier kannst du es kostenlos herunterladen:\n"

            if platform.system() != "Darwin":
                message += "https://www.pdflabs.com/tools/pdftk-server/"
            else:
                message += "https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk_server-2.02-mac_osx-10.11-setup.pkg \n\nBitte exakt diese Version!"
            messagebox.setText(message)
            messagebox.setIcon(QtWidgets.QMessageBox.Critical)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec()
            return
        
        result = -1

        for bogen in Wolke.Charakterbögen:
            if Wolke.Char.charakterbogen == os.path.basename(os.path.splitext(bogen)[0]):
                self.pdfExporter.setCharakterbogen(EventBus.applyFilter("set_charakterbogen", Wolke.Charakterbögen[bogen]))
                break

        # Check if there is a base Charakterbogen.pdf:
        if not os.path.isfile(self.pdfExporter.CharakterBogen.filePath):
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Fehler!")
            messagebox.setText("Konnte " + self.pdfExporter.CharakterBogen.filePath + " nicht im Installationsordner finden")
            messagebox.setIcon(QtWidgets.QMessageBox.Critical)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec()
            return
        
        if os.path.isfile(self.savepath):
            startDir = os.path.dirname(self.savepath)
        elif os.path.isdir(Wolke.Settings['Pfad-Chars']):
            startDir = Wolke.Settings['Pfad-Chars']
        else:
            startDir = ""

        startDir = os.path.join(startDir, Wolke.Char.name or os.path.splitext(os.path.basename(self.savepath))[0])
            
        # Let the user choose a saving location and name
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Charakterbogen erstellen...",startDir,"PDF-Datei (*.pdf)")
        if spath == "":
            return
        if ".pdf" not in spath:
            spath = spath + ".pdf"
            
        try:
            self.showProgressBar(True)
            self.pdfExporter.pdfErstellen(spath, Wolke.Char.regelnAnhaengen, self.pdfExporterProgressCallback)
            self.showProgressBar(False)
        except Exception as e:
            self.showProgressBar(False)
            raise e