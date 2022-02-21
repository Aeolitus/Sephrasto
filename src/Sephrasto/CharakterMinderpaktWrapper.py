# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:21:03 2017

@author: Aeolitus
"""
from Wolke import Wolke
import UI.CharakterMinderpakt
from PyQt5 import QtWidgets, QtCore, QtGui
import logging

class CharakterMinderpaktWrapper():    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing Minderpakt...")
        self.formVor = QtWidgets.QDialog()
        self.uiVor = UI.CharakterMinderpakt.Ui_Dialog()
        self.uiVor.setupUi(self.formVor)
        self.formVor.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.uiVor.splitter.adjustSize()
        width = self.uiVor.splitter.size().width()
        self.uiVor.splitter.setSizes([int(width*0.6), int(width*0.4)])

        self.vorteilTypen = Wolke.DB.einstellungen["Vorteile: Typen"].toTextList()
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
        for vortTyp in self.vorteilTypen:
            vortList.append([])
        for el in Wolke.DB.vorteile:
            if Wolke.DB.vorteile[el].kosten > 20 and not Wolke.DB.vorteile[el].variableKosten:
                continue
            if Wolke.DB.vorteile[el].kosten < 0:
                continue
            if el in Wolke.Char.vorteile:
                continue
            idx = min(Wolke.DB.vorteile[el].typ, len(vortList)-1)
            vortList[idx].append(el)

        for vorteile in vortList:
            vorteile.sort()

        for i in range(len(vortList)):
            parent = QtWidgets.QTreeWidgetItem(self.uiVor.treeWidget)
            parent.setText(0, self.vorteilTypen[i])
            parent.setText(1,"")
            parent.setExpanded(True)
            font = QtWidgets.QApplication.instance().font()
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            font.setPointSize(max(Wolke.Settings["FontSize"] + 1, Wolke.Settings["FontHeadingSize"]))
            parent.setFont(0, font)
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
            if el.text(0) in self.vorteilTypen:
                continue
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()
 
    def updateInfo(self):
        if self.currentVort != "":
            self.uiVor.labelVorteil.setText(Wolke.DB.vorteile[self.currentVort].name)
            typ = min(Wolke.DB.vorteile[self.currentVort].typ, len(self.vorteilTypen)-1)
            self.uiVor.labelTyp.setText(self.vorteilTypen[typ])
            self.uiVor.labelNachkauf.setText(Wolke.DB.vorteile[self.currentVort].nachkauf)
            self.uiVor.plainText.setPlainText(Wolke.DB.vorteile[self.currentVort].text)
            if Wolke.DB.vorteile[self.currentVort].variableKosten:
                self.uiVor.labelKosten.setText("20 EP")
            else:
                self.uiVor.labelKosten.setText(str(Wolke.DB.vorteile[self.currentVort].kosten) + " EP")