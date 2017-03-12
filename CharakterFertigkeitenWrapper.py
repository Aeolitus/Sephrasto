# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
import Wolke
import CharakterFertigkeiten
import TalentPicker
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
        
        #Signals
        self.uiFert.spinFW.valueChanged.connect(self.fwChanged)
        
        self.uiFert.tableWidget.cellClicked.connect(self.tableClicked)   
        self.uiFert.buttonAdd.clicked.connect(self.editTalents)
        
        #A bit hacky. Sorry.
        try:
            self.currentFertName = Wolke.Char.fertigkeiten.__iter__().__next__()
        except StopIteration:
            self.currentFertName = ''
        else:
            self.initFertigkeiten()
            
    def updateFertigkeiten(self):
        pass
        
    def loadFertigkeiten(self):
        for i in range(self.uiFert.tableWidget.rowCount):
            name = self.uiFert.tableWidget.itemAt(i,0).text()
            self.uiFert.tableWidget.setItem(i,1,str(Wolke.Char.fertigkeiten[name].wert))
            self.uiFert.tableWidget.setItem(i,2,str(len(Wolke.Char.fertigkeiten[name].gekaufteTalente)))
    
    def initFertigkeiten(self):
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
            #self.uiFert.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("-"))
            #self.uiFert.tableWidget.setItem(count, 2, QtWidgets.QTableWidgetItem("-"))
            count += 1
        self.uiFert.tableWidget.cellClicked.connect(self.tableClicked) 
        self.loadFertigkeiten()
            
    def tableClicked(self,row,col):
        self.currentFertName = self.uiFert.tableWidget.itemAt(row,0).text()
        self.updateInfo()
        
    def fwChanged(self):
        Wolke.Char.fertigkeiten[self.currentFertName].wert = self.uiFert.spinFW.value()
        Wolke.Char.fertigkeiten[self.currentFertName].aktualisieren()
        self.uiFert.spinPW.setValue(Wolke.Char.fertigkeiten[self.currentFertName].probenwert)
        self.uiFert.spinPWT.setValue(Wolke.Char.fertigkeiten[self.currentFertName].probenwertTalent)
        self.loadFertigkeiten()
        
    def updateInfo(self):
        fert = Wolke.Char.fertigkeiten[self.currentFertName]
        fert.aktualisieren()
        self.uiFert.labelFertigkeit.setText(self.currentFertName)
        self.uiFert.labelAttribute.setText(fert.attribute[0] + "/" 
                                           + fert.attribute[1] + "/" 
                                           + fert.attribute[2])
        self.uiFert.spinSF.setValue(fert.steigerungsfaktor)
        self.uiFert.spinBasis.setValue(fert.basiswert)
        self.uiFert.spinFW.setValue(fert.wert)
        self.uiFert.spinFW.setMaximum(fert.maxWert)
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
        tal = TalentPicker.TalentPicker(self.currentFertName)
        if tal.gekaufteTalente is not None:
            #TODO: Voraussetzungen, Kosten
            Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente = tal.gekaufteTalente
            self.updateTalents()
            self.loadFertigkeiten()