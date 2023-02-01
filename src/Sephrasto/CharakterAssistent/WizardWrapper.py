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
        datadirs = [os.path.join("Data", "CharakterAssistent"), os.path.join(Wolke.Settings['Pfad-Plugins'], "CharakterAssistent")]

        for datadir in datadirs:
            if not os.path.isdir(datadir):
                continue

            for regelnFolder in PathHelper.listdir(datadir):
                if not os.path.isdir(os.path.join(datadir, regelnFolder)):
                    continue
                regelnName = os.path.splitext(os.path.basename(regelnFolder))[0]
                if not regelnName in self.regelList:
                    self.regelList[regelnName] = Regeln()
                regeln = self.regelList[regelnName]

                speziesFolder = os.path.join(datadir, regelnFolder, "Spezies")
                regeln.spezies = {**regeln.spezies, **self.mapContainedFileNamesToPaths(speziesFolder)} #syntax = merge dict b into a

                kulturenFolder = os.path.join(datadir, regelnFolder, "Kultur")
                regeln.kulturen = {**regeln.kulturen, **self.mapContainedFileNamesToPaths(kulturenFolder)}

                professionenFolder = os.path.join(datadir, regelnFolder, "Profession")
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

                        if logging.root.level == logging.DEBUG:
                            logging.debug("CharakterAssistent: Verifiziere " + path)
                            CharakterMerger.readChoices(path) # print log warnings for entire data folder on char creation
                    else:
                        elPath = path
                        if appendEP:
                            root = etree.parse(path).getroot()
                            elName += " | " + root.find('Erfahrung/EPspent').text + " EP"

                    if elKey in result:
                        if elVarPath:
                            result[elKey].varPath = elVarPath
                        else:
                            result[elKey].path = elPath
                            result[elKey].comboName = elName
                    else:
                        result[elKey] = Element(elPath, elVarPath, elKey, elName)
        return result

    def setupMainForm(self):
        rl = sorted(list(self.regelList.keys()))
        if "Ilaris" in rl:
            rl.remove("Ilaris")
            rl.insert(0, "Ilaris")
        self.ui.cbRegeln.addItems(rl)

        if "CharakterAssistent_Regeln" in Wolke.Settings:
            regeln = Wolke.Settings["CharakterAssistent_Regeln"]
            if regeln in rl:
                self.ui.cbRegeln.setCurrentIndex(rl.index(regeln))

        self.ui.cbRegeln.currentIndexChanged.connect(self.regelnChanged)
        self.ui.cbSpezies.currentIndexChanged.connect(self.updateAcceptButton)
        self.ui.cbKultur.currentIndexChanged.connect(self.updateAcceptButton)
        self.ui.cbProfession.currentIndexChanged.connect(self.updateAcceptButton)
        self.ui.cbProfessionKategorie.currentIndexChanged.connect(self.professionKategorieChanged)

        self.regelnChanged()
        self.ui.btnAccept.clicked.connect(self.acceptClickedHandler)
        self.ui.btnCancel.clicked.connect(self.cancelClickedHandler)

    def updateAcceptButton(self):
        self.ui.btnAccept.setEnabled(self.ui.cbSpezies.currentText() != "Überspringen" or
                                     self.ui.cbKultur.currentText() != "Überspringen" or
                                     (self.ui.cbProfession.currentText() != "" and self.ui.cbProfession.currentText() != "Überspringen"))

    def professionKategorieChanged(self):
        regeln = self.regelList[self.ui.cbRegeln.currentText()]

        self.ui.cbProfession.clear()
        kategorie = self.ui.cbProfessionKategorie.currentText()

        self.ui.cbProfession.setEnabled(kategorie != "Überspringen")
        if kategorie != "Überspringen":
            self.ui.cbProfession.addItem("Überspringen")
            self.professionen = sorted(list(regeln.professionen[kategorie].values()), key = lambda el: el.name)
            self.ui.cbProfession.addItems([el.comboName for el in self.professionen])

    def regelnChanged(self):
        Wolke.Settings["CharakterAssistent_Regeln"] = self.ui.cbRegeln.currentText()
        EinstellungenWrapper.save()

        if not self.ui.cbRegeln.currentText() in self.regelList:
            return
        regeln = self.regelList[self.ui.cbRegeln.currentText()]

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
        self.form.close()

    def acceptClickedHandler(self):
        if not self.ui.cbRegeln.currentText() in self.regelList:
            self.form.close()
            return

        regeln = self.regelList[self.ui.cbRegeln.currentText()]

        geschlecht = ""
        if self.ui.btnWeiblich.isChecked():
            geschlecht = "weiblich"
        else:
            geschlecht = "männlich"

        Wolke.Char.kurzbeschreibung = "Geschlecht: " + geschlecht
        Wolke.Char.geschlecht = geschlecht

        # 1. add default weapons (Sephrasto only adds them if the weapons array is empty, which might not be the case here)
        for waffe in Wolke.DB.einstellungen["Waffen: Standardwaffen"].toTextList():
            if waffe in Wolke.DB.waffen:
                Wolke.Char.waffen.append(copy.copy(Wolke.DB.waffen[waffe]))

        # 2. add selected SKP
        if self.ui.cbSpezies.currentText() != "Überspringen":
            spezies = self.spezies[self.ui.cbSpezies.currentIndex()-1]
            CharakterMerger.xmlLesen(spezies.path, True, False)

        if self.ui.cbKultur.currentText() != "Überspringen":
            kultur = self.kulturen[self.ui.cbKultur.currentIndex()-1]
            CharakterMerger.xmlLesen(kultur.path, False, True)

        if self.ui.cbProfessionKategorie.currentText() != "Überspringen":
            professionKategorie = regeln.professionen[self.ui.cbProfessionKategorie.currentText()]

            if self.ui.cbProfession.currentText() != "Überspringen":
                profession = self.professionen[self.ui.cbProfession.currentIndex()-1]
                CharakterMerger.xmlLesen(profession.path, False, False)

        # 3. Handle choices afterwards so EP spent can be displayed accurately
        if self.ui.cbSpezies.currentText() != "Überspringen":
            spezies = self.spezies[self.ui.cbSpezies.currentIndex()-1]
            CharakterMerger.handleChoices(spezies, geschlecht, True, False, False)

        if self.ui.cbKultur.currentText() != "Überspringen":
            kultur = self.kulturen[self.ui.cbKultur.currentIndex()-1]
            CharakterMerger.handleChoices(kultur, geschlecht, False, True, False)

        if self.ui.cbProfessionKategorie.currentText() != "Überspringen":
            professionKategorie = regeln.professionen[self.ui.cbProfessionKategorie.currentText()]

            if self.ui.cbProfession.currentText() != "Überspringen":
                profession = self.professionen[self.ui.cbProfession.currentIndex()-1]
                CharakterMerger.handleChoices(profession, geschlecht, False, False, True)

        Wolke.Char.aktualisieren()

        self.form.hide()