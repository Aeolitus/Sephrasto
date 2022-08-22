#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:30:34 2017

@author: Aeolitus
"""
from PyQt5 import QtWidgets, QtCore, QtGui
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
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QToolTip
from Hilfsmethoden import Hilfsmethoden
import platform

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
    messagebox.exec_()

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
        logging.critical("Qt " + QtCore.qVersion() + " PyQt " + QtCore.PYQT_VERSION_STR) #for people that start from source

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
        
        #Make sure the application scales properly, i.e. in Win10 users can change the UI scale in the display settings
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
   
        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
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
        
        if platform.system() != 'Windows': # hardcoded for windows, qt doesnt provide the correct font here
            defaultFont = QtGui.QFont()
            Wolke.DefaultOSFont = defaultFont.family()
            fontSize = defaultFont.pointSize()
            if fontSize != -1:
                Wolke.DefaultOSFontSize = fontSize

        # Get the Settings loaded
        EinstellungenWrapper.load()
        logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])

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
                messagebox.exec_()

        EventBus.doAction("plugins_geladen")

        EventBus.addAction("charaktereditor_reload", self.charakterEditorReloadHook)
        EventBus.addAction("charaktereditor_modified", self.charakterEditorModifiedHook)

        self.form.show()

        exitcode = self.app.exec_()
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

    def buildStylesheet(self, readonlyColor, panelColor, buttonColor = None):
        standardFont = f"font-family: '{Wolke.Settings['Font']}'"
        headingFont = f"font-family: '{Wolke.Settings['FontHeading']}'; color: {Wolke.HeadingColor}"

        css = f"""*[readOnly=\"true\"] {{ background-color: {readonlyColor}; border: none; }}
        QWidget, QToolTip {{ {standardFont}; font-size: {Wolke.Settings['FontSize']}pt; }}
        QHeaderView::section {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']-1}pt; {headingFont}; }}
        .smallText {{ font-size: {Wolke.Settings['FontSize']-1}pt; }}
        .italic {{ font-style: italic; }}
        .panel {{ background: {panelColor}; }}
        .h1 {{ font-weight: bold; font-size: {Wolke.FontHeadingSizeL1}pt; {headingFont}; }}
        .h2 {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']}pt; {headingFont}; }}
        .h3, QGroupBox {{ font-weight: bold; font-variant: small-caps; font-size: {Wolke.FontHeadingSizeL3}pt; {standardFont}; color: {Wolke.HeadingColor}; }}
        .h4 {{ font-weight: bold; }}
        .title {{ font-weight: bold; font-size: 16pt; {headingFont}; }}
        .icon {{ font-size: {Wolke.Settings['IconSize']}pt; font-weight: {Hilfsmethoden.qtWeightToCSS(QtGui.QFont.Black)}; font-family: 'Font Awesome 6 Free Solid'; }}"""

        if buttonColor:
            css += f"QPushButton {{ background-color: {buttonColor}; }}"
        self.app.setStyleSheet(css)

    def updateAppearance(self):
        fonts = ["Aniron", "Crimson Pro", "Fontawesome"]
        for font in fonts:
            for file in Hilfsmethoden.listdir(os.path.join("Data", "Fonts", font)):
                if file.endswith(".ttf"):
                    # We need an absolute path here for macos
                    QtGui.QFontDatabase.addApplicationFont(os.path.join(os.getcwd(), "Data", "Fonts", font, file))

        Wolke.FontHeadingSizeL1 = Wolke.Settings["FontHeadingSize"] + 1
        Wolke.FontHeadingSizeL3 = Wolke.Settings["FontSize"] + 2

        style = Wolke.Settings['Theme']
        if style == "Windows Vista":
            self.app.setStyle("windowsvista")
            palette = self.app.style().standardPalette()
            self.app.setPalette(palette)
            QToolTip.setPalette(self.app.style().standardPalette())
            Wolke.HeadingColor = "#000000"
            Wolke.BorderColor = "rgba(0,0,0,0.2)"
            self.buildStylesheet("#ffffff", "#b3b3b3")
        elif style == "Fusion Light":
            self.app.setStyle('fusion')
            palette = self.app.style().standardPalette()
            palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
            palette.setColor(QPalette.ToolTipText, QtCore.Qt.black)
            self.app.setPalette(palette)
            QToolTip.setPalette(palette)
            Wolke.HeadingColor = "#000000"
            Wolke.BorderColor = "rgba(0,0,0,0.2)"
            self.buildStylesheet("#ffffff", "#b3b3b3")
        elif style == "Fusion Dark":
            self.app.setStyle('fusion')
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, QtCore.Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, QtCore.Qt.black)
            palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
            palette.setColor(QPalette.Text, QtCore.Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
            palette.setColor(QPalette.BrightText, QtCore.Qt.white)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
            palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, QtCore.Qt.darkGray)
            palette.setColor(QPalette.Disabled, QPalette.WindowText, QtCore.Qt.darkGray)
            palette.setColor(QPalette.Disabled, QPalette.Text, QtCore.Qt.darkGray)
            palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QtCore.Qt.darkGray)
            palette.setColor(QPalette.Disabled, QPalette.Base, QColor(53, 53, 53))
            self.app.setPalette(palette)
            QToolTip.setPalette(palette)
            Wolke.HeadingColor = "#ffffff"
            Wolke.BorderColor = "rgba(255,255,255,0.2)"
            self.buildStylesheet("#434343", "#7d7d7d")
        elif style == "Ilaris":
            self.app.setStyle('fusion')

            palette = QPalette()
            colors = {
                "box" : QColor("#d1be9d"),
                "bg": QColor("#f1e6ce"),
                "heading" : QColor("#4A000B"),
                "text": QColor("#221E1F"),
                "table": QColor("#e8c5a9"),
                "bg_bestiarium" : QColor("#f7e5cd"),
                "bg_dark" : QColor("#e4d0a5"),
                "text_dark": QColor("#7a561c")
            }

            palette.setColor(QPalette.Window, colors["bg"])
            palette.setColor(QPalette.WindowText, colors["text"])
            palette.setColor(QPalette.Base, colors["bg"])
            palette.setColor(QPalette.AlternateBase, colors["table"])
            palette.setColor(QPalette.ToolTipBase, colors["bg"])
            palette.setColor(QPalette.ToolTipText, colors["text"])
            palette.setColor(QPalette.Text, colors["text"])
            palette.setColor(QPalette.Button, colors["bg_dark"])
            palette.setColor(QPalette.ButtonText, colors["text"])
            palette.setColor(QPalette.BrightText, colors["text"])
            palette.setColor(QPalette.Link, colors["heading"])
            palette.setColor(QPalette.Highlight, colors["box"])
            palette.setColor(QPalette.HighlightedText, colors["text"])
            #palette.setColor(QPalette.Active, QPalette.Button, colors["box"])
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.WindowText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.Text, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.HighlightedText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.Base, colors["bg_dark"])
            self.app.setPalette(palette)
            QToolTip.setPalette(palette)
            Wolke.HeadingColor = "#4A000B"
            Wolke.BorderColor = "rgba(0,0,0,0.2)"
            self.buildStylesheet("#e4d0a5", Wolke.HeadingColor, Wolke.BorderColor, "#d1bd94")
        elif style == "Loirana":
            self.app.setStyle('fusion')

            palette = QPalette()
            colors = {
                "box" : QColor("#ffb86c"),
                "bg": QColor("#282a36"),
                "heading" : QColor("#bd93f9"),
                "text": QColor("#f8f8f2"),
                "table": QColor("#6272a4"),
                "bg_bestiarium" : QColor("#44475a"),
                "bg_dark" : QColor("#44475a"),
                "text_dark": QColor("#ff5555")
            }

            palette.setColor(QPalette.Window, colors["bg"])
            palette.setColor(QPalette.WindowText, colors["text"])
            palette.setColor(QPalette.Base, colors["bg"])
            palette.setColor(QPalette.AlternateBase, colors["table"])
            palette.setColor(QPalette.ToolTipBase, colors["bg"])
            palette.setColor(QPalette.ToolTipText, colors["text"])
            palette.setColor(QPalette.Text, colors["text"])
            palette.setColor(QPalette.Button, colors["bg_dark"])
            palette.setColor(QPalette.ButtonText, colors["text"])
            palette.setColor(QPalette.BrightText, colors["text"])
            palette.setColor(QPalette.Link, colors["heading"])
            palette.setColor(QPalette.Highlight, colors["box"])
            palette.setColor(QPalette.HighlightedText, colors["text"])
            #palette.setColor(QPalette.Active, QPalette.Button, colors["box"])
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.WindowText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.Text, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.HighlightedText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.Base, colors["bg_dark"])
            self.app.setPalette(palette)
            QToolTip.setPalette(palette)
            Wolke.HeadingColor = "#bd93f9"
            Wolke.BorderColor = "rgba(0,0,0,0.2)"
            self.buildStylesheet("#44475a", Wolke.HeadingColor, Wolke.BorderColor, "#44475a")
            self.buildStylesheet("#e4d0a5", "#e8c5a9", "#d1bd94")
        elif style == "DSA Forum":
            self.app.setStyle('fusion')
            palette = QPalette()
            # DSA-Forum colors (picked from screenshot)
            colors = {
                "bg_light": QColor("#f6efe2"),
                "bg": QColor("#f1e2c3"),
                "bg_dark": QColor("#cdad74"),  # bg braun (hover tabs) 
                "button": QColor("#dcc484"),  # tabs buttons rahmen
                "text": QColor("#000000"),
                "text_dark": QColor("#7a561c"),
                "alert": QColor("#ae0007"),  # text rot
            }
            palette.setColor(QPalette.Window, colors["bg"])
            palette.setColor(QPalette.WindowText, colors["text"])
            palette.setColor(QPalette.Base, colors["bg"])
            palette.setColor(QPalette.AlternateBase, colors["bg_light"])
            palette.setColor(QPalette.ToolTipBase, colors["bg"])
            palette.setColor(QPalette.ToolTipText, colors["text"])
            palette.setColor(QPalette.Text, colors["text"])
            palette.setColor(QPalette.Button, colors["button"])
            palette.setColor(QPalette.ButtonText, colors["text"])
            palette.setColor(QPalette.BrightText, colors["text"])
            palette.setColor(QPalette.Link, colors["text_dark"])
            palette.setColor(QPalette.Highlight, colors["bg_dark"])
            palette.setColor(QPalette.HighlightedText, colors["text"])
            #palette.setColor(QPalette.Active, QPalette.Button, colors["alert"])
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.WindowText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.Text, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.HighlightedText, colors["text_dark"])
            palette.setColor(QPalette.Disabled, QPalette.Base, colors["bg_dark"])
            self.app.setPalette(palette)
            QToolTip.setPalette(palette)
            Wolke.HeadingColor = "#000000"
            Wolke.BorderColor = "rgba(0,0,0,0.2)"
            self.buildStylesheet("#dcc484", "#f6efe2")
        
if __name__ == "__main__":
    itm = MainWindowWrapper()