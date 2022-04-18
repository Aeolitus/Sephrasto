# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterInventar
from PyQt5 import QtWidgets, QtCore, QtGui
import Objekte
import Definitionen
from CharakterRuestungPickerWrapper import RuestungPicker
import logging
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
import re
from TextTagCompleter import TextTagCompleter
import copy

class CharakterInventarWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing InventarWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterInventar.Ui_formInventar()
        self.ui.setupUi(self.form)
        logging.debug("UI Setup...")

        palette = QtWidgets.QApplication.instance().palette()
        alternateBgStyle = "background-color: " + palette.alternateBase().color().name() + ";"

        self.editRName = []
        self.spinBE = []
        self.spinRS = []
        self.spinZRS = []
        self.spinPunkte = []
        for i in range(3):
            editRName = getattr(self.ui, "editR" + str(i+1) + "name")
            editRName.editingFinished.connect(self.updateRuestungen)
            self.editRName.append(editRName)

            spinBE = getattr(self.ui, "spinR" + str(i+1) + "be")
            spinBE.valueChanged.connect(self.updateRuestungen)
            self.spinBE.append(spinBE)

            spinRS = getattr(self.ui, "spinR" + str(i+1) + "RS")
            spinRS.valueChanged.connect(self.updateRuestungen)
            self.spinRS.append(spinRS)

            self.spinZRS.append([getattr(self.ui, "spinR" + str(i+1) + "bein"),
                getattr(self.ui, "spinR" + str(i+1) + "larm"),
                getattr(self.ui, "spinR" + str(i+1) + "rarm"),
                getattr(self.ui, "spinR" + str(i+1) + "bauch"),
                getattr(self.ui, "spinR" + str(i+1) + "brust"),
                getattr(self.ui, "spinR" + str(i+1) + "kopf")])
            for spin in self.spinZRS[-1]:
                spin.valueChanged.connect(self.updateRuestungen)

            self.spinPunkte.append(getattr(self.ui, "spinR" + str(i+1) + "punkte"))

            addR = getattr(self.ui, "addR" + str(i+1))
            addR.setFont(QtGui.QFont("Font Awesome 6 Free Solid", 9, QtGui.QFont.Black))
            addR.setText('\u002b')
            addR.setMaximumSize(QtCore.QSize(20, 20))
            addR.clicked.connect(lambda state, idx=i: self.selectArmor(idx))

        logging.debug("Check Toggle...")
        self.ui.checkZonen.setChecked(Wolke.Char.zonenSystemNutzen)
        self.ui.checkZonen.stateChanged.connect(self.refreshZRSVisibility)

        self.inventoryLines = []
        for i in range(0,20):
            lineEdit = getattr(self.ui, "lineEdit_"+ str(i+1))
            lineEdit.editingFinished.connect(self.updateInventory)
            self.inventoryLines.append(lineEdit)

            if i in [2, 3, 6, 7, 10, 11, 14, 15, 18, 19]:
                lineEdit.setStyleSheet(alternateBgStyle)

        self.currentlyLoading = False
        
        self.refreshZRSVisibility()

    def refreshDerivedArmorValues(self, R, index):
        if self.ui.checkZonen.isChecked():
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

    def createRuestung(self, index):
        R = Objekte.Ruestung() 
        R.name = self.editRName[index].text()
        R.be = int(self.spinBE[index].value())
        if self.ui.checkZonen.isChecked():
            for i in range(0, 6):
                R.rs[i] = self.spinZRS[index][i].value()
        else:
            R.rs = 6*[self.spinRS[index].value()]
        return R

    def updateRuestungen(self):
        if self.currentlyLoading:
            return
        changed = False

        ruestungNeu = []
        for index in range(3):
            R = self.createRuestung(index)
            ruestungNeu.append(R)
            self.refreshDerivedArmorValues(R, index)

        if not Hilfsmethoden.ArrayEqual(ruestungNeu, Wolke.Char.rüstung):
            changed = True
            Wolke.Char.rüstung = ruestungNeu

        if Wolke.Char.zonenSystemNutzen != self.ui.checkZonen.isChecked():
            Wolke.Char.zonenSystemNutzen = self.ui.checkZonen.isChecked()
            changed = True

        if changed:
            self.modified.emit()

    def load(self):
        self.currentlyLoading = True

        # Load in Armor
        for index in range(len(Wolke.Char.rüstung)):
            R = Wolke.Char.rüstung[index]
            if index < 3:
                self.loadArmorIntoFields(R, index, True)

        # Load in inventory
        count = 0
        for el in Wolke.Char.ausrüstung:
            self.inventoryLines[count].setText(el)
            count += 1
            if count >= 20:
                break

        self.currentlyLoading = False

    def updateInventory(self):
        # Update inventory
        ausruestungNeu = []
        for i in range(0,20):
            ausruestungNeu.append(self.inventoryLines[i].text())

        #Preserve the position of actual elements but remove any trailing empty elements
        #This is needed for ArrayEqual later to work as intended
        for ausr in reversed(ausruestungNeu):
            if ausr == "":
                ausruestungNeu.pop()
            else:
                break

        if not Hilfsmethoden.ArrayEqual(ausruestungNeu, Wolke.Char.ausrüstung):
            Wolke.Char.ausrüstung = ausruestungNeu
            self.modified.emit()

    def loadArmorIntoFields(self, R, index, replace):
        if replace or self.editRName[index].text() == "":
            self.editRName[index].setText(R.name)
        else:
            self.editRName[index].setText(self.editRName[index].text() + ", " + R.name)

        if not replace:
            for i in range(0, 6):
                R.rs[i] += self.spinZRS[index][i].value()
            beDelta = self.spinBE[index].value() - self.spinRS[index].value()
            R.be = R.getRSGesamtInt() + beDelta

        for i in range(0, 6):
            if self.ui.checkZonen.isChecked():
                self.spinZRS[index][i].setValue(R.rs[i])
            else:
                self.spinZRS[index][i].setValue(R.getRSGesamtInt())

        self.spinBE[index].setValue(EventBus.applyFilter("ruestung_be", R.be, { "name" : R.name }))
        self.spinRS[index].setValue(R.getRSGesamtInt())

        self.refreshDerivedArmorValues(R, index)

    def selectArmor(self, index):
        logging.debug("Starting RuestungPicker")

        pickerClass = EventBus.applyFilter("class_ruestungspicker_wrapper", RuestungPicker)
        picker = pickerClass(self.editRName[index].text(), 2 if self.ui.checkZonen.isChecked() else 1)
        logging.debug("RuestungPicker created")
        if picker.ruestung is not None:
            self.currentlyLoading = True
            self.loadArmorIntoFields(picker.ruestung, index, picker.ruestungErsetzen)
            self.currentlyLoading = False
            self.updateRuestungen()

    def refreshZRSVisibility(self):
        if self.currentlyLoading:
            return
        self.currentlyLoading = True
        labels = [self.ui.labelBein, self.ui.labelBauch, self.ui.labelBrust, self.ui.labelLarm, self.ui.labelRarm, self.ui.labelKopf, self.ui.labelPunkte]

        if self.ui.checkZonen.isChecked():
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