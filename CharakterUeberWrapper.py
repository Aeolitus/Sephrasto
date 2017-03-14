# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:35:48 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterUeber
from PyQt5 import QtWidgets, QtGui
class UeberWrapper(object):
    def __init__(self):
        super().__init__()
        self.formUeber = QtWidgets.QWidget()
        self.uiUeber = CharakterUeber.Ui_Form()
        self.uiUeber.setupUi(self.formUeber)
        
        self.model = QtGui.QStandardItemModel(None)
        self.ui.listTalente.setModel(self.model)
        
    def loadUeber(self):
        pass
    
    def updateUeber(self):
        pass
    
    def updateInfo(self):
        pass
    
    def updateTalents(self):
        pass
    
    def fwChanged(self):
        pass