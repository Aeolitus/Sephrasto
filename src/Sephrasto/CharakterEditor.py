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
from UI import CharakterMain
import platform
from CharakterAssistent.CharakterMerger import CharakterMerger
from Core.Waffe import Waffe

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

    def __init__(self, plugins, onCloseCB, savePathUpdatedCallback):
        super().__init__()
        self.plugins = plugins
        self.enabledPlugins = []
        self.onCloseCB = onCloseCB
        self.savePathUpdatedCallback = savePathUpdatedCallback
        self.savepath = ""
        self.changed = False
        self.pdfExporter = PdfExporter.PdfExporter()
        Wolke.DB = Datenbank.Datenbank()

    def loadCharacter(self, path):
        self.savepath = path
        storedHausregeln = Charakter.Char.xmlHausregelnLesen(self.savepath)
        availableHausregeln = EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"])
        if storedHausregeln in availableHausregeln:
            hausregeln = storedHausregeln
        else:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Hausregeln nicht gefunden!")
            messagebox.setText(f"Der Charakter wurde mit den Hausregeln {storedHausregeln} erstellt. Die Datei konnte nicht gefunden werden.\n\n"\
                "Bitte wähle aus, mit welchen Hausregeln der Charakter stattdessen geladen werden soll.")
            messagebox.setIcon(QtWidgets.QMessageBox.Critical )
            messagebox.addButton("OK", QtWidgets.QMessageBox.YesRole)
            messagebox.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
            combo = QtWidgets.QComboBox()
            combo.addItems(availableHausregeln)
            messagebox.layout().addWidget(combo, 1, 2)
            messagebox.exec()
            hausregeln = combo.currentText()

        self.loadDB(hausregeln)
        Wolke.Char = Charakter.Char()
        Wolke.Char.xmlLesen(self.savepath)
        
        missingPlugins = set(Wolke.Char.enabledPlugins) - set(self.enabledPlugins)
        if len(missingPlugins) > 0:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setWindowTitle("Plugin fehlt!")
            infoBox.setText("Der Charakter wurde mit einem oder mehreren Plugins erstellt, die seine Werte beeinflussen. "\
            "Nicht alle davon sind aktiv, daher können beim Speichern Daten dieser Plugins verloren gehen:\n\n" + ", ".join(missingPlugins))
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec()

        Wolke.Char.enabledPlugins = self.enabledPlugins.copy()
        Wolke.Char.aktualisieren() # A bit later because it needs access to itself

        self.show()

    def newCharacter(self):
        self.loadDB(Wolke.Settings['Datenbank'])
        Wolke.Char = Charakter.Char()
        Wolke.Char.enabledPlugins = self.enabledPlugins.copy()
        Wolke.Char.aktualisieren() # A bit later because it needs access to itself
        self.show()

    def newCharacterFromWizard(self, wizardConfig):
        self.loadDB(wizardConfig.hausregeln)
        Wolke.Char = Charakter.Char()

        if wizardConfig.geschlecht is not None:
            Wolke.Char.kurzbeschreibung = "Geschlecht: " + wizardConfig.geschlecht
            Wolke.Char.geschlecht = wizardConfig.geschlecht

        # 1. add default weapons (Sephrasto only adds them if the weapons array is empty, which might not be the case here)
        for waffe in Wolke.DB.einstellungen["Waffen: Standardwaffen"].wert:
            if waffe in Wolke.DB.waffen:
                Wolke.Char.waffen.append(Waffe(Wolke.DB.waffen[waffe]))

        # 2. add selected SKP
        if wizardConfig.spezies is not None:
            CharakterMerger.xmlLesen(Wolke.DB, wizardConfig.spezies.path, True, False)

        if wizardConfig.kultur is not None:
            CharakterMerger.xmlLesen(Wolke.DB, wizardConfig.kultur.path, False, True)

        if wizardConfig.profession is not None:
            CharakterMerger.xmlLesen(Wolke.DB, wizardConfig.profession.path, False, False)

        # 3. Handle choices afterwards so EP spent can be displayed accurately
        if wizardConfig.spezies is not None:
            CharakterMerger.handleChoices(Wolke.DB, wizardConfig.spezies, wizardConfig.geschlecht, True, False, False)

        if wizardConfig.kultur is not None:
            CharakterMerger.handleChoices(Wolke.DB, wizardConfig.kultur, wizardConfig.geschlecht, False, True, False)

        if wizardConfig.profession is not None:
            CharakterMerger.handleChoices(Wolke.DB, wizardConfig.profession, wizardConfig.geschlecht, False, False, True)

        Wolke.Char.enabledPlugins = self.enabledPlugins.copy()
        Wolke.Char.aktualisieren() # A bit later because it needs access to itself
        self.show()

    def loadDB(self, hausregeln):
        if Wolke.DB.datei is None or Wolke.DB.hausregelDatei != hausregeln:
            if not Wolke.DB.xmlLaden(hausregeln = hausregeln, isCharakterEditor = True):
                messagebox = QtWidgets.QMessageBox()
                messagebox.setWindowTitle("Fehler!")
                messagebox.setText(hausregeln + " ist keine valide Datenbank-Datei! Der Charaktereditor wird ohne Hausregeln gestartet.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)  
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messagebox.exec()
        self.enabledPlugins = []
        for pluginData in self.plugins:
            if pluginData.plugin is not None and hasattr(pluginData.plugin, "changesCharacter") and pluginData.plugin.changesCharacter():
                self.enabledPlugins.append(pluginData.name)

    def show(self):
        self.form = QtWidgets.QWidget()
        self.ui = CharakterMain.Ui_formMain()
        self.ui.setupUi(self.form)
        self.ui.tabs.removeTab(0)
        self.ui.tabs.removeTab(0)
        
        windowSize = Wolke.Settings["WindowSize-Charakter"]
        self.form.resize(windowSize[0], windowSize[1])

        self.ui.scrollArea.wheelEvent = self.wheelEvent

        self.updateEP()

        tabs = []

        beschrWrapper = EventBus.applyFilter("class_beschreibung_wrapper", CharakterBeschreibungWrapper.BeschrWrapper)
        if beschrWrapper:
            self.beschrWrapper = beschrWrapper()
            tabs.append(Tab(0, self.beschrWrapper, self.beschrWrapper.form, "Beschreibung"))

        detailsWrapper = EventBus.applyFilter("class_beschreibungdetails_wrapper", CharakterBeschreibungDetailsWrapper.CharakterBeschreibungDetailsWrapper)
        if detailsWrapper:
            self.beschrDetailsWrapper = detailsWrapper()
            tabs.append(Tab(10, self.beschrDetailsWrapper, self.beschrDetailsWrapper.form, "Hintergrund"))

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
        self.updateDetailsVisibility()

        self.ui.buttonSave.clicked.connect(self.saveButton)
        self.ui.buttonQuicksave.clicked.connect(self.quicksaveButton)
        self.ui.buttonSavePDF.clicked.connect(self.pdfButton)
        self.ui.spinEP.valueChanged.connect(self.epChanged)

        self.reload(self.ui.tabs.currentIndex())

        self.form.closeEvent = self.closeEvent
        self.form.show()
        
    def wheelEvent(self, ev):
        if ev.type() == QtCore.QEvent.Wheel:
            if not self.ui.scrollArea.hasFocus():
                ev.ignore()

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
            Wolke.Char = None
            Wolke.DB = None
            self.onCloseCB()
    
    def onModified(self):
        self.changed = True
        Wolke.Char.aktualisieren()
        self.updateEP()
        self.updateDetailsVisibility()

    def updateDetailsVisibility(self):
        if hasattr(self, "beschrDetailsWrapper"):
            self.ui.tabs.setTabVisible(self.ui.tabs.indexOf(self.beschrDetailsWrapper.form), Wolke.Char.detailsAnzeigen)
            if hasattr(self, "beschrWrapper"):
                self.beschrWrapper.onDetailsVisibilityChanged(Wolke.Char.detailsAnzeigen)

    def updateEP(self):
        self.ui.spinEP.setValue(Wolke.Char.epGesamt)
        self.ui.spinRemaining.setValue(Wolke.Char.epGesamt-Wolke.Char.epAusgegeben)
        if Wolke.Char.epGesamt < Wolke.Char.epAusgegeben:
            self.ui.spinRemaining.setStyleSheet("QSpinBox { color: white; background-color: rgb(200,50,50) }")
        else:
            self.ui.spinRemaining.setStyleSheet("")
        self.ui.spinSpent.setStyleSheet("")
        self.ui.spinSpent.setValue(Wolke.Char.epAusgegeben)
    
    def epChanged(self):
        Wolke.Char.epGesamt = self.ui.spinEP.value()
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
            
        self.pdfExporter.pdfErstellen(spath, Wolke.Char.regelnAnhaengen)