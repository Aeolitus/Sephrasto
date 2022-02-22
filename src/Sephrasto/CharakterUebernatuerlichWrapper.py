# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterUebernatuerlich
import TalentPicker
import MousewheelProtector
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QHeaderView
import logging
from CharakterProfaneFertigkeitenWrapper import FertigkeitItemDelegate

class UebernatuerlichWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing UebernatuerlichWrapper...")
        self.formFert = QtWidgets.QWidget()
        self.uiFert = UI.CharakterUebernatuerlich.Ui_Form()
        self.uiFert.setupUi(self.formFert)
        
        self.model = QtGui.QStandardItemModel(self.uiFert.listTalente)
        self.uiFert.listTalente.setModel(self.model)

        self.mwp = MousewheelProtector.MousewheelProtector()

        self.uiFert.splitter.adjustSize()
        width = self.uiFert.splitter.size().width()
        self.uiFert.splitter.setSizes([int(width*0.6), int(width*0.4)])

        #Signals
        self.uiFert.spinFW.valueChanged.connect(lambda state : self.fwChanged(False))
        self.uiFert.tableWidget.currentItemChanged.connect(self.tableClicked)   
        self.uiFert.buttonAdd.setStyle(None) # dont know why but the below settings wont do anything without it
        self.uiFert.buttonAdd.setFont(QtGui.QFont("Font Awesome 6 Free Solid", 9, QtGui.QFont.Black))
        self.uiFert.buttonAdd.setText('\u002b')
        self.uiFert.buttonAdd.setMaximumSize(QtCore.QSize(20, 20))
        self.uiFert.buttonAdd.setMinimumSize(QtCore.QSize(20, 20))
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
        
        self.uiFert.tableWidget.setColumnHidden(0, not Wolke.Char.ueberPDFAnzeigen)

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
            self.uiFert.tableWidget.setColumnCount(5)
            header = self.uiFert.tableWidget.horizontalHeader()
            header.setMinimumSectionSize(0)
            header.setSectionResizeMode(0, QHeaderView.Fixed)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.Fixed)
            header.setSectionResizeMode(3, QHeaderView.Fixed)
            header.setSectionResizeMode(4, QHeaderView.Fixed)
            self.uiFert.tableWidget.setColumnWidth(0, 40)
            self.uiFert.tableWidget.setColumnWidth(2, 65)
            self.uiFert.tableWidget.setColumnWidth(3, 65)
            self.uiFert.tableWidget.setColumnWidth(4, 90)

            item = QtWidgets.QTableWidgetItem()
            item.setText("PDF")
            item.setToolTip("Fertigkeit in Charakterblatt übernehmen?")
            self.uiFert.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("Name")
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            self.uiFert.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("FW")
            item.setToolTip("Fertigkeitswert")
            self.uiFert.tableWidget.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("PW")
            item.setToolTip("Probenwert")
            self.uiFert.tableWidget.setHorizontalHeaderItem(3, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("Talente")
            self.uiFert.tableWidget.setHorizontalHeaderItem(4, item)
            
    
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
                fert = Wolke.Char.übernatürlicheFertigkeiten[el]
                fert.aktualisieren(Wolke.Char.attribute)

                self.pdfRef[el] = QtWidgets.QCheckBox()
                self.pdfRef[el].setStyleSheet("margin-left:10; margin-right:10;");
                self.pdfRef[el].setChecked(fert.addToPDF)
                self.pdfRef[el].stateChanged.connect(lambda state, name=el: self.addToPDFClicked(name, state))
                self.uiFert.tableWidget.setCellWidget(count,0,self.pdfRef[el])

                self.uiFert.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem(el))
                
                # Add Spinner for FW
                self.spinRef[el] = QtWidgets.QSpinBox()
                self.spinRef[el].setFocusPolicy(QtCore.Qt.StrongFocus)
                self.spinRef[el].installEventFilter(self.mwp)
                self.spinRef[el].setMinimum(0)
                self.spinRef[el].setMaximum(fert.maxWert)
                self.spinRef[el].setValue(fert.wert)
                self.spinRef[el].setAlignment(QtCore.Qt.AlignCenter)
                self.spinRef[el].valueChanged.connect(lambda state, name=el: self.spinnerClicked(name))
                self.uiFert.tableWidget.setCellWidget(count,2,self.spinRef[el])
                
                # Add PW
                self.labelRef[el + "PW"] = QtWidgets.QLabel()
                self.labelRef[el + "PW"].setText(str(fert.probenwertTalent))
                self.labelRef[el + "PW"].setAlignment(QtCore.Qt.AlignCenter)
                self.uiFert.tableWidget.setCellWidget(count,3,self.labelRef[el + "PW"])

                # Add Talents Count and Add Button
                self.layoutRef[el] = QtWidgets.QHBoxLayout()
                self.labelRef[el] = QtWidgets.QLabel()
                self.labelRef[el].setText(str(len(fert.gekaufteTalente)))
                self.labelRef[el].setAlignment(QtCore.Qt.AlignCenter)
                self.layoutRef[el].addWidget(self.labelRef[el])
                self.buttonRef[el] = QtWidgets.QPushButton()
                self.buttonRef[el].setFont(QtGui.QFont("Font Awesome 6 Free Solid", 9, QtGui.QFont.Black))
                self.buttonRef[el].setText('\u002b')
                self.buttonRef[el].setMaximumSize(QtCore.QSize(20, 20))
                self.buttonRef[el].setMinimumSize(QtCore.QSize(20, 20))
                self.buttonRef[el].clicked.connect(lambda state, name=el: self.addClicked(name))
                self.layoutRef[el].addWidget(self.buttonRef[el])
                self.widgetRef[el] = QtWidgets.QWidget()
                self.widgetRef[el].setLayout(self.layoutRef[el])
                self.uiFert.tableWidget.setCellWidget(count,4,self.widgetRef[el])

                self.rowRef.update({fert.name: count})
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
                Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].aktualisieren(Wolke.Char.attribute)
                self.uiFert.spinPW.setValue(Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].probenwertTalent)
                if flag:
                    self.uiFert.spinFW.setValue(val)
                else:
                    self.spinRef[self.currentFertName].setValue(val)

                self.labelRef[self.currentFertName + "PW"].setText(str(Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName].probenwertTalent))

                self.updateAddToPDF()

                self.modified.emit()
    
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
                self.uiFert.labelKategorie.setText("")
                self.model.clear()
                return
            self.currentlyLoading = True
            fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
            fert.aktualisieren(Wolke.Char.attribute)
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
            self.uiFert.plainText.setPlainText(fert.text)
            fertigkeitTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen übernatürlich"].toTextList()
            self.uiFert.labelKategorie.setText(fertigkeitTypen[fert.printclass])
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
                item.setSelectable(False)
                self.model.appendRow(item)
            self.uiFert.listTalente.setMaximumHeight(max(len(fert.gekaufteTalente), 1) * self.uiFert.listTalente.sizeHintForRow(0) +\
               self.uiFert.listTalente.contentsMargins().top() +\
               self.uiFert.listTalente.contentsMargins().bottom() +\
               self.uiFert.listTalente.spacing())
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
            self.labelRef[fert].setText(str(len(Wolke.Char.übernatürlicheFertigkeiten[fert].gekaufteTalente)))

    def updateAddToPDF(self):
        if self.currentFertName != "":
            fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
            add = len(fert.gekaufteTalente) > 0 and fert.wert > 0
            fert.addToPDF = add
            self.pdfRef[self.currentFertName].setChecked(add)
            