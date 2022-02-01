# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:53:43 2017

@author: Aeolitus
"""
from Wolke import Wolke
import UI.CharakterItems
from PyQt5 import QtWidgets, QtCore
import logging
from Hilfsmethoden import Hilfsmethoden

class CharakterItemsWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing ItemsWrapper...")
        self.formIt = QtWidgets.QWidget()
        self.uiIt = UI.CharakterItems.Ui_Form()
        self.uiIt.setupUi(self.formIt)
        self.lineEdits = []
        for i in range(0,20):
            lineEdit = getattr(self.uiIt, "lineEdit_"+ str(i+1))
            lineEdit.editingFinished.connect(self.update)
            self.lineEdits.append(lineEdit)
        self.currentlyLoading = False

    def load(self):
        self.currentlyLoading = True
        count = 0
        for el in Wolke.Char.ausrüstung:
            self.lineEdits[count].setText(el)
            count += 1
            if count >= 20:
                break
        self.currentlyLoading = False
    
    def update(self):
        if self.currentlyLoading:
            return
        ausruestungNeu = []
        for i in range(0,20):
            ausruestungNeu.append(self.lineEdits[i].text())

        #Preserve the position of actual elements but remove any trailing empty elements
        #This is needed for ArrayEqual later to work as intended
        for ausr in reversed(ausruestungNeu):
            if ausr == "":
                ausruestungNeu.pop()
            else:
                break

        if not Hilfsmethoden.ArrayEqual(ausruestungNeu, Wolke.Char.ausrüstung):
            Wolke.Char.ausrüstung = ausruestungNeu
            self.modified.emit()