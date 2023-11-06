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
from Datenbank import Datenbank
from Charakter import Char
from UI import CharakterMain, Wizard
from Core.Waffe import Waffe

class WizardConfig():
    def __init__(self, hausregeln, geschlecht, spezies, kultur, profession):
        self.hausregeln = hausregeln
        self.geschlecht = geschlecht
        self.spezies = spezies
        self.kultur = kultur
        self.profession = profession

    def apply(self, char, db):
        if self.geschlecht is not None:
            char.kurzbeschreibung = "Geschlecht: " + self.geschlecht
            char.geschlecht = self.geschlecht

        # 1. add default weapons (Sephrasto only adds them if the weapons array is empty, which might not be the case here)
        for waffe in db.einstellungen["Waffen: Standardwaffen"].wert:
            if waffe in db.waffen:
                char.waffen.append(Waffe(db.waffen[waffe]))

        # 2. add selected SKP
        if self.spezies is not None:
            CharakterMerger.xmlLesen(char, db, self.spezies.path, True, False)

        if self.kultur is not None:
            CharakterMerger.xmlLesen(char, db, self.kultur.path, False, True)

        if self.profession is not None:
            CharakterMerger.xmlLesen(char, db, self.profession.path, False, False)

        # 3. Handle choices afterwards so EP spent can be displayed accurately
        if self.spezies is not None:
            CharakterMerger.handleChoices(char, db, self.spezies, self.geschlecht, True, False, False)

        if self.kultur is not None:
            CharakterMerger.handleChoices(char, db, self.kultur, self.geschlecht, False, True, False)

        if self.profession is not None:
            CharakterMerger.handleChoices(char, db, self.profession, self.geschlecht, False, False, True)

class Regeln():
    def __init__(self):
        self.spezies = {}
        self.kulturen = {}
        self.professionen = {}

class Element():
    def __init__(self, path, varPath, name, comboName):
        self.path = path
        self.varPath = varPath
        self.name = name
        self.comboName = comboName

class WizardWrapper(object):
    def getBaukastenFolders():
        baukastenFolders = []
        for dataFolder in [os.path.join("Data", "CharakterAssistent"), os.path.join(Wolke.Settings['Pfad-Plugins'], "CharakterAssistent")]:
            if not os.path.isdir(dataFolder):
                continue
            for dir in PathHelper.listdir(dataFolder):
                baukastenFolders.append(os.path.join(dataFolder, dir))
        return baukastenFolders

    def __init__(self):
        self.config = None
        self.regelList = {}

        self.baukastenFolders = WizardWrapper.getBaukastenFolders()

        self.loadTemplates()
        self.form = QtWidgets.QDialog()
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)

        self.ui = Wizard.Ui_formMain()
        self.ui.setupUi(self.form)
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
        if len(rl) == 1:
            self.ui.lblRegeln.setVisible(False)
            self.ui.cbBaukasten.setVisible(False)

        self.ui.cbProfessionKategorie.currentIndexChanged.connect(self.professionKategorieChanged)
        self.regelnChanged()
        self.ui.btnAccept.clicked.connect(self.acceptClickedHandler)

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()

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

    def verify(db, baukastenFolder):
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

    def acceptClickedHandler(self):
        if not self.ui.cbBaukasten.currentText() in self.regelList:
            self.config = None
            self.form.reject()
            return

        geschlecht = None
        if self.ui.btnWeiblich.isChecked():
            geschlecht = "weiblich"
        elif self.ui.btnMaennlich.isChecked():
            geschlecht = "männlich"
        elif self.ui.btnDivers.isChecked():
            geschlecht = self.ui.leDivers.text()

        spezies = None
        if self.ui.cbSpezies.currentText() != "Überspringen":
            spezies = self.spezies[self.ui.cbSpezies.currentIndex()-1]

        kultur = None
        if self.ui.cbKultur.currentText() != "Überspringen":
            kultur = self.kulturen[self.ui.cbKultur.currentIndex()-1]

        profession = None
        if self.ui.cbProfessionKategorie.currentText() != "Überspringen" and self.ui.cbProfession.currentText() != "Überspringen":
            profession = self.professionen[self.ui.cbProfession.currentIndex()-1]

        self.config = WizardConfig(self.ui.cbRegeln.currentText(), geschlecht, spezies, kultur, profession)
        self.form.accept()