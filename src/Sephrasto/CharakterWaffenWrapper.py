# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterWaffen
from PySide6 import QtWidgets, QtCore, QtGui
import Objekte
import Definitionen
from CharakterWaffenPickerWrapper import WaffenPicker
import logging
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
import re
from TextTagCompleter import TextTagCompleter
import copy

class CharakterWaffenWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing WaffenWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterWaffen.Ui_formWaffen()
        self.ui.setupUi(self.form)
        logging.debug("UI Setup...")

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
        self.addW = []
        
        for i in range(8):
            self.waffenTypen.append("")

            editWName = getattr(self.ui, "editW" + str(i+1) + "name")
            editWName.editingFinished.connect(self.updateWaffen)
            editWName.setEnabled(False)
            self.editWName.append(editWName)

            spinW6 = getattr(self.ui, "spinW" + str(i+1) + "w6")
            spinW6.valueChanged.connect(self.updateWaffen)
            spinW6.setEnabled(False)
            self.spinW6.append(spinW6)

            spinPlus = getattr(self.ui, "spinW" + str(i+1) + "plus")
            spinPlus.valueChanged.connect(self.updateWaffen)
            spinPlus.setEnabled(False)
            self.spinPlus.append(spinPlus)

            spinRW = getattr(self.ui, "spinW" + str(i+1) + "rw")
            spinRW.valueChanged.connect(self.updateWaffen)
            spinRW.setEnabled(False)
            self.spinRW.append(spinRW)

            spinWM = getattr(self.ui, "spinW" + str(i+1) + "wm")
            spinWM.valueChanged.connect(self.updateWaffen)
            spinWM.setEnabled(False)
            self.spinWM.append(spinWM)

            spinLZ = getattr(self.ui, "spinW" + str(i+1) + "lz")
            spinLZ.valueChanged.connect(self.updateWaffen)
            spinLZ.setEnabled(False)
            self.spinLZ.append(spinLZ)

            spinHaerte = getattr(self.ui, "spinW" + str(i+1) + "h")
            spinHaerte.valueChanged.connect(self.updateWaffen)
            spinHaerte.setEnabled(False)
            self.spinHaerte.append(spinHaerte)

            editEig = getattr(self.ui, "editW" + str(i+1) + "eig")
            editEig.editingFinished.connect(self.updateWaffen)
            editEig.setEnabled(False)
            self.editEig.append(editEig)
            eigenschaftenCompleter = TextTagCompleter(editEig, Wolke.DB.waffeneigenschaften.keys())
            self.eigenschaftenCompleter.append(eigenschaftenCompleter)

            comboStil = getattr(self.ui, "comboStil" + str(i+1))
            comboStil.currentIndexChanged.connect(self.updateWaffen)
            comboStil.setEnabled(False)
            self.comboStil.append(comboStil)

            addW = getattr(self.ui, "addW" + str(i+1))
            addW.setText('\u002b')
            addW.setMaximumSize(QtCore.QSize(20, 20))
            addW.clicked.connect(lambda qtNeedsThis=False, idx=i: self.selectWeapon(idx))
            self.addW.append(addW)

            if i > 0:
                upW = getattr(self.ui, "buttonW" + str(i+1) + "Up")
                upW.setText('\uf106')
                upW.setMaximumSize(QtCore.QSize(20, 10))
                upW.clicked.connect(lambda qtNeedsThis=False, idx=i: self.moveWeapon(idx, -1))
            if i < 7:
                downW = getattr(self.ui, "buttonW" + str(i+1) + "Down")
                downW.setText('\uf078')
                downW.setMaximumSize(QtCore.QSize(20, 10))
                downW.clicked.connect(lambda qtNeedsThis=False, idx=i: self.moveWeapon(idx, +1))

            color = Wolke.BorderColor
            labelWerte = getattr(self.ui, "labelW" + str(i+1))
            style = "border-left: 1px solid " + color + ";"\
                "border-right: 1px solid " + color + ";"\
                "border-bottom: 1px solid " + color + ";"\
                "border-bottom-left-radius : 0px;"\
                "border-bottom-right-radius : 0px;"
            labelWerte.setStyleSheet(style)
            labelWerte.setToolTip(f"""<p style='white-space:pre'><span style='{Wolke.FontAwesomeCSS}'>\uf0c1</span>  Waffentyp, unabhängig vom selbst gewählten Namen
<span style='{Wolke.FontAwesomeCSS}'>\uf00b</span>   Kampfwerte inklusive BE
<span style='{Wolke.FontAwesomeCSS}'>\uf6e3</span>   Werteveränderungen</p>""")
            self.labelWerte.append(labelWerte)

            labelTopFrame = getattr(self.ui, "labelW" + str(i+1) + "TopFrame")
            style = "border-left: 1px solid " + color + ";"\
                "border-right: 1px solid " + color + ";"\
                "border-top: 1px solid " + color + ";"\
                "border-top-left-radius : 0px;"\
                "border-top-right-radius : 0px;"
            labelTopFrame.setStyleSheet(style)

            labelLeftFrame = getattr(self.ui, "labelW" + str(i+1) + "LeftFrame")
            style = "border-left: 1px solid " + color + "; border-top-left-radius : 0px;"
            labelLeftFrame.setStyleSheet(style)

            labelRightFrame = getattr(self.ui, "labelW" + str(i+1) + "RightFrame")
            style = "border-right: 1px solid " + color + "; border-top-right-radius : 0px;"
            labelRightFrame.setStyleSheet(style)

        self.currentlyLoading = False

    def moveWeapon(self, index, direction):
        self.currentlyLoading = True
        targetIndex = index + direction
        self.loadWeaponIntoFields(Wolke.Char.waffen[targetIndex], index)
        self.loadWeaponIntoFields(Wolke.Char.waffen[index], targetIndex)
        self.currentlyLoading = False
        self.updateWaffen()

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

            verbesserung = []
            if self.waffenTypen[index] in Wolke.DB.waffen:
                dbWaffe = Wolke.DB.waffen[self.waffenTypen[index]]

                w6Diff = waffe.W6 - dbWaffe.W6
                plusDiff = waffe.plus - dbWaffe.plus

                haerteDiff = waffe.haerte - dbWaffe.haerte
                waffenHaerteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].toTextList()
                if dbWaffe.name in waffenHaerteWSStern:
                    haerteDiff = waffe.haerte - Wolke.Char.wsStern
                wmDiff = waffe.wm - dbWaffe.wm
                rwDiff = waffe.rw - dbWaffe.rw
                lzDiff = 0
                if type(waffe) is Objekte.Fernkampfwaffe:
                    lzDiff = waffe.lz - dbWaffe.lz

                eigPlusDiff = list(set(waffe.eigenschaften) - set(dbWaffe.eigenschaften))
                eigMinusDiff = list(set(dbWaffe.eigenschaften) - set(waffe.eigenschaften))

                if w6Diff != 0:
                    verbesserung.append("TP " + ("+" if w6Diff >= 0 else "") + str(w6Diff) + "W6")
                if plusDiff != 0:
                    tmp = ("+" if plusDiff >= 0 else "") + str(plusDiff)
                    if w6Diff != 0:
                        verbesserung[0] += tmp
                    else:
                        verbesserung.append("TP " + tmp)
                if rwDiff != 0:
                    verbesserung.append("RW " + ("+" if rwDiff >= 0 else "") + str(rwDiff))
                if wmDiff != 0:
                    verbesserung.append("WM " + ("+" if wmDiff >= 0 else "") + str(wmDiff))
                if lzDiff != 0:
                    verbesserung.append("LZ " + ("+" if lzDiff >= 0 else "") + str(lzDiff))
                if haerteDiff != 0:
                    verbesserung.append("Härte " + ("+" if haerteDiff >= 0 else "") + str(haerteDiff))
                if len(eigPlusDiff) > 0:
                    verbesserung.append("Eigenschaften +" + ", +".join(eigPlusDiff))
                if len(eigMinusDiff) > 0:
                    if len(eigPlusDiff) > 0:
                        verbesserung.append("-" + ", -".join(eigMinusDiff))
                    else:
                        verbesserung.append("Eigenschaften -" + ", -".join(eigMinusDiff))
            verbesserung = ', '.join(verbesserung).replace(", Eigenschaften", "; Eigenschaften")

            text = f"""<span style='{Wolke.FontAwesomeCSS}'>\uf0c1</span>&nbsp;&nbsp;{self.waffenTypen[index]}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span style='{Wolke.FontAwesomeCSS}'>\uf00b</span>&nbsp;&nbsp;AT* {ww.AT}, VT* {vt}, TP* {ww.TPW6}W6{"+" if ww.TPPlus >= 0 else ""}{ww.TPPlus}"""
            if len(verbesserung) > 0:
                text += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='{Wolke.FontAwesomeCSS}'>\uf6e3</span>&nbsp;&nbsp;{verbesserung}"
            self.labelWerte[index].setText(text)

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
        comboStil.setEnabled(comboStil.count() > 1)
        comboStil.blockSignals(False)
        
    def createWaffe(self, index):
        name = self.waffenTypen[index]
        anzeigename = self.editWName[index].text()
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
        return W

    def updateWaffen(self):
        if self.currentlyLoading:
            return
        changed = False

        waffenNeu = []
        for index in range(8):
            W = self.createWaffe(index)
            waffenNeu.append(W)
            self.refreshDerivedWeaponValues(W, index)
            
        if not Hilfsmethoden.ArrayEqual(waffenNeu, Wolke.Char.waffen):
            Wolke.Char.waffen = waffenNeu
            changed = True

        if changed:
            self.modified.emit()
            self.updateWeaponStats()

    def load(self):
        self.currentlyLoading = True

        aktualisieren = False
        if len(Wolke.Char.waffen) == 0 and "Hand" in Wolke.DB.waffen:
            Wolke.Char.waffen.append(copy.copy(Wolke.DB.waffen["Hand"]))
            aktualisieren = True
        while len(Wolke.Char.waffen) < 8:
            aktualisieren = True
            Wolke.Char.waffen.append(Objekte.Nahkampfwaffe())
        if aktualisieren:
            Wolke.Char.aktualisieren()

        for index in range(len(Wolke.Char.waffen)):
            W = Wolke.Char.waffen[index]
            if index < 8:
                self.loadWeaponIntoFields(W, index)

        self.updateWeaponStats()
   
        self.currentlyLoading = False

    def loadWeaponIntoFields(self, W, index):
        self.editWName[index].setText(W.anzeigename or W.name)

        self.waffenTypen[index] = W.name

        self.editEig[index].setText(", ".join(W.eigenschaften))
        self.spinW6[index].setValue(W.W6)
        self.spinPlus[index].setValue(W.plus)
        waffenHaerteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].toTextList()
        if W.name in waffenHaerteWSStern:
            W.haerte = Wolke.Char.wsStern
            self.spinHaerte[index].setEnabled(False)
        else:
            self.spinHaerte[index].setEnabled(True)
        self.spinHaerte[index].setValue(W.haerte)
        self.spinRW[index].setValue(W.rw)
        self.spinWM[index].setValue(W.wm)

        if type(W) == Objekte.Fernkampfwaffe:
            self.spinLZ[index].setValue(W.lz)
            self.spinLZ[index].setEnabled(True)
        elif type(W) == Objekte.Nahkampfwaffe:
            self.spinLZ[index].setEnabled(False)
        
        self.refreshDerivedWeaponValues(W, index)

        isEmpty = W == Objekte.Nahkampfwaffe()
        self.editWName[index].setEnabled(not isEmpty)
        self.editEig[index].setEnabled(not isEmpty)
        self.spinW6[index].setEnabled(not isEmpty)
        self.spinPlus[index].setEnabled(not isEmpty)
        self.spinRW[index].setEnabled(not isEmpty)
        self.spinWM[index].setEnabled(not isEmpty)
        self.comboStil[index].setEnabled(not isEmpty and self.comboStil[index].count() > 1)
        if isEmpty:
            self.spinHaerte[index].setEnabled(False)
            self.addW[index].setText('\u002b')
        else:
            self.addW[index].setText('\uf2ed')

    def selectWeapon(self, index):
        if Wolke.Char.waffen[index] == Objekte.Nahkampfwaffe():
            W = None
            if self.waffenTypen[index] in Wolke.DB.waffen:
                W = Wolke.DB.waffen[self.waffenTypen[index]].name
            logging.debug("Starting WaffenPicker")
            pickerClass = EventBus.applyFilter("class_waffenpicker_wrapper", WaffenPicker)
            picker = pickerClass(W)
            logging.debug("WaffenPicker created")
            if picker.waffe is not None:
                self.currentlyLoading = True
                self.loadWeaponIntoFields(picker.waffe, index)
                self.currentlyLoading = False
                self.updateWaffen()
        else:
            self.currentlyLoading = True
            self.loadWeaponIntoFields(Objekte.Nahkampfwaffe(), index)
            self.currentlyLoading = False
            self.updateWaffen()