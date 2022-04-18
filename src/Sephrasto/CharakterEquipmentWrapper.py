# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
from PyQt5 import QtWidgets, QtCore, QtGui
from CharakterWaffenWrapper import CharakterWaffenWrapper
from CharakterInventarWrapper import CharakterInventarWrapper
import UI.CharakterTabWidget
from EventBus import EventBus

class EquipWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterTabWidget.Ui_Form()
        self.ui.setupUi(self.form)

        waffenWrapper = EventBus.applyFilter("class_waffen_wrapper", CharakterWaffenWrapper)
        if waffenWrapper:
            self.waffenWrapper = waffenWrapper()
            self.waffenWrapper.modified.connect(self.onModified)
            self.ui.tabs.addTab(self.waffenWrapper.form, "Waffen")

        inventarWrapper = EventBus.applyFilter("class_inventar_wrapper", CharakterInventarWrapper)
        if inventarWrapper:
            self.inventarWrapper = inventarWrapper()
            self.inventarWrapper.modified.connect(self.onModified)
            self.ui.tabs.addTab(self.inventarWrapper.form, "Inventar")

        self.ui.tabs.currentChanged.connect(self.load)
        for i in range(self.ui.tabs.tabBar().count()):
            self.ui.tabs.tabBar().setTabTextColor(i, QtGui.QColor(Wolke.HeadingColor))
        self.ui.tabs.setStyleSheet('QTabBar { font-size: ' + str(Wolke.Settings["FontHeadingSize"]) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')

    def load(self):
        if hasattr(self, "waffenWrapper") and self.ui.tabs.currentWidget() == self.waffenWrapper.form:
            self.waffenWrapper.load()
        elif hasattr(self, "inventarWrapper") and self.ui.tabs.currentWidget() == self.inventarWrapper.form:
            self.inventarWrapper.load()

    def onModified(self):
        self.modified.emit()