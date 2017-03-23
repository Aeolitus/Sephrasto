# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:30:34 2017

@author: Aeolitus
"""
from PyQt5 import QtWidgets, QtCore
import sys
import MainWindow
import CharakterEditor
import DatenbankEdit
import CharakterMain
import DatenbankMain

class MainWindowWrapper(object):
    def __init__(self):
        super().__init__()
            
        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = MainWindow.Ui_Form()
        self.ui.setupUi(self.Form)
        self.ui.buttonNew.clicked.connect(self.createNew)
        self.ui.buttonEdit.clicked.connect(self.editExisting)
        self.ui.buttonRules.clicked.connect(self.editRuleset)
        self.Form.show()
        sys.exit(self.app.exec_())
        
    def createNew(self):
        self.ed = CharakterEditor.Editor()
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        self.ed.formMain.show()
        
    def editExisting(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Charakter laden...","","XML-Datei (*.xml)")
        if ".xml" not in spath:
            spath = spath + ".xml"
        try:
            self.ed = CharakterEditor.Editor(spath)
        except:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Charakterdatei öffnen fehlgeschlagen")
            infoBox.setInformativeText("Die XML-Datei konnte nicht gelesen werden. Ist sie mit dieser Version von Sephrasto kompatibel?")
            infoBox.setWindowTitle("Fehlerhafte Datei")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = CharakterMain.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.ui.tabs.removeTab(0)
        self.ed.ui.tabs.removeTab(0)
        self.ed.setupMainForm()
        self.ed.formMain.show()
        
    def editRuleset(self):
        self.D = DatenbankEdit.DatenbankEdit()
        self.D.Form = QtWidgets.QWidget()
        self.D.ui = DatenbankMain.Ui_Form()
        self.D.ui.setupUi(self.D.Form)
        self.D.setupGUI()
        self.D.Form.show()
        
        
if __name__ == "__main__":
    itm = MainWindowWrapper()