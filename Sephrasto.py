#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:30:34 2017

@author: Aeolitus
"""
import logging
import os
import os.path
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import CharakterEditor
import CharakterMain
import DatenbankEdit
import DatenbankMain
import MainWindow
import Version
from EinstellungenWrapper import EinstellungenWrapper
from EventBus import EventBus
from PluginLoader import PluginLoader
from Wolke import Wolke

loglevels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.DEBUG}
logging.basicConfig(
    filename="sephrasto.log",
    level=loglevels[Wolke.Settings["Logging"]],
    format="%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s(%(lineno)d) | %(message)s",
)


def sephrasto_excepthook(exc_type, exc_value, tb):
    traceback = [" Traceback (most recent call last):"]
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        traceback.append(
            '   File "%.500s", line %d, in %.500s' % (filename, lineno, name)
        )
        tb = tb.tb_next

    # Exception type and value
    exception = " %s: %s" % (exc_type.__name__, exc_value)
    logging.critical(exception + "\n".join(traceback))

    # Try to show message box, hopefully its not a crash in Qt
    messagebox = QtWidgets.QMessageBox()
    messagebox.setWindowTitle("Fehler!")
    messagebox.setText(
        "Unerwarteter Fehler:"
        + exception
        + ". Bei Fragen zum diesem Fehler bitte sephrasto.log mitsenden."
    )
    messagebox.setIcon(QtWidgets.QMessageBox.Critical)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    messagebox.exec_()


class MainWindowWrapper(object):
    """
    Main Class responsible for running the entire application.
    Just shows three buttons and handles the execution of the individual subparts.
    """

    def __init__(self):
        sys.excepthook = sephrasto_excepthook

        """
        Initializes the GUI and connects the buttons.
        """
        self._version_ = (
            "v"
            + str(Version._sephrasto_version_major)
            + "."
            + str(Version._sephrasto_version_minor)
            + "."
            + str(Version._sephrasto_version_build)
        )
        logging.critical(
            "Starte Sephrasto " + self._version_
        )  # critical so it's always printed, independent of the debug level setting

        super().__init__()

        # Make sure the application scales properly, i.e. in Win10 users can change the UI scale in the display settings
        if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        # self.app.setStyleSheet("*[readOnly=\"true\"] { background-color: #F5F5F5 } QAbstractScrollArea #scrollAreaWidgetContents { background-color: #FFFFFF }")
        self.app.setStyleSheet(
            """
        *[readOnly=\"true\"]
        {
            background-color: #FFFFFF;
            border: none
        }
        QAbstractScrollArea #scrollAreaWidgetContents
        {
            background-color: #FFFFFF
        }
        """
        )
        self.Form = QtWidgets.QWidget()
        self.ui = MainWindow.Ui_Form()
        self.ui.setupUi(self.Form)
        self.ui.buttonNew.clicked.connect(self.createNew)
        self.ui.buttonEdit.clicked.connect(self.editExisting)
        self.ui.buttonRules.clicked.connect(self.editRuleset)
        self.ui.buttonSettings.clicked.connect(self.editSettings)
        self.ui.labelVersion.setText(self._version_ + " - by Aeolitus ")

        self.app.setWindowIcon(QtGui.QIcon("icon_large.png"))

        # Get the Settings loaded
        EinstellungenWrapper.load()
        logging.getLogger().setLevel(loglevels[Wolke.Settings["Logging"]])

        self._plugins = []
        pluginPaths = ["Plugins", Wolke.Settings["Pfad-Plugins"]]

        for pluginPath in pluginPaths:
            pluginNames = PluginLoader.getPlugins(pluginPath)

            for pluginName in pluginNames:
                if pluginName in Wolke.Settings["Deaktivierte-Plugins"]:
                    continue
                plugin = PluginLoader.loadPlugin(pluginPath, pluginName)
                self._plugins.append(plugin)
                logging.info("Plugin: loaded " + pluginName)
                if hasattr(plugin, "createMainWindowButtons"):
                    for button in plugin.createMainWindowButtons():
                        button.setParent(self.Form)
                        button.setMinimumSize(QtCore.QSize(0, 25))
                        self.ui.vlPluginButtons.addWidget(button)

        EventBus.doAction("plugins_geladen")

        EventBus.addAction("charaktereditor_reload", self.charakterEditorReloadHook)
        EventBus.addAction("charaktereditor_modified", self.charakterEditorModifiedHook)

        self.Form.show()
        sys.exit(self.app.exec_())

    def charakterEditorReloadHook(self, params):
        if self.ed and not self.ed.formMain.isHidden():
            self.ed.reloadAll()

    def charakterEditorModifiedHook(self, params):
        if hasattr(self, "ed") and self.ed and not self.ed.formMain.isHidden():
            self.ed.onModified()

    def createNew(self):
        """
        Creates a new CharakterEditor which is empty and shows it.
        """
        EventBus.doAction("charaktereditor_oeffnet", {"neu": True, "filepath": ""})
        self.ed = CharakterEditor.Editor(self.savePathUpdated)
        if self.ed.noDatabase:
            raise Exception("Konnte datenbank.xml nicht finden")
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm(self._plugins)
        self.savePathUpdated()
        self.ed.formMain.show()
        EventBus.doAction("charaktereditor_geoeffnet", {"neu": True, "filepath": ""})

    def editExisting(self):
        """
        Creates a CharakterEditor for an existing character and shows it.
        """
        if os.path.isdir(Wolke.Settings["Pfad-Chars"]):
            startDir = Wolke.Settings["Pfad-Chars"]
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Charakter laden...", startDir, "XML-Datei (*.xml)"
        )
        if spath == "":
            return
        if not spath.endswith(".xml"):
            spath = spath + ".xml"
        try:
            EventBus.doAction(
                "charaktereditor_oeffnet", {"neu": False, "filepath": spath}
            )
            self.ed = CharakterEditor.Editor(self.savePathUpdated, spath)
        except Exception as e:
            logging.error(
                "Sephrasto Fehlercode "
                + str(Wolke.Fehlercode)
                + ". Exception: "
                + str(e)
            )
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            if Wolke.Fehlercode <= -40 and Wolke.Fehlercode > -80:
                infoBox.setText("Charakterdatei öffnen fehlgeschlagen")
                infoBox.setInformativeText(
                    "Die XML-Datei konnte nicht gelesen werden.\n\
Fehlercode: "
                    + str(Wolke.Fehlercode)
                    + "\n\
Fehlermeldung: "
                    + Wolke.ErrorCode[Wolke.Fehlercode]
                    + "\n"
                )
                infoBox.setWindowTitle("Fehlerhafte Datei")
            else:
                infoBox.setText("Ein unerwarteter Fehler ist aufgetreten!")
                infoBox.setInformativeText(
                    "Ein Fehler ist aufgetreten. Versuche, Sephrasto neu zu starten?\n\
Fehlercode: "
                    + str(Wolke.Fehlercode)
                    + "\n"
                )
                infoBox.setWindowTitle("Unbekannter Fehler")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)
            infoBox.exec_()
        else:
            if self.ed.noDatabase:
                raise Exception("Konnte datenbank.xml nicht finden")
            self.ed.formMain = QtWidgets.QWidget()
            self.ed.ui = CharakterMain.Ui_formMain()
            self.ed.ui.setupUi(self.ed.formMain)
            self.ed.ui.tabs.removeTab(0)
            self.ed.ui.tabs.removeTab(0)
            self.ed.setupMainForm(self._plugins)
            self.savePathUpdated()
            self.ed.formMain.show()
            EventBus.doAction(
                "charaktereditor_geoeffnet", {"neu": False, "filepath": spath}
            )

    def editRuleset(self):
        """
        Creates the DatenbankEdit Form and shows the contents of datenbank.xml.
        """
        self.D = DatenbankEdit.DatenbankEdit()
        self.D.Form = QtWidgets.QWidget()
        self.D.ui = DatenbankMain.Ui_Form()
        self.D.ui.setupUi(self.D.Form)
        self.D.setupGUI()
        self.D.Form.show()

    def editSettings(self):
        EinstellungenWrapper()

    def savePathUpdated(self):
        file = " - Neuer Charakter"
        if self.ed.savepath:
            file = " - " + os.path.basename(self.ed.savepath)
        rules = " (" + os.path.basename(Wolke.DB.datei) + ")" if Wolke.DB.datei else ""
        self.ed.formMain.setWindowTitle("Sephrasto" + file + rules)


if __name__ == "__main__":
    itm = MainWindowWrapper()
