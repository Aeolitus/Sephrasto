# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:09:33 2017

@author: Aeolitus
"""
import Fertigkeiten
from Wolke import Wolke
import CharakterFreieFert
from PyQt5 import QtWidgets, QtCore
import logging
from Hilfsmethoden import Hilfsmethoden

class CharakterFreieFertWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing FreieFertWrapper...")
        self.formFert = QtWidgets.QWidget()
        self.uiFert = CharakterFreieFert.Ui_Form()
        self.uiFert.setupUi(self.formFert)
        
        for count in range(1,13):
            eval("self.uiFert.editFF" + str(count) + ".editingFinished.connect(self.updateFreie)")
            eval("self.uiFert.comboFF" + str(count) + ".currentIndexChanged.connect(self.updateFreie)")
        
        self.loadFreie()
        
    def loadFreie(self):
        count = 1
        for el in Wolke.Char.freieFertigkeiten:
            #if el.name == "Muttersprache":
            #    continue
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(True)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(True)")
            getName = lambda : el.name
            eval("self.uiFert.editFF" + str(count) + ".setText(getName())")
            eval("self.uiFert.comboFF" + str(count) + ".setCurrentIndex(" + str(el.wert-1) + ")")
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(False)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(False)")
            count += 1
            if count > 12:
                break
        while count < 13:
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(True)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(True)")
            eval("self.uiFert.editFF" + str(count) + ".setText(\"\")")
            eval("self.uiFert.comboFF" + str(count) + ".setCurrentIndex(0)")
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(False)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(False)")
            count += 1
            
        self.uiFert.comboFF1.blockSignals(True)
        self.uiFert.comboFF1.setCurrentIndex(2)
        self.uiFert.comboFF1.blockSignals(False)
    
    def updateFreie(self):
        freieNeu = []
        for count in range(1,13):
            tmp = eval("self.uiFert.editFF" + str(count) + ".text()")
            val = eval("self.uiFert.comboFF" + str(count) + ".currentIndex()")+1
            fert = Fertigkeiten.FreieFertigkeit()
            fert.name = tmp
            fert.wert = val
            freieNeu.append(fert)

        #Preserve the position of actual elements but remove any trailing empty elements
        #This is needed for ArrayEqual later to work as intended
        for frei in reversed(freieNeu):
            if frei.name == "":
                freieNeu.pop()
            else:
                break

        if not Hilfsmethoden.ArrayEqual(freieNeu, Wolke.Char.freieFertigkeiten):
            Wolke.Char.freieFertigkeiten = freieNeu
            self.modified.emit()