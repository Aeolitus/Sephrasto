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
import DatenbankEdit
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

loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
logging.basicConfig(filename="sephrasto.log", \
    level=loglevels[Wolke.Settings['Logging']], \
    format="%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s(%(lineno)d) | %(message)s")

def sephrasto_excepthook(exc_type, exc_value, tb):
    traceback = [' Traceback (most recent call last):']
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        traceback.append('   File "%.500s", line %d, in %.500s' %(filename, lineno, name))
        tb = tb.tb_next

    # Exception type and value
    exception = ' %s: %s' %(exc_type.__name__, exc_value)
    logging.critical(exception + "\n".join(traceback))

    #Try to show message box, hopefully its not a crash in Qt
    messagebox = QtWidgets.QMessageBox()
    messagebox.setWindowTitle("Fehler!")
    messagebox.setText("Unerwarteter Fehler:" + exception + ". Bei Fragen zum diesem Fehler bitte sephrasto.log mitsenden.")
    messagebox.setIcon(QtWidgets.QMessageBox.Critical)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    messagebox.exec_()

class PluginData(object):
    def __init__(self, name, description, plugin):
        super().__init__()
        self.name = name
        self.description = description
        self.plugin = plugin

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

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        #Make sure the application scales properly, i.e. in Win10 users can change the UI scale in the display settings
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
   
        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)

        self.Form = QtWidgets.QWidget()
        self.ui = UI.MainWindow.Ui_Form()
        self.ui.setupUi(self.Form)
        self.ui.buttonNew.clicked.connect(self.createNew)
        self.ui.buttonEdit.clicked.connect(self.editExisting)
        self.ui.buttonRules.clicked.connect(self.editRuleset)
        self.ui.buttonSettings.clicked.connect(self.editSettings)
        self.ui.buttonHelp.clicked.connect(self.help)
        self.ui.labelVersion.setText(self._version_ + " - by Aeolitus ")

        self.app.setWindowIcon(QtGui.QIcon('icon_large.png'))
        
        # Get the Settings loaded
        EinstellungenWrapper.load()
        logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])

        windowSize = Wolke.Settings["WindowSize-Main"]
        self.Form.resize(windowSize[0], windowSize[1])

        self.updateAppearance()
        self.ui.label.setFont(QtGui.QFont("Aniron", 16))
        self.ui.label.setStyleSheet("color: " + Wolke.HeadingColor + ";}")

        UpdateChecker.checkForUpdate()

        self._plugins = []
        for pluginName in PluginLoader.getPlugins(Wolke.Settings['Pfad-Plugins']):
            description = PluginLoader.getPluginDescription(Wolke.Settings['Pfad-Plugins'], pluginName)
            if pluginName in Wolke.Settings['Deaktivierte-Plugins']:
                self._plugins.append(PluginData(pluginName, description, None))
                continue

            plugin = PluginLoader.loadPlugin(Wolke.Settings['Pfad-Plugins'], pluginName)
            self._plugins.append(PluginData(pluginName, description, plugin))
            logging.critical("Plugin: loaded " + pluginName)
            if hasattr(plugin, "createMainWindowButtons"):
                for button in plugin.createMainWindowButtons():
                    button.setParent(self.Form)
                    self.ui.vlPluginButtons.addWidget(button)

        EventBus.doAction("plugins_geladen")

        EventBus.addAction("charaktereditor_reload", self.charakterEditorReloadHook)
        EventBus.addAction("charaktereditor_modified", self.charakterEditorModifiedHook)

        self.Form.show()

        exitcode = self.app.exec_()
        Wolke.Settings["WindowSize-Main"] = [self.Form.size().width(), self.Form.size().height()]
        EinstellungenWrapper.save()

        sys.exit(exitcode)

    def charakterEditorReloadHook(self, params):
        if self.ed and not self.ed.formMain.isHidden():
            self.ed.reloadAll()
            
    def charakterEditorModifiedHook(self, params):
        if hasattr(self, "ed") and self.ed and not self.ed.formMain.isHidden():
            self.ed.onModified()
        
    def createNew(self):
        '''
        Creates a new CharakterEditor which is empty and shows it.
        '''
        EventBus.doAction("charaktereditor_oeffnet", { "neu" : True, "filepath" : "" })
        self.ed = CharakterEditor.Editor(self._plugins, self.savePathUpdated)
        if self.ed.noDatabase:
            raise Exception("Konnte datenbank.xml nicht finden")
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = UI.CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        self.savePathUpdated()
        self.ed.formMain.show()
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
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = UI.CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        self.savePathUpdated()
        self.ed.formMain.show()
        EventBus.doAction("charaktereditor_geoeffnet", { "neu" : False, "filepath" : spath })
        
    def editRuleset(self):
        '''
        Creates the DatenbankEdit Form and shows the contents of datenbank.xml.
        '''
        self.D = DatenbankEdit.DatenbankEdit(self._plugins)
        self.D.Form = QtWidgets.QWidget()
        self.D.ui = UI.DatenbankMain.Ui_Form()
        self.D.ui.setupUi(self.D.Form)
        self.D.setupGUI()
        self.D.Form.show()
        
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
        self.ed.formMain.setWindowTitle("Sephrasto" + file + rules)

    def buildStylesheet(self, readonlyColor, headingColor, borderColor, buttonColor = None):
        fontSize = str(Wolke.Settings['FontSize'])
        fontFamily = str(Wolke.Settings['Font'])
        styleReadonly = "*[readOnly=\"true\"] { background-color: " + readonlyColor + "; border: none; }"
        styleTooltip =  "QToolTip { font: " + str(fontSize) + "pt '" + fontFamily + "'; }"
        styleCombo = "QComboBox { font: " + str(fontSize) + "pt '" + fontFamily + "'; }"
        styleTableHeader = "QHeaderView::section { font: bold " + str(Wolke.Settings['FontHeadingSize']-1) + "pt '" + Wolke.Settings['FontHeading'] + "'; color: " + headingColor + "; }"
        styleTable = "QTableView { font: " + str(fontSize) + "pt '" + fontFamily + "'; }"
        styleList = "QListView { font: " + str(fontSize) + "pt '" + fontFamily + "'; }"
        styleTree = "QTreeWidget { font: " + str(fontSize) + "pt '" + fontFamily + "'; }"
        styleGroupbox = "QGroupBox { font: " + str(Wolke.FontHeadingSizeL3) + "pt '" + fontFamily + "'; font-weight: bold; font-variant: small-caps; color: " + headingColor + "; }"
        styleMessagebox = "QMessageBox { font: " + str(fontSize) + "pt '" + fontFamily + "'; }"
        styleButton = ""
        if buttonColor:
            styleButton = "QPushButton { background-color: " + buttonColor + " }"
        self.app.setStyleSheet(styleReadonly + styleTooltip + styleCombo + styleTableHeader + styleTable + styleList + styleTree + styleGroupbox + styleButton + styleMessagebox)

    def updateAppearance(self):
        fonts = ["Crimson Pro", "Fontawesome"]
        for font in fonts:
            for file in Hilfsmethoden.listdir(os.path.join("Data", "Fonts", font)):
                if file.endswith(".ttf"):
                    QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "Fonts", font, file))

        fontSize = Wolke.Settings['FontSize']
        fontFamily = Wolke.Settings['Font']
        if fontFamily:
            font = QtGui.QFontDatabase().font(fontFamily, "Regular", fontSize)
            self.app.setFont(font)
        else:
            font = self.app.font()
            font.setPointSize(fontSize)
            self.app.setFont(font)

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
            self.buildStylesheet("#ffffff", Wolke.HeadingColor, Wolke.BorderColor)
        elif style == "Fusion Light":
            self.app.setStyle('fusion')
            palette = self.app.style().standardPalette()
            palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
            palette.setColor(QPalette.ToolTipText, QtCore.Qt.black)
            self.app.setPalette(palette)
            QToolTip.setPalette(palette)
            Wolke.HeadingColor = "#000000"
            Wolke.BorderColor = "rgba(0,0,0,0.2)"
            self.buildStylesheet("#ffffff", Wolke.HeadingColor, Wolke.BorderColor)
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
            self.buildStylesheet("#434343", Wolke.HeadingColor, Wolke.BorderColor)
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
            self.buildStylesheet("#dcc484", Wolke.HeadingColor, Wolke.BorderColor)
        
if __name__ == "__main__":
    itm = MainWindowWrapper()