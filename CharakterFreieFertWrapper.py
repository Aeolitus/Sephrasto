# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:09:33 2017

@author: Aeolitus
"""
import Fertigkeiten
from Wolke import Wolke
import CharakterFreieFert
from PyQt5 import QtWidgets, QtCore

class CharakterFreieFertWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.formFert = QtWidgets.QWidget()
        self.uiFert = CharakterFreieFert.Ui_Form()
        self.uiFert.setupUi(self.formFert)
        
        for count in range(1,13):
            eval("self.uiFert.editFF" + str(count) + ".editingFinished.connect(self.changedEntry)")
            eval("self.uiFert.comboFF" + str(count) + ".currentIndexChanged.connect(self.changedEntry)")
        
        self.loadFreie()
        
    def loadFreie(self):
        count = 1
        for el in Wolke.Char.freieFertigkeiten:
            if el.name == "Muttersprache":
                count += 1
                continue
            eval("self.uiFert.editFF" + str(count) + ".setText(\"" + el.name + "\")")
            eval("self.uiFert.comboFF" + str(count) + ".setCurrentIndex(" + str(el.wert-1) + ")")
            count += 1
            if count > 12:
                break
    
    def updateFreie(self):
        Wolke.Char.freieFertigkeiten.clear()
        for count in range(1,13):
            tmp = eval("self.uiFert.editFF" + str(count) + ".text()")
            if tmp != "":
                fert = Fertigkeiten.FreieFertigkeit()
                fert.name = tmp
                fert.wert = eval("self.uiFert.comboFF" + str(count) + ".currentIndex()")+1
                Wolke.Char.freieFertigkeiten.append(fert)
        self.modified.emit()
        
    def changedEntry(self):
        self.updateFreie()
        self.modified.emit()