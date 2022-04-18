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
            self.beschrWrapper.modified.connect(lambda: self.modified.emit())
            self.ui.tabWidget.insertTab(0, self.beschrWrapper.form, "Allgemein")

        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget.currentChanged.connect(self.load)

        for i in range(self.ui.tabWidget.tabBar().count()):
            self.ui.tabWidget.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))

        self.ui.tabWidget.setStyleSheet('QTabBar { font-weight: bold; font-size: ' + str(Wolke.Settings["FontHeadingSize"]) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')

        self.ui.chkKultur.stateChanged.connect(self.updateDetails)

        self.ui.leKultur.editingFinished.connect(self.updateDetails)
        self.ui.leProfession.editingFinished.connect(self.updateDetails)
        self.ui.leGeschlecht.editingFinished.connect(self.updateDetails)
        self.ui.leGeburtsdatum.editingFinished.connect(self.updateDetails)
        self.ui.leGroesse.editingFinished.connect(self.updateDetails)
        self.ui.leGewicht.editingFinished.connect(self.updateDetails)
        self.ui.leHaarfarbe.editingFinished.connect(self.updateDetails)
        self.ui.leAugenfarbe.editingFinished.connect(self.updateDetails)
        self.ui.leTitel.editingFinished.connect(self.updateDetails)

        self.ui.leAussehen1.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen2.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen3.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen4.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen5.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen6.editingFinished.connect(self.updateDetails)

        self.ui.leHintergrund0.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund1.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund2.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund3.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund4.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund5.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund6.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund7.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund8.editingFinished.connect(self.updateDetails)

        self.characterImage = None
        self.labelImageText = self.ui.labelImage.text()
        self.ui.buttonLoadImage.clicked.connect(self.buttonLoadImageClicked)
        self.ui.buttonDeleteImage.clicked.connect(self.buttonDeleteImageClicked)

        self.currentlyLoading = False

    def load(self):
        if hasattr(self, "beschrWrapper") and self.ui.tabWidget.currentWidget() == self.beschrWrapper.form:
            self.beschrWrapper.load()
        elif self.ui.tabWidget.currentWidget() == self.ui.tab_2:
            self.currentlyLoading = True

            if Wolke.Char.kultur:
                self.ui.chkKultur.setChecked(True)
                self.ui.leKultur.setText(Wolke.Char.kultur)

            self.ui.leKultur.setEnabled(self.ui.chkKultur.isChecked())

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

    def updateDetails(self):
        if self.currentlyLoading:
            return

        changed = False

        self.ui.leKultur.setEnabled(self.ui.chkKultur.isChecked())
        if self.ui.chkKultur.isChecked():
            if Wolke.Char.kultur != self.ui.leKultur.text():
                Wolke.Char.kultur = self.ui.leKultur.text()
                changed = True
        else:
            if Wolke.Char.kultur:
                Wolke.Char.kultur = ""
                changed = True

        if Wolke.Char.profession != self.ui.leProfession.text():
            Wolke.Char.profession = self.ui.leProfession.text()
            changed = True
        if Wolke.Char.geschlecht != self.ui.leGeschlecht.text():
            Wolke.Char.geschlecht = self.ui.leGeschlecht.text()
            changed = True
        if Wolke.Char.geburtsdatum != self.ui.leGeburtsdatum.text():
            Wolke.Char.geburtsdatum = self.ui.leGeburtsdatum.text()
            changed = True
        if Wolke.Char.groesse != self.ui.leGroesse.text():
            Wolke.Char.groesse = self.ui.leGroesse.text()
            changed = True
        if Wolke.Char.gewicht != self.ui.leGewicht.text():
            Wolke.Char.gewicht = self.ui.leGewicht.text()
            changed = True
        if Wolke.Char.haarfarbe != self.ui.leHaarfarbe.text():
            Wolke.Char.haarfarbe = self.ui.leHaarfarbe.text()
            changed = True
        if Wolke.Char.augenfarbe != self.ui.leAugenfarbe.text():
            Wolke.Char.augenfarbe = self.ui.leAugenfarbe.text()
            changed = True
        if Wolke.Char.titel != self.ui.leTitel.text():
            Wolke.Char.titel = self.ui.leTitel.text()
            changed = True

        if Wolke.Char.aussehen1 != self.ui.leAussehen1.text():
            Wolke.Char.aussehen1 = self.ui.leAussehen1.text()
            changed = True
        if Wolke.Char.aussehen2 != self.ui.leAussehen2.text():
            Wolke.Char.aussehen2 = self.ui.leAussehen2.text()
            changed = True
        if Wolke.Char.aussehen3 != self.ui.leAussehen3.text():
            Wolke.Char.aussehen3 = self.ui.leAussehen3.text()
            changed = True
        if Wolke.Char.aussehen4 != self.ui.leAussehen4.text():
            Wolke.Char.aussehen4 = self.ui.leAussehen4.text()
            changed = True
        if Wolke.Char.aussehen5 != self.ui.leAussehen5.text():
            Wolke.Char.aussehen5 = self.ui.leAussehen5.text()
            changed = True
        if Wolke.Char.aussehen6 != self.ui.leAussehen6.text():
            Wolke.Char.aussehen6 = self.ui.leAussehen6.text()
            changed = True

        if Wolke.Char.hintergrund0 != self.ui.leHintergrund0.text():
            Wolke.Char.hintergrund0 = self.ui.leHintergrund0.text()
            changed = True
        if Wolke.Char.hintergrund1 != self.ui.leHintergrund1.text():
            Wolke.Char.hintergrund1 = self.ui.leHintergrund1.text()
            changed = True
        if Wolke.Char.hintergrund2 != self.ui.leHintergrund2.text():
            Wolke.Char.hintergrund2 = self.ui.leHintergrund2.text()
            changed = True
        if Wolke.Char.hintergrund3 != self.ui.leHintergrund3.text():
            Wolke.Char.hintergrund3 = self.ui.leHintergrund3.text()
            changed = True
        if Wolke.Char.hintergrund4 != self.ui.leHintergrund4.text():
            Wolke.Char.hintergrund4 = self.ui.leHintergrund4.text()
            changed = True
        if Wolke.Char.hintergrund5 != self.ui.leHintergrund5.text():
            Wolke.Char.hintergrund5 = self.ui.leHintergrund5.text()
            changed = True
        if Wolke.Char.hintergrund6 != self.ui.leHintergrund6.text():
            Wolke.Char.hintergrund6 = self.ui.leHintergrund6.text()
            changed = True
        if Wolke.Char.hintergrund7 != self.ui.leHintergrund7.text():
            Wolke.Char.hintergrund7 = self.ui.leHintergrund7.text()
            changed = True
        if Wolke.Char.hintergrund8 != self.ui.leHintergrund8.text():
            Wolke.Char.hintergrund8 = self.ui.leHintergrund8.text()
            changed = True

        if changed:
            self.modified.emit()

    def setImage(self, pixmap):
        self.ui.labelImage.setPixmap(pixmap.scaled(self.ui.labelImage.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def buttonLoadImageClicked(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Bild laden...", "", "Bild Dateien (*.png *.jpg *.bmp)")
        if spath == "":
            return
        
        self.characterImage = QPixmap(spath).scaled(QtCore.QSize(260, 340), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setImage(self.characterImage)

        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.WriteOnly);
        self.characterImage.save(buffer, "JPG")
        imageDdata = buffer.data()
        if Wolke.Char.bild != imageDdata:
            Wolke.Char.bild = imageDdata
            self.modified.emit()

    def buttonDeleteImageClicked(self):
        self.characterImage = None
        self.ui.labelImage.setPixmap(QPixmap())
        self.ui.labelImage.setText(self.labelImageText)

        if Wolke.Char.bild != None:
            Wolke.Char.bild = None
            self.modified.emit()