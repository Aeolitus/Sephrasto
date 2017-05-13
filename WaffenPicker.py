# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import CharakterWaffen
from PyQt5 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import Objekte
import Definitionen

class WaffenPicker(object):
    def __init__(self,waffe=None):
        super().__init__()
        self.waffe = waffe
        self.current = waffe.name
        self.Form = QtWidgets.QDialog()
        self.ui = CharakterWaffen.Ui_Dialog()
        self.ui.setupUi(self.Form)
        
        for kind in Definitionen.Kampftalente:
            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWeapons)
            parent.setText(0,kind)
            parent.setText(1,"")
            parent.setExpanded(True)
            wafs = []
            for waf in Wolke.DB.waffen:
                if Wolke.DB.waffen[waf].fertigkeit == kind:
                    wafs.append(waf)
            wafs.sort()
            for el in wafs:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0,el)
                child.setText(1,Wolke.DB.waffen[waf].talent)  
        
        self.ui.treeWeapons.itemChanged.connect(self.changeHandler)
        self.ui.treeWeapons.header().setSectionResizeMode(0,1)
        self.updateInfo()
        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted and self.current != '':
            self.waffe = Wolke.DB.waffen[self.current]
        else:
            self.waffe = None
    
    def changeHandler(self):
        for el in self.ui.treeWeapons.selectedItems():
            if el.text(0) in Definitionen.Kampftalente:
                continue
            self.current = el
            break
        self.updateInfo()
        
    def updateInfo(self):
        if self.current != "":
            w = Wolke.DB.waffen[self.current]
            self.ui.labelName.setText(w.name)
            if type(w) == Objekte.Nahkampfwaffe:
                self.ui.labelTyp.setText("Nah")
            else:
                self.ui.labelTyp.setText("Fern")
            self.ui.labelFert.setText(w.fertigkeit + ": " + w.talent)
            stile = ""
            if w.beid:
                stile += "Beidhändiger Kampf, "
            if w.pari:
                stile += "Parierwaffenkampf, "
            if w.reit:
                stile += "Reiterkampf, "
            if w.schi:
                stile += "Schildkampf, "
            if w.kraf:
                stile += "Kraftvoller Kampf, "
            if w.schn:
                stile += "Schneller Kampf, "
            if len(stile)>2:
                stile = stile[:-2]
            self.ui.labelStile.setText(stile)
            tp = str(w.W6) + " W6"
            if w.plus < 0:
                tp += " " + str(w.plus)
            else:
                tp += " +" + str(w.plus)
            self.ui.labelTP.setText(tp)
            if type(w) == Objekte.Nahkampfwaffe:
                self.ui.labelRW.setText(str(w.rw))
                self.ui.labelWMLZ_Text.setText("Waffenmodifikator")
                if w.wm<0:
                    self.ui.labelWMLZ.setText(str(w.wm))
                else:
                    self.ui.labelWMLZ.setText("+" + str(w.wm))
            else:
                self.ui.labelRW.setText(str(w.rwnah) + " / " + str(w.rwfern))
                self.ui.labelWMLZ_Text.setText("Ladezeit")
                self.ui.labelWMLZ.setText(str(w.lz))
            self.ui.labelH.setText(str(w.haerte))
            self.ui.plainEigenschaften.setPlainText(w.eigenschaften)
        
            