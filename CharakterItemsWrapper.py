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
        if Wolke.Debug:
            print("Initializing ItemsWrapper...")
        self.formIt = QtWidgets.QWidget()
        self.uiIt = CharakterItems.Ui_Form()
        self.uiIt.setupUi(self.formIt)
        for i in range(1,21):
            eval("self.uiIt.lineEdit_" + str(i) + ".editingFinished.connect(self.updateItems)")
        self.currentlyLoading = False

    def loadItems(self):
        self.currentlyLoading = True
        count = 1
        for el in Wolke.Char.ausrüstung:
            getName = lambda : el
            eval("self.uiIt.lineEdit_" + str(count) + ".setText(getName())")
            count += 1
            if count > 20:
                break
#==============================================================================
#         while count <= 20:
#             eval("self.uiIt.lineEdit_" + str(count) + ".clear()")
#             count += 1
#==============================================================================
        self.currentlyLoading = False
    
    def updateItems(self):
        if not self.currentlyLoading:
            Wolke.Char.ausrüstung.clear()
            for i in range(1,21):
                txt = eval("self.uiIt.lineEdit_" + str(i) + ".text()")
                #if txt != "":
                Wolke.Char.ausrüstung.append(txt)