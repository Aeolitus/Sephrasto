# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:21:03 2017

@author: Aeolitus
"""
from Wolke import Wolke
import CharakterMinderpakt
from PyQt5 import QtWidgets, QtCore
from Definitionen import VorteilTypen
import logging

class CharakterMinderpaktWrapper():    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing Minderpakt...")
        self.formVor = QtWidgets.QDialog()
        self.uiVor = CharakterMinderpakt.Ui_Dialog()
        self.uiVor.setupUi(self.formVor)
        self.formVor.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.uiVor.treeWidget.itemSelectionChanged.connect(self.vortClicked)
        self.uiVor.treeWidget.header().setSectionResizeMode(0,1)
        if len(Wolke.Char.vorteile) > 0:
            self.currentVort = Wolke.Char.vorteile[0]
        else:
            self.currentVort = ""
        self.initVorteile()
        self.formVor.setWindowModality(QtCore.Qt.ApplicationModal)
        self.formVor.show()
        self.ret = self.formVor.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            if self.currentVort not in Wolke.DB.vorteile:
                self.minderpakt = None
            else:
                self.minderpakt = self.currentVort
        else:
            self.minderpakt = None
          
    def initVorteile(self):
        self.uiVor.treeWidget.blockSignals(True)
        vortList = []
        for vortTyp in VorteilTypen:
            vortList.append([])
        for el in Wolke.DB.vorteile:
            if Wolke.DB.vorteile[el].kosten > 20 and not Wolke.DB.vorteile[el].variableKosten:
                continue
            if Wolke.DB.vorteile[el].kosten < 0:
                continue
            if el in Wolke.Char.vorteile:
                continue
            idx = Wolke.DB.vorteile[el].typ
            vortList[idx].append(el)

        for vorteile in vortList:
            vorteile.sort()

        for i in range(len(vortList)):
            parent = QtWidgets.QTreeWidgetItem(self.uiVor.treeWidget)
            parent.setText(0, VorteilTypen[i])
            parent.setText(1,"")
            parent.setExpanded(True)
            for el in vortList[i]:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, Wolke.DB.vorteile[el].name)
                if Wolke.DB.vorteile[el].variableKosten:
                    child.setText(1, "20 EP")
                else:
                    child.setText(1, str(Wolke.DB.vorteile[el].kosten) + " EP")
        self.updateInfo()
        self.uiVor.treeWidget.blockSignals(False)
    
    def vortClicked(self):
        for el in self.uiVor.treeWidget.selectedItems():
            if el.text(0) in VorteilTypen:
                continue
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()
 
    def updateInfo(self):
        if self.currentVort != "":
            self.uiVor.labelVorteil.setText(Wolke.DB.vorteile[self.currentVort].name)
            self.uiVor.labelTyp.setText(VorteilTypen[Wolke.DB.vorteile[self.currentVort].typ])
            self.uiVor.labelNachkauf.setText(Wolke.DB.vorteile[self.currentVort].nachkauf)
            self.uiVor.plainText.setPlainText(Wolke.DB.vorteile[self.currentVort].text)
            if Wolke.DB.vorteile[self.currentVort].variableKosten:
                self.uiVor.spinKosten.setValue(20)
            else:
                self.uiVor.spinKosten.setValue(Wolke.DB.vorteile[self.currentVort].kosten)      