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
import UI.DatenbankMain
from Wolke import Wolke
import yaml
from EinstellungenWrapper import EinstellungenWrapper
from WebEngineWrapper import WebEngineWrapper
import Version
from EventBus import EventBus
from PluginLoader import PluginLoader
from UpdateChecker import UpdateChecker
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QToolTip
from PySide6.QtCore import QLocale
from Hilfsmethoden import Hilfsmethoden
import platform
import PathHelper
from CharakterListe import CharakterListe
from CharakterAssistent import WizardWrapper
import argparse
import Charakter
import Datenbank
import locale

locale.setlocale(locale.LC_ALL, "") # set the current locale from the OS

loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}

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
    exception = '%s: %s' %(exc_type.__name__, exc_value)
    logging.critical(exception + "\n".join(traceback))

    #Try to show message box, hopefully its not a crash in Qt
    text = exception + "\n\nBei Fragen zum diesem Fehler bitte sephrasto.log aus dem Installationsordner mitsenden."
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

def breakIfDebuggerAttached():
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        breakpoint()

def qt_message_handler(mode, context, message):
    message = "%s (%s:%d, %s)" % (message, context.file, context.line, context.file)
    if mode == QtCore.QtMsgType.QtInfoMsg:
        logging.info(message)
    elif mode == QtCore.QtMsgType.QtWarningMsg:
        if "qtwebengine_locales" in message:
            # we can ignore this warning, we deleted the locales on purpose to save space
            return

        if "crbug/1173575" in message:
            # we can ignore this warning, apparently it is thrown for no good reason when there is no internet connection
            return

        if "Path override failed for key base::DIR_APP_DICTIONARIES" in message:
            # linux apparently doesnt like that we delete some chromium resource files that we dont actually need
            return

        logging.warning(message)
        breakIfDebuggerAttached()
    elif mode == QtCore.QtMsgType.QtCriticalMsg:
        if "Content Security Policy" in message:
            # many websites violate their own CSP - chromium applies it as configured though, no need to log this
            return
        logging.error(message)
        breakIfDebuggerAttached()
    elif mode == QtCore.QtMsgType.QtFatalMsg:
        logging.critical(message)
        breakIfDebuggerAttached()
    else:
        logging.debug(message)

