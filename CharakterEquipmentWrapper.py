# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterEquipment
from PyQt5 import QtWidgets, QtCore
import Objekte
import Definitionen
from WaffenPicker import WaffenPicker

class EquipWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        if Wolke.Debug:
            print("Initializing EquipWrapper...")
        self.formEq = QtWidgets.QWidget()
        self.uiEq = CharakterEquipment.Ui_formAusruestung()
        self.uiEq.setupUi(self.formEq)
        self.initialLoad = True
        if Wolke.Debug:
            print("UI Setup...")
        #Signals
        # Connect all Spins and Edit boxes - hacky, sorry
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "spin"]
        for el in fields:
            eval("self.uiEq." + el + ".valueChanged.connect(self.updateEquipment)")
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "edit"]
        for el in fields:
            eval("self.uiEq." + el + ".editingFinished.connect(self.updateEquipment)")
        if Wolke.Debug:
            print("Signals Set...")
        for el in range(1,6):
            eval("self.uiEq.comboStil"+str(el)+".setCurrentIndex(0)")
            eval("self.uiEq.comboStil"+str(el)+".clear()")
            for el2 in Definitionen.Kampfstile:
                eval("self.uiEq.comboStil"+str(el)+".addItem(\""+el2+"\")")
        if Wolke.Debug:
            print("Kampfstile added...")
        self.uiEq.addW1.clicked.connect(lambda state, idx=1: self.selectWeapon(idx))   
        self.uiEq.addW2.clicked.connect(lambda state, idx=2: self.selectWeapon(idx))   
        self.uiEq.addW3.clicked.connect(lambda state, idx=3: self.selectWeapon(idx))   
        self.uiEq.addW4.clicked.connect(lambda state, idx=4: self.selectWeapon(idx))   
        self.uiEq.addW5.clicked.connect(lambda state, idx=5: self.selectWeapon(idx))   
        if Wolke.Debug:
            print("Check Toggle...")
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
                        W.lz = eval("self.uiEq.spin" + el + "wm.value()")
                    else:
                        W = Objekte.Nahkampfwaffe()
                        W.wm = eval("self.uiEq.spin" + el + "wm.value()")
                    W.name = eval("self.uiEq.edit" + el + "name.text()")
                    W.rw = eval("self.uiEq.spin" + el + "rw.value()")
                    W.haerte = eval("self.uiEq.spin" + el + "h.value()")
                    W.W6 = eval("self.uiEq.spin" + el + "w6.value()")
                    W.plus = eval("self.uiEq.spin" + el + "plus.value()")
                    W.eigenschaften = eval("self.uiEq.edit" + el + "eig.text()")
                    self.refreshKampfstile(int(el[-1])-1)
                    tmp = eval("self.uiEq.comboStil" + el[-1] + ".currentText()")
                    if tmp in Definitionen.Kampfstile:
                        W.kampfstil = Definitionen.Kampfstile.index(tmp)
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
            eval("self.uiEq.spin" + Rarr[count] + "RS.setValue(" + str(int(sum(R.rs)/6+0.5)) +")")
            count += 1
        
        count = 0
        while count < len(Wolke.Char.waffen):
            W = Wolke.Char.waffen[count]
            self.loadWeaponIntoFields(W, count+1)
            count += 1
        self.initialLoad = False
        self.currentlyLoading = False
        
    def refreshKampfstile(self, index):
        if Wolke.Debug:
            print("Starting refreshKampfstile for index " + str(index))
        name = eval("self.uiEq.editW" + str(index+1) + "name.text()")
        tmp = eval("self.uiEq.comboStil" + str(index+1) + ".currentText()")
        if name != "":
            if name in Wolke.DB.waffen:
                entries = []
                entries.append(Definitionen.Kampfstile[0])
                if Wolke.DB.waffen[name].beid and Definitionen.Kampfstile[1] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[1])
                if Wolke.DB.waffen[name].pari and Definitionen.Kampfstile[2] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[2])
                if Wolke.DB.waffen[name].reit and Definitionen.Kampfstile[3] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[3])
                if Wolke.DB.waffen[name].schi and Definitionen.Kampfstile[4] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[4])
                if Wolke.DB.waffen[name].kraf and Definitionen.Kampfstile[5] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[5])
                if Wolke.DB.waffen[name].schn and Definitionen.Kampfstile[6] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[6])
                eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(0)")
                eval("self.uiEq.comboStil" + str(index+1) + ".clear()")
                for el in entries:
                    eval("self.uiEq.comboStil" + str(index+1) + ".addItem(\"" + el + "\")")
                if self.initialLoad:
                    stil = Definitionen.Kampfstile[Wolke.Char.waffen[index].kampfstil]
                    if stil in entries:
                        eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(" + str(entries.index(stil)) + ")")
                    else:
                        eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(0)")
                elif tmp in entries:
                    eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(" + str(entries.index(tmp)) + ")")
                
                    
    def loadWeaponIntoFields(self, W, index):
        Warr = ["W1","W2","W3","W4","W5"]
        count = index - 1
        eval("self.uiEq.edit" + Warr[count] + "name.setText(\""+ W.name +"\")")
        self.refreshKampfstile(count)
        eval("self.uiEq.edit" + Warr[count] + "eig.setText(\""+ W.eigenschaften +"\")")
        eval("self.uiEq.spin" + Warr[count] + "w6.setValue("+ str(W.W6) +")")
        eval("self.uiEq.spin" + Warr[count] + "plus.setValue("+ str(W.plus) +")")
        if W.name == "Unbewaffnet":
            wsmod = Wolke.Char.rsmod + Wolke.Char.ws
            if len(Wolke.Char.rüstung) > 0:    
                wsmod += int(sum(Wolke.Char.rüstung[0].rs)/6+0.5)
            eval("self.uiEq.spin" + Warr[count] + "h.setValue("+ str(wsmod) +")")
        else:
            eval("self.uiEq.spin" + Warr[count] + "h.setValue("+ str(W.haerte) +")")
        eval("self.uiEq.spin" + Warr[count] + "rw.setValue("+ str(W.rw) +")")
        if type(W) == Objekte.Fernkampfwaffe:
            eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.lz) +")")
            eval("self.uiEq.check" + Warr[count] + "FK.setChecked(True)")
        elif type(W) == Objekte.Nahkampfwaffe:
            eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.wm) +")")
            eval("self.uiEq.check" + Warr[count] + "FK.setChecked(False)")
        
    def selectWeapon(self, index):
        W = None
        try:
            wname = eval("self.uiEq.editW" + str(index) + "name.text()")
            for el in Wolke.DB.waffen:
                if Wolke.DB.waffen[el].name == wname:
                    W = el
                    if Wolke.Debug:
                        print("Weapon found - its " + wname)
                    break
        except:
            pass
            #print("Error in selectWeapon!")
        if Wolke.Debug:
            print("Starting WaffenPicker")
        picker = WaffenPicker(W)
        if Wolke.Debug:
            print("WaffenPicker created")
        if picker.waffe is not None:
            self.currentlyLoading = True
            self.loadWeaponIntoFields(picker.waffe, index)
            self.currentlyLoading = False
            self.updateEquipment()
        
    def checkToggleEquip(self):
        if not self.currentlyLoading:
            self.currentlyLoading = True
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