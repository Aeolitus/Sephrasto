# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterUebernatuerlich
import CharakterTalentPickerWrapper
from QtUtils.MousewheelProtector import MousewheelProtector
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QHeaderView
import logging
from CharakterProfaneFertigkeitenWrapper import ProfaneFertigkeitenWrapper, FertigkeitItemDelegate
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
from QtUtils.AutoResizingTextBrowser import TextEditAutoResizer
from functools import partial

class UebernatuerlichWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing UebernatuerlichWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterUebernatuerlich.Ui_Form()
        self.ui.setupUi(self.form)
        
        self.autoResizeHelper = TextEditAutoResizer(self.ui.plainText)

        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)

        self.mwp = MousewheelProtector()

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        #Signals
        self.ui.spinFW.valueChanged.connect(lambda: self.fwChanged(False))
        self.ui.tableWidget.currentCellChanged.connect(self.tableClicked)   
        self.ui.tableWidget.cellClicked.connect(self.tableClicked) 
        self.ui.buttonAdd.setStyle(None) # dont know why but the below settings wont do anything without it
        self.ui.buttonAdd.setText('\u002b')
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
            if not talent.spezialTalent:
                continue
            if talent.name.endswith("(passiv)") or talent.name.endswith("(Passiv)"):
                if not " PW " in talent.text:
                    continue
            if Wolke.Char.voraussetzungenPrüfen(talent):
                availableTalents.append(talent)

        result = {}
        for el in ferts:
            totalTalentCost = 0
             # going to use the word unique for talents that the char has only one fert for
            uniqueTalentCost = 0
            uniqueTalentOwned = False
            for talent in availableTalents:
                available = False
                unique = True
                owned = False
                for fertName in talent.fertigkeiten:
                    if fertName in Wolke.Char.übernatürlicheFertigkeiten:
                        owned = owned or talent.name in Wolke.Char.talente
                    if fertName == el:
                        available = True
                    elif fertName in ferts:
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

            if totalTalentCost == 0:
                result[el] = """Unter dieser Fertigkeit stehen dir keine Talente zur Verfügung. Du benötigst einen (anderen) Traditionsvorteil.
Du kannst die Fertigkeit dennoch steigern, aber es wird nicht empfohlen."""
            elif totalTalentCost < 120 or (totalTalentCost < 180 and uniqueTalentCost < 60):
                if uniqueTalentCost == 0:
                    result[el] = """Diese Fertigkeit bietet dir nur wenige Talente, von denen alle über andere Fertigkeiten gewirkt werden können.
Du kannst die Fertigkeit dennoch steigern, aber es wird nicht empfohlen."""
                elif totalTalentCost == uniqueTalentCost:
                    result[el] = """Diese Fertigkeit bietet dir nur wenige Talente. Du kannst die Fertigkeit dennoch steigern, aber es wird nicht empfohlen.
Das Warnsymbol verschwindet, sobald du ein Talent erwirbst."""
                else:
                    result[el] = """Diese Fertigkeit bietet dir nur wenige Talente von denen die meisten über andere Fertigkeiten gewirkt werden können.
Du kannst die Fertigkeit dennoch steigern, aber es wird nicht empfohlen.
Das Warnsymbol verschwindet, sobald du ein Talent erwirbst, das nur mit dieser Fertigkeit gewirkt werden kann."""

        return result

    def load(self):
        self.currentlyLoading = True
        
        self.ui.tableWidget.setColumnHidden(0, not Wolke.Char.ueberPDFAnzeigen)

        temp = list(Wolke.Char.übernatürlicheFertigkeiten.keys())
        nonOptimalFerts = self.getNonOptimalFerts(temp)
        def getType(fert):
             return Wolke.Char.übernatürlicheFertigkeiten[fert].typ + (99999 if fert in nonOptimalFerts else 0)

        temp = []
        lastType = -1
        for fert in sorted(Wolke.Char.übernatürlicheFertigkeiten.values(), key = lambda x: (getType(x.name), x.name)):
            type = getType(fert.name)
            if type != lastType:
                lastType = type
                temp.append("Nicht empfohlen" if fert.name in nonOptimalFerts else fert.definition.typname(Wolke.DB))
            temp.append(fert.name)

        if Hilfsmethoden.ArrayEqual(temp, self.availableFerts):
            for i in range(self.ui.tableWidget.rowCount()):
                item = self.ui.tableWidget.cellWidget(i, 1)
                if item is None or item.property("name") not in Wolke.Char.übernatürlicheFertigkeiten:
                    continue
                fert = Wolke.Char.übernatürlicheFertigkeiten[item.property("name")]
                self.pdfRef[fert.name].setChecked(fert.addToPDF)
                text, tooltip = ProfaneFertigkeitenWrapper.getSteigerungskosten(fert)
                self.labelRef[fert.name + "KO"].setText(text)
                self.labelRef[fert.name + "KO"].setToolTip(tooltip)
                self.labelRef[fert.name + "PW"].setText(str(fert.probenwertTalent))
                if fert.basiswertMod != 0:
                    self.labelRef[fert.name + "PW"].setText(str(fert.probenwertTalent + fert.basiswertMod) + "*")
                self.labelRef[fert.name].setText(str(len(fert.gekaufteTalente)))
        else:
            self.availableFerts = temp

            rowIndicesWithLinePaint = []
            count = 0
            for el in self.availableFerts:
                if el not in Wolke.DB.übernatürlicheFertigkeiten:
                    rowIndicesWithLinePaint.append(count-1)
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
            self.ui.tableWidget.setColumnWidth(0, Hilfsmethoden.emToPixels(4.5))
            self.ui.tableWidget.setColumnWidth(2, Hilfsmethoden.emToPixels(6.7))
            self.ui.tableWidget.setColumnWidth(3, Hilfsmethoden.emToPixels(8.9))
            self.ui.tableWidget.setColumnWidth(4, Hilfsmethoden.emToPixels(7.3))
            self.ui.tableWidget.setColumnWidth(5, Hilfsmethoden.emToPixels(10))

            vheader = self.ui.tableWidget.verticalHeader()
            vheader.setSectionResizeMode(QHeaderView.Fixed)
            vheader.setDefaultSectionSize(Hilfsmethoden.emToPixels(3.4));
            vheader.setMaximumSectionSize(Hilfsmethoden.emToPixels(3.4));

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
            
            fontHeader = QtWidgets.QApplication.instance().font()
            fontHeader.setBold(True)
            fontHeader.setCapitalization(QtGui.QFont.SmallCaps)
            fontHeader.setPointSize(Wolke.FontHeadingSizeL3)
            lastType = -1
            for el in self.availableFerts:
                if el not in Wolke.Char.übernatürlicheFertigkeiten:
                    tableWidget = QtWidgets.QTableWidgetItem(el)
                    tableWidget.setFont(fontHeader)
                    tableWidget.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.setItem(count, 1, tableWidget)
                    count += 1
                    continue

                fert = Wolke.Char.übernatürlicheFertigkeiten[el]
                fert.aktualisieren()

                self.pdfRef[el] = QtWidgets.QCheckBox()
                self.pdfRef[el].setStyleSheet("margin-left:1.1em;");
                self.pdfRef[el].setChecked(fert.addToPDF)
                self.pdfRef[el].stateChanged.connect(partial(self.addToPDFClicked, fert=el))
                self.ui.tableWidget.setCellWidget(count,0,self.pdfRef[el])

                if el in nonOptimalFerts:
                    self.labelRef[el + "Name"] =  QtWidgets.QLabel("<span style='" + Wolke.FontAwesomeCSS + "'>\uf071</span>&nbsp;&nbsp;" + el)
                    self.labelRef[el + "Name"].setToolTip(nonOptimalFerts[el])
                else:
                    self.labelRef[el + "Name"] =  QtWidgets.QLabel(el)
                self.labelRef[el + "Name"].setContentsMargins(3, 0, 0, 0)
                self.labelRef[el + "Name"].setProperty("name", el)
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
                self.spinRef[el].valueChanged.connect(partial(self.spinnerClicked, fert=el))
                self.ui.tableWidget.setCellWidget(count,2,self.spinRef[el])
                
                # Add Kosten
                self.labelRef[el + "KO"] = QtWidgets.QLabel()
                self.labelRef[el + "KO"].setStyleSheet("margin-left:1.1em;");
                text, tooltip = ProfaneFertigkeitenWrapper.getSteigerungskosten(fert)
                self.labelRef[el + "KO"].setText(text)
                self.labelRef[el + "KO"].setToolTip(tooltip)
                self.labelRef[el + "KO"].setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.ui.tableWidget.setCellWidget(count,3,self.labelRef[el + "KO"])

                # Add PW
                self.labelRef[el + "PW"] = QtWidgets.QLabel()
                self.labelRef[el + "PW"].setText(str(fert.probenwertTalent))
                if fert.basiswertMod != 0:
                    self.labelRef[fert.name + "PW"].setText(str(fert.probenwertTalent + fert.basiswertMod) + "*")
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
                self.buttonRef[el].setProperty("class", "iconSmall")
                self.buttonRef[el].setText('\u002b')
                self.buttonRef[el].clicked.connect(partial(self.addClicked, fert=el))
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
            item = self.ui.tableWidget.cellWidget(self.ui.tableWidget.currentRow(), 1)
            if item is not None and item.property("name") in Wolke.Char.übernatürlicheFertigkeiten:  
                self.currentFertName = item.property("name")
                self.updateInfo()

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
        fert.aktualisieren()
        self.ui.spinPW.setValue(fert.probenwertTalent + fert.basiswertMod)
        if flag:
            self.ui.spinFW.setValue(val)
        else:
            self.spinRef[fert.name].setValue(val)
        
        text, tooltip = ProfaneFertigkeitenWrapper.getSteigerungskosten(fert)
        self.labelRef[fert.name + "KO"].setText(text)
        self.labelRef[fert.name + "KO"].setToolTip(tooltip)
        self.labelRef[fert.name + "PW"].setText(str(fert.probenwertTalent))
        if fert.basiswertMod != 0:
            self.labelRef[fert.name + "PW"].setText(str(fert.probenwertTalent + fert.basiswertMod) + "*")

        self.updateAddToPDF()

        self.modified.emit()
    
    def addToPDFClicked(self, state, fert):
        Wolke.Char.übernatürlicheFertigkeiten[fert].addToPDF = state
        self.modified.emit()

    def spinnerClicked(self, value, fert):
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
        fert.aktualisieren()
        self.ui.labelFertigkeit.setText(self.currentFertName)
        self.ui.labelAttribute.setText(fert.attribute[0] + "/" 
                                            + fert.attribute[1] + "/" 
                                            + fert.attribute[2])
        self.ui.spinSF.setValue(fert.steigerungsfaktor)
        self.ui.spinBasis.setValue(fert.basiswert + fert.basiswertMod)
        self.ui.spinFW.setMaximum(fert.maxWert)
        self.spinRef[self.currentFertName].setMaximum(fert.maxWert)
        self.ui.spinFW.setValue(fert.wert)
        self.ui.spinPW.setValue(fert.probenwertTalent + fert.basiswertMod)
        self.ui.plainText.setText(Hilfsmethoden.fixHtml(fert.text))
        self.ui.labelKategorie.setText(fert.typname(Wolke.DB))
        self.updateTalents()
        self.currentlyLoading = False
        
    def updateTalents(self):
        if self.currentFertName == "":
            return
        self.model.clear()
        fert = Wolke.Char.übernatürlicheFertigkeiten[self.currentFertName]
        for el in fert.gekaufteTalente:
            item = QtGui.QStandardItem(Wolke.Char.talente[el].anzeigenameExt)
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
            