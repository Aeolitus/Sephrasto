# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterProfaneFertigkeiten
import CharakterTalentPickerWrapper
from QtUtils.MousewheelProtector import MousewheelProtector
from PySide6 import QtWidgets, QtCore, QtGui
import logging
from PySide6.QtWidgets import QHeaderView
from Core.Fertigkeit import Fertigkeit, KampffertigkeitTyp
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
import copy
from QtUtils.AutoResizingTextBrowser import TextEditAutoResizer
from functools import partial
from Hilfsmethoden import SortedCategoryToListDict

# This item delegate is used to draw a seperator line between different fertigkeit types
class FertigkeitItemDelegate(QtWidgets.QItemDelegate):
    def __init__(self, rowIndicesWithLinePaint):
        super().__init__()
        self.rowIndicesWithLinePaint = rowIndicesWithLinePaint

    def paint (self, painter, option, index):
        super().paint(painter, option, index)
        if index.row() in self.rowIndicesWithLinePaint:
            painter.setPen(QtGui.QPen(QtGui.QColor(Wolke.HeadingColor), 2))
            painter.drawLine(option.rect.bottomLeft() + QtCore.QPoint(0, 1), option.rect.bottomRight() + QtCore.QPoint(0, 1));

class ProfaneFertigkeitenWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing FertigkeitenWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterProfaneFertigkeiten.Ui_Form()
        self.ui.setupUi(self.form)

        self.autoResizeHelper = TextEditAutoResizer(self.ui.plainText)

        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)

        self.mwp = MousewheelProtector()

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        #Signals
        self.ui.spinFW.valueChanged.connect(lambda: self.fwChanged(False))
        self.ui.tableWidget.currentItemChanged.connect(self.tableClicked)
        self.ui.tableWidget.currentCellChanged.connect(self.tableClicked)
        self.ui.tableWidget.cellClicked.connect(self.tableClicked) 
        self.ui.buttonAdd.setText('\u002b')
        self.ui.buttonAdd.clicked.connect(self.editTalents)
        
        self.nahkampfFerts = []
        self.availableFerts = []
        self.rowRef = {}
        self.spinRef = {}
        self.labelRef = {}
        self.layoutRef = {}
        self.buttonRef = {}
        self.widgetRef = {}

        #If there is an ability already, then we take it to display already
        if len(Wolke.Char.fertigkeiten) > 0:
            self.currentFertName = Wolke.Char.fertigkeiten.__iter__().__next__()
        else:
            self.currentFertName = ''
        self.currentlyLoading = False
            
    def update(self):
        #Already implemented for the individual events
        pass
        
    def load(self):
        self.currentlyLoading = True

        fertigkeitenByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Fertigkeiten: Kategorien profan"].wert)
        availableFerts = []
        for fert in Wolke.Char.fertigkeiten.values():
            fertigkeitenByKategorie.append(fert.kategorie, fert.name)
            availableFerts.append(fert.name)
        fertigkeitenByKategorie.sortValues()

        if Hilfsmethoden.ArrayEqual(availableFerts, self.availableFerts):
            for i in range(self.ui.tableWidget.rowCount()):
                item = self.ui.tableWidget.item(i,0)
                if item.text() not in Wolke.Char.fertigkeiten:
                    continue
                fert = Wolke.Char.fertigkeiten[item.text()]
                text, tooltip = ProfaneFertigkeitenWrapper.getSteigerungskosten(fert)
                self.labelRef[fert.name + "KO"].setText(text)
                self.labelRef[fert.name + "KO"].setToolTip(tooltip)
                self.labelRef[fert.name + "PW"].setText(str(fert.probenwert))
                self.labelRef[fert.name + "PWT"].setText(str(fert.probenwertTalent))
                if fert.basiswertMod != 0:
                    self.labelRef[fert.name + "PW"].setText(str(fert.probenwert + fert.basiswertMod) + "*")
                    self.labelRef[fert.name + "PWT"].setText(str(fert.probenwertTalent + fert.basiswertMod) + "*")
                self.labelRef[fert.name].setText(str(len(fert.gekaufteTalente)))
            self.updateInfo()
            self.updateTalents()    
            self.currentlyLoading = False
            return

        self.availableFerts = availableFerts
        rowIndicesWithLinePaint = []
        count = 0
        for kategorie, ferts in fertigkeitenByKategorie.items():
            if len(ferts) == 0:
                continue
            count += 1 + len(ferts)
            rowIndicesWithLinePaint.append(count-1)
        if len(rowIndicesWithLinePaint) > 0:
            rowIndicesWithLinePaint.pop()

        self.ui.tableWidget.clear()
        self.rowRef = {}
        self.spinRef = {}
        self.labelRef = {}
        self.layoutRef = {}
        self.buttonRef = {}
        self.widgetRef = {}
        self.ui.tableWidget.setItemDelegate(FertigkeitItemDelegate(rowIndicesWithLinePaint))
            
        self.ui.tableWidget.setRowCount(count)
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.verticalHeader().setVisible(False)

        header = self.ui.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(0)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(1, Hilfsmethoden.emToPixels(6))
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(2, Hilfsmethoden.emToPixels(8.9))
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(3, Hilfsmethoden.emToPixels(6))
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(4, Hilfsmethoden.emToPixels(6))
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(5, Hilfsmethoden.emToPixels(10))

        vheader = self.ui.tableWidget.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.Fixed)
        vheader.setDefaultSectionSize(Hilfsmethoden.emToPixels(3.4));
        vheader.setMaximumSectionSize(Hilfsmethoden.emToPixels(3.4));

        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ui.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("FW")
        item.setToolTip("Fertigkeitswert")
        self.ui.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("Kosten")
        self.ui.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("PW")
        item.setToolTip("Probenwert")
        self.ui.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("PW(T)")
        item.setToolTip("Probenwert mit Talent")
        self.ui.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("Talente")
        self.ui.tableWidget.setHorizontalHeaderItem(5, item)
    
        count = 0

        self.nahkampfFerts = []

        fontHeader = QtWidgets.QApplication.instance().font()
        fontHeader.setBold(True)
        fontHeader.setCapitalization(QtGui.QFont.SmallCaps)
        fontHeader.setPointSize(Wolke.FontHeadingSizeL3)

        for kategorie, ferts in fertigkeitenByKategorie.items():
            if len(ferts) == 0:
                continue
            tableWidget = QtWidgets.QTableWidgetItem(kategorie)
            tableWidget.setFont(fontHeader)
            tableWidget.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(count, 0, tableWidget)
            count += 1
            
            for el in ferts:
                fert = Wolke.Char.fertigkeiten[el]
                fert.aktualisieren()

                if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf:
                    self.nahkampfFerts.append(fert)

                tableWidget = QtWidgets.QTableWidgetItem(el)
                self.ui.tableWidget.setItem(count, 0, tableWidget)

                # Add Spinner for FW
                self.spinRef[el] = QtWidgets.QSpinBox()
                self.spinRef[el].setFocusPolicy(QtCore.Qt.StrongFocus)
                self.spinRef[el].installEventFilter(self.mwp)
                self.spinRef[el].setKeyboardTracking(False)
                self.spinRef[el].setMinimum(0)
                self.spinRef[el].setMaximum(fert.maxWert)
                self.spinRef[el].setValue(fert.wert)
                self.spinRef[el].setAlignment(QtCore.Qt.AlignCenter)
                self.spinRef[el].setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                self.spinRef[el].valueChanged.connect(partial(self.spinnerClicked, fert=el))
                self.ui.tableWidget.setCellWidget(count,1,self.spinRef[el])

                # Add Kosten
                self.labelRef[el + "KO"] = QtWidgets.QLabel()
                self.labelRef[el + "KO"].setStyleSheet("width: 100%;");
                text, tooltip = ProfaneFertigkeitenWrapper.getSteigerungskosten(fert)
                self.labelRef[el + "KO"].setText(text)
                self.labelRef[el + "KO"].setToolTip(tooltip)
                self.labelRef[el + "KO"].setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
                self.ui.tableWidget.setCellWidget(count,2,self.labelRef[el + "KO"])

                # Add PW
                self.labelRef[el + "PW"] = QtWidgets.QLabel()
                self.labelRef[el + "PW"].setText(str(fert.probenwert))
                self.labelRef[el + "PW"].setAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setCellWidget(count,3,self.labelRef[el + "PW"])
                if fert.basiswertMod != 0:
                    self.labelRef[fert.name + "PW"].setText(str(fert.probenwert + fert.basiswertMod) + "*")

                # Add PW (T)
                self.labelRef[el + "PWT"] = QtWidgets.QLabel()
                self.labelRef[el + "PWT"].setText(str(fert.probenwertTalent))
                self.labelRef[el + "PWT"].setAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setCellWidget(count,4,self.labelRef[el + "PWT"])

                if fert.basiswertMod != 0:
                    self.labelRef[fert.name + "PW"].setText(str(fert.probenwert + fert.basiswertMod) + "*")
                    self.labelRef[fert.name + "PWT"].setText(str(fert.probenwertTalent + fert.basiswertMod) + "*")

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
            row = self.ui.tableWidget.currentRow()
            item = self.ui.tableWidget.item(row, 0)
            if item is not None and item.text() in Wolke.Char.fertigkeiten:    
                self.currentFertName = item.text()
                self.updateInfo()

    def fwChanged(self, flag = False):
        if self.currentlyLoading:
            return
        if self.currentFertName == "":
            return
        self.currentlyLoading = True
        if flag:
            val = self.spinRef[self.currentFertName].value()
        else:
            val = self.ui.spinFW.value()
        fert = Wolke.Char.fertigkeiten[self.currentFertName]
        fert.wert = val
        Wolke.Char.fertigkeiten[self.currentFertName].aktualisieren()
        self.ui.spinPW.setValue(fert.probenwert + fert.basiswertMod)
        self.ui.spinPWT.setValue(fert.probenwertTalent + fert.basiswertMod)
        if fert == Fertigkeit.getHöchsteKampffertigkeit(Wolke.Char.fertigkeiten):
            self.ui.spinSF.setValue(4)
        else:
            self.ui.spinSF.setValue(fert.steigerungsfaktor)

        if flag:
            self.ui.spinFW.setValue(val)
        else:
            self.spinRef[self.currentFertName].setValue(val)

        updateKosten = [fert]
        if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf:
            updateKosten = self.nahkampfFerts

        for f in updateKosten:
            text, tooltip = ProfaneFertigkeitenWrapper.getSteigerungskosten(f)
            self.labelRef[f.name + "KO"].setText(text)
            self.labelRef[f.name + "KO"].setToolTip(tooltip)
        self.labelRef[fert.name + "PW"].setText(str(fert.probenwert))
        self.labelRef[fert.name + "PWT"].setText(str(fert.probenwertTalent))
        if fert.basiswertMod != 0:
            self.labelRef[fert.name + "PW"].setText(str(fert.probenwert + fert.basiswertMod) + "*")
            self.labelRef[fert.name + "PWT"].setText(str(fert.probenwertTalent + fert.basiswertMod) + "*")

        self.modified.emit()
        self.currentlyLoading = False
    
    def spinnerClicked(self, val, fert):
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
        if self.currentFertName not in Wolke.Char.fertigkeiten:
            self.currentFertName = ""
            self.ui.labelFertigkeit.setText("Fertigkeit")
            self.ui.labelAttribute.setText("Attribute")
            self.ui.spinSF.setValue(0)
            self.ui.spinBasis.setValue(0)
            self.ui.spinFW.setMaximum(0)
            self.ui.spinFW.setValue(0)
            self.ui.spinPW.setValue(0)
            self.ui.spinPWT.setValue(0)
            self.ui.plainText.setPlainText("")
            self.ui.labelKategorie.setText("")
            self.model.clear()
            return
        self.currentlyLoading = True
        fert = Wolke.Char.fertigkeiten[self.currentFertName]
        fert.aktualisieren()
        self.ui.labelFertigkeit.setText(self.currentFertName)
        self.ui.labelAttribute.setText("/".join(fert.attribute))
        if fert == Fertigkeit.getHöchsteKampffertigkeit(Wolke.Char.fertigkeiten):
            self.ui.spinSF.setValue(4)
        else:
            self.ui.spinSF.setValue(fert.steigerungsfaktor)
        self.ui.spinBasis.setValue(fert.basiswert + fert.basiswertMod)
        self.ui.spinFW.setMaximum(fert.maxWert)
        self.spinRef[self.currentFertName].setMaximum(fert.maxWert)
        self.ui.spinFW.setValue(fert.wert)
        self.ui.spinPW.setValue(fert.probenwert + fert.basiswertMod)
        self.ui.spinPWT.setValue(fert.probenwertTalent + fert.basiswertMod)
        self.ui.plainText.setText(Hilfsmethoden.fixHtml(fert.text))
        self.ui.labelKategorie.setText(fert.kategorieName(Wolke.DB))
        self.updateTalents()
        self.currentlyLoading = False
        
    def updateTalents(self):
        if self.currentFertName == "":
            return
        self.model.clear()
        talente = Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente
        for el in talente:
            item = QtGui.QStandardItem(Wolke.Char.talente[el].anzeigenameExt)
            item.setEditable(False)
            item.setSelectable(False)
            self.model.appendRow(item)
        self.ui.listTalente.setMaximumHeight(max(len(talente), 1) * self.ui.listTalente.sizeHintForRow(0) +\
            self.ui.listTalente.contentsMargins().top() +\
            self.ui.listTalente.contentsMargins().bottom() +\
            self.ui.listTalente.spacing())
        self.ui.scrollAreaWidgetContents.layout().update()

    def editTalents(self):
        if self.currentFertName == "":
            return
        pickerClass = EventBus.applyFilter("class_talentpicker_wrapper", CharakterTalentPickerWrapper.TalentPicker)
        tal = pickerClass(self.currentFertName, False)
        if tal.gekaufteTalente is not None:
            self.modified.emit()
            self.updateTalents()
            self.labelRef[self.currentFertName].setText(str(len(tal.gekaufteTalente)))        

    @staticmethod
    def getSteigerungskosten(fert):
        if fert.wert == fert.maxWert:
            maxWert = max(fert.attributswerte)
            attribute = [attr for attr in fert.attribute if Wolke.Char.attribute[attr].wert == maxWert]
            kosten = Wolke.Char.attribute[attribute[0]].steigerungskosten()
            attribute = list(dict.fromkeys(attribute))
            attribute = ", ".join(attribute)
            attribute = attribute[::-1].replace(" ,"," redo ", 1)[::-1] #replace last ", " by " oder "
            return "max", f"Steigere das höchste Attribut von {fert.name} ({attribute} für {kosten} EP), um das Maximum zu erhöhen."
        else:
            kosten, attribute = ProfaneFertigkeitenWrapper.basiswertSteigern(fert, Wolke.Char.attribute)
            if kosten != -1 and kosten <= fert.steigerungskosten():
                steigern = []
                for attr in attribute:
                    if Wolke.Char.attribute[attr].wert < attribute[attr].wert:
                        steigern.append(attr + " +" + str(attribute[attr].wert - Wolke.Char.attribute[attr].wert))
                steigern = ", ".join(steigern)
                steigern = steigern[::-1].replace(" ,"," dnu ", 1)[::-1] #replace last ", " by " und "
                warnIcon = "<span style='" + Wolke.FontAwesomeCSS + "'>\uf071</span>&nbsp;&nbsp;"
                return warnIcon + str(fert.steigerungskosten()) + " EP", "Es lohnt sich mehr, den Basiswert durch Attribute zu steigern (zum Beispiel " + steigern + " für " + str(kosten) + " EP)."
            else:     
                arrowUpIcon = "<span style='" + Wolke.FontAwesomeCSS + "'>\uf176</span>&nbsp;&nbsp;"
                return arrowUpIcon + str(fert.steigerungskosten()) + " EP" , ""

    @staticmethod
    def basiswertSteigern(fert, attr):
        def cost(attribut):
            return attribut.kosten() / fert.attribute.count(attribut.name)

        attribute = copy.deepcopy(attr)
        bwKosten = 0
        iterationCount = 0 #just a safety measure in case someone changes the BW script setting
        diff = 0
        while diff == 0:
            niedrigstesAttr = fert.attribute[0]
            for attr in fert.attribute:
                cost1 = cost(attribute[niedrigstesAttr])
                cost2 = cost(attribute[attr])
                if (cost1 == cost2 and attribute[attr].wert > attribute[niedrigstesAttr].wert) or cost1 > cost2:
                    niedrigstesAttr = attr
            bwKosten += attribute[niedrigstesAttr].steigerungskosten()
            attribute[niedrigstesAttr].wert += 1
            attribute[niedrigstesAttr].aktualisieren()
            diff = fert.diffBasiswert(attribute)
            iterationCount += 1
            if iterationCount == 20:
                return -1, attribute

        return bwKosten, attribute