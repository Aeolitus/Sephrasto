# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterFertigkeiten
import TalentPicker
from PyQt5 import QtWidgets, QtCore, QtGui

class FertigkeitenWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        if Wolke.Debug:
            print("Initializing FertigkeitenWrapper...")
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
        self.uiFert.tableWidget.currentItemChanged.connect(self.tableClicked)   
        self.uiFert.buttonAdd.clicked.connect(self.editTalents)
        
        self.availableFerts = []
        self.rowRef = {}
        self.spinRef = {}
        self.labelRef = {}
        self.layoutRef = {}
        self.buttonRef = {}
        self.widgetRef = {}
        
        #If there is an ability already, then we take it to display already
        try:
            self.currentFertName = Wolke.Char.fertigkeiten.__iter__().__next__()
        except StopIteration:
            self.currentFertName = ''
        self.currentlyLoading = False
        self.loadFertigkeiten()
            
    def updateFertigkeiten(self):
        #Already implemented for the individual events
        pass
        
    def loadFertigkeiten(self):
        self.currentlyLoading = True
        temp = [el for el in Wolke.DB.fertigkeiten 
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.fertigkeiten[el].voraussetzungen)]
        if temp != self.availableFerts:
            self.availableFerts = temp
            self.uiFert.tableWidget.clear()
            
            self.uiFert.tableWidget.setRowCount(len(self.availableFerts))
            self.uiFert.tableWidget.setColumnCount(3)
            self.uiFert.tableWidget.verticalHeader().setVisible(False)
            item = QtWidgets.QTableWidgetItem()
            item.setText("Name")
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
            
            #Remove Abilities for which the conditions are not met
            for el in Wolke.Char.fertigkeiten:
                if el not in self.availableFerts:
                    Wolke.Char.fertigkeiten.pop(el,None)
            
            for el in self.availableFerts:
                #Add abilities that werent there before
                if el not in Wolke.Char.fertigkeiten:
                    Wolke.Char.fertigkeiten.update({el: Wolke.DB.fertigkeiten[el].__deepcopy__()})
                    Wolke.Char.fertigkeiten[el].wert = 0
                Wolke.Char.fertigkeiten[el].aktualisieren()
                self.uiFert.tableWidget.setItem(count, 0, QtWidgets.QTableWidgetItem(Wolke.Char.fertigkeiten[el].name))
                
                # Add Spinner for FW
                #self.uiFert.tableWidget.setItem(count,1,QtWidgets.QTableWidgetItem(str(Wolke.Char.fertigkeiten[el].wert)))
                self.spinRef[Wolke.Char.fertigkeiten[el].name] = QtWidgets.QSpinBox()
                self.spinRef[Wolke.Char.fertigkeiten[el].name].setMinimum(0)
                self.spinRef[Wolke.Char.fertigkeiten[el].name].setMaximum(Wolke.Char.fertigkeiten[el].maxWert)
                self.spinRef[Wolke.Char.fertigkeiten[el].name].setValue(Wolke.Char.fertigkeiten[el].wert)
                self.spinRef[Wolke.Char.fertigkeiten[el].name].setAlignment(QtCore.Qt.AlignCenter)
                self.spinRef[Wolke.Char.fertigkeiten[el].name].valueChanged.connect(lambda state, name=Wolke.Char.fertigkeiten[el].name: self.spinnerClicked(name))
                self.uiFert.tableWidget.setCellWidget(count,1,self.spinRef[Wolke.Char.fertigkeiten[el].name])
                
                # Add Talents Count and Add Button
                self.layoutRef[Wolke.Char.fertigkeiten[el].name] = QtWidgets.QHBoxLayout()
                self.labelRef[Wolke.Char.fertigkeiten[el].name] = QtWidgets.QLabel()
                self.labelRef[Wolke.Char.fertigkeiten[el].name].setText(str(len(Wolke.Char.fertigkeiten[el].gekaufteTalente)))
                self.labelRef[Wolke.Char.fertigkeiten[el].name].setAlignment(QtCore.Qt.AlignCenter)
                #self.labelRef.update({Wolke.Char.fertigkeiten[el].name: lab})
                self.layoutRef[Wolke.Char.fertigkeiten[el].name].addWidget(self.labelRef[Wolke.Char.fertigkeiten[el].name])
                self.buttonRef[Wolke.Char.fertigkeiten[el].name] = QtWidgets.QPushButton()
                self.buttonRef[Wolke.Char.fertigkeiten[el].name].setText("+")
                self.buttonRef[Wolke.Char.fertigkeiten[el].name].setMaximumSize(QtCore.QSize(25, 20))
                self.buttonRef[Wolke.Char.fertigkeiten[el].name].clicked.connect(lambda state, name=Wolke.Char.fertigkeiten[el].name: self.addClicked(name))
                self.layoutRef[Wolke.Char.fertigkeiten[el].name].addWidget(self.buttonRef[Wolke.Char.fertigkeiten[el].name])
                self.widgetRef[Wolke.Char.fertigkeiten[el].name] = QtWidgets.QWidget()
                self.widgetRef[Wolke.Char.fertigkeiten[el].name].setLayout(self.layoutRef[Wolke.Char.fertigkeiten[el].name])
                self.uiFert.tableWidget.setCellWidget(count,2,self.widgetRef[Wolke.Char.fertigkeiten[el].name])
                #self.uiFert.tableWidget.setItem(count,2,QtWidgets.QTableWidgetItem(str(len(Wolke.Char.fertigkeiten[el].gekaufteTalente))))
                self.rowRef.update({Wolke.Char.fertigkeiten[el].name: count})
                count += 1
            self.uiFert.tableWidget.cellClicked.connect(self.tableClicked) 
        self.updateInfo()
        self.updateTalents()    
        self.currentlyLoading = False
        
    def tableClicked(self):
        if not self.currentlyLoading:
            tmp = self.uiFert.tableWidget.item(self.uiFert.tableWidget.currentRow(),0).text()
            if tmp in Wolke.Char.fertigkeiten:    
                self.currentFertName = tmp
                self.updateInfo()
        
    def fwChanged(self, flag = False):
        if not self.currentlyLoading:
            if self.currentFertName != "":
                if flag:
                    val = self.spinRef[self.currentFertName].value()
                else:
                    val = self.uiFert.spinFW.value()
                Wolke.Char.fertigkeiten[self.currentFertName].wert = val
                Wolke.Char.fertigkeiten[self.currentFertName].aktualisieren()
                self.uiFert.spinPW.setValue(Wolke.Char.fertigkeiten[self.currentFertName].probenwert)
                self.uiFert.spinPWT.setValue(Wolke.Char.fertigkeiten[self.currentFertName].probenwertTalent)
                self.modified.emit()
                #self.uiFert.tableWidget.setItem(self.rowRef[self.currentFertName],1,QtWidgets.QTableWidgetItem(str(Wolke.Char.fertigkeiten[self.currentFertName].wert)))
                if flag:
                    self.uiFert.spinFW.setValue(val)
                else:
                    self.spinRef[self.currentFertName].setValue(val)
    
    def spinnerClicked(self, fert):
        if not self.currentlyLoading:
            self.currentFertName = fert
            self.updateInfo()
            self.fwChanged(True)
            
    def addClicked(self, fert):
        self.currentFertName = fert
        self.updateInfo()
        self.editTalents()
        
    def updateInfo(self):
        if self.currentFertName != "":
            self.currentlyLoading = True
            fert = Wolke.Char.fertigkeiten[self.currentFertName]
            fert.aktualisieren()
            self.uiFert.labelFertigkeit.setText(self.currentFertName)
            self.uiFert.labelAttribute.setText(fert.attribute[0] + "/" 
                                               + fert.attribute[1] + "/" 
                                               + fert.attribute[2])
            self.uiFert.spinSF.setValue(fert.steigerungsfaktor)
            self.uiFert.spinBasis.setValue(fert.basiswert)
            self.uiFert.spinFW.setMaximum(fert.maxWert)
            self.spinRef[self.currentFertName].setMaximum(fert.maxWert)
            self.uiFert.spinFW.setValue(fert.wert)
            self.uiFert.spinPW.setValue(fert.probenwert)
            self.uiFert.spinPWT.setValue(fert.probenwertTalent)
            self.uiFert.plainText.setPlainText(fert.text)
            self.updateTalents()
            self.currentlyLoading = False
        
    def updateTalents(self):
        if self.currentFertName != "":
            self.model.clear()
            for el in Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente:
                if el.startswith("Gebräuche: "):
                    talStr = el[11:]
                elif el.startswith("Mythen: "):
                    talStr = el[8:]
                elif el.startswith("Überleben: "):
                    talStr = el[11:]
                else:
                    talStr = el
                item = QtGui.QStandardItem(talStr)
                item.setEditable(False)
                self.model.appendRow(item)
            self.updateTalentRow()
        
    def editTalents(self):
        if self.currentFertName != "":
            tal = TalentPicker.TalentPicker(self.currentFertName, False)
            if tal.gekaufteTalente is not None:
                self.modified.emit()
                self.updateTalents()
                
    def updateTalentRow(self):
        for i in range(self.uiFert.tableWidget.rowCount()):
            fert = self.uiFert.tableWidget.item(i,0).text()
            #self.uiFert.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(len(Wolke.Char.fertigkeiten[fert].gekaufteTalente))))
            self.labelRef[fert].setText(str(len(Wolke.Char.fertigkeiten[fert].gekaufteTalente)))
            