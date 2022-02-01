# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterEquipment
from PyQt5 import QtWidgets, QtCore
import Objekte
import Definitionen
from WaffenPicker import WaffenPicker
from RuestungPicker import RuestungPicker
import logging
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
import re
from EventBus import EventBus
from TextTagCompleter import TextTagCompleter

class EquipWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing EquipWrapper...")
        self.formEq = QtWidgets.QWidget()
        self.uiEq = UI.CharakterEquipment.Ui_formAusruestung()
        self.uiEq.setupUi(self.formEq)
        logging.debug("UI Setup...")
       
        self.editRName = []
        self.spinBE = []
        self.spinRS = []
        self.spinZRS = []
        self.spinPunkte = []
        for el in ["R1", "R2", "R3"]:
            editRName = getattr(self.uiEq, "edit" + el + "name")
            editRName.editingFinished.connect(self.updateRuestung)
            self.editRName.append(editRName)

            spinBE = getattr(self.uiEq, "spin" + el + "be")
            spinBE.valueChanged.connect(self.updateRuestung)
            self.spinBE.append(spinBE)

            spinRS = getattr(self.uiEq, "spin" + el + "RS")
            spinRS.valueChanged.connect(self.updateRuestung)
            self.spinRS.append(spinRS)

            self.spinZRS.append([getattr(self.uiEq, "spin" + el + "bein"),
                getattr(self.uiEq, "spin" + el + "larm"),
                getattr(self.uiEq, "spin" + el + "rarm"),
                getattr(self.uiEq, "spin" + el + "bauch"),
                getattr(self.uiEq, "spin" + el + "brust"),
                getattr(self.uiEq, "spin" + el + "kopf")])
            for spin in self.spinZRS[-1]:
                spin.valueChanged.connect(self.updateRuestung)

            self.spinPunkte.append(getattr(self.uiEq, "spin" + el + "punkte"))

            addR = getattr(self.uiEq, "add" + el)
            addR.clicked.connect(lambda state, idx=int(el[-1])-1: self.selectArmor(idx))

        self.editWName = []
        self.labelTyp = []
        self.spinW6 = []
        self.spinPlus = []
        self.spinRW = []
        self.spinWM = []
        self.spinLZ = []
        self.spinHaerte = []
        self.editEig = []
        self.eigenschaftenCompleter = []
        self.comboStil = []
        
        for el in ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8']:
            editWName = getattr(self.uiEq, "edit" + el + "name")
            editWName.editingFinished.connect(self.updateWaffen)
            self.editWName.append(editWName)

            self.labelTyp.append(getattr(self.uiEq, "label" + el + "typ"))

            spinW6 = getattr(self.uiEq, "spin" + el + "w6")
            spinBE.valueChanged.connect(self.updateWaffen)
            self.spinW6.append(spinW6)

            spinPlus = getattr(self.uiEq, "spin" + el + "plus")
            spinPlus.valueChanged.connect(self.updateWaffen)
            self.spinPlus.append(spinPlus)

            spinRW = getattr(self.uiEq, "spin" + el + "rw")
            spinRW.valueChanged.connect(self.updateWaffen)
            self.spinRW.append(spinRW)

            spinWM = getattr(self.uiEq, "spin" + el + "wm")
            spinWM.valueChanged.connect(self.updateWaffen)
            self.spinWM.append(spinWM)

            spinLZ = getattr(self.uiEq, "spin" + el + "lz")
            spinLZ.valueChanged.connect(self.updateWaffen)
            self.spinLZ.append(spinLZ)

            spinHaerte = getattr(self.uiEq, "spin" + el + "h")
            spinHaerte.valueChanged.connect(self.updateWaffen)
            self.spinHaerte.append(spinHaerte)

            editEig = getattr(self.uiEq, "edit" + el + "eig")
            editEig.editingFinished.connect(self.updateWaffen)
            self.editEig.append(editEig)
            eigenschaftenCompleter = TextTagCompleter(editEig, Wolke.DB.waffeneigenschaften.keys())
            self.eigenschaftenCompleter.append(eigenschaftenCompleter)

            comboStil = getattr(self.uiEq, "comboStil" + el[-1])
            comboStil.currentIndexChanged.connect(self.updateWaffen)
            self.comboStil.append(comboStil)

            addW = getattr(self.uiEq, "add" + el)
            addW.clicked.connect(lambda state, idx=int(el[-1])-1: self.selectWeapon(idx))

        logging.debug("Check Toggle...")
        self.uiEq.checkZonen.setChecked(Wolke.Char.zonenSystemNutzen)
        self.uiEq.checkZonen.stateChanged.connect(self.refreshZRSVisibility)

        self.currentlyLoading = False
        
        self.refreshZRSVisibility()
        self.load()

    def refreshDerivedArmorValues(self, R, index):
        if self.uiEq.checkZonen.isChecked():
            self.spinRS[index].blockSignals(True)
            self.spinRS[index].setValue(R.getRSGesamtInt())
            self.spinRS[index].blockSignals(False)
        else:
            for i in range(0, 6):
               self.spinZRS[index][i].blockSignals(True)
               self.spinZRS[index][i].setValue(R.getRSGesamtInt())
               self.spinZRS[index][i].blockSignals(False)

        spinPunkte = self.spinPunkte[index]
        if sum(R.rs) % 6 != 0:
            spinPunkte.setStyleSheet("border: 1px solid orange;")
            missingPoints = 6 - sum(R.rs) % 6
            if missingPoints == 1:
                spinPunkte.setToolTip("Der Rüstung fehlt " + str(missingPoints) + " Punkt ZRS.")
            else:
                spinPunkte.setToolTip("Der Rüstung fehlen " + str(missingPoints) + " Punkte ZRS.")
        else:
            spinPunkte.setStyleSheet("")
            spinPunkte.setToolTip("")

        spinPunkte.setValue(sum(R.rs))

    def updateRuestung(self):
        if self.currentlyLoading:
            return
        changed = False

        ruestungNeu = []
        for index in range(3):
            R = Objekte.Ruestung() 
            R.name = self.editRName[index].text()
            R.be = int(self.spinBE[index].value())
            if self.uiEq.checkZonen.isChecked():
                for i in range(0, 6):
                    R.rs[i] = self.spinZRS[index][i].value()
            else:
                R.rs = 6*[self.spinRS[index].value()]
            ruestungNeu.append(R)
            self.refreshDerivedArmorValues(R, index)

        if not Hilfsmethoden.ArrayEqual(ruestungNeu, Wolke.Char.rüstung):
            changed = True
            Wolke.Char.rüstung = ruestungNeu

        if Wolke.Char.zonenSystemNutzen != self.uiEq.checkZonen.isChecked():
            Wolke.Char.zonenSystemNutzen = self.uiEq.checkZonen.isChecked()
            changed = True

        if changed:
            Wolke.Char.aktualisieren()
            self.modified.emit()

    def refreshDerivedWeaponValues(self, W, index):
        # Waffen Typ
        if W.name != self.labelTyp[index].text():
            self.labelTyp[index].setText(W.name)

        # Waffeneigenschaften tooltip
        tooltip = ""
        for we in W.eigenschaften:
            name = re.sub(r"\((.*?)\)", "", we, re.UNICODE).strip() # remove parameters
            if name in Wolke.DB.waffeneigenschaften:
                waffeneigenschaft = Wolke.DB.waffeneigenschaften[name]
                if waffeneigenschaft.text:
                    tooltip += "<b>" + we + ":</b> " + waffeneigenschaft.text + "\n"
            else:
                tooltip += "<b>" + we + ":</b> Unbekannte Eigenschaft\n"
        
        if tooltip:
            tooltip = "<html><head/><body><div>" + tooltip[:-1].replace("\n", "<br>") + "</div></body></html>"
        self.editEig[index].setToolTip(tooltip)

        # Kampfstil combobox
        comboStil = self.comboStil[index]
        comboStil.blockSignals(True)
        comboStil.setCurrentIndex(0)
        comboStil.clear()
        comboStil.setToolTip(None)
        name = self.labelTyp[index].text() or self.editWName[index].text()
        if name:
            if name in Wolke.DB.waffen:
                entries = [Definitionen.KeinKampfstil] + [ks for ks in Wolke.DB.waffen[name].kampfstile if ks + " I" in Wolke.Char.vorteile]
                comboStil.addItems(entries)
                if W.kampfstil in entries:
                    comboStil.setCurrentIndex(entries.index(W.kampfstil))
            else:
                comboStil.addItem('Waffe unbekannt')
                comboStil.setToolTip('Der Name der Waffe ist unbekannt, daher kann kein Kampfstil ausgewählt werden. Die Kampfwerte müssen in der PDF manuell ausgefüllt werden.')
        comboStil.blockSignals(False)
        
    def updateWaffen(self):
        if self.currentlyLoading:
            return
        changed = False

        waffenNeu = []
        for index in range(8):
            # Remove weapon if display name is deleted
            anzeigename = self.editWName[index].text()
            if self.labelTyp[index].text() and not anzeigename:
                self.currentlyLoading = True
                self.loadWeaponIntoFields(Objekte.Nahkampfwaffe(), index)
                self.currentlyLoading = False

            # Load weapon if an existing weapons name is entered into displayname of an empty row
            name = self.labelTyp[index].text()
            if not name and anzeigename in Wolke.DB.waffen:
                self.currentlyLoading = True
                self.loadWeaponIntoFields(Wolke.DB.waffen[anzeigename], index)
                self.currentlyLoading = False
                name = anzeigename

            # Create
            if (not name in Wolke.DB.waffen) or type(Wolke.DB.waffen[name]) != Objekte.Fernkampfwaffe:
                W = Objekte.Nahkampfwaffe()
            else:
                W = Objekte.Fernkampfwaffe()
                W.lz = self.spinLZ[index].value()

            W.anzeigename = anzeigename
            W.name = name
            if W.name in Wolke.DB.waffen:
                dbWaffe = Wolke.DB.waffen[W.name]
                W.fertigkeit = dbWaffe.fertigkeit
                W.talent = dbWaffe.talent
                W.kampfstile = dbWaffe.kampfstile.copy()
            W.wm = self.spinWM[index].value()
            W.rw = self.spinRW[index].value()
            W.W6 = self.spinW6[index].value()
            W.plus = self.spinPlus[index].value()

            self.editEig[index].setText(self.editEig[index].text().strip().rstrip(","))
            if self.editEig[index].text().strip():
                W.eigenschaften = list(map(str.strip, self.editEig[index].text().strip().rstrip(",").split(",")))
            W.kampfstil = self.comboStil[index].currentText()

            waffenHaerteWSStern = Wolke.DB.einstellungen["WaffenHärteWSStern"].toTextList()
            if W.name in waffenHaerteWSStern:
                W.haerte = Wolke.Char.wsStern
            else:
                W.haerte = self.spinHaerte[index].value()

            waffenNeu.append(W)
            self.refreshDerivedWeaponValues(W, index)
            
        if not Hilfsmethoden.ArrayEqual(waffenNeu, Wolke.Char.waffen):
            Wolke.Char.waffen = waffenNeu
            changed = True

        if changed:
            Wolke.Char.aktualisieren()
            self.modified.emit()

    def load(self):
        self.currentlyLoading = True
        # Load in Armor
        for index in range(len(Wolke.Char.rüstung)):
            R = Wolke.Char.rüstung[index]
            if index < 3:
                self.loadArmorIntoFields(R, index, True)

        # Load in Weapons
        for index in range(len(Wolke.Char.waffen)):
            W = Wolke.Char.waffen[index]
            if index < 8:
                self.loadWeaponIntoFields(W, index)

        self.currentlyLoading = False

    def loadArmorIntoFields(self, R, index, replace):
        if replace or self.editRName[index].text() == "":
            self.editRName[index].setText(R.name)
        else:
            self.editRName[index].setText(self.editRName[index].text() + ", " + R.name)

        if not replace:
            for i in range(0, 6):
                R.rs[i] += self.spinZRS[index][i].value()

        for i in range(0, 6):
            if self.uiEq.checkZonen.isChecked():
                self.spinZRS[index][i].setValue(R.rs[i])
            else:
                self.spinZRS[index][i].setValue(R.getRSGesamtInt())

        self.spinBE[index].setValue(EventBus.applyFilter("ruestung_be", R.getRSGesamtInt(), { "name" : R.name }))
        self.spinRS[index].setValue(R.getRSGesamtInt())

        self.refreshDerivedArmorValues(R, index)

    def loadWeaponIntoFields(self, W, index):
        self.editWName[index].setText(W.anzeigename or W.name)
        self.labelTyp[index].setText(W.name)
        self.editEig[index].setText(", ".join(W.eigenschaften))
        self.spinW6[index].setValue(W.W6)
        self.spinPlus[index].setValue(W.plus)
        waffenHaerteWSStern = Wolke.DB.einstellungen["WaffenHärteWSStern"].toTextList()
        if W.name in waffenHaerteWSStern:
            self.spinHaerte[index].setValue(Wolke.Char.wsStern)
            self.spinHaerte[index].setEnabled(False)
        else:
            self.spinHaerte[index].setValue(W.haerte)
            self.spinHaerte[index].setEnabled(True)
        self.spinRW[index].setValue(W.rw)
        self.spinWM[index].setValue(W.wm)

        if type(W) == Objekte.Fernkampfwaffe:
            self.spinLZ[index].setValue(W.lz)
            self.spinLZ[index].setEnabled(True)
        elif type(W) == Objekte.Nahkampfwaffe:
            self.spinLZ[index].setEnabled(False)
        
        self.refreshDerivedWeaponValues(W, index)

    def selectArmor(self, index):
        logging.debug("Starting RuestungPicker")
        picker = RuestungPicker(self.editRName[index].text(), 2 if self.uiEq.checkZonen.isChecked() else 1)
        logging.debug("RuestungPicker created")
        if picker.ruestung is not None:
            self.currentlyLoading = True
            self.loadArmorIntoFields(picker.ruestung, index, picker.ruestungErsetzen)
            self.currentlyLoading = False
            self.updateRuestung()

    def selectWeapon(self, index):
        W = None
        for el in Wolke.DB.waffen:
            if Wolke.DB.waffen[el].name == self.labelTyp[index].text():
                W = el
                logging.debug("Weapon found - its " + self.labelTyp[index].text())
                break
        logging.debug("Starting WaffenPicker")
        picker = WaffenPicker(W)
        logging.debug("WaffenPicker created")
        if picker.waffe is not None:
            self.currentlyLoading = True
            #Wolke.Char.waffen.append(picker.waffe)
            self.loadWeaponIntoFields(picker.waffe, index)
            self.currentlyLoading = False
            self.updateWaffen()

    def refreshZRSVisibility(self):
        if self.currentlyLoading:
            return
        self.currentlyLoading = True
        labels = [self.uiEq.labelBein, self.uiEq.labelBauch, self.uiEq.labelBrust, self.uiEq.labelLarm, self.uiEq.labelRarm, self.uiEq.labelKopf, self.uiEq.labelPunkte]

        if self.uiEq.checkZonen.isChecked():
            for index in range(3):
                for j in range(6):
                    self.spinZRS[index][j].show()
                self.spinPunkte[index].show()
                self.spinRS[index].setEnabled(False)
            for label in labels:
                label.show()
        else:
            for index in range(3):
                for j in range(6):
                    self.spinZRS[index][j].hide()
                self.spinPunkte[index].hide()
                self.spinRS[index].setEnabled(True)
            for label in labels:
                label.hide()

        self.currentlyLoading = False