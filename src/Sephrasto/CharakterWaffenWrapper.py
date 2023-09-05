# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterWaffen
from PySide6 import QtWidgets, QtCore, QtGui
from Core.Waffe import Waffe, WaffeDefinition
from CharakterWaffenPickerWrapper import WaffenPicker
import logging
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
import re
from QtUtils.TextTagCompleter import TextTagCompleter
import copy
from functools import partial

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
        self.spinHärte = []
        self.editEig = []
        self.eigenschaftenCompleter = []
        self.comboBE = []
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

            spinHärte = getattr(self.ui, "spinW" + str(i+1) + "h")
            spinHärte.valueChanged.connect(self.updateWaffen)
            spinHärte.setEnabled(False)
            self.spinHärte.append(spinHärte)

            editEig = getattr(self.ui, "editW" + str(i+1) + "eig")
            editEig.editingFinished.connect(self.updateWaffen)
            editEig.setEnabled(False)
            self.editEig.append(editEig)
            eigenschaftenCompleter = TextTagCompleter(editEig, Wolke.DB.waffeneigenschaften.keys())
            self.eigenschaftenCompleter.append(eigenschaftenCompleter)

            comboBE = getattr(self.ui, "comboBEW" + str(i+1))
            comboBE.currentIndexChanged.connect(self.updateWaffen)
            comboBE.setEnabled(False)
            self.comboBE.append(comboBE)

            comboStil = getattr(self.ui, "comboStil" + str(i+1))
            comboStil.currentIndexChanged.connect(self.updateWaffen)
            comboStil.setEnabled(False)
            self.comboStil.append(comboStil)

            addW = getattr(self.ui, "addW" + str(i+1))
            addW.clicked.connect(partial(self.selectWeapon, index=i))
            self.addW.append(addW)

            if i > 0:
                upW = getattr(self.ui, "buttonW" + str(i+1) + "Up")
                upW.setText('\uf106')
                upW.clicked.connect(partial(self.moveWeapon, index=i, direction=-1))
            if i < 7:
                downW = getattr(self.ui, "buttonW" + str(i+1) + "Down")
                downW.setText('\uf078')
                downW.clicked.connect(partial(self.moveWeapon, index=i, direction=+1))

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

