# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
import Wolke
import CharakterFertigkeiten
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
        
        self.currentFertName = Wolke.Char.fertigkeiten.
        
        self.uiFert.tableWidget.cellClicked.connect(self.tableClicked)        
        self.loadFertigkeiten()
        
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
        name = self.uiFert.tableWidget.itemAt(row,0).text()
        fert = Wolke.Char.fertigkeiten[name]
        self.uiFert.labelFertigkeit.setText(name)
        self.uiFert.labelAttribute.setText(fert.attribute[0] + "/" 
                                           + fert.attribute[1] + "/" 
                                           + fert.attribute[2])
        self.uiFert.spinSF.setValue(fert.steigerungsfaktor)
        self.uiFert.spinBasis.setValue(fert.basiswert)
        self.uiFert.spinFW.setValue(fert.wert)
        self.uiFert.spinPW.setValue(fert.probenwert)
        self.uiFert.spinPWT.setValue(fert.probenwertTalent)
        self.uiFert.plainText.setPlainText(fert.text)
        self.updateTalents(name)
            
    def updateTalents(self, fertName):
        self.model.clear()
        for el in Wolke.Char.fertigkeiten[fertName].gekaufteTalente:
            item = QtGui.QStandardItem(el)
            item.setEditable(False)
            self.model.appendRow(item)
        
    def editTalents(self, fertName):
        pass