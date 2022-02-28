# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
from PyQt5 import QtWidgets, QtCore, QtGui
from CharakterProfaneFertigkeitenWrapper import ProfaneFertigkeitenWrapper
from CharakterFreieFertWrapper import CharakterFreieFertWrapper
from CharakterUebernatuerlichWrapper import UebernatuerlichWrapper
import UI.CharakterFertigkeiten
from EventBus import EventBus

class FertigkeitenWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.formFert = QtWidgets.QWidget()
        self.uiFert = UI.CharakterFertigkeiten.Ui_Form()
        self.uiFert.setupUi(self.formFert)

        profanWrapper = EventBus.applyFilter("class_profanefertigkeiten_wrapper", ProfaneFertigkeitenWrapper)
        if profanWrapper:
            self.profanWrapper = profanWrapper()
            self.profanWrapper.modified.connect(self.onModified)
            self.uiFert.tabs.addTab(self.profanWrapper.formFert, "Profane")

        freieWrapper = EventBus.applyFilter("class_freiefertigkeiten_wrapper", CharakterFreieFertWrapper)
        if freieWrapper:
            self.freieWrapper = freieWrapper()
            self.freieWrapper.modified.connect(self.onModified)
            self.uiFert.tabs.addTab(self.freieWrapper.formFert, "Freie")

        ueberWrapper = EventBus.applyFilter("class_uebernatuerlichefertigkeiten_wrapper", UebernatuerlichWrapper)
        if ueberWrapper:
            self.ueberWrapper = ueberWrapper()
            self.ueberWrapper.modified.connect(self.onModified)
            self.uiFert.tabs.addTab(self.ueberWrapper.formFert, "Übernatürliche")

        self.uiFert.tabs.currentChanged.connect(self.reload)
        for i in range(self.uiFert.tabs.tabBar().count()):
            self.uiFert.tabs.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))
        self.uiFert.tabs.setStyleSheet('QTabBar { font-size: ' + str(Wolke.Settings["FontHeadingSize"]) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')

    def load(self):
        self.reload(self.uiFert.tabs.currentIndex())
        if hasattr(self, "ueberWrapper"):
            self.uiFert.tabs.setTabVisible(self.uiFert.tabs.indexOf(self.ueberWrapper.formFert), len(Wolke.Char.übernatürlicheFertigkeiten) > 0)

    def reload(self, idx):
        if idx == 0:
            if hasattr(self, "profanWrapper"):
                self.profanWrapper.load()
        elif idx == 1:
            if hasattr(self, "freieWrapper"):
                self.freieWrapper.load()
        elif idx == 2:
            if hasattr(self, "ueberWrapper"):
                self.ueberWrapper.load()

    def update(self):
        self.profanWrapper.update()
        self.freieWrapper.update()
        self.ueberWrapper.update()

    def onModified(self):
        self.modified.emit()