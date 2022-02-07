# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:29:39 2017

@author: Aeolitus
"""
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import Fertigkeiten
import Datenbank
import UI.DatenbankMain
import DatenbankEditFertigkeitWrapper
import DatenbankEditFreieFertigkeitWrapper
import DatenbankEditTalentWrapper
import DatenbankEditVorteilWrapper
import DatenbankSelectTypeWrapper
import DatenbankEditWaffeneigenschaftWrapper
import DatenbankEditWaffeWrapper
import DatenbankEditRuestungWrapper
import DatenbankEditManoeverWrapper
import DatenbankEditEinstellungWrapper
from DatenbankEinstellung import DatenbankEinstellung
import Objekte
import os
from EinstellungenWrapper import EinstellungenWrapper
from Wolke import Wolke
from copy import copy
import logging
from EventBus import EventBus

class DatabaseType(object):
    def __init__(self, databaseDict, addFunc, editFunc, showCheckbox):
        super().__init__()
        self.databaseDict = databaseDict
        self.addFunc = addFunc
        self.editFunc = editFunc
        self.showCheckbox = showCheckbox

class DatenbankEdit(object):
    def __init__(self, plugins):
        super().__init__()
        self.plugins = plugins
        self.databaseTypes = {}
        self.datenbank = Datenbank.Datenbank()
        self.savepath = self.datenbank.datei
        self.changed = False
        self.windowTitleDefault = ""
    
    def setupGUI(self):
        for plugin in [p.plugin for p in self.plugins]:
            if hasattr(plugin, "createDatabaseButtons"):
                for button in plugin.createDatabaseButtons():
                    self.ui.verticalLayout.addWidget(button)

        self.initDatabaseTypes()

        # GUI Mods
        self.model = QtGui.QStandardItemModel(self.ui.listDatenbank)
        self.ui.listDatenbank.setModel(self.model)
        self.ui.listDatenbank.doubleClicked["QModelIndex"].connect(self.editSelected)
        self.ui.listDatenbank.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ui.listDatenbank.selectionModel().selectionChanged.connect(self.listSelectionChanged)
        self.ui.checkFilterTyp.stateChanged.connect(self.filterTypChanged)
        self.ui.nameFilterEdit.textChanged.connect(self.updateGUI)
        self.ui.buttonCloseDB.clicked.connect(self.closeDatenbank)
        self.ui.buttonLoadDB.clicked.connect(self.loadDatenbank)
        self.ui.buttonSaveDB.clicked.connect(self.saveDatenbank)
        self.ui.buttonQuicksave.clicked.connect(self.quicksaveDatenbank)
        self.ui.buttonEditieren.clicked.connect(self.editSelected)
        self.ui.buttonEditieren.setEnabled(False)
        self.ui.buttonDuplizieren.clicked.connect(self.duplicateSelected)
        self.ui.buttonDuplizieren.setEnabled(False)
        self.ui.buttonLoeschen.clicked.connect(self.deleteSelected)
        self.ui.buttonLoeschen.setEnabled(False)
        self.ui.buttonLoeschen.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
        self.ui.buttonHinzufuegen.clicked.connect(self.hinzufuegen)
        self.ui.buttonWiederherstellen.clicked.connect(self.wiederherstellen)

        self.ui.showUserAdded.stateChanged.connect(self.updateGUI)
        self.ui.showDeleted.stateChanged.connect(self.updateGUI)
        for dbType in self.pluginDatabaseTypes.values():
            self.ui.verticalLayout_3.addWidget(dbType.showCheckbox)
        for dbType in self.databaseTypes.values():
            dbType.showCheckbox.stateChanged.connect(self.updateGUI)

        self.Form.closeEvent = self.closeEvent
        self.windowTitleDefault = self.Form.windowTitle()

        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
    
    def filterTypChanged(self):
        if self.ui.checkFilterTyp.checkState() == 0:
            for dbType in self.databaseTypes.values():
                dbType.showCheckbox.setChecked(False)
        elif self.ui.checkFilterTyp.checkState() == 1 or self.ui.checkFilterTyp.checkState() == 2:
            for dbType in self.databaseTypes.values():
                dbType.showCheckbox.setChecked(True)

    def listSelectionChanged(self):
        indexes = self.ui.listDatenbank.selectedIndexes()
        if not indexes:
            self.ui.buttonEditieren.setEnabled(False)
            self.ui.buttonLoeschen.setEnabled(False)
            self.ui.buttonLoeschen.setVisible(True)
            self.ui.buttonWiederherstellen.setVisible(False)
            self.ui.buttonDuplizieren.setEnabled(False)
            return
        item = self.model.itemData(indexes[0])[0]
        if item.endswith(" (gelöscht)"):
            self.ui.buttonDuplizieren.setEnabled(False)
            self.ui.buttonEditieren.setEnabled(True)
            self.ui.buttonLoeschen.setVisible(False)
            self.ui.buttonWiederherstellen.setVisible(True)
        else:
            self.ui.buttonDuplizieren.setEnabled(True)
            self.ui.buttonEditieren.setEnabled(True)
            self.ui.buttonLoeschen.setEnabled(True)
            self.ui.buttonLoeschen.setVisible(True)
            self.ui.buttonWiederherstellen.setVisible(False)
            tmp = item.split(" : ")
            if tmp[1] == "Einstellung":
                databaseType = self.databaseTypes["Einstellung"]
                if tmp[0] in databaseType.databaseDict and not databaseType.databaseDict[tmp[0]].isUserAdded:
                    self.ui.buttonLoeschen.setEnabled(False)

    def initDatabaseTypes(self):
        self.databaseTypes = {}
        self.databaseTypes["Talent"] = DatabaseType(self.datenbank.talente, self.addTalent, self.editTalent, self.ui.showTalente)
        self.databaseTypes["Vorteil"] = DatabaseType(self.datenbank.vorteile, self.addVorteil, self.editVorteil, self.ui.showVorteile)
        self.databaseTypes["Fertigkeit"] = DatabaseType(self.datenbank.fertigkeiten, self.addFertigkeit, self.editFertigkeit, self.ui.showFertigkeiten)
        self.databaseTypes["Übernatürliche Fertigkeit"] = DatabaseType(self.datenbank.übernatürlicheFertigkeiten, self.addUebernatuerlich, self.editUebernatuerlich, self.ui.showUebernatuerlicheFertigkeiten)
        self.databaseTypes["Freie Fertigkeit"] = DatabaseType(self.datenbank.freieFertigkeiten, self.addFreieFertigkeit, self.editFreieFertigkeit, self.ui.showFreieFertigkeiten)
        self.databaseTypes["Waffeneigenschaft"] = DatabaseType(self.datenbank.waffeneigenschaften, self.addWaffeneigenschaft, self.editWaffeneigenschaft, self.ui.showWaffeneigenschaften)
        self.databaseTypes["Waffe"] = DatabaseType(self.datenbank.waffen, self.addWaffe, self.editWaffe, self.ui.showWaffen)
        self.databaseTypes["Rüstung"] = DatabaseType(self.datenbank.rüstungen, self.addRuestung, self.editRuestung, self.ui.showRuestungen)
        self.databaseTypes["Manöver / Modifikation"] = DatabaseType(self.datenbank.manöver, self.addManoever, self.editManoever, self.ui.showManoever)
        self.databaseTypes["Einstellung"] = DatabaseType(self.datenbank.einstellungen, self.addEinstellung, self.editEinstellung, self.ui.showEinstellung)
        self.pluginDatabaseTypes = {}
        self.pluginDatabaseTypes = EventBus.applyFilter("datenbank_editor_typen", self.pluginDatabaseTypes)
        for dbType in self.pluginDatabaseTypes:
            if dbType in self.databaseTypes.keys():
                del self.pluginDatabaseTypes[dbType]
            else:
                self.databaseTypes[dbType] = self.pluginDatabaseTypes[dbType]

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
        self.listSelectionChanged()
    
    def updateWindowTitleAndCloseButton(self):
        splitpath = self.savepath and os.path.split(self.savepath) or ["keine Hausregeln geladen"]
        self.Form.setWindowTitle(self.windowTitleDefault + " (" + splitpath[-1] + ")")
        self.ui.buttonCloseDB.setEnabled(self.savepath and True or False)

    def updateGUI(self):
        self.model.clear()
        showUserAdded = self.ui.showUserAdded.isChecked()

        allChecked = True
        anyChecked = False
        for dbType in self.databaseTypes.values():
            anyChecked = anyChecked or dbType.showCheckbox.isChecked()
            allChecked = allChecked and dbType.showCheckbox.isChecked()

        self.ui.checkFilterTyp.blockSignals(True)
        if allChecked:
            self.ui.checkFilterTyp.setCheckState(2)
        elif anyChecked:
            self.ui.checkFilterTyp.setCheckState(1)
        else:
            self.ui.checkFilterTyp.setCheckState(0)
        self.ui.checkFilterTyp.blockSignals(False)

        for dbTypeName,dbType in self.databaseTypes.items():
            if dbType.showCheckbox.isChecked():
                for itm, value in sorted(dbType.databaseDict.items()):
                    if not value.isUserAdded and showUserAdded:
                        continue
                    if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm.lower():
                        continue
                    item = QtGui.QStandardItem(itm + " : " + dbTypeName)
                    item.setEditable(False)
                    if value.isUserAdded:
                        item.setBackground(QtGui.QBrush(QtCore.Qt.green))
                        item.setForeground(QtGui.QBrush(QtCore.Qt.black))
                    self.model.appendRow(item)

        if self.ui.showDeleted.isChecked():
            for itm in sorted(self.datenbank.removeList):
                if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in itm[0].lower():
                    continue

                if itm[1] in self.databaseTypes:
                    databaseType = self.databaseTypes[itm[1]]
                    if databaseType.showCheckbox.isChecked():
                        item = QtGui.QStandardItem(itm[0] + " : "  + itm[1] + " (gelöscht)")
                        item.setEditable(False)
                        item.setBackground(QtGui.QBrush(QtCore.Qt.red))
                        item.setForeground(QtGui.QBrush(QtCore.Qt.white))
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

            if tmp[1] in self.databaseTypes:
                databaseType = self.databaseTypes[tmp[1]]
                if tmp[0] in databaseType.databaseDict:
                    exists = True
                else:
                    databaseType.databaseDict.update({tmp[0]: removed[2]})
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
        dbS = DatenbankSelectTypeWrapper.DatenbankSelectTypeWrapper(self.databaseTypes)
        if dbS.entryType is not None and dbS.entryType in self.databaseTypes:
            databaseType = self.databaseTypes[dbS.entryType]
            val = databaseType.addFunc()
            if val is not None:
                databaseType.databaseDict.update({val.name : val})
                self.onDatabaseChange()

    def addTalent(self):
        tal = Fertigkeiten.Talent()
        return self.editTalent(tal)
                          
    def addVorteil(self):
        vor = Fertigkeiten.Vorteil()
        return self.editVorteil(vor)
                          
    def addFertigkeit(self):
        fer = Fertigkeiten.Fertigkeit()
        return self.editFertigkeit(fer)
                          
    def addUebernatuerlich(self):
        fer = Fertigkeiten.Fertigkeit()
        return self.editUebernatuerlich(fer)
            
    def addFreieFertigkeit(self):
        fer = Fertigkeiten.FreieFertigkeitDB()
        return self.editFreieFertigkeit(fer)
                      
    def addWaffeneigenschaft(self):
        we = Objekte.Waffeneigenschaft()
        return self.editWaffeneigenschaft(we)

    def addWaffe(self):
        waf = Objekte.Nahkampfwaffe()
        return self.editWaffe(waf)
            
    def addRuestung(self):
        rüs = Objekte.Ruestung()
        return self.editRuestung(rüs)
    
    def addManoever(self):
        man = Fertigkeiten.Manoever()
        return self.editManoever(man)
            
    def addEinstellung(self):
        de = DatenbankEinstellung()
        return self.editEinstellung(de)
    
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
    
    def editFreieFertigkeit(self, inp, readonly = False):
        dbU = DatenbankEditFreieFertigkeitWrapper.DatenbankEditFreieFertigkeitWrapper(self.datenbank, inp, readonly)
        return dbU.freieFertigkeit
    
    def editWaffeneigenschaft(self, inp, readonly = False):
        dbW = DatenbankEditWaffeneigenschaftWrapper.DatenbankEditWaffeneigenschaftWrapper(self.datenbank, inp, readonly)
        return dbW.waffeneigenschaft

    def editWaffe(self, inp, readonly = False):
        dbW = DatenbankEditWaffeWrapper.DatenbankEditWaffeWrapper(self.datenbank, inp, readonly)
        return dbW.waffe
    
    def editRuestung(self, inp, readonly = False):
        dbW = DatenbankEditRuestungWrapper.DatenbankEditRuestungWrapper(self.datenbank, inp, readonly)
        return dbW.ruestung
        
    def editManoever(self, inp, readonly = False):
        dbM = DatenbankEditManoeverWrapper.DatenbankEditManoeverWrapper(self.datenbank, inp, readonly)
        return dbM.man

    def editEinstellung(self, inp, readonly = False):
        dbE = DatenbankEditEinstellungWrapper.DatenbankEditEinstellungWrapper(self.datenbank, inp, readonly)
        return dbE.einstellung

    def editSelected(self):
        databaseChanged = False
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1].endswith(" (gelöscht)"):
                tmp[1] = tmp[1][:-11]
                deletedItem = [item for item in self.datenbank.removeList if item[0] == tmp[0] and item[1] == tmp[1]][0]
                if not deletedItem:
                    raise Exception('State corrupted.')

                if deletedItem[1] in self.databaseTypes:
                    databaseType = self.databaseTypes[deletedItem[1]]
                    databaseType.editFunc(deletedItem[2], True)
                continue

            if tmp[1] in self.databaseTypes:
                databaseType = self.databaseTypes[tmp[1]]
                element = databaseType.databaseDict[tmp[0]]
                if element is not None:
                    ret = databaseType.editFunc(element)
                    if ret is not None:
                        if not element.isUserAdded:
                            self.datenbank.removeList.append((tmp[0], tmp[1], element))
                        databaseType.databaseDict.pop(tmp[0],None)
                        databaseType.databaseDict.update({ret.name: ret})
                        databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()

    def duplicate(self, list, name):
        item = list[name]
        clone = copy(item)
        clone.isUserAdded = True
        while clone.name in list:
            clone.name = clone.name + " (Kopie)"
        list[clone.name] = clone

    def duplicateSelected(self):
        databaseChanged = False
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")

            if tmp[1] in self.databaseTypes:
                databaseType = self.databaseTypes[tmp[1]]
                self.duplicate(databaseType.databaseDict, tmp[0])
                databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
                                
    def deleteSelected(self):
        databaseChanged = False
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] in self.databaseTypes:
                databaseType = self.databaseTypes[tmp[1]]
                element  = databaseType.databaseDict[tmp[0]]
                if not element.isUserAdded:
                    if tmp[1] == "Einstellung":
                        continue
                    self.datenbank.removeList.append((tmp[0], tmp[1], element))
                databaseType.databaseDict.pop(tmp[0],None)

                if tmp[1] == "Einstellung":
                    # Auto restore
                    removed = [item for item in self.datenbank.removeList if item[0] == tmp[0] and item[1] == tmp[1]]
                    if len(removed) > 0:
                        databaseType.databaseDict.update({tmp[0]: removed[0][2]})
                        self.datenbank.removeList.remove(removed[0])
                    else:
                        logging.warn("Tried to auto restore " + tmp[0] + " but didn't find it in the database.")

                databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
                              
    def saveDatenbank(self):
        if os.path.isdir(Wolke.Settings['Pfad-Regeln']):
            startDir = Wolke.Settings['Pfad-Regeln']
        else:
            startDir = ""
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Hausregeln speichern...",startDir,"XML-Datei (*.xml)")
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
            infoBox.setWindowTitle("Hausregeln speichern")
            infoBox.addButton(QtWidgets.QPushButton("Ja"), QtWidgets.QMessageBox.YesRole)
            infoBox.addButton(QtWidgets.QPushButton("Anderer Pfad"), QtWidgets.QMessageBox.NoRole)
            infoBox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.RejectRole)
            result = infoBox.exec_()
            if result == 1:
                self.saveDatenbank()
                return
            elif result == 2:
                return

        refDatabaseFile = os.getcwd() + os.path.normpath("/Data/datenbank.xml")
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
            infoBox.setText("Sollen die neuen Hausregeln in den Einstellungen aktiv gesetzt werden?")
            infoBox.setWindowTitle("Hausregeln aktiv setzen")
            infoBox.addButton(QtWidgets.QPushButton("Ja"), QtWidgets.QMessageBox.YesRole)
            infoBox.addButton(QtWidgets.QPushButton("Nein"), QtWidgets.QMessageBox.NoRole)
            result = infoBox.exec_()
            if result == 0:
                Wolke.Settings['Datenbank'] = os.path.basename(spath)
                EinstellungenWrapper.save()
        
    def quicksaveDatenbank(self):
        if not self.savepath:
            self.saveDatenbank()
            return

        refDatabaseFile = os.getcwd() + os.path.normpath("/Data/datenbank.xml")
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
        self.initDatabaseTypes()
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
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Hausregeln laden...",startDir,"XML-Datei (*.xml)")
        if not spath:
            return
        spath = os.path.realpath(spath)
        databaseFile = os.getcwd() + os.path.normpath("/Data/datenbank.xml")
        if spath == databaseFile:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Diese Funktion dient dem Laden einer Hausregel-Datenbank. Die zentrale Sephrasto-Datenbank 'database.xml' wird sowieso immer geladen!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
            self.loadDatenbank()
            return
        self.savepath = spath
        self.datenbank.datei = spath
        self.datenbank.xmlLaden()
        self.initDatabaseTypes()
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.changed = False
        
if __name__ == "__main__":
    D = DatenbankEdit()
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    D.Form = QtWidgets.QWidget()
    D.ui = UI.DatenbankMain.Ui_Form()
    D.ui.setupUi(D.Form)
    D.setupGUI()
    D.Form.show()
    app.exec_()