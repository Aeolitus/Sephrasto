# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
import Wolke
import CharakterFertigkeiten
import TalentPicker
import Fertigkeiten
from PyQt5 import QtWidgets, QtCore, QtGui

class FertWrapper(object):
    def __init__(self):
        super().__init__()
        self.formFert = QtWidgets.QWidget()
        self.uiFert = CharakterFertigkeiten.Ui_Form()
        self.uiFert.setupUi(self.formFert)
        header = self.uiFert.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, 1)
        header.setSectionResizeMode(1, 3)
        header.setSectionResizeMode(2, 3)
        
        self.model = QtGui.QStandardItemModel(self.uiFert.listTalente)
        self.uiFert.listTalente.setModel(self.model)
        
        self.uiFert.tableWidget.cellClicked.connect(self.tableClicked)   
        self.uiFert.buttonAdd.clicked.connect(self.editTalents)
        
        #A bit hacky. Sorry.
        try:
            self.currentFertName = Wolke.Char.fertigkeiten.__iter__().__next__()
        except StopIteration:
            self.currentFertName = ''
        else:
            self.loadFertigkeiten()
        
    def updateFertigkeiten(self):
        for i in range(self.uiFert.tableWidget.rowCount):
            name = self.uiFert.tableWidget.itemAt(i,0).text()
            fert = Wolke.Char.fertigkeiten[name]
            if fert is None:
                fert = Fertigkeiten.Fertigkeit()
                fert.name = name
            fert.wert = self.uiFert.spinFW.value()
            fert.aktualisieren()
            Wolke.Char.fertigkeiten.update({name: fert})
        Wolke.Char.aktualisieren()
    
    def loadFertigkeiten(self):
        Wolke.Char.aktualisieren()
        self.uiFert.tableWidget.clear()
        
        self.uiFert.tableWidget.setRowCount(len(Wolke.DB.fertigkeiten))
        self.uiFert.tableWidget.setColumnCount(3)
        self.uiFert.tableWidget.verticalHeader().setVisible(False)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Bezeichnung")
        self.uiFert.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("FW")
        self.uiFert.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("Talente")
        self.uiFert.tableWidget.setHorizontalHeaderItem(2, item)

        count = 0
        for el in Wolke.DB.fertigkeiten:
            self.uiFert.tableWidget.setItem(count, 0, QtWidgets.QTableWidgetItem(Wolke.DB.fertigkeiten[el].name))
            self.uiFert.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("1"))
            self.uiFert.tableWidget.setItem(count, 2, QtWidgets.QTableWidgetItem("2"))
        self.uiFert.tableWidget.cellClicked.connect(self.tableClicked) 
            
    def tableClicked(self,row,col):
        self.currentFertName = self.uiFert.tableWidget.itemAt(row,0).text()
        self.updateInfo()
        
    def updateInfo(self):
        fert = Wolke.Char.fertigkeiten[self.currentFertName]
        self.uiFert.labelFertigkeit.setText(self.currentFertName)
        self.uiFert.labelAttribute.setText(fert.attribute[0] + "/" 
                                           + fert.attribute[1] + "/" 
                                           + fert.attribute[2])
        self.uiFert.spinSF.setValue(fert.steigerungsfaktor)
        self.uiFert.spinBasis.setValue(fert.basiswert)
        self.uiFert.spinFW.setValue(fert.wert)
        self.uiFert.spinPW.setValue(fert.probenwert)
        self.uiFert.spinPWT.setValue(fert.probenwertTalent)
        self.uiFert.plainText.setPlainText(fert.text)
        self.updateTalents()
            
    def updateTalents(self):
        self.model.clear()
        for el in Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente:
            item = QtGui.QStandardItem(el)
            item.setEditable(False)
            self.model.appendRow(item)
        
    def editTalents(self):
        tal = TalentPicker.TalentPicker()
        if tal.gekaufteTalente is not None:
            #TODO: Voraussetzungen, Kosten
            Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente = tal.gekaufteTalente