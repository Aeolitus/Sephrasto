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
import Objekte

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
        self.uiEq.checkW1FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW2FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW3FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW4FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkW5FK.stateChanged.connect(self.checkToggleEquip)
        self.uiEq.checkZonen.stateChanged.connect(self.checkToggleEquip)
        self.checkToggleEquip()
        
        self.ui.tabs.addTab(self.formBeschr, "Beschreibung")
        self.ui.tabs.addTab(self.formAttr, "Attribute")
        self.ui.tabs.addTab(self.formEq, "Waffen und Rüstung")    
        
        self.ui.buttonSave.clicked.connect(self.updateEquipment)
        self.ui.buttonSavePDF.clicked.connect(self.loadEquipment)
        
        
        self.formMain.show()
        
    def updateBeschreibung(self):
        if self.uiBeschr.editName.text() != "":
            self.char.name = self.uiBeschr.editName.text()
        if self.uiBeschr.editRasse.text() != "":
            self.char.rasse = self.uiBeschr.editRasse.text()
        self.char.status = self.uiBeschr.comboStatus.currentIndex()
        self.char.finanzen = self.uiBeschr.comboFinanzen.currentIndex()
        self.char.kurzbeschreibung = self.uiBeschr.editKurzbeschreibung.text()
        self.char.eigenheiten = []
        self.char.eigenheiten.append(self.uiBeschr.editEig1.text())
        self.char.eigenheiten.append(self.uiBeschr.editEig2.text())
        self.char.eigenheiten.append(self.uiBeschr.editEig3.text())
        self.char.eigenheiten.append(self.uiBeschr.editEig4.text())
        self.char.eigenheiten.append(self.uiBeschr.editEig5.text())
        self.char.eigenheiten.append(self.uiBeschr.editEig6.text())
        self.char.eigenheiten.append(self.uiBeschr.editEig7.text())
        self.char.eigenheiten.append(self.uiBeschr.editEig8.text())

    def loadBeschreibung(self):
        self.uiBeschr.editName.setText(self.char.name)
        self.uiBeschr.editRasse.setText(self.char.rasse)
        self.uiBeschr.comboStatus.setCurrentIndex(self.char.status)
        self.uiBeschr.comboFinanzen.setCurrentIndex(self.char.finanzen)
        self.uiBeschr.editKurzbeschreibung.setText(self.char.kurzbeschreibung)
        arr = ["", "", "", "", "", "", "", ""]
        count = 0
        for el in self.char.eigenheiten:
            arr[count] = el
            count += 1
        self.uiBeschr.editEig1.setText(arr[0])
        self.uiBeschr.editEig2.setText(arr[1])
        self.uiBeschr.editEig3.setText(arr[2])
        self.uiBeschr.editEig4.setText(arr[3])
        self.uiBeschr.editEig5.setText(arr[4])
        self.uiBeschr.editEig6.setText(arr[5])
        self.uiBeschr.editEig7.setText(arr[6])
        self.uiBeschr.editEig8.setText(arr[7])
        
    def updateAttribute(self):
        self.char.attribute['KO'].wert = self.uiAttr.spinKO.value()
        self.char.attribute['KO'].aktualisieren()
        self.char.attribute['MU'].wert = self.uiAttr.spinMU.value()
        self.char.attribute['MU'].aktualisieren()
        self.char.attribute['GE'].wert = self.uiAttr.spinGE.value()
        self.char.attribute['GE'].aktualisieren()
        self.char.attribute['KK'].wert = self.uiAttr.spinKK.value()
        self.char.attribute['KK'].aktualisieren()
        self.char.attribute['IN'].wert = self.uiAttr.spinIN.value()
        self.char.attribute['IN'].aktualisieren()
        self.char.attribute['KL'].wert = self.uiAttr.spinKL.value()
        self.char.attribute['KL'].aktualisieren()
        self.char.attribute['CH'].wert = self.uiAttr.spinCH.value()
        self.char.attribute['CH'].aktualisieren()
        self.char.attribute['FF'].wert = self.uiAttr.spinFF.value()
        self.char.attribute['FF'].aktualisieren()
        self.char.asp.wert = self.uiAttr.spinAsP.value()
        self.char.kap.wert = self.uiAttr.spinKaP.value()
        self.char.aktualisieren()
        
    def loadAttribute(self):
        self.char.aktualisieren()
        self.uiAttr.spinKO.setValue(self.char.attribute['KO'].wert)
        self.uiAttr.pwKO.setValue(self.char.attribute['KO'].wert*2)
        self.uiAttr.spinMU.setValue(self.char.attribute['MU'].wert)
        self.uiAttr.pwMU.setValue(self.char.attribute['MU'].wert*2)
        self.uiAttr.spinGE.setValue(self.char.attribute['GE'].wert)
        self.uiAttr.pwGE.setValue(self.char.attribute['GE'].wert*2)
        self.uiAttr.spinKK.setValue(self.char.attribute['KK'].wert)
        self.uiAttr.pwKK.setValue(self.char.attribute['KK'].wert*2)
        self.uiAttr.spinIN.setValue(self.char.attribute['IN'].wert)
        self.uiAttr.pwIN.setValue(self.char.attribute['IN'].wert*2)
        self.uiAttr.spinKL.setValue(self.char.attribute['KL'].wert)
        self.uiAttr.pwKL.setValue(self.char.attribute['KL'].wert*2)
        self.uiAttr.spinCH.setValue(self.char.attribute['CH'].wert)
        self.uiAttr.pwCH.setValue(self.char.attribute['CH'].wert*2)
        self.uiAttr.spinFF.setValue(self.char.attribute['FF'].wert)
        self.uiAttr.pwFF.setValue(self.char.attribute['FF'].wert*2)
        self.uiAttr.abWS.setValue(self.char.ws)
        self.uiAttr.abGS.setValue(self.char.gs)
        self.uiAttr.abIN.setValue(self.char.ini)
        self.uiAttr.abMR.setValue(self.char.mr)
        self.uiAttr.abSB.setValue(self.char.schadensbonus)
        self.uiAttr.spinAsP.setValue(self.char.asp.wert)
        self.uiAttr.spinKaP.setValue(self.char.kap.wert)
        
    def updateEquipment(self):
        self.char.rüstung = []
        if self.uiEq.editR1name.text() != "":
            R = Objekte.Ruestung() 
            R.name = self.uiEq.editR1name.text()
            R.be = int(self.uiEq.spinR1be.value())
            if self.uiEq.checkZonen:
                R.rs = [self.uiEq.spinR1bein.value(), self.uiEq.spinR1larm.value(), self.uiEq.spinR1rarm.value(), self.uiEq.spinR1bauch.value(), self.uiEq.spinR1brust.value(), self.uiEq.spinR1kopf.value()]
            else:
                R.rs = 6*[self.uiEq.spinR1RS]
            self.char.rüstung.append(R)
        if self.uiEq.editR2name.text() != "":
            R = Objekte.Ruestung() 
            R.name = self.uiEq.editR2name.text()
            R.be = self.uiEq.spinR2be.value()
            if self.uiEq.checkZonen:
                R.rs = [self.uiEq.spinR2bein.value(), self.uiEq.spinR2larm.value(), self.uiEq.spinR2rarm.value(), self.uiEq.spinR2bauch.value(), self.uiEq.spinR2brust.value(), self.uiEq.spinR2kopf.value()]
            else:
                R.rs = 6*[self.uiEq.spinR2RS]
            self.char.rüstung.append(R)
            
        self.char.waffen = []
        for el in ['W1', 'W2', 'W3', 'W4', 'W5']:
            if (eval("self.uiEq.edit" + el + "name.text()") != ""):
                W = Objekte.Waffe()
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
                self.char.waffen.append(W)
        self.char.aktualisieren()
        
    def loadEquipment(self):
        Rarr = ["R1", "R2"]
        count = 0
        while count < len(self.char.rüstung):
            R = self.char.rüstung[count]
            eval("self.uiEq.edit" + Rarr[count] + "name.setText(\"" + R.name +"\")")
            eval("self.uiEq.spin" + Rarr[count] + "be.setValue(" + str(R.be) +")")
            eval("self.uiEq.spin" + Rarr[count] + "bein.setValue(" + str(R.rs[0]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "larm.setValue(" + str(R.rs[1]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "rarm.setValue(" + str(R.rs[2]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "bauch.setValue(" + str(R.rs[3]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "brust.setValue(" + str(R.rs[4]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "kopf.setValue(" + str(R.rs[5]) +")")
            eval("self.uiEq.spin" + Rarr[count] + "kopf.setValue(" + str(round(sum(R.rs)/6)) +")")
            count += 1
        Warr = ["W1","W2","W3","W4","W5"]
        count = 0
        while count < len(self.char.waffen):
            W = self.char.waffen[count]
            eval("self.uiEq.edit" + Warr[count] + "name.setText(\""+ W.name +"\")")
            eval("self.uiEq.edit" + Warr[count] + "eig.setText(\""+ W.eigenschaften +"\")")
            eval("self.uiEq.spin" + Warr[count] + "w6.setValue("+ str(W.W6) +")")
            eval("self.uiEq.spin" + Warr[count] + "plus.setValue("+ str(W.plus) +")")
            eval("self.uiEq.spin" + Warr[count] + "h.setValue("+ str(W.haerte) +")")
            if type(W) == Objekte.Fernkampfwaffe:
                eval("self.uiEq.spin" + Warr[count] + "rw.setValue("+ str(W.rwnah) +")")
                eval("self.uiEq.spin" + Warr[count] + "rw2.setValue("+ str(W.rwfern) +")")
                eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.lz) +")")
                eval("self.uiEq.check" + Warr[count] + "FK.setChecked(True)")
            elif type(W) == Objekte.Nahkampfwaffe:
                eval("self.uiEq.spin" + Warr[count] + "rw.setValue("+ str(W.rw) +")")
                eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.wm) +")")
                eval("self.uiEq.check" + Warr[count] + "FK.setChecked(False)")
            count += 1
        
        
        
    def checkToggleEquip(self):
        Warr = ["W1","W2","W3","W4","W5"]
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
        
if __name__ == "__main__":
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    ed = Editor()
    ed.setupMainForm()
    sys.exit(app.exec_())            
    