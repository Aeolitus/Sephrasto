# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:29:39 2017

@author: Aeolitus
"""
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import Fertigkeiten
import Datenbank
import DatenbankMain
import DatenbankEditFertigkeitWrapper
import DatenbankEditTalentWrapper
import DatenbankEditVorteilWrapper
import DatenbankSelectTypeWrapper

class DatenbankEdit(object):
    def __init__(self):
        super().__init__()
        self.datenbank = Datenbank.Datenbank()
        self.app = QtCore.QCoreApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = DatenbankMain.Ui_Form()
        self.ui.setupUi(self.Form)
        
        # GUI Mods
        self.model = QtGui.QStandardItemModel(self.ui.listDatenbank)
        self.ui.listDatenbank.setModel(self.model)
        self.ui.listDatenbank.doubleClicked.connect(self.listItemEvent)
        self.ui.showTalente.stateChanged.connect(self.updateGUI)
        self.ui.showVorteile.stateChanged.connect(self.updateGUI)
        self.ui.showFertigkeiten.stateChanged.connect(self.updateGUI)
        self.ui.showUebernatuerlicheFertigkeiten.stateChanged.connect(self.updateGUI)
        self.ui.buttonLoadDB.clicked.connect(self.loadDatenbank)
        self.ui.buttonSaveDB.clicked.connect(self.saveDatenbank)
        self.ui.buttonEditieren.clicked.connect(self.editSelected)
        self.ui.buttonLoeschen.clicked.connect(self.deleteSelected)
        self.ui.buttonHinzufuegen.clicked.connect(self.hinzufuegen)
        self.updateGUI()
        
        self.Form.show()
        self.app.exec_()
        
    def updateGUI(self):
        self.model.clear()
        if self.ui.showTalente.isChecked():
            for itm in self.datenbank.talente:
                item = QtGui.QStandardItem(itm + " : Talent")
                item.setEditable(False)
                self.model.appendRow(item)
        if self.ui.showVorteile.isChecked():
            for itm in self.datenbank.vorteile:
                item = QtGui.QStandardItem(itm + " : Vorteil")
                item.setEditable(False)
                self.model.appendRow(item) 
        if self.ui.showFertigkeiten.isChecked():
            for itm in self.datenbank.fertigkeiten:
                item = QtGui.QStandardItem(itm + " : Fertigkeit")
                item.setEditable(False)
                self.model.appendRow(item) 
        if self.ui.showUebernatuerlicheFertigkeiten.isChecked():
            for itm in self.datenbank.übernatürlicheFertigkeiten:
                item = QtGui.QStandardItem(itm + " : Übernatürliche Fertigkeit")
                item.setEditable(False)
                self.model.appendRow(item) 
        self.ui.listDatenbank.setModel(self.model)
               
    @QtCore.pyqtSlot("QModelIndex")   
    def listItemEvent(self, item):
        tmp = self.model.itemData(item)[0].split(" : ")
        if tmp[1] == "Talent":
            nameSt = self.datenbank.talente[tmp[0]].name
            tal = self.editTalent(self.datenbank.talente[tmp[0]])
            if tal is not None:
                self.datenbank.talente.pop(nameSt,None)
                self.datenbank.talente.update({tal.name: tal})
                self.updateGUI()
        elif tmp[1] == "Vorteil":
            nameSt = self.datenbank.vorteile[tmp[0]].name
            vor = self.editVorteil(self.datenbank.vorteile[tmp[0]])
            if vor is not None:
                self.datenbank.vorteile.pop(nameSt,None)
                self.datenbank.vorteile.update({vor.name: vor})
                self.updateGUI()
        elif tmp[1] == "Fertigkeit":
            nameSt = self.datenbank.fertigkeiten[tmp[0]].name
            fer = self.editFertigkeit(self.datenbank.fertigkeiten[tmp[0]])
            if fer is not None:
                self.datenbank.fertigkeiten.pop(nameSt,None)
                self.datenbank.fertigkeiten.update({fer.name: fer})
                self.updateGUI()
        elif tmp[1] == "Übernatürliche Fertigkeit":
            nameSt = self.datenbank.übernatürlicheFertigkeiten[tmp[0]].name
            fer = self.editUebernatuerlich(self.datenbank.übernatürlicheFertigkeiten[tmp[0]])
            if fer is not None:
                self.datenbank.übernatürlicheFertigkeiten.pop(nameSt,None)
                self.datenbank.übernatürlicheFertigkeiten.update({fer.name: fer})
                self.updateGUI()
    
    def hinzufuegen(self):
        '''
        Lässt den Nutzer einen neuen Eintrag in die Datenbank einfügen.
        Öffnet zunächst den DatenbankSelectType-Dialog, welcher den 
        Nutzer fragt, was für ein Eintrag angelegt werden soll. 
        Akzeptiert der Nutzer, wird seiner Auswahl nach ein Dialog zum
        Erstellen des Eintrages geöffnet.
        '''
        dbS = DatenbankSelectTypeWrapper.DatenbankSelectTypeWrapper()
        if dbS.entryType is not None:
            if dbS.entryType is "Talent":
                self.addTalent()
            elif dbS.entryType is "Vorteil":
                self.addVorteil()
            elif dbS.entryType is "Fertigkeit":
                self.addFertigkeit()
            else:
                self.addUebernatuerlich()
        
    def addTalent(self):
        tal = Fertigkeiten.Talent()
        ret = self.editTalent(tal)
        if ret is not None:
            self.datenbank.talente.update({ret.name: ret})
            self.updateGUI();
                          
    def addVorteil(self):
        vor = Fertigkeiten.Vorteil()
        ret = self.editVorteil(vor)
        if ret is not None:
            self.datenbank.vorteile.update({ret.name: ret})
            self.updateGUI();
                          
    def addFertigkeit(self):
        fer = Fertigkeiten.Fertigkeit()
        ret = self.editFertigkeit(fer)
        if ret is not None:
            self.datenbank.fertigkeiten.update({ret.name: ret})
            self.updateGUI();
                          
    def addUebernatuerlich(self):
        fer = Fertigkeiten.Fertigkeit()
        ret = self.editUebernatuerlich(fer)
        if ret is not None:
            self.datenbank.übernatürlicheFertigkeiten.update({ret.name: ret})
            self.updateGUI();
                          
    def editTalent(self, inp):
        dbT = DatenbankEditTalentWrapper.DatenbankEditTalentWrapper(inp)
        return dbT.talent

    def editVorteil(self, inp):
        dbV = DatenbankEditVorteilWrapper.DatenbankEditVorteilWrapper(inp)
        return dbV.vorteil

    def editFertigkeit(self, inp):
        dbF = DatenbankEditFertigkeitWrapper.DatenbankEditFertigkeitWrapper(inp, False)
        return dbF.fertigkeit

    def editUebernatuerlich(self, inp):
        dbU = DatenbankEditFertigkeitWrapper.DatenbankEditFertigkeitWrapper(inp, True)
        return dbU.fertigkeit
        
    def editSelected(self):
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] == "Talent":
                tal = self.datenbank.talente[tmp[0]]
                if tal is not None:
                    ret = self.editTalent(tal)
                    if ret is not None:
                        self.datenbank.talente.pop(tmp[0],None)
                        self.datenbank.talente.update({ret.name: ret})
                        self.updateGUI();
            elif tmp[1] == "Vorteil":
                tal = self.datenbank.vorteile[tmp[0]]
                if tal is not None:
                    ret = self.editVorteil(tal)
                    if ret is not None:
                        self.datenbank.vorteile.pop(tmp[0],None)
                        self.datenbank.vorteile.update({ret.name: ret})
                        self.updateGUI();
            elif tmp[1] == "Fertigkeit":
                tal = self.datenbank.fertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editFertigkeit(tal)
                    if ret is not None:
                        self.datenbank.fertigkeiten.pop(tmp[0],None)
                        self.datenbank.fertigkeiten.update({ret.name: ret})
                        self.updateGUI();
            elif tmp[1] == "Übernatürliche Fertigkeit":
                tal = self.datenbank.übernatürlicheFertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editUebernatuerlich(tal)
                    if ret is not None:
                        self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                        self.datenbank.übernatürlicheFertigkeiten.update({ret.name: ret})
                        self.updateGUI();
                                
    def deleteSelected(self):
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] == "Talent":
                self.datenbank.talente.pop(tmp[0],None)
                self.updateGUI();
            elif tmp[1] == "Vorteil":
                self.datenbank.vorteile.pop(tmp[0],None)
                self.updateGUI();
            elif tmp[1] == "Fertigkeit":
                self.datenbank.fertigkeiten.pop(tmp[0],None)
                self.updateGUI();
            elif tmp[1] == "Übernatürliche Fertigkeit":
                self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                self.updateGUI();
                              
    def saveDatenbank(self):
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Datenbank speichern...","","XML-Datei (*.xml)")
        if ".xml" not in spath:
            spath = spath + ".xml"
        self.datenbank.datei = spath
        self.datenbank.xmlSchreiben()
        
    def loadDatenbank(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Datenbank laden...","","XML-Datei (*.xml)")
        self.datenbank.datei = spath
        self.datenbank.xmlLaden()
        self.updateGUI()
        
if __name__ == "__main__":
    D = DatenbankEdit()