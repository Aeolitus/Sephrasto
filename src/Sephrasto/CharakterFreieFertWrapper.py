# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:09:33 2017

@author: Aeolitus
"""
import Fertigkeiten
from Wolke import Wolke
import UI.CharakterFreieFert
from PyQt5 import QtWidgets, QtCore, QtGui
import logging
from Hilfsmethoden import Hilfsmethoden
import CharakterFreieFertigkeitenPickerWrapper

class CharakterFreieFertWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing FreieFertWrapper...")
        self.formFert = QtWidgets.QWidget()
        self.uiFert = UI.CharakterFreieFert.Ui_Form()
        self.uiFert.setupUi(self.formFert)

        kosten = [str(Wolke.DB.einstellungen["FreieFertigkeiten: Kosten Stufe1"].toInt()),
                  str(Wolke.DB.einstellungen["FreieFertigkeiten: Kosten Stufe2"].toInt()),
                  str(Wolke.DB.einstellungen["FreieFertigkeiten: Kosten Stufe3"].toInt())]
        self.uiFert.labelRegeln.setText(self.uiFert.labelRegeln.text() +
                                        " Sie kosten jeweils " + kosten[0] + "/" + kosten[1] + "/" + kosten[2] + " EP.")

        self.ffCount = 0

        self.editFF = []
        self.comboFF = []
        self.buttonFF = []
        font = QtGui.QFont("Times", QtWidgets.QApplication.instance().font().pointSize()) # serif font for the roman letters
        for row in range(0,7):
            for column in range(0,4):
                self.ffCount +=1
                ffLayout = QtWidgets.QHBoxLayout()
                ffEdit = QtWidgets.QLineEdit()
                ffEdit.editingFinished.connect(self.update)
                self.editFF.append(ffEdit)
                ffLayout.addWidget(ffEdit)
                ffCombo = QtWidgets.QComboBox()

                ffCombo.addItem("I")
                ffCombo.addItem("II")
                ffCombo.addItem("III")
                ffCombo.setFont(font)
                ffCombo.currentIndexChanged.connect(self.update)
                if self.ffCount <= Wolke.Char.freieFertigkeitenNumKostenlos:
                    ffCombo.setEnabled(False)
                self.comboFF.append(ffCombo)
                ffLayout.addWidget(ffCombo)

                ffButton = QtWidgets.QPushButton()
                self.buttonFF.append(ffButton)
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
        count = 0
        for el in Wolke.Char.freieFertigkeiten:
            self.editFF[count].blockSignals(True)
            self.comboFF[count].blockSignals(True)
            self.editFF[count].setText(el.name)

            index = el.wert-1
            if count <= Wolke.Char.freieFertigkeitenNumKostenlos:
                index = 2
            self.comboFF[count].setCurrentIndex(index)
            self.editFF[count].blockSignals(False)
            self.comboFF[count].blockSignals(False)

            count += 1
            if count >= self.ffCount:
                break
        while count < self.ffCount:
            self.editFF[count].blockSignals(True)
            self.comboFF[count].blockSignals(True)
            self.editFF[count].setText("")
            index = 0
            if count < Wolke.Char.freieFertigkeitenNumKostenlos:
                index = 2
            self.comboFF[count].setCurrentIndex(index)
            self.editFF[count].blockSignals(False)
            self.comboFF[count].blockSignals(False)
            count += 1
    
    def update(self):
        freieNeu = []
        for count in range(0,self.ffCount):
            fert = Fertigkeiten.FreieFertigkeit()
            fert.name = self.editFF[count].text()
            fert.wert = self.comboFF[count].currentIndex()+1
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