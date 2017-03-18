# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:21:03 2017

@author: Aeolitus
"""
from Wolke import Wolke
import CharakterVorteile
from PyQt5 import QtWidgets, QtCore
from Definitionen import VorteilTypen
from Hilfsmethoden import Hilfsmethoden

class CharakterVorteileWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.formVor = QtWidgets.QWidget()
        self.uiVor = CharakterVorteile.Ui_Form()
        self.uiVor.setupUi(self.formVor)
        
        self.uiVor.treeWidget.itemSelectionChanged.connect(self.vortClicked)
        self.uiVor.treeWidget.itemChanged.connect(self.itemChangeHandler)
        self.uiVor.treeWidget.header().setSectionResizeMode(0,1)
        
        if len(Wolke.Char.vorteile) > 0:
            self.currentVort = Wolke.Char.vorteile[0]
        else:
            self.currentVort = ""
        
        self.loadVorteile()
            
    def loadVorteile(self):
        self.uiVor.treeWidget.blockSignals(True)
        try:
            vortList = [[],[],[],[],[],[],[],[]]
            for el in Wolke.DB.vorteile:
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.vorteile[el].voraussetzungen):
                    idx = Wolke.DB.vorteile[el].typ-1
                    vortList[idx].append(el)
            self.uiVor.treeWidget.clear()
            for i in range(len(vortList)):
                parent = QtWidgets.QTreeWidgetItem(self.uiVor.treeWidget)
                parent.setText(0, VorteilTypen[i])
                parent.setExpanded(True)
                for el in vortList[i]:
                    child = QtWidgets.QTreeWidgetItem(parent)
                    #child.setC #setFlags(child.flags() | QtGui.Qt.ItemIsUserCheckable)
                    child.setText(0, Wolke.DB.vorteile[el].name)
                    if el in Wolke.Char.vorteile:    
                        child.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        child.setCheckState(0, QtCore.Qt.Unchecked)
                    child.setText(1, str(Wolke.DB.vorteile[el].kosten))
            self.updateInfo()
        except:
            pass
        self.uiVor.treeWidget.blockSignals(False)
        
    def updateVorteile(self):
        pass
    
    def itemChangeHandler(self, item, column):
        # Block Signals to make sure we dont repeat infinitely
        self.uiVor.treeWidget.blockSignals(True)
        try:
            name = item.text(0)
            self.currentVort = name
            self.updateInfo()
            cs = item.checkState(0)
            if cs ==  QtCore.Qt.Checked:
                if name not in Wolke.Char.vorteile and name != "":
                    Wolke.Char.vorteile.append(name)
            else:
                if name in Wolke.Char.vorteile:
                    Wolke.Char.vorteile.remove(name)
            self.modified.emit()
            self.loadVorteile()        
        except:
            pass
        self.uiVor.treeWidget.blockSignals(False)
    
    def vortClicked(self):
        for el in self.uiVor.treeWidget.selectedItems():
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()
    
    def updateInfo(self):
        if self.currentVort != "":
            self.uiVor.labelVorteil.setText(Wolke.DB.vorteile[self.currentVort].name)
            self.uiVor.labelTyp.setText(VorteilTypen[Wolke.DB.vorteile[self.currentVort].typ-1])
            self.uiVor.labelNachkauf.setText(Wolke.DB.vorteile[self.currentVort].nachkauf)
            self.uiVor.plainText.setPlainText(Wolke.DB.vorteile[self.currentVort].text)
            self.uiVor.plainVoraussetzungen.setPlainText(Hilfsmethoden.VorArray2Str(
                    Wolke.DB.vorteile[self.currentVort].voraussetzungen, Wolke.DB))
            self.uiVor.spinKosten.setValue(Wolke.DB.vorteile[self.currentVort].kosten)
        
            