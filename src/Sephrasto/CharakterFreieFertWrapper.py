# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:09:33 2017

@author: Aeolitus
"""
from Wolke import Wolke
import UI.CharakterFreieFert
from PySide6 import QtWidgets, QtCore, QtGui
import logging
from Hilfsmethoden import Hilfsmethoden
from CharakterFreieFertigkeitenPickerWrapper import CharakterFreieFertigkeitenPickerWrapper
from EventBus import EventBus
from Core.FreieFertigkeit import FreieFertigkeit, FreieFertigkeitDefinition
from functools import partial

class CharakterFreieFertWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing FreieFertWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterFreieFert.Ui_Form()
        self.ui.setupUi(self.form)

        info = Wolke.DB.einstellungen["FreieFertigkeiten: Beschreibung"].wert
        info = info.replace("$unerfahren$", str(FreieFertigkeitDefinition.steigerungskosten[1]))
        info = info.replace("$erfahren$", str(FreieFertigkeitDefinition.steigerungskosten[2]))
        info = info.replace("$meisterlich$", str(FreieFertigkeitDefinition.steigerungskosten[3]))
        self.ui.labelInfo.setText(info)

        self.ffCount = 0

        self.editFF = []
        self.comboFF = []
        self.buttonFF = []

        self.ui.scrollAreaWidgetContents.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
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
                ffCombo.currentIndexChanged.connect(self.update)
                if self.ffCount <= Wolke.Char.freieFertigkeitenNumKostenlos:
                    ffCombo.setEnabled(False)
                self.comboFF.append(ffCombo)
                ffLayout.addWidget(ffCombo)

                ffButton = QtWidgets.QPushButton()
                self.buttonFF.append(ffButton)
                ffButton.setProperty("class", "iconSmall")
                ffButton.setText('\u002b')
                font = ffButton.font()
                font.setHintingPreference(QtGui.QFont.PreferNoHinting)
                ffButton.setFont(font)
                ffButton.clicked.connect(partial(self.ffButtonClicked, edit=ffEdit))
                ffLayout.addWidget(ffButton)

                if row % 2 != 0:
                    ffEdit.setProperty("class", "alternateBase")

                self.ui.freieFertsGrid.addLayout(ffLayout, row, column)

    def ffButtonClicked(self, edit):
        pickerClass = EventBus.applyFilter("class_freiefertigkeitenpicker_wrapper", CharakterFreieFertigkeitenPickerWrapper)
        picker = pickerClass(edit.text())
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
            if count < Wolke.Char.freieFertigkeitenNumKostenlos:
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
            name = self.editFF[count].text()
            definition = None
            if name in Wolke.DB.freieFertigkeiten:
                definition = Wolke.DB.freieFertigkeiten[name]
            else:
                definition = FreieFertigkeitDefinition()
                definition.name = name
            fert = FreieFertigkeit(definition, Wolke.Char)
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