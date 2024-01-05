# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import UI.CharakterWaffenPicker
from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import logging
from Core.Fertigkeit import KampffertigkeitTyp
from Core.Waffe import WaffeDefinition
import CharakterEquipmentWrapper
import copy

class WaffenPicker(object):
    def __init__(self,waffe=None):
        super().__init__()
        logging.debug("Initializing WaffenPicker...")
        self.waffe = None
        if waffe is not None and waffe in Wolke.DB.waffen:
            self.current = waffe
        else:
            self.current = ""
        self.form = QtWidgets.QDialog()
        self.ui = UI.CharakterWaffenPicker.Ui_Dialog()
        self.ui.setupUi(self.form)
        
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)
        
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Abbrechen")

        windowSize = Wolke.Settings["WindowSize-Waffen"]
        self.form.resize(windowSize[0], windowSize[1])

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        logging.debug("Ui is Setup...")
        self.populateTree()
        logging.debug("Tree Filled...")
        self.ui.treeWeapons.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeWeapons.itemDoubleClicked.connect(lambda item, column: self.ui.buttonBox.buttons()[0].click())
        self.ui.treeWeapons.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)

        self.ui.labelFilter.setText("\uf002")
        self.ui.nameFilterEdit.setFocus()
        self.updateInfo()
        logging.debug("Info Updated...")
        self.ui.nameFilterEdit.textChanged.connect(self.populateTree)
        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()

        Wolke.Settings["WindowSize-Waffen"] = [self.form.size().width(), self.form.size().height()]

        if self.ret == QtWidgets.QDialog.Accepted and self.current != '':
            self.waffe = copy.copy(Wolke.DB.waffen[self.current])
        else:
            self.waffe = None

    def populateTree(self):
        currSet = self.current != ""
        self.ui.treeWeapons.clear();
        kampfferts = self.findKampfFertigkeiten()
        for kind in kampfferts:
            wafs = []
            for waf in Wolke.DB.waffen:
                if self.ui.nameFilterEdit.text():
                    filterText = self.ui.nameFilterEdit.text().lower()
                    if (not filterText in Wolke.DB.waffen[waf].anzeigename.lower()):
                        continue
                if Wolke.DB.waffen[waf].fertigkeit == kind.name:
                    wafs.append(waf)
            wafs.sort(key=Hilfsmethoden.unicodeCaseInsensitive)
            if len(wafs) == 0:
                continue

            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWeapons)
            parent.setText(0,kind.name)
            parent.setText(1,"")
            parent.setExpanded(True)
            font = QtGui.QFont(Wolke.Settings["Font"], Wolke.FontHeadingSizeL3)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            parent.setFont(0, font)
            for el in wafs:
                if not currSet:
                    self.current = el
                    currSet = True
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, Wolke.DB.waffen[el].anzeigename or el)
                child.setText(1, Wolke.DB.waffen[el].talent)
                child.setData(0, QtCore.Qt.UserRole, el) # store key of weapon in user data

        self.ui.treeWeapons.sortItems(1,QtCore.Qt.AscendingOrder)

        if self.current in Wolke.DB.waffen:
            found = self.ui.treeWeapons.findItems(Wolke.DB.waffen[self.current].anzeigename, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            if len(found) > 0:
                self.ui.treeWeapons.setCurrentItem(found[0], 0, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        elif self.ui.treeWeapons.topLevelItemCount() > 0 and self.ui.treeWeapons.topLevelItem(0).childCount() > 0:
            self.ui.treeWeapons.setCurrentItem(self.ui.treeWeapons.topLevelItem(0).child(0), 0, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        self.changeHandler()


    def findKampfFertigkeiten(self):
        return [el for el in Wolke.DB.fertigkeiten.values() if el.kampffertigkeit != KampffertigkeitTyp.Keine]

    def changeHandler(self):
        kampfferts = []
        for fert in self.findKampfFertigkeiten():
            kampfferts.append(fert.name)
        self.current = ""
        for el in self.ui.treeWeapons.selectedItems():
            if el.text(0) in kampfferts:
                continue
            self.current = el.data(0, QtCore.Qt.UserRole) # contains key of weapon
            break
        self.updateInfo()
        
    def updateInfo(self):
        self.ui.buttonBox.buttons()[0].setEnabled(self.current != "")
        if self.current == "":
            self.ui.labelName.setText("Keine Waffe selektiert")
            self.ui.labelTyp.setText("")
            self.ui.labelFert.setText("")
            self.ui.labelTalent.setText("")
            self.ui.labelKampfstile.setText("Kampfstile:")
            self.ui.labelTP.setText("")
            self.ui.labelRW.setText("")
            self.ui.labelWM.setText("")
            self.ui.labelLZ.setText("")
            self.ui.labelH.setText("")
            self.ui.labelEigenschaften.setText("Eigenschaften:")
        else:
            w = Wolke.DB.waffen[self.current]
            name = w.name
            if name.endswith(" (" + w.talent + ")"):
                name = name[:-3-len(w.talent)]
            self.ui.labelName.setText(name)
            if w.nahkampf:
                self.ui.labelTyp.setText("Nahkampfwaffe")
            else:
                self.ui.labelTyp.setText("Fernkampfwaffe")
            self.ui.labelFert.setText(w.fertigkeit)
            self.ui.labelTalent.setText(w.talent)
            stile = WaffeDefinition.keinKampfstil

            if len(w.kampfstile) > 0:
                stile = ", ".join(w.kampfstile)

            self.ui.labelKampfstile.setText("Kampfstile: " + stile)
            tp = str(w.würfel) + "W" + str(w.würfelSeiten)
            if w.plus < 0:
                tp += "" + str(w.plus)
            else:
                tp += "+" + str(w.plus)
            self.ui.labelTP.setText(tp)
            self.ui.labelRW.setText(str(w.rw))

            if w.wm<0:
                self.ui.labelWM.setText(str(w.wm))
            else:
                self.ui.labelWM.setText("+" + str(w.wm))

            if w.nahkampf:
                self.ui.labelLZ_Text.hide()
                self.ui.labelLZ.hide()
            else:
                self.ui.labelLZ_Text.show()
                self.ui.labelLZ.show()
                self.ui.labelLZ.setText(str(w.lz))
            self.ui.labelH.setText(str(w.härte))
            if len(w.eigenschaften) > 0:
                self.ui.labelEigenschaften.setText("Eigenschaften: " + ", ".join(w.eigenschaften))
            else:
                self.ui.labelEigenschaften.setText("Eigenschaften: keine")