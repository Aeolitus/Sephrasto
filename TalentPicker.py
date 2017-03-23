# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import CharakterTalente
from PyQt5 import QtCore, QtWidgets, QtGui
from Wolke import Wolke

class TalentPicker(object):
    def __init__(self,fert,ueber):
        super().__init__()
        if ueber:    
            self.refC = Wolke.Char.übernatürlicheFertigkeiten
            self.refD = Wolke.DB.übernatürlicheFertigkeiten
        else:
            self.refC = Wolke.Char.fertigkeiten
            self.refD = Wolke.DB.fertigkeiten
        self.gekaufteTalente = self.refC[fert].gekaufteTalente.copy()
        self.fert = fert
        self.Form = QtWidgets.QDialog()
        self.ui = CharakterTalente.Ui_Dialog()
        self.ui.setupUi(self.Form)
        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)
        self.ui.listTalente.clicked.connect(self.talClicked)
        self.rowCount = 0
        for el in Wolke.DB.talente:
            if fert in Wolke.DB.talente[el].fertigkeiten and Wolke.Char.voraussetzungenPrüfen(Wolke.DB.talente[el].voraussetzungen):
                item = QtGui.QStandardItem(el)
                item.setEditable(False)
                item.setCheckable(True)
                if el in self.gekaufteTalente:
                    item.setCheckState(2)
                else:
                    item.setCheckState(0)
                self.model.appendRow(item)
                self.rowCount += 1
        if self.rowCount > 0:
            self.updateFields(self.model.item(0).text())
        self.ui.listTalente.setModel(self.model)
        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            self.gekaufteTalente = []
            for i in range(self.rowCount):
                tmp = self.model.item(i).text()
                if self.model.item(i).checkState() == QtCore.Qt.Checked:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp not in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.append(tmp)
                else:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.remove(tmp)

            self.gekaufteTalente = self.refC[fert].gekaufteTalente
        else:
            self.gekaufteTalente = None
        
    @QtCore.pyqtSlot("QModelIndex")   
    def talClicked(self, item):
        text = self.model.itemData(item)[0]
        self.updateFields(text)
        
    def updateFields(self, talent):
        self.ui.labelName.setText(Wolke.DB.talente[talent].name)
        if Wolke.DB.talente[talent].kosten == -1:
            if Wolke.DB.talente[talent].verbilligt:
                self.ui.labelInfo.setText("Verbilligt")
                self.ui.spinKosten.setValue(self.refD[self.fert].steigerungsfaktor*10)
            else:
                self.ui.labelInfo.setText("")
                self.ui.spinKosten.setValue(self.refD[self.fert].steigerungsfaktor*20)
        else:
            self.ui.labelInfo.setText("Spezialtalent")
            self.ui.spinKosten.setValue(Wolke.DB.talente[talent].kosten)
        self.ui.plainText.setPlainText(Wolke.DB.talente[talent].text)
