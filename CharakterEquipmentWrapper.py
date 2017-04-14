# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterEquipment
from PyQt5 import QtWidgets, QtCore
import Objekte

class EquipWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.formEq = QtWidgets.QWidget()
        self.uiEq = CharakterEquipment.Ui_formAusruestung()
        self.uiEq.setupUi(self.formEq)
        #Signals
        # Connect all Spins and Edit boxes - hacky, sorry
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "spin"]
        for el in fields:
            eval("self.uiEq." + el + ".valueChanged.connect(self.updateEquipment)")
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "edit"]
        for el in fields:
            eval("self.uiEq." + el + ".editingFinished.connect(self.updateEquipment)")
        
        
        self.uiEq.checkW1FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW2FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW3FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW4FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW5FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkZonen.stateChanged.connect(self.checkToggleEquip)
        
        self.currentlyLoading = False
        
        self.checkToggleEquip()
        
    def updateEquipment(self):
        if not self.currentlyLoading:
            Wolke.Char.rüstung = []
            if self.uiEq.editR1name.text() != "":
                R = Objekte.Ruestung() 
                R.name = self.uiEq.editR1name.text()
                R.be = int(self.uiEq.spinR1be.value())
                if self.uiEq.checkZonen.isChecked():
                    R.rs = [self.uiEq.spinR1bein.value(), self.uiEq.spinR1larm.value(), self.uiEq.spinR1rarm.value(), self.uiEq.spinR1bauch.value(), self.uiEq.spinR1brust.value(), self.uiEq.spinR1kopf.value()]
                else:
                    R.rs = 6*[self.uiEq.spinR1RS.value()]
                Wolke.Char.rüstung.append(R)
            if self.uiEq.editR2name.text() != "":
                R = Objekte.Ruestung() 
                R.name = self.uiEq.editR2name.text()
                R.be = self.uiEq.spinR2be.value()
                if self.uiEq.checkZonen.isChecked():
                    R.rs = [self.uiEq.spinR2bein.value(), self.uiEq.spinR2larm.value(), self.uiEq.spinR2rarm.value(), self.uiEq.spinR2bauch.value(), self.uiEq.spinR2brust.value(), self.uiEq.spinR2kopf.value()]
                else:
                    R.rs = 6*[self.uiEq.spinR2RS]
                Wolke.Char.rüstung.append(R)
                
            Wolke.Char.waffen = []
            for el in ['W1', 'W2', 'W3', 'W4', 'W5']:
                if (eval("self.uiEq.edit" + el + "name.text()") != ""):
                    if eval("self.uiEq.check" + el + "FK.isChecked()"):
                        W = Objekte.Fernkampfwaffe()
                        W.rwnah = eval("self.uiEq.spin" + el + "rw.value()")
                        W.rwfern = eval("self.uiEq.spin" + el + "rw2.value()")
                        W.lz = eval("self.uiEq.spin" + el + "wm.value()")
                    else:
                        W = Objekte.Nahkampfwaffe()
                        W.rw = eval("self.uiEq.spin" + el + "rw.value()")
                        W.wm = eval("self.uiEq.spin" + el + "wm.value()")
                    W.name = eval("self.uiEq.edit" + el + "name.text()")
                    W.haerte = eval("self.uiEq.spin" + el + "h.value()")
                    W.W6 = eval("self.uiEq.spin" + el + "w6.value()")
                    W.plus = eval("self.uiEq.spin" + el + "plus.value()")
                    W.eigenschaften = eval("self.uiEq.edit" + el + "eig.text()")
                    Wolke.Char.waffen.append(W)
            Wolke.Char.aktualisieren()
            self.modified.emit()
        
    def loadEquipment(self):
        self.currentlyLoading = True
        Rarr = ["R1", "R2"]
        count = 0
        while count < len(Wolke.Char.rüstung):
            R = Wolke.Char.rüstung[count]
            eval("self.uiEq.edit" + Rarr[count] + "name.setText(\"" + R.name +"\")")
            eval("self.uiEq.spin" + Rarr[count] + "be.setValue(" + str(R.be) +")")
            eval("self.uiEq.spin" + Rarr[count] + "bein.setValue(" + str(R.rs[0]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "larm.setValue(" + str(R.rs[1]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "rarm.setValue(" + str(R.rs[2]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "bauch.setValue(" + str(R.rs[3]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "brust.setValue(" + str(R.rs[4]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "kopf.setValue(" + str(R.rs[5]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "kopf.setValue(" + str(int(sum(R.rs)/6+0.5)) +")")
            count += 1
        Warr = ["W1","W2","W3","W4","W5"]
        count = 0
        while count < len(Wolke.Char.waffen):
            W = Wolke.Char.waffen[count]
            eval("self.uiEq.edit" + Warr[count] + "name.setText(\""+ W.name +"\")")
            eval("self.uiEq.edit" + Warr[count] + "eig.setText(\""+ W.eigenschaften +"\")")
            eval("self.uiEq.spin" + Warr[count] + "w6.setValue("+ str(W.W6) +")")
            eval("self.uiEq.spin" + Warr[count] + "plus.setValue("+ str(W.plus) +")")
            eval("self.uiEq.spin" + Warr[count] + "h.setValue("+ str(W.haerte) +")")
            if type(W) == Objekte.Fernkampfwaffe:
                eval("self.uiEq.spin" + Warr[count] + "rw.setValue("+ str(W.rwnah) +")")
                eval("self.uiEq.spin" + Warr[count] + "rw2.setEnabled(True)")
                eval("self.uiEq.spin" + Warr[count] + "rw2.show()")
                eval("self.uiEq.spin" + Warr[count] + "rw2.setValue("+ str(W.rwfern) +")")
                eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.lz) +")")
                eval("self.uiEq.check" + Warr[count] + "FK.setChecked(True)")
                eval("self.uiEq.labelDash" + Warr[count] + ".show()")
            elif type(W) == Objekte.Nahkampfwaffe:
                eval("self.uiEq.spin" + Warr[count] + "rw.setValue("+ str(W.rw) +")")
                eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.wm) +")")
                eval("self.uiEq.spin" + Warr[count] + "rw2.setEnabled(False)")
                eval("self.uiEq.spin" + Warr[count] + "rw2.hide()")
                eval("self.uiEq.check" + Warr[count] + "FK.setChecked(False)")
                eval("self.uiEq.labelDash" + Warr[count] + ".hide()")
            count += 1
        self.currentlyLoading = False
        
    def checkToggleEquip(self):
        if not self.currentlyLoading:
            Warr = ["W1","W2","W3","W4","W5"]
            self.currentlyLoading = True
            for el in Warr:
                if not eval("self.uiEq.check" + el + "FK.isChecked()"):
                    eval("self.uiEq.spin" + el + "rw2.setValue(0)")
                    eval("self.uiEq.spin" + el + "rw2.hide()")
                    eval("self.uiEq.spin" + el + "rw2.setEnabled(False)")
                    eval("self.uiEq.labelDash" + el + ".hide()")
                else:
                    eval("self.uiEq.spin" + el + "rw2.show()")
                    eval("self.uiEq.spin" + el + "rw2.setEnabled(True)")
                    eval("self.uiEq.labelDash" + el + ".show()")
            if self.uiEq.checkZonen.isChecked():
                self.uiEq.spinR1bauch.show()
                self.uiEq.spinR1brust.show()
                self.uiEq.spinR1larm.show()
                self.uiEq.spinR1rarm.show()
                self.uiEq.spinR1kopf.show()
                self.uiEq.spinR1bein.show()
                self.uiEq.spinR2bauch.show()
                self.uiEq.spinR2brust.show()
                self.uiEq.spinR2larm.show()
                self.uiEq.spinR2rarm.show()
                self.uiEq.spinR2kopf.show()
                self.uiEq.spinR2bein.show()
                self.uiEq.spinR1RS.hide()
                self.uiEq.spinR2RS.hide()
                self.uiEq.labelRS.hide()
                self.uiEq.labelBein.show()
                self.uiEq.labelBauch.show()
                self.uiEq.labelBrust.show()
                self.uiEq.labelLarm.show()
                self.uiEq.labelRarm.show()
                self.uiEq.labelKopf.show()
            else:
                self.uiEq.spinR1bauch.hide()
                self.uiEq.spinR1brust.hide()
                self.uiEq.spinR1larm.hide()
                self.uiEq.spinR1rarm.hide()
                self.uiEq.spinR1kopf.hide()
                self.uiEq.spinR1bein.hide()
                self.uiEq.spinR2bauch.hide()
                self.uiEq.spinR2brust.hide()
                self.uiEq.spinR2larm.hide()
                self.uiEq.spinR2rarm.hide()
                self.uiEq.spinR2kopf.hide()
                self.uiEq.spinR2bein.hide()
                self.uiEq.spinR1RS.show()
                self.uiEq.spinR2RS.show()
                self.uiEq.labelRS.show()
                self.uiEq.labelBein.hide()
                self.uiEq.labelBauch.hide()
                self.uiEq.labelBrust.hide()
                self.uiEq.labelLarm.hide()
                self.uiEq.labelRarm.hide()
                self.uiEq.labelKopf.hide()
            self.currentlyLoading = False