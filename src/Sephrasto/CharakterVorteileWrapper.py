# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:21:03 2017

@author: Aeolitus
"""
from Wolke import Wolke
import UI.CharakterVorteile
import CharakterMinderpaktWrapper
from PySide6 import QtWidgets, QtCore, QtGui
import logging
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden

class CharakterVorteileWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing VorteileWrapper...")
        self.rowHeight = 30
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterVorteile.Ui_Form()
        self.ui.setupUi(self.form)
        
        self.vorteilTypen = Wolke.DB.einstellungen["Vorteile: Typen"].toTextList()
        font = QtWidgets.QApplication.instance().font()
        self.ui.treeWidget.itemSelectionChanged.connect(self.vortClicked)
        self.ui.treeWidget.itemChanged.connect(self.itemChangeHandler)
        self.ui.treeWidget.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        
        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        if len(Wolke.Char.vorteile) > 0:
            self.currentVort = Wolke.Char.vorteile[0]
        else:
            self.currentVort = ""
            
        self.itemWidgets = {}
        
        self.ui.checkShowAll.stateChanged.connect(self.onShowAllClicked)
        self.showUnavailable = False
        self.initVorteile()

    def onShowAllClicked(self):
        self.showUnavailable = self.ui.checkShowAll.isChecked()
        self.load()

    def initVorteile(self):
        self.ui.treeWidget.blockSignals(True)
        vortList = []
        for vortTyp in self.vorteilTypen:
            vortList.append([])

        for el in Wolke.DB.vorteile:
            idx = min(Wolke.DB.vorteile[el].typ, len(vortList) - 1)
            vortList[idx].append(el)
        
        for vorteile in vortList:
            vorteile.sort()

        for i in range(len(vortList)):
            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            parent.setText(0, self.vorteilTypen[i])
            parent.setText(1,"")
            parent.setExpanded(True)
            parent.setSizeHint(0, QtCore.QSize(0, self.rowHeight))
            font = parent.font(0)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            font.setPointSize(Wolke.FontHeadingSizeL3)
            parent.setFont(0, font)
            for el in vortList[i]:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, Wolke.DB.vorteile[el].name)
                child.setSizeHint(0, QtCore.QSize(0, self.rowHeight))
                if el in Wolke.Char.vorteile:    
                    child.setCheckState(0, QtCore.Qt.Checked)
                else:
                    child.setCheckState(0, QtCore.Qt.Unchecked)
                if Wolke.DB.vorteile[el].variableKosten:
                    spin = QtWidgets.QSpinBox()
                    spin.setFixedHeight(self.rowHeight)
                    spin.setMinimum(-9999)
                    spin.setSuffix(" EP")
                    spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
                    spin.setMaximum(9999)
                    if el == Wolke.Char.minderpakt:
                        spin.setValue(20)
                        spin.setReadOnly(True)
                    else:
                        if el in Wolke.Char.vorteileVariableKosten:
                            spin.setValue(Wolke.Char.vorteileVariableKosten[el])
                        else:
                            spin.setValue(Wolke.DB.vorteile[el].kosten)
                    spin.setSingleStep(20)
                    self.itemWidgets[el] = spin
                    spin.valueChanged.connect(lambda qtNeedsThis=False, name=el: self.spinnerChanged(name))
                    self.ui.treeWidget.setItemWidget(child,1,spin)
                else:
                    child.setText(1, "20 EP" if el == Wolke.Char.minderpakt else str(Wolke.DB.vorteile[el].kosten) + " EP")

                if Wolke.DB.vorteile[el].kommentarErlauben:
                    if child.checkState(0) == QtCore.Qt.Checked:
                        self.handleAddKommentarWidget(el, child)
                else:
                    child.setText(1, "20 EP" if el == Wolke.Char.minderpakt else str(Wolke.DB.vorteile[el].kosten) + " EP")

        self.updateInfo()
        self.ui.treeWidget.blockSignals(False)
        
    def load(self):
        self.ui.checkShowAll.setVisible(Wolke.Char.voraussetzungenPruefen)

        self.ui.treeWidget.blockSignals(True)
        vortList = []
        for vortTyp in self.vorteilTypen:
            vortList.append([])

        for el in Wolke.DB.vorteile:
            if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.vorteile[el].voraussetzungen) or el == Wolke.Char.minderpakt:
                idx = min(Wolke.DB.vorteile[el].typ, len(vortList) -1)
                vortList[idx].append(el)

        for i in range(len(vortList)):
            itm = self.ui.treeWidget.topLevelItem(i)
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
                    if txt in Wolke.Char.vorteileVariableKosten and Wolke.DB.vorteile[txt].variableKosten:
                        self.itemWidgets[txt].setValue(Wolke.Char.vorteileVariableKosten[txt])

                    if txt in Wolke.Char.vorteileKommentare and Wolke.DB.vorteile[txt].kommentarErlauben:
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

                if Wolke.DB.vorteile[txt].variableKosten and not txt in Wolke.Char.vorteileVariableKosten:
                    if txt in self.itemWidgets:
                        Wolke.Char.vorteileVariableKosten[txt] = self.itemWidgets[txt].value()
                    else:
                        Wolke.Char.vorteileVariableKosten[txt] = Wolke.DB.vorteile[txt].kosten

                if Wolke.DB.vorteile[txt].kommentarErlauben and not txt in Wolke.Char.vorteileKommentare:
                    Wolke.Char.vorteileKommentare[txt] = ""

        self.updateInfo()
        self.ui.treeWidget.blockSignals(False)
        
    def update(self):
        pass

    def spinnerChanged(self,name):
        if Wolke.DB.vorteile[name].variableKosten:
            Wolke.Char.vorteileVariableKosten[name] = self.itemWidgets[name].value()
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

    def kommentarChanged(self, name, text):
        if Wolke.DB.vorteile[name].kommentarErlauben:
            Wolke.Char.vorteileKommentare[name] = text
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

    def handleAddKommentarWidget(self, name, parent):
        if not Wolke.DB.vorteile[name].kommentarErlauben or parent.childCount() > 0:
            return
        kommentar = ""
        if name in Wolke.Char.vorteileKommentare:
            kommentar = Wolke.Char.vorteileKommentare[name]

        w = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        margin = 4
        layout.setContentsMargins(0, margin, 0, margin)
        label = QtWidgets.QLabel("Kommentar")
        text = QtWidgets.QLineEdit(kommentar)
        layout.addWidget(label)
        layout.addWidget(text)
        w.setLayout(layout)
        text.textChanged.connect(lambda text, name=name: self.kommentarChanged(name, text))

        child = QtWidgets.QTreeWidgetItem(parent)
        child.setSizeHint(0, QtCore.QSize(0, self.rowHeight + 2*margin))
        self.ui.treeWidget.setItemWidget(child,0,w)
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
            minderpaktWidget = self.ui.treeWidget.findItems(Wolke.Char.minderpakt, QtCore.Qt.MatchRecursive)[0]

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
            minderpaktWidget = self.ui.treeWidget.findItems(Wolke.Char.minderpakt, QtCore.Qt.MatchRecursive)[0]
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
        self.ui.treeWidget.blockSignals(True)
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
        self.ui.treeWidget.blockSignals(False)

        if manualUpdate:
            self.itemChangeHandler(manualUpdate, 0)
    
    def vortClicked(self):
        for el in self.ui.treeWidget.selectedItems():
            if el.text(0) in self.vorteilTypen:
                continue
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()
        
    def updateInfo(self):
        if self.currentVort != "":
            vorteil = Wolke.DB.vorteile[self.currentVort]
            self.ui.labelVorteil.setText(vorteil.name)
            self.ui.labelTyp.setText(self.vorteilTypen[vorteil.typ])
            self.ui.labelNachkauf.setText(vorteil.nachkauf)

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
            self.ui.labelVoraussetzungen.setText(voraussetzungen)

            self.ui.plainText.setPlainText("")
            self.ui.plainText.appendHtml(Hilfsmethoden.fixHtml(vorteil.text))
            if vorteil.variableKosten and self.currentVort in Wolke.Char.vorteileVariableKosten:
                self.ui.labelKosten.setText(str(Wolke.Char.vorteileVariableKosten[self.currentVort]) + " EP")
            else:
                self.ui.labelKosten.setText(str(vorteil.kosten) + " EP")
            