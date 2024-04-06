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
from QtUtils.Section import Section
from QtUtils.AutoResizingTextBrowser import AutoResizingTextBrowser, TextEditAutoResizer
from functools import partial
from Core.Vorteil import Vorteil
from VoraussetzungenListe import VoraussetzungenListe

class CharakterVorteileWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self, supportedTypes = []):
        super().__init__()
        logging.debug("Initializing VorteileWrapper...")
        self.rowHeight = Hilfsmethoden.emToPixels(3.9)
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterVorteile.Ui_Form()
        self.ui.setupUi(self.form)

        font = QtWidgets.QApplication.instance().font()
        self.ui.treeWidget.setProperty("class", "treeVorteile")
        self.ui.treeWidget.itemSelectionChanged.connect(self.vortClicked)
        self.ui.treeWidget.itemChanged.connect(self.itemChangeHandler)
        self.ui.treeWidget.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.ui.treeWidget.header().resizeSection(1, Hilfsmethoden.emToPixels(10))

        self.autoResizeHelper = TextEditAutoResizer(self.ui.plainText)

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        if len(Wolke.Char.vorteile) > 0:
            self.currentVort = Wolke.Char.vorteile.__iter__().__next__()
        else:
            self.currentVort = Wolke.DB.vorteile.__iter__().__next__()

        self.itemWidgets = {}
        self.qvSlots = {}
        self.qvTexts = {}
        self.qvSections = {}

        self.ui.checkShowAll.stateChanged.connect(self.onShowAllClicked)
        self.showUnavailable = False

        # Set supported Vorteil Typen - all by default. This increases the reusability and might be useful for plugins.
        self.supportedTypes = supportedTypes
        if len(self.supportedTypes) == 0:
            for i in range(len(Wolke.DB.einstellungen["Vorteile: Typen"].wert)):
                self.supportedTypes.append(i)
        self.initVorteile()

        self.ui.labelFilter.setText("\uf002")
        self.ui.nameFilterEdit.setFocus()
        self.ui.nameFilterEdit.textChanged.connect(self.load)

    def onShowAllClicked(self):
        self.showUnavailable = self.ui.checkShowAll.isChecked()
        self.load()

    def kosten(self, vorteil):
        if isinstance(vorteil, Vorteil):
            return vorteil.kosten
        else:
            return EventBus.applyFilter("vorteil_kosten", vorteil.kosten, { "charakter" : Wolke.Char, "vorteil" : vorteil.name })

    def initVorteile(self):
        self.ui.treeWidget.blockSignals(True)
        vortList = []
        for vortTyp in Wolke.DB.einstellungen["Vorteile: Typen"].wert:
            vortList.append([])

        for el in Wolke.DB.vorteile:
            idx = min(Wolke.DB.vorteile[el].typ, len(vortList) - 1)
            if idx not in self.supportedTypes:
                continue
            vortList[idx].append(el)
        
        for vorteile in vortList:
            vorteile.sort(key=Hilfsmethoden.unicodeCaseInsensitive)

        for i in range(len(vortList)):
            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            parent.setText(0, Wolke.DB.einstellungen["Vorteile: Typen"].wert[i])
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
                child.setText(0, el)
                child.setSizeHint(0, QtCore.QSize(0, self.rowHeight))

                vorteil = Wolke.DB.vorteile[el]
                if el in Wolke.Char.vorteile:
                    vorteil = Wolke.Char.vorteile[el]
                    child.setCheckState(0, QtCore.Qt.Checked)

                if vorteil.variableKosten:
                    spin = QtWidgets.QSpinBox()
                    spin.setMinimum(-9999)
                    spin.setSuffix(" EP")
                    spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
                    spin.setMaximum(9999)
                    spin.setValue(self.kosten(vorteil))
                    spin.setReadOnly("Minderpakt" in Wolke.Char.vorteile and vorteil.name == Wolke.Char.vorteile["Minderpakt"].kommentar)
                    spin.setSingleStep(20)
                    self.itemWidgets[el] = spin
                    spin.valueChanged.connect(partial(self.spinnerChanged, name=vorteil.name))
                    self.ui.treeWidget.setItemWidget(child,1,spin)
                else:
                    child.setText(1, str(self.kosten(vorteil)) + " EP")

                if vorteil.kommentarErlauben and child.checkState(0) == QtCore.Qt.Checked:
                    self.handleAddKommentarWidget(el, child)

        self.ui.treeWidget.blockSignals(False)
        
    def load(self):
        self.ui.checkShowAll.setVisible(Wolke.Char.voraussetzungenPruefen)

        self.ui.treeWidget.blockSignals(True)
        vortList = []
        for vortTyp in Wolke.DB.einstellungen["Vorteile: Typen"].wert:
            vortList.append([])

        for vorteil in Wolke.DB.vorteile.values():
            idx = min(vorteil.typ, len(vortList) -1)
            if idx not in self.supportedTypes:
                continue

            if vorteil.name in Wolke.Char.vorteile:
                vorteil = Wolke.Char.vorteile[vorteil.name]

            if Wolke.Char.voraussetzungenPrüfen(vorteil):
                vortList[idx].append(vorteil.name)

        for i in range(len(vortList)):
            itm = self.ui.treeWidget.topLevelItem(i)
            if type(itm) != QtWidgets.QTreeWidgetItem:
                continue
            if itm == 0: 
                continue

            if self.showUnavailable:
                itm.setHidden(itm.childCount() == 0)
            else:
                itm.setHidden(len(vortList[i]) == 0)

            for j in range(itm.childCount()):
                chi = itm.child(j)
                if type(chi) != QtWidgets.QTreeWidgetItem:
                    continue
                vorteil = Wolke.DB.vorteile[chi.text(0)]
                if vorteil.name in Wolke.Char.vorteile:
                    vorteil = Wolke.Char.vorteile[vorteil.name]
                    chi.setCheckState(0, QtCore.Qt.Checked)
                    if vorteil.kommentarErlauben:
                        self.handleAddKommentarWidget(vorteil.name, chi)
                else:
                    chi.setCheckState(0, QtCore.Qt.Unchecked)
                    # remove potential kommentar widget (call doesnt do anything if it doesnt exist)
                    chi.takeChild(0)
                    # restore potential widget changes by minderpakt
                    if vorteil.name in self.itemWidgets:
                        self.itemWidgets[vorteil.name].setReadOnly(False)

                if vorteil.variableKosten:
                    self.itemWidgets[vorteil.name].setValue(self.kosten(vorteil))
                else:
                    chi.setText(1, str(self.kosten(vorteil)) + " EP")


                isFiltered = self.ui.nameFilterEdit.text() != "" and \
                    (not self.ui.nameFilterEdit.text().lower() in vorteil.name.lower()) and \
                    (not self.ui.nameFilterEdit.text().lower() in itm.text(0).lower())

                if vorteil.name not in vortList[i]:
                    if self.showUnavailable:
                        chi.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                        chi.setCheckState(0,QtCore.Qt.Unchecked)
                        chi.setForeground(0, QtGui.QBrush(QtCore.Qt.red))
                        chi.setHidden(isFiltered)
                    else:
                        chi.setHidden(True)
                    Wolke.Char.removeVorteil(vorteil.name)
                else:
                    chi.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    chi.setForeground(0, QtGui.QBrush())
                    chi.setHidden(isFiltered)

        self.updateInfo()
        self.ui.treeWidget.blockSignals(False)
        
    def update(self):
        pass

    def spinnerChanged(self, value, name):
        if name in Wolke.Char.vorteile and Wolke.Char.vorteile[name].variableKosten:
            Wolke.Char.vorteile[name].kosten = self.itemWidgets[name].value()
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

    def kommentarChanged(self, text, name):
        if name in Wolke.Char.vorteile and Wolke.Char.vorteile[name].kommentarErlauben:
            Wolke.Char.vorteile[name].kommentar = text
        self.currentVort = name
        self.modified.emit()
        self.updateInfo()

    def handleAddKommentarWidget(self, name, parent):
        if not Wolke.DB.vorteile[name].kommentarErlauben or parent.childCount() > 0:
            return
        kommentar = ""
        if name in Wolke.Char.vorteile:
            kommentar = Wolke.Char.vorteile[name].kommentar

        w = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel("Kommentar")
        text = QtWidgets.QLineEdit(kommentar)
        text.setReadOnly(name == "Minderpakt")
        layout.addWidget(label)
        layout.addWidget(text)
        w.setLayout(layout)
        text.textChanged.connect(partial(self.kommentarChanged, name=name))
        child = QtWidgets.QTreeWidgetItem(parent)
        child.setSizeHint(0, QtCore.QSize(0, self.rowHeight))
        self.ui.treeWidget.setItemWidget(child,0,w)
        parent.setExpanded(True)

    def handleAddMinderpakt(self, name, item):
        if name != "Minderpakt":
            return None
        mpWrapper = CharakterMinderpaktWrapper.CharakterMinderpaktWrapper()
        if mpWrapper.minderpakt is None:
            Wolke.Char.removeVorteil(name)
            return None
        if mpWrapper.minderpakt not in Wolke.Char.vorteile:
            minderpakt = Wolke.Char.vorteile["Minderpakt"]
            minderpakt.kommentar = mpWrapper.minderpakt
            minderpakt.voraussetzungen = VoraussetzungenListe().compile("Vorteil " + minderpakt.kommentar, Wolke.DB)
            vorteil = Wolke.Char.addVorteil(minderpakt.kommentar)
            vorteil.voraussetzungen = VoraussetzungenListe().compile("Vorteil Minderpakt", Wolke.DB)
            vorteil.kosten = 20
           
            minderpaktWidget = self.ui.treeWidget.findItems(vorteil.name, QtCore.Qt.MatchRecursive)[0]

            if vorteil.name in self.itemWidgets:
                self.itemWidgets[vorteil.name].setReadOnly(True)
                self.itemWidgets[vorteil.name].setValue(20)
            else:
                minderpaktWidget.setText(1, "20 EP")
            return minderpaktWidget
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
            manualUpdate = self.handleAddMinderpakt(name, item)
            self.handleAddKommentarWidget(name, item)
        elif cs != QtCore.Qt.Checked and name in Wolke.Char.vorteile:
            Wolke.Char.removeVorteil(name)

        self.modified.emit()
        self.load()
        self.ui.treeWidget.blockSignals(False)

        if manualUpdate:
           self.itemChangeHandler(manualUpdate, 0)
    
    def vortClicked(self):
        for el in self.ui.treeWidget.selectedItems():
            if el.text(0) in Wolke.DB.einstellungen["Vorteile: Typen"].wert:
                continue
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()

    def updateInfo(self):
        if self.currentVort != "":
            vorteil = Wolke.DB.vorteile[self.currentVort]
            if self.currentVort in Wolke.Char.vorteile:
                vorteil = Wolke.Char.vorteile[self.currentVort]
            self.ui.labelVorteil.setText(vorteil.name)
            self.ui.labelTyp.setText(Wolke.DB.einstellungen["Vorteile: Typen"].wert[vorteil.typ])
            self.ui.labelNachkauf.setText(vorteil.nachkauf)
            voraussetzungen = vorteil.voraussetzungen.anzeigetext(Wolke.DB)
            self.ui.labelVoraussetzungen.setText(voraussetzungen)

            text = vorteil.text
            if vorteil.bedingungen:
                text = f"<i>Bedingungen</i>: {vorteil.bedingungen}\n\n" + text

            if vorteil.info:
                text += f"\n\n<b>Sephrasto</b>: {vorteil.info}"
            self.ui.plainText.setText(Hilfsmethoden.fixHtml(text))

            kosten = self.kosten(vorteil)
            if self.currentVort in Wolke.Char.vorteile:
                kosten = Wolke.Char.vorteile[self.currentVort].kosten
            self.ui.labelKosten.setText(str(kosten) + " EP")

            # delete old querverweise ui elements
            for qv in self.qvSlots:
                self.qvTexts[qv].sizeChanged.disconnect(self.qvSlots[qv]) #leaks otherwise
            self.qvSlots = {}
            self.qvTexts = {}
            self.qvSections = {}

            for i in reversed(range(self.ui.vlQuerverweise.count())):
                widget = self.ui.vlQuerverweise.itemAt(i).widget()
                widget.setParent(None)
                del widget

            # build new querverweise ui elements
            if len(vorteil.querverweise) > 0:
                header = QtWidgets.QLabel()
                header.setText("Querverweise:")
                self.ui.vlQuerverweise.addWidget(header)

            for qv in vorteil.querverweiseResolved:
                section = Section(qv)
                self.qvSections[qv] = section
                contentLayout = QtWidgets.QVBoxLayout()
                contentLayout.setContentsMargins(0, 0, 0, 0)
                qvText = AutoResizingTextBrowser()
                self.qvTexts[qv] = qvText
                qvText.setText(Hilfsmethoden.fixHtml(vorteil.querverweiseResolved[qv]))
                self.qvSlots[qv] = partial(self.updateSectionHeight, qv=qv)
                qvText.sizeChanged.connect(self.qvSlots[qv])
                contentLayout.addWidget(qvText)
                section.setContentLayout(contentLayout)
                self.ui.vlQuerverweise.addWidget(section)

    def updateSectionHeight(self, width, height, qv):
        self.qvSections[qv].updateHeight(height, True)