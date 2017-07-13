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
        self.talenteVariable = Wolke.Char.talenteVariable.copy()
        self.gekaufteTalente = self.refC[fert].gekaufteTalente.copy()
        self.fert = fert
        self.Form = QtWidgets.QDialog()
        self.ui = CharakterTalente.Ui_Dialog()
        self.ui.setupUi(self.Form)
        
        self.Form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)
        self.ui.listTalente.selectionModel().currentChanged.connect(self.talChanged)
        
        if self.fert == "Gebräuche":
            self.baseStr = "Gebräuche: "
#==============================================================================
#         elif self.fert == "Mythenkunde":
#             self.baseStr = "Mythen: "
#==============================================================================
        elif self.fert == "Überleben":
            self.baseStr = "Überleben: "
        else: 
            self.baseStr = None
        
        self.rowCount = 0
        for el in Wolke.DB.talente:
            if fert in Wolke.DB.talente[el].fertigkeiten and Wolke.Char.voraussetzungenPrüfen(Wolke.DB.talente[el].voraussetzungen):
                if Wolke.DB.talente[el].variable:
                    if el not in self.talenteVariable:
                        self.talenteVariable[el] = Wolke.DB.talente[el].kosten
                item = QtGui.QStandardItem(self.displayStr(el))
                item.setEditable(False)
                item.setCheckable(True)
                if el in self.gekaufteTalente:
                    item.setCheckState(2)
                else:
                    item.setCheckState(0)
                self.model.appendRow(item)
                self.rowCount += 1
        if self.rowCount > 0:
            self.updateFields(self.dataStr(self.model.item(0).text()))
        self.ui.spinKosten.valueChanged.connect(self.spinChanged)
        self.ui.spinKosten.setStyleSheet("QSpinBox {background-color: #FFFFFF}")
        self.ui.listTalente.setModel(self.model)
        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            self.gekaufteTalente = []
            for i in range(self.rowCount):
                tmp = self.dataStr(self.model.item(i).text())
                if self.model.item(i).checkState() == QtCore.Qt.Checked:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp not in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.append(tmp)
                    if Wolke.DB.talente[tmp].variable:
                        Wolke.Char.talenteVariable[tmp] = self.talenteVariable[tmp]
                else:
                    for el in Wolke.DB.talente[tmp].fertigkeiten:
                        if el in self.refC:
                            if tmp in self.refC[el].gekaufteTalente:
                                self.refC[el].gekaufteTalente.remove(tmp)

            self.gekaufteTalente = self.refC[fert].gekaufteTalente
        else:
            self.gekaufteTalente = None
    
    @QtCore.pyqtSlot("QModelIndex", "QModelIndex")       
    def talChanged(self, item, prev):
        text = self.dataStr(self.model.itemData(item)[0])
        self.updateFields(text)
        
    def spinChanged(self):
        self.talenteVariable[self.ui.labelName.text()] = self.ui.spinKosten.value()
        
    def updateFields(self, talent):
        if talent is not None:
            self.ui.labelName.setText(self.displayStr(Wolke.DB.talente[talent].name))
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
            if Wolke.DB.talente[talent].variable:
                self.ui.spinKosten.setReadOnly(False)
                self.ui.spinKosten.setButtonSymbols(0)
                if talent in Wolke.Char.talenteVariable:
                    self.ui.spinKosten.setValue(Wolke.Char.talenteVariable[talent])
            else:
                self.ui.spinKosten.setReadOnly(True)
                self.ui.spinKosten.setButtonSymbols(2)
            self.ui.plainText.setPlainText(Wolke.DB.talente[talent].text)

    def displayStr(self,inp):
        if self.baseStr is not None:
            if inp.startswith(self.baseStr):
                return inp[len(self.baseStr):]
        return inp
        
    def dataStr(self,inp):
        if self.baseStr is not None:
            return self.baseStr + inp
        return inp
        