# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 22:36:35 2017

@author: Aeolitus
"""

from PyQt5 import QtCore, QtWidgets
import CharakterMain
import CharakterBeschreibung
import CharakterAttribute
import CharakterEquipment
import sys
import Charakter

class Editor(object):
    def __init__(self, Character=None):
        super().__init__()
        if Character is not None:
            self.char = Character
        else:
            self.char = Charakter.Char()
        
    def setupMainForm(self):
        self.formMain = QtWidgets.QWidget()
        self.ui = CharakterMain.Ui_formMain()
        self.ui.setupUi(self.formMain)
        self.ui.tabs.removeTab(0)
        self.ui.tabs.removeTab(0)
        
        self.formBeschr = QtWidgets.QWidget()
        self.uiBeschr = CharakterBeschreibung.Ui_formBeschreibung()
        self.uiBeschr.setupUi(self.formBeschr)
        
        self.formAttr = QtWidgets.QWidget()
        self.uiAttr = CharakterAttribute.Ui_formAttribute()
        self.uiAttr.setupUi(self.formAttr)
        
        self.formEq = QtWidgets.QWidget()
        self.uiEq = CharakterEquipment.Ui_formAusruestung()
        self.uiEq.setupUi(self.formEq)
        
        self.ui.tabs.addTab(self.formBeschr, "Beschreibung")
        self.ui.tabs.addTab(self.formAttr, "Attribute")
        self.ui.tabs.addTab(self.formEq, "Waffen und Rüstung")    
        
        self.formMain.show()
        
    def updateBeschreibung(self):
        if self.uiBeschr.editName.text() != "":
            self.char.name = self.uiBeschr.editName.text()
        if self.uiBeschr.editRasse.text() != "":
            self.char.rasse = self.uiBeschr.editRasse.text()
        self.char.status = self.uiBeschr.comboStatus.currentIndex()
        self.char.finanzen = self.uiBeschr.comboFinanzen.currentIndex()
        self.char.kurzbeschreibung = self.uiBeschr.editKurzbeschreibung
        self.char.eigenheiten = []
        for i in range(8):
            if eval("self.uiBeschr.editEig" + str(i) + ".text() != \"\""):
                self.char.eigenheiten.append(eval("self.uiBeschr.editEig" + str(i) + ".text()"))
        
    def loadBeschreibung(self):
        self.uiBeschr.editName.setText(self.char.name)
        self.uiBeschr.editRasse.setText(self.char.rasse)
        self.uiBeschr.comboStatus.setCurrentIndex(self.char.status)
        self.uiBeschr.comboFinanzen.setCurrentIndex(self.char.finanzen)
        self.uiBeschr.editKurzbeschreibung.setText(self.char.kurzbeschreibung)
        count = 1
        for el in self.char.eigenheiten:
            eval("self.uiBeschr.editEig" + str(count) + ".setText(" + el + ")")
            count += 1
        #TODO: Update Widget
        
if __name__ == "__main__":
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    ed = Editor()
    ed.setupMainForm()
    sys.exit(app.exec_())            
    