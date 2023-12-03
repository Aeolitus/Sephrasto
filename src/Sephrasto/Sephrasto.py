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
from CharakterListe import CharakterListe
from CharakterAssistent import WizardWrapper
import argparse

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
    exception = '%s: %s' %(exc_type.__name__, exc_value)
    logging.critical(exception + "\n".join(traceback))

    #Try to show message box, hopefully its not a crash in Qt
    text = exception + "\nBei Fragen zum diesem Fehler bitte sephrasto.log aus dem Installationsordner mitsenden."
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
        parser = argparse.ArgumentParser(prog='Sephrasto', description='Der Charaktergenerator für Ilaris')
        parser.add_argument('--settingsfile', required = False, help='Overrides the default location of the settings file')
        parser.add_argument('--noplugins', required = False, action='store_true', help='With this option no plugins are loaded, even if they are enabled in the settings')
        parser.add_argument('--debug', required = False, action='store_true', help='This option will forward log messages to the console and enable further debug features')
        parser.add_argument('--loglevel', required = False, type=int, choices=[0,1,2], help='Sets the loglevel (0 = error, 1 = warning, 2 = debug). This overrides the loglevel configured in setting file.')
        Wolke.CmdArgs = parser.parse_args()

        if Wolke.CmdArgs.debug:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        sys.excepthook = sephrasto_excepthook
        QtCore.qInstallMessageHandler(qt_message_handler)

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
        EinstellungenWrapper.loadPreQt()
        if Wolke.CmdArgs.loglevel is not None:
            logging.getLogger().setLevel(loglevels[Wolke.CmdArgs.loglevel])
        else:
            logging.getLogger().setLevel(loglevels[Wolke.Settings['Logging']])

        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1" if Wolke.Settings['DPI-Skalierung'] else "0"

        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)

        EinstellungenWrapper.loadPostQt()

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
                Wolke.Settings['FontHeadingSize'] = Wolke.DefaultOSFontSize -1

        self.form = QtWidgets.QWidget()
        self.ui = UI.MainWindow.Ui_Form()
        self.ui.setupUi(self.form)
        self.ui.labelVersion.setText(self._version_ + " - by Aeolitus & Gatsu")
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
        self.ui.scrollArea.setWidget(self.charakterListe)

        # Check for updates
        UpdateChecker.checkForUpdate()

        # Load plugins and add buttons (if any)
        buttons = [self.ui.buttonRules]
        self._plugins = []

        if not Wolke.CmdArgs.noplugins:
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

        EventBus.addAction("charaktereditor_reload", self.charakterEditorReloadHook)
        EventBus.addAction("charaktereditor_modified", self.charakterEditorModifiedHook)

        self.updateRecents()
        self.form.show()
        exitcode = self.app.exec()
        Wolke.Settings["WindowSize-Main"] = [self.form.size().width(), self.form.size().height()]
        EinstellungenWrapper.save()

        sys.exit(exitcode)

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

    def charakterEditorClosedHandler(self):
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
            self.hilfe = HilfeWrapper()
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
        palette = self.app.style().standardPalette()
        themeName = Wolke.Settings['Theme']
        if themeName in Wolke.Themes:
            theme = Wolke.Themes[themeName]

            # Set style, i.e. fusion
            self.app.setStyle(theme["Style"])

            # Set color palette
            if "StandardPalette" not in theme or not theme["StandardPalette"]:
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
        Wolke.FontAwesomeCSS = f"font-size: {Wolke.Settings['FontSize']}pt; font-family: \"Font Awesome 6 Free Solid\"; font-weight: 900;"
        Wolke.FontAwesomeFont = QtGui.QFont("Font Awesome 6 Free Solid", Wolke.Settings['FontSize'], QtGui.QFont.Black)
        Wolke.FontAwesomeRegularFont = QtGui.QFont("Font Awesome 6 Free Regular", Wolke.Settings['FontSize'], QtGui.QFont.Normal)
        css = f"""*[readOnly=\"true\"] {{ background-color: {Wolke.ReadonlyColor}; border: none; }}
QWidget, QToolTip {{ {standardFont}; font-size: {Wolke.Settings['FontSize']}pt; }}
QHeaderView::section {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']-1}pt; {headingFont}; }}
QListView::item {{ margin-top: 0.3em; margin-bottom: 0.3em; }}
QTreeView::item {{ margin-top: 0.3em; margin-bottom: 0.3em; }}
.treeVorteile::item {{ margin: 0.1em; }}
QLineEdit {{color: {palette.text().color().name()};}} /* for some reason the color isnt applied to the palceholder text otherwise */
QCheckBox::indicator {{ width: {Hilfsmethoden.emToPixels(1.9)}px; height: {Hilfsmethoden.emToPixels(1.9)}px; }} /* doesnt work for tree/list - setting it via ::indicator breaks text offsets*/
.smallText {{ font-size: {Wolke.Settings['FontSize']-1}pt; }}
.smallTextBright {{ font-size: {Wolke.Settings['FontSize']-1}pt; color: #ffffff }}
.italic {{ font-style: italic; }}
.panel {{ background: {Wolke.PanelColor}; }}
.h1 {{ font-weight: bold; font-size: {Wolke.FontHeadingSizeL1}pt; {headingFont}; }}
.h2 {{ font-weight: bold; font-size: {Wolke.Settings['FontHeadingSize']}pt; {headingFont}; }}
.h3, QGroupBox {{ font-weight: bold; font-variant: small-caps; font-size: {Wolke.FontHeadingSizeL3}pt; {standardFont}; color: {Wolke.HeadingColor}; }}
.h4 {{ font-weight: bold; }}
.title {{ font-weight: bold; font-size: 16pt; {headingFont}; color: #ffffff }}
.subtitle {{ font-size: 10pt; color: #ffffff }}
.icon {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(3.2)}px; max-height: {Hilfsmethoden.emToPixels(3.2)}px;}}
.iconSmall {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(2.3)}px; max-height: {Hilfsmethoden.emToPixels(2.3)}px;}}
.iconTiny {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(1.5)}px; max-height: {Hilfsmethoden.emToPixels(1.5)}px;}}
.iconTopDownArrow {{ {Wolke.FontAwesomeCSS} max-width: {Hilfsmethoden.emToPixels(2.3)}px; max-height: {Hilfsmethoden.emToPixels(1.2)}px;}}
.charListScrollArea {{ background-color:#44444444; }}
.charWidget {{ border-image: url(Data/Images/recents_background.png) 0 0 0 0 stretch stretch; }}
.charWidget:hover {{ border-image: url(Data/Images/recents_background_hovered.png) 0 0 0 0 stretch stretch; }}
.charWidget[pressed="true"] {{ border-image: url(Data/Images/recents_background_pressed.png) 0 0 0 0 stretch stretch; }}
.charWidgetLabel {{ color: #000000; }}
.charWidgetIcon {{ {Wolke.FontAwesomeCSS} font-size: 14pt; color: #ffffff; background: #44444444; }}
\n"""

        if 'CSS' in theme:
            css += theme['CSS']
        self.app.setStyleSheet(css)
        
if __name__ == "__main__":
    itm = MainWindowWrapper()