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
        
        self.initVorteile()
          
    def initVorteile(self):
        try:
            self.uiVor.treeWidget.blockSignals(True)
            vortList = [[],[],[],[],[],[],[],[]]
            for el in Wolke.DB.vorteile:
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.vorteile[el].voraussetzungen):
                    idx = Wolke.DB.vorteile[el].typ
                    vortList[idx].append(el)
            for i in range(len(vortList)):
                parent = QtWidgets.QTreeWidgetItem(self.uiVor.treeWidget)
                parent.setText(0, VorteilTypen[i])
                parent.setText(1,"")
                parent.setExpanded(True)
                for el in vortList[i]:
                    child = QtWidgets.QTreeWidgetItem(parent)
                    child.setText(0, Wolke.DB.vorteile[el].name)
                    if el in Wolke.Char.vorteile:    
                        child.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        child.setCheckState(0, QtCore.Qt.Unchecked)
                    child.setText(1, str(Wolke.DB.vorteile[el].kosten))
            self.updateInfo()
            self.uiVor.treeWidget.blockSignals(False)
        except:
            print("Error thrown in CVW->initVorteile")
        
    def loadVorteile(self):
        try:
            self.uiVor.treeWidget.blockSignals(True)
            vortList = [[],[],[],[],[],[],[],[]]
            for el in Wolke.DB.vorteile:
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.vorteile[el].voraussetzungen):
                    idx = Wolke.DB.vorteile[el].typ
                    vortList[idx].append(el)
            #self.uiVor.treeWidget.clear()
            # Workaround since clear causes python to crash sometimes:
            cpy = vortList[:]
            for i in range(len(vortList)):
                itm = self.uiVor.treeWidget.topLevelItem(i)
                if type(itm) != QtWidgets.QTreeWidgetItem:
                        continue
                if itm == 0: 
                    continue
                for j in range(itm.childCount()):
                    chi = itm.child(j)
                    if type(chi) != QtWidgets.QTreeWidgetItem:
                        continue
                    txt = chi.text(0)
                    if txt not in vortList[i]:
                        chi.setHidden(True)
                    else:
                        chi.setHidden(False)
                        cpy[i].remove(txt)
                for el in cpy[i]:
                    ix = 0
                    for i in range(itm.childCount()):
                        if el < itm.child(i).text(0):
                            break
                        ix += 1
                    child = QtWidgets.QTreeWidgetItem()
                    child.setText(0, Wolke.DB.vorteile[el].name)
                    if el in Wolke.Char.vorteile:    
                        child.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        child.setCheckState(0, QtCore.Qt.Unchecked)
                    child.setText(1, str(Wolke.DB.vorteile[el].kosten))
                    itm.insertChild(ix, child)
            self.updateInfo()
            self.uiVor.treeWidget.blockSignals(False)
        except:
            print("Error thrown in CVW->loadVorteile")
        
    def updateVorteile(self):
        pass
    
    def itemChangeHandler(self, item, column):
        # Block Signals to make sure we dont repeat infinitely
        try:            
            self.uiVor.treeWidget.blockSignals(True)
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
            self.uiVor.treeWidget.blockSignals(False)
        except:
            print("Error thrown in CVW->itemChangeHandler")            
    
    def vortClicked(self):
        try:
            for el in self.uiVor.treeWidget.selectedItems():
                if el.text(1) == "":
                    continue
                self.currentVort = el.text(0)
                break #First one should be all of them
            self.updateInfo()
        except:
            print("Error thrown in CVW->vortClicked")

    
    def updateInfo(self):
        try:
            if self.currentVort != "":
                self.uiVor.labelVorteil.setText(Wolke.DB.vorteile[self.currentVort].name)
                self.uiVor.labelTyp.setText(VorteilTypen[Wolke.DB.vorteile[self.currentVort].typ-1])
                self.uiVor.labelNachkauf.setText(Wolke.DB.vorteile[self.currentVort].nachkauf)
                self.uiVor.plainText.setPlainText(Wolke.DB.vorteile[self.currentVort].text)
                self.uiVor.plainVoraussetzungen.setPlainText(Hilfsmethoden.VorArray2Str(
                        Wolke.DB.vorteile[self.currentVort].voraussetzungen, None))
                self.uiVor.spinKosten.setValue(Wolke.DB.vorteile[self.currentVort].kosten)
        except:
            print("Error thrown in CVW->updateInfo")
        
            