# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import UI.CharakterTalentPicker
from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import copy
from Hilfsmethoden import Hilfsmethoden
from Core.Talent import Talent
from QtUtils.AutoResizingTextBrowser import TextEditAutoResizer
from EventBus import EventBus

class TalentPicker(object):
    def __init__(self,fert,ueber):
        super().__init__()
        self.fert = fert
        self.form = QtWidgets.QDialog()
        self.ui = UI.CharakterTalentPicker.Ui_Dialog()
        self.ui.setupUi(self.form)

        if ueber:    
            self.refC = Wolke.Char.übernatürlicheFertigkeiten
            self.refD = Wolke.DB.übernatürlicheFertigkeiten
            windowSize = Wolke.Settings["WindowSize-TalentUeber"]
            self.form.resize(windowSize[0], windowSize[1])
        else:
            self.refC = Wolke.Char.fertigkeiten
            self.refD = Wolke.DB.fertigkeiten
            self.form.resize(self.form.size()*0.7)
        
            windowSize = Wolke.Settings["WindowSize-TalentProfan"]
            self.form.resize(windowSize[0], windowSize[1])

        if self.fert is None:
            self.gekaufteTalente = list(Wolke.Char.talente.keys())
        else:
            self.gekaufteTalente = self.refC[fert].gekaufteTalente.copy()

        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)
        
        self.autoResizeHelper = TextEditAutoResizer(self.ui.plainText)

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.4), int(width*0.6)])

        self.onSetupUi()

        self.currentTalent = ""
        self.talentKosten = {}
        self.talentKommentare = {}

        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        
        talente = []
        for el in Wolke.DB.talente:
            talent = Wolke.DB.talente[el]
            if el in Wolke.Char.talente:
                talent = Wolke.Char.talente[el]

            if (ueber and not talent.spezialTalent) or (not ueber and talent.spezialTalent):
                continue

            fertMatch = False
            if self.fert is None:
                for f in talent.fertigkeiten:
                    if f in Wolke.Char.übernatürlicheFertigkeiten:
                        fertMatch = True
                        break
            else:
                fertMatch = self.fert in talent.fertigkeiten

            if fertMatch and Wolke.Char.voraussetzungenPrüfen(talent):
                talente.append(talent.name)
                if talent.name in Wolke.Char.talente:
                    self.talentKosten[talent.name] = Wolke.Char.talente[talent.name].kosten
                    self.talentKommentare[talent.name] = Wolke.Char.talente[talent.name].kommentar
                else:
                    self.talentKosten[talent.name] = EventBus.applyFilter("talent_kosten", talent.kosten, { "charakter" : Wolke.Char, "talent" : talent.name })
                    self.talentKommentare[talent.name] = ""
        talente = sorted(talente, key=Hilfsmethoden.unicodeCaseInsensitive)

        self.rowCount = 0
        for el in talente:
            talent = Wolke.DB.talente[el]
            item = QtGui.QStandardItem(talent.anzeigename)
            item.setData(el, QtCore.Qt.UserRole) # store talent name in user data
            item.setEditable(False)
            item.setCheckable(True)
            if talent.name in self.gekaufteTalente:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.model.appendRow(item)
            self.rowCount += 1
        if self.rowCount > 0:
            self.updateFields(self.model.item(0).data(QtCore.Qt.UserRole))
        self.ui.textKommentar.textChanged.connect(self.kommentarChanged)
        self.ui.spinKosten.valueChanged.connect(self.spinChanged)
        self.ui.listTalente.setModel(self.model)
        self.ui.listTalente.selectionModel().currentChanged.connect(self.talChanged)
        self.ui.listTalente.setFocus()
        self.ui.listTalente.setCurrentIndex(self.model.index(0, 0))

        fwWarnung = Wolke.DB.einstellungen["Talente: FW Warnung"].wert
        if self.fert is None or ueber or self.refC[self.fert].wert >= fwWarnung:
            self.ui.labelTip.hide()
        else:
            self.ui.labelTip.setText("<span style='" + Wolke.FontAwesomeCSS + f"'>\uf071</span>&nbsp;&nbsp;Talente lohnen sich üblicherweise erst ab einem Fertigkeitswert von {fwWarnung}.")

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()

        if ueber:
            Wolke.Settings["WindowSize-TalentUeber"] = [self.form.size().width(), self.form.size().height()]
        else:
            Wolke.Settings["WindowSize-TalentProfan"] = [self.form.size().width(), self.form.size().height()]

        if self.ret == QtWidgets.QDialog.Accepted:
            self.gekaufteTalente = []
            for i in range(self.rowCount):
                el = self.model.item(i).data(QtCore.Qt.UserRole)
                if self.model.item(i).checkState() == QtCore.Qt.Checked:  
                    self.gekaufteTalente.append(el)
                    talent = Wolke.Char.addTalent(el)
                    if talent.variableKosten:
                        talent.kosten = self.talentKosten[el]
                    if talent.kommentarErlauben:
                        talent.kommentar = self.talentKommentare[el]
                else:
                    Wolke.Char.removeTalent(el)
        else:
            self.gekaufteTalente = None
            
    def onSetupUi(self):
        pass # for usage in plugins

    def talChanged(self, item, prev):
        talent = item.data(QtCore.Qt.UserRole)
        self.updateFields(talent)

    def spinChanged(self):
        if not self.currentTalent:
            return
        self.talentKosten[self.currentTalent] = self.ui.spinKosten.value()
        
    def kommentarChanged(self, text):
        if not self.currentTalent:
            return
        self.talentKommentare[self.currentTalent] = text

    def updateFields(self, tal):
        if tal is None:
            return
        talent = Wolke.DB.talente[tal]

        self.currentTalent = talent.name
        self.ui.labelName.setText(talent.anzeigename + (" (verbilligt)" if talent.verbilligt else ""))
        self.ui.labelInfo.hide()
        self.ui.spinKosten.setReadOnly(True)
        self.ui.spinKosten.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        if talent.spezialTalent:
            self.ui.labelInfo.show()
            self.ui.labelInfo.setText(talent.kategorieName(Wolke.DB))

        if talent.variableKosten:
            self.ui.spinKosten.setReadOnly(False)
            self.ui.spinKosten.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            self.ui.spinKosten.setSingleStep(talent.kosten)

        self.ui.spinKosten.setValue(self.talentKosten[tal])

        if talent.kommentarErlauben:
            self.ui.textKommentar.show()
            self.ui.labelKommentar.show()
            self.ui.textKommentar.setText(self.talentKommentare[tal])
        else:
            self.ui.textKommentar.hide()
            self.ui.labelKommentar.hide()

        text = talent.text
        if talent.info:
            text += f"\n<b>Sephrasto</b>: {talent.info}"
        self.ui.plainText.setText(Hilfsmethoden.fixHtml(text))