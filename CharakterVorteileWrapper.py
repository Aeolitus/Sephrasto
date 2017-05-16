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
        if Wolke.Debug:
            print("Initializing VorteileWrapper...")
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
            
        self.itemWidgets = {}
        
        self.initVorteile()
          
    def initVorteile(self):
        self.uiVor.treeWidget.blockSignals(True)
        vortList = [[],[],[],[],[],[],[],[]]
        for el in Wolke.DB.vorteile:
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
                if Wolke.DB.vorteile[el].variable!=0:
                    spin = QtWidgets.QSpinBox()
                    spin.setMinimum(0)
                    spin.setSuffix(" EP")
                    spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
                    spin.setMaximum(9999)
                    if el in Wolke.Char.vorteileVariable:
                        spin.setValue(Wolke.Char.vorteileVariable[el])
                    else:
                        spin.setValue(Wolke.DB.vorteile[el].kosten)
                    spin.setSingleStep(20)
                    self.itemWidgets[el] = spin
                    spin.valueChanged.connect(lambda state, name=el: self.spinnerChanged(name,state))
                    self.uiVor.treeWidget.setItemWidget(child,1,spin)
                else:
                    child.setText(1, str(Wolke.DB.vorteile[el].kosten) + " EP")
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.vorteile[el].voraussetzungen):
                    child.setHidden(False)
                else:
                    child.setHidden(True)
        self.updateInfo()
        self.uiVor.treeWidget.blockSignals(False)
        
    def loadVorteile(self):
        self.uiVor.treeWidget.blockSignals(True)
        vortList = [[],[],[],[],[],[],[],[]]
        for el in Wolke.DB.vorteile:
            if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.vorteile[el].voraussetzungen):
                idx = Wolke.DB.vorteile[el].typ
                vortList[idx].append(el)
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
                if txt in Wolke.Char.vorteile:    
                    chi.setCheckState(0, QtCore.Qt.Checked)
                else:
                    chi.setCheckState(0, QtCore.Qt.Unchecked) 
                if txt not in vortList[i]:
                    chi.setHidden(True)
                    if txt in Wolke.Char.vorteile:
                        chi.setCheckState(0,QtCore.Qt.Unchecked)
                        Wolke.Char.vorteile.remove(txt)
                else:
                    chi.setHidden(False)
                if Wolke.DB.vorteile[el].variable!=0:
                    Wolke.Char.vorteileVariable[el] = self.itemWidgets[el].value()
        self.updateInfo()
        self.uiVor.treeWidget.blockSignals(False)
        
    def updateVorteile(self):
        pass
    
    def spinnerChanged(self,name,state):
        Wolke.Char.vorteileVariable[name] = state
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()
    
    def itemChangeHandler(self, item, column):
        # Block Signals to make sure we dont repeat infinitely
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
            self.uiVor.labelTyp.setText(VorteilTypen[Wolke.DB.vorteile[self.currentVort].typ-1])
            self.uiVor.labelNachkauf.setText(Wolke.DB.vorteile[self.currentVort].nachkauf)
            self.uiVor.plainText.setPlainText(Wolke.DB.vorteile[self.currentVort].text)
            self.uiVor.plainVoraussetzungen.setPlainText(Hilfsmethoden.VorArray2Str(
                    Wolke.DB.vorteile[self.currentVort].voraussetzungen, None))
            if Wolke.DB.vorteile[self.currentVort].variable!=0 and self.currentVort in Wolke.Char.vorteileVariable:
                self.uiVor.spinKosten.setValue(Wolke.Char.vorteileVariable[self.currentVort])
            else:
                self.uiVor.spinKosten.setValue(Wolke.DB.vorteile[self.currentVort].kosten)      
            