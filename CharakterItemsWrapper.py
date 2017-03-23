# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:53:43 2017

@author: Aeolitus
"""
from Wolke import Wolke
import CharakterItems
from PyQt5 import QtWidgets, QtCore

class CharakterItemsWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.formIt = QtWidgets.QWidget()
        self.uiIt = CharakterItems.Ui_Form()
        self.uiIt.setupUi(self.formIt)
        
        
    def loadItems(self):
        count = 1
        for el in Wolke.Char.ausrüstung:
            eval("self.uiIt.lineEdit_" + str(count) + ".setText(\"" + el + "\")")
            count += 1
            if count > 26:
                break
    
    def updateFreie(self):
        Wolke.Char.ausrüstung.clear()
        for i in range(1,27):
            txt = eval("self.uiIt.lineEdit_" + str(i) + ".text()")
            if txt != "":
                Wolke.Char.ausrüstung.append(txt)
        #self.modified.emit() - Not needed since this is not costing any EP