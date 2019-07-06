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
import DatenbankEditWaffeneigenschaftWrapper
import DatenbankEditWaffeWrapper
import DatenbankEditManoeverWrapper
import Objekte
import os
from Wolke import Wolke

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
        self.ui.listDatenbank.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ui.listDatenbank.selectionModel().selectionChanged.connect(self.listSelectionChanged)
        self.ui.showTalente.stateChanged.connect(self.updateGUI)
        self.ui.showVorteile.stateChanged.connect(self.updateGUI)
        self.ui.showFertigkeiten.stateChanged.connect(self.updateGUI)
        self.ui.showUebernatuerlicheFertigkeiten.stateChanged.connect(self.updateGUI)
        self.ui.showWaffeneigenschaften.stateChanged.connect(self.updateGUI)
        self.ui.showWaffen.stateChanged.connect(self.updateGUI)
        self.ui.showManoever.stateChanged.connect(self.updateGUI)
        self.ui.showUserAdded.stateChanged.connect(self.updateGUI)
        self.ui.showDeleted.stateChanged.connect(self.updateGUI)
        self.ui.nameFilterEdit.textChanged.connect(self.updateGUI)
        self.ui.buttonCloseDB.clicked.connect(self.closeDatenbank)
        self.ui.buttonLoadDB.clicked.connect(self.loadDatenbank)
        self.ui.buttonSaveDB.clicked.connect(self.saveDatenbank)
        self.ui.buttonQuicksave.clicked.connect(self.quicksaveDatenbank)
        self.ui.buttonEditieren.clicked.connect(self.editSelected)
        self.ui.buttonEditieren.setEnabled(False)
        self.ui.buttonLoeschen.clicked.connect(self.deleteSelected)
        self.ui.buttonLoeschen.setEnabled(False)
        self.ui.buttonLoeschen.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
        self.ui.buttonHinzufuegen.clicked.connect(self.hinzufuegen)
        self.ui.buttonWiederherstellen.clicked.connect(self.wiederherstellen)

        self.Form.closeEvent = self.closeEvent
        self.windowTitleDefault = self.Form.windowTitle()
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
    
    def listSelectionChanged(self):
        indexes = self.ui.listDatenbank.selectedIndexes()
        if not indexes:
            self.ui.buttonEditieren.setEnabled(False)
            self.ui.buttonLoeschen.setEnabled(False)
            self.ui.buttonLoeschen.setVisible(True)
            self.ui.buttonWiederherstellen.setVisible(False)
            return
        item = self.model.itemData(indexes[0])[0]
        if item.endswith(" (gelöscht)"):
            self.ui.buttonEditieren.setEnabled(True)
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
    
    def updateWindowTitleAndCloseButton(self):
        splitpath = self.savepath and os.path.split(self.savepath) or ["keine Nutzer-DB geladen"]
        self.Form.setWindowTitle(self.windowTitleDefault + " (" + splitpath[-1] + ")")
        self.ui.buttonCloseDB.setEnabled(self.savepath and True or False)

    def updateGUI(self):

        self.model.clear()
        showUserAdded = self.ui.showUserAdded.isChecked()
        if self.ui.showTalente.isChecked():
            for itm, value in self.datenbank.talente.items():
                if not value.isUserAdded and showUserAdded:
                    continue
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                    continue
                item = QtGui.QStandardItem(itm + " : Talent")
                item.setEditable(False)
                if value.isUserAdded:
                    item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                self.model.appendRow(item)
        if self.ui.showVorteile.isChecked():
            for itm, value in self.datenbank.vorteile.items():
                if not value.isUserAdded and showUserAdded:
                    continue
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                    continue
                item = QtGui.QStandardItem(itm + " : Vorteil")
                item.setEditable(False)
                if value.isUserAdded:
                    item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                self.model.appendRow(item) 
        if self.ui.showFertigkeiten.isChecked():
            for itm, value in self.datenbank.fertigkeiten.items():
                if not value.isUserAdded and showUserAdded:
                    continue
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                    continue
                item = QtGui.QStandardItem(itm + " : Fertigkeit")
                item.setEditable(False)
                if value.isUserAdded:
                    item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                self.model.appendRow(item) 
        if self.ui.showUebernatuerlicheFertigkeiten.isChecked():
            for itm, value in self.datenbank.übernatürlicheFertigkeiten.items():
                if not value.isUserAdded and showUserAdded:
                    continue
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                    continue
                item = QtGui.QStandardItem(itm + " : Übernatürliche Fertigkeit")
                item.setEditable(False)
                if value.isUserAdded:
                    item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                self.model.appendRow(item) 
        if self.ui.showWaffeneigenschaften.isChecked():
            for itm, value in self.datenbank.waffeneigenschaften.items():
                if not value.isUserAdded and showUserAdded:
                    continue
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                    continue
                item = QtGui.QStandardItem(itm + " : Waffeneigenschaft")
                item.setEditable(False)
                if value.isUserAdded:
                    item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                self.model.appendRow(item) 
        if self.ui.showWaffen.isChecked():
            for itm, value in self.datenbank.waffen.items():
                if not value.isUserAdded and showUserAdded:
                    continue
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                    continue
                item = QtGui.QStandardItem(itm + " : Waffe")
                item.setEditable(False)
                if value.isUserAdded:
                    item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                self.model.appendRow(item) 
        if self.ui.showManoever.isChecked():
            for itm, value in self.datenbank.manöver.items():
                if not value.isUserAdded and showUserAdded:
                    continue
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                    continue
                item = QtGui.QStandardItem(itm + " : Manöver / Modifikation")
                item.setEditable(False)
                if value.isUserAdded:
                    item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                self.model.appendRow(item)
        if self.ui.showDeleted.isChecked():
            for itm in self.datenbank.removeList:
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm[0].lower():
                    continue
                if itm[1] == "Talent" and self.ui.showTalente.isChecked() or\
                   itm[1] == "Vorteil" and self.ui.showVorteile.isChecked() or\
                   itm[1] == "Fertigkeit" and self.ui.showFertigkeiten.isChecked() or\
                   itm[1] == "Übernatürliche Fertigkeit" and self.ui.showUebernatuerlicheFertigkeiten.isChecked() or\
                   itm[1] == "Waffeneigenschaft" and self.ui.showWaffeneigenschaften.isChecked() or\
                   itm[1] == "Waffe" and self.ui.showWaffen.isChecked() or\
                   itm[1] == "Manöver / Modifikation" and self.ui.showManoever.isChecked():
                    item = QtGui.QStandardItem(itm[0] + " : "  + itm[1] + " (gelöscht)")
                    item.setEditable(False)
                    item.setBackground(QtGui.QBrush(QtCore.Qt.red))
                    self.model.appendRow(item)
        self.ui.listDatenbank.setModel(self.model)
               
    def wiederherstellen(self):
        for itm in self.ui.listDatenbank.selectedIndexes():
            item = self.model.itemData(itm)[0]
            if not item.endswith(" (gelöscht)"):
                continue
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
            elif tmp[1] == "Waffeneigenschaft":
                if tmp[0] in self.datenbank.waffeneigenschaften:
                    exists = True
                else:
                    self.datenbank.waffeneigenschaften.update({tmp[0]: removed[2]})
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
            elif dbS.entryType is "Waffeneigenschaft":
                self.addWaffeneigenschaft()
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
                      
    def addWaffeneigenschaft(self):
        we = Objekte.Waffeneigenschaft()
        ret = self.editWaffeneigenschaft(we)
        if ret is not None:
            self.datenbank.waffeneigenschaften.update({ret.name: ret})
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
    
    def editTalent(self, inp, readonly = False):
        dbT = DatenbankEditTalentWrapper.DatenbankEditTalentWrapper(self.datenbank, inp, readonly)
        return dbT.talent

    def editVorteil(self, inp, readonly = False):
        dbV = DatenbankEditVorteilWrapper.DatenbankEditVorteilWrapper(self.datenbank, inp, readonly)
        return dbV.vorteil

    def editFertigkeit(self, inp, readonly = False):
        dbF = DatenbankEditFertigkeitWrapper.DatenbankEditFertigkeitWrapper(self.datenbank, inp, False, readonly)
        return dbF.fertigkeit

    def editUebernatuerlich(self, inp, readonly = False):
        dbU = DatenbankEditFertigkeitWrapper.DatenbankEditFertigkeitWrapper(self.datenbank, inp, True, readonly)
        return dbU.fertigkeit
    
    def editWaffeneigenschaft(self, inp, readonly = False):
        dbW = DatenbankEditWaffeneigenschaftWrapper.DatenbankEditWaffeneigenschaftWrapper(self.datenbank, inp, readonly)
        return dbW.waffeneigenschaft

    def editWaffe(self, inp, readonly = False):
        dbW = DatenbankEditWaffeWrapper.DatenbankEditWaffeWrapper(self.datenbank, inp, readonly)
        return dbW.waffe
        
    def editManoever(self, inp, readonly = False):
        dbM = DatenbankEditManoeverWrapper.DatenbankEditManoeverWrapper(self.datenbank, inp, readonly)
        return dbM.man

    def editSelected(self):
        databaseChanged = False
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1].endswith(" (gelöscht)"):
                tmp[1] = tmp[1][:-11]
                deletedItem = [item for item in self.datenbank.removeList if item[0] == tmp[0] and item[1] == tmp[1]][0]
                if not deletedItem:
                    raise Exception('State corrupted.')
                if deletedItem[1] == "Talent":
                    self.editTalent(deletedItem[2], True)
                elif deletedItem[1] == "Vorteil":
                    self.editVorteil(deletedItem[2], True)
                elif deletedItem[1] == "Fertigkeit":
                    self.editFertigkeit(deletedItem[2], True)
                elif deletedItem[1] == "Übernatürliche Fertigkeit":
                    self.editUebernatuerlich(deletedItem[2], True)
                elif deletedItem[1] == "Waffeneigenschaft":
                    self.editWaffeneigenschaft(deletedItem[2], True)
                elif deletedItem[1] == "Waffe":
                    self.editWaffe(deletedItem[2], True)
                elif deletedItem[1] == "Manöver / Modifikation":
                    self.editManoever(deletedItem[2], True)
                continue

            if tmp[1] == "Talent":
                tal = self.datenbank.talente[tmp[0]]
                if tal is not None:
                    ret = self.editTalent(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.talente.pop(tmp[0],None)
                        self.datenbank.talente.update({ret.name: ret})
                        databaseChanged = True
            elif tmp[1] == "Vorteil":
                tal = self.datenbank.vorteile[tmp[0]]
                if tal is not None:
                    ret = self.editVorteil(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.vorteile.pop(tmp[0],None)
                        self.datenbank.vorteile.update({ret.name: ret})
                        databaseChanged = True
            elif tmp[1] == "Fertigkeit":
                tal = self.datenbank.fertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editFertigkeit(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.fertigkeiten.pop(tmp[0],None)
                        self.datenbank.fertigkeiten.update({ret.name: ret})
                        databaseChanged = True
            elif tmp[1] == "Übernatürliche Fertigkeit":
                tal = self.datenbank.übernatürlicheFertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editUebernatuerlich(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                        self.datenbank.übernatürlicheFertigkeiten.update({ret.name: ret})
                        databaseChanged = True
            elif tmp[1] == "Waffeneigenschaft":
                tal = self.datenbank.waffeneigenschaften[tmp[0]]
                if tal is not None:
                    ret = self.editWaffeneigenschaft(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.waffeneigenschaften.pop(tmp[0],None)
                        self.datenbank.waffeneigenschaften.update({ret.name: ret})
                        databaseChanged = True
            elif tmp[1] == "Waffe":
                tal = self.datenbank.waffen[tmp[0]]
                if tal is not None:
                    ret = self.editWaffe(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.waffen.pop(tmp[0],None)
                        self.datenbank.waffen.update({ret.name: ret})
                        databaseChanged = True
            elif tmp[1] == "Manöver / Modifikation":
                tal = self.datenbank.manöver[tmp[0]]
                if tal is not None:
                    ret = self.editManoever(tal)
                    if ret is not None:
                        if not tal.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], tal))
                        self.datenbank.manöver.pop(tmp[0],None)
                        self.datenbank.manöver.update({ret.name: ret})
                        databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
                                
    def deleteSelected(self):
        databaseChanged = False
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] == "Talent":
                t = self.datenbank.talente[tmp[0]]
                if not t.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], t))
                self.datenbank.talente.pop(tmp[0],None)
                databaseChanged = True
            elif tmp[1] == "Vorteil":
                v = self.datenbank.vorteile[tmp[0]]
                if not v.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], v))
                self.datenbank.vorteile.pop(tmp[0],None)
                databaseChanged = True
            elif tmp[1] == "Fertigkeit":
                f = self.datenbank.fertigkeiten[tmp[0]]
                if not f.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], f))
                self.datenbank.fertigkeiten.pop(tmp[0],None)
                databaseChanged = True
            elif tmp[1] == "Übernatürliche Fertigkeit":
                f = self.datenbank.übernatürlicheFertigkeiten[tmp[0]]
                if not f.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], f))
                self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                databaseChanged = True
            elif tmp[1] == "Waffeneigenschaft":
                w = self.datenbank.waffeneigenschaften[tmp[0]]
                if not w.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], w))
                self.datenbank.waffeneigenschaften.pop(tmp[0],None)
                databaseChanged = True
            elif tmp[1] == "Waffe":
                w = self.datenbank.waffen[tmp[0]]
                if not w.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], w))
                self.datenbank.waffen.pop(tmp[0],None)
                databaseChanged = True
            elif tmp[1] == "Manöver / Modifikation":
                m = self.datenbank.manöver[tmp[0]]
                if not m.isUserAdded:
                    self.datenbank.removeList.append((tmp[0], tmp[1], m))
                self.datenbank.manöver.pop(tmp[0],None)
                databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
                              
    def saveDatenbank(self):
        if os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            startDir = Wolke.Settings['Pfad-Regeln']
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"User Datenbank speichern...",startDir,"XML-Datei (*.xml)")
        if spath == "":
            return
        spath = os.path.realpath(spath)
        if not spath.endswith(".xml"):
            spath = spath + ".xml"

        isInRulesPath = os.path.dirname(spath) == Wolke.Settings['Pfad-Regeln']
        if not isInRulesPath:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Question)
            infoBox.setText("Der Charakter-Editor kann nur Datenbanken aus dem in den Einstellungen gesetzten Pfad laden, sicher dass du die Datenbank hierhin speichern möchtest?")
            infoBox.setWindowTitle("User Datenbank speichern")
            infoBox.addButton(QtWidgets.QPushButton("Ja"), QtWidgets.QMessageBox.YesRole)
            infoBox.addButton(QtWidgets.QPushButton("Nein"), QtWidgets.QMessageBox.NoRole)
            infoBox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.RejectRole)
            result = infoBox.exec_()
            if result == 1:
                self.saveDatenbank()
                return
            elif result == 2:
                return

        refDatabaseFile = os.getcwd() + os.path.normpath("/datenbank.xml")
        if spath == refDatabaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Überschreiben der zentralen Datenbank verhindert!")
            infoBox.setInformativeText("Bitte schreibe deine eigenen Regeln nicht mit in die zentrale datenbank.xml - \
diese wird bei vielen Updates von Sephrasto verändert, wodurch du deine Regeln \
verlieren würdest. Stattdessen kannst du sie als separate Datei abspeichern und in den Einstellungen selektieren. \
Sie wird dann automatisch beim Programmstart mit geladen. Änderungen darin überschreiben \
die datenbank.xml, aber bleiben bei Updates erhalten!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
            self.saveDatenbank()
            return

        self.savepath = spath
        self.quicksaveDatenbank()
        self.updateWindowTitleAndCloseButton()

        if isInRulesPath and Wolke.Settings['Datenbank'] != os.path.basename(spath):
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Question)
            infoBox.setText("Soll die neue Nutzer-Datenbank in den Einstellungen aktiv gesetzt werden?")
            infoBox.setWindowTitle("Nutzer-Datenbank aktiv setzen")
            infoBox.addButton(QtWidgets.QPushButton("Ja"), QtWidgets.QMessageBox.YesRole)
            infoBox.addButton(QtWidgets.QPushButton("Nein"), QtWidgets.QMessageBox.NoRole)
            result = infoBox.exec_()
            if result == 0:
                Wolke.Settings['Datenbank'] = os.path.basename(spath)
        
    def quicksaveDatenbank(self):
        if not self.savepath:
            self.saveDatenbank()
            return

        refDatabaseFile = os.getcwd() + os.path.normpath("/datenbank.xml")
        if self.savepath == refDatabaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Information)
            infoBox.setText("Überschreiben der zentralen Datenbank verhindert!")
            infoBox.setInformativeText("Bitte schreibe deine eigenen Regeln nicht mit in die zentrale datenbank.xml - \
diese wird bei vielen Updates von Sephrasto verändert, wodurch du deine Regeln \
verlieren würdest. Stattdessen kannst du sie als separate Datei abspeichern und in den Einstellungen selektieren. \
Sie wird dann automatisch beim Programmstart mit geladen. Änderungen darin überschreiben \
die datenbank.xml, aber bleiben bei Updates erhalten!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
        else:
            self.datenbank.datei = self.savepath
            self.datenbank.xmlSchreiben()
            self.changed = False
    
    def closeDatenbank(self):
        if self.cancelDueToPendingChanges("Datenbank schließen"):
            return
        self.datenbank.datei = None
        self.savepath = None
        self.datenbank.xmlLaden()
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.changed = False

    def loadDatenbank(self):
        if self.cancelDueToPendingChanges("Andere Datenbank laden"):
            return
        if os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            startDir = Wolke.Settings['Pfad-Regeln']
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"User Datenbank laden...",startDir,"XML-Datei (*.xml)")
        if not spath:
            return
        spath = os.path.realpath(spath)
        databaseFile = os.getcwd() + os.path.normpath("/datenbank.xml")
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
        self.updateWindowTitleAndCloseButton()
        self.changed = False
        
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