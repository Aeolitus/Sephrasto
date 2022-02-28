# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:21:49 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterAttribute
from PyQt5 import QtWidgets, QtCore, QtGui
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
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        ''' Initialize the GUI and set signals for the spinners'''
        super().__init__()
        logging.debug("Initializing AttrWrapper...")
        self.formAttr = QtWidgets.QWidget()
        self.uiAttr = UI.CharakterAttribute.Ui_formAttribute()
        self.uiAttr.setupUi(self.formAttr)

        # pre-sort and -filter vorteile to improve performance of tooltip generation
        self.vorteile = {}
        for attribut in Definitionen.Attribute:
            self.vorteile[attribut] = []
        for vorteil in sorted(Wolke.DB.vorteile.values(), key = lambda v: v.typ):
            for attribut in Definitionen.Attribute:
                if Hilfsmethoden.isAttributVoraussetzung(attribut, vorteil.voraussetzungen):
                    self.vorteile[attribut].append(vorteil)

        font = QtGui.QFont(Wolke.Settings["FontHeading"], Wolke.Settings["FontHeadingSize"])
        font.setBold(True)
        self.uiAttr.labelWert.setFont(font)
        self.uiAttr.labelWert.setStyleSheet("color: " + Wolke.HeadingColor + ";}")
        self.uiAttr.labelWert2.setFont(font)
        self.uiAttr.labelWert2.setStyleSheet("color: " + Wolke.HeadingColor + ";}")
        self.uiAttr.labelPW.setFont(font)
        self.uiAttr.labelPW.setStyleSheet("color: " + Wolke.HeadingColor + ";}")
        self.uiAttr.labelKosten.setFont(font)
        self.uiAttr.labelKosten.setStyleSheet("color: " + Wolke.HeadingColor + ";}")
        self.uiAttr.labelFormel.setFont(font)
        self.uiAttr.labelFormel.setStyleSheet("color: " + Wolke.HeadingColor + ";}")

        #Signals
        self.uiAttr.spinAsP.valueChanged.connect(self.update)
        self.uiAttr.spinKaP.valueChanged.connect(self.update)
        self.uiAttr.spinKO.valueChanged.connect(self.update)
        self.uiAttr.spinMU.valueChanged.connect(self.update)
        self.uiAttr.spinIN.valueChanged.connect(self.update)
        self.uiAttr.spinGE.valueChanged.connect(self.update)
        self.uiAttr.spinKK.valueChanged.connect(self.update)
        self.uiAttr.spinFF.valueChanged.connect(self.update)
        self.uiAttr.spinKL.valueChanged.connect(self.update)
        self.uiAttr.spinCH.valueChanged.connect(self.update)
        self.currentlyLoading = False
     
    def updateTooltip(self, attribut, uiElement):
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
        for vort in self.vorteile[attribut]:
            if vort.name in Wolke.Char.vorteile:
                continue
            elif Hilfsmethoden.voraussetzungenPrüfen(Wolke.Char.vorteile, Wolke.Char.waffen, Wolke.Char.attribute,  Wolke.Char.übernatürlicheFertigkeiten, Wolke.Char.fertigkeiten, vort.voraussetzungen):
                continue
            elif Hilfsmethoden.voraussetzungenPrüfen(Wolke.Char.vorteile, Wolke.Char.waffen, attribute,  Wolke.Char.übernatürlicheFertigkeiten, Wolke.Char.fertigkeiten, vort.voraussetzungen):
                vortNew.append(vort.name + " erwerbbar")

        fertNew = []
        ferts = copy.deepcopy(Wolke.Char.fertigkeiten)
        for fert in sorted(ferts.values(), key = lambda f: f.printclass):
            fert.aktualisieren(Wolke.Char.attribute)
            basisAlt = fert.basiswert
            fert.aktualisieren(attribute)
            if basisAlt != fert.basiswert:
                fertNew.append(fert.name + " +" + str(fert.basiswert - basisAlt))

        fertsÜberNew = []
        ferts = copy.deepcopy(Wolke.Char.übernatürlicheFertigkeiten)
        more = 0
        for fert in sorted(ferts.values(), key = lambda f: f.printclass):
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

        uiElement.setToolTip(tooltip)

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
            messageBox.addButton(QtWidgets.QPushButton("Ja"), QtWidgets.QMessageBox.YesRole)
            messageBox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.RejectRole)
            result = messageBox.exec_()
            return result == 0
        return True

    def updateAttribut(self, attribut, uiElement):
        changed = False
        if Wolke.Char.attribute[attribut].wert != uiElement.value():
            if self.checkConsequences(attribut, uiElement.value()):
                Wolke.Char.attribute[attribut].wert = uiElement.value()
                Wolke.Char.attribute[attribut].aktualisieren()
                changed = True
            else:
                uiElement.setValue(Wolke.Char.attribute[attribut].wert)

            self.updateTooltip(attribut, uiElement)

        return changed

    def update(self):
        if self.currentlyLoading:
            return

        ''' Set and refresh all Attributes '''
        changed = False

        if self.updateAttribut('KO', self.uiAttr.spinKO):
            changed = True
        if self.updateAttribut('MU', self.uiAttr.spinMU):
            changed = True
        if self.updateAttribut('GE', self.uiAttr.spinGE):
            changed = True
        if self.updateAttribut('KK', self.uiAttr.spinKK):
            changed = True
        if self.updateAttribut('IN', self.uiAttr.spinIN):
            changed = True
        if self.updateAttribut('KL', self.uiAttr.spinKL):
            changed = True
        if self.updateAttribut('CH', self.uiAttr.spinCH):
            changed = True
        if self.updateAttribut('FF', self.uiAttr.spinFF):
            changed = True

        if Wolke.Char.asp.wert != self.uiAttr.spinAsP.value():
            Wolke.Char.asp.wert = self.uiAttr.spinAsP.value()
            changed = True

        if Wolke.Char.kap.wert != self.uiAttr.spinKaP.value():
            Wolke.Char.kap.wert = self.uiAttr.spinKaP.value()
            changed = True

        self.updateDerivedValues()

        if changed:
            self.modified.emit()
        
    def getSteigerungskostenAsP(self):
        val = (Wolke.Char.asp.wert + 1) * Wolke.Char.asp.steigerungsfaktor
        return "(<span style='font-size: 9pt; font-weight: 900; font-family: \"Font Awesome 6 Free Solid\";'>\uf176</span>&nbsp;&nbsp;" + str(EventBus.applyFilter("asp_kosten", val, { "charakter" : Wolke.Char, "wert" : Wolke.Char.asp.wert })) + " EP)"

    def getSteigerungskostenKaP(self):
        val = (Wolke.Char.kap.wert + 1) * Wolke.Char.kap.steigerungsfaktor
        return "(<span style='font-size: 9pt; font-weight: 900; font-family: \"Font Awesome 6 Free Solid\";'>\uf176</span>&nbsp;&nbsp;" + str(EventBus.applyFilter("asp_kosten", val, { "charakter" : Wolke.Char, "wert" : Wolke.Char.kap.wert })) + " EP)"

    def getAttributSteigerungskosten(self, attr):
        attribut = Wolke.Char.attribute[attr]
        val = (attribut.wert + 1) * attribut.steigerungsfaktor
        return "<span style='font-size: 9pt; font-weight: 900; font-family: \"Font Awesome 6 Free Solid\";'>\uf176</span>&nbsp;&nbsp;" + str(EventBus.applyFilter("attribut_kosten", val, { "charakter" : Wolke.Char, "attribut" : attr, "wert" : attribut.wert + 1 })) + " EP"

    def updateDerivedValues(self):
        self.uiAttr.pwKO.setValue(Wolke.Char.attribute['KO'].wert*2)
        self.uiAttr.labelKostenKO.setText(self.getAttributSteigerungskosten('KO'))

        self.uiAttr.pwMU.setValue(Wolke.Char.attribute['MU'].wert*2)
        self.uiAttr.labelKostenMU.setText(self.getAttributSteigerungskosten('MU'))

        self.uiAttr.pwGE.setValue(Wolke.Char.attribute['GE'].wert*2)
        self.uiAttr.labelKostenGE.setText(self.getAttributSteigerungskosten('GE'))

        self.uiAttr.pwKK.setValue(Wolke.Char.attribute['KK'].wert*2)
        self.uiAttr.labelKostenKK.setText(self.getAttributSteigerungskosten('KK'))

        self.uiAttr.pwIN.setValue(Wolke.Char.attribute['IN'].wert*2)
        self.uiAttr.labelKostenIN.setText(self.getAttributSteigerungskosten('IN'))

        self.uiAttr.pwKL.setValue(Wolke.Char.attribute['KL'].wert*2)
        self.uiAttr.labelKostenKL.setText(self.getAttributSteigerungskosten('KL'))

        self.uiAttr.pwCH.setValue(Wolke.Char.attribute['CH'].wert*2)
        self.uiAttr.labelKostenCH.setText(self.getAttributSteigerungskosten('CH'))

        self.uiAttr.pwFF.setValue(Wolke.Char.attribute['FF'].wert*2)
        self.uiAttr.labelKostenFF.setText(self.getAttributSteigerungskosten('FF'))

        self.uiAttr.abWS.setValue(Wolke.Char.ws)
        self.uiAttr.abGS.setValue(Wolke.Char.gs)
        self.uiAttr.abIN.setValue(Wolke.Char.ini)
        self.uiAttr.abMR.setValue(Wolke.Char.mr)
        self.uiAttr.abSB.setValue(Wolke.Char.schadensbonus)

        self.uiAttr.labelKostenAsP.setText(self.getSteigerungskostenAsP())
        self.uiAttr.labelKostenKaP.setText(self.getSteigerungskostenKaP())

    def load(self):
        self.currentlyLoading = True

        ''' Load all values and derived values '''
        self.uiAttr.spinKO.setValue(Wolke.Char.attribute['KO'].wert)
        self.updateTooltip('KO', self.uiAttr.spinKO)

        self.uiAttr.spinMU.setValue(Wolke.Char.attribute['MU'].wert)
        self.updateTooltip('MU', self.uiAttr.spinMU)

        self.uiAttr.spinGE.setValue(Wolke.Char.attribute['GE'].wert)
        self.updateTooltip('GE', self.uiAttr.spinGE)

        self.uiAttr.spinKK.setValue(Wolke.Char.attribute['KK'].wert)
        self.updateTooltip('KK', self.uiAttr.spinKK)

        self.uiAttr.spinIN.setValue(Wolke.Char.attribute['IN'].wert)
        self.updateTooltip('IN', self.uiAttr.spinIN)

        self.uiAttr.spinKL.setValue(Wolke.Char.attribute['KL'].wert)
        self.updateTooltip('KL', self.uiAttr.spinKL)

        self.uiAttr.spinCH.setValue(Wolke.Char.attribute['CH'].wert)
        self.updateTooltip('CH', self.uiAttr.spinCH)

        self.uiAttr.spinFF.setValue(Wolke.Char.attribute['FF'].wert)
        self.updateTooltip('FF', self.uiAttr.spinFF)

        self.uiAttr.abAsP.setValue(Wolke.Char.aspBasis + Wolke.Char.aspMod)
        self.uiAttr.abKaP.setValue(Wolke.Char.kapBasis + Wolke.Char.kapMod)
        if "Zauberer I" in Wolke.Char.vorteile:
            self.uiAttr.spinAsP.setEnabled(True)
            self.uiAttr.spinAsP.setValue(Wolke.Char.asp.wert)
        else:
            self.uiAttr.spinAsP.setValue(0)
            self.uiAttr.spinAsP.setEnabled(False)

        self.uiAttr.lblKap.setText("KaP")
        self.uiAttr.lblKapZugekauft.setText("Karmaenergie")
        self.uiAttr.lblKapZugekauft.setToolTip("<html><head/><body><p>Als Geweihter stellt dir deine Gottheit Karmaenergie zur Verfügung: "\
            "Die Vorteile Geweiht I/II/III/IV verleihen dir 8/16/24/32 Karmapunkte (KaP), die du für Liturgien nutzen kannst. "\
            "Du kannst diesen Vorrat an maximalen KaP durch den Zukauf nach Steigerungsfaktor 1 erhöhen.</p></body></html>")
        if "Geweiht I" in Wolke.Char.vorteile:
            self.uiAttr.spinKaP.setEnabled(True)
            self.uiAttr.spinKaP.setValue(Wolke.Char.kap.wert)
        elif "Paktierer I" in Wolke.Char.vorteile:
            self.uiAttr.spinKaP.setEnabled(True)
            self.uiAttr.spinKaP.setValue(Wolke.Char.kap.wert)
            self.uiAttr.lblKap.setText("GuP")
            self.uiAttr.lblKapZugekauft.setText("Gunstpunkte")
            self.uiAttr.lblKapZugekauft.setToolTip("<html><head/><body><p>Ein Paktierer selbst verfügt nicht über übernatürliche Macht, sondern "\
               "erbittet den Beistand seines Erzdämonen: Der Vorteil Paktierer I/II/III/IV verleiht ihm 8/16/24/32 Gunstpunkte (GuP), "\
               "mit denen er den Erzdämon anrufen kann. GuP werden nach Steigerungsfaktor 1 gesteigert. Meist geschieht das, wenn der Paktierer "\
               "ohnehin einen Kreis der Verdammnis aufsteigt oder dem Erzdämonen auf andere Weise nahe ist.</p></body></html>")
        else:
            self.uiAttr.spinKaP.setValue(0)
            self.uiAttr.spinKaP.setEnabled(False)

        self.updateDerivedValues()

        self.currentlyLoading = False