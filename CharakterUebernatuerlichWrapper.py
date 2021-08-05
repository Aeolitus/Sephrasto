# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterUebernatuerlich
import TalentPicker
import MousewheelProtector
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QHeaderView
import logging
from CharakterFertigkeitenWrapper import FertigkeitItemDelegate

class UebernatuerlichWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing UebernatuerlichWrapper...")
        self.formFert = QtWidgets.QWidget()
        self.uiFert = CharakterUebernatuerlich.Ui_Form()
        self.uiFert.setupUi(self.formFert)
        header = self.uiFert.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, 1)
        header.setSectionResizeMode(1, 3)
        header.setSectionResizeMode(2, 3)
        
        self.model = QtGui.QStandardItemModel(self.uiFert.listTalente)
        self.uiFert.listTalente.setModel(self.model)

        self.mwp = MousewheelProtector.MousewheelProtector()

        #Signals
        self.uiFert.spinFW.valueChanged.connect(lambda state : self.fwChanged(False))
        self.uiFert.tableWidget.currentItemChanged.connect(self.tableClicked)   
        self.uiFert.buttonAdd.clicked.connect(self.editTalents)
        
        self.availableFerts = []
        self.rowRef = {}
        self.spinRef = {}
        self.labelRef = {}
        self.layoutRef = {}
        self.buttonRef = {}
        self.widgetRef = {}
        self.pdfRef = {}
        
        #If there is an ability already, then we take it to display already
        self.currentFertName = next(iter(Wolke.Char.übernatürlicheFertigkeiten), "")
        self.currentlyLoading = False
        self.load()
            
    def update(self):
        #Already implemented for the individual events
        pass
        
    def load(self):
        self.currentlyLoading = True
        temp = [el for el in Wolke.DB.übernatürlicheFertigkeiten 
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.übernatürlicheFertigkeiten[el].voraussetzungen)]
        if temp != self.availableFerts:
            self.availableFerts = temp

            # sort by printclass, then by name
            self.availableFerts.sort(key = lambda x: (Wolke.DB.übernatürlicheFertigkeiten[x].printclass, x)) 

            rowIndicesWithLinePaint = []
            count = 0
            if len(self.availableFerts) > 0:
                lastPrintclass = Wolke.DB.übernatürlicheFertigkeiten[self.availableFerts[0]].printclass
                for el in self.availableFerts:
                    if Wolke.DB.übernatürlicheFertigkeiten[el].printclass != lastPrintclass:
                        rowIndicesWithLinePaint.append(count-1)
                        lastPrintclass = Wolke.DB.übernatürlicheFertigkeiten[el].printclass
                    count += 1

            self.uiFert.tableWidget.clear()
            self.uiFert.tableWidget.setItemDelegate(FertigkeitItemDelegate(rowIndicesWithLinePaint))

            self.uiFert.tableWidget.setRowCount(len(self.availableFerts))
            self.uiFert.tableWidget.setColumnCount(4)
            header = self.uiFert.tableWidget.horizontalHeader()
            header.setMinimumSectionSize(0)
            header.setSectionResizeMode(0, QHeaderView.Fixed)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.Fixed)
            header.setSectionResizeMode(3, QHeaderView.Fixed)
            self.uiFert.tableWidget.setColumnWidth(0, 40)
            self.uiFert.tableWidget.setColumnWidth(2, 80)
            self.uiFert.tableWidget.setColumnWidth(3, 80)

            #header.setMinimumSectionSize

            self.uiFert.tableWidget.verticalHeader().setVisible(False)
            item = QtWidgets.QTableWidgetItem()
            item.setText("PDF")
            self.uiFert.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("Name")
            self.uiFert.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("FW")
            self.uiFert.tableWidget.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("Talente")
            self.uiFert.tableWidget.setHorizontalHeaderItem(3, item)
    
            count = 0
            
            #Remove Abilities for which the conditions are not met
            for el in Wolke.Char.übernatürlicheFertigkeiten:
                if el not in self.availableFerts:
                    Wolke.Char.übernatürlicheFertigkeiten.pop(el,None)
            
            for el in self.availableFerts:
                #Add abilities that werent there before
                if el not in Wolke.Char.übernatürlicheFertigkeiten:
                    Wolke.Char.übernatürlicheFertigkeiten.update({el: Wolke.DB.übernatürlicheFertigkeiten[el].__deepcopy__()})
                    Wolke.Char.übernatürlicheFertigkeiten[el].wert = 0
                    Wolke.Char.übernatürlicheFertigkeiten[el].addToPDF = False
                Wolke.Char.übernatürlicheFertigkeiten[el].aktualisieren()

                self.pdfRef[Wolke.Char.übernatürlicheFertigkeiten[el].name] = QtWidgets.QCheckBox()
                self.pdfRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setStyleSheet("margin-left:10; margin-right:10;");
                self.pdfRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setChecked(Wolke.Char.übernatürlicheFertigkeiten[el].addToPDF)
                self.pdfRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].stateChanged.connect(lambda state, name=Wolke.Char.übernatürlicheFertigkeiten[el].name: self.addToPDFClicked(name, state))
                self.uiFert.tableWidget.setCellWidget(count,0,self.pdfRef[Wolke.Char.übernatürlicheFertigkeiten[el].name])

                self.uiFert.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem(Wolke.Char.übernatürlicheFertigkeiten[el].name))
                
                # Add Spinner for FW
                #self.uiFert.tableWidget.setItem(count,1,QtWidgets.QTableWidgetItem(str(Wolke.Char.übernatürlicheFertigkeiten[el].wert)))
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name] = QtWidgets.QSpinBox()
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setFocusPolicy(QtCore.Qt.StrongFocus)
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].installEventFilter(self.mwp)
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setMinimum(0)
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setMaximum(Wolke.Char.übernatürlicheFertigkeiten[el].maxWert)
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setValue(Wolke.Char.übernatürlicheFertigkeiten[el].wert)
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setAlignment(QtCore.Qt.AlignCenter)
                self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].valueChanged.connect(lambda state, name=Wolke.Char.übernatürlicheFertigkeiten[el].name: self.spinnerClicked(name))
                self.uiFert.tableWidget.setCellWidget(count,2,self.spinRef[Wolke.Char.übernatürlicheFertigkeiten[el].name])
                
                # Add Talents Count and Add Button
                self.layoutRef[Wolke.Char.übernatürlicheFertigkeiten[el].name] = QtWidgets.QHBoxLayout()
                self.labelRef[Wolke.Char.übernatürlicheFertigkeiten[el].name] = QtWidgets.QLabel()
                self.labelRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setText(str(len(Wolke.Char.übernatürlicheFertigkeiten[el].gekaufteTalente)))
                self.labelRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setAlignment(QtCore.Qt.AlignCenter)
                #self.labelRef.update({Wolke.Char.übernatürlicheFertigkeiten[el].name: lab})
                self.layoutRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].addWidget(self.labelRef[Wolke.Char.übernatürlicheFertigkeiten[el].name])
                self.buttonRef[Wolke.Char.übernatürlicheFertigkeiten[el].name] = QtWidgets.QPushButton()
                self.buttonRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setText("+")
                self.buttonRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setMaximumSize(QtCore.QSize(25, 20))
                self.buttonRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].clicked.connect(lambda state, name=Wolke.Char.übernatürlicheFertigkeiten[el].name: self.addClicked(name))
                self.layoutRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].addWidget(self.buttonRef[Wolke.Char.übernatürlicheFertigkeiten[el].name])
                self.widgetRef[Wolke.Char.übernatürlicheFertigkeiten[el].name] = QtWidgets.QWidget()
                self.widgetRef[Wolke.Char.übernatürlicheFertigkeiten[el].name].setLayout(self.layoutRef[Wolke.Char.übernatürlicheFertigkeiten[el].name])
                self.uiFert.tableWidget.setCellWidget(count,3,self.widgetRef[Wolke.Char.übernatürlicheFertigkeiten[el].name])
                #self.uiFert.tableWidget.setItem(count,2,QtWidgets.QTableWidgetItem(str(len(Wolke.Char.übernatürlicheFertigkeiten[el].gekaufteTalente))))
                self.rowRef.update({Wolke.Char.übernatürlicheFertigkeiten[el].name: count})
                count += 1
            self.uiFert.tableWidget.cellClicked.connect(self.tableClicked) 
        self.updateInfo()
        self.updateTalents()    
        self.currentlyLoading = False
        
    def tableClicked(self):
        if not self.currentlyLoading:
            tmp = self.uiFert.tableWidget.item(self.uiFert.tableWidget.currentRow(),1).text()
            if tmp in Wolke.Char.übernatürlicheFertigkeiten:    
                self.currentFertName = tmp
                self.updateInfo()
        
    def fwChanged(self, flag = False):
        if not self.currentlyLoading:
            if self.currentFertName != "":
                if flag:
                    val = self.spinRef[self.currentFertName].value()
                else:
                    val = self.uiFert.spinFW.value()
                Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].wert = val
                Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].aktualisieren()
                self.uiFert.spinPW.setValue(Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].probenwertTalent)
                #self.uiFert.spinPWT.setValue(Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].probenwertTalent)
                self.modified.emit()
                #self.uiFert.tableWidget.setItem(self.rowRef[self.currentFertName],1,QtWidgets.QTableWidgetItem(str(Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].wert)))
                if flag:
                    self.uiFert.spinFW.setValue(val)
                else:
                    self.spinRef[self.currentFertName].setValue(val)
                self.updateAddToPDF()
    
    def addToPDFClicked(self, fert, state):
        Wolke.Char.übernatürlicheFertigkeiten[fert].addToPDF = state
        self.modified.emit()

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
            if self.currentFertName not in Wolke.Char.übernatürlicheFertigkeiten:
                self.currentFertName = ""
                self.uiFert.labelFertigkeit.setText("Fertigkeit")
                self.uiFert.labelAttribute.setText("Attribute")
                self.uiFert.spinSF.setValue(0)
                self.uiFert.spinBasis.setValue(0)
                self.uiFert.spinFW.setMaximum(0)
                self.uiFert.spinFW.setValue(0)
                self.uiFert.spinPW.setValue(0)
                self.uiFert.plainText.setPlainText("")
                self.model.clear()
                return
            self.currentlyLoading = True
            fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
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
            self.uiFert.spinPW.setValue(fert.probenwertTalent)
            #self.uiFert.spinPWT.setValue(fert.probenwertTalent)
            self.uiFert.plainText.setPlainText(fert.text)
            self.updateTalents()
            self.currentlyLoading = False
        
    def updateTalents(self):
        if self.currentFertName != "":
            self.model.clear()
            fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
            for el in fert.gekaufteTalente:
                talStr = Wolke.DB.talente[el].getFullName(Wolke.Char).replace(self.currentFertName + ": ", "")
                costStr = ""
                if not el in Wolke.Char.talenteVariable:
                    costStr = " (" + str(Wolke.Char.getTalentCost(el, fert.steigerungsfaktor)) + " EP)"
                item = QtGui.QStandardItem(talStr + costStr)
                item.setEditable(False)
                self.model.appendRow(item)
            self.updateTalentRow()
        
    def editTalents(self):
        if self.currentFertName != "":
            tal = TalentPicker.TalentPicker(self.currentFertName, True)
            self.updateAddToPDF()
            if tal.gekaufteTalente is not None:
                self.modified.emit()
                self.updateTalents()
                
    def updateTalentRow(self):
        for i in range(self.uiFert.tableWidget.rowCount()):
            fert = self.uiFert.tableWidget.item(i,1).text()
            #self.uiFert.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(len(Wolke.Char.übernatürlicheFertigkeiten[fert].gekaufteTalente))))
            self.labelRef[fert].setText(str(len(Wolke.Char.übernatürlicheFertigkeiten[fert].gekaufteTalente)))

    def updateAddToPDF(self):
        if self.currentFertName != "":
            fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
            add = len(fert.gekaufteTalente) > 0 and fert.wert > 0
            fert.addToPDF = add
            self.pdfRef[self.currentFertName].setChecked(add)
            