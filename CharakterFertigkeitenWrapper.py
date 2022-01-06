# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterFertigkeiten
import TalentPicker
import MousewheelProtector
from PyQt5 import QtWidgets, QtCore, QtGui
import logging
from PyQt5.QtWidgets import QHeaderView

# This item delegate is used to draw a seperator line between different fertigkeit categories ('printclasses')
class FertigkeitItemDelegate(QtWidgets.QItemDelegate):
    def __init__(self, rowIndicesWithLinePaint):
        super().__init__()
        self.rowIndicesWithLinePaint = rowIndicesWithLinePaint

    def paint (self, painter, option, index):
        if index.row() in self.rowIndicesWithLinePaint:
            painter.setPen(QtGui.QPen(QtCore.Qt.gray, 2))
            painter.drawLine(option.rect.bottomLeft() + QtCore.QPoint(0, 1), option.rect.bottomRight() + QtCore.QPoint(0, 1));
        super().paint(painter, option, index)

class FertigkeitenWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing FertigkeitenWrapper...")
        self.formFert = QtWidgets.QWidget()
        self.uiFert = CharakterFertigkeiten.Ui_Form()
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

        #If there is an ability already, then we take it to display already
        try:
            self.currentFertName = Wolke.Char.fertigkeiten.__iter__().__next__()
        except StopIteration:
            self.currentFertName = ''
        self.currentlyLoading = False
        self.load()
            
    def update(self):
        #Already implemented for the individual events
        pass
        
    def load(self):
        self.currentlyLoading = True
        temp = [el for el in Wolke.DB.fertigkeiten 
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.fertigkeiten[el].voraussetzungen)]
        if temp != self.availableFerts:
            self.availableFerts = temp

            # sort by printclass, then by name
            self.availableFerts.sort(key = lambda x: (Wolke.DB.fertigkeiten[x].printclass, x)) 
            
            rowIndicesWithLinePaint = []
            count = 0
            if len(self.availableFerts) > 0:
                lastPrintclass = Wolke.DB.fertigkeiten[self.availableFerts[0]].printclass
                for el in self.availableFerts:
                    if Wolke.DB.fertigkeiten[el].printclass != lastPrintclass:
                        rowIndicesWithLinePaint.append(count-1)
                        lastPrintclass = Wolke.DB.fertigkeiten[el].printclass
                    count += 1

            self.uiFert.tableWidget.clear()
            self.uiFert.tableWidget.setItemDelegate(FertigkeitItemDelegate(rowIndicesWithLinePaint))
            
            self.uiFert.tableWidget.setRowCount(len(self.availableFerts))
            self.uiFert.tableWidget.setColumnCount(5)
            self.uiFert.tableWidget.verticalHeader().setVisible(False)

            header = self.uiFert.tableWidget.horizontalHeader()
            header.setMinimumSectionSize(0)
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Fixed)
            self.uiFert.tableWidget.setColumnWidth(1, 80)
            header.setSectionResizeMode(2, QHeaderView.Fixed)
            self.uiFert.tableWidget.setColumnWidth(2, 80)
            header.setSectionResizeMode(3, QHeaderView.Fixed)
            self.uiFert.tableWidget.setColumnWidth(3, 40)
            header.setSectionResizeMode(4, QHeaderView.Fixed)
            self.uiFert.tableWidget.setColumnWidth(4, 40)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Name")
            self.uiFert.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("FW")
            item.setToolTip("Fertigkeitswert")
            self.uiFert.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("Talente")
            self.uiFert.tableWidget.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("PW")
            item.setToolTip("Probenwert")
            self.uiFert.tableWidget.setHorizontalHeaderItem(3, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("PW(T)")
            item.setToolTip("Probenwert mit Talent")
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setStretch(87)
            item.setFont(font)
            self.uiFert.tableWidget.setHorizontalHeaderItem(4, item)
    
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
                tableWidget = QtWidgets.QTableWidgetItem(Wolke.Char.fertigkeiten[el].name)
                self.uiFert.tableWidget.setItem(count, 0, tableWidget)

                # Add Spinner for FW
                #self.uiFert.tableWidget.setItem(count,1,QtWidgets.QTableWidgetItem(str(Wolke.Char.fertigkeiten[el].wert)))
                self.spinRef[Wolke.Char.fertigkeiten[el].name] = QtWidgets.QSpinBox()
                self.spinRef[Wolke.Char.fertigkeiten[el].name].setFocusPolicy(QtCore.Qt.StrongFocus)
                self.spinRef[Wolke.Char.fertigkeiten[el].name].installEventFilter(self.mwp)
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

                # Add PW
                self.labelRef[Wolke.Char.fertigkeiten[el].name + "PW"] = QtWidgets.QLabel()
                self.labelRef[Wolke.Char.fertigkeiten[el].name + "PW"].setText(str(Wolke.Char.fertigkeiten[el].probenwert))
                self.labelRef[Wolke.Char.fertigkeiten[el].name + "PW"].setAlignment(QtCore.Qt.AlignCenter)
                self.uiFert.tableWidget.setCellWidget(count,3,self.labelRef[Wolke.Char.fertigkeiten[el].name + "PW"])

                # Add PW (T)
                self.labelRef[Wolke.Char.fertigkeiten[el].name + "PWT"] = QtWidgets.QLabel()
                self.labelRef[Wolke.Char.fertigkeiten[el].name + "PWT"].setText(str(Wolke.Char.fertigkeiten[el].probenwertTalent))
                self.labelRef[Wolke.Char.fertigkeiten[el].name + "PWT"].setAlignment(QtCore.Qt.AlignCenter)
                self.uiFert.tableWidget.setCellWidget(count,4,self.labelRef[Wolke.Char.fertigkeiten[el].name + "PWT"])

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
                #self.uiFert.tableWidget.setItem(self.rowRef[self.currentFertName],1,QtWidgets.QTableWidgetItem(str(Wolke.Char.fertigkeiten[self.currentFertName].wert)))
                if flag:
                    self.uiFert.spinFW.setValue(val)
                else:
                    self.spinRef[self.currentFertName].setValue(val)

                self.labelRef[self.currentFertName + "PW"].setText(str(Wolke.Char.fertigkeiten[self.currentFertName].probenwert))
                self.labelRef[self.currentFertName + "PWT"].setText(str(Wolke.Char.fertigkeiten[self.currentFertName].probenwertTalent))

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
            if self.currentFertName not in Wolke.Char.fertigkeiten:
                self.currentFertName = ""
                self.uiFert.labelFertigkeit.setText("Fertigkeit")
                self.uiFert.labelAttribute.setText("Attribute")
                self.uiFert.spinSF.setValue(0)
                self.uiFert.spinBasis.setValue(0)
                self.uiFert.spinFW.setMaximum(0)
                self.uiFert.spinFW.setValue(0)
                self.uiFert.spinPW.setValue(0)
                self.uiFert.spinPWT.setValue(0)
                self.uiFert.plainText.setPlainText("")
                self.model.clear()
                return
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
                talStr = Wolke.DB.talente[el].getFullName(Wolke.Char).replace(self.currentFertName + ": ", "")
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
            