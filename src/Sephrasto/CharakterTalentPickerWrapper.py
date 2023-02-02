# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import UI.CharakterTalentPicker
from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import copy

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

        self.talenteVariableKosten = copy.deepcopy(Wolke.Char.talenteVariableKosten)
        self.talenteKommentare = copy.deepcopy(Wolke.Char.talenteKommentare)
        self.gekaufteTalente = self.refC[fert].gekaufteTalente.copy()

        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)
        
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Abbrechen")

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.4), int(width*0.6)])

        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        
        talente = []
        for el in Wolke.DB.talente:
            talent = Wolke.DB.talente[el]
            if (ueber and not talent.isSpezialTalent()) or (not ueber and talent.isSpezialTalent()):
                continue
            if fert in talent.fertigkeiten and Wolke.Char.voraussetzungenPrüfen(talent.voraussetzungen):
                if talent.variableKosten and not el in self.talenteVariableKosten:
                    self.talenteVariableKosten[el] = Wolke.Char.getTalentCost(el, self.refD[self.fert].steigerungsfaktor)
                if talent.kommentarErlauben and not el in self.talenteKommentare:
                    self.talenteKommentare[el] = ""
                talente.append(el)
        talente.sort()

        self.rowCount = 0
        for el in talente:
            item = QtGui.QStandardItem(self.displayStr(el))
            item.setData(el, QtCore.Qt.UserRole) # store talent name in user data
            item.setEditable(False)
            item.setCheckable(True)
            if el in self.gekaufteTalente:
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
                tmp = self.model.item(i).data(QtCore.Qt.UserRole)
                if self.model.item(i).checkState() == QtCore.Qt.Checked:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp not in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.append(tmp)
                    if tmp in self.talenteVariableKosten:
                        Wolke.Char.talenteVariableKosten[tmp] = self.talenteVariableKosten[tmp]
                    if tmp in self.talenteKommentare:
                        Wolke.Char.talenteKommentare[tmp] = self.talenteKommentare[tmp]
                else:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.remove(tmp)

            self.gekaufteTalente = self.refC[fert].gekaufteTalente
        else:
            self.gekaufteTalente = None

    def talChanged(self, item, prev):
        text = item.data(QtCore.Qt.UserRole)
        self.updateFields(text)
        
    def spinChanged(self):
        tal = self.ui.labelName.property("data")
        if Wolke.DB.talente[tal].variableKosten:
            self.talenteVariableKosten[tal] = self.ui.spinKosten.value()
        
    def kommentarChanged(self, text):
        tal = self.ui.labelName.property("data")
        if Wolke.DB.talente[tal].kommentarErlauben:
            self.talenteKommentare[tal] = text

    def updateFields(self, talent):
        if talent is not None:
            self.ui.labelName.setText(self.displayStr(talent))
            self.ui.labelName.setProperty("data", talent) # store talent name in user data
            self.ui.labelInfo.hide()
            self.ui.spinKosten.setReadOnly(True)
            self.ui.spinKosten.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            self.ui.spinKosten.setMinimum(0)

            if Wolke.DB.talente[talent].kosten == -1:
                if Wolke.DB.talente[talent].verbilligt:
                    self.ui.labelInfo.show()
                    self.ui.labelInfo.setText("Verbilligt")
            else:
                self.ui.labelInfo.show()
                self.ui.labelInfo.setText("Spezialtalent")

            if talent in self.talenteVariableKosten and Wolke.DB.talente[talent].variableKosten:
                if Wolke.DB.talente[talent].variableKosten:
                    self.ui.spinKosten.setReadOnly(False)
                    self.ui.spinKosten.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                    step = Wolke.Char.getDefaultTalentCost(talent, self.refD[self.fert].steigerungsfaktor)
                    self.ui.spinKosten.setSingleStep(step)
                    self.ui.spinKosten.setMinimum(step)
                    self.ui.spinKosten.setValue(self.talenteVariableKosten[talent])
            else:
                self.ui.spinKosten.setValue(Wolke.Char.getDefaultTalentCost(talent, self.refD[self.fert].steigerungsfaktor))

            if talent in self.talenteKommentare and Wolke.DB.talente[talent].kommentarErlauben:
                self.ui.textKommentar.show()
                self.ui.labelKommentar.show()
                self.ui.textKommentar.setText(self.talenteKommentare[talent])
            else:
                self.ui.textKommentar.hide()
                self.ui.labelKommentar.hide()

            if self.fert == "Gebräuche":
                if self.displayStr(Wolke.DB.talente[talent].name) == \
                        Wolke.Char.heimat:
                    self.ui.spinKosten.setValue(0)
            self.ui.plainText.setPlainText(Wolke.DB.talente[talent].text)

    def displayStr(self,inp):
        return inp.replace(self.fert + ": ", "")