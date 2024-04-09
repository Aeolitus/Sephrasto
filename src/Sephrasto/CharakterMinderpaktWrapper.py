# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:21:03 2017

@author: Aeolitus
"""
from Wolke import Wolke
import UI.CharakterMinderpakt
from PySide6 import QtWidgets, QtCore, QtGui
import logging
from Hilfsmethoden import Hilfsmethoden, SortedCategoryToListDict
from QtUtils.AutoResizingTextBrowser import TextEditAutoResizer

class CharakterMinderpaktWrapper():    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing Minderpakt...")
        self.form = QtWidgets.QDialog()
        self.ui = UI.CharakterMinderpakt.Ui_Dialog()
        self.ui.setupUi(self.form)
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.autoResizeHelper = TextEditAutoResizer(self.ui.plainText)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Abbrechen")

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.6), int(width*0.4)])

        self.ui.treeWidget.itemSelectionChanged.connect(self.vortClicked)
        self.ui.treeWidget.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)

        if len(Wolke.Char.vorteile) > 0:
            self.currentVort = next(iter(Wolke.Char.vorteile))
        else:
            self.currentVort = ""
        self.initVorteile()
        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()
        if self.ret == QtWidgets.QDialog.Accepted:
            if self.currentVort not in Wolke.DB.vorteile:
                self.minderpakt = None
            else:
                self.minderpakt = self.currentVort
        else:
            self.minderpakt = None
          
    def initVorteile(self):
        self.ui.treeWidget.blockSignals(True)
        vorteileByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Vorteile: Kategorien"].wert)
        for vorteil in Wolke.DB.vorteile.values():
            if vorteil.kosten > 20 and not vorteil.variableKosten:
                continue
            if vorteil.kosten < 0:
                continue
            if vorteil.name in Wolke.Char.vorteile:
                continue
            vorteileByKategorie.append(vorteil.kategorie, vorteil.name)

        vorteileByKategorie.sortValues()

        for kategorie, vorteile in vorteileByKategorie.items():
            if len(vorteile) == 0:
                continue
            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            parent.setText(0, kategorie)
            parent.setText(1,"")
            parent.setExpanded(True)
            font = QtGui.QFont(Wolke.Settings["Font"], Wolke.FontHeadingSizeL3)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            parent.setFont(0, font)
            for el in vorteile:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, el)
                if Wolke.DB.vorteile[el].variableKosten:
                    child.setText(1, "20 EP")
                else:
                    child.setText(1, str(Wolke.DB.vorteile[el].kosten) + " EP")
        self.updateInfo()
        self.ui.treeWidget.blockSignals(False)
    
    def vortClicked(self):
        for el in self.ui.treeWidget.selectedItems():
            if el.text(0) in Wolke.DB.einstellungen["Vorteile: Kategorien"].wert:
                continue
            self.currentVort = el.text(0)
            break #First one should be all of them
        self.updateInfo()
 
    def updateInfo(self):
        if self.currentVort == "":
            return
        vorteil = Wolke.DB.vorteile[self.currentVort]
        self.ui.labelVorteil.setText(vorteil.name)
        self.ui.labelTyp.setText(vorteil.kategorieName(Wolke.DB))
        self.ui.labelNachkauf.setText(vorteil.nachkauf)

        text = vorteil.text
        if vorteil.info:
            text += f"\n\n<b>Sephrasto</b>: {vorteil.info}"
        self.ui.plainText.setText(Hilfsmethoden.fixHtml(text))
        if vorteil.variableKosten:
            self.ui.labelKosten.setText("20 EP")
        else:
            self.ui.labelKosten.setText(str(vorteil.kosten) + " EP")