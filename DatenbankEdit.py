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
import DatenbankEditWaffeWrapper
import DatenbankEditManoeverWrapper
import Objekte
import os

class DatenbankEdit(object):
    def __init__(self):
        super().__init__()
        self.datenbank = Datenbank.Datenbank()
        self.savepath = self.datenbank.datei
        self.changed = False
        self.windowTitleDefault = ""
    
    def setupGUI(self):
        # GUI Mods
        self.model = QtGui.QStandardItemModel(self.ui.listDatenbank)
        self.ui.listDatenbank.setModel(self.model)
        self.ui.listDatenbank.doubleClicked["QModelIndex"].connect(self.editSelected)
        self.ui.listDatenbank.selectionModel().selectionChanged.connect(self.listSelectionChanged)
        self.ui.showTalente.stateChanged.connect(self.updateGUI)
        self.ui.showVorteile.stateChanged.connect(self.updateGUI)
        self.ui.showFertigkeiten.stateChanged.connect(self.updateGUI)
        self.ui.showUebernatuerlicheFertigkeiten.stateChanged.connect(self.updateGUI)
        self.ui.showWaffen.stateChanged.connect(self.updateGUI)
        self.ui.showManoever.stateChanged.connect(self.updateGUI)
        self.ui.buttonLoadDB.clicked.connect(self.loadDatenbank)
        self.ui.buttonSaveDB.clicked.connect(self.saveDatenbank)
        self.ui.buttonQuicksave.clicked.connect(self.quicksaveDatenbank)
        self.ui.buttonEditieren.clicked.connect(self.editSelected)
        self.ui.buttonEditieren.setEnabled(False)
        self.ui.buttonLoeschen.clicked.connect(self.deleteSelected)
        self.ui.buttonLoeschen.setEnabled(False)
        self.ui.buttonHinzufuegen.clicked.connect(self.hinzufuegen)
        self.ui.buttonWiederherstellen.clicked.connect(self.wiederherstellen)

        self.Form.closeEvent = self.closeEvent
        self.windowTitleDefault = self.Form.windowTitle()
        self.updateGUI()
        self.updateWindowTitle()
    
    def listSelectionChanged(self):
        indexes = self.ui.listDatenbank.selectedIndexes()
        if len(indexes) > 1:
            raise Exception('There really shouldn\'t be more than one item selectable...') 
        if not indexes:
            self.ui.buttonEditieren.setEnabled(False)
            self.ui.buttonLoeschen.setEnabled(False)
            self.ui.buttonLoeschen.setVisible(True)
            self.ui.buttonWiederherstellen.setVisible(False)
            return
        item = self.model.itemData(indexes[0])[0]
        if item.endswith(" (gelöscht)"):
            self.ui.buttonEditieren.setEnabled(False)
            self.ui.buttonLoeschen.setVisible(False)
            self.ui.buttonWiederherstellen.setVisible(True)
        else:
            self.ui.buttonEditieren.setEnabled(True)
            self.ui.buttonLoeschen.setEnabled(True)
            self.ui.buttonLoeschen.setVisible(True)
            self.ui.buttonWiederherstellen.setVisible(False)


    def cancelDueToPendingChanges(self, action):
        if self.changed:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle(action)
            messagebox.setText("Sollen die ausstehenden Änderungen gespeichert werden?")
            messagebox.setIcon(QtWidgets.QMessageBox.Question)
            messagebox.addButton(QtWidgets.QPushButton("Ja"), QtWidgets.QMessageBox.YesRole)
            messagebox.addButton(QtWidgets.QPushButton("Nein"), QtWidgets.QMessageBox.NoRole)
            messagebox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.RejectRole)
            result = messagebox.exec_()
            if result == 0:
                self.quicksaveDatenbank()
            elif result == 2:
                return True
        return False

    def closeEvent(self,event):
        if self.cancelDueToPendingChanges("Beenden"):
            event.ignore()

    def onDatabaseChange(self):
        self.changed = True
        self.updateGUI()
    
    def updateWindowTitle(self):
        splitpath = os.path.split(self.savepath)
        self.Form.setWindowTitle(self.windowTitleDefault + " (" + splitpath[-1] + ")")

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
        if self.ui.showWaffen.isChecked():
            for itm in self.datenbank.waffen:
                item = QtGui.QStandardItem(itm + " : Waffe")
                item.setEditable(False)
                self.model.appendRow(item) 
        if self.ui.showManoever.isChecked():
            for itm in self.datenbank.manöver:
                item = QtGui.QStandardItem(itm + " : Manöver / Modifikation")
                item.setEditable(False)
                self.model.appendRow(item)

        for itm in self.datenbank.removeList:
            item = QtGui.QStandardItem(itm[0] + " : "  + itm[1] + " (gelöscht)")
            item.setEditable(False)
            item.setBackground(QtGui.QBrush(QtCore.Qt.red))
            self.model.appendRow(item)
        self.ui.listDatenbank.setModel(self.model)
               
    def wiederherstellen(self):
        indexes = self.ui.listDatenbank.selectedIndexes()
        if len(indexes) > 1:
            raise Exception('There really shouldn\'t be more than one item selectable...') 
        if not indexes:
            raise Exception('This button shouldnt be visible...') 
        item = self.model.itemData(indexes[0])[0]
        if not item.endswith(" (gelöscht)"):
            raise Exception('This button shouldnt be visible...')
        item = item[:-11]
        tmp = item.split(" : ")

        removed = [item for item in self.datenbank.removeList if item[0] == tmp[0] and item[1] == tmp[1]][0]
        if not removed:
            raise Exception('State corrupted.')

        exists = False
        if tmp[1] == "Talent":
            if tmp[0] in self.datenbank.talente:
                exists = True
            else:
                self.datenbank.talente.update({tmp[0]: removed[2]})
        elif tmp[1] == "Vorteil":
            if tmp[0] in self.datenbank.vorteile:
                exists = True
            else:
                self.datenbank.vorteile.update({tmp[0]: removed[2]})
        elif tmp[1] == "Fertigkeit":
            if tmp[0] in self.datenbank.fertigkeiten:
                exists = True
            else:
                self.datenbank.fertigkeiten.update({tmp[0]: removed[2]})
        elif tmp[1] == "Übernatürliche Fertigkeit":
            if tmp[0] in self.datenbank.übernatürlicheFertigkeiten:
                exists = True
            else:
                self.datenbank.übernatürlicheFertigkeiten.update({tmp[0]: removed[2]})
        elif tmp[1] == "Waffe":
            if tmp[0] in self.datenbank.waffen:
                exists = True
            else:
                self.datenbank.waffen.update({tmp[0]: removed[2]})
        elif tmp[1] == "Manöver / Modifikation":
            if tmp[0] in self.datenbank.manöver:
                exists = True
            else:
                self.datenbank.manöver.update({tmp[0]: removed[2]})
        else:
            raise Exception('Unknown category.')

        if exists:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setWindowTitle('Wiederherstellen nicht möglich!')
            messageBox.setText('Es existiert bereits ein(e) ' + tmp[1] + ' mit dem Namen "' + tmp[0] + '"')            
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec_()
            return
        self.datenbank.removeList.remove(removed)
        self.onDatabaseChange();
    
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
            elif dbS.entryType is "Uebernatuerlich":
                self.addUebernatuerlich()
            elif dbS.entryType is "Manoever":
                self.addManoever()
            else:
                self.addWaffe()
        
    def addTalent(self):
        tal = Fertigkeiten.Talent()
        ret = self.editTalent(tal)
        if ret is not None:
            self.datenbank.talente.update({ret.name: ret})
            self.onDatabaseChange()
                          
    def addVorteil(self):
        vor = Fertigkeiten.Vorteil()
        ret = self.editVorteil(vor)
        if ret is not None:
            self.datenbank.vorteile.update({ret.name: ret})
            self.onDatabaseChange()
                          
    def addFertigkeit(self):
        fer = Fertigkeiten.Fertigkeit()
        ret = self.editFertigkeit(fer)
        if ret is not None:
            self.datenbank.fertigkeiten.update({ret.name: ret})
            self.onDatabaseChange()
                          
    def addUebernatuerlich(self):
        fer = Fertigkeiten.Fertigkeit()
        ret = self.editUebernatuerlich(fer)
        if ret is not None:
            self.datenbank.übernatürlicheFertigkeiten.update({ret.name: ret})
            self.onDatabaseChange()
                          
    def addWaffe(self):
        waf = Objekte.Nahkampfwaffe()
        ret = self.editWaffe(waf)
        if ret is not None:
            self.datenbank.waffen.update({ret.name: ret})
            self.onDatabaseChange()
    
    def addManoever(self):
        man = Fertigkeiten.Manoever()
        ret = self.editManoever(man)
        if ret is not None:
            self.datenbank.manöver.update({ret.name: ret})
            self.onDatabaseChange()
                          
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
    
    def editWaffe(self, inp):
        dbW = DatenbankEditWaffeWrapper.DatenbankEditWaffeWrapper(self.datenbank, inp)
        return dbW.waffe
        
    def editManoever(self, inp):
        dbM = DatenbankEditManoeverWrapper.DatenbankEditManoeverWrapper(inp)
        return dbM.man
        
    def editSelected(self):
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] == "Talent":
                tal = self.datenbank.talente[tmp[0]]
                if tal is not None:
                    ret = self.editTalent(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.talente.pop(tmp[0],None)
                        self.datenbank.talente.update({ret.name: ret})
                        self.onDatabaseChange()
            elif tmp[1] == "Vorteil":
                tal = self.datenbank.vorteile[tmp[0]]
                if tal is not None:
                    ret = self.editVorteil(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.vorteile.pop(tmp[0],None)
                        self.datenbank.vorteile.update({ret.name: ret})
                        self.onDatabaseChange()
            elif tmp[1] == "Fertigkeit":
                tal = self.datenbank.fertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editFertigkeit(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.fertigkeiten.pop(tmp[0],None)
                        self.datenbank.fertigkeiten.update({ret.name: ret})
                        self.onDatabaseChange()
            elif tmp[1] == "Übernatürliche Fertigkeit":
                tal = self.datenbank.übernatürlicheFertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editUebernatuerlich(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                        self.datenbank.übernatürlicheFertigkeiten.update({ret.name: ret})
                        self.onDatabaseChange()
            elif tmp[1] == "Waffe":
                tal = self.datenbank.waffen[tmp[0]]
                if tal is not None:
                    ret = self.editWaffe(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.waffen.pop(tmp[0],None)
                        self.datenbank.waffen.update({ret.name: ret})
                        self.onDatabaseChange()
            elif tmp[1] == "Manöver / Modifikation":
                tal = self.datenbank.manöver[tmp[0]]
                if tal is not None:
                    ret = self.editManoever(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.manöver.pop(tmp[0],None)
                        self.datenbank.manöver.update({ret.name: ret})
                        self.onDatabaseChange()
                                
    def deleteSelected(self):
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] == "Talent":
                t = self.datenbank.talente[tmp[0]]
                if not t.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], t))
                self.datenbank.talente.pop(tmp[0],None)
                self.onDatabaseChange()
            elif tmp[1] == "Vorteil":
                v = self.datenbank.vorteile[tmp[0]]
                if not v.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], v))
                self.datenbank.vorteile.pop(tmp[0],None)
                self.onDatabaseChange()
            elif tmp[1] == "Fertigkeit":
                f = self.datenbank.fertigkeiten[tmp[0]]
                if not f.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], f))
                self.datenbank.fertigkeiten.pop(tmp[0],None)
                self.onDatabaseChange()
            elif tmp[1] == "Übernatürliche Fertigkeit":
                f = self.datenbank.übernatürlicheFertigkeiten[tmp[0]]
                if not f.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], f))
                self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                self.onDatabaseChange()
            elif tmp[1] == "Waffe":
                w = self.datenbank.waffen[tmp[0]]
                if not w.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], w))
                self.datenbank.waffen.pop(tmp[0],None)
                self.onDatabaseChange()
            elif tmp[1] == "Manöver / Modifikation":
                m = self.datenbank.manöver[tmp[0]]
                if not m.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], m))
                self.datenbank.manöver.pop(tmp[0],None)
                self.onDatabaseChange()
                              
    def saveDatenbank(self):
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"User Datenbank speichern...","","XML-Datei (*.xml)")
        spath = os.path.realpath(spath)
        refDatabaseFile = os.getcwd() + "\\datenbank.xml"

        if not spath.endswith(".xml"):
            spath = spath + ".xml"
        if spath == refDatabaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Überschreiben der zentralen Datenbank verhindert!")
            infoBox.setInformativeText("Bitte schreibe deine eigenen Regeln nicht mit in die zentrale datenbank.xml - \
diese wird bei vielen Updates von Sephrasto verändert, wodurch du deine Regeln \
verlieren würdest. Stattdessen kannst du die datenbank_user.xml verwenden, die \
automatisch beim Programmstart mit geladen wird. Änderungen darin überschreiben \
die datenbank.xml, aber bleiben bei Updates erhalten! Auch andere Dateien sind \
in Ordnung, werden aber nicht von Sephrasto geladen.")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
            self.saveDatenbank()
        else:
            self.savepath = spath
            self.quicksaveDatenbank()
            self.updateWindowTitle()
        
    def quicksaveDatenbank(self):
        refDatabaseFile = os.getcwd() + "\\datenbank.xml"
        if self.savepath == refDatabaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Überschreiben der zentralen Datenbank verhindert!")
            infoBox.setInformativeText("Bitte schreibe deine eigenen Regeln nicht mit in die zentrale datenbank.xml - \
diese wird bei vielen Updates von Sephrasto verändert, wodurch du deine Regeln \
verlieren würdest. Stattdessen kannst du die datenbank_user.xml verwenden, die \
automatisch beim Programmstart mit geladen wird. Änderungen darin überschreiben \
die datenbank.xml, aber bleiben bei Updates erhalten! Auch andere Dateien sind \
in Ordnung, werden aber nicht von Sephrasto geladen.")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
        else:
            self.datenbank.datei = self.savepath
            self.datenbank.xmlSchreiben()
            self.changed = False
        
    def loadDatenbank(self):
        if self.cancelDueToPendingChanges("Andere Datenbank laden"):
            return
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"User Datenbank laden...","","XML-Datei (*.xml)")
        if not spath:
            return
        spath = os.path.realpath(spath)
        databaseFile = os.getcwd() + "\\datenbank.xml"
        if spath == databaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Diese Funktion dient dem Laden einer Nutzer-Datenbank wie der 'database_user.xml'. Die zentrale Sephrasto-Datenbank 'database.xml' wird sowieso immer geladen!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
            self.loadDatenbank()
            return
        self.savepath = spath
        self.datenbank.datei = spath
        self.datenbank.xmlLaden()
        self.updateGUI()
        self.updateWindowTitle()
        
if __name__ == "__main__":
    D = DatenbankEdit()
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    D.Form = QtWidgets.QWidget()
    D.ui = DatenbankMain.Ui_Form()
    D.ui.setupUi(D.Form)
    D.setupGUI()
    D.Form.show()
    app.exec_()