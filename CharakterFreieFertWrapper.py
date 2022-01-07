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
import CharakterFreieFertigkeitenPickerWrapper

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
                ffEdit.editingFinished.connect(self.update)
                setattr(self.uiFert, "editFF" + str(self.ffCount), ffEdit)
                ffLayout.addWidget(ffEdit)
                ffCombo = QtWidgets.QComboBox()
                ffCombo.addItem("I")
                ffCombo.addItem("II")
                ffCombo.addItem("III")
                ffCombo.setFont(QtWidgets.QApplication.instance().font()) #hack to refresh font in fusion style
                ffCombo.currentIndexChanged.connect(self.update)
                if self.ffCount <= Wolke.Char.freieFertigkeitenNumKostenlos:
                    ffCombo.setEnabled(False)
                setattr(self.uiFert, "comboFF" + str(self.ffCount), ffCombo)
                ffLayout.addWidget(ffCombo)

                ffButton = QtWidgets.QPushButton()
                setattr(self.uiFert, "buttonFF" + str(self.ffCount), ffButton)
                ffButton.setText("+")
                ffButton.setMaximumSize(QtCore.QSize(25, 20))
                ffButton.clicked.connect(lambda state, edit=ffEdit: self.ffButtonClicked(edit))
                ffLayout.addWidget(ffButton)

                self.uiFert.freieFertsGrid.addLayout(ffLayout, row, column)
        
        self.load()

    def ffButtonClicked(self, edit):
        picker = CharakterFreieFertigkeitenPickerWrapper.CharakterFreieFertigkeitenPickerWrapper(edit.text())
        if picker.fertigkeit != None:
            edit.setText(picker.fertigkeit)
            self.update()
        
    def load(self):
        count = 1
        for el in Wolke.Char.freieFertigkeiten:
            #if el.name == "Muttersprache":
            #    continue
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(True)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(True)")
            getName = lambda : el.name
            eval("self.uiFert.editFF" + str(count) + ".setText(getName())")

            index = el.wert-1
            if count <= Wolke.Char.freieFertigkeitenNumKostenlos:
                index = 2
            eval("self.uiFert.comboFF" + str(count) + ".setCurrentIndex(" + str(index) + ")")
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(False)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(False)")

            count += 1
            if count > self.ffCount:
                break
        while count < self.ffCount + 1:
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(True)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(True)")
            eval("self.uiFert.editFF" + str(count) + ".setText(\"\")")
            index = 0
            if count <= Wolke.Char.freieFertigkeitenNumKostenlos:
                index = 2
            eval("self.uiFert.comboFF" + str(count) + ".setCurrentIndex(" + str(index) + ")")
            eval("self.uiFert.editFF" + str(count) + ".blockSignals(False)")
            eval("self.uiFert.comboFF" + str(count) + ".blockSignals(False)")
            count += 1
    
    def update(self):
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