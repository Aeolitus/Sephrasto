from PyQt5 import QtWidgets, QtCore
import os.path
import logging
from Wolke import Wolke
import lxml.etree as etree
from EinstellungenWrapper import EinstellungenWrapper
from EventBus import EventBus
from CharakterAssistent.CharakterMerger import CharakterMerger
from Hilfsmethoden import Hilfsmethoden

class Regeln(object):
    def __init__(self):
        self.spezies = {}
        self.kulturen = {}
        self.professionen = {}

class WizardWrapper(object):
    def __init__(self):
        self.regelList = {}
        rootdir = os.path.dirname(os.path.abspath(__file__))
        datadirs = [os.path.join(rootdir, "Data"), os.path.join(Wolke.Settings['Pfad-Plugins'], "CharakterAssistent", "Data")]

        for datadir in datadirs:
            if not os.path.isdir(datadir):
                continue

            for regelnFolder in Hilfsmethoden.listdir(datadir):
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
                    for professionKategorieFolder in Hilfsmethoden.listdir(professionenFolder):
                        professionKategorieFolder = os.path.join(professionenFolder, professionKategorieFolder)
                        if os.path.isdir(professionKategorieFolder):
                            kategorie = os.path.basename(professionKategorieFolder)
                            if not kategorie in regeln.professionen:
                                regeln.professionen[kategorie] = {}
                            regeln.professionen[kategorie] = {**regeln.professionen[kategorie], **self.mapContainedFileNamesToPaths(professionKategorieFolder)}

    def mapContainedFileNamesToPaths(self, folderPath, appendEP = True):
        result = {}
        if os.path.isdir(folderPath):
            for path in Hilfsmethoden.listdir(folderPath):
                path = os.path.join(folderPath, path)
                if os.path.isfile(path):
                    fileNameSplit = os.path.splitext(os.path.basename(path))
                    if fileNameSplit[1] != ".xml":
                        continue

                    fileName = fileNameSplit[0]
                    index = 0
                    if fileName.endswith("_var"):
                        index = 1
                        fileName = fileName[:-4]

                        if logging.root.level == logging.DEBUG:
                            logging.debug("CharakterAssistent: Verifiziere " + path)
                            CharakterMerger.readChoices(path) # print log warnings for entire data folder on char creation
                    elif appendEP:
                        root = etree.parse(path).getroot()
                        fileName += " | " + root.find('Erfahrung/EPspent').text + " EP"

                    if fileName in result:
                        result[fileName].insert(index, path)
                    else:
                        result[fileName] = [path]
        return result

    def setupMainForm(self):
        rl = list(self.regelList.keys())
        self.ui.cbRegeln.addItems(rl)

        if "CharakterAssistent_Regeln" in Wolke.Settings:
            regeln = Wolke.Settings["CharakterAssistent_Regeln"]
            if regeln in rl:
                self.ui.cbRegeln.setCurrentIndex(rl.index(regeln))

        self.ui.cbRegeln.currentIndexChanged.connect(self.regelnChanged)
        self.ui.cbProfessionKategorie.currentIndexChanged.connect(self.professionKategorieChanged)

        self.regelnChanged()
        self.ui.btnAccept.clicked.connect(self.acceptClickedHandler)

        font = QtWidgets.QApplication.instance().font()
        font.setPointSize(font.pointSize()-1)
        self.ui.label.setFont(font)

    def professionKategorieChanged(self):
        regeln = self.regelList[self.ui.cbRegeln.currentText()]

        self.ui.cbProfession.clear()
        kategorie = self.ui.cbProfessionKategorie.currentText()

        self.ui.cbProfession.setEnabled(kategorie != "Überspringen")
        if kategorie != "Überspringen":
            self.ui.cbProfession.addItem("Überspringen")
            self.ui.cbProfession.addItems(regeln.professionen[kategorie].keys())

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
        self.ui.cbSpezies.addItems(regeln.spezies.keys())
        self.ui.cbKultur.addItem("Überspringen")
        self.ui.cbKultur.addItems(regeln.kulturen.keys())

        self.ui.cbProfessionKategorie.addItem("Überspringen")
        self.ui.cbProfessionKategorie.addItems(regeln.professionen.keys())
        self.professionKategorieChanged()

    def acceptClickedHandler(self):
        if not self.ui.cbRegeln.currentText() in self.regelList:
            self.formMain.hide()
            return

        regeln = self.regelList[self.ui.cbRegeln.currentText()]

        geschlecht = ""
        if self.ui.btnWeiblich.isChecked():
            geschlecht = "weiblich"
        else:
            geschlecht = "männlich"

        Wolke.Char.kurzbeschreibung = "Geschlecht: " + geschlecht
        EventBus.doAction("cbext_update", { 'name' : "geschlecht", 'value' : geschlecht })

        if self.ui.cbSpezies.currentText() != "Überspringen":
            spezies = regeln.spezies[self.ui.cbSpezies.currentText()]
            CharakterMerger.xmlLesen(spezies[0], True, False)
            CharakterMerger.handleChoices(spezies, self.ui.cbSpezies.currentText(), geschlecht, True, False, False)

        if self.ui.cbKultur.currentText() != "Überspringen":
            kultur = regeln.kulturen[self.ui.cbKultur.currentText()]
            CharakterMerger.xmlLesen(kultur[0], False, True)
            CharakterMerger.handleChoices(kultur, self.ui.cbKultur.currentText(), geschlecht, False, True, False)

        if self.ui.cbProfessionKategorie.currentText() != "Überspringen":
            professionKategorie = regeln.professionen[self.ui.cbProfessionKategorie.currentText()]

            if self.ui.cbProfession.currentText() != "Überspringen":
                profession = professionKategorie[self.ui.cbProfession.currentText()]
                CharakterMerger.xmlLesen(profession[0], False, False)
                CharakterMerger.handleChoices(profession, self.ui.cbProfession.currentText(), geschlecht, False, False, True)

        Wolke.Char.aktualisieren()

        self.formMain.hide()
        EventBus.doAction("charaktereditor_reload")