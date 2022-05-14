# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterProfaneFertigkeiten
import CharakterTalentPickerWrapper
import MousewheelProtector
from PyQt5 import QtWidgets, QtCore, QtGui
import logging
from PyQt5.QtWidgets import QHeaderView
from Fertigkeiten import KampffertigkeitTyp
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus

# This item delegate is used to draw a seperator line between different fertigkeit categories ('printclasses')
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
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing FertigkeitenWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterProfaneFertigkeiten.Ui_Form()
        self.ui.setupUi(self.form)

        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, 1)
        header.setSectionResizeMode(1, 3)
        header.setSectionResizeMode(2, 3)
        
        self.model = QtGui.QStandardItemModel(self.ui.listTalente)
        self.ui.listTalente.setModel(self.model)

        self.mwp = MousewheelProtector.MousewheelProtector()

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        #Signals
        self.ui.spinFW.valueChanged.connect(lambda state : self.fwChanged(False))
        self.ui.tableWidget.currentItemChanged.connect(self.tableClicked)
        self.ui.tableWidget.currentCellChanged.connect(self.tableClicked)
        self.ui.tableWidget.cellClicked.connect(self.tableClicked) 
        self.ui.buttonAdd.setStyle(None) # dont know why but the below settings wont do anything without it
        self.ui.buttonAdd.setFont(QtGui.QFont("Font Awesome 6 Free Solid", 9, QtGui.QFont.Black))
        self.ui.buttonAdd.setText('\u002b')
        self.ui.buttonAdd.setMaximumSize(QtCore.QSize(20, 20))
        self.ui.buttonAdd.setMinimumSize(QtCore.QSize(20, 20))
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
        try:
            self.currentFertName = Wolke.Char.fertigkeiten.__iter__().__next__()
        except StopIteration:
            self.currentFertName = ''
        self.currentlyLoading = False
            
    def update(self):
        #Already implemented for the individual events
        pass
        
    def load(self):
        self.currentlyLoading = True
        temp = [el for el in Wolke.DB.fertigkeiten 
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.fertigkeiten[el].voraussetzungen)]
        # sort by printclass, then by name
        temp.sort(key = lambda x: (Wolke.DB.fertigkeiten[x].printclass, x)) 

        if Hilfsmethoden.ArrayEqual(temp, self.availableFerts):
            for i in range(self.ui.tableWidget.rowCount()):
                fert = Wolke.Char.fertigkeiten[self.ui.tableWidget.item(i,0).text()]
                self.labelRef[fert.name + "KO"].setText(self.getSteigerungskosten(fert))
                self.labelRef[fert.name + "PW"].setText(str(fert.probenwert))
                self.labelRef[fert.name + "PWT"].setText(str(fert.probenwertTalent))
                self.labelRef[fert.name].setText(str(len(fert.gekaufteTalente)))
        else:
            self.availableFerts = temp
            rowIndicesWithLinePaint = []
            count = 0
            if len(self.availableFerts) > 0:
                lastPrintclass = Wolke.DB.fertigkeiten[self.availableFerts[0]].printclass
                for el in self.availableFerts:
                    if Wolke.DB.fertigkeiten[el].printclass != lastPrintclass:
                        rowIndicesWithLinePaint.append(count-1)
                        lastPrintclass = Wolke.DB.fertigkeiten[el].printclass
                    count += 1

            self.ui.tableWidget.clear()
            self.rowRef = {}
            self.spinRef = {}
            self.labelRef = {}
            self.layoutRef = {}
            self.buttonRef = {}
            self.widgetRef = {}
            self.ui.tableWidget.setItemDelegate(FertigkeitItemDelegate(rowIndicesWithLinePaint))
            
            self.ui.tableWidget.setRowCount(len(self.availableFerts))
            self.ui.tableWidget.setColumnCount(6)
            self.ui.tableWidget.verticalHeader().setVisible(False)

            header = self.ui.tableWidget.horizontalHeader()
            header.setMinimumSectionSize(0)
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Fixed)
            self.ui.tableWidget.setColumnWidth(1, 60)
            header.setSectionResizeMode(2, QHeaderView.Fixed)
            self.ui.tableWidget.setColumnWidth(2, 80)
            header.setSectionResizeMode(3, QHeaderView.Fixed)
            self.ui.tableWidget.setColumnWidth(3, 65)
            header.setSectionResizeMode(4, QHeaderView.Fixed)
            self.ui.tableWidget.setColumnWidth(4, 65)
            header.setSectionResizeMode(4, QHeaderView.Fixed)
            self.ui.tableWidget.setColumnWidth(5, 90)

            vheader = self.ui.tableWidget.verticalHeader()
            vheader.setSectionResizeMode(QHeaderView.Fixed)
            vheader.setDefaultSectionSize(30);
            vheader.setMaximumSectionSize(30);

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

            for el in self.availableFerts:
                fert = Wolke.Char.fertigkeiten[el]
                fert.aktualisieren(Wolke.Char.attribute)

                if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf:
                    self.nahkampfFerts.append(fert)

                tableWidget = QtWidgets.QTableWidgetItem(el)
                self.ui.tableWidget.setItem(count, 0, tableWidget)

                # Add Spinner for FW
                self.spinRef[el] = QtWidgets.QSpinBox()
                self.spinRef[el].setFocusPolicy(QtCore.Qt.StrongFocus)
                self.spinRef[el].installEventFilter(self.mwp)
                self.spinRef[el].setMinimum(0)
                self.spinRef[el].setMaximum(fert.maxWert)
                self.spinRef[el].setValue(fert.wert)
                self.spinRef[el].setAlignment(QtCore.Qt.AlignCenter)
                self.spinRef[el].setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                self.spinRef[el].valueChanged.connect(lambda state, name=el: self.spinnerClicked(name))
                self.ui.tableWidget.setCellWidget(count,1,self.spinRef[el])

                # Add Kosten
                self.labelRef[el + "KO"] = QtWidgets.QLabel()
                self.labelRef[el + "KO"].setStyleSheet("margin-left:10; margin-right:10;");
                self.labelRef[el + "KO"].setText(self.getSteigerungskosten(fert))
                self.labelRef[el + "KO"].setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.ui.tableWidget.setCellWidget(count,2,self.labelRef[el + "KO"])

                # Add PW
                self.labelRef[el + "PW"] = QtWidgets.QLabel()
                self.labelRef[el + "PW"].setText(str(fert.probenwert))
                self.labelRef[el + "PW"].setAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setCellWidget(count,3,self.labelRef[el + "PW"])

                # Add PW (T)
                self.labelRef[el + "PWT"] = QtWidgets.QLabel()
                self.labelRef[el + "PWT"].setText(str(fert.probenwertTalent))
                self.labelRef[el + "PWT"].setAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setCellWidget(count,4,self.labelRef[el + "PWT"])

                # Add Talents Count and Add Button
                self.layoutRef[el] = QtWidgets.QHBoxLayout()
                self.layoutRef[el].setContentsMargins(10, 0, 10, 0)
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
                self.ui.tableWidget.setCellWidget(count,5,self.widgetRef[el])

                self.rowRef.update({fert.name: count})
                count += 1
        self.updateInfo()
        self.updateTalents()    
        self.currentlyLoading = False
        
    def tableClicked(self):
        if not self.currentlyLoading:
            tmp = self.availableFerts[self.ui.tableWidget.currentRow()]
            if tmp in Wolke.Char.fertigkeiten:    
                self.currentFertName = tmp
                self.updateInfo()
        
    def getSteigerungskosten(self, fert):
        ep = (fert.wert+1) * fert.steigerungsfaktor
        höchste = Wolke.Char.getHöchsteKampffertigkeit()
        if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf and fert.wert == höchste.wert:
            ep = (fert.wert+1) * 4
        return "<span style='font-size: 9pt; font-weight: " + Hilfsmethoden.qtWeightToCSS(QtGui.QFont.Black) + "; font-family: \"Font Awesome 6 Free Solid\";'>\uf176</span>&nbsp;&nbsp;" + str(ep) + " EP"

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
        Wolke.Char.fertigkeiten[self.currentFertName].aktualisieren(Wolke.Char.attribute)
        self.ui.spinPW.setValue(fert.probenwert)
        self.ui.spinPWT.setValue(fert.probenwertTalent)
        if fert == Wolke.Char.getHöchsteKampffertigkeit():
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
            self.labelRef[f.name + "KO"].setText(self.getSteigerungskosten(f))
        self.labelRef[self.currentFertName + "PW"].setText(str(fert.probenwert))
        self.labelRef[self.currentFertName + "PWT"].setText(str(fert.probenwertTalent))

        self.modified.emit()
        self.currentlyLoading = False
    
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
        fert.aktualisieren(Wolke.Char.attribute)
        self.ui.labelFertigkeit.setText(self.currentFertName)
        self.ui.labelAttribute.setText(fert.attribute[0] + "/" + fert.attribute[1] + "/" + fert.attribute[2])
        if fert == Wolke.Char.getHöchsteKampffertigkeit():
            self.ui.spinSF.setValue(4)
        else:
            self.ui.spinSF.setValue(fert.steigerungsfaktor)
        self.ui.spinBasis.setValue(fert.basiswert)
        self.ui.spinFW.setMaximum(fert.maxWert)
        self.spinRef[self.currentFertName].setMaximum(fert.maxWert)
        self.ui.spinFW.setValue(fert.wert)
        self.ui.spinPW.setValue(fert.probenwert)
        self.ui.spinPWT.setValue(fert.probenwertTalent)
        self.ui.plainText.setPlainText(fert.text)
        fertigkeitTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen profan"].toTextList()
        self.ui.labelKategorie.setText(fertigkeitTypen[min(fert.printclass, len(fertigkeitTypen)-1)])
        self.updateTalents()
        self.currentlyLoading = False
        
    def updateTalents(self):
        if self.currentFertName == "":
            return
        self.model.clear()
        talente = Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente
        for el in talente:
            talStr = Wolke.DB.talente[el].getFullName(Wolke.Char).replace(self.currentFertName + ": ", "")
            item = QtGui.QStandardItem(talStr)
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
            