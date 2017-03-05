# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import CharakterTalente
from PyQt5 import QtCore, QtWidgets, QtGui

class TalentPicker(object):
    def __init__(self,fert,datenbank,gekauft=[]):
        super().__init__()
        
        self.gekaufteTalente = gekauft
        self.db = datenbank
        self.fert = fert
        
        self.Form = QtWidgets.QDialog()
        self.ui = CharakterTalente.Ui_Dialog()
        self.ui.setupUi(self.Form)
        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)
        self.ui.listTalente.clicked.connect(self.talClicked)
        
        for el in datenbank.talente:
            if fert in datenbank.talente[el].fertigkeiten:
                item = QtGui.QStandardItem(el)
                item.setEditable(False)
                item.setCheckable(True)
                if el in self.gekaufteTalente:
                    item.setCheckState(2)
                else:
                    item.setCheckState(0)
                #TODO: Voraussetzungen prüfen!
                self.model.appendRow(item)
        self.ui.listTalente.setModel(self.model)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            self.gekaufteTalente = []
            for i in range(self.model.rowCount()):
                if self.model.item(i).checkState:
                    self.gekaufteTalente.append(self.model.item(i).text())
        else:
            self.gekaufteTalente = None
        
    @QtCore.pyqtSlot("QModelIndex")   
    def talClicked(self, item):
        text = self.model.itemData(item)[0]
        self.updateFields(text)
        
    def updateFields(self, talent):
        self.ui.labelName.setText(self.db.talente[talent].name)
        if self.db.talente[talent].kosten == -1:
            if self.db.talente[talent].verbilligt:
                self.ui.labelInfo.setText("Verbilligt")
                self.ui.spinKosten.setValue(self.db.fertigkeiten[self.fert].steigerungsfaktor*20)
            else:
                self.ui.labelInfo.setText("")
                self.ui.spinKosten.setValue(self.db.fertigkeiten[self.fert].steigerungsfaktor*10)
        else:
            self.ui.labelInfo.setText("Spezialtalent")
            self.ui.spinKosten.setValue(self.db.talente[talent].kosten)
        self.ui.plainText.setPlainText(self.db.talente[talent].text)
