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
import Definitionen

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
        for attribut in Definitionen.Attribute:
            self.vorteile[attribut] = []
        for vorteil in sorted(Wolke.DB.vorteile.values(), key = lambda v: v.typ):
            for attribut in Definitionen.Attribute:
                if Hilfsmethoden.isAttributVoraussetzung(attribut, vorteil.voraussetzungen):
                    self.vorteile[attribut].append(vorteil)

        #Signals
        self.widgetWert = {}
        self.widgetKosten = {}
        self.widgetPW = {}
        for attribut in Definitionen.Attribute:
            self.widgetWert[attribut] = getattr(self.ui, "spin" + attribut)
            self.widgetKosten[attribut] = getattr(self.ui, "labelKosten" + attribut)
            self.widgetPW[attribut] = getattr(self.ui, "pw" + attribut)
            self.widgetWert[attribut].setKeyboardTracking(False)
            self.widgetWert[attribut].valueChanged.connect(self.update)
        self.ui.spinAsP.valueChanged.connect(self.update)
        self.ui.spinKaP.valueChanged.connect(self.update)

        self.currentlyLoading = False
     
    def updateTooltip(self, attribut):
        attribute = copy.deepcopy(Wolke.Char.attribute)
        attribute[attribut].wert += 1
        attribute[attribut].aktualisieren()

        tooltip = "Eine Steigerung von " + attribut + " auf " + str(attribute[attribut].wert) + " bewirkt:\n"

        abgeleitetNew = []
        scriptAPI = { 'getAttribut' : lambda attribut: attribute[attribut].wert }
        wsBasis = eval(Wolke.DB.einstellungen["Basis WS Script"].toText(), scriptAPI)
        mrBasis = eval(Wolke.DB.einstellungen["Basis MR Script"].toText(), scriptAPI)
        gsBasis = eval(Wolke.DB.einstellungen["Basis GS Script"].toText(), scriptAPI)
        iniBasis = eval(Wolke.DB.einstellungen["Basis INI Script"].toText(), scriptAPI)
        dhBasis = eval(Wolke.DB.einstellungen["Basis DH Script"].toText(), scriptAPI)
        schadensbonusBasis = eval(Wolke.DB.einstellungen["Basis Schadensbonus Script"].toText(), scriptAPI)

        scriptAPI = { 'getAttribut' : lambda attribut: Wolke.Char.attribute[attribut].wert }
        wsBasis -= eval(Wolke.DB.einstellungen["Basis WS Script"].toText(), scriptAPI)
        mrBasis -= eval(Wolke.DB.einstellungen["Basis MR Script"].toText(), scriptAPI)
        gsBasis -= eval(Wolke.DB.einstellungen["Basis GS Script"].toText(), scriptAPI)
        iniBasis -= eval(Wolke.DB.einstellungen["Basis INI Script"].toText(), scriptAPI)
        dhBasis -= eval(Wolke.DB.einstellungen["Basis DH Script"].toText(), scriptAPI)
        schadensbonusBasis -= eval(Wolke.DB.einstellungen["Basis Schadensbonus Script"].toText(), scriptAPI)

        if wsBasis != 0:
            abgeleitetNew.append("Wundschwelle " + ("+" if wsBasis > 0 else "") + str(wsBasis))
        if mrBasis != 0:
            abgeleitetNew.append("Magieresistenz " + ("+" if mrBasis > 0 else "") + str(mrBasis))
        if gsBasis != 0:
            abgeleitetNew.append("Geschwindigkeit " + ("+" if gsBasis > 0 else "") + str(gsBasis))
        if iniBasis != 0:
            abgeleitetNew.append("Initiative " + ("+" if iniBasis > 0 else "") + str(iniBasis))
        if schadensbonusBasis != 0:
            abgeleitetNew.append("Schadensbonus " + ("+" if schadensbonusBasis > 0 else "") + str(schadensbonusBasis))
        if dhBasis != 0:
            abgeleitetNew.append("Durchhaltevermögen " + ("+" if dhBasis > 0 else "") + str(dhBasis))

        vortNew = []
        if Wolke.Char.voraussetzungenPruefen:
            for vort in self.vorteile[attribut]:
                if vort.name in Wolke.Char.vorteile:
                    continue
                elif Hilfsmethoden.voraussetzungenPrüfen(Wolke.Char.vorteile, Wolke.Char.waffen, Wolke.Char.attribute, Wolke.Char.übernatürlicheFertigkeiten, Wolke.Char.fertigkeiten, vort.voraussetzungen):
                    continue
                elif Hilfsmethoden.voraussetzungenPrüfen(Wolke.Char.vorteile, Wolke.Char.waffen, attribute, Wolke.Char.übernatürlicheFertigkeiten, Wolke.Char.fertigkeiten, vort.voraussetzungen):
                    vortNew.append(vort.name + " erwerbbar")

        fertNew = []
        ferts = copy.deepcopy(Wolke.Char.fertigkeiten)
        for fert in sorted(ferts.values(), key = lambda f: f.typ):
            fert.aktualisieren(Wolke.Char.attribute)
            basisAlt = fert.basiswert
            fert.aktualisieren(attribute)
            if basisAlt != fert.basiswert:
                fertNew.append(fert.name + " +" + str(fert.basiswert - basisAlt))

        fertsÜberNew = []
        ferts = copy.deepcopy(Wolke.Char.übernatürlicheFertigkeiten)
        more = 0
        for fert in sorted(ferts.values(), key = lambda f: f.typ):
            if len(fert.gekaufteTalente) == 0:
                more += 1
                continue
            fert.aktualisieren(Wolke.Char.attribute)
            basisAlt = fert.basiswert
            fert.aktualisieren(attribute)
            if basisAlt != fert.basiswert:
                fertsÜberNew.append(fert.name + " +" + str(fert.basiswert - basisAlt))
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

        self.widgetWert[attribut].setToolTip(tooltip)

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
        uiElement = self.widgetWert[attribut]
        if Wolke.Char.attribute[attribut].wert != uiElement.value():
            if self.checkConsequences(attribut, uiElement.value()):
                Wolke.Char.attribute[attribut].wert = uiElement.value()
                Wolke.Char.attribute[attribut].aktualisieren()
                changed = True
            else:
                uiElement.setValue(Wolke.Char.attribute[attribut].wert)

            for attribut in Definitionen.Attribute:
                self.updateTooltip(attribut)

        return changed

    def update(self):
        if self.currentlyLoading:
            return

        ''' Set and refresh all Attributes '''
        changed = False

        for attribut in Definitionen.Attribute:
            if self.updateAttribut(attribut):
                changed = True

        if Wolke.Char.asp.wert != self.ui.spinAsP.value():
            Wolke.Char.asp.wert = self.ui.spinAsP.value()
            changed = True

        if Wolke.Char.kap.wert != self.ui.spinKaP.value():
            Wolke.Char.kap.wert = self.ui.spinKaP.value()
            changed = True

        if changed:
            self.modified.emit()
            self.updateDerivedValues()
        
    def getSteigerungskostenAsP(self):
        val = (Wolke.Char.asp.wert + 1) * Wolke.Char.asp.steigerungsfaktor
        return "(<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(EventBus.applyFilter("asp_kosten", val, { "charakter" : Wolke.Char, "wert" : Wolke.Char.asp.wert })) + " EP)"

    def getSteigerungskostenKaP(self):
        val = (Wolke.Char.kap.wert + 1) * Wolke.Char.kap.steigerungsfaktor
        return "(<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(EventBus.applyFilter("asp_kosten", val, { "charakter" : Wolke.Char, "wert" : Wolke.Char.kap.wert })) + " EP)"

    def getAttributSteigerungskosten(self, attr):
        attribut = Wolke.Char.attribute[attr]
        val = (attribut.wert + 1) * attribut.steigerungsfaktor
        return "<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(EventBus.applyFilter("attribut_kosten", val, { "charakter" : Wolke.Char, "attribut" : attr, "wert" : attribut.wert + 1 })) + " EP"

    def updateDerivedValues(self):
        for attribut in Definitionen.Attribute:
            self.widgetPW[attribut].setValue(Wolke.Char.attribute[attribut].wert*2)
            self.widgetKosten[attribut].setText(self.getAttributSteigerungskosten(attribut))

        self.ui.abWS.setValue(Wolke.Char.ws)
        self.ui.abGS.setValue(Wolke.Char.gs)
        self.ui.abIN.setValue(Wolke.Char.ini)
        self.ui.abMR.setValue(Wolke.Char.mr)
        self.ui.abSB.setValue(Wolke.Char.schadensbonus)
        self.ui.abDH.setValue(Wolke.Char.dh)

        self.ui.labelKostenAsP.setText(self.getSteigerungskostenAsP())
        self.ui.labelKostenKaP.setText(self.getSteigerungskostenKaP())

    def load(self):
        self.currentlyLoading = True

        ''' Load all values and derived values '''
        for attribut in Definitionen.Attribute:
            self.widgetWert[attribut].setValue(Wolke.Char.attribute[attribut].wert)
            self.updateTooltip(attribut)

        self.ui.abAsP.setValue(Wolke.Char.aspBasis + Wolke.Char.aspMod)
        self.ui.abKaP.setValue(Wolke.Char.kapBasis + Wolke.Char.kapMod)
        if "Zauberer I" in Wolke.Char.vorteile:
            self.ui.spinAsP.setEnabled(True)
            self.ui.spinAsP.setValue(Wolke.Char.asp.wert)
        else:
            self.ui.spinAsP.setValue(0)
            self.ui.spinAsP.setEnabled(False)

        self.ui.lblKap.setText("KaP")
        self.ui.lblKapZugekauft.setText("Karmaenergie")
        self.ui.lblKapZugekauft.setToolTip("<html><head/><body><p>Als Geweihter stellt dir deine Gottheit Karmaenergie zur Verfügung: "\
            "Die Vorteile Geweiht I/II/III/IV verleihen dir 8/16/24/32 Karmapunkte (KaP), die du für Liturgien nutzen kannst. "\
            "Du kannst diesen Vorrat an maximalen KaP durch den Zukauf nach Steigerungsfaktor 1 erhöhen.</p></body></html>")
        if "Geweiht I" in Wolke.Char.vorteile:
            self.ui.spinKaP.setEnabled(True)
            self.ui.spinKaP.setValue(Wolke.Char.kap.wert)
        elif "Paktierer I" in Wolke.Char.vorteile:
            self.ui.spinKaP.setEnabled(True)
            self.ui.spinKaP.setValue(Wolke.Char.kap.wert)
            self.ui.lblKap.setText("GuP")
            self.ui.lblKapZugekauft.setText("Gunstpunkte")
            self.ui.lblKapZugekauft.setToolTip("<html><head/><body><p>Ein Paktierer selbst verfügt nicht über übernatürliche Macht, sondern "\
               "erbittet den Beistand seines Erzdämonen: Der Vorteil Paktierer I/II/III/IV verleiht ihm 8/16/24/32 Gunstpunkte (GuP), "\
               "mit denen er den Erzdämon anrufen kann. GuP werden nach Steigerungsfaktor 1 gesteigert. Meist geschieht das, wenn der Paktierer "\
               "ohnehin einen Kreis der Verdammnis aufsteigt oder dem Erzdämonen auf andere Weise nahe ist.</p></body></html>")
        else:
            self.ui.spinKaP.setValue(0)
            self.ui.spinKaP.setEnabled(False)

        self.updateDerivedValues()

        self.currentlyLoading = False