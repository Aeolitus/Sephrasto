from PySide6 import QtWidgets, QtCore
import os.path
import logging
from Wolke import Wolke
import lxml.etree as etree
from EinstellungenWrapper import EinstellungenWrapper
from EventBus import EventBus
from CharakterAssistent.CharakterMerger import CharakterMerger
import PathHelper
import copy
from Core.Waffe import Waffe
from Datenbank import Datenbank
from Charakter import Char

class Regeln(object):
    def __init__(self):
        self.spezies = {}
        self.kulturen = {}
        self.professionen = {}

class Element(object):
    def __init__(self, path, varPath, name, comboName):
        self.path = path
        self.varPath = varPath
        self.name = name
        self.comboName = comboName

class WizardWrapper(object):
    def __init__(self):
        self.regelList = {}

        self.baukastenFolders = []
        for dataFolder in [os.path.join("Data", "CharakterAssistent"), os.path.join(Wolke.Settings['Pfad-Plugins'], "CharakterAssistent")]:
            if not os.path.isdir(dataFolder):
                continue
            for baukastenFolders in PathHelper.listdir(dataFolder):
                self.baukastenFolders.append(os.path.join(dataFolder, baukastenFolders))

    def loadTemplates(self):
        for baukastenFolder in self.baukastenFolders:
            baukastenName = os.path.splitext(os.path.basename(baukastenFolder))[0]
            if not baukastenName in self.regelList:
                self.regelList[baukastenName] = Regeln()
            regeln = self.regelList[baukastenName]

            speziesFolder = os.path.join(baukastenFolder, "Spezies")
            regeln.spezies = {**regeln.spezies, **self.mapContainedFileNamesToPaths(speziesFolder)} #syntax = merge dict b into a

            kulturenFolder = os.path.join(baukastenFolder, "Kultur")
            regeln.kulturen = {**regeln.kulturen, **self.mapContainedFileNamesToPaths(kulturenFolder)}

            professionenFolder = os.path.join(baukastenFolder, "Profession")
            if os.path.isdir(professionenFolder):
                for professionKategorieFolder in PathHelper.listdir(professionenFolder):
                    professionKategorieFolder = os.path.join(professionenFolder, professionKategorieFolder)
                    if os.path.isdir(professionKategorieFolder):
                        kategorie = os.path.basename(professionKategorieFolder)
                        if not kategorie in regeln.professionen:
                            regeln.professionen[kategorie] = {}
                        regeln.professionen[kategorie] = {**regeln.professionen[kategorie], **self.mapContainedFileNamesToPaths(professionKategorieFolder)}

    def mapContainedFileNamesToPaths(self, folderPath, appendEP = True):
        result = {}
        if os.path.isdir(folderPath):
            for path in PathHelper.listdir(folderPath):
                path = os.path.join(folderPath, path)
                if os.path.isfile(path):
                    fileNameSplit = os.path.splitext(os.path.basename(path))
                    if fileNameSplit[1] != ".xml":
                        continue

                    elKey = fileNameSplit[0]
                    elName = elKey
                    elPath = ""
                    elVarPath = ""
                    if elKey.endswith("_var"):
                        elVarPath = path
                        elKey = elKey[:-4]
                    else:
                        elPath = path
                        if appendEP:
                            root = etree.parse(path).getroot()
                            if root.find('Erfahrung/EPspent') is not None: #deprecated
                                elName += " | " + root.find('Erfahrung/EPspent').text + " EP"
                            elif root.find('Erfahrung/Ausgegeben') is not None:
                                elName += " | " + root.find('Erfahrung/Ausgegeben').text + " EP"

                    if elKey in result:
                        if elVarPath:
                            result[elKey].varPath = elVarPath
                        else:
                            result[elKey].path = elPath
                            result[elKey].comboName = elName
                    else:
                        result[elKey] = Element(elPath, elVarPath, elKey, elName)
        return result

    def verify(self, db, baukastenFolder):
        errors = []
        foldersToCheck = []
        foldersToCheck.append(os.path.join(baukastenFolder, "Spezies"))
        foldersToCheck.append(os.path.join(baukastenFolder, "Kultur"))
        professionenFolder = os.path.join(baukastenFolder, "Profession")
        if os.path.isdir(professionenFolder):
            foldersToCheck.extend([os.path.join(professionenFolder, p) for p in PathHelper.listdir(professionenFolder)])
        for folderPath in foldersToCheck:
            for path in PathHelper.listdir(folderPath):
                path = os.path.join(folderPath, path)
                if os.path.isfile(path):
                    fileNameSplit = os.path.splitext(os.path.basename(path))
                    if fileNameSplit[0].endswith("_var") and fileNameSplit[1] == ".xml":
                        errors.extend(CharakterMerger.verifyChoices(db, path))
        return errors


    def setupMainForm(self):
        self.ui.cbRegeln.addItems(EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"]))
        self.ui.cbRegeln.setCurrentText(Wolke.Settings['Datenbank'])

        rl = sorted(list(self.regelList.keys()))
        if "Ilaris" in rl:
            rl.remove("Ilaris")
            rl.insert(0, "Ilaris")
        self.ui.cbBaukasten.addItems(rl)

        if "CharakterAssistent_Regeln" in Wolke.Settings:
            regeln = Wolke.Settings["CharakterAssistent_Regeln"]
            if regeln in rl:
                self.ui.cbBaukasten.setCurrentIndex(rl.index(regeln))

        self.ui.cbBaukasten.currentIndexChanged.connect(self.regelnChanged)
        self.ui.cbProfessionKategorie.currentIndexChanged.connect(self.professionKategorieChanged)

        self.regelnChanged()
        self.ui.btnAccept.clicked.connect(self.acceptClickedHandler)
        self.ui.btnCancel.clicked.connect(self.cancelClickedHandler)

    def professionKategorieChanged(self):
        regeln = self.regelList[self.ui.cbBaukasten.currentText()]

        self.ui.cbProfession.clear()
        kategorie = self.ui.cbProfessionKategorie.currentText()

        self.ui.cbProfession.setEnabled(kategorie != "Überspringen")
        if kategorie != "Überspringen":
            self.ui.cbProfession.addItem("Überspringen")
            self.professionen = sorted(list(regeln.professionen[kategorie].values()), key = lambda el: el.name)
            self.ui.cbProfession.addItems([el.comboName for el in self.professionen])

    def regelnChanged(self):
        Wolke.Settings["CharakterAssistent_Regeln"] = self.ui.cbBaukasten.currentText()
        EinstellungenWrapper.save()

        if not self.ui.cbBaukasten.currentText() in self.regelList:
            return
        regeln = self.regelList[self.ui.cbBaukasten.currentText()]

        self.ui.cbSpezies.clear()
        self.ui.cbKultur.clear()
        self.ui.cbProfessionKategorie.blockSignals(True)
        self.ui.cbProfessionKategorie.clear()
        self.ui.cbProfessionKategorie.blockSignals(False)

        self.ui.cbSpezies.addItem("Überspringen")
        self.spezies = sorted(list(regeln.spezies.values()), key = lambda el: el.name)
        self.ui.cbSpezies.addItems([el.comboName for el in self.spezies])
        self.ui.cbKultur.addItem("Überspringen")
        self.kulturen = sorted(list(regeln.kulturen.values()), key = lambda el: el.name)
        self.ui.cbKultur.addItems([el.comboName for el in self.kulturen])

        self.ui.cbProfessionKategorie.addItem("Überspringen")
        self.ui.cbProfessionKategorie.addItems(sorted(regeln.professionen.keys()))
        self.professionKategorieChanged()

    def cancelClickedHandler(self):
        self.form.reject()

    def acceptClickedHandler(self):
        if not self.ui.cbBaukasten.currentText() in self.regelList:
            self.form.reject()
            return
        Wolke.DB = Datenbank(self.ui.cbRegeln.currentText(), True)
        Wolke.Char = Char()
        regeln = self.regelList[self.ui.cbBaukasten.currentText()]

        geschlecht = ""
        if self.ui.btnWeiblich.isChecked():
            geschlecht = "weiblich"
        elif self.ui.btnMaennlich.isChecked():
            geschlecht = "männlich"
        else:
            geschlecht = self.ui.leDivers.text()

        Wolke.Char.kurzbeschreibung = "Geschlecht: " + geschlecht
        Wolke.Char.geschlecht = geschlecht

        # 1. add default weapons (Sephrasto only adds them if the weapons array is empty, which might not be the case here)
        for waffe in Wolke.DB.einstellungen["Waffen: Standardwaffen"].wert:
            if waffe in Wolke.DB.waffen:
                Wolke.Char.waffen.append(Waffe(Wolke.DB.waffen[waffe]))

        # 2. add selected SKP
        if self.ui.cbSpezies.currentText() != "Überspringen":
            spezies = self.spezies[self.ui.cbSpezies.currentIndex()-1]
            CharakterMerger.xmlLesen(Wolke.DB, spezies.path, True, False)

        if self.ui.cbKultur.currentText() != "Überspringen":
            kultur = self.kulturen[self.ui.cbKultur.currentIndex()-1]
            CharakterMerger.xmlLesen(Wolke.DB, kultur.path, False, True)

        if self.ui.cbProfessionKategorie.currentText() != "Überspringen":
            professionKategorie = regeln.professionen[self.ui.cbProfessionKategorie.currentText()]

            if self.ui.cbProfession.currentText() != "Überspringen":
                profession = self.professionen[self.ui.cbProfession.currentIndex()-1]
                CharakterMerger.xmlLesen(Wolke.DB, profession.path, False, False)

        # 3. Handle choices afterwards so EP spent can be displayed accurately
        if self.ui.cbSpezies.currentText() != "Überspringen":
            spezies = self.spezies[self.ui.cbSpezies.currentIndex()-1]
            CharakterMerger.handleChoices(Wolke.DB, spezies, geschlecht, True, False, False)

        if self.ui.cbKultur.currentText() != "Überspringen":
            kultur = self.kulturen[self.ui.cbKultur.currentIndex()-1]
            CharakterMerger.handleChoices(Wolke.DB, kultur, geschlecht, False, True, False)

        if self.ui.cbProfessionKategorie.currentText() != "Überspringen":
            professionKategorie = regeln.professionen[self.ui.cbProfessionKategorie.currentText()]

            if self.ui.cbProfession.currentText() != "Überspringen":
                profession = self.professionen[self.ui.cbProfession.currentIndex()-1]
                CharakterMerger.handleChoices(Wolke.DB, profession, geschlecht, False, False, True)

        self.form.accept()