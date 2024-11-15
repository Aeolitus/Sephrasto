# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import UI.CharakterRuestungPicker
from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import logging
import copy
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden
from QtUtils.AutoResizingTextBrowser import TextEditAutoResizer
from Hilfsmethoden import SortedCategoryToListDict
from QtUtils.TreeExpansionHelper import TreeExpansionHelper

class RuestungPicker(object):

    def __init__(self,ruestung=None,system=0):
        super().__init__()
        logging.debug("Initializing RuestungPicker...")

        self.system = system
        self.ruestungErsetzen = False
        self.ruestung = None
        if ruestung is not None and ruestung in Wolke.DB.rüstungen:
            self.current = ruestung
        else:
            self.current = ""

        self.form = QtWidgets.QDialog()
        self.ui = UI.CharakterRuestungPicker.Ui_Dialog()
        self.ui.setupUi(self.form)
        
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.autoResizeHelper = TextEditAutoResizer(self.ui.teBeschreibung)

        self.ui.labelUnofficial.setVisible(Wolke.DB.einstellungen["Rüstungen: Inoffiziell-Warnung anzeigen"].wert)

        windowSize = Wolke.Settings["WindowSize-Ruestungen"]
        self.form.resize(windowSize[0], windowSize[1])

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        if ruestung is not None and ruestung != "":
            self.replaceButton = QtWidgets.QPushButton("Rüstung ersetzen")
            self.replaceButton.clicked.connect(self.replaceClicked)
            self.ui.buttonBox.addButton(self.replaceButton, QtWidgets.QDialogButtonBox.AcceptRole)

        self.onSetupUi()
        logging.debug("Ui is Setup...")
        self.ui.treeArmors.setHeaderHidden(True)
        self.populateTree()
        logging.debug("Tree Filled...")
        self.ui.treeArmors.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeArmors.itemDoubleClicked.connect(lambda item, column: self.ui.buttonBox.buttons()[0].click())
        self.ui.treeArmors.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Fixed)

        self.expansionHelper = TreeExpansionHelper(self.ui.treeArmors, self.ui.buttonExpandToggle)

        self.ui.labelFilter.setText("\uf002")
        self.ui.nameFilterEdit.setFocus()

        self.shortcutSearch = QtGui.QAction()
        self.shortcutSearch.setShortcut("Ctrl+F")
        self.shortcutSearch.triggered.connect(self.ui.nameFilterEdit.setFocus)
        self.form.addAction(self.shortcutSearch)
        self.shortcutClearSearch = QtGui.QAction()
        self.shortcutClearSearch.setShortcut("Esc")
        self.shortcutClearSearch.triggered.connect(lambda: self.ui.nameFilterEdit.setText("") if self.ui.nameFilterEdit.hasFocus() and self.ui.nameFilterEdit.text() else self.form.reject())
        self.form.addAction(self.shortcutClearSearch)

        self.updateInfo()
        logging.debug("Info Updated...")
        self.ui.nameFilterEdit.textChanged.connect(self.populateTree)

        if self.system == 1:
            self.ui.lblBeine.hide()
            self.ui.lblSchwert.hide()
            self.ui.lblSchild.hide()
            self.ui.lblBauch.hide()
            self.ui.lblBrust.hide()
            self.ui.lblKopf.hide()
            self.ui.lblBeineL.hide()
            self.ui.lblSchwertL.hide()
            self.ui.lblSchildL.hide()
            self.ui.lblBauchL.hide()
            self.ui.lblBrustL.hide()
            self.ui.lblKopfL.hide()
            self.ui.lblZRS.hide()
        else:
            self.ui.lblBeine.show()
            self.ui.lblSchwert.show()
            self.ui.lblSchild.show()
            self.ui.lblBauch.show()
            self.ui.lblBrust.show()
            self.ui.lblKopf.show()
            self.ui.lblBeineL.show()
            self.ui.lblSchwertL.show()
            self.ui.lblSchildL.show()
            self.ui.lblBauchL.show()
            self.ui.lblBrustL.show()
            self.ui.lblKopfL.show()
            self.ui.lblZRS.show()

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()

        Wolke.Settings["WindowSize-Ruestungen"] = [self.form.size().width(), self.form.size().height()]

        if self.ret == QtWidgets.QDialog.Accepted and self.current != '':
            self.ruestung = copy.deepcopy(Wolke.DB.rüstungen[self.current])
            if self.ruestung.name.endswith(" (ZRS)"):
                self.ruestung.name = self.ruestung.name[:-6]
        else:
            self.ruestung = None

    def replaceClicked(self):
        self.ruestungErsetzen = True

    def onSetupUi(self):
        pass # for usage in plugins

    def populateTree(self):
        currSet = self.current != ""
        self.ui.treeArmors.clear()

        rüstungenByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Rüstungen: Kategorien"].wert)
        rüstungenByKategorie.setNameFilter(self.ui.nameFilterEdit.text())
        for r in Wolke.DB.rüstungen.values():
            if r.system != 0 and r.system != self.system:
                continue
            rüstungenByKategorie.append(r.kategorie, r.name)
        rüstungenByKategorie.sortValues()

        for kategorie, rüstungen in rüstungenByKategorie.items():
            if len(rüstungen) == 0:
                continue

            parent = QtWidgets.QTreeWidgetItem(self.ui.treeArmors)
            parent.setText(0, kategorie)
            parent.setExpanded(True)
            font = QtGui.QFont(Wolke.Settings["Font"], Wolke.FontHeadingSizeL3)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            parent.setFont(0, font)
            for el in rüstungen:
                if not currSet:
                    self.current = el
                    currSet = True
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setData(0, QtCore.Qt.UserRole, el)
                if el.endswith(" (ZRS)"):
                    child.setText(0, el[:-6])
                else:
                    child.setText(0, el)

        if self.current in Wolke.DB.rüstungen:
            found = self.ui.treeArmors.findItems(self.current, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            if len(found) > 0:
                self.ui.treeArmors.setCurrentItem(found[0], 0, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        elif self.ui.treeArmors.topLevelItemCount() > 0 and self.ui.treeArmors.topLevelItem(0).childCount() > 0:
            self.ui.treeArmors.setCurrentItem(self.ui.treeArmors.topLevelItem(0).child(0), 0, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        self.changeHandler()

    def changeHandler(self):
        self.current = ""
        for el in self.ui.treeArmors.selectedItems():
            if el.text(0) in Wolke.DB.einstellungen["Rüstungen: Kategorien"].wert:
                continue
            self.current = el.data(0, QtCore.Qt.UserRole) # contains key of armor
            break
        self.updateInfo()
        
    def updateInfo(self):
        self.ui.buttonBox.buttons()[0].setEnabled(self.current != "")
        if not self.current:
            self.ui.lblName.setText("Keine Rüstung selektiert")
            self.ui.lblTyp.setText("")
            self.ui.lblRS.setText("")
            self.ui.lblBeine.setText("")
            self.ui.lblSchwert.setText("")
            self.ui.lblSchild.setText("")
            self.ui.lblBauch.setText("")
            self.ui.lblBrust.setText("")
            self.ui.lblKopf.setText("")
            self.ui.lblZRS.setText("")
            self.ui.teBeschreibung.setPlainText("")
        else:
            r = Wolke.DB.rüstungen[self.current]

            name = r.name
            if name.endswith(" (ZRS)"):
                name = name[:-6]
            self.ui.lblName.setText(name)
            self.ui.lblTyp.setText(r.kategorieName(Wolke.DB))

            if self.system == 1:
                be = EventBus.applyFilter("ruestung_be", r.getRSGesamtInt(), { "name" : r.name })
                if be != r.getRSGesamtInt():
                    self.ui.lblRS.setText(str(r.getRSGesamtInt()) + "/" + str(be))
                else:
                    self.ui.lblRS.setText(str(r.getRSGesamtInt()))
            else:
                self.ui.lblRS.setText(str(r.getRSGesamt()))
            self.ui.lblBeine.setText(str(r.rs[0]))
            self.ui.lblSchwert.setText(str(r.rs[1]))
            self.ui.lblSchild.setText(str(r.rs[2]))
            self.ui.lblBauch.setText(str(r.rs[3]))
            self.ui.lblBrust.setText(str(r.rs[4]))
            self.ui.lblKopf.setText(str(r.rs[5]))
            self.ui.lblZRS.setText("= " + str(sum(r.rs)))
            self.ui.teBeschreibung.setText(Hilfsmethoden.fixHtml(r.text))