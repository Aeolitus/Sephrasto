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
import UI.CharakterTabWidget
from EventBus import EventBus

class FertigkeitenWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterTabWidget.Ui_Form()
        self.ui.setupUi(self.form)

        profanWrapper = EventBus.applyFilter("class_profanefertigkeiten_wrapper", ProfaneFertigkeitenWrapper)
        if profanWrapper:
            self.profanWrapper = profanWrapper()
            self.profanWrapper.modified.connect(self.onModified)
            self.ui.tabs.addTab(self.profanWrapper.form, "Profane")

        freieWrapper = EventBus.applyFilter("class_freiefertigkeiten_wrapper", CharakterFreieFertWrapper)
        if freieWrapper:
            self.freieWrapper = freieWrapper()
            self.freieWrapper.modified.connect(self.onModified)
            self.ui.tabs.addTab(self.freieWrapper.form, "Freie")

        ueberWrapper = EventBus.applyFilter("class_uebernatuerlichefertigkeiten_wrapper", UebernatuerlichWrapper)
        if ueberWrapper:
            self.ueberWrapper = ueberWrapper()
            self.ueberWrapper.modified.connect(self.onModified)
            self.ui.tabs.addTab(self.ueberWrapper.form, "Übernatürliche")

        self.ui.tabs.currentChanged.connect(self.load)
        for i in range(self.ui.tabs.tabBar().count()):
            self.ui.tabs.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))
        self.ui.tabs.setStyleSheet('QTabBar { font-size: ' + str(Wolke.Settings["FontHeadingSize"]) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')

    def load(self):
        if hasattr(self, "profanWrapper") and self.ui.tabs.currentWidget() == self.profanWrapper.form:
            self.profanWrapper.load()
        elif hasattr(self, "freieWrapper") and self.ui.tabs.currentWidget() == self.freieWrapper.form:
            self.freieWrapper.load()
        elif hasattr(self, "ueberWrapper") and self.ui.tabs.currentWidget() == self.ueberWrapper.form:
            self.ueberWrapper.load()

        if hasattr(self, "ueberWrapper"):
            self.ui.tabs.setTabVisible(self.ui.tabs.indexOf(self.ueberWrapper.form), len(Wolke.Char.übernatürlicheFertigkeiten) > 0)

    def onModified(self):
        self.modified.emit()