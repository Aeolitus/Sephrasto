# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterEquipment
from PyQt5 import QtWidgets, QtCore, QtGui
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

        self.uiEq.tabWidget.currentChanged.connect(self.reload)
        for i in range(self.uiEq.tabWidget.tabBar().count()):
            self.uiEq.tabWidget.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))
        self.uiEq.tabWidget.setStyleSheet('QTabBar { font-size: ' + str(Wolke.Settings["FontHeadingSize"]) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')

        palette = QtWidgets.QApplication.instance().palette()
        alternateBgStyle = "background-color: " + palette.alternateBase().color().name() + ";"

        self.editRName = []
        self.spinBE = []
        self.spinRS = []
        self.spinZRS = []
        self.spinPunkte = []
        for i in range(3):
            editRName = getattr(self.uiEq, "editR" + str(i+1) + "name")
            editRName.editingFinished.connect(self.updateRuestung)
            self.editRName.append(editRName)

            spinBE = getattr(self.uiEq, "spinR" + str(i+1) + "be")
            spinBE.valueChanged.connect(self.updateRuestung)
            self.spinBE.append(spinBE)

            spinRS = getattr(self.uiEq, "spinR" + str(i+1) + "RS")
            spinRS.valueChanged.connect(self.updateRuestung)
            self.spinRS.append(spinRS)

            self.spinZRS.append([getattr(self.uiEq, "spinR" + str(i+1) + "bein"),
                getattr(self.uiEq, "spinR" + str(i+1) + "larm"),
                getattr(self.uiEq, "spinR" + str(i+1) + "rarm"),
                getattr(self.uiEq, "spinR" + str(i+1) + "bauch"),
                getattr(self.uiEq, "spinR" + str(i+1) + "brust"),
                getattr(self.uiEq, "spinR" + str(i+1) + "kopf")])
            for spin in self.spinZRS[-1]:
                spin.valueChanged.connect(self.updateRuestung)

            self.spinPunkte.append(getattr(self.uiEq, "spinR" + str(i+1) + "punkte"))

            addR = getattr(self.uiEq, "addR" + str(i+1))
            addR.setFont(QtGui.QFont("Font Awesome 6 Free Solid", 9, QtGui.QFont.Black))
            addR.setText('\u002b')
            addR.setMaximumSize(QtCore.QSize(20, 20))
            addR.clicked.connect(lambda state, idx=i: self.selectArmor(idx))

        self.editWName = []
        self.spinW6 = []
        self.spinPlus = []
        self.spinRW = []
        self.spinWM = []
        self.spinLZ = []
        self.spinHaerte = []
        self.editEig = []
        self.eigenschaftenCompleter = []
        self.comboStil = []
        self.labelWerte = []
        self.waffenTypen = []

        
        for i in range(8):
            self.waffenTypen.append("")

            editWName = getattr(self.uiEq, "editW" + str(i+1) + "name")
            editWName.editingFinished.connect(self.updateWaffen)
            self.editWName.append(editWName)

            spinW6 = getattr(self.uiEq, "spinW" + str(i+1) + "w6")
            spinW6.valueChanged.connect(self.updateWaffen)
            self.spinW6.append(spinW6)

            spinPlus = getattr(self.uiEq, "spinW" + str(i+1) + "plus")
            spinPlus.valueChanged.connect(self.updateWaffen)
            self.spinPlus.append(spinPlus)

            spinRW = getattr(self.uiEq, "spinW" + str(i+1) + "rw")
            spinRW.valueChanged.connect(self.updateWaffen)
            self.spinRW.append(spinRW)

            spinWM = getattr(self.uiEq, "spinW" + str(i+1) + "wm")
            spinWM.valueChanged.connect(self.updateWaffen)
            self.spinWM.append(spinWM)

            spinLZ = getattr(self.uiEq, "spinW" + str(i+1) + "lz")
            spinLZ.valueChanged.connect(self.updateWaffen)
            self.spinLZ.append(spinLZ)

            spinHaerte = getattr(self.uiEq, "spinW" + str(i+1) + "h")
            spinHaerte.valueChanged.connect(self.updateWaffen)
            self.spinHaerte.append(spinHaerte)

            editEig = getattr(self.uiEq, "editW" + str(i+1) + "eig")
            editEig.editingFinished.connect(self.updateWaffen)
            self.editEig.append(editEig)
            eigenschaftenCompleter = TextTagCompleter(editEig, Wolke.DB.waffeneigenschaften.keys())
            self.eigenschaftenCompleter.append(eigenschaftenCompleter)

            comboStil = getattr(self.uiEq, "comboStil" + str(i+1))
            comboStil.currentIndexChanged.connect(self.updateWaffen)
            self.comboStil.append(comboStil)

            addW = getattr(self.uiEq, "addW" + str(i+1))
            addW.setFont(QtGui.QFont("Font Awesome 6 Free Solid", 9, QtGui.QFont.Black))
            addW.setText('\u002b')
            addW.setMaximumSize(QtCore.QSize(20, 20))
            addW.clicked.connect(lambda state, idx=i: self.selectWeapon(idx))

            color = Wolke.BorderColor
            labelWerte = getattr(self.uiEq, "labelW" + str(i+1))
            style = "border-left: 1px solid " + color + ";"\
                "border-right: 1px solid " + color + ";"\
                "border-bottom: 1px solid " + color + ";"\
                "border-bottom-left-radius : 0px;"\
                "border-bottom-right-radius : 0px;"
            labelWerte.setStyleSheet(style)
            self.labelWerte.append(labelWerte)

            labelTopFrame = getattr(self.uiEq, "labelW" + str(i+1) + "TopFrame")
            style = "border-left: 1px solid " + color + ";"\
                "border-right: 1px solid " + color + ";"\
                "border-top: 1px solid " + color + ";"\
                "border-top-left-radius : 0px;"\
                "border-top-right-radius : 0px;"
            labelTopFrame.setStyleSheet(style)

            labelLeftFrame = getattr(self.uiEq, "labelW" + str(i+1) + "LeftFrame")
            style = "border-left: 1px solid " + color + "; border-top-left-radius : 0px;"
            labelLeftFrame.setStyleSheet(style)

            labelRightFrame = getattr(self.uiEq, "labelW" + str(i+1) + "RightFrame")
            style = "border-right: 1px solid " + color + "; border-top-right-radius : 0px;"
            labelRightFrame.setStyleSheet(style)

        logging.debug("Check Toggle...")
        self.uiEq.checkZonen.setChecked(Wolke.Char.zonenSystemNutzen)
        self.uiEq.checkZonen.stateChanged.connect(self.refreshZRSVisibility)

        self.inventoryLines = []
        for i in range(0,20):
            lineEdit = getattr(self.uiEq, "lineEdit_"+ str(i+1))
            lineEdit.editingFinished.connect(self.updateInventory)
            self.inventoryLines.append(lineEdit)

            if i in [2, 3, 6, 7, 10, 11, 14, 15, 18, 19]:
                lineEdit.setStyleSheet(alternateBgStyle)

        self.currentlyLoading = False
        
        self.refreshZRSVisibility()

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
            self.modified.emit()

    def updateWeaponStats(self):
        vtVerboten = Wolke.DB.einstellungen["Waffen: Talente VT verboten"].toTextList()
        for index in range(8):
            if index >= len(Wolke.Char.waffen) or not Wolke.Char.waffen[index].name:
                self.labelWerte[index].setText("-")
                continue
            ww = Wolke.Char.waffenwerte[index]
            waffe = Wolke.Char.waffen[index]
            vt = ww.VT
            if waffe.name in vtVerboten or waffe.talent in vtVerboten:
                vt = "-"
            self.labelWerte[index].setText("<b>Typ</b> " + self.waffenTypen[index] + " | <b>Kampfwerte</b> AT* " + str(ww.AT) + ", VT* " + str(vt) + ", TP* " + str(ww.TPW6) + "W6" + ("+" if ww.TPPlus >= 0 else "") + str(ww.TPPlus))

    def refreshDerivedWeaponValues(self, W, index):
        # Waffen Typ
        self.waffenTypen[index] = W.name

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
            tooltip = tooltip[:-1].replace("\n", "<br>")
        self.editEig[index].setToolTip(tooltip)

        # Kampfstil combobox
        comboStil = self.comboStil[index]
        comboStil.blockSignals(True)
        comboStil.setCurrentIndex(0)
        comboStil.clear()
        comboStil.setToolTip(None)
        name = self.waffenTypen[index] or self.editWName[index].text()
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
            if self.waffenTypen[index] and not anzeigename:
                self.currentlyLoading = True
                self.loadWeaponIntoFields(Objekte.Nahkampfwaffe(), index)
                self.currentlyLoading = False

            # Load weapon if an existing weapons name is entered into displayname of an empty row
            name = self.waffenTypen[index]
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
            W.name = self.waffenTypen[index]
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

            waffenHaerteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].toTextList()
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
            self.modified.emit()
            self.updateWeaponStats()

    def load(self):
        self.reload(self.uiEq.tabWidget.currentIndex())

    def reload(self, idx):
        self.currentlyLoading = True

        if idx == 0:
            # Load in Weapons
            for index in range(len(Wolke.Char.waffen)):
                W = Wolke.Char.waffen[index]
                if index < 8:
                    self.loadWeaponIntoFields(W, index)

            self.updateWeaponStats()
        elif idx == 1:
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

    def update(self):
        if self.currentlyLoading:
            return
        self.updateWaffen()
        self.updateRuestung()
        self.updateInventory()

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

        self.waffenTypen[index] = W.name

        self.editEig[index].setText(", ".join(W.eigenschaften))
        self.spinW6[index].setValue(W.W6)
        self.spinPlus[index].setValue(W.plus)
        waffenHaerteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].toTextList()
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
        if self.waffenTypen[index] in Wolke.DB.waffen:
            W = Wolke.DB.waffen[self.waffenTypen[index]].name
        logging.debug("Starting WaffenPicker")
        picker = WaffenPicker(W)
        logging.debug("WaffenPicker created")
        if picker.waffe is not None:
            self.currentlyLoading = True
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