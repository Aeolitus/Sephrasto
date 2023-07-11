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
from Hilfsmethoden import Hilfsmethoden
import copy

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
        self.ui.checkFormular.stateChanged.connect(self.einstellungenChanged)
        self.ui.checkDetails.stateChanged.connect(self.einstellungenChanged)

        boegen = [bogen for bogen in Wolke.Charakterbögen]
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
        self.ui.spinRegelnGroesse.valueChanged.connect(self.einstellungenChanged)
        self.ui.checkReq.stateChanged.connect(self.reqChanged)

        self.ui.buttonRegeln.setText('\uf0ae')
        self.ui.buttonRegeln.clicked.connect(self.showRegelKategorien)
        self.ui.buttonRegeln.setEnabled(Wolke.Char.regelnAnhaengen)
        self.focusWatcher = FocusWatcher(self.notizChanged)
        self.ui.teNotiz.installEventFilter(self.focusWatcher)

        self.ui.spinRegelnGroesse.setEnabled(Wolke.Char.regelnAnhaengen)

        self.currentlyLoading = False

    def update(self):
        pass

    def reqChanged(self):
        if self.currentlyLoading:
            return

        Wolke.Char.voraussetzungenPruefen = self.ui.checkReq.isChecked()
        self.modified.emit()

    @staticmethod
    def getCharakterbogen(name):
        if name in Wolke.Charakterbögen:
            return Wolke.Charakterbögen[name]
        return None

    def einstellungenChanged(self):
        if self.currentlyLoading:
            return
        Wolke.Char.finanzenAnzeigen = self.ui.checkFinanzen.isChecked()
        Wolke.Char.ueberPDFAnzeigen = self.ui.checkUeberPDF.isChecked()
        Wolke.Char.regelnAnhaengen = self.ui.checkRegeln.isChecked()
        Wolke.Char.detailsAnzeigen = self.ui.checkDetails.isChecked()
        Wolke.Char.regelnGroesse = self.ui.spinRegelnGroesse.value()
        Wolke.Char.charakterbogen = self.ui.comboCharsheet.currentText()
        Wolke.Char.formularEditierbar = self.ui.checkFormular.isChecked()

        cbi = InfoWrapper.getCharakterbogen(Wolke.Char.charakterbogen)
        if cbi:
            self.ui.comboCharsheet.setToolTip(cbi.info)

        if self.ui.comboHausregeln.currentText() == Wolke.DB.hausregelnAnzeigeName:
            self.ui.labelReload.setVisible(False)
            Wolke.Char.neueHausregeln = None
        else:
            self.ui.labelReload.setVisible(True)
            Wolke.Char.neueHausregeln = self.ui.comboHausregeln.currentText()

        self.ui.spinRegelnGroesse.setEnabled(Wolke.Char.regelnAnhaengen)
        self.ui.buttonRegeln.setEnabled(Wolke.Char.regelnAnhaengen)

        self.modified.emit()

    def load(self):
        self.currentlyLoading = True
        self.ui.teNotiz.setPlainText(Wolke.Char.notiz)

        self.ui.checkReq.setChecked(Wolke.Char.voraussetzungenPruefen)
        self.ui.checkFinanzen.setChecked(Wolke.Char.finanzenAnzeigen)
        self.ui.checkUeberPDF.setChecked(Wolke.Char.ueberPDFAnzeigen)
        self.ui.checkRegeln.setChecked(Wolke.Char.regelnAnhaengen)
        self.ui.checkDetails.setChecked(Wolke.Char.detailsAnzeigen)
        self.ui.spinRegelnGroesse.setValue(Wolke.Char.regelnGroesse)
        self.ui.comboHausregeln.setCurrentText(Wolke.DB.hausregelnAnzeigeName)
        self.ui.comboCharsheet.setCurrentText(Wolke.Char.charakterbogen)
        cbi = InfoWrapper.getCharakterbogen(Wolke.Char.charakterbogen)
        if cbi:
            self.ui.comboCharsheet.setToolTip(cbi.info)
        self.ui.checkFormular.setChecked(Wolke.Char.formularEditierbar)

        ''' Load all values and derived values '''
        totalVal = 0
        if Wolke.Char.epGesamt > 0:
            totalVal = Wolke.Char.epGesamt
        else:
            totalVal = Wolke.Char.epAusgegeben
        if totalVal == 0:
            totalVal = 1

        self.ui.spinAttributeSpent.setValue(Wolke.Char.epAttribute)
        self.ui.spinAttributePercent.setValue(round(Wolke.Char.epAttribute / totalVal * 100))

        self.ui.spinVorteileSpent.setValue(Wolke.Char.epVorteile)
        self.ui.spinVorteilePercent.setValue(round(Wolke.Char.epVorteile / totalVal * 100))

        total = Wolke.Char.epFertigkeiten + Wolke.Char.epFertigkeitenTalente + Wolke.Char.epFreieFertigkeiten

        self.ui.spinProfanSpent.setValue(total)
        self.ui.spinProfanPercent.setValue(round(total / totalVal * 100))

        self.ui.spinFertigkeitenSpent.setValue(Wolke.Char.epFertigkeiten)
        self.ui.spinFertigkeitenPercent.setValue(round(Wolke.Char.epFertigkeiten / max(total, 1) * 100))

        self.ui.spinTalenteSpent.setValue(Wolke.Char.epFertigkeitenTalente)
        self.ui.spinTalentePercent.setValue(round(Wolke.Char.epFertigkeitenTalente / max(total, 1) * 100))

        self.ui.spinFreieSpent.setValue(Wolke.Char.epFreieFertigkeiten)
        self.ui.spinFreiePercent.setValue(round(Wolke.Char.epFreieFertigkeiten / max(total, 1) * 100))

        if Wolke.Char.epÜbernatürlich + Wolke.Char.epÜbernatürlichTalente > 0:
            self.ui.spinUebernatuerlichSpent.show()
            self.ui.spinUebernatuerlichPercent.show()
            self.ui.spinUeberFertigkeitenSpent.show()
            self.ui.spinUeberFertigkeitenPercent.show()
            self.ui.spinUeberTalenteSpent.show()
            self.ui.spinUeberTalentePercent.show()
            self.ui.labelUeber1.show()
            self.ui.labelUeber2.show()
            self.ui.labelUeber3.show()

            total = Wolke.Char.epÜbernatürlich + Wolke.Char.epÜbernatürlichTalente

            self.ui.spinUebernatuerlichSpent.setValue(total)
            self.ui.spinUebernatuerlichPercent.setValue(round(total / totalVal * 100))

            self.ui.spinUeberFertigkeitenSpent.setValue(Wolke.Char.epÜbernatürlich)
            self.ui.spinUeberFertigkeitenPercent.setValue(round(Wolke.Char.epÜbernatürlich / max(total, 1) * 100))

            self.ui.spinUeberTalenteSpent.setValue(Wolke.Char.epÜbernatürlichTalente)
            self.ui.spinUeberTalentePercent.setValue(round(Wolke.Char.epÜbernatürlichTalente / max(total, 1) * 100))
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

    def showRegelKategorien(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Regelanhang Auswahl")
        rootLayout = QtWidgets.QVBoxLayout()

        tree = QtWidgets.QTreeWidget()
        rootLayout.addWidget(tree)

        vorteilTypen = Wolke.DB.einstellungen["Vorteile: Typen"].wert
        regelnTypen = Wolke.DB.einstellungen["Regeln: Typen"].wert
        spezialTalentTypen = list(Wolke.DB.einstellungen["Talente: Spezialtalent Typen"].wert.values())

        def createItem(parent, name, cat):
            if isinstance(parent, QtWidgets.QTreeWidgetItem) and parent.text(0) == name:
                parent.setData(0, QtCore.Qt.UserRole, cat)
                if cat in Wolke.Char.deaktivierteRegelKategorien:
                    parent.setCheckState(0, QtCore.Qt.Unchecked)
                return parent

            item = QtWidgets.QTreeWidgetItem(parent)
            item.setText(0, name)
            item.setData(0, QtCore.Qt.UserRole, cat)
            if cat in Wolke.Char.deaktivierteRegelKategorien:
                item.setCheckState(0, QtCore.Qt.Unchecked)
            else:
                item.setCheckState(0, QtCore.Qt.Checked)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsAutoTristate)
            return item

        parent = tree
        for r in Wolke.DB.einstellungen["Regelanhang: Reihenfolge"].wert:
            if r[0] == "T" and len(r) > 2:
                parent = QtWidgets.QTreeWidgetItem(tree)
                parent.setText(0, r[2:])
                parent.setExpanded(True)
                parent.setCheckState(0, QtCore.Qt.Checked)
                parent.setFlags(parent.flags() | QtCore.Qt.ItemIsAutoTristate)
            elif r[0] == "V" and len(r) > 2 and r[2:].isnumeric():
                typ = int(r[2:])
                item = createItem(parent, vorteilTypen[typ], r)
                for v in Wolke.Char.vorteile.values():
                    if v.cheatsheetAuflisten and v.typ == typ:
                        createItem(item, v.name, "V:" + v.name)
            elif r[0] == "R" and len(r) > 2 and r[2:].isnumeric():
                typ = int(r[2:])
                item = createItem(parent, regelnTypen[typ], r)
                for r in Wolke.DB.regeln.values():
                    if r.typ == typ and Wolke.Char.voraussetzungenPrüfen(r):
                        createItem(item, r.anzeigename, "R:" + r.name)
            elif r[0] == "W":
                createItem(parent, "Waffeneigenschaften", r)
            elif r[0] == "S" and len(r) > 2 and r[2:].isnumeric():
                typ = int(r[2:])
                item = createItem(parent, spezialTalentTypen[typ], r)
                for t in Wolke.Char.talente.values():
                    if t.cheatsheetAuflisten and t.spezialTyp == typ:
                        createItem(item, t.anzeigename, "S:" + t.name)
            else:
                name = EventBus.applyFilter("regelanhang_reihenfolge_name", r)
                createItem(parent, name, r)

        tree.setHeaderHidden(True)
        tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)


        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.addButton("OK", QtWidgets.QDialogButtonBox.YesRole).clicked.connect(lambda: dialog.accept())
        buttonBox.addButton("Abbrechen", QtWidgets.QDialogButtonBox.RejectRole).clicked.connect(lambda: dialog.reject())
        rootLayout.addWidget(buttonBox)

        dialog.setLayout(rootLayout)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        windowSize = Wolke.Settings["WindowSize-Regelanhang"]
        dialog.resize(windowSize[0], windowSize[1])
        dialog.show()
        accepted = dialog.exec() == QtWidgets.QDialog.Accepted
        Wolke.Settings["WindowSize-Regelanhang"] = [dialog.size().width(), dialog.size().height()]
        if accepted:
            Wolke.Char.deaktivierteRegelKategorien = []
            for i in range(tree.topLevelItemCount()):
                parent = tree.topLevelItem(i)
                if parent.childCount() == 0:
                    if parent.checkState(0) == QtCore.Qt.Unchecked:
                        Wolke.Char.deaktivierteRegelKategorien.append(parent.data(0, QtCore.Qt.UserRole))
                else:
                    for j in range(parent.childCount()):
                        child = parent.child(j)
                        if child.checkState(0) == QtCore.Qt.Unchecked:
                            Wolke.Char.deaktivierteRegelKategorien.append(child.data(0, QtCore.Qt.UserRole))
                        for k in range(child.childCount()):
                            actualElement = child.child(k)
                            if actualElement.checkState(0) == QtCore.Qt.Unchecked:
                                Wolke.Char.deaktivierteRegelKategorien.append(actualElement.data(0, QtCore.Qt.UserRole))
            self.modified.emit()