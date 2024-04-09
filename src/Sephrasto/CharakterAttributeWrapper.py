# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:21:49 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterAttribute
from PySide6 import QtWidgets, QtCore, QtGui
import logging
import copy
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus

class AttrWrapper(QtCore.QObject):
    ''' 
    Wrapper class for the Attribute setting GUI. Contains methods for updating
    the GUI elements to the current values and for changing the current values
    to the values set by the user. 
    '''
    modified = QtCore.Signal()
    
    def __init__(self):
        ''' Initialize the GUI and set signals for the spinners'''
        super().__init__()
        logging.debug("Initializing AttrWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterAttribute.Ui_formAttribute()
        self.ui.setupUi(self.form)

        # pre-sort and -filter vorteile to improve performance of tooltip generation
        self.vorteile = {}
        for attribut in Wolke.Char.attribute:
            self.vorteile[attribut] = []
        for vorteil in sorted(Wolke.DB.vorteile.values(), key = lambda v: v.kategorie):
            for attribut in Wolke.Char.attribute:
                if vorteil.voraussetzungen.isAttributVoraussetzung(attribut):
                    self.vorteile[attribut].append(vorteil)

        # Init Attribute
        self.widgetAttributVollerName = {}
        self.widgetAttributName = {}
        self.widgetAttributWert = {}
        self.widgetAttributPW = {}
        self.widgetAttributKosten = {}

        rowIndex = 1
        attribute = [a.name for a in sorted(Wolke.Char.attribute.values(), key=lambda value: value.sortorder)]
        for attribut in attribute:
            labelVollerName = QtWidgets.QLabel(Wolke.Char.attribute[attribut].anzeigename)
            font=QtGui.QFont()
            font.setBold(True)
            labelVollerName.setFont(font)
            labelVollerName.setToolTip(f"<html><head/><body><p>{Wolke.Char.attribute[attribut].text}</p></body></html>")
            self.ui.gridLayout.addWidget(labelVollerName, rowIndex, 0)
            self.widgetAttributVollerName[attribut] = labelVollerName

            labelName = QtWidgets.QLabel(attribut)
            font=QtGui.QFont()
            font.setItalic(True)
            labelName.setFont(font)
            labelName.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.ui.gridLayout.addWidget(labelName, rowIndex, 1)
            self.widgetAttributName[attribut] = labelName
            
            spinWert = QtWidgets.QSpinBox()
            spinWert.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            spinWert.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spinWert.setKeyboardTracking(False)
            spinWert.valueChanged.connect(self.update)
            self.ui.gridLayout.addWidget(spinWert, rowIndex, 2)
            self.widgetAttributWert[attribut] = spinWert
            
            spinPW = QtWidgets.QSpinBox() 
            spinPW.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            spinPW.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spinPW.setReadOnly(True)
            spinPW.setFocusPolicy(QtCore.Qt.NoFocus)
            self.ui.gridLayout.addWidget(spinPW, rowIndex, 3)
            self.widgetAttributPW[attribut] = spinPW

            labelKosten = QtWidgets.QLabel()
            self.ui.gridLayout.addWidget(labelKosten, rowIndex, 4)
            self.widgetAttributKosten[attribut] = labelKosten

            rowIndex += 1

        # Init Abgeleitete Werte
        self.widgetAbgeleitetVollerName = {}
        self.widgetAbgeleitetName = {}
        self.widgetAbgeleitetWert = {}
        self.widgetAbgeleitetKosten = {}

        rowIndex = 1
        abgeleiteteWerte = [a.name for a in sorted(Wolke.Char.abgeleiteteWerte.values(), key=lambda value: value.sortorder) if a.anzeigen]
        for ab in abgeleiteteWerte:
            labelVollerName = QtWidgets.QLabel(Wolke.Char.abgeleiteteWerte[ab].anzeigename)
            font=QtGui.QFont()
            font.setBold(True)
            labelVollerName.setFont(font)
            labelVollerName.setToolTip(f"<html><head/><body><p>{Wolke.DB.abgeleiteteWerte[ab].text}</p></body></html>")
            self.ui.gridLayout.addWidget(labelVollerName, rowIndex, 6)
            self.widgetAbgeleitetVollerName[ab] = labelVollerName

            labelName = QtWidgets.QLabel(ab)
            font=QtGui.QFont()
            font.setItalic(True)
            labelName.setFont(font)
            labelName.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.ui.gridLayout.addWidget(labelName, rowIndex, 7)
            self.widgetAbgeleitetName[ab] = labelName
            
            spinWert = QtWidgets.QSpinBox()
            spinWert.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            spinWert.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spinWert.setReadOnly(True)
            spinWert.setFocusPolicy(QtCore.Qt.NoFocus)
            self.ui.gridLayout.addWidget(spinWert, rowIndex, 8)
            self.widgetAbgeleitetWert[ab] = spinWert

            labelFormel = QtWidgets.QLabel(Wolke.Char.abgeleiteteWerte[ab].formel)
            self.ui.gridLayout.addWidget(labelFormel, rowIndex, 10)
            self.widgetAbgeleitetKosten[ab] = labelFormel

            rowIndex += 1

        # Init Energien (UI is generated in Load because energien have voraussetzungen that might change)
        self.energienStartIndex = rowIndex
        self.widgetEnergieVollerName = {}
        self.widgetEnergieName = {}
        self.widgetEnergieWert = {}
        self.widgetEnergiePlus = {}
        self.layoutEnergieZugekauft = {}
        self.widgetEnergieSpinZugekauft = {}
        self.widgetEnergieLabelZugekauft = {}
        self.widgetEnergieKosten = {}
        self.availableEnergien = []

        self.currentlyLoading = False
     
    def updateTooltip(self, attribut):
        attribute = copy.deepcopy(Wolke.Char.attribute)
        attribute[attribut].wert += 1
        attribute[attribut].aktualisieren()

        tooltip = "Eine Steigerung von " + attribut + " auf " + str(attribute[attribut].wert) + " bewirkt:\n"

        abgeleitetNew = []
        for aw in Wolke.Char.abgeleiteteWerte.values():
            if not aw.anzeigen:
                continue
            diff = aw.diffBasiswert(attribute)
            if diff != 0:
                abgeleitetNew.append(aw.anzeigename + (" +" if diff > 0 else " ") + str(diff))

        vortNew = []
        if Wolke.Char.voraussetzungenPruefen:
            for vort in self.vorteile[attribut]:
                if vort.name in Wolke.Char.vorteile:
                    continue
                elif Hilfsmethoden.voraussetzungenPrüfen(vort, Wolke.Char.vorteile, Wolke.Char.waffen, Wolke.Char.attribute, Wolke.Char.übernatürlicheFertigkeiten, Wolke.Char.fertigkeiten, Wolke.Char.talente):
                    continue
                elif Hilfsmethoden.voraussetzungenPrüfen(vort, Wolke.Char.vorteile, Wolke.Char.waffen, attribute, Wolke.Char.übernatürlicheFertigkeiten, Wolke.Char.fertigkeiten, Wolke.Char.talente):
                    vortNew.append(vort.name + " erwerbbar")

        fertNew = []
        for fert in sorted(Wolke.Char.fertigkeiten.values(), key = lambda f: f.kategorie):
            diff = fert.diffBasiswert(attribute)
            if diff != 0:
                fertNew.append(fert.name + " +" + str(diff))

        fertsÜberNew = []
        more = 0
        for fert in sorted(Wolke.Char.übernatürlicheFertigkeiten.values(), key = lambda f: f.kategorie):
            if len(fert.gekaufteTalente) == 0:
                more += 1
                continue
            diff = fert.diffBasiswert(attribute)
            if diff != 0:
                fertsÜberNew.append(fert.name + " +" + str(diff))
        if more > 0:
            fertsÜberNew.append(str(more) + " ungenutzte übernat. Fertigkeiten +1")

        tooltipAdd = []
        for infos in [abgeleitetNew, fertNew, fertsÜberNew, vortNew]:
            tooltipAdd += infos
            if len(infos) > 0:
                tooltipAdd.append("")

        if len(tooltipAdd) > 0:
            tooltipAdd.pop()
            tooltip += "\n".join(tooltipAdd)
        else:
            tooltip = tooltip[:-2] + " keine weiteren Verbesserungen."

        self.widgetAttributWert[attribut].setToolTip(tooltip)

    def checkConsequences(self, attribut, wert):
        attribute = copy.deepcopy(Wolke.Char.attribute)
        attribute[attribut].wert = wert
        attribute[attribut].aktualisieren()
        remove = Wolke.Char.findUnerfüllteVorteilVoraussetzungen(attribute=attribute)
        if remove:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Question)
            messageBox.setWindowTitle(attribut + " senken")
            messageBox.setText("Wenn du " + attribut + " auf " + str(wert) + " senkst, verlierst du die folgenden Vorteile:")
            remove.append("\nBist du sicher?")
            messageBox.setInformativeText("\n".join(remove))
            messageBox.addButton("Ja", QtWidgets.QMessageBox.YesRole)
            messageBox.addButton("Abbrechen", QtWidgets.QMessageBox.RejectRole)
            result = messageBox.exec()
            return result == 0
        return True

    def updateAttribut(self, attribut):
        changed = False
        uiElement = self.widgetAttributWert[attribut]
        if Wolke.Char.attribute[attribut].wert != uiElement.value():
            if self.checkConsequences(attribut, uiElement.value()):
                Wolke.Char.attribute[attribut].wert = uiElement.value()
                Wolke.Char.attribute[attribut].aktualisieren()
                changed = True
            else:
                uiElement.setValue(Wolke.Char.attribute[attribut].wert)

        return changed

    def update(self):
        if self.currentlyLoading:
            return

        ''' Set and refresh all Attributes '''
        changed = False

        for attribut in Wolke.Char.attribute:
            if self.updateAttribut(attribut):
                changed = True

        for energie in Wolke.Char.energien:
            if Wolke.Char.energien[energie].wert != self.widgetEnergieSpinZugekauft[energie].value():
                Wolke.Char.energien[energie].wert = self.widgetEnergieSpinZugekauft[energie].value()
                changed = True

        if changed:
            self.modified.emit()
            for attribut in Wolke.Char.attribute:
                self.updateTooltip(attribut)
            self.updateDerivedValues()
        
    def getEnergieSteigerungskosten(self, energie):
        en = Wolke.Char.energien[energie]
        return "(<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(en.steigerungskosten()) + " EP)"

    def getAttributSteigerungskosten(self, attr):
        attribut = Wolke.Char.attribute[attr]
        return "<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(attribut.steigerungskosten()) + " EP"

    def updateDerivedValues(self):
        for attribut in Wolke.Char.attribute:
            self.widgetAttributPW[attribut].setValue(Wolke.Char.attribute[attribut].probenwert)
            self.widgetAttributKosten[attribut].setText(self.getAttributSteigerungskosten(attribut))

        for ab in Wolke.Char.abgeleiteteWerte:
            if not Wolke.Char.abgeleiteteWerte[ab].anzeigen:
                continue
            self.widgetAbgeleitetWert[ab].setValue(Wolke.Char.abgeleiteteWerte[ab].wert)

        for en in Wolke.Char.energien:
            self.widgetEnergieKosten[en].setText(self.getEnergieSteigerungskosten(en))

    def load(self):
        self.currentlyLoading = True

        # Attribute
        for attribut in Wolke.Char.attribute:
            self.widgetAttributWert[attribut].setValue(Wolke.Char.attribute[attribut].wert)
            self.updateTooltip(attribut)

        # Energien (generate UI)
        energien = [e.name for e in sorted(Wolke.Char.energien.values(), key=lambda value: value.sortorder)]
        if not Hilfsmethoden.ArrayEqual(self.availableEnergien, energien):
            self.availableEnergien = energien

            # Delete old UI widgets
            refs = [self.widgetEnergieVollerName,
                    self.widgetEnergieName,
                    self.widgetEnergieWert,
                    self.widgetEnergiePlus,
                    self.widgetEnergieSpinZugekauft,
                    self.widgetEnergieLabelZugekauft,
                    self.widgetEnergieKosten]
            for widgets in refs:
                for widget in widgets.values():
                    self.ui.gridLayout.removeWidget(widget)
                    widget.deleteLater()
                widgets.clear()

            for layout in self.layoutEnergieZugekauft.values():
                layout.deleteLater()
            self.layoutEnergieZugekauft.clear()

            # Generate new UI widgets            
            rowIndex = self.energienStartIndex
            for energie in energien:
                labelVollerName = QtWidgets.QLabel(Wolke.Char.energien[energie].anzeigename)
                font=QtGui.QFont()
                font.setBold(True)
                labelVollerName.setFont(font)
                labelVollerName.setToolTip(f"<html><head/><body><p>{Wolke.Char.energien[energie].text}</p></body></html>")
                self.ui.gridLayout.addWidget(labelVollerName, rowIndex, 6)
                self.widgetEnergieVollerName[energie] = labelVollerName

                labelName = QtWidgets.QLabel(energie)
                font=QtGui.QFont()
                font.setItalic(True)
                labelName.setFont(font)
                labelName.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                self.ui.gridLayout.addWidget(labelName, rowIndex, 7)
                self.widgetEnergieName[energie] = labelName

                spinWert = QtWidgets.QSpinBox()
                spinWert.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
                spinWert.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                spinWert.setReadOnly(True)
                spinWert.setFocusPolicy(QtCore.Qt.NoFocus)
                spinWert.setMaximum(9999)
                spinWert.valueChanged.connect(self.update)
                self.ui.gridLayout.addWidget(spinWert, rowIndex, 8)
                self.widgetEnergieWert[energie] = spinWert

                labelPlus = QtWidgets.QLabel("+") #minmax 20, hcenter
                self.ui.gridLayout.addWidget(labelPlus, rowIndex, 9)
                self.widgetEnergiePlus[energie] = labelPlus

                layout = QtWidgets.QHBoxLayout()
                self.ui.gridLayout.addLayout(layout, rowIndex, 10)
                self.layoutEnergieZugekauft[energie] = layout

                spin = QtWidgets.QSpinBox()
                spin.setMinimumWidth(60)
                spin.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                spin.setMaximum(999)
                spin.valueChanged.connect(self.update)
                layout.addWidget(spin)
                self.widgetEnergieSpinZugekauft[energie] = spin

                labelZugekauft = QtWidgets.QLabel("zugekauft")
                layout.addWidget(labelZugekauft)
                self.widgetEnergieLabelZugekauft[energie] = labelZugekauft

                labelKosten = QtWidgets.QLabel()
                labelKosten.setMinimumWidth(80)
                layout.addWidget(labelKosten)
                self.widgetEnergieKosten[energie] = labelKosten

                rowIndex += 1

        # Energien (Update)
        for en in Wolke.Char.energien:
            self.widgetEnergieWert[en].setValue(Wolke.Char.energien[en].basiswert + Wolke.Char.energien[en].mod)
            self.widgetEnergieSpinZugekauft[en].setValue(Wolke.Char.energien[en].wert)

        self.updateDerivedValues()

        self.currentlyLoading = False