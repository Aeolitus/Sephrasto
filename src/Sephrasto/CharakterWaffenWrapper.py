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
        self.spinWürfel = []
        self.labelSeiten = []
        self.spinPlus = []
        self.spinRW = []
        self.spinWM = []
        self.spinLZ = []
        self.spinHaerte = []
        self.editEig = []
        self.eigenschaftenCompleter = []
        self.comboStil = []
        self.labelBasis = []
        self.labelWerte = []
        self.labelMods = []
        self.waffenTypen = []
        self.addW = []
        
        for i in range(8):
            self.waffenTypen.append("")

            editWName = getattr(self.ui, "editW" + str(i+1) + "name")
            editWName.editingFinished.connect(self.updateWaffen)
            editWName.setEnabled(False)
            self.editWName.append(editWName)

            spinWürfel = getattr(self.ui, "spinW" + str(i+1) + "w6")
            spinWürfel.valueChanged.connect(self.updateWaffen)
            spinWürfel.setEnabled(False)
            self.spinWürfel.append(spinWürfel)

            labelSeiten = getattr(self.ui, "labelW" + str(i+1) + "seiten")
            self.labelSeiten.append(labelSeiten)

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
            labelContainer = getattr(self.ui, "labelContainerW" + str(i+1))
            style = "border-left: 1px solid " + color + ";"\
                "border-right: 1px solid " + color + ";"\
                "border-bottom: 1px solid " + color + ";"\
                "border-bottom-left-radius : 0px;"\
                "border-bottom-right-radius : 0px;"
            labelContainer.setStyleSheet(style)
            labelBasis = getattr(self.ui, "labelW" + str(i+1) + "Basis")
            labelBasis.setToolTip(f"""<p style='white-space:pre'><span style='{Wolke.FontAwesomeCSS}'>\uf02d</span>  Basiswaffe

Sephrasto leitet von der Basiswaffe das verwendete Talent, die erlaubten Kampfstile und von dir vorgenommene Anpassungen der Waffenwerte ab.
Du kannst deiner Waffe jederzeit einen eigenen Namen geben, die Basiswaffe ändert sich dadurch nicht.</p>""")
            labelBasis.setStyleSheet("border: none;")
            self.labelBasis.append(labelBasis)
            labelWerte = getattr(self.ui, "labelW" + str(i+1) + "Werte")
            labelWerte.setToolTip(f"""<p style='white-space:pre'><span style='{Wolke.FontAwesomeCSS}'>\uf6cf</span>   Kampfwerte

- AT* und VT*: Talent-PW + Waffen-WM + Kampfstilbonus - BE der ersten Rüstung
- TP*: Waffen-TP + Schadensbonus (x2, falls kopflastig) + Kampfstilbonus</p>""")
            labelWerte.setStyleSheet("border: none;")
            self.labelWerte.append(labelWerte)
            labelMods = getattr(self.ui, "labelW" + str(i+1) + "Mods")
            labelMods.setToolTip(f"""<p style='white-space:pre'><span style='{Wolke.FontAwesomeCSS}'>\uf6e3</span>   Anpassungen der Waffenwerte

Üblich sind hier TP +1 und Härte +2 je Stufe Hohe Qualität bei der Fertigung (kein Härtebonus bei Fernkampfwaffen) und WM +1 für persönliche Waffen.</p>""")
            labelMods.setStyleSheet("border: none;")
            self.labelMods.append(labelMods)

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

    def diffWeapons(self, weapon1, weapon2):
        diff = []
        würfelDiff = weapon1.würfel - weapon2.würfel
        plusDiff = weapon1.plus - weapon2.plus

        haerteDiff = weapon1.haerte - weapon2.haerte
        waffenHaerteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].toTextList()
        if weapon2.name in waffenHaerteWSStern:
            haerteDiff = weapon1.haerte - Wolke.Char.wsStern
        wmDiff = weapon1.wm - weapon2.wm
        rwDiff = weapon1.rw - weapon2.rw
        lzDiff = 0
        if type(weapon1) is Objekte.Fernkampfwaffe:
            lzDiff = weapon1.lz - weapon2.lz

        eigPlusDiff = list(set(weapon1.eigenschaften) - set(weapon2.eigenschaften))
        eigMinusDiff = list(set(weapon2.eigenschaften) - set(weapon1.eigenschaften))

        if würfelDiff != 0:
            diff.append("TP " + ("+" if würfelDiff >= 0 else "") + str(würfelDiff) + "W" + str(weapon1.würfelSeiten))
        if plusDiff != 0:
            tmp = ("+" if plusDiff >= 0 else "") + str(plusDiff)
            if würfelDiff != 0:
                diff[0] += tmp
            else:
                diff.append("TP " + tmp)
        if rwDiff != 0:
            diff.append("RW " + ("+" if rwDiff >= 0 else "") + str(rwDiff))
        if wmDiff != 0:
            diff.append("WM " + ("+" if wmDiff >= 0 else "") + str(wmDiff))
        if lzDiff != 0:
            diff.append("LZ " + ("+" if lzDiff >= 0 else "") + str(lzDiff))
        if haerteDiff != 0:
            diff.append("Härte " + ("+" if haerteDiff >= 0 else "") + str(haerteDiff))
        if len(eigPlusDiff) > 0:
            diff.append("Eigenschaften +" + ", +".join(eigPlusDiff))
        if len(eigMinusDiff) > 0:
            if len(eigPlusDiff) > 0:
                diff[-1] += ", " + ("-" + ", -".join(eigMinusDiff))
            else:
                diff.append("Eigenschaften -" + ", -".join(eigMinusDiff))
        return diff


    def updateWeaponStats(self):
        vtVerboten = Wolke.DB.einstellungen["Waffen: Talente VT verboten"].toTextList()
        for index in range(8):
            if index >= len(Wolke.Char.waffen) or not Wolke.Char.waffen[index].name:
                self.labelBasis[index].setText(f"<span style='{Wolke.FontAwesomeCSS}'>\uf02d</span>&nbsp;&nbsp;-")
                self.labelWerte[index].hide()
                self.labelMods[index].hide()
                continue
            self.labelWerte[index].show()
            self.labelMods[index].show()
            ww = Wolke.Char.waffenwerte[index]
            waffe = Wolke.Char.waffen[index]
            vt = ww.VT
            if waffe.name in vtVerboten or waffe.talent in vtVerboten:
                vt = "-"
            
            diff = []
            if self.waffenTypen[index] in Wolke.DB.waffen:
                dbWaffe = Wolke.DB.waffen[self.waffenTypen[index]]
                diff = self.diffWeapons(waffe, dbWaffe)

            diff = ', '.join(diff).replace(", Eigenschaften", "; Eigenschaften")
            self.labelBasis[index].setText(f"<span style='{Wolke.FontAwesomeCSS}'>\uf02d</span>&nbsp;&nbsp;{self.waffenTypen[index]}")
            self.labelWerte[index].setText(f"""<span style='{Wolke.FontAwesomeCSS}'>\uf6cf</span>&nbsp;&nbsp;AT* {ww.AT}, VT* {vt}, TP* {ww.TPW6}W{str(waffe.würfelSeiten)}{"+" if ww.TPPlus >= 0 else ""}{ww.TPPlus}""")
            if len(diff) > 0:
                self.labelMods[index].setText(f"<span style='{Wolke.FontAwesomeCSS}'>\uf6e3</span>&nbsp;&nbsp;{diff}")
            else:
                self.labelMods[index].setText("")


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
            W.würfelSeiten = dbWaffe.würfelSeiten
        W.wm = self.spinWM[index].value()
        W.rw = self.spinRW[index].value()
        W.würfel = self.spinWürfel[index].value()
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
        if len(Wolke.Char.waffen) == 0:
            for waffe in Wolke.DB.einstellungen["Waffen: Standardwaffen"].toTextList():
                if waffe in Wolke.DB.waffen:
                    Wolke.Char.waffen.append(copy.copy(Wolke.DB.waffen[waffe]))
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
        self.spinWürfel[index].setValue(W.würfel)
        self.labelSeiten[index].setText("W" + str(W.würfelSeiten) + "+")
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
        self.spinWürfel[index].setEnabled(not isEmpty)
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