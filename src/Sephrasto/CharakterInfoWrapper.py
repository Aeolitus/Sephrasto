# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 15:58:13 2017

@author: Lennart
"""

from Wolke import Wolke
import UI.CharakterInfo
from PySide6 import QtWidgets, QtCore, QtGui
import logging
from EinstellungenWrapper import EinstellungenWrapper
import os
from EventBus import EventBus

class FocusWatcher(QtCore.QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obje, even):
        if type(even) == QtGui.QFocusEvent:
            if not obje.hasFocus():
                self.callback()
        return False

class InfoWrapper(QtCore.QObject):
    '''
    Wrapper class for the EP Reference GUI. Contains methods for updating
    the GUI elements to the current values.
    '''
    modified = QtCore.Signal()

    def __init__(self):
        ''' Initialize the GUI and set signals for the spinners'''
        super().__init__()
        logging.debug("Initializing InfoWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterInfo.Ui_Form()
        self.ui.setupUi(self.form)

        self.ui.labelReload.setVisible(False)

        self.ui.comboHausregeln.addItems(EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"]))
        self.ui.checkFinanzen.stateChanged.connect(self.einstellungenChanged)
        self.ui.checkUeberPDF.stateChanged.connect(self.einstellungenChanged)
        self.ui.checkRegeln.stateChanged.connect(self.einstellungenChanged)
        self.ui.comboHausregeln.currentIndexChanged.connect(self.einstellungenChanged)

        boegen = [os.path.basename(os.path.splitext(bogen)[0]) for bogen in Wolke.Charakterbögen]
        for bogen in boegen:
            if bogen == "Standard Charakterbogen":
                self.ui.comboCharsheet.insertItem(0, bogen)
            elif bogen == "Langer Charakterbogen":
                self.ui.comboCharsheet.insertItem(0, bogen)
            else:
                self.ui.comboCharsheet.addItem(bogen)
        if not (Wolke.Char.charakterbogen in boegen):
            Wolke.Char.charakterbogen = self.ui.comboCharsheet.itemText(0)
        self.ui.comboCharsheet.currentIndexChanged.connect(self.einstellungenChanged)
        self.ui.comboRegelnGroesse.currentIndexChanged.connect(self.einstellungenChanged)
        self.ui.checkReq.stateChanged.connect(self.reqChanged)

        self.focusWatcher = FocusWatcher(self.notizChanged)
        self.ui.teNotiz.installEventFilter(self.focusWatcher)

        self.initialHausregeln = Wolke.Char.hausregeln

        self.initialDetails = False
        for bogen in Wolke.Charakterbögen:
            if Wolke.Char.charakterbogen == os.path.basename(os.path.splitext(bogen)[0]):
                self.initialDetails = Wolke.Charakterbögen[bogen].beschreibungDetails
                break

        self.ui.comboRegelnGroesse.setEnabled(Wolke.Char.regelnAnhaengen)
        self.ui.listRegelKategorien.setEnabled(Wolke.Char.regelnAnhaengen)

        vorteilTypen = Wolke.DB.einstellungen["Vorteile: Typen"].toTextList()
        manöverTypen = Wolke.DB.einstellungen["Manöver: Typen"].toTextList()
        self.regelKategorien = []
        for r in Wolke.DB.einstellungen["Regelanhang: Reihenfolge"].toTextList():
            if r[0] == "V":
                typ = int(r[1:])
                self.regelKategorien.append([vorteilTypen[typ], r])
            elif r[0] == "M":
                typ = int(r[1:])
                self.regelKategorien.append([manöverTypen[typ], r])
            elif r[0] == "W":
                self.regelKategorien.append(["Waffeneigenschaften", r])
            elif r[0] == "Z":
                self.regelKategorien.append(["Zauber", r])
            elif r[0] == "L":
                self.regelKategorien.append(["Liturgien", r])
            elif r[0] == "A":
                self.regelKategorien.append(["Anrufungen", r])
            else:
                name = EventBus.applyFilter("regelanhang_reihenfolge_name", r)
                self.regelKategorien.append([name, r])

        model = QtGui.QStandardItemModel(self.ui.listRegelKategorien)
        for kategorie in self.regelKategorien:
            item = QtGui.QStandardItem(kategorie[0])
            item.setCheckable(True)
            if kategorie[1] in Wolke.Char.regelnKategorien:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            model.appendRow(item)

        self.ui.listRegelKategorien.setModel(model)
        self.ui.listRegelKategorien.model().dataChanged.connect(self.regelKategorienChanged)

        self.currentlyLoading = False

    def update(self):
        pass

    def reqChanged(self):
        if self.currentlyLoading:
            return

        Wolke.Char.voraussetzungenPruefen = self.ui.checkReq.isChecked()
        self.modified.emit()

    def regelKategorienChanged(self):
        aktiveKategorien = []

        for i in range(self.ui.listRegelKategorien.model().rowCount()):
            item = self.ui.listRegelKategorien.model().item(i)
            if item.checkState() == QtCore.Qt.Checked:
                aktiveKategorien.append(self.regelKategorien[i][1])

        Wolke.Char.regelnKategorien = aktiveKategorien
        self.modified.emit()

    def einstellungenChanged(self):
        if self.currentlyLoading:
            return
        Wolke.Char.finanzenAnzeigen = self.ui.checkFinanzen.isChecked()
        Wolke.Char.ueberPDFAnzeigen = self.ui.checkUeberPDF.isChecked()
        Wolke.Char.regelnAnhaengen = self.ui.checkRegeln.isChecked()
        Wolke.Char.regelnGroesse = self.ui.comboRegelnGroesse.currentIndex()
        Wolke.Char.hausregeln = self.ui.comboHausregeln.currentText() if self.ui.comboHausregeln.currentText() != "Keine" else None
        Wolke.Char.charakterbogen = self.ui.comboCharsheet.currentText()

        details = False
        for bogen in Wolke.Charakterbögen:
            if Wolke.Char.charakterbogen == os.path.basename(os.path.splitext(bogen)[0]):
                details = Wolke.Charakterbögen[bogen].beschreibungDetails
                break

        self.ui.labelReload.setVisible(Wolke.Char.hausregeln != self.initialHausregeln or self.initialDetails != details)

        self.ui.comboRegelnGroesse.setEnabled(Wolke.Char.regelnAnhaengen)
        self.ui.listRegelKategorien.setEnabled(Wolke.Char.regelnAnhaengen)

        self.modified.emit()

    def load(self):
        self.currentlyLoading = True
        self.ui.teNotiz.setPlainText(Wolke.Char.notiz)

        self.ui.checkReq.setChecked(Wolke.Char.voraussetzungenPruefen)
        self.ui.checkFinanzen.setChecked(Wolke.Char.finanzenAnzeigen)
        self.ui.checkUeberPDF.setChecked(Wolke.Char.ueberPDFAnzeigen)
        self.ui.checkRegeln.setChecked(Wolke.Char.regelnAnhaengen)
        self.ui.comboRegelnGroesse.setCurrentIndex(Wolke.Char.regelnGroesse)
        self.ui.comboHausregeln.setCurrentText(Wolke.Char.hausregeln or "Keine")
        self.ui.comboCharsheet.setCurrentText(Wolke.Char.charakterbogen)

        ''' Load all values and derived values '''
        totalVal = 0
        if Wolke.Char.EPtotal > 0:
            totalVal = Wolke.Char.EPtotal
        else:
            totalVal = Wolke.Char.EPspent
        if totalVal == 0:
            totalVal = 1

        self.ui.spinAttributeSpent.setValue(Wolke.Char.EP_Attribute)
        self.ui.spinAttributePercent.setValue(round(Wolke.Char.EP_Attribute / totalVal * 100))

        self.ui.spinVorteileSpent.setValue(Wolke.Char.EP_Vorteile)
        self.ui.spinVorteilePercent.setValue(round(Wolke.Char.EP_Vorteile / totalVal * 100))

        total = Wolke.Char.EP_Fertigkeiten + Wolke.Char.EP_Fertigkeiten_Talente + Wolke.Char.EP_FreieFertigkeiten

        self.ui.spinProfanSpent.setValue(total)
        self.ui.spinProfanPercent.setValue(round(total / totalVal * 100))

        self.ui.spinFertigkeitenSpent.setValue(Wolke.Char.EP_Fertigkeiten)
        self.ui.spinFertigkeitenPercent.setValue(round(Wolke.Char.EP_Fertigkeiten / max(total, 1) * 100))

        self.ui.spinTalenteSpent.setValue(Wolke.Char.EP_Fertigkeiten_Talente)
        self.ui.spinTalentePercent.setValue(round(Wolke.Char.EP_Fertigkeiten_Talente / max(total, 1) * 100))

        self.ui.spinFreieSpent.setValue(Wolke.Char.EP_FreieFertigkeiten)
        self.ui.spinFreiePercent.setValue(round(Wolke.Char.EP_FreieFertigkeiten / max(total, 1) * 100))

        if Wolke.Char.EP_Uebernatuerlich + Wolke.Char.EP_Uebernatuerlich_Talente > 0:
            self.ui.spinUebernatuerlichSpent.show()
            self.ui.spinUebernatuerlichPercent.show()
            self.ui.spinUeberFertigkeitenSpent.show()
            self.ui.spinUeberFertigkeitenPercent.show()
            self.ui.spinUeberTalenteSpent.show()
            self.ui.spinUeberTalentePercent.show()
            self.ui.labelUeber1.show()
            self.ui.labelUeber2.show()
            self.ui.labelUeber3.show()

            total = Wolke.Char.EP_Uebernatuerlich + Wolke.Char.EP_Uebernatuerlich_Talente

            self.ui.spinUebernatuerlichSpent.setValue(total)
            self.ui.spinUebernatuerlichPercent.setValue(round(total / totalVal * 100))

            self.ui.spinUeberFertigkeitenSpent.setValue(Wolke.Char.EP_Uebernatuerlich)
            self.ui.spinUeberFertigkeitenPercent.setValue(round(Wolke.Char.EP_Uebernatuerlich / max(total, 1) * 100))

            self.ui.spinUeberTalenteSpent.setValue(Wolke.Char.EP_Uebernatuerlich_Talente)
            self.ui.spinUeberTalentePercent.setValue(round(Wolke.Char.EP_Uebernatuerlich_Talente / max(total, 1) * 100))
        else:
            self.ui.spinUebernatuerlichSpent.hide()
            self.ui.spinUebernatuerlichPercent.hide()
            self.ui.spinUeberFertigkeitenSpent.hide()
            self.ui.spinUeberFertigkeitenPercent.hide()
            self.ui.spinUeberTalenteSpent.hide()
            self.ui.spinUeberTalentePercent.hide()
            self.ui.labelUeber1.hide()
            self.ui.labelUeber2.hide()
            self.ui.labelUeber3.hide()

        self.currentlyLoading = False

    def notizChanged(self):
        if self.currentlyLoading:
            return
        
        if Wolke.Char.notiz != self.ui.teNotiz.toPlainText():
            Wolke.Char.notiz = self.ui.teNotiz.toPlainText()
            self.modified.emit()