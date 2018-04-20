#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:30:34 2017

@author: Aeolitus
"""
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import logging
import os.path
import MainWindow
import CharakterEditor
import DatenbankEdit
import CharakterMain
import DatenbankMain
from Wolke import Wolke

logging.basicConfig(filename="sephrasto.log", level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s(%(lineno)d) | %(message)s")

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
        self._version_ = "v0.5.2"
        super().__init__()
        
        #Make sure the application scales properly, i.e. in Win10 users can change the UI scale in the display settings
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        #self.app.setStyleSheet("*[readOnly=\"true\"] { background-color: #F5F5F5 } QAbstractScrollArea #scrollAreaWidgetContents { background-color: #FFFFFF }")
        self.app.setStyleSheet("""
        *[readOnly=\"true\"] 
        { 
            background-color: #FFFFFF;
            border: none
        } 
        QAbstractScrollArea #scrollAreaWidgetContents 
        { 
            background-color: #FFFFFF 
        }
        """)
        self.Form = QtWidgets.QWidget()
        self.ui = MainWindow.Ui_Form()
        self.ui.setupUi(self.Form)
        self.ui.buttonNew.clicked.connect(self.createNew)
        self.ui.buttonEdit.clicked.connect(self.editExisting)
        self.ui.buttonRules.clicked.connect(self.editRuleset)
        self.ui.labelVersion.setText(self._version_ + " - by Aeolitus ")

        self.app.setWindowIcon(QtGui.QIcon('icon_large.png'))

        self.Form.show()
        sys.exit(self.app.exec_())
        
    def createNew(self):
        '''
        Creates a new CharakterEditor which is empty and shows it.
        '''
        self.ed = CharakterEditor.Editor()
        if self.ed.noDatabase:
            raise Exception("Konnte datenbank.xml nicht finden")
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        splitpath = os.path.split(Wolke.DB.datei)
        self.ed.formMain.setWindowTitle(self.ed.formMain.windowTitle() + " (" + splitpath[-1] + ")")
        self.ed.formMain.show()
        
    def editExisting(self):
        '''
        Creates a CharakterEditor for an existing character and shows it.
        '''
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Charakter laden...","","XML-Datei (*.xml)")
        if spath == "":
            return
        if not spath.endswith(".xml"):
            spath = spath + ".xml"
        try:
            self.ed = CharakterEditor.Editor(spath)
        except:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            if Wolke.Fehlercode <= -40 and Wolke.Fehlercode > -80:
                infoBox.setText("Charakterdatei öffnen fehlgeschlagen")
                infoBox.setInformativeText("Die XML-Datei konnte nicht gelesen werden.\n\
Fehlercode: " + str(Wolke.Fehlercode) + "\n\
Fehlermeldung: " + Wolke.ErrorCode[Wolke.Fehlercode] + "\n")
                infoBox.setWindowTitle("Fehlerhafte Datei")
            else:
                infoBox.setText("Ein unerwarteter Fehler ist aufgetreten!")
                infoBox.setInformativeText("Ein Fehler ist aufgetreten. Versuche, Sephrasto neu zu starten?\n\
Fehlercode: " + str(Wolke.Fehlercode) + "\n")
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
            self.ed.setupMainForm()
            splitpath = os.path.split(Wolke.DB.datei)
            self.ed.formMain.setWindowTitle(self.ed.formMain.windowTitle() + " (" + splitpath[-1] + ")")
            self.ed.formMain.show()
        
    def editRuleset(self):
        '''
        Creates the DatenbankEdit Form and shows the contents of datenbank.xml.
        '''
        self.D = DatenbankEdit.DatenbankEdit()
        self.D.Form = QtWidgets.QWidget()
        self.D.ui = DatenbankMain.Ui_Form()
        self.D.ui.setupUi(self.D.Form)
        self.D.setupGUI()
        self.D.Form.show()
        
if __name__ == "__main__":
    itm = MainWindowWrapper()