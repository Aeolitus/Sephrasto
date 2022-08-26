#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:30:34 2017

@author: Aeolitus
"""
import PySide6
from PySide6 import QtWidgets, QtCore, QtGui
import sys
import logging
import os
import os.path
import UI.MainWindow
import CharakterEditor
import DatenbankEditor
import UI.CharakterMain
import UI.DatenbankMain
from Wolke import Wolke
import yaml
from EinstellungenWrapper import EinstellungenWrapper
from HilfeWrapper import HilfeWrapper
import Version
from EventBus import EventBus
from PluginLoader import PluginLoader
from UpdateChecker import UpdateChecker
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QToolTip
from Hilfsmethoden import Hilfsmethoden
import platform

import PathHelper

loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
logging.basicConfig(filename="sephrasto.log", \
    level=loglevels[Wolke.Settings['Logging']], \
    format="%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s(%(lineno)d) | %(message)s")

def sephrasto_excepthook(exc_type, exc_value, tb):
    traceback = [' Traceback (most recent call last):']

    filename = ""
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        traceback.append('   File "%.500s", line %d, in %.500s' %(filename, lineno, name))
        if not tb.tb_next:
            break
        tb = tb.tb_next

    # Exception type and value
    exception = ' %s: %s' %(exc_type.__name__, exc_value)
    logging.critical(exception + "\n".join(traceback))

    #Try to show message box, hopefully its not a crash in Qt
    text = "Unerwarteter Fehler:" + exception + ". Bei Fragen zum diesem Fehler bitte sephrasto.log mitsenden."
    if Wolke.Settings['Pfad-Plugins'] in filename:
        splitPath = os.path.split(os.path.relpath(filename, Wolke.Settings['Pfad-Plugins']))
        if len(splitPath) > 0:
            text = f"Das Plugin {splitPath[0]} hat einen Fehler verursacht:\n{exception}.\n\nEs ist vermutlich nicht mit dieser Sephrastoversion kompatibel, bitte wende dich an den Plugin-Autor."    

    messagebox = QtWidgets.QMessageBox()
    messagebox.setWindowTitle("Fehler!")
    messagebox.setText(text)
    messagebox.setIcon(QtWidgets.QMessageBox.Critical)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    messagebox.exec()

class MainWindowWrapper(object):
    '''
    Main Class responsible for running the entire application. 
    Just shows three buttons and handles the execution of the individual subparts.
    '''

    def __init__(self):
        sys.excepthook = sephrasto_excepthook

        '''
        Initializes the GUI and connects the buttons.
        '''
        self._version_ = "v" + str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build)
        logging.critical("Starte Sephrasto " + self._version_) #critical so it's always printed, independent of the debug level setting
        logging.critical(f"Qt {QtCore.qVersion()} PySide {PySide6.__version__} (compiled with Qt {QtCore.__version__})") #for people that start from source

        super().__init__()

        # Set current directory so we can use relative paths
        # There are many test cases, i.e. starting from VS, from a different folder, with python, directly Sephrasto.py via shebang, built exe etc. and much can go wrong
        # We need to remember the old current dir for restarting purposes via settings  - again things can go wrong otherwise
        # Also on windows there is a weird issue when starting Sephrasto.exe from a different folder, so we use sys.argv[0] as a fallback (which doesnt work in other cases -.-)
        EinstellungenWrapper.oldWorkingDir = os.getcwd() 
        if os.path.isfile(os.path.abspath(__file__)):
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
        else:
            os.chdir(os.path.dirname(sys.argv[0]))

        # Get the Settings loaded
        EinstellungenWrapper.load()
        logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])

        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1" if Wolke.Settings['DPI-Skalierung'] else "0"

        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)

        # Font hinting adjusts font outlines for lining up with the raster grid. This was apparently important for low res which nobody has anymore today.
        # In my tests it made stuff look worse, especially the fontawesome icons, so we are disabling it
        font = self.app.font()
        font.setHintingPreference(QtGui.QFont.HintingPreference.PreferNoHinting)
        self.app.setFont(font)

        # Query system font and font size for settings dialog restore option
        defaultFont = QtGui.QFont()
        Wolke.DefaultOSFont = defaultFont.family() 
        fontSize = defaultFont.pointSize()
        if fontSize != -1:
            Wolke.DefaultOSFontSize = fontSize
            if Wolke.Settings['FontSize'] == 0:
                Wolke.Settings['FontSize'] = Wolke.DefaultOSFontSize

        self.form = QtWidgets.QWidget()
        self.ui = UI.MainWindow.Ui_Form()
        self.ui.setupUi(self.form)
        self.ui.buttonNew.clicked.connect(self.createNew)
        self.ui.buttonEdit.clicked.connect(self.editExisting)
        self.ui.buttonRules.clicked.connect(self.editRuleset)
        self.ui.buttonSettings.clicked.connect(self.editSettings)
        self.ui.buttonHelp.clicked.connect(self.help)
        self.ui.labelVersion.setText(self._version_ + " - by Aeolitus ")
        self.app.setWindowIcon(QtGui.QIcon('icon_large.png'))

        windowSize = Wolke.Settings["WindowSize-Main"]
        self.form.resize(windowSize[0], windowSize[1])

        self.updateAppearance()

        self.ui.buttonHelp.setText("\uf059")
        self.ui.buttonSettings.setText("\uf013")

        UpdateChecker.checkForUpdate()

        self._plugins = []
        for pluginData in PluginLoader.getPlugins(Wolke.Settings['Pfad-Plugins']):
            if pluginData.name in Wolke.Settings['Deaktivierte-Plugins']:
                self._plugins.append(pluginData)
                continue

            if pluginData.load():
                self._plugins.append(pluginData)
                logging.critical("Plugin: loaded " + pluginData.name)
                if hasattr(pluginData.plugin, "createMainWindowButtons"):
                    for button in pluginData.plugin.createMainWindowButtons():
                        button.setParent(self.form)
                        self.ui.vlPluginButtons.addWidget(button)
            else:
                messagebox = QtWidgets.QMessageBox()
                messagebox.setWindowTitle("Fehler!")
                messagebox.setText(f"Das Laden des Plugins {pluginData.name} ist fehlgeschlagen.\nEs ist vermutlich nicht mit dieser Sephrastoversion kompatibel, bitte wende dich an den Plugin-Autor.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messagebox.exec()

        EventBus.doAction("plugins_geladen")

        EventBus.addAction("charaktereditor_reload", self.charakterEditorReloadHook)
        EventBus.addAction("charaktereditor_modified", self.charakterEditorModifiedHook)

        self.form.show()

        exitcode = self.app.exec()
        Wolke.Settings["WindowSize-Main"] = [self.form.size().width(), self.form.size().height()]
        EinstellungenWrapper.save()

        sys.exit(exitcode)

    def charakterEditorReloadHook(self, params):
        if self.ed and not self.ed.form.isHidden():
            self.ed.reloadByName(params["name"])
            
    def charakterEditorModifiedHook(self, params):
        if hasattr(self, "ed") and self.ed and not self.ed.form.isHidden():
            self.ed.onModified()
        
    def createNew(self):
        '''
        Creates a new CharakterEditor which is empty and shows it.
        '''
        EventBus.doAction("charaktereditor_oeffnet", { "neu" : True, "filepath" : "" })
        self.ed = CharakterEditor.Editor(self._plugins, self.savePathUpdated)
        if self.ed.noDatabase:
            raise Exception("Konnte datenbank.xml nicht finden")
        self.ed.form = QtWidgets.QWidget()
        self.ed.ui = UI.CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.form)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        self.savePathUpdated()
        self.ed.form.show()
        EventBus.doAction("charaktereditor_geoeffnet", { "neu" : True, "filepath" : "" })
        
    def editExisting(self):
        '''
        Creates a CharakterEditor for an existing character and shows it.
        '''
        if os.path.isdir(Wolke.Settings['Pfad-Chars']):
            startDir = Wolke.Settings['Pfad-Chars']
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Charakter laden...",startDir,"XML-Datei (*.xml)")
        if spath == "":
            return
        if not spath.endswith(".xml"):
            spath = spath + ".xml"

        EventBus.doAction("charaktereditor_oeffnet", { "neu" : False, "filepath" : spath })
        self.ed = CharakterEditor.Editor(self._plugins, self.savePathUpdated, spath)
        if self.ed.noDatabase:
            raise Exception("Konnte datenbank.xml nicht finden")
        self.ed.form = QtWidgets.QWidget()
        self.ed.ui = UI.CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.form)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        self.savePathUpdated()
        self.ed.form.show()
        EventBus.doAction("charaktereditor_geoeffnet", { "neu" : False, "filepath" : spath })
        
    def editRuleset(self):
        '''
        Creates the DatenbankEdit Form and shows the contents of datenbank.xml.
        '''
        self.D = DatenbankEditor.DatenbankEditor(self._plugins)
        self.D.form = QtWidgets.QWidget()
        self.D.ui = UI.DatenbankMain.Ui_Form()
        self.D.ui.setupUi(self.D.form)
        self.D.setupGUI()
        self.D.form.show()
        
    def editSettings(self):
        EinstellungenWrapper(self._plugins)

    def help(self):
        if not hasattr(self, "hilfe"):
            self.hilfe = HilfeWrapper()
        else:
            self.hilfe.form.show()
            self.hilfe.form.activateWindow()

    def savePathUpdated(self):
        file = " - Neuer Charakter"
        if self.ed.savepath:
            file = " - " + os.path.basename(self.ed.savepath)
        rules = ""
        if Wolke.DB.datei:
           rules = " (" + os.path.splitext(os.path.basename(Wolke.DB.datei))[0] + ")"
        self.ed.form.setWindowTitle("Sephrasto" + file + rules)

    def updateAppearance(self):
        # Load fonts
        fonts = ["Aniron", "Crimson Pro", "Fontawesome"]
        for font in fonts:
            for file in PathHelper.listdir(os.path.join("Data", "Fonts", font)):
                if file.endswith(".ttf") or file.endswith(".otf"):
                    # We need an absolute path here for macos
                    result = QtGui.QFontDatabase.addApplicationFont(os.path.join(os.getcwd(), "Data", "Fonts", font, file))
                    if result == -1:
                        logging.error("Could not add font " + file)

        Wolke.FontHeadingSizeL1 = Wolke.Settings["FontHeadingSize"] + 1
        Wolke.FontHeadingSizeL3 = Wolke.Settings["FontSize"] + 2

        # Set theme
        themeName = Wolke.Settings['Theme']
        if themeName in Wolke.Themes:
            theme = Wolke.Themes[themeName]

            # Set style, i.e. fusion
            self.app.setStyle(theme["Style"])

            # Set color palette
            if "StandardPalette" in theme and theme["StandardPalette"]:
                palette = self.app.style().standardPalette()
            else:
                palette = QPalette()

            if "Palette" in theme:
                for elem, col in theme["Palette"].items():
                    if not hasattr(QPalette, elem):
                        logging.warning("Theme tries to set invalid QPalette element " + elem)
                        continue
                    palette.setColor(getattr(QPalette, elem), QColor(col))

            if "Palette-Active" in theme:
                for elem, col in theme["Palette-Active"].items():
                    if not hasattr(QPalette, elem):
                        logging.warning("Theme tries to set invalid QPalette element " + elem)
                        continue
                    palette.setColor(QPalette.Active, getattr(QPalette, elem), QColor(col))

            if "Palette-Disabled" in theme:
                for elem, col in theme["Palette-Disabled"].items():
                    if not hasattr(QPalette, elem):
                        logging.warning("Theme tries to set invalid QPalette element " + elem)
                        continue
                    palette.setColor(QPalette.Disabled, getattr(QPalette, elem), QColor(col))

            self.app.setPalette(palette)
            QToolTip.setPalette(palette)

            # Set remaining colors that we also need elsewhere in the code
            if "HeadingColor" in theme:
                Wolke.HeadingColor = theme["HeadingColor"]
            if "BorderColor" in theme:
                Wolke.BorderColor = theme["BorderColor"]
            if "ReadonlyColor" in theme:
                Wolke.ReadonlyColor = theme["ReadonlyColor"]
            if "PanelColor" in theme:
                Wolke.PanelColor = theme["PanelColor"]
        else:
            theme = ''

        # Create stylesheet
        standardFont = f"font-family: '{Wolke.Settings['Font']}'"
        headingFont = f"font-family: '{Wolke.Settings['FontHeading']}'; color: {Wolke.HeadingColor}"
        Wolke.FontAwesomeCSS = f"font-size: {min(Wolke.Settings['FontSize'], 12)}pt; font-family: \"Font Awesome 6 Free Solid\"; font-weight: 900;"
        css = f"""*[readOnly=\"true\"] {{ background-color: {Wolke.ReadonlyColor}; border: none; }}
QWidget, QToolTip {{ {standardFont}; font-size: {Wolke.Settings['FontSize']}pt; }}
QHeaderView::section {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']-1}pt; {headingFont}; }}
QListView::item {{ margin-top: 4px; margin-bottom: 4px; }}
QTreeView::item {{ margin-top: 4px; margin-bottom: 4px; }}
.smallText {{ font-size: {Wolke.Settings['FontSize']-1}pt; }}
.italic {{ font-style: italic; }}
.panel {{ background: {Wolke.PanelColor}; }}
.h1 {{ font-weight: bold; font-size: {Wolke.FontHeadingSizeL1}pt; {headingFont}; }}
.h2 {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']}pt; {headingFont}; }}
.h3, QGroupBox {{ font-weight: bold; font-variant: small-caps; font-size: {Wolke.FontHeadingSizeL3}pt; {standardFont}; color: {Wolke.HeadingColor}; }}
.h4 {{ font-weight: bold; }}
.title {{ font-weight: bold; font-size: 16pt; {headingFont}; }}
.icon {{ {Wolke.FontAwesomeCSS} }}\n"""

        if 'CSS' in theme:
            css += theme['CSS']
        self.app.setStyleSheet(css)
        
if __name__ == "__main__":
    itm = MainWindowWrapper()