- AT und VT: Talent-PW + WM + Kampfstilbonus - BE -2 (falls zu schwer)
- TP: Waffen-TP + Schadensbonus (x2, falls kopflastig) + Kampfstilbonus</p>""")
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

    def diffWaffeDefinition(self, waffe):
        diff = []
        würfelDiff = waffe.würfel - waffe.definition.würfel
        plusDiff = waffe.plus - waffe.definition.plus

        härteDiff = waffe.härte - waffe.definition.härte
        waffenHärteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].wert
        if waffe.definition.name in waffenHärteWSStern:
            härteDiff = 0
        wmDiff = waffe.wm - waffe.definition.wm
        rwDiff = waffe.rw - waffe.definition.rw
        lzDiff = 0
        if waffe.fernkampf:
            lzDiff = waffe.lz - waffe.definition.lz

        eigPlusDiff = list(set(waffe.eigenschaften) - set(waffe.definition.eigenschaften))
        eigMinusDiff = list(set(waffe.definition.eigenschaften) - set(waffe.eigenschaften))

        if würfelDiff != 0:
            diff.append("TP " + ("+" if würfelDiff >= 0 else "") + str(würfelDiff) + "W" + str(waffe.würfelSeiten))
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
        if härteDiff != 0:
            diff.append("Härte " + ("+" if härteDiff >= 0 else "") + str(härteDiff))
        if len(eigPlusDiff) > 0:
            diff.append(f"<span style='{Wolke.FontAwesomeCSS}'>\u002b</span>&nbsp;&nbsp;" + ", ".join(eigPlusDiff))
        if len(eigMinusDiff) > 0:
            if len(eigPlusDiff) > 0:
                diff[-1] += f"&nbsp;&nbsp;<span style='{Wolke.FontAwesomeCSS}'>\uf068</span>&nbsp;&nbsp;" + ",a ".join(eigMinusDiff)
            else:
                diff.append(f"<span style='{Wolke.FontAwesomeCSS}'>\uf068</span>&nbsp;&nbsp;" + ", ".join(eigMinusDiff))
        return diff

    def updateWeaponStats(self):
        atVerboten = Wolke.DB.einstellungen["Waffen: Talente AT verboten"].wert
        vtVerboten = Wolke.DB.einstellungen["Waffen: Talente VT verboten"].wert
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

            at = ww.at
            tp = f"""{ww.würfel}W{str(waffe.würfelSeiten)}{"+" if ww.plus >= 0 else ""}{ww.plus}"""
            if waffe.name in atVerboten or waffe.talent in atVerboten:
                at = "-"
                tp = "-"

            vt = ww.vt
            if waffe.name in vtVerboten or waffe.talent in vtVerboten:
                vt = "-"
            
            diff = self.diffWaffeDefinition(waffe)

            diff = ', '.join(diff).replace(", Eigenschaften", "; Eigenschaften")

            self.labelBasis[index].setText(f"<span style='{Wolke.FontAwesomeCSS}'>\uf02d</span>&nbsp;&nbsp;{waffe.definition.anzeigename} ({waffe.talent})")
            self.labelWerte[index].setText(f"""<span style='{Wolke.FontAwesomeCSS}'>\uf6cf</span>&nbsp;&nbsp;AT {at}, VT {vt}, TP {tp}""")
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
        if W.name:
            entries = [WaffeDefinition.keinKampfstil] + [ks for ks in W.kampfstile if ks + " I" in Wolke.Char.vorteile]
            comboStil.addItems(entries)
            if W.kampfstil in entries:
                comboStil.setCurrentIndex(entries.index(W.kampfstil))
        comboStil.setEnabled(comboStil.count() > 1)
        comboStil.blockSignals(False)
        
    def createWaffe(self, index):
        name = self.waffenTypen[index]
        anzeigename = self.editWName[index].text()
        if name in Wolke.DB.waffen:
            W = Waffe(Wolke.DB.waffen[name])
        else:
            definition = WaffeDefinition()
            definition.name = name
            W = Waffe(definition)

        if W.fernkampf:
            W.lz = self.spinLZ[index].value()

        W.anzeigename = anzeigename
        W.wm = self.spinWM[index].value()
        W.rw = self.spinRW[index].value()
        W.würfel = self.spinWürfel[index].value()
        W.plus = self.spinPlus[index].value()

        eigenschaften = self.editEig[index].text().strip().rstrip(",")
        self.editEig[index].setText(eigenschaften)
        if eigenschaften:
            W.eigenschaften = list(map(str.strip, eigenschaften.split(",")))
        else:
            W.eigenschaften = []
        W.beSlot = self.comboBE[index].currentIndex()
        W.kampfstil = self.comboStil[index].currentText()

        waffenHärteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].wert
        if "WS" in Wolke.Char.abgeleiteteWerte and W.name in waffenHärteWSStern:
            W.härte = Wolke.Char.abgeleiteteWerte["WS"].finalwert
        else:
            W.härte = self.spinHärte[index].value()
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
            for waffe in Wolke.DB.einstellungen["Waffen: Standardwaffen"].wert:
                if waffe in Wolke.DB.waffen:
                    Wolke.Char.waffen.append(Waffe(Wolke.DB.waffen[waffe]))
                    aktualisieren = True
        while len(Wolke.Char.waffen) < 8:
            aktualisieren = True
            Wolke.Char.waffen.append(Waffe(WaffeDefinition()))
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
        waffenHärteWSStern = Wolke.DB.einstellungen["Waffen: Härte WSStern"].wert
        if "WS" in Wolke.Char.abgeleiteteWerte and W.name in waffenHärteWSStern:
            W.härte = Wolke.Char.abgeleiteteWerte["WS"].finalwert
            self.spinHärte[index].setEnabled(False)
        else:
            self.spinHärte[index].setEnabled(True)
        self.spinHärte[index].setValue(W.härte)
        self.spinRW[index].setValue(W.rw)
        self.spinWM[index].setValue(W.wm)
        self.comboBE[index].setCurrentIndex(W.beSlot)

        if W.fernkampf:
            self.spinLZ[index].setValue(W.lz)
            self.spinLZ[index].setEnabled(True)
        else:
            self.spinLZ[index].setEnabled(False)
        
        self.refreshDerivedWeaponValues(W, index)

        isEmpty = W.name == ""
        atVerboten = W.name in Wolke.DB.einstellungen["Waffen: Talente AT verboten"].wert or W.talent in Wolke.DB.einstellungen["Waffen: Talente AT verboten"].wert
        self.editWName[index].setEnabled(not isEmpty)
        self.editEig[index].setEnabled(not isEmpty)
        self.spinWürfel[index].setEnabled(not isEmpty and not atVerboten)
        self.spinPlus[index].setEnabled(not isEmpty and not atVerboten)
        self.spinRW[index].setEnabled(not isEmpty and not atVerboten)
        self.spinWM[index].setEnabled(not isEmpty)
        self.comboBE[index].setEnabled(not isEmpty)
        self.comboStil[index].setEnabled(not isEmpty and self.comboStil[index].count() > 1)
        if isEmpty:
            self.spinHärte[index].setEnabled(False)
            self.addW[index].setText('\u002b')
        else:
            self.addW[index].setText('\uf2ed')

    def selectWeapon(self, index):
        if Wolke.Char.waffen[index].name == "":
            # add
            logging.debug("Starting WaffenPicker")
            pickerClass = EventBus.applyFilter("class_waffenpicker_wrapper", WaffenPicker)
            picker = pickerClass()
            logging.debug("WaffenPicker created")
            if picker.waffe is not None:
                self.currentlyLoading = True
                self.loadWeaponIntoFields(Waffe(picker.waffe), index)
                self.currentlyLoading = False
                self.updateWaffen()
        else:
            #remove
            self.currentlyLoading = True
            self.loadWeaponIntoFields(Waffe(WaffeDefinition()), index)
            self.currentlyLoading = False
            self.updateWaffen()