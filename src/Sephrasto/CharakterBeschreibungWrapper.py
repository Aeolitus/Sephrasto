# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:11:39 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterBeschreibung
from PySide6 import QtWidgets, QtCore
import logging
from Hilfsmethoden import Hilfsmethoden
from PySide6.QtGui import QPixmap

class BeschrWrapper(QtCore.QObject):
    '''
    Wrapper class for the Beschreibung GUI. Contains methods for updating
    the GUI elements to the current values and for changing the current values
    to the values set by the user.
    '''
    modified = QtCore.Signal()

    def __init__(self):
        ''' Initialize and connect signals '''
        super().__init__()
        logging.debug("Initializing BeschrWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterBeschreibung.Ui_formBeschreibung()
        self.ui.setupUi(self.form)

        self.ui.editName.editingFinished.connect(self.update)
        self.ui.editSpezies.editingFinished.connect(self.update)
        self.ui.editKurzbeschreibung.editingFinished.connect(self.update)
        for i in range(8):
            editEig = getattr(self.ui, "editEig" + str(i+1))
            editEig.editingFinished.connect(self.update)

        finanzen = Wolke.DB.einstellungen["Finanzen"].wert
        self.ui.comboFinanzen.addItems(Wolke.DB.einstellungen["Finanzen"].wert)
        if "Normal" in finanzen:
            self.ui.comboFinanzen.setCurrentText("Normal")
        self.ui.comboFinanzen.activated.connect(self.update)
        self.ui.comboStatus.addItems(Wolke.DB.einstellungen["Statusse"].wert)
        self.ui.comboStatus.activated.connect(self.update)
        self.ui.comboHeimat.activated.connect(self.update)

        self.ui.comboStatus.setToolTip(Hilfsmethoden.fixHtml(Wolke.DB.einstellungen["Statusse: Beschreibung"].wert))
        self.ui.comboFinanzen.setToolTip(Hilfsmethoden.fixHtml(Wolke.DB.einstellungen["Finanzen: Beschreibung"].wert))
        self.ui.comboHeimat.setToolTip(Hilfsmethoden.fixHtml(Wolke.DB.einstellungen["Heimaten: Beschreibung"].wert))

        self.characterImage = None
        self.labelImageText = self.ui.labelImage.text()
        self.ui.buttonLoadImage.clicked.connect(self.buttonLoadImageClicked)
        self.ui.buttonDeleteImage.clicked.connect(self.buttonDeleteImageClicked)
        self.currentlyLoading = False

    def update(self):
        if self.currentlyLoading:
            return

        ''' Transfer current values to Char object '''
        changed = False

        if Wolke.Char.name != self.ui.editName.text():
            Wolke.Char.name = self.ui.editName.text()
            changed = True

        if Wolke.Char.spezies != self.ui.editSpezies.text():
            Wolke.Char.spezies = self.ui.editSpezies.text()
            changed = True

        if Wolke.Char.status != self.ui.comboStatus.currentIndex():
            Wolke.Char.status = self.ui.comboStatus.currentIndex()
            changed = True

        if Wolke.Char.finanzen != self.ui.comboFinanzen.currentIndex():
            Wolke.Char.finanzen = self.ui.comboFinanzen.currentIndex()
            changed = True

        if Wolke.Char.heimat != self.ui.comboHeimat.currentText():
            Wolke.Char.heimat = self.ui.comboHeimat.currentText()
            changed = True

        if Wolke.Char.kurzbeschreibung != self.ui.editKurzbeschreibung.text():
            Wolke.Char.kurzbeschreibung = self.ui.editKurzbeschreibung.text()
            changed = True

        eigenheitenNeu = []
        for i in range(8):
            lineEdit = getattr(self.ui, "editEig" + str(i+1))
            eigenheitenNeu.append(lineEdit.text())

        #Preserve the position of actual elements but remove any trailing empty elements
        #This is needed for ArrayEqual later to work as intended
        for eig in reversed(eigenheitenNeu):
            if eig == "":
                eigenheitenNeu.pop()
            else:
                break

        if not Hilfsmethoden.ArrayEqual(eigenheitenNeu, Wolke.Char.eigenheiten):
            changed = True
            Wolke.Char.eigenheiten = eigenheitenNeu

        if changed:
            self.modified.emit()

    def load(self):
        self.currentlyLoading = True

        self.ui.labelFinanzen.setVisible(Wolke.Char.finanzenAnzeigen)
        self.ui.comboFinanzen.setVisible(Wolke.Char.finanzenAnzeigen)

        ''' Load values from Char object '''
        self.ui.editName.setText(Wolke.Char.name)
        self.ui.editSpezies.setText(Wolke.Char.spezies)
        statusse = Wolke.DB.einstellungen["Statusse"].wert
        if Wolke.Char.status < len(statusse):
            self.ui.comboStatus.setCurrentIndex(Wolke.Char.status)
        finanzen = Wolke.DB.einstellungen["Finanzen"].wert
        if Wolke.Char.finanzen < len(finanzen):
            self.ui.comboFinanzen.setCurrentIndex(Wolke.Char.finanzen)
        self.ui.editKurzbeschreibung.setText(Wolke.Char.kurzbeschreibung)
        arr = ["", "", "", "", "", "", "", ""]
        count = 0
        for el in Wolke.Char.eigenheiten:
            arr[count] = el
            count += 1
        self.ui.editEig1.setText(arr[0])
        self.ui.editEig2.setText(arr[1])
        self.ui.editEig3.setText(arr[2])
        self.ui.editEig4.setText(arr[3])
        self.ui.editEig5.setText(arr[4])
        self.ui.editEig6.setText(arr[5])
        self.ui.editEig7.setText(arr[6])
        self.ui.editEig8.setText(arr[7])

        ''' Fill and set Heimat '''
        self.ui.comboHeimat.clear()
        heimaten = sorted(Wolke.DB.einstellungen["Heimaten"].wert, key=Hilfsmethoden.unicodeCaseInsensitive)
        self.ui.comboHeimat.addItems(heimaten)
        self.ui.comboHeimat.setCurrentText(Wolke.Char.heimat)

        if Wolke.Char.bild:
            self.characterImage = QPixmap()
            self.characterImage.loadFromData(Wolke.Char.bild)
            self.setImage(self.characterImage)

        self.currentlyLoading = False

    def setImage(self, pixmap):
        self.ui.labelImage.setPixmap(pixmap.scaled(self.ui.labelImage.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def buttonLoadImageClicked(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Bild laden...", "", "Bild Dateien (*.png *.jpg *.bmp)")
        if spath == "":
            return
        
        self.characterImage = QPixmap(spath).scaled(Wolke.CharImageSize[0], Wolke.CharImageSize[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setImage(self.characterImage)

        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.WriteOnly);
        self.characterImage.save(buffer, "JPG")
        imageData = buffer.data().data()
        if Wolke.Char.bild != imageData:
            Wolke.Char.bild = imageData
            self.modified.emit()

    def buttonDeleteImageClicked(self):
        self.characterImage = None
        self.ui.labelImage.setPixmap(QPixmap())
        self.ui.labelImage.setText(self.labelImageText)

        if Wolke.Char.bild != None:
            Wolke.Char.bild = None
            self.modified.emit()

    def onDetailsVisibilityChanged(self, visible):
        self.ui.labelKurzbeschreibung.setVisible(not visible)
        self.ui.editKurzbeschreibung.setVisible(not visible)