class MainWindowWrapper(object):
    '''
    Main Class responsible for running the entire application. 
    Just shows three buttons and handles the execution of the individual subparts.
    '''

    def __init__(self):
        # Set current directory so we can use relative paths
        # There are many test cases, i.e. starting from VS, from a different folder, with python, directly Sephrasto.py via shebang, built exe etc. and much can go wrong
        # We need to remember the old current dir for restarting purposes via settings  - again things can go wrong otherwise
        # Also on windows there is a weird issue when starting Sephrasto.exe from a different folder, so we use sys.argv[0] as a fallback (which doesnt work in other cases -.-)
        EinstellungenWrapper.oldWorkingDir = os.getcwd() 
        if os.path.isfile(os.path.abspath(__file__)):
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
        else:
            os.chdir(os.path.dirname(sys.argv[0]) or ".")

        # Setup logger (after chdir so file is created in the correct location)
        logging.basicConfig(filename="sephrasto.log", \
            level=loglevels[Wolke.Settings['Logging']], \
            format="%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s(%(lineno)d) | %(message)s")

        # Log and check version
        logging.critical("Starte Sephrasto " + Version.clientToString() + " auf " + platform.system()) #critical so it's always printed, independent of the debug level setting
        logging.critical(f"Python {platform.python_version()}, Qt {QtCore.qVersion()}, PySide {PySide6.__version__} (compiled with Qt {QtCore.__version__})") #for people that start from source

        pythonMinVersion = "3.9.0"
        if Version.isLower(Version.fromString(pythonMinVersion), Version.fromString(platform.python_version())):
            print("Fehler: Sephrasto benötigt mindestens Python " + pythonMinVersion)
            logging.critical("Sephrasto benötigt mindestens Python " + pythonMinVersion)
            sys.exit(1)
            return

        pysideMinVersion = "6.7.0"
        if Version.isLower(Version.fromString(pysideMinVersion), Version.fromString(PySide6.__version__)):
            print("Fehler: Sephrasto benötigt mindestens PySide " + pysideMinVersion)
            logging.critical("Sephrasto benötigt mindestens PySide " + pysideMinVersion)
            sys.exit(1)
            return

        # Parse commandline arguments
        # on a built windows exe stdout is not available, we need to redirect the output
        # to a dummy stream so it doesnt crash when something like argparse tries to use it
        if not hasattr(sys.stdout, "write"):
            class DummyStream:
                def __init__(self): pass
                def write(self,data): pass
                def read(self,data): pass
                def flush(self): pass
                def close(self): pass
            sys.stdout = DummyStream()
            sys.stderr = DummyStream()
            sys.stdin = DummyStream()
            sys.__stdout__ = DummyStream()
            sys.__stderr__ = DummyStream()
            sys.__stdin__ = DummyStream()

        parser = argparse.ArgumentParser(prog='Sephrasto', description='Der Charaktergenerator für Ilaris')
        parser.add_argument('--settingsfile', required = False, help='Requires a path to an .ini file. If it doesnt exist it will be created. Overrides the default location of the settings file')
        parser.add_argument('--noplugins', required = False, action='store_true', help='With this option no plugins are loaded, even if they are enabled in the settings')
        parser.add_argument('--debug', required = False, action='store_true', help='This option will forward log messages to the console and enable further debug features')
        parser.add_argument('--loglevel', required = False, type=int, choices=[0,1,2], help='Sets the loglevel (0 = error, 1 = warning, 2 = debug). This overrides the loglevel configured in setting file.')
        parser.add_argument('--migrate', required = False, help='Requires a path to a character xml file. Loads and then saves the character, applying any migration without UI interaction. Please make a backup, any loading warnings will be ignored.')
        parser.add_argument('--prerelease-plugins', required = False, action='store_true', help='Instructs the Pluginmanager to download the latest prerelease plugins if available.')
        Wolke.CmdArgs = parser.parse_args()

        if Wolke.CmdArgs.debug:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        # Setup crash and error handler
        sys.excepthook = sephrasto_excepthook
        QtCore.qInstallMessageHandler(qt_message_handler)

        '''
        Initializes the GUI and connects the buttons.
        '''


        super().__init__()

        # Get the Settings loaded
        EinstellungenWrapper.loadPreQt()
        if Wolke.CmdArgs.loglevel is not None:
            logging.getLogger().setLevel(loglevels[Wolke.CmdArgs.loglevel])
        else:
            logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])

        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1" if Wolke.Settings['DPI-Skalierung'] else "0"
        if Wolke.Settings['DPI-Skalierung']:
            os.environ.pop("QT_FONT_DPI", None)
        else:
            os.environ["QT_FONT_DPI"] = "96"

        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)

        # Install translator. We dont have our own translation resource but we can load 
        # the german resource that qt provides i.e. for default-button and shortcut translations
        translator = QtCore.QTranslator(self.app)
        if translator.load(QLocale(QLocale.German, QLocale.Germany), 'qtbase', '_', QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.TranslationsPath)):
            self.app.installTranslator(translator)
        else:
            logging.warning("Failed to load translation resource.")

        EinstellungenWrapper.loadPostQt()

        # Query system font and font size for settings dialog restore option
        defaultFont = QtGui.QFont()
        Wolke.DefaultOSFont = defaultFont.family()
        if not Wolke.Settings['Font']:
            Wolke.Settings['Font'] = Wolke.DefaultOSFont

        fontSize = defaultFont.pointSize()
        if fontSize != -1:
            Wolke.DefaultOSFontSize = fontSize
            if Wolke.Settings['FontSize'] == 0:
                Wolke.Settings['FontSize'] = Wolke.DefaultOSFontSize
                Wolke.Settings['FontHeadingSize'] = Wolke.DefaultOSFontSize -1

        self.form = QtWidgets.QWidget()
        self.ui = UI.MainWindow.Ui_Form()
        self.ui.setupUi(self.form)
        self.ui.labelVersion.setText(Version.clientToString() + " - by Aeolitus & Gatsu")
        self.app.setWindowIcon(QtGui.QIcon('icon_large.png'))

        windowSize = Wolke.Settings["WindowSize-Main"]
        self.form.resize(windowSize[0], windowSize[1])

        self.updateAppearance()

        self.ui.buttonRules.setText("\uf1c0")
        self.ui.buttonRules.clicked.connect(self.editRuleset)

        self.ui.buttonSettings.setText("\uf013")
        self.ui.buttonSettings.clicked.connect(self.editSettings)

        self.ui.buttonHelp.setText("\uf059")
        self.ui.buttonHelp.clicked.connect(self.help)

        # Load Background image and make sure it resizes dynamically
        self.background = QtGui.QPixmap("Data/Images/background.png")
        self.form.paintEvent = self.paintEvent

        # Glow effect for sephrasto label
        self.glow = QtWidgets.QGraphicsDropShadowEffect()
        self.glow.setBlurRadius(10)
        self.glow.setXOffset(0)
        self.glow.setYOffset(0)
        self.glow.setColor(QColor("#ffffff"))
        self.ui.label.setGraphicsEffect(self.glow)

        # Init recent characters list (including new and load buttons)
        self.charakterListe = CharakterListe(Wolke.Settings['CharListCols'], Wolke.Settings['CharListRows'])
        self.charakterListe.load.connect(self.editExisting)
        self.charakterListe.createNew.connect(self.createNew)
        self.charakterListe.remove.connect(self.remove)
        self.ui.scrollArea.setWidget(self.charakterListe)

        # Check for updates
        UpdateChecker.checkForUpdate()

        # Load plugins and add buttons (if any)
        buttons = [self.ui.buttonRules]
        self._plugins = []

        if not Wolke.CmdArgs.noplugins:
            for pluginData in PluginLoader.getPlugins(Wolke.Settings['Pfad-Plugins']):
                if not pluginData.loadable:
                    self._plugins.append(pluginData)
                    continue

                if pluginData.load():
                    self._plugins.append(pluginData)
                    logging.critical("Plugin: loaded " + pluginData.name)
                    if hasattr(pluginData.plugin, "createMainWindowButtons"):
                        for button in pluginData.plugin.createMainWindowButtons():
                            button.setParent(self.form)
                            self.ui.horizontalLayout.insertWidget(0, button)
                            buttons.append(button)
                else:
                    messagebox = QtWidgets.QMessageBox()
                    messagebox.setWindowTitle("Fehler!")
                    messagebox.setText(f"Das Laden des Plugins {pluginData.name} ist fehlgeschlagen.\nEs ist vermutlich nicht mit dieser Sephrastoversion kompatibel, bitte wende dich an den Plugin-Autor.")
                    messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    messagebox.exec()

        self.dbEditor = None

        loadedPlugins = [p.name for p in self._plugins if p.isLoaded()]
        EventBus.doAction("plugins_geladen", { "plugins" : loadedPlugins})

        if Wolke.CmdArgs.migrate is not None:
            self.migrateCharacter(Wolke.CmdArgs.migrate)
            sys.exit(0)
            return

        EventBus.addAction("charaktereditor_reload", self.charakterEditorReloadHook)
        EventBus.addAction("charaktereditor_modified", self.charakterEditorModifiedHook)

        self.updateRecents()
        self.form.show()
        exitcode = self.app.exec()
        Wolke.Settings["WindowSize-Main"] = [self.form.size().width(), self.form.size().height()]
        EinstellungenWrapper.save()

        sys.exit(exitcode)

    def migrateCharacter(self, path):
        if not os.path.isfile(path):
            print("Path is not a file.")
            return
        storedHausregeln = Charakter.Char.hausregelnLesen(path)
        availableHausregeln = EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"])
        if storedHausregeln not in availableHausregeln:
            print(f"Character requires a houserule database that is unavailable in the rules path ({storedHausregeln}).")
            return
        Wolke.DB = Datenbank.Datenbank()
        if not Wolke.DB.loadFile(hausregeln = storedHausregeln, isCharakterEditor = True):
            print("Failed to load database.")
            return

        char = Charakter.Char()
        success, result = char.loadFile(path)
        if result[0] != Charakter.Char.LoadResultNone:
            print(result[1])
            print(result[2])
        if not success:
            return
        char.aktualisieren() #plugins listening to "serialize" might depend on this
        char.saveFile(path)
        print("Character saved.")

    def updateRecents(self):
        self.charakterListe.update(Wolke.Settings['Letzte-Chars'])
        self.ui.scrollArea.setFixedWidth(self.charakterListe.totalWidth)
        self.ui.scrollArea.setMaximumHeight(self.charakterListe.totalHeight)

    def paintEvent(self, pe):
        painter = QtGui.QPainter(self.form)
        winSize = self.form.size()
        pixmapRatio = self.background.width() / self.background.height()
        windowRatio = winSize.width() / winSize.height()

        if pixmapRatio > windowRatio:
          newWidth = winSize.height() * pixmapRatio
          offset = (newWidth - winSize.width()) / -2
          painter.drawPixmap(offset, 0, newWidth, winSize.height(), self.background)
        else:
          newHeight = winSize.width() / windowRatio
          newWidth = newHeight * pixmapRatio      
          offsetW = (newWidth - winSize.width()) / -2
          offsetH = (newHeight - winSize.height()) / -2
          painter.drawPixmap(offsetW, offsetH, newWidth, newHeight, self.background)

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
        wizardConfig = None
        if Wolke.Settings['Charakter-Assistent']:
            wizardEd = WizardWrapper.WizardWrapper()
            result = wizardEd.form.exec()
            if result == QtWidgets.QDialog.Accepted:
                wizardConfig = wizardEd.config
            wizardEd.form.hide()
            wizardEd.form.deleteLater()
            if result != QtWidgets.QDialog.Accepted:
                return

        EventBus.doAction("charaktereditor_oeffnet", { "neu" : True, "filepath" : "" })
        self.form.hide()
        self.ed = CharakterEditor.Editor(self._plugins, self.charakterEditorClosedHandler, self.savePathUpdated)
        if wizardConfig is None:
            self.ed.newCharacter()
        else:
            self.ed.newCharacterFromWizard(wizardConfig)

        self.savePathUpdated()        
        EventBus.doAction("charaktereditor_geoeffnet", { "neu" : True, "filepath" : "" })
        
    def editExisting(self, spath = ""):
        '''
        Creates a CharakterEditor for an existing character and shows it.
        '''
        if spath == "":
            if os.path.isdir(Wolke.Settings['Pfad-Chars']):
                startDir = Wolke.Settings['Pfad-Chars']
            else:
                startDir = ""
            spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Charakter laden...",startDir,"XML-Datei (*.xml)")
        if spath == "":
            return
        if not spath.endswith(".xml"):
            spath = spath + ".xml"

        if not os.path.isfile(spath):
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Datei existiert nicht")
            messagebox.setText(f"Der Charakter kann nicht geladen werden, da die Datei {spath} nicht mehr existiert. Hast du sie verschoben oder umbenannt?")
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec()
            return

        EventBus.doAction("charaktereditor_oeffnet", { "neu" : False, "filepath" : spath })
        self.form.hide()
        self.ed = CharakterEditor.Editor(self._plugins, self.charakterEditorClosedHandler, self.savePathUpdated)
        self.ed.loadCharacter(spath)
        self.savePathUpdated()
        EventBus.doAction("charaktereditor_geoeffnet", { "neu" : False, "filepath" : spath })

    def remove(self, path):
        for char in Wolke.Settings['Letzte-Chars']:
            if char["path"] != path:
                continue

            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle("Charakter entfernen")
            messageBox.setIcon(QtWidgets.QMessageBox.Question)
            messageBox.setText("Möchtest du den Charakter nur aus der Liste enfernen oder permanent löschen?")
            removeList = messageBox.addButton("Aus Liste entfernen", QtWidgets.QMessageBox.AcceptRole)
            delete = messageBox.addButton("Löschen", QtWidgets.QMessageBox.AcceptRole)
            cancel = messageBox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            messageBox.setDefaultButton(removeList)
            messageBox.exec()
            if messageBox.clickedButton() == removeList:
                Wolke.Settings['Letzte-Chars'].remove(char)
                self.updateRecents()
            elif messageBox.clickedButton() == delete:
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle("Charakter enfernen")
                messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                messageBox.setText("Der Charakter wird permanent gelöscht. Fortfahren?")
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
                result = messageBox.exec()
                if result == QtWidgets.QMessageBox.Yes:
                    os.remove(char["path"])
                    Wolke.Settings['Letzte-Chars'].remove(char)
                    self.updateRecents()
            break

    def charakterEditorClosedHandler(self):
        EventBus.doAction("charaktereditor_geschlossen")
        self.ed.form.deleteLater()
        del self.ed
        self.ed = None
        self.updateRecents()
        self.form.show()

    def editRuleset(self):
        '''
        Creates the DatenbankEdit Form and shows the contents of datenbank.xml.
        '''
        if self.dbEditor is not None:
            self.dbEditor.form.show()
            self.dbEditor.form.activateWindow()
            return
        self.form.hide()
        self.dbEditor = DatenbankEditor.DatenbankEditor(self._plugins, self.dbeClosedHandler)
        self.dbEditor.form = QtWidgets.QMainWindow()
        self.dbEditor.ui = UI.DatenbankMain.Ui_Form()
        self.dbEditor.ui.setupUi(self.dbEditor.form)
        self.dbEditor.setupGUI()
        self.dbEditor.form.show()

    def dbeClosedHandler(self):
        self.dbEditor.form.deleteLater()
        del self.dbEditor
        self.dbEditor = None
        self.form.show()
        
    def editSettings(self):
        EinstellungenWrapper(self._plugins)

    def help(self):
        if not hasattr(self, "hilfe"):
            self.hilfe = WebEngineWrapper("Hilfe", "./Doc/index.html", Wolke.MkDocsCSS, "WindowSize-Hilfe")
            self.hilfe.form.show()
        else:
            self.hilfe.form.show()
            self.hilfe.form.activateWindow()

    def savePathUpdated(self):
        file = " - Neuer Charakter"
        if self.ed.savepath:
            file = " - " + os.path.basename(self.ed.savepath)
        rules = ""
        if Wolke.DB.hausregelDatei:
           rules = " (" + os.path.splitext(os.path.basename(Wolke.DB.hausregelDatei))[0] + ")"
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
            
            if "ForceColorScheme" in theme:
                self.app.styleHints().setColorScheme(getattr(QtCore.Qt.ColorScheme, theme["ForceColorScheme"]))

            # Set style, i.e. fusion
            self.app.setStyle(theme["Style"])
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
            Wolke.HeadingColor = theme["HeadingColor"] if "HeadingColor" in theme else palette.text().color().name()
            Wolke.BorderColor = theme["BorderColor"] if "BorderColor" in theme else palette.mid().color().name()
            Wolke.ReadonlyColor = theme["ReadonlyColor"] if "ReadonlyColor" in theme else palette.color(QPalette.Disabled, QPalette.Base).name()
            
            if "ValidColor" in theme:
                Wolke.ValidColor = theme["ValidColor"]
            if "WarningColor" in theme:
                Wolke.WarningColor = theme["WarningColor"]
            if "ErrorColor" in theme:
                Wolke.ErrorColor = theme["ErrorColor"]
            if "ModifiedColor" in theme:
                Wolke.ModifiedColor = theme["ModifiedColor"]
            if "CodeKeywordColor" in theme:
                Wolke.CodeKeywordColor = theme["CodeKeywordColor"]
            if "CodeOperatorsBracesColor" in theme:
                Wolke.CodeOperatorsBracesColor = theme["CodeOperatorsBracesColor"]
            if "CodeDeclarationColor" in theme:
                Wolke.CodeDeclarationColor = theme["CodeDeclarationColor"]
            if "CodeStringColor" in theme:
                Wolke.CodeStringColor = theme["CodeStringColor"]
            if "CodeCommentColor" in theme:
                Wolke.CodeCommentColor = theme["CodeCommentColor"]
            if "CodeNumberColor" in theme:
                Wolke.CodeNumberColor = theme["CodeNumberColor"]
            if "CodeBackgroundColor" in theme:
                Wolke.CodeBackgroundColor = theme["CodeBackgroundColor"]   
        else:
            theme = ''
            palette = QPalette()
            
        # Create stylesheet
        standardFont = f"font-family: '{Wolke.Settings['Font']}'"
        headingFont = f"font-family: '{Wolke.Settings['FontHeading']}'; color: {Wolke.HeadingColor}"
        Wolke.FontAwesomeCSS = f"font-size: {Wolke.Settings['FontSize']}pt; font-family: \"Font Awesome 6 Free Solid\"; font-weight: 900;"
        Wolke.FontAwesomeRegularCSS = f"font-size: {Wolke.Settings['FontSize']}pt; font-family: \"Font Awesome 6 Free Regular\"; font-weight: 400;"
        Wolke.FontAwesomeFont = QtGui.QFont("Font Awesome 6 Free Solid", Wolke.Settings['FontSize'], QtGui.QFont.Black)
        Wolke.FontAwesomeFont.setHintingPreference(QtGui.QFont.PreferNoHinting)
        Wolke.FontAwesomeRegularFont = QtGui.QFont("Font Awesome 6 Free Regular", Wolke.Settings['FontSize'], QtGui.QFont.Normal)
        Wolke.FontAwesomeRegularFont.setHintingPreference(QtGui.QFont.PreferNoHinting)
        css = f"""*[readOnly=\"true\"] {{ background-color: {Wolke.ReadonlyColor}; border: none; }}
QWidget, QToolTip {{ {standardFont}; font-size: {Wolke.Settings['FontSize']}pt; }}
QWidget[valid=true] {{ border: 2px solid {Wolke.ValidColor}; border-radius: 2px; padding: 1px;}}
QWidget[warning=true] {{ border: 2px solid {Wolke.WarningColor}; border-radius: 2px; padding: 1px;}}
QWidget[error=true] {{ border: 2px solid {Wolke.ErrorColor}; border-radius: 2px; padding: 1px;}}
QHeaderView::section {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']-1}pt; {headingFont}; }}
QListView::item {{ margin-top: 0.3em; margin-bottom: 0.3em; }}
QTreeView::item {{ margin-top: 0.3em; margin-bottom: 0.3em; }}
QLineEdit {{color: {palette.text().color().name()};}} /* for some reason the color isnt applied to the placeholder text otherwise */
QCheckBox::indicator {{ width: {Hilfsmethoden.emToPixels(1.9)}px; height: {Hilfsmethoden.emToPixels(1.9)}px; }} /* doesnt work for tree/list - setting it via ::indicator breaks text offsets*/
.smallText {{ font-size: {Wolke.Settings['FontSize']-1}pt; }}
.smallTextBright {{ font-size: {Wolke.Settings['FontSize']-1}pt; color: #ffffff }}
.italic {{ font-style: italic; }}
.h1 {{ font-weight: bold; font-size: {Wolke.FontHeadingSizeL1}pt; {headingFont}; }}
.h2 {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']}pt; {headingFont}; }}
.h3, QGroupBox {{ font-weight: bold; font-variant: small-caps; font-size: {Wolke.FontHeadingSizeL3}pt; {standardFont}; color: {Wolke.HeadingColor}; }}
.h4 {{ font-weight: bold; }}
.title {{ font-weight: bold; font-size: 16pt; {headingFont}; color: #ffffff }}
.subtitle {{ font-size: 10pt; color: #ffffff }}
.icon {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(3.2)}px; max-height: {Hilfsmethoden.emToPixels(3.2)}px;}}
.iconRegular {{ {Wolke.FontAwesomeRegularCSS} max-width: {Hilfsmethoden.emToPixels(3.2)}px; max-height: {Hilfsmethoden.emToPixels(3.2)}px;}}
.iconSmall {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(2.3)}px; max-height: {Hilfsmethoden.emToPixels(2.3)}px;}}
.iconTiny {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(1.5)}px; max-height: {Hilfsmethoden.emToPixels(1.5)}px;}}
.iconTopDownArrow {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(2.3)}px; max-height: {Hilfsmethoden.emToPixels(1.2)}px;}}
.alternateBase {{ background-color: {palette.alternateBase().color().name()}; }}
.noBorder {{ border: none; }}
.transparent {{ background-color: transparent; }}
.transparent > QWidget > QWidget {{ background-color: transparent; }}
.transparent > QWidget > QScrollBar {{ background: 1; }}
.tabNavigation > QTabBar, .tabmain > QTabBar::tab {{ font-weight: bold; font-size: {Wolke.FontHeadingSizeL1}pt; {headingFont};}}
.tabSubnavigation > QTabBar, .tabmain > QTabBar::tab {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']}pt; {headingFont};}}
.treeVorteile::item {{ margin: 0.1em; }}
.monospace {{ font-family: Consolas,'Lucida Console','Liberation Mono','DejaVu Sans Mono','Bitstream Vera Sans Mono','Courier New',monospace,sans-serif; }}
.codeEditor {{ background: {Wolke.CodeBackgroundColor}; }}
.weaponsBorderTop {{ border-left: 1px solid {Wolke.BorderColor}; border-right: 1px solid {Wolke.BorderColor}; border-top: 1px solid {Wolke.BorderColor}; border-top-left-radius : 0px; border-top-right-radius : 0px; }}
.weaponsBorderBottom {{ border-left: 1px solid {Wolke.BorderColor}; border-right: 1px solid {Wolke.BorderColor}; border-bottom: 1px solid {Wolke.BorderColor}; border-bottom-left-radius : 0px; border-bottom-right-radius : 0px; }}
.weaponsBorderLeft {{ border-left: 1px solid {Wolke.BorderColor}; border-top-left-radius : 0px; }}
.weaponsBorderRight {{ border-right: 1px solid {Wolke.BorderColor}; border-top-right-radius : 0px; }}
.charListScrollArea {{ background-color:#44444444; border: none; }}
.charWidget {{ border-image: url(Data/Images/recents_background.png) 0 0 0 0 stretch stretch; }}
.charWidget:hover {{ border-image: url(Data/Images/recents_background_hovered.png) 0 0 0 0 stretch stretch; }}
.charWidget[pressed="true"] {{ border-image: url(Data/Images/recents_background_pressed.png) 0 0 0 0 stretch stretch; }}
.charWidgetLabel {{ color: #000000; }}
.charWidgetIcon {{ {Wolke.FontAwesomeCSS} font-size: 14pt; color: #ffffff; background: #44444444; }}
\n"""

        if 'CSS' in theme:
            css += theme['CSS']
        self.app.setStyleSheet(css)

        sephrasto_dir = "file:///" + os.getcwd().replace('\\', '/')
        Wolke.MkDocsCSS = f"""
@font-face {{
	font-family: 'Aniron';
	src: url('{sephrasto_dir}/Data/Fonts/Aniron/anirb___.ttf') format('truetype');
}}

@font-face {{
	font-family: 'Crimson Pro';
	src: url('{sephrasto_dir}/Data/Fonts/Crimson Pro/CrimsonPro-Regular.ttf') format('truetype');
	font-style: normal;
	font-weight: 400;
}}

@font-face {{
	font-family: 'Crimson Pro';
	src: url('{sephrasto_dir}/Data/Fonts/Crimson Pro/CrimsonPro-Italic.ttf') format('truetype');
	font-style: italic;
	font-weight: 400;
}}

@font-face {{
	font-family: 'Crimson Pro';
	src: url('{sephrasto_dir}/Data/Fonts/Crimson Pro/CrimsonPro-Bold.ttf') format('truetype');
	font-weight: 700;
}}

html {{
    /* This undoes the invisibility set in docs/stylesheets/extra.css 
       Sephrastos css is set late which causes flickering otherwise. */
    visibility: visible;
    opacity: 1;
}}

body {{
    /* Set background and font colors to Sephrasto theme */
    --md-default-bg-color: {palette.color(QPalette.Base).name()} !important;
    --md-default-bg-color--light: {palette.color(QPalette.Window).name()} !important;

    --md-default-fg-color: {palette.color(QPalette.Text).name()} !important;
    --md-default-fg-color--light: {palette.color(QPalette.BrightText).name()} !important;
    --md-default-fg-color--lightest: {palette.color(QPalette.BrightText).name()} !important;
    --md-default-fg-color--dark: {palette.color(QPalette.Text).name()} !important;

    /* The following classes are used for code. By default they use the default font color instead of code color, probably a bug.
       That causes some characters to by invisible in dark mode, so we set them to the code color instead. */
    --md-code-hl-operator-color: var(--md-code-fg-color) !important;
    --md-code-hl-punctuation-color: var(--md-code-fg-color) !important;
    --md-code-hl-comment-color: var(--md-code-fg-color) !important;
    --md-code-hl-generic-color: var(--md-code-fg-color) !important;
    --md-code-hl-variable-color: var(--md-code-fg-color) !important;

    --md-text-font: "{Wolke.Settings['Font']}" !important;
}}

.md-typeset h1 {{ font-weight: bold; font-size: {Wolke.FontHeadingSizeL1}pt; {headingFont}; }}
.md-header__title, .md-nav__title {{ font-weight: bold; font-size: {Wolke.FontHeadingSizeL1}pt; font-family: '{Wolke.Settings['FontHeading']}'; }}
.md-typeset h2 {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']}pt; {headingFont}; }}
.md-typeset h3 {{ font-weight: bold; font-variant: small-caps; font-size: {Wolke.FontHeadingSizeL3}pt; {standardFont}; color: {Wolke.HeadingColor}; }}
.md-typeset h4 {{ font-weight: bold; }}
"""
        
if __name__ == "__main__":
    itm = MainWindowWrapper()