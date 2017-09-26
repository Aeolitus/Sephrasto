# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:11:39 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterBeschreibung
from PyQt5 import QtWidgets, QtCore


class BeschrWrapper(QtCore.QObject):
    '''
    Wrapper class for the Beschreibung GUI. Contains methods for updating
    the GUI elements to the current values and for changing the current values
    to the values set by the user.
    '''
    modified = QtCore.pyqtSignal()

    def __init__(self):
        ''' Initialize and connect signals '''
        super().__init__()
        if Wolke.Debug:
            print("Initializing BeschrWrapper...")
        self.formBeschr = QtWidgets.QWidget()
        self.uiBeschr = CharakterBeschreibung.Ui_formBeschreibung()
        self.uiBeschr.setupUi(self.formBeschr)
        self.loadBeschreibung()
        self.uiBeschr.editName.editingFinished.connect(self.updateBeschreibung)
        self.uiBeschr.editRasse.editingFinished.connect(
                self.updateBeschreibung)
        self.uiBeschr.editKurzbeschreibung.editingFinished.connect(
            self.updateBeschreibung)
        for i in range(8):
            eval("self.uiBeschr.editEig" + str(i+1) +
                 ".editingFinished.connect(self.updateBeschreibung)")
        self.uiBeschr.comboFinanzen.activated.connect(self.updateBeschreibung)
        self.uiBeschr.comboStatus.activated.connect(self.updateBeschreibung)
        self.uiBeschr.comboHeimat.activated.connect(self.updateBeschreibung)
        self.currentGebraeuche = Wolke.Char.heimat
        if "Gebräuche: " + self.currentGebraeuche not in \
                Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente:
            Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente.append(
                    "Gebräuche: " + self.currentGebraeuche)

    def updateBeschreibung(self):
        ''' Transfer current values to Char object '''
        if self.uiBeschr.editName.text() != "":
            Wolke.Char.name = self.uiBeschr.editName.text()
        if self.uiBeschr.editRasse.text() != "":
            Wolke.Char.rasse = self.uiBeschr.editRasse.text()
        Wolke.Char.status = self.uiBeschr.comboStatus.currentIndex()
        Wolke.Char.finanzen = self.uiBeschr.comboFinanzen.currentIndex()

        if self.uiBeschr.comboHeimat.currentText() != self.currentGebraeuche:
            if "Gebräuche: " + self.currentGebraeuche in \
                    Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente:
                Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente.remove(
                        "Gebräuche: " + self.currentGebraeuche)
            self.currentGebraeuche = self.uiBeschr.comboHeimat.currentText()
            if "Gebräuche: " + self.currentGebraeuche not in \
                    Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente:
                Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente.append(
                    "Gebräuche: " + self.currentGebraeuche)
        Wolke.Char.heimat = self.uiBeschr.comboHeimat.currentText()
        Wolke.Char.kurzbeschreibung = self.uiBeschr.editKurzbeschreibung.text()
        Wolke.Char.eigenheiten = []
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig1.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig2.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig3.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig4.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig5.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig6.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig7.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig8.text())
        self.modified.emit()

    def loadBeschreibung(self):
        ''' Load values from Char object '''
        self.uiBeschr.editName.setText(Wolke.Char.name)
        self.uiBeschr.editRasse.setText(Wolke.Char.rasse)
        self.uiBeschr.comboStatus.setCurrentIndex(Wolke.Char.status)
        self.uiBeschr.comboFinanzen.setCurrentIndex(Wolke.Char.finanzen)
        self.uiBeschr.comboHeimat.setCurrentText(Wolke.Char.heimat)
        self.uiBeschr.editKurzbeschreibung.setText(Wolke.Char.kurzbeschreibung)
        arr = ["", "", "", "", "", "", "", ""]
        count = 0
        for el in Wolke.Char.eigenheiten:
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
        