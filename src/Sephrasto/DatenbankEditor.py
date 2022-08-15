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

class DatenbankTypWrapper(object):
    def __init__(self, addFunc, editFunc, showCheckbox = None):
        super().__init__()
        self.addFunc = addFunc
        self.editFunc = editFunc
        self.showCheckbox = showCheckbox

class DatenbankEditor(object):
    def __init__(self, plugins):
        super().__init__()
        self.plugins = plugins
        self.databaseTypes = {}
        self.datenbank = Datenbank.Datenbank(Wolke.Settings['Datenbank'])
        self.savepath = self.datenbank.datei
        self.changed = False
        self.windowTitleDefault = ""
        self.checkMissingPlugins()

    def checkMissingPlugins(self):
        enabledPlugins = []
        for pluginData in self.plugins:
            if pluginData.plugin is not None and hasattr(pluginData.plugin, "changesDatabase") and pluginData.plugin.changesDatabase():
                enabledPlugins.append(pluginData.name)
        
        missingPlugins = set(self.datenbank.enabledPlugins) - set(enabledPlugins)
        if len(missingPlugins) > 0:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setWindowTitle("Plugin fehlt!")
            infoBox.setText("Die Datenbank wurde mit einem oder mehreren Plugins erstellt, die sie beeinflussen. "\
            "Nicht alle davon sind aktiv, daher können beim Speichern Daten dieser Plugins verloren gehen:\n\n" + ", ".join(missingPlugins))
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()

        self.datenbank.enabledPlugins = enabledPlugins
    
    def setupGUI(self):
        windowSize = Wolke.Settings["WindowSize-Datenbank"]
        self.form.resize(windowSize[0], windowSize[1])

        for pd in self.plugins:
            if pd.plugin is None:
                continue

            if hasattr(pd.plugin, "createDatabaseButtons"):
                for button in pd.plugin.createDatabaseButtons():
                    self.ui.verticalLayout.addWidget(button)

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
        self.ui.buttonEditieren.setText("\uf044")

        self.ui.buttonDuplizieren.clicked.connect(self.duplicateSelected)
        self.ui.buttonDuplizieren.setEnabled(False)
        self.ui.buttonDuplizieren.setText("\uf24d")

        self.ui.buttonLoeschen.clicked.connect(self.deleteSelected)
        self.ui.buttonLoeschen.setEnabled(False)
        self.ui.buttonLoeschen.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
        self.ui.buttonLoeschen.setText("\uf2ed")

        self.ui.buttonHinzufuegen.clicked.connect(self.hinzufuegen)
        self.ui.buttonHinzufuegen.setText("\u002b")

        self.ui.buttonWiederherstellen.clicked.connect(self.wiederherstellen)
        self.ui.buttonWiederherstellen.setText("\uf829")

        self.ui.showUserAdded.stateChanged.connect(self.updateGUI)
        self.ui.showDeleted.stateChanged.connect(self.updateGUI)

        self.databaseTypes = {}
        self.databaseTypes["Talent"] = DatenbankTypWrapper(self.addTalent, self.editTalent, self.ui.showTalente)
        self.databaseTypes["Vorteil"] = DatenbankTypWrapper(self.addVorteil, self.editVorteil, self.ui.showVorteile)
        self.databaseTypes["Fertigkeit"] = DatenbankTypWrapper(self.addFertigkeit, self.editFertigkeit, self.ui.showFertigkeiten)
        self.databaseTypes["Übernatürliche Fertigkeit"] = DatenbankTypWrapper(self.addUebernatuerlich, self.editUebernatuerlich, self.ui.showUebernatuerlicheFertigkeiten)
        self.databaseTypes["Freie Fertigkeit"] = DatenbankTypWrapper(self.addFreieFertigkeit, self.editFreieFertigkeit, self.ui.showFreieFertigkeiten)
        self.databaseTypes["Waffeneigenschaft"] = DatenbankTypWrapper(self.addWaffeneigenschaft, self.editWaffeneigenschaft, self.ui.showWaffeneigenschaften)
        self.databaseTypes["Waffe"] = DatenbankTypWrapper(self.addWaffe, self.editWaffe, self.ui.showWaffen)
        self.databaseTypes["Rüstung"] = DatenbankTypWrapper(self.addRuestung, self.editRuestung, self.ui.showRuestungen)
        self.databaseTypes["Manöver / Modifikation"] = DatenbankTypWrapper(self.addManoever, self.editManoever, self.ui.showManoever)
        self.databaseTypes["Einstellung"] = DatenbankTypWrapper(self.addEinstellung, self.editEinstellung, self.ui.showEinstellung)
        pluginDatabaseTypes = {}
        pluginDatabaseTypes = EventBus.applyFilter("datenbank_editor_typen", pluginDatabaseTypes)
        for dbType in pluginDatabaseTypes:
            self.databaseTypes[dbType] = pluginDatabaseTypes[dbType]
            if not self.databaseTypes[dbType].showCheckbox:
                self.databaseTypes[dbType].showCheckbox = QtWidgets.QCheckBox(dbType)
                self.databaseTypes[dbType].showCheckbox.setChecked(True)
            self.ui.verticalLayout_3.addWidget(pluginDatabaseTypes[dbType].showCheckbox)

        for dbType in self.databaseTypes.values():
            dbType.showCheckbox.stateChanged.connect(self.updateGUI)

        self.form.closeEvent = self.closeEvent
        self.windowTitleDefault = self.form.windowTitle()

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
            name = tmp[0]
            typ = tmp[1]
            if typ == "Einstellung":
                table = self.datenbank.tablesByName["Einstellung"]
                if name in table and not table[name].isUserAdded:
                    self.ui.buttonLoeschen.setEnabled(False)
                    self.ui.buttonDuplizieren.setEnabled(False)

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
        else:
            Wolke.Settings["WindowSize-Datenbank"] = [self.form.size().width(), self.form.size().height()]

    def onDatabaseChange(self):
        self.changed = True
        self.updateGUI()
        self.listSelectionChanged()
    
    def updateWindowTitleAndCloseButton(self):
        splitpath = self.savepath and os.path.split(self.savepath) or ["keine Hausregeln geladen"]
        self.form.setWindowTitle(self.windowTitleDefault + " (" + splitpath[-1] + ")")
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
            if not dbType.showCheckbox.isChecked():
                continue
            table = self.datenbank.tablesByName[dbTypeName]
            for itm, value in sorted(table.items()):
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
            for type in sorted(self.datenbank.removeList):
                for name in self.datenbank.removeList[type]:
                    if self.ui.nameFilterEdit.text() and not self.ui.nameFilterEdit.text().lower() in name.lower():
                        continue

                    if type in self.databaseTypes:
                        databaseType = self.databaseTypes[type]
                        if databaseType.showCheckbox.isChecked():
                            item = QtGui.QStandardItem(name + " : "  + type + " (gelöscht)")
                            item.setEditable(False)
                            item.setBackground(QtGui.QBrush(QtCore.Qt.red))
                            item.setForeground(QtGui.QBrush(QtCore.Qt.white))
                            self.model.appendRow(item)

        self.ui.listDatenbank.setModel(self.model)

        if self.datenbank.datei:
            self.ui.buttonLoadDB.setText("Weitere Hausregeln laden")
        else:
            self.ui.buttonLoadDB.setText("Hausregeln laden")
               
    def wiederherstellen(self):
        for itm in self.ui.listDatenbank.selectedIndexes():
            item = self.model.itemData(itm)[0]
            if not item.endswith(" (gelöscht)"):
                continue
            item = item[:-11].split(" : ")
            name = item[0]
            typ = item[1]

            removed = False
            if typ in self.datenbank.removeList and name in self.datenbank.removeList[typ]:
                removed = self.datenbank.removeList[typ][name]

            if not removed:
                raise Exception('State corrupted.')

            exists = False

            if typ in self.datenbank.tablesByName:
                table = self.datenbank.tablesByName[typ]
                if name in table:
                    exists = True
                else:
                    table.update({name: removed})
            else:
                raise Exception('Unknown category.')

            if exists:
                messageBox = QtWidgets.QMessageBox()
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setWindowTitle('Wiederherstellen nicht möglich!')
                messageBox.setText('Es existiert bereits ein(e) ' + typ + ' mit dem Namen "' + name + '"')            
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
                messageBox.exec_()
                return
            del self.datenbank.removeList[typ][name]

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
                self.datenbank.tablesByName[dbS.entryType].update({val.name : val})
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
            name = tmp[0]
            typ = tmp[1]
            if typ.endswith(" (gelöscht)"):
                typ = typ[:-11]
                deletedItem = False
                if typ in self.datenbank.removeList and name in self.datenbank.removeList[typ]:
                    deletedItem = self.datenbank.removeList[typ][name]
                if not deletedItem:
                    raise Exception('State corrupted.')

                if typ in self.databaseTypes:
                    databaseType = self.databaseTypes[typ]
                    databaseType.editFunc(deletedItem, True)
                continue

            if not typ in self.datenbank.tablesByName:
                continue
            table = self.datenbank.tablesByName[typ]
            element = table[name]
            if element is None:
                continue
            if not typ in self.databaseTypes:
                continue
            ret = self.databaseTypes[typ].editFunc(element)
            if ret is None:
                continue
            if not element.isUserAdded:
                if not typ in self.datenbank.removeList:
                    self.datenbank.removeList[typ] = {}
                self.datenbank.removeList[typ][name] = element
            table.pop(name,None)
            table.update({ret.name: ret})
            databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()

    def duplicate(self, table, name):
        item = table[name]
        clone = copy(item)
        clone.isUserAdded = True
        while clone.name in table:
            clone.name = clone.name + " (Kopie)"
        table[clone.name] = clone

    def duplicateSelected(self):
        databaseChanged = False
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            name = tmp[0]
            typ = tmp[1]

            if typ in self.datenbank.tablesByName:
                table = self.datenbank.tablesByName[typ]
                self.duplicate(table, name)
                databaseChanged = True

        if databaseChanged:
            self.onDatabaseChange()
                                
    def deleteSelected(self):
        databaseChanged = False
        for itm in self.ui.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            name = tmp[0]
            typ = tmp[1]
            if typ in self.datenbank.tablesByName:
                table = self.datenbank.tablesByName[typ]
                element  = table[name]
                if not element.isUserAdded:
                    if typ == "Einstellung":
                        continue
                    if not typ in self.datenbank.removeList:
                        self.datenbank.removeList[typ] = {}
                    self.datenbank.removeList[typ][name] = element
                table.pop(name,None)

                if typ == "Einstellung":
                    # Auto restore
                    removed = False
                    if typ in self.datenbank.removeList and name in self.datenbank.removeList[typ]:
                        removed = self.datenbank.removeList[typ][name]

                    if removed:
                        table.update({name: removed})
                        del self.datenbank.removeList[typ][name]
                    else:
                        logging.warn("Tried to auto restore " + name + " but didn't find it in the database.")

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
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.changed = False

    RememberConflictResult = -1

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

        if spath == self.datenbank.datei:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Diese Hausregeln sind bereits geladen!")
            infoBox.setWindowTitle("Ungültige Datei!")
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            infoBox.exec_()
            self.loadDatenbank()
            return

        def showConflict(typ, old, new):
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Question)
            infoBox.setText(typ + " " + old.name + " wurde sowohl in den bestehenden, als auch in den neu geladenen Hausregeln geändert. Welche Version möchtest du beibehalten?")
            infoBox.setWindowTitle("Zusätzliche Hausregeln laden: Konflikt")

            infoBox.addButton(QtWidgets.QPushButton("Aktuell ansehen"), QtWidgets.QMessageBox.YesRole)
            infoBox.addButton(QtWidgets.QPushButton("Neu ansehen"), QtWidgets.QMessageBox.YesRole)
            infoBox.addButton(QtWidgets.QPushButton("Aktuell auswählen"), QtWidgets.QMessageBox.YesRole)
            infoBox.addButton(QtWidgets.QPushButton("Neu auswählen"), QtWidgets.QMessageBox.YesRole)
            check = QtWidgets.QCheckBox("Alle weiteren Konflikte gleich behandeln.")
            infoBox.setCheckBox(check)
            return (infoBox.exec_(), infoBox.checkBox().isChecked())

        def conflictCB(typ, old, new):
            result = -1
            if DatenbankEditor.RememberConflictResult != -1:
                result = DatenbankEditor.RememberConflictResult

            while result < 2: 
                result, checked = showConflict(typ, old, new)
                if result < 2 and typ in self.databaseTypes:
                    databaseType = self.databaseTypes[typ]
                    databaseType.editFunc(old if result == 0 else new, True)
                elif result >= 2 and checked:
                    DatenbankEditor.RememberConflictResult = result

            return old if result == 2 else new

        if self.datenbank.datei:
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Warning)
            infoBox.setText("Es sind bereits Hausregeln geladen. Wenn du zusätzlich noch andere Hausregeln lädst, werden beide zusammengefasst!\n" +
                            "Wenn in beiden Hausregeln die gleichen Datenbank-Elemente geändert wurden, wirst du dich zwischen einer Version entscheiden müssen - Sephrasto wird dir dabei helfen. " +
                            "Du kannst dies ohne Risiko ausprobieren: Die zusammengefassten Hausregeln werden erst gespeichert, wenn du den Speichern-Button drückst.\n" +
                            "In jedem Fall solltest du hinterher aber überprüfen, ob alle geänderten Elemente noch intakt sind. " +
                            "Beispielsweise könnten die zusätzlichen Hausregeln einen Vorteil gelöscht haben, der in den aktuellen Hausregeln irgendwo als Voraussetzung gelistet ist.")
            infoBox.setWindowTitle("Mehrere Hausregeln laden")
            infoBox.addButton(QtWidgets.QPushButton("Abbrechen"), QtWidgets.QMessageBox.NoRole)
            infoBox.addButton(QtWidgets.QPushButton("Verstanden!"), QtWidgets.QMessageBox.YesRole)
            result = infoBox.exec_()
            if result == 1:
                DatenbankEditor.RememberConflictResult = -1
                self.datenbank.xmlLadenAdditiv(spath, conflictCB)
                DatenbankEditor.RememberConflictResult = -1
            else:
                return
        else:
            self.savepath = spath
            self.datenbank.datei = spath
            self.datenbank.xmlLaden()
        
        self.updateGUI()
        self.updateWindowTitleAndCloseButton()
        self.checkMissingPlugins()
        self.changed = False
        
if __name__ == "__main__":
    D = DatenbankEditor()
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    D.Form = QtWidgets.QWidget()
    D.ui = UI.DatenbankMain.Ui_Form()
    D.ui.setupUi(D.Form)
    D.setupGUI()
    D.Form.show()
    app.exec_()