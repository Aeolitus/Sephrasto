# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:21:03 2017

@author: Aeolitus
"""
from Wolke import Wolke
import UI.CharakterVorteile
import CharakterMinderpaktWrapper
from Charakter import VariableKosten
from PyQt5 import QtWidgets, QtCore, QtGui
import logging
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden

class CharakterVorteileWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing VorteileWrapper...")
        self.formVor = QtWidgets.QWidget()
        self.uiVor = UI.CharakterVorteile.Ui_Form()
        self.uiVor.setupUi(self.formVor)
        
        self.vorteilTypen = Wolke.DB.einstellungen["Vorteile: Typen"].toTextList()
        font = QtWidgets.QApplication.instance().font()
        self.uiVor.treeWidget.itemSelectionChanged.connect(self.vortClicked)
        self.uiVor.treeWidget.itemChanged.connect(self.itemChangeHandler)
        self.uiVor.treeWidget.header().setSectionResizeMode(0,1)
        
        self.uiVor.splitter.adjustSize()
        width = self.uiVor.splitter.size().width()
        self.uiVor.splitter.setSizes([int(width*0.6), int(width*0.4)])

        if len(Wolke.Char.vorteile) > 0:
            self.currentVort = Wolke.Char.vorteile[0]
        else:
            self.currentVort = ""
            
        self.itemWidgets = {}
        
        self.uiVor.checkShowAll.stateChanged.connect(self.onShowAllClicked)
        self.showUnavailable = False
        self.initVorteile()

    def onShowAllClicked(self):
        self.showUnavailable = self.uiVor.checkShowAll.isChecked()
        self.load()

    def initVorteile(self):
        self.uiVor.treeWidget.blockSignals(True)
        vortList = []
        for vortTyp in self.vorteilTypen:
            vortList.append([])

        for el in Wolke.DB.vorteile:
            idx = min(Wolke.DB.vorteile[el].typ, len(vortList) - 1)
            vortList[idx].append(el)
        
        for vorteile in vortList:
            vorteile.sort()

        rowHeight = 30

        for i in range(len(vortList)):
            parent = QtWidgets.QTreeWidgetItem(self.uiVor.treeWidget)
            parent.setText(0, self.vorteilTypen[i])
            parent.setText(1,"")
            parent.setExpanded(True)
            parent.setSizeHint(0, QtCore.QSize(0, rowHeight))
            font = parent.font(0)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            font.setPointSize(Wolke.FontHeadingSizeL3)
            parent.setFont(0, font)
            for el in vortList[i]:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, Wolke.DB.vorteile[el].name)
                child.setSizeHint(0, QtCore.QSize(0, rowHeight))
                if el in Wolke.Char.vorteile:    
                    child.setCheckState(0, QtCore.Qt.Checked)
                else:
                    child.setCheckState(0, QtCore.Qt.Unchecked)
                if Wolke.DB.vorteile[el].variableKosten:
                    spin = QtWidgets.QSpinBox()
                    spin.setFixedHeight(rowHeight)
                    spin.setMinimum(-9999)
                    spin.setSuffix(" EP")
                    spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
                    spin.setMaximum(9999)
                    if el == Wolke.Char.minderpakt:
                        spin.setValue(20)
                        spin.setReadOnly(True)
                    else:
                        if el in Wolke.Char.vorteileVariable:
                            spin.setValue(Wolke.Char.vorteileVariable[el].kosten)
                        else:
                            spin.setValue(Wolke.DB.vorteile[el].kosten)
                    spin.setSingleStep(20)
                    self.itemWidgets[el] = spin
                    spin.valueChanged.connect(lambda state, name=el: self.spinnerChanged(name,state))
                    self.uiVor.treeWidget.setItemWidget(child,1,spin)
                else:
                    child.setText(1, "20 EP" if el == Wolke.Char.minderpakt else str(Wolke.DB.vorteile[el].kosten) + " EP")

                if Wolke.DB.vorteile[el].kommentarErlauben:
                    if child.checkState(0) == QtCore.Qt.Checked:
                        self.handleAddKommentarWidget(el, child)
                else:
                    child.setText(1, "20 EP" if el == Wolke.Char.minderpakt else str(Wolke.DB.vorteile[el].kosten) + " EP")

        self.updateInfo()
        self.uiVor.treeWidget.blockSignals(False)
        
    def load(self):
        self.uiVor.treeWidget.blockSignals(True)
        vortList = []
        for vortTyp in self.vorteilTypen:
            vortList.append([])

        for el in Wolke.DB.vorteile:
            if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.vorteile[el].voraussetzungen) or el == Wolke.Char.minderpakt:
                idx = min(Wolke.DB.vorteile[el].typ, len(vortList) -1)
                vortList[idx].append(el)

        for i in range(len(vortList)):
            itm = self.uiVor.treeWidget.topLevelItem(i)
            if type(itm) != QtWidgets.QTreeWidgetItem:
                continue
            if itm == 0: 
                continue

            if self.showUnavailable:
                itm.setHidden(False)
            else:
                itm.setHidden(len(vortList[i]) == 0)

            for j in range(itm.childCount()):
                chi = itm.child(j)
                if type(chi) != QtWidgets.QTreeWidgetItem:
                    continue
                txt = chi.text(0)
                if txt in Wolke.Char.vorteile or txt == Wolke.Char.minderpakt:    
                    chi.setCheckState(0, QtCore.Qt.Checked)
                    if txt in Wolke.Char.vorteileVariable:
                        if Wolke.DB.vorteile[txt].variableKosten:
                            self.itemWidgets[txt].setValue(Wolke.Char.vorteileVariable[txt].kosten)
                        if Wolke.DB.vorteile[txt].kommentarErlauben:
                            self.handleAddKommentarWidget(txt, chi)
                else:
                    chi.setCheckState(0, QtCore.Qt.Unchecked) 
                if txt not in vortList[i]:
                    if self.showUnavailable:
                        chi.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                        chi.setCheckState(0,QtCore.Qt.Unchecked)
                        chi.setForeground(0, QtGui.QBrush(QtCore.Qt.red))
                        chi.setHidden(False)
                    else:
                        chi.setHidden(True)
                    Wolke.Char.removeVorteil(txt)
                else:
                    chi.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    chi.setForeground(0, QtGui.QBrush())
                    chi.setHidden(False)

                if (Wolke.DB.vorteile[txt].variableKosten or Wolke.DB.vorteile[txt].kommentarErlauben) and not txt in Wolke.Char.vorteileVariable:
                    if txt in self.itemWidgets:
                        self.setVariableKosten(txt, self.itemWidgets[txt].value(), "")
                    else:
                        self.setVariableKosten(txt, Wolke.DB.vorteile[txt].kosten, "")
        self.updateInfo()
        self.uiVor.treeWidget.blockSignals(False)
        
    def update(self):
        pass

    def setVariableKosten(self, name, kosten, kommentar):
        if not name in Wolke.Char.vorteileVariable:
            vk = VariableKosten()
            Wolke.Char.vorteileVariable[name] = vk

        if kosten != None:
            Wolke.Char.vorteileVariable[name].kosten = kosten
        if kommentar != None:
            Wolke.Char.vorteileVariable[name].kommentar = kommentar

    def spinnerChanged(self,name,state):
        self.setVariableKosten(name, state, None)
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

    def kommentarChanged(self, name, text):
        self.setVariableKosten(name, None, text)
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

    def handleAddKommentarWidget(self, name, parent):
        if not Wolke.DB.vorteile[name].kommentarErlauben or parent.childCount() > 0:
            return
        kommentar = ""
        if name in Wolke.Char.vorteileVariable:
            kommentar = Wolke.Char.vorteileVariable[name].kommentar

        w = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Kommentar")
        text = QtWidgets.QLineEdit(kommentar)
        layout.addWidget(label)
        layout.addWidget(text)
        w.setLayout(layout)
        text.textChanged.connect(lambda text, name=name: self.kommentarChanged(name, text))

        child = QtWidgets.QTreeWidgetItem(parent)
        self.uiVor.treeWidget.setItemWidget(child,0,w)
        parent.setExpanded(True)

    def handleRemoveKommentarWidget(self, parent):
        parent.takeChild(0) #doesnt do anything if it doesnt exist

    def handleAddMinderpakt(self, name, item):
        if name != "Minderpakt":
            return None
        minderp = CharakterMinderpaktWrapper.CharakterMinderpaktWrapper()
        if minderp.minderpakt is None:
            Wolke.Char.removeVorteil(name)
            return None
        if minderp.minderpakt in Wolke.DB.vorteile and minderp.minderpakt not in Wolke.Char.vorteile:
            Wolke.Char.minderpakt = minderp.minderpakt
            Wolke.Char.addVorteil(minderp.minderpakt)
            minderpaktWidget = self.uiVor.treeWidget.findItems(Wolke.Char.minderpakt, QtCore.Qt.MatchRecursive)[0]

            if Wolke.Char.minderpakt in self.itemWidgets:
                self.itemWidgets[Wolke.Char.minderpakt].setReadOnly(True)
                self.itemWidgets[Wolke.Char.minderpakt].setValue(20)
            else:
                minderpaktWidget.setText(1, "20 EP")
            return minderpaktWidget
        return None

    def restoreMinderpaktWidgets(self, name, item):
            if name in self.itemWidgets:
                self.itemWidgets[name].setReadOnly(False)
                self.itemWidgets[name].setValue(Wolke.DB.vorteile[name].kosten)
            else:
                item.setText(1, str(Wolke.DB.vorteile[name].kosten) + " EP")

    def handleRemoveMinderpakt(self, name, item):
        if name == "Minderpakt":
            Wolke.Char.removeVorteil(Wolke.Char.minderpakt)
            minderpaktWidget = self.uiVor.treeWidget.findItems(Wolke.Char.minderpakt, QtCore.Qt.MatchRecursive)[0]
            self.restoreMinderpaktWidgets(Wolke.Char.minderpakt, minderpaktWidget)
            Wolke.Char.minderpakt = None
            return minderpaktWidget

        if Wolke.Char.minderpakt is not None and name == Wolke.Char.minderpakt:
            Wolke.Char.removeVorteil("Minderpakt")
            self.restoreMinderpaktWidgets(Wolke.Char.minderpakt, item)
            Wolke.Char.minderpakt = None
        return None
    
    def itemChangeHandler(self, item, column):
        # Block Signals to make sure we dont repeat infinitely
        self.uiVor.treeWidget.blockSignals(True)
        name = item.text(0)
        self.currentVort = name
        self.updateInfo()
        cs = item.checkState(0)
        manualUpdate = None

        if cs == QtCore.Qt.Checked and name not in Wolke.Char.vorteile and name != "":
            Wolke.Char.addVorteil(name)
            self.handleAddKommentarWidget(name, item)
            manualUpdate = self.handleAddMinderpakt(name, item)
        elif cs != QtCore.Qt.Checked and name in Wolke.Char.vorteile:
            Wolke.Char.removeVorteil(name)
            self.handleRemoveKommentarWidget(item)
            manualUpdate = self.handleRemoveMinderpakt(name, item)

        self.modified.emit()
        self.load()
        self.uiVor.treeWidget.blockSignals(False)

        if manualUpdate:
            self.itemChangeHandler(manualUpdate, 0)
    
    def vortClicked(self):
        for el in self.uiVor.treeWidget.selectedItems():
            if el.text(0) in self.vorteilTypen:
                continue
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()
        
    def updateInfo(self):
        if self.currentVort != "":
            vorteil = Wolke.DB.vorteile[self.currentVort]
            self.uiVor.labelVorteil.setText(vorteil.name)
            self.uiVor.labelTyp.setText(self.vorteilTypen[vorteil.typ])
            self.uiVor.labelNachkauf.setText(vorteil.nachkauf)

            voraussetzungen = [v.strip() for v in Hilfsmethoden.VorArray2Str(vorteil.voraussetzungen).split(",")]
            voraussetzungen = [v for v in voraussetzungen if not v.startswith("Kein Vorteil Tradition")]
            voraussetzungen = [v + " und 2 weitere Attribute auf insgesamt 16" if "MeisterAttribut" in v else v for v in voraussetzungen]
            voraussetzungen = ", ".join(voraussetzungen)
            voraussetzungen = voraussetzungen.replace(" ODER ", " oder ")
            voraussetzungen = voraussetzungen.replace("'", "") # remove apostrophes from "Fertigkeit" and "Übernatürliche-Fertigkeit"
            voraussetzungen = voraussetzungen.replace("Fertigkeit ", "")
            voraussetzungen = voraussetzungen.replace("Übernatürliche-Fertigkeit ", "")
            voraussetzungen = voraussetzungen.replace("MeisterAttribut ", "")
            voraussetzungen = voraussetzungen.replace("Attribut ", "")
            voraussetzungen = voraussetzungen.replace("Vorteil ", "")
            voraussetzungen = voraussetzungen.replace("Kein ", "kein ")
            if not voraussetzungen:
                voraussetzungen = "keine"
            self.uiVor.labelVoraussetzungen.setText(voraussetzungen)

            self.uiVor.plainText.setPlainText(vorteil.text)
            if vorteil.variableKosten and self.currentVort in Wolke.Char.vorteileVariable:
                self.uiVor.labelKosten.setText(str(Wolke.Char.vorteileVariable[self.currentVort].kosten) + " EP")
            else:
                self.uiVor.labelKosten.setText(str(vorteil.kosten) + " EP")
            