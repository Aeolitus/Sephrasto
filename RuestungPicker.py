# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import copy
import logging

from PyQt5 import QtCore, QtWidgets

import CharakterRuestungen
import Definitionen
from EventBus import EventBus
from Wolke import Wolke


class RuestungPicker(object):
    def __init__(self, ruestung=None, system=0):
        super().__init__()
        logging.debug("Initializing RuestungPicker...")

        self.system = system
        self.ruestungErsetzen = False
        self.ruestung = None
        if ruestung is not None and ruestung in Wolke.DB.rüstungen:
            self.current = ruestung
        else:
            self.current = ""

        self.Form = QtWidgets.QDialog()
        self.ui = CharakterRuestungen.Ui_Dialog()
        self.ui.setupUi(self.Form)

        self.Form.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        if ruestung is not None and ruestung != "":
            self.replaceButton = QtWidgets.QPushButton("Rüstung ersetzen")
            self.replaceButton.clicked.connect(self.replaceClicked)
            self.ui.buttonBox.addButton(
                self.replaceButton, QtWidgets.QDialogButtonBox.AcceptRole
            )

        logging.debug("Ui is Setup...")
        self.populateTree()
        logging.debug("Tree Filled...")
        self.ui.treeArmors.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeArmors.itemDoubleClicked.connect(
            lambda item, column: self.ui.buttonBox.buttons()[0].click()
        )
        self.ui.treeArmors.header().setSectionResizeMode(0, 1)
        self.ui.treeArmors.setFocus()
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

        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()

        if self.ret == QtWidgets.QDialog.Accepted and self.current != "":
            self.ruestung = copy.deepcopy(Wolke.DB.rüstungen[self.current])
            if self.ruestung.name.endswith(" (ZRS)"):
                self.ruestung.name = self.ruestung.name[:-6]
        else:
            self.ruestung = None

    def replaceClicked(self):
        self.ruestungErsetzen = True

    def populateTree(self):
        currSet = self.current != ""
        self.ui.treeArmors.clear()

        for typ in Definitionen.RuestungsTypen:
            ruestungen = []
            for rues in Wolke.DB.rüstungen:
                if Wolke.DB.rüstungen[rues].system not in [0, self.system]:
                    continue

                if self.ui.nameFilterEdit.text():
                    filterText = self.ui.nameFilterEdit.text().lower()
                    if filterText not in Wolke.DB.rüstungen[rues].name.lower():
                        continue

                if Definitionen.RuestungsTypen[Wolke.DB.rüstungen[rues].typ] == typ:
                    ruestungen.append(rues)

            ruestungen.sort()
            if not ruestungen:
                continue

            parent = QtWidgets.QTreeWidgetItem(self.ui.treeArmors)
            parent.setText(0, typ + "en")
            parent.setExpanded(True)
            for el in ruestungen:
                if not currSet:
                    self.current = el
                    currSet = True
                child = QtWidgets.QTreeWidgetItem(parent)
                name = Wolke.DB.rüstungen[el].name or el
                if name.endswith(" (ZRS)"):
                    name = name[:-6]
                child.setText(0, name)
                child.setData(
                    0, QtCore.Qt.UserRole, el
                )  # store key of weapon in user data

        self.ui.treeArmors.sortItems(1, QtCore.Qt.AscendingOrder)

        if self.current in Wolke.DB.rüstungen:
            found = self.ui.treeArmors.findItems(
                Wolke.DB.rüstungen[self.current].name,
                QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive,
            )
            if len(found) > 0:
                self.ui.treeArmors.setCurrentItem(
                    found[0], 0, QtCore.QItemSelectionModel.Select
                )
        elif (
            self.ui.treeArmors.topLevelItemCount() > 0
            and self.ui.treeArmors.topLevelItem(0).childCount() > 0
        ):
            self.ui.treeArmors.setCurrentItem(
                self.ui.treeArmors.topLevelItem(0).child(0),
                0,
                QtCore.QItemSelectionModel.Select,
            )
        self.changeHandler()

    def changeHandler(self):
        self.current = ""
        for el in self.ui.treeArmors.selectedItems():
            if el.text(0)[:-2] in Definitionen.RuestungsTypen:
                continue
            self.current = el.data(0, QtCore.Qt.UserRole)  # contains key of armor
            break
        self.updateInfo()

    def updateInfo(self):
        self.ui.buttonBox.buttons()[0].setEnabled(self.current != "")
        if self.current == "":
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
            self.ui.lblTyp.setText(Definitionen.RuestungsTypen[r.typ])

            if self.system == 1:
                be = EventBus.applyFilter(
                    "ruestung_be", r.getRSGesamtInt(), {"name": r.name}
                )
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
            self.ui.teBeschreibung.setPlainText(r.text)
