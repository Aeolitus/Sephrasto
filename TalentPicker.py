# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import copy

from PyQt5 import QtCore, QtGui, QtWidgets

import CharakterTalente
from Charakter import VariableKosten
from Wolke import Wolke


class TalentPicker(object):
    def __init__(self, fert, ueber):
        super().__init__()
        if ueber:
            self.refC = Wolke.Char.übernatürlicheFertigkeiten
            self.refD = Wolke.DB.übernatürlicheFertigkeiten
        else:
            self.refC = Wolke.Char.fertigkeiten
            self.refD = Wolke.DB.fertigkeiten
        self.talenteVariable = copy.deepcopy(Wolke.Char.talenteVariable)
        self.gekaufteTalente = self.refC[fert].gekaufteTalente.copy()
        self.fert = fert
        self.Form = QtWidgets.QDialog()
        self.ui = CharakterTalente.Ui_Dialog()
        self.ui.setupUi(self.Form)

        self.Form.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)
        self.ui.listTalente.selectionModel().currentChanged.connect(self.talChanged)

        talente = []
        for el in Wolke.DB.talente:
            talent = Wolke.DB.talente[el]
            if (ueber and not talent.isSpezialTalent()) or (
                not ueber and talent.isSpezialTalent()
            ):
                continue
            if fert in talent.fertigkeiten and Wolke.Char.voraussetzungenPrüfen(
                talent.voraussetzungen
            ):
                if (
                    talent.variableKosten or talent.kommentarErlauben
                ) and not el in self.talenteVariable:
                    self.setVariableKosten(
                        el,
                        Wolke.Char.getTalentCost(
                            el, self.refD[self.fert].steigerungsfaktor
                        ),
                        "",
                    )
                talente.append(el)
        talente.sort()

        self.rowCount = 0
        for el in talente:
            item = QtGui.QStandardItem(self.displayStr(el))
            item.setData(el, QtCore.Qt.UserRole)  # store talent name in user data
            item.setEditable(False)
            item.setCheckable(True)
            if el in self.gekaufteTalente:
                item.setCheckState(2)
            else:
                item.setCheckState(0)
            self.model.appendRow(item)
            self.rowCount += 1
        if self.rowCount > 0:
            self.updateFields(self.model.item(0).data(QtCore.Qt.UserRole))
        self.ui.textKommentar.textChanged.connect(self.kommentarChanged)
        self.ui.spinKosten.valueChanged.connect(self.spinChanged)
        self.ui.spinKosten.setStyleSheet("QSpinBox {background-color: #FFFFFF}")
        self.ui.listTalente.setModel(self.model)
        self.ui.listTalente.setFocus()
        self.ui.listTalente.setCurrentIndex(self.model.index(0, 0))
        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            self.gekaufteTalente = []
            for i in range(self.rowCount):
                tmp = self.model.item(i).data(QtCore.Qt.UserRole)
                if self.model.item(i).checkState() == QtCore.Qt.Checked:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp not in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.append(tmp)
                    if tmp in self.talenteVariable:
                        Wolke.Char.talenteVariable[tmp] = self.talenteVariable[tmp]
                else:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.remove(tmp)

            self.gekaufteTalente = self.refC[fert].gekaufteTalente
        else:
            self.gekaufteTalente = None

    def setVariableKosten(self, talent, kosten, kommentar):
        if (
            not Wolke.DB.talente[talent].variableKosten
            and not Wolke.DB.talente[talent].kommentarErlauben
        ):
            return

        if not talent in self.talenteVariable:
            vk = VariableKosten()
            self.talenteVariable[talent] = vk

        if kosten != None:
            self.talenteVariable[talent].kosten = kosten
        if kommentar != None:
            self.talenteVariable[talent].kommentar = kommentar

    def talChanged(self, item, prev):
        text = item.data(QtCore.Qt.UserRole)
        self.updateFields(text)

    def spinChanged(self):
        self.setVariableKosten(
            self.ui.labelName.property("data"), self.ui.spinKosten.value(), None
        )

    def kommentarChanged(self, text):
        self.setVariableKosten(self.ui.labelName.property("data"), None, text)

    def updateFields(self, talent):
        if talent is not None:
            self.ui.labelName.setText(self.displayStr(talent))
            self.ui.labelName.setProperty(
                "data", talent
            )  # store talent name in user data
            self.ui.labelInfo.hide()
            self.ui.spinKosten.setReadOnly(True)
            self.ui.spinKosten.setButtonSymbols(2)
            self.ui.spinKosten.setMinimum(0)
            self.ui.textKommentar.hide()
            self.ui.labelKommentar.hide()
            if Wolke.DB.talente[talent].kosten == -1:
                if Wolke.DB.talente[talent].verbilligt:
                    self.ui.labelInfo.show()
                    self.ui.labelInfo.setText("Verbilligt")
            else:
                self.ui.labelInfo.show()
                self.ui.labelInfo.setText("Spezialtalent")

            if talent in self.talenteVariable:
                if Wolke.DB.talente[talent].variableKosten:
                    self.ui.spinKosten.setReadOnly(False)
                    self.ui.spinKosten.setButtonSymbols(0)
                    step = Wolke.Char.getDefaultTalentCost(
                        talent, self.refD[self.fert].steigerungsfaktor
                    )
                    self.ui.spinKosten.setSingleStep(step)
                    self.ui.spinKosten.setMinimum(step)
                    self.ui.spinKosten.setValue(self.talenteVariable[talent].kosten)
                else:
                    self.ui.spinKosten.setValue(
                        Wolke.Char.getDefaultTalentCost(
                            talent, self.refD[self.fert].steigerungsfaktor
                        )
                    )
                self.ui.textKommentar.show()
                self.ui.labelKommentar.show()
                self.ui.textKommentar.setText(self.talenteVariable[talent].kommentar)
            else:
                self.ui.spinKosten.setValue(
                    Wolke.Char.getDefaultTalentCost(
                        talent, self.refD[self.fert].steigerungsfaktor
                    )
                )
            if self.fert == "Gebräuche":
                if self.displayStr(Wolke.DB.talente[talent].name) == Wolke.Char.heimat:
                    self.ui.spinKosten.setValue(0)
            self.ui.plainText.setPlainText(Wolke.DB.talente[talent].text)

    def displayStr(self, inp):
        return inp.replace(self.fert + ": ", "")
