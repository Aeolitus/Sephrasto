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
            self.ui.gbAttribute.layout().addWidget(labelVollerName, rowIndex, 0)
            self.widgetAttributVollerName[attribut] = labelVollerName

            labelName = QtWidgets.QLabel(attribut)
            font=QtGui.QFont()
            font.setItalic(True)
            labelName.setFont(font)
            labelName.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.ui.gbAttribute.layout().addWidget(labelName, rowIndex, 1)
            self.widgetAttributName[attribut] = labelName
            
            spinWert = QtWidgets.QSpinBox()
            spinWert.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            spinWert.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spinWert.valueChanged.connect(self.update)
            spinWert.setFixedWidth(Hilfsmethoden.emToPixels(6))
            self.ui.gbAttribute.layout().addWidget(spinWert, rowIndex, 2)
            self.widgetAttributWert[attribut] = spinWert
            
            spinPW = QtWidgets.QSpinBox() 
            spinPW.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            spinPW.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spinPW.setReadOnly(True)
            spinPW.setFocusPolicy(QtCore.Qt.NoFocus)
            spinPW.setMaximum(999)
            spinPW.setFixedWidth(Hilfsmethoden.emToPixels(6))
            self.ui.gbAttribute.layout().addWidget(spinPW, rowIndex, 3)
            self.widgetAttributPW[attribut] = spinPW

            labelKosten = QtWidgets.QLabel()
            self.ui.gbAttribute.layout().addWidget(labelKosten, rowIndex, 4)
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
            self.ui.gbAbgeleiteteWerte.layout().addWidget(labelVollerName, rowIndex, 0)
            self.widgetAbgeleitetVollerName[ab] = labelVollerName

            labelName = QtWidgets.QLabel(ab)
            font=QtGui.QFont()
            font.setItalic(True)
            labelName.setFont(font)
            labelName.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.ui.gbAbgeleiteteWerte.layout().addWidget(labelName, rowIndex, 1)
            self.widgetAbgeleitetName[ab] = labelName
            
            spinWert = QtWidgets.QSpinBox()
            spinWert.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            spinWert.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spinWert.setReadOnly(True)
            spinWert.setFocusPolicy(QtCore.Qt.NoFocus)
            spinWert.setMinimum(-999)
            spinWert.setMaximum(999)
            spinWert.setFixedWidth(Hilfsmethoden.emToPixels(6))
            self.ui.gbAbgeleiteteWerte.layout().addWidget(spinWert, rowIndex, 2)
            self.widgetAbgeleitetWert[ab] = spinWert

            labelFormel = QtWidgets.QLabel(Wolke.Char.abgeleiteteWerte[ab].formel)
            self.ui.gbAbgeleiteteWerte.layout().addWidget(labelFormel, rowIndex, 3)
            self.widgetAbgeleitetKosten[ab] = labelFormel

            rowIndex += 1

        # Init Energien (generate for all from db and toggle visibility because energien have voraussetzungen that might change)        
        self.widgetEnergieVollerName = {}
        self.widgetEnergieName = {}
        self.widgetEnergieWert = {}
        self.widgetEnergieSpinZugekauft = {}
        self.widgetEnergieKosten = {}
        self.widgetEnergieSpinGebunden = {}
        self.widgetEnergieSpinGesamt = {}
        
        rowIndex = 1
        energien = [e.name for e in sorted(Wolke.DB.energien.values(), key=lambda value: value.sortorder)]
        for energie in energien:
            labelVollerName = QtWidgets.QLabel(Wolke.DB.energien[energie].anzeigename)
            labelVollerName.setVisible(False)
            font=QtGui.QFont()
            font.setBold(True)
            labelVollerName.setFont(font)
            labelVollerName.setToolTip(f"<html><head/><body><p>{Wolke.DB.energien[energie].text}</p></body></html>")
            self.ui.gbEnergien.layout().addWidget(labelVollerName, rowIndex, 0)
            self.widgetEnergieVollerName[energie] = labelVollerName

            labelName = QtWidgets.QLabel(energie)
            labelName.setVisible(False)
            font=QtGui.QFont()
            font.setItalic(True)
            labelName.setFont(font)
            labelName.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.ui.gbEnergien.layout().addWidget(labelName, rowIndex, 1)
            self.widgetEnergieName[energie] = labelName

            spinWert = QtWidgets.QSpinBox()
            spinWert.setVisible(False)
            spinWert.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            spinWert.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spinWert.setReadOnly(True)
            spinWert.setFocusPolicy(QtCore.Qt.NoFocus)
            spinWert.setMaximum(999)
            spinWert.setFixedWidth(Hilfsmethoden.emToPixels(6))
            spinWert.valueChanged.connect(self.update)
            self.ui.gbEnergien.layout().addWidget(spinWert, rowIndex, 2)
            self.widgetEnergieWert[energie] = spinWert


            spin = QtWidgets.QSpinBox()
            spin.setVisible(False)
            spin.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            spin.setMaximum(999)
            spin.setFixedWidth(Hilfsmethoden.emToPixels(6))
            spin.valueChanged.connect(self.update)
            self.ui.gbEnergien.layout().addWidget(spin, rowIndex, 3)
            self.widgetEnergieSpinZugekauft[energie] = spin

            labelKosten = QtWidgets.QLabel()
            labelKosten.setVisible(False)
            self.ui.gbEnergien.layout().addWidget(labelKosten, rowIndex, 4)
            self.widgetEnergieKosten[energie] = labelKosten

            spin = QtWidgets.QSpinBox()
            spin.setVisible(False)
            spin.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            spin.setMaximum(999)
            spin.setFixedWidth(Hilfsmethoden.emToPixels(6))
            spin.valueChanged.connect(self.update)
            spin.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
            spin.setToolTip(f"Talente, die g{energie} erfordern, geben diese nach Beenden der Bindung wieder frei.\n"\
                f"Bei vielen dieser Talente lohnt es sich aber, die Bindung langfristig aufrecht zu erhalten. Diese g{energie} kannst du hier eintragen.")
            self.ui.gbEnergien.layout().addWidget(spin, rowIndex, 5, QtCore.Qt.AlignHCenter)
            self.widgetEnergieSpinGebunden[energie] = spin

            spin = QtWidgets.QSpinBox() 
            spin.setVisible(False)
            spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            spin.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            spin.setReadOnly(True)
            spin.setFocusPolicy(QtCore.Qt.NoFocus)
            spin.setMaximum(999)
            spin.setFixedWidth(Hilfsmethoden.emToPixels(6))
            self.ui.gbEnergien.layout().addWidget(spin, rowIndex, 6)
            self.widgetEnergieSpinGesamt[energie] = spin

            rowIndex += 1

        self.ui.labelEnergien.setVisible(False)
        self.ui.gbEnergien.setVisible(False)

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

            if Wolke.Char.energien[energie].gebunden != self.widgetEnergieSpinGebunden[energie].value():
                Wolke.Char.energien[energie].gebunden = self.widgetEnergieSpinGebunden[energie].value()
                changed = True

        if changed:
            self.modified.emit()
            for attribut in Wolke.Char.attribute:
                self.updateTooltip(attribut)
            self.updateAbgeleiteteWerte()
            self.updateEnergien()
        
    def getEnergieSteigerungskosten(self, energie):
        en = Wolke.Char.energien[energie]
        return "<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(en.steigerungskosten()) + " EP"

    def getAttributSteigerungskosten(self, attr):
        attribut = Wolke.Char.attribute[attr]
        return "<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(attribut.steigerungskosten()) + " EP"

    def updateAbgeleiteteWerte(self):
        for attribut in Wolke.Char.attribute:
            self.widgetAttributPW[attribut].setValue(Wolke.Char.attribute[attribut].probenwert)
            self.widgetAttributKosten[attribut].setText(self.getAttributSteigerungskosten(attribut))

        for ab in Wolke.Char.abgeleiteteWerte:
            if not Wolke.Char.abgeleiteteWerte[ab].anzeigen:
                continue
            self.widgetAbgeleitetWert[ab].setValue(Wolke.Char.abgeleiteteWerte[ab].wert)

        for en in Wolke.Char.energien:
            self.widgetEnergieKosten[en].setText(self.getEnergieSteigerungskosten(en))

    def updateEnergien(self):
        for en in Wolke.DB.energien:
            if en not in Wolke.Char.energien:
                continue
            energie = Wolke.Char.energien[en]
            self.widgetEnergieSpinGebunden[en].setMaximum(energie.wertFinal)
            self.widgetEnergieSpinGesamt[en].setValue(energie.wertAktuell)

    def load(self):
        self.currentlyLoading = True

        # Attribute
        for attribut in Wolke.Char.attribute:
            self.widgetAttributWert[attribut].setValue(Wolke.Char.attribute[attribut].wert)
            self.updateTooltip(attribut)

        #Abgeleitete Werte
        self.updateAbgeleiteteWerte()

        # Energien
        self.ui.labelEnergien.setVisible(len(Wolke.Char.energien) > 0)
        self.ui.gbEnergien.setVisible(len(Wolke.Char.energien) > 0)

        for col in range(self.ui.gbAttribute.layout().columnCount()):
            width = max(self.ui.gbAttribute.layout().cellRect(0, col).width(),
                        self.ui.gbEnergien.layout().cellRect(0, col).width())
            self.ui.gbAttribute.layout().setColumnMinimumWidth(col, width)
            self.ui.gbEnergien.layout().setColumnMinimumWidth(col, width)

        for en in Wolke.DB.energien:
            owned = en in Wolke.Char.energien
            self.widgetEnergieVollerName[en].setVisible(owned)
            self.widgetEnergieName[en].setVisible(owned)
            self.widgetEnergieWert[en].setVisible(owned)
            self.widgetEnergieSpinZugekauft[en].setVisible(owned)
            self.widgetEnergieKosten[en].setVisible(owned)
            self.widgetEnergieSpinGebunden[en].setVisible(owned)
            self.widgetEnergieSpinGesamt[en].setVisible(owned)

            if owned:
                self.widgetEnergieWert[en].setValue(Wolke.Char.energien[en].basiswert + Wolke.Char.energien[en].mod)
                self.widgetEnergieSpinZugekauft[en].setValue(Wolke.Char.energien[en].wert)
                self.widgetEnergieSpinGebunden[en].setValue(Wolke.Char.energien[en].gebunden)
        self.updateEnergien()

        self.currentlyLoading = False