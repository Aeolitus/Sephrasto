# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
import logging
import re

from PyQt5 import QtCore, QtWidgets

import CharakterEquipment
import Definitionen
import Objekte
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden
from RuestungPicker import RuestungPicker
from WaffenPicker import WaffenPicker
from Wolke import Wolke


class EquipWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        logging.debug("Initializing EquipWrapper...")
        self.formEq = QtWidgets.QWidget()
        self.uiEq = CharakterEquipment.Ui_formAusruestung()
        self.uiEq.setupUi(self.formEq)
        self.initialLoad = True
        logging.debug("UI Setup...")
        # Signals
        # Connect all Spins and Edit boxes - hacky, sorry
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "spin"]
        for el in fields:
            eval("self.uiEq." + el + ".valueChanged.connect(self.update)")
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "edit"]
        for el in fields:
            eval("self.uiEq." + el + ".editingFinished.connect(self.update)")
        logging.debug("Signals Set...")

        kampfstile = [Definitionen.KeinKampfstil] + Wolke.DB.findKampfstile()
        for el in range(1, 9):
            eval("self.uiEq.comboStil" + str(el) + ".setCurrentIndex(0)")
            eval("self.uiEq.comboStil" + str(el) + ".clear()")
            for el2 in kampfstile:

                def getName():
                    return el2

                eval("self.uiEq.comboStil" + str(el) + ".addItem(getName())")
        logging.debug("Kampfstile added...")
        self.uiEq.addR1.clicked.connect(lambda state, idx=1: self.selectArmor(idx))
        self.uiEq.addR2.clicked.connect(lambda state, idx=2: self.selectArmor(idx))
        self.uiEq.addR3.clicked.connect(lambda state, idx=3: self.selectArmor(idx))
        self.uiEq.addW1.clicked.connect(lambda state, idx=1: self.selectWeapon(idx))
        self.uiEq.addW2.clicked.connect(lambda state, idx=2: self.selectWeapon(idx))
        self.uiEq.addW3.clicked.connect(lambda state, idx=3: self.selectWeapon(idx))
        self.uiEq.addW4.clicked.connect(lambda state, idx=4: self.selectWeapon(idx))
        self.uiEq.addW5.clicked.connect(lambda state, idx=5: self.selectWeapon(idx))
        self.uiEq.addW6.clicked.connect(lambda state, idx=6: self.selectWeapon(idx))
        self.uiEq.addW7.clicked.connect(lambda state, idx=7: self.selectWeapon(idx))
        self.uiEq.addW8.clicked.connect(lambda state, idx=8: self.selectWeapon(idx))

        logging.debug("Check Toggle...")
        self.uiEq.checkZonen.setChecked(Wolke.Char.zonenSystemNutzen)
        self.uiEq.checkZonen.stateChanged.connect(self.checkToggleEquip)

        self.currentlyLoading = False

        self.checkToggleEquip()

    def update(self):
        if self.currentlyLoading:
            return

        changed = False
        ruestungNeu = []

        for el in ["R1", "R2", "R3"]:
            editName = getattr(self.uiEq, "edit" + el + "name")
            spinBE = getattr(self.uiEq, "spin" + el + "be")
            spinRS = getattr(self.uiEq, "spin" + el + "RS")
            spinZRS = [
                getattr(self.uiEq, "spin" + el + "bein"),
                getattr(self.uiEq, "spin" + el + "larm"),
                getattr(self.uiEq, "spin" + el + "rarm"),
                getattr(self.uiEq, "spin" + el + "bauch"),
                getattr(self.uiEq, "spin" + el + "brust"),
                getattr(self.uiEq, "spin" + el + "kopf"),
            ]
            spinPunkte = getattr(self.uiEq, "spin" + el + "punkte")

            if editName.text() == "":
                spinPunkte.setStyleSheet("")
                spinPunkte.setToolTip("")
                continue

            R = Objekte.Ruestung()
            R.name = editName.text()
            R.be = int(spinBE.value())
            if self.uiEq.checkZonen.isChecked():
                for i in range(6):
                    R.rs[i] = spinZRS[i].value()
            else:
                R.rs = 6 * [spinRS.value()]
            ruestungNeu.append(R)

            if sum(R.rs) % 6 != 0:
                spinPunkte.setStyleSheet("border: 1px solid orange;")
                missingPoints = 6 - sum(R.rs) % 6
                if missingPoints == 1:
                    spinPunkte.setToolTip(
                        "Der Rüstung fehlt " + str(6 - sum(R.rs) % 6) + " Punkt ZRS."
                    )
                else:
                    spinPunkte.setToolTip(
                        "Der Rüstung fehlen " + str(6 - sum(R.rs) % 6) + " Punkte ZRS."
                    )
            else:
                spinPunkte.setStyleSheet("")
                spinPunkte.setToolTip("")

        if not Hilfsmethoden.ArrayEqual(ruestungNeu, Wolke.Char.rüstung):
            changed = True
            Wolke.Char.rüstung = ruestungNeu

        if Wolke.Char.zonenSystemNutzen != self.uiEq.checkZonen.isChecked():
            Wolke.Char.zonenSystemNutzen = self.uiEq.checkZonen.isChecked()
            changed = True

        waffenNeu = []
        kampfstile = [Definitionen.KeinKampfstil] + Wolke.DB.findKampfstile()

        for el in ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]:
            if eval("self.uiEq.edit" + el + "name.text()") != "":
                name = eval("self.uiEq.label" + el + "typ.text()")
                if name not in Wolke.DB.waffen:
                    W = Objekte.Nahkampfwaffe()
                elif type(Wolke.DB.waffen[name]) == Objekte.Fernkampfwaffe:
                    W = Objekte.Fernkampfwaffe()
                    W.lz = eval("self.uiEq.spin" + el + "lz.value()")
                else:
                    W = Objekte.Nahkampfwaffe()

                W.wm = eval("self.uiEq.spin" + el + "wm.value()")
                W.name = eval("self.uiEq.label" + el + "typ.text()")
                W.anzeigename = eval("self.uiEq.edit" + el + "name.text()")
                if not W.name and W.anzeigename and W.anzeigename in Wolke.DB.waffen:
                    W.name = W.anzeigename
                if W.name in Wolke.DB.waffen:
                    dbWaffe = Wolke.DB.waffen[W.name]
                    W.fertigkeit = dbWaffe.fertigkeit
                    W.talent = dbWaffe.talent
                    W.kampfstile = dbWaffe.kampfstile.copy()

                W.rw = eval("self.uiEq.spin" + el + "rw.value()")
                W.W6 = eval("self.uiEq.spin" + el + "w6.value()")
                W.plus = eval("self.uiEq.spin" + el + "plus.value()")
                eigenschaftStr = eval("self.uiEq.edit" + el + "eig.text()")
                if eigenschaftStr:
                    W.eigenschaften = list(map(str.strip, eigenschaftStr.split(",")))

                self.refreshKampfstile(int(el[-1]) - 1)
                tmp = eval("self.uiEq.comboStil" + el[-1] + ".currentText()")
                if tmp in kampfstile:
                    W.kampfstil = tmp

                if EventBus.applyFilter(
                    "waffe_haerte_wsstern", W.name in ["Hand", "Fuß"], {"waffe": W}
                ):
                    W.haerte = Wolke.Char.wsStern
                else:
                    W.haerte = eval("self.uiEq.spin" + el + "h.value()")
                waffenNeu.append(W)

        if not Hilfsmethoden.ArrayEqual(waffenNeu, Wolke.Char.waffen):
            Wolke.Char.waffen = waffenNeu
            changed = True

        if changed:
            Wolke.Char.aktualisieren()
            self.modified.emit()
        self.load()

    def load(self):
        self.currentlyLoading = True
        Rarr = ["R1", "R2", "R3"]
        count = 0
        # Add in Armor
        while count < len(Wolke.Char.rüstung):
            if count < len(Rarr):
                R = Wolke.Char.rüstung[count]

                def getName():
                    return R.name

                eval("self.uiEq.edit" + Rarr[count] + "name.setText(getName())")
                eval("self.uiEq.spin" + Rarr[count] + "be.setValue(" + str(R.be) + ")")
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "bein.setValue("
                    + str(R.rs[0])
                    + ")"
                )
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "larm.setValue("
                    + str(R.rs[1])
                    + ")"
                )
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "rarm.setValue("
                    + str(R.rs[2])
                    + ")"
                )
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "bauch.setValue("
                    + str(R.rs[3])
                    + ")"
                )
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "brust.setValue("
                    + str(R.rs[4])
                    + ")"
                )
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "kopf.setValue("
                    + str(R.rs[5])
                    + ")"
                )
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "RS.setValue("
                    + str(R.getRSGesamtInt())
                    + ")"
                )
                eval(
                    "self.uiEq.spin"
                    + Rarr[count]
                    + "punkte.setValue("
                    + str(sum(R.rs))
                    + ")"
                )
                count += 1

        # Empty all other cells
        while count < 3:
            eval("self.uiEq.edit" + Rarr[count] + 'name.setText("")')
            eval("self.uiEq.spin" + Rarr[count] + "be.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "bein.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "larm.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "rarm.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "bauch.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "brust.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "kopf.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "RS.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "punkte.setValue(0)")
            count += 1

        count = 0
        # Load in Weapons
        while count < len(Wolke.Char.waffen):
            W = Wolke.Char.waffen[count]
            self.loadWeaponIntoFields(W, count + 1)
            count += 1

        Warr = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]
        # Empty all other fields
        while count < 8:
            eval("self.uiEq.edit" + Warr[count] + 'name.setText("")')
            eval("self.uiEq.label" + Warr[count] + 'typ.setText("")')
            eval("self.uiEq.comboStil" + str(count + 1) + ".clear()")
            eval("self.uiEq.edit" + Warr[count] + 'eig.setText("")')
            eval("self.uiEq.edit" + Warr[count] + 'eig.setToolTip("")')
            eval("self.uiEq.spin" + Warr[count] + "w6.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "plus.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "h.setValue(6)")
            eval("self.uiEq.spin" + Warr[count] + "rw.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "wm.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "lz.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "lz.setEnabled(False)")
            count += 1

        self.initialLoad = False
        self.currentlyLoading = False

    def loadArmorIntoFields(self, R, index, replace):
        Rarr = ["R1", "R2", "R3"]
        count = index - 1
        editName = getattr(self.uiEq, "edit" + Rarr[count] + "name")
        spinBE = getattr(self.uiEq, "spin" + Rarr[count] + "be")
        spinRS = getattr(self.uiEq, "spin" + Rarr[count] + "RS")
        spinZRS = [
            getattr(self.uiEq, "spin" + Rarr[count] + "bein"),
            getattr(self.uiEq, "spin" + Rarr[count] + "larm"),
            getattr(self.uiEq, "spin" + Rarr[count] + "rarm"),
            getattr(self.uiEq, "spin" + Rarr[count] + "bauch"),
            getattr(self.uiEq, "spin" + Rarr[count] + "brust"),
            getattr(self.uiEq, "spin" + Rarr[count] + "kopf"),
        ]
        spinPunkte = getattr(self.uiEq, "spin" + Rarr[count] + "punkte")

        if replace or editName.text() == "":
            editName.setText(R.name)
        else:
            editName.setText(editName.text() + ", " + R.name)

        if not replace:
            for i in range(6):
                R.rs[i] += spinZRS[i].value()

        for i in range(6):
            spinZRS[i].setValue(R.rs[i])

        spinBE.setValue(
            EventBus.applyFilter("ruestung_be", R.getRSGesamtInt(), {"name": R.name})
        )
        spinRS.setValue(R.getRSGesamtInt())
        spinPunkte.setValue(sum(R.rs))

    def selectArmor(self, index):
        logging.debug("Starting RuestungPicker")
        picker = RuestungPicker(
            eval("self.uiEq.editR" + str(index) + "name.text()"),
            2 if self.uiEq.checkZonen.isChecked() else 1,
        )
        logging.debug("RuestungPicker created")
        if picker.ruestung is not None:
            self.currentlyLoading = True
            self.loadArmorIntoFields(picker.ruestung, index, picker.ruestungErsetzen)
            self.currentlyLoading = False
            self.update()

    def refreshKampfstile(self, index):
        logging.debug("Starting refreshKampfstile for index " + str(index))
        name = eval("self.uiEq.labelW" + str(index + 1) + "typ.text()")
        anzeigename = eval("self.uiEq.editW" + str(index + 1) + "name.text()")
        tmp = eval("self.uiEq.comboStil" + str(index + 1) + ".currentText()")
        if name != "" or anzeigename != "":
            if name in Wolke.DB.waffen:
                entries = []
                entries.append(Definitionen.KeinKampfstil)
                kampfstile = Wolke.DB.findKampfstile()
                for kampfstil in Wolke.DB.waffen[name].kampfstile:
                    if (
                        kampfstil in kampfstile
                        and kampfstil + " I" in Wolke.Char.vorteile
                    ):
                        # if kampfstil in list(map(str.strip, kampfstile.split(","))) and kampfstil + " I" in Wolke.Char.vorteile:
                        entries.append(kampfstil)

                eval("self.uiEq.comboStil" + str(index + 1) + ".setCurrentIndex(0)")
                eval("self.uiEq.comboStil" + str(index + 1) + ".clear()")
                eval("self.uiEq.comboStil" + str(index + 1) + ".setToolTip(None)")

                for el in entries:

                    def getName():
                        return el

                    eval("self.uiEq.comboStil" + str(index + 1) + ".addItem(getName())")
                if self.initialLoad:
                    stil = Wolke.Char.waffen[index].kampfstil
                    if stil in entries:
                        eval(
                            "self.uiEq.comboStil"
                            + str(index + 1)
                            + ".setCurrentIndex("
                            + str(entries.index(stil))
                            + ")"
                        )
                    else:
                        eval(
                            "self.uiEq.comboStil"
                            + str(index + 1)
                            + ".setCurrentIndex(0)"
                        )
                elif tmp in entries:
                    eval(
                        "self.uiEq.comboStil"
                        + str(index + 1)
                        + ".setCurrentIndex("
                        + str(entries.index(tmp))
                        + ")"
                    )
            else:
                eval("self.uiEq.comboStil" + str(index + 1) + ".setCurrentIndex(0)")
                eval("self.uiEq.comboStil" + str(index + 1) + ".clear()")
                eval(
                    "self.uiEq.comboStil"
                    + str(index + 1)
                    + ".addItem('Waffe unbekannt')"
                )
                eval(
                    "self.uiEq.comboStil"
                    + str(index + 1)
                    + ".setToolTip('Der Name der Waffe ist unbekannt, daher kann kein Kampfstil ausgewählt werden. Die Kampfwerte müssen in der PDF manuell ausgefüllt werden.')"
                )

    def loadWeaponIntoFields(self, W, index):
        Warr = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]
        count = index - 1

        def getName():
            return W.name

        getAnzeigename = lambda: W.anzeigename or W.name
        eval("self.uiEq.edit" + Warr[count] + "name.setText(getAnzeigename())")
        eval("self.uiEq.label" + Warr[count] + "typ.setText(getName())")
        self.refreshKampfstile(count)
        getEigenschaften = lambda: ", ".join(W.eigenschaften)

        def getWaffeneigenschaftenTooltip():
            result = ""
            for we in W.eigenschaften:
                name = re.sub(r"\((.*?)\)", "", we, re.UNICODE).strip()
                if name in Wolke.DB.waffeneigenschaften:
                    waffeneigenschaft = Wolke.DB.waffeneigenschaften[name]
                    if waffeneigenschaft.text:
                        result += "<b>" + we + ":</b> " + waffeneigenschaft.text + "\n"
                else:
                    result += "<b>" + we + ":</b> Unbekannte Eigenschaft\n"

            return (
                "<html><head/><body><div>"
                + result[:-1].replace("\n", "<br>")
                + "</div></body></html>"
            )

        eval("self.uiEq.edit" + Warr[count] + "eig.setText(getEigenschaften())")
        eval(
            "self.uiEq.edit"
            + Warr[count]
            + "eig.setToolTip(getWaffeneigenschaftenTooltip())"
        )
        eval("self.uiEq.spin" + Warr[count] + "w6.setValue(" + str(W.W6) + ")")
        eval("self.uiEq.spin" + Warr[count] + "plus.setValue(" + str(W.plus) + ")")
        if EventBus.applyFilter(
            "waffe_haerte_wsstern", W.name == "Hand" or W.name == "Fuß", {"waffe": W}
        ):
            eval(
                "self.uiEq.spin"
                + Warr[count]
                + "h.setValue("
                + str(Wolke.Char.wsStern)
                + ")"
            )
        else:
            eval("self.uiEq.spin" + Warr[count] + "h.setValue(" + str(W.haerte) + ")")
        eval("self.uiEq.spin" + Warr[count] + "rw.setValue(" + str(W.rw) + ")")
        eval("self.uiEq.spin" + Warr[count] + "wm.setValue(" + str(W.wm) + ")")
        if type(W) == Objekte.Fernkampfwaffe:
            eval("self.uiEq.spin" + Warr[count] + "lz.setValue(" + str(W.lz) + ")")
            eval("self.uiEq.spin" + Warr[count] + "lz.setEnabled(True)")
        elif type(W) == Objekte.Nahkampfwaffe:
            eval("self.uiEq.spin" + Warr[count] + "lz.setEnabled(False)")

    def selectWeapon(self, index):
        W = None
        try:
            wname = eval("self.uiEq.labelW" + str(index) + "typ.text()")
            for el in Wolke.DB.waffen:
                if Wolke.DB.waffen[el].name == wname:
                    W = el
                    logging.debug("Weapon found - its " + wname)
                    break
        except:
            pass
        logging.debug("Starting WaffenPicker")
        picker = WaffenPicker(W)
        logging.debug("WaffenPicker created")
        if picker.waffe is not None:
            self.currentlyLoading = True
            self.loadWeaponIntoFields(picker.waffe, index)
            self.currentlyLoading = False
            self.update()

    def checkToggleEquip(self):
        if self.currentlyLoading:
            return

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
            self.uiEq.spinR3bauch.show()
            self.uiEq.spinR3brust.show()
            self.uiEq.spinR3larm.show()
            self.uiEq.spinR3rarm.show()
            self.uiEq.spinR3kopf.show()
            self.uiEq.spinR3bein.show()
            self.uiEq.spinR1RS.setEnabled(False)
            self.uiEq.spinR2RS.setEnabled(False)
            self.uiEq.spinR3RS.setEnabled(False)
            self.uiEq.labelBein.show()
            self.uiEq.labelBauch.show()
            self.uiEq.labelBrust.show()
            self.uiEq.labelLarm.show()
            self.uiEq.labelRarm.show()
            self.uiEq.labelKopf.show()
            self.uiEq.labelPunkte.show()
            self.uiEq.spinR1punkte.show()
            self.uiEq.spinR2punkte.show()
            self.uiEq.spinR3punkte.show()
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
            self.uiEq.spinR3bauch.hide()
            self.uiEq.spinR3brust.hide()
            self.uiEq.spinR3larm.hide()
            self.uiEq.spinR3rarm.hide()
            self.uiEq.spinR3kopf.hide()
            self.uiEq.spinR3bein.hide()
            self.uiEq.spinR1RS.setEnabled(True)
            self.uiEq.spinR2RS.setEnabled(True)
            self.uiEq.spinR3RS.setEnabled(True)
            self.uiEq.labelBein.hide()
            self.uiEq.labelBauch.hide()
            self.uiEq.labelBrust.hide()
            self.uiEq.labelLarm.hide()
            self.uiEq.labelRarm.hide()
            self.uiEq.labelKopf.hide()
            self.uiEq.labelPunkte.hide()
            self.uiEq.spinR1punkte.hide()
            self.uiEq.spinR2punkte.hide()
            self.uiEq.spinR3punkte.hide()
        self.currentlyLoading = False
