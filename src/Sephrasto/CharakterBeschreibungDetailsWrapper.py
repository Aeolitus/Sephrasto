from PyQt5 import QtWidgets, QtCore, QtGui
import UI.CharakterBeschreibungDetails
import UI.CharakterBeschreibung
import CharakterBeschreibungWrapper
import lxml.etree as etree
from Wolke import Wolke
import logging
from PyQt5.QtGui import QPixmap
import tempfile
import os
from EventBus import EventBus

class CharakterBeschreibungDetailsWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterBeschreibungDetails.Ui_formBeschreibung()
        self.ui.setupUi(self.form)

        beschrWrapper = EventBus.applyFilter("class_beschreibung_wrapper", CharakterBeschreibungWrapper.BeschrWrapper)
        if beschrWrapper:
            self.beschrWrapper = beschrWrapper()
            self.ui.tabWidget.insertTab(0, self.beschrWrapper.formBeschr, "Allgemein")

        self.ui.tabWidget.setCurrentIndex(0)

        for i in range(self.ui.tabWidget.tabBar().count()):
            self.ui.tabWidget.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))

        self.ui.tabWidget.setStyleSheet('QTabBar { font-weight: bold; font-size: ' + str(Wolke.Settings["FontHeadingSize"]) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')

        self.ui.chkKultur.stateChanged.connect(lambda state: self.ui.leKultur.setEnabled(self.ui.chkKultur.isChecked()))

        self.ui.leProfession.textChanged.connect(self.update)
        self.ui.leGeschlecht.textChanged.connect(self.update)
        self.ui.leGeburtsdatum.textChanged.connect(self.update)
        self.ui.leGroesse.textChanged.connect(self.update)
        self.ui.leGewicht.textChanged.connect(self.update)
        self.ui.leHaarfarbe.textChanged.connect(self.update)
        self.ui.leAugenfarbe.textChanged.connect(self.update)
        self.ui.leTitel.textChanged.connect(self.update)

        self.ui.leAussehen1.textChanged.connect(self.update)
        self.ui.leAussehen2.textChanged.connect(self.update)
        self.ui.leAussehen3.textChanged.connect(self.update)
        self.ui.leAussehen4.textChanged.connect(self.update)
        self.ui.leAussehen5.textChanged.connect(self.update)
        self.ui.leAussehen6.textChanged.connect(self.update)

        self.ui.leHintergrund0.textChanged.connect(self.update)
        self.ui.leHintergrund1.textChanged.connect(self.update)
        self.ui.leHintergrund2.textChanged.connect(self.update)
        self.ui.leHintergrund3.textChanged.connect(self.update)
        self.ui.leHintergrund4.textChanged.connect(self.update)
        self.ui.leHintergrund5.textChanged.connect(self.update)
        self.ui.leHintergrund6.textChanged.connect(self.update)
        self.ui.leHintergrund7.textChanged.connect(self.update)
        self.ui.leHintergrund8.textChanged.connect(self.update)

        self.characterImage = None
        self.labelImageText = self.ui.labelImage.text()
        self.ui.buttonLoadImage.clicked.connect(self.buttonLoadImageClicked)
        self.ui.buttonDeleteImage.clicked.connect(self.buttonDeleteImageClicked)

        self.currentlyLoading = False

    def load(self):
        self.currentlyLoading = True
        self.beschrWrapper.load()

        if Wolke.Char.kultur:
            self.ui.chkKultur.setChecked(True)
            self.ui.leKultur.setText(Wolke.Char.kultur)

        self.ui.leProfession.setText(Wolke.Char.profession)
        self.ui.leGeschlecht.setText(Wolke.Char.geschlecht)
        self.ui.leGeburtsdatum.setText(Wolke.Char.geburtsdatum)
        self.ui.leGroesse.setText(Wolke.Char.groesse)
        self.ui.leGewicht.setText(Wolke.Char.gewicht)
        self.ui.leHaarfarbe.setText(Wolke.Char.haarfarbe)
        self.ui.leAugenfarbe.setText(Wolke.Char.augenfarbe)
        self.ui.leTitel.setText(Wolke.Char.titel)

        self.ui.leAussehen1.setText(Wolke.Char.aussehen1)
        self.ui.leAussehen2.setText(Wolke.Char.aussehen2)
        self.ui.leAussehen3.setText(Wolke.Char.aussehen3)
        self.ui.leAussehen4.setText(Wolke.Char.aussehen4)
        self.ui.leAussehen5.setText(Wolke.Char.aussehen5)
        self.ui.leAussehen6.setText(Wolke.Char.aussehen6)

        self.ui.leHintergrund0.setText(Wolke.Char.hintergrund0)
        self.ui.leHintergrund1.setText(Wolke.Char.hintergrund1)
        self.ui.leHintergrund2.setText(Wolke.Char.hintergrund2)
        self.ui.leHintergrund3.setText(Wolke.Char.hintergrund3)
        self.ui.leHintergrund4.setText(Wolke.Char.hintergrund4)
        self.ui.leHintergrund5.setText(Wolke.Char.hintergrund5)
        self.ui.leHintergrund6.setText(Wolke.Char.hintergrund6)
        self.ui.leHintergrund7.setText(Wolke.Char.hintergrund7)
        self.ui.leHintergrund8.setText(Wolke.Char.hintergrund8)

        if Wolke.Char.bild:
            self.characterImage = QtGui.QPixmap()
            self.characterImage.loadFromData(Wolke.Char.bild)
            self.setImage(self.characterImage)

        self.currentlyLoading = False

    def update(self):
        if self.currentlyLoading:
            return

        self.beschrWrapper.update()

        if self.ui.chkKultur.isChecked():
            Wolke.Char.kultur = self.ui.leKultur.text()
        else:
            Wolke.Char.kultur = ""

        Wolke.Char.profession = self.ui.leProfession.text()
        Wolke.Char.geschlecht = self.ui.leGeschlecht.text()
        Wolke.Char.geburtsdatum = self.ui.leGeburtsdatum.text()
        Wolke.Char.groesse = self.ui.leGroesse.text()
        Wolke.Char.gewicht = self.ui.leGewicht.text()
        Wolke.Char.haarfarbe = self.ui.leHaarfarbe.text()
        Wolke.Char.augenfarbe = self.ui.leAugenfarbe.text()
        Wolke.Char.titel = self.ui.leTitel.text()

        Wolke.Char.aussehen1 = self.ui.leAussehen1.text()
        Wolke.Char.aussehen2 = self.ui.leAussehen2.text()
        Wolke.Char.aussehen3 = self.ui.leAussehen3.text()
        Wolke.Char.aussehen4 = self.ui.leAussehen4.text()
        Wolke.Char.aussehen5 = self.ui.leAussehen5.text()
        Wolke.Char.aussehen6 = self.ui.leAussehen6.text()

        Wolke.Char.hintergrund0 = self.ui.leHintergrund0.text()
        Wolke.Char.hintergrund1 = self.ui.leHintergrund1.text()
        Wolke.Char.hintergrund2 = self.ui.leHintergrund2.text()
        Wolke.Char.hintergrund3 = self.ui.leHintergrund3.text()
        Wolke.Char.hintergrund4 = self.ui.leHintergrund4.text()
        Wolke.Char.hintergrund5 = self.ui.leHintergrund5.text()
        Wolke.Char.hintergrund6 = self.ui.leHintergrund6.text()
        Wolke.Char.hintergrund7 = self.ui.leHintergrund7.text()
        Wolke.Char.hintergrund8 = self.ui.leHintergrund8.text()

        if self.ui.labelImage.pixmap():
            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QIODevice.WriteOnly);
            self.characterImage.save(buffer, "JPG")
            Wolke.Char.bild = buffer.data()
        else:
            Wolke.Char.bild = None

        self.modified.emit()

    def setImage(self, pixmap):
        self.ui.labelImage.setPixmap(pixmap.scaled(self.ui.labelImage.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def buttonLoadImageClicked(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Bild laden...", "", "Bild Dateien (*.png *.jpg *.bmp)")
        if spath == "":
            return
        
        self.characterImage = QPixmap(spath).scaled(QtCore.QSize(260, 340), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setImage(self.characterImage)

    def buttonDeleteImageClicked(self):
        self.characterImage = None
        self.ui.labelImage.setPixmap(QPixmap())
        self.ui.labelImage.setText(self.labelImageText)