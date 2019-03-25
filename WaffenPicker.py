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
import logging

class WaffenPicker(object):
    def __init__(self,waffe=None):
        super().__init__()
        logging.debug("Initializing WaffenPicker...")
        self.waffe = None
        if waffe is not None and waffe in Wolke.DB.waffen:
            self.current = waffe
        else:
            self.current = ""
        self.Form = QtWidgets.QDialog()
        self.ui = CharakterWaffen.Ui_Dialog()
        self.ui.setupUi(self.Form)
        
        self.Form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        logging.debug("Ui is Setup...")
        currSet = self.current != ""

        kampfferts = self.findKampfFertigkeiten()

        for kind in kampfferts:
            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWeapons)
            parent.setText(0,kind.name)
            parent.setText(1,"")
            parent.setExpanded(True)
            wafs = []
            for waf in Wolke.DB.waffen:
                if Wolke.DB.waffen[waf].fertigkeit == kind.name:
                    wafs.append(waf)
            wafs.sort()
            for el in wafs:
                if not currSet:
                    self.current = el
                    currSet = True
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0,Wolke.DB.waffen[el].anzeigename or el)
                child.setText(1,Wolke.DB.waffen[el].talent)
                child.setData(0, QtCore.Qt.UserRole, el) # store key of weapon in user data
        self.ui.treeWeapons.sortItems(1,QtCore.Qt.AscendingOrder)
        logging.debug("Tree Filled...")
        self.ui.treeWeapons.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeWeapons.header().setSectionResizeMode(0,1)
        self.updateInfo()
        logging.debug("Info Updated...")
        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted and self.current != '':
            self.waffe = Wolke.DB.waffen[self.current]
        else:
            self.waffe = None

    def findKampfFertigkeiten(self):
        return [el for el in Wolke.DB.fertigkeiten.values() if el.kampffertigkeit > 0]

    def changeHandler(self):
        kampfferts = []
        for fert in self.findKampfFertigkeiten():
            kampfferts.append(fert.name)

        for el in self.ui.treeWeapons.selectedItems():
            if el.text(0) in kampfferts:
                continue
            self.current = el.data(0, QtCore.Qt.UserRole) # contains key of weapon
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
            self.ui.labelFert.setText(w.fertigkeit + " (" + w.talent + ")")
            stile = Definitionen.KeinKampfstil

            if len(w.kampfstile) > 0:
                stile = ", ".join(w.kampfstile)

            self.ui.plainStile.setPlainText(stile)
            tp = str(w.W6) + " W6"
            if w.plus < 0:
                tp += " " + str(w.plus)
            else:
                tp += " +" + str(w.plus)
            self.ui.labelTP.setText(tp)
            self.ui.labelRW.setText(str(w.rw))
            if type(w) == Objekte.Nahkampfwaffe:
                self.ui.labelWMLZ_Text.setText("Waffenmodifikator")
                if w.wm<0:
                    self.ui.labelWMLZ.setText(str(w.wm))
                else:
                    self.ui.labelWMLZ.setText("+" + str(w.wm))
            else:
                self.ui.labelWMLZ_Text.setText("Ladezeit")
                self.ui.labelWMLZ.setText(str(w.lz))
            self.ui.labelH.setText(str(w.haerte))
            self.ui.plainEigenschaften.setPlainText(", ".join(w.eigenschaften))
        
            