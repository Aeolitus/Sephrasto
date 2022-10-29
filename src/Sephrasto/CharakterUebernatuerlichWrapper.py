# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterUebernatuerlich
import CharakterTalentPickerWrapper
import MousewheelProtector
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QHeaderView
import logging
from CharakterProfaneFertigkeitenWrapper import FertigkeitItemDelegate
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus

class UebernatuerlichWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing UebernatuerlichWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterUebernatuerlich.Ui_Form()
        self.ui.setupUi(self.form)
        
        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)

        self.mwp = MousewheelProtector.MousewheelProtector()

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        #Signals
        self.ui.spinFW.valueChanged.connect(lambda: self.fwChanged(False))
        self.ui.tableWidget.currentCellChanged.connect(self.tableClicked)   
        self.ui.tableWidget.cellClicked.connect(self.tableClicked) 
        self.ui.buttonAdd.setStyle(None) # dont know why but the below settings wont do anything without it
        self.ui.buttonAdd.setText('\u002b')
        self.ui.buttonAdd.setMaximumSize(QtCore.QSize(20, 20))
        self.ui.buttonAdd.setMinimumSize(QtCore.QSize(20, 20))
        self.ui.buttonAdd.clicked.connect(self.editTalents)
        
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
            
    def update(self):
        #Already implemented for the individual events
        pass

    def getNonOptimalFerts(self, ferts):
        availableTalents = []
        for t in Wolke.DB.talente:
            talent = Wolke.DB.talente[t]
            if not talent.isSpezialTalent():
                continue
            if talent.name.endswith("(passiv)") or talent.name.endswith("(Passiv)"):
                if not " PW " in talent.text:
                    continue
            if Wolke.Char.voraussetzungenPrüfen(talent.voraussetzungen):
                availableTalents.append(talent)

        result = []
        for el in ferts:
            totalTalentCost = 0
             # going to use the word unique for talents that the char has only one fert for
            uniqueTalentCost = 0
            uniqueTalentOwned = False
            for talent in availableTalents:
                available = False
                unique = True
                owned = False
                for talFert in talent.fertigkeiten:
                    if talFert in Wolke.Char.übernatürlicheFertigkeiten:
                        owned = owned or talent.name in Wolke.Char.übernatürlicheFertigkeiten[talFert].gekaufteTalente
                    if talFert == el:
                        available = True
                    elif talFert in ferts:
                        unique = False
                if not available:
                    continue
                totalTalentCost += talent.kosten
                if unique:
                    uniqueTalentCost += talent.kosten
                    if owned:
                        uniqueTalentOwned = True

            if uniqueTalentOwned:
                continue
            if totalTalentCost < 120 or (totalTalentCost < 180 and uniqueTalentCost < 60):
                result.append(el)

        return result

    def load(self):
        self.currentlyLoading = True
        
        self.ui.tableWidget.setColumnHidden(0, not Wolke.Char.ueberPDFAnzeigen)

        temp = []
        for el in Wolke.DB.übernatürlicheFertigkeiten:
            if not Wolke.Char.voraussetzungenPrüfen(Wolke.DB.übernatürlicheFertigkeiten[el].voraussetzungen):
                continue

            # check if at least one talent is available
            for tal in Wolke.DB.talente:
                if el in Wolke.DB.talente[tal].fertigkeiten and Wolke.Char.voraussetzungenPrüfen(Wolke.DB.talente[tal].voraussetzungen):
                    temp.append(el)
                    break

        nonOptimalFerts = self.getNonOptimalFerts(temp)
        def getPrintclass(fert, nonOptimalFerts):
             return Wolke.DB.übernatürlicheFertigkeiten[fert].printclass + (99999 if fert in nonOptimalFerts else 0)

        # sort by printclass, then by name
        temp.sort(key = lambda x: (getPrintclass(x, nonOptimalFerts), x))

        if Hilfsmethoden.ArrayEqual(temp, self.availableFerts):
            for i in range(self.ui.tableWidget.rowCount()):
                fert = Wolke.Char.übernatürlicheFertigkeiten[self.availableFerts[i]]
                self.pdfRef[fert.name].setChecked(fert.addToPDF)
                self.labelRef[fert.name + "KO"].setText(self.getSteigerungskosten(fert))
                self.labelRef[fert.name + "PW"].setText(str(fert.probenwertTalent))
                self.labelRef[fert.name].setText(str(len(fert.gekaufteTalente)))
        else:
            self.availableFerts = temp

            rowIndicesWithLinePaint = []
            count = 0
            if len(self.availableFerts) > 0:
                lastPrintclass = getPrintclass(self.availableFerts[0], nonOptimalFerts)
                for el in self.availableFerts:
                    if getPrintclass(el, nonOptimalFerts) != lastPrintclass:
                        rowIndicesWithLinePaint.append(count-1)
                        lastPrintclass = getPrintclass(el, nonOptimalFerts)
                    count += 1

            self.ui.tableWidget.clear()
            self.rowRef = {}
            self.spinRef = {}
            self.labelRef = {}
            self.layoutRef = {}
            self.buttonRef = {}
            self.widgetRef = {}
            self.pdfRef = {}
            self.ui.tableWidget.setItemDelegate(FertigkeitItemDelegate(rowIndicesWithLinePaint))

            self.ui.tableWidget.setRowCount(len(self.availableFerts))
            self.ui.tableWidget.setColumnCount(6)
            header = self.ui.tableWidget.horizontalHeader()
            header.setMinimumSectionSize(0)
            header.setSectionResizeMode(0, QHeaderView.Fixed)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.Fixed)
            header.setSectionResizeMode(3, QHeaderView.Fixed)
            header.setSectionResizeMode(4, QHeaderView.Fixed)
            header.setSectionResizeMode(5, QHeaderView.Fixed)
            self.ui.tableWidget.setColumnWidth(0, 40)
            self.ui.tableWidget.setColumnWidth(2, 60)
            self.ui.tableWidget.setColumnWidth(3, 80)
            self.ui.tableWidget.setColumnWidth(4, 65)
            self.ui.tableWidget.setColumnWidth(5, 90)

            vheader = self.ui.tableWidget.verticalHeader()
            vheader.setSectionResizeMode(QHeaderView.Fixed)
            vheader.setDefaultSectionSize(30);
            vheader.setMaximumSectionSize(30);

            item = QtWidgets.QTableWidgetItem()
            item.setText("PDF")
            item.setToolTip("Fertigkeit in Charakterblatt übernehmen?")
            self.ui.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("Name")
            item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("FW")
            item.setToolTip("Fertigkeitswert")
            self.ui.tableWidget.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("Kosten")
            self.ui.tableWidget.setHorizontalHeaderItem(3, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("PW")
            item.setToolTip("Probenwert")
            self.ui.tableWidget.setHorizontalHeaderItem(4, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("Talente")
            self.ui.tableWidget.setHorizontalHeaderItem(5, item)
    
            count = 0
            
            font = QtGui.QFont(Wolke.Settings["Font"], Wolke.Settings["FontSize"])

            for el in self.availableFerts:
                fert = Wolke.Char.übernatürlicheFertigkeiten[el]
                fert.aktualisieren(Wolke.Char.attribute)

                self.pdfRef[el] = QtWidgets.QCheckBox()
                self.pdfRef[el].setStyleSheet("margin-left:10; margin-right:10;");
                self.pdfRef[el].setChecked(fert.addToPDF)
                self.pdfRef[el].stateChanged.connect(lambda state, name=el: self.addToPDFClicked(name, state))
                self.ui.tableWidget.setCellWidget(count,0,self.pdfRef[el])

                if el in nonOptimalFerts:
                    self.labelRef[el + "Name"] =  QtWidgets.QLabel("<span style='" + Wolke.FontAwesomeCSS + "'>\uf071</span>&nbsp;&nbsp;" + el)
                    self.labelRef[el + "Name"].setToolTip("""Diese Fertigkeit bietet dir nur wenige Talente von denen (meistens) alle über andere Fertigkeiten gewirkt werden können.
Du kannst die Fertigkeit dennoch steigern, aber es wird nicht empfohlen.
Das Warnsymbol verschwindet, sobald du ein Talent erwirbst, das nur mit dieser Fertigkeit gewirkt werden kann.""")
                else:
                    self.labelRef[el + "Name"] =  QtWidgets.QLabel(el)
                self.labelRef[el + "Name"].setContentsMargins(3, 0, 0, 0)
                self.ui.tableWidget.setCellWidget(count, 1, self.labelRef[el + "Name"])
                # Add Spinner for FW
                self.spinRef[el] = QtWidgets.QSpinBox()
                self.spinRef[el].setFocusPolicy(QtCore.Qt.StrongFocus)
                self.spinRef[el].installEventFilter(self.mwp)
                self.spinRef[el].setMinimum(0)
                self.spinRef[el].setMaximum(fert.maxWert)
                self.spinRef[el].setValue(fert.wert)
                self.spinRef[el].setAlignment(QtCore.Qt.AlignCenter)
                self.spinRef[el].setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                self.spinRef[el].valueChanged.connect(lambda qtNeedsThis=False, name=el: self.spinnerClicked(name))
                self.ui.tableWidget.setCellWidget(count,2,self.spinRef[el])
                
                # Add Kosten
                self.labelRef[el + "KO"] = QtWidgets.QLabel()
                self.labelRef[el + "KO"].setStyleSheet("margin-left:10; margin-right:10;");
                self.labelRef[el + "KO"].setText(self.getSteigerungskosten(fert))
                self.labelRef[el + "KO"].setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.ui.tableWidget.setCellWidget(count,3,self.labelRef[el + "KO"])

                # Add PW
                self.labelRef[el + "PW"] = QtWidgets.QLabel()
                self.labelRef[el + "PW"].setText(str(fert.probenwertTalent))
                self.labelRef[el + "PW"].setAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setCellWidget(count,4,self.labelRef[el + "PW"])

                # Add Talents Count and Add Button
                self.layoutRef[el] = QtWidgets.QHBoxLayout()
                self.layoutRef[el].setContentsMargins(10, 0, 10, 0)
                self.labelRef[el] = QtWidgets.QLabel()
                self.labelRef[el].setText(str(len(fert.gekaufteTalente)))
                self.labelRef[el].setAlignment(QtCore.Qt.AlignCenter)
                self.layoutRef[el].addWidget(self.labelRef[el])
                self.buttonRef[el] = QtWidgets.QPushButton()
                self.buttonRef[el].setProperty("class", "icon")
                self.buttonRef[el].setText('\u002b')
                self.buttonRef[el].setMaximumSize(QtCore.QSize(20, 20))
                self.buttonRef[el].setMinimumSize(QtCore.QSize(20, 20))
                self.buttonRef[el].clicked.connect(lambda qtNeedsThis=False, name=el: self.addClicked(name))
                self.layoutRef[el].addWidget(self.buttonRef[el])
                self.widgetRef[el] = QtWidgets.QWidget()
                self.widgetRef[el].setLayout(self.layoutRef[el])
                self.ui.tableWidget.setCellWidget(count,5,self.widgetRef[el])

                self.rowRef.update({fert.name: count})
                count += 1
        self.updateInfo()
        self.updateTalents()    
        self.currentlyLoading = False
        
    def tableClicked(self):
        if not self.currentlyLoading:
            tmp = self.availableFerts[self.ui.tableWidget.currentRow()]
            if tmp in Wolke.Char.übernatürlicheFertigkeiten:    
                self.currentFertName = tmp
                self.updateInfo()
        
    def getSteigerungskosten(self, fert):
        ep = (fert.wert+1) * fert.steigerungsfaktor
        return "&nbsp;&nbsp;<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;" + str(ep) + " EP"

    def fwChanged(self, flag = False):
        if self.currentlyLoading:
            return
        if self.currentFertName == "":
            return
        if flag:
            val = self.spinRef[self.currentFertName].value()
        else:
            val = self.ui.spinFW.value()
        fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
        fert.wert = val
        fert.aktualisieren(Wolke.Char.attribute)
        self.ui.spinPW.setValue(fert.probenwertTalent)
        if flag:
            self.ui.spinFW.setValue(val)
        else:
            self.spinRef[fert.name].setValue(val)

        self.labelRef[fert.name + "KO"].setText(self.getSteigerungskosten(fert))
        self.labelRef[fert.name + "PW"].setText(str(fert.probenwertTalent))

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
        if self.currentFertName == "":
            return
        if self.currentFertName not in Wolke.Char.übernatürlicheFertigkeiten:
            self.currentFertName = ""
            self.ui.labelFertigkeit.setText("Fertigkeit")
            self.ui.labelAttribute.setText("Attribute")
            self.ui.spinSF.setValue(0)
            self.ui.spinBasis.setValue(0)
            self.ui.spinFW.setMaximum(0)
            self.ui.spinFW.setValue(0)
            self.ui.spinPW.setValue(0)
            self.ui.plainText.setPlainText("")
            self.ui.labelKategorie.setText("")
            self.model.clear()
            return
        self.currentlyLoading = True
        fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
        fert.aktualisieren(Wolke.Char.attribute)
        self.ui.labelFertigkeit.setText(self.currentFertName)
        self.ui.labelAttribute.setText(fert.attribute[0] + "/" 
                                            + fert.attribute[1] + "/" 
                                            + fert.attribute[2])
        self.ui.spinSF.setValue(fert.steigerungsfaktor)
        self.ui.spinBasis.setValue(fert.basiswert)
        self.ui.spinFW.setMaximum(fert.maxWert)
        self.spinRef[self.currentFertName].setMaximum(fert.maxWert)
        self.ui.spinFW.setValue(fert.wert)
        self.ui.spinPW.setValue(fert.probenwertTalent)
        self.ui.plainText.setPlainText(fert.text)
        fertigkeitTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen übernatürlich"].toTextList()
        self.ui.labelKategorie.setText(fertigkeitTypen[min(fert.printclass, len(fertigkeitTypen)-1)])
        self.updateTalents()
        self.currentlyLoading = False
        
    def updateTalents(self):
        if self.currentFertName == "":
            return
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
        self.ui.listTalente.setMaximumHeight(max(len(fert.gekaufteTalente), 1) * self.ui.listTalente.sizeHintForRow(0) +\
            self.ui.listTalente.contentsMargins().top() +\
            self.ui.listTalente.contentsMargins().bottom() +\
            self.ui.listTalente.spacing())
        
    def editTalents(self):
        if self.currentFertName == "":
            return
        pickerClass = EventBus.applyFilter("class_talentpicker_wrapper", CharakterTalentPickerWrapper.TalentPicker)
        tal = pickerClass(self.currentFertName, True)
        self.updateAddToPDF()
        if tal.gekaufteTalente is not None:
            self.modified.emit()
            self.load()

    def updateAddToPDF(self):
        if self.currentFertName == "":
            return
        fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
        add = len(fert.gekaufteTalente) > 0 and fert.wert > 0
        fert.addToPDF = add
        self.pdfRef[self.currentFertName].setChecked(add)
            