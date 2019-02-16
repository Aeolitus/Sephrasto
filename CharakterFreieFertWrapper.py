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
        
        self.ffCount = 0
        for row in range(1,8):
            for column in range(1,5):
                self.ffCount +=1
                ffLayout = QtWidgets.QHBoxLayout()
                ffEdit = QtWidgets.QLineEdit()
                ffEdit.editingFinished.connect(self.updateFreie)
                setattr(self.uiFert, "editFF" + str(self.ffCount), ffEdit)
                ffLayout.addWidget(ffEdit)
                ffCombo = QtWidgets.QComboBox()
                ffCombo.addItem("I")
                ffCombo.addItem("II")
                ffCombo.addItem("III")
                ffCombo.currentIndexChanged.connect(self.updateFreie)
                setattr(self.uiFert, "comboFF" + str(self.ffCount), ffCombo)
                ffLayout.addWidget(ffCombo)

                self.uiFert.freieFertsGrid.addLayout(ffLayout, row, column)
                
        self.uiFert.comboFF1.setEnabled(False)
        
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
            if count > self.ffCount:
                break
        while count < self.ffCount + 1:
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
        for count in range(1,self.ffCount + 1):
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