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

class Element(object):
    def __init__(self, path, varPath, name, comboName):
        self.path = path
        self.varPath = varPath
        self.name = name
        self.comboName = comboName

class WizardWrapper(object):
    def __init__(self):
        self.regelList = {}
        rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        datadirs = [os.path.join(rootdir, "Data", "CharakterAssistent"), os.path.join(Wolke.Settings['Pfad-Plugins'], "CharakterAssistent")]

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
        self.ui.cbProfessionKategorie.currentIndexChanged.connect(self.professionKategorieChanged)

        self.regelnChanged()
        self.ui.btnAccept.clicked.connect(self.acceptClickedHandler)
        self.ui.btnCancel.clicked.connect(self.cancelClickedHandler)

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
        self.formMain.close()

    def acceptClickedHandler(self):
        if not self.ui.cbRegeln.currentText() in self.regelList:
            self.formMain.close()
            return

        regeln = self.regelList[self.ui.cbRegeln.currentText()]

        geschlecht = ""
        if self.ui.btnWeiblich.isChecked():
            geschlecht = "weiblich"
        else:
            geschlecht = "männlich"

        Wolke.Char.kurzbeschreibung = "Geschlecht: " + geschlecht
        Wolke.Char.geschlecht = geschlecht

        if self.ui.cbSpezies.currentText() != "Überspringen":
            spezies = self.spezies[self.ui.cbSpezies.currentIndex()-1]
            CharakterMerger.xmlLesen(spezies.path, True, False)
            CharakterMerger.handleChoices(spezies, geschlecht, True, False, False)

        if self.ui.cbKultur.currentText() != "Überspringen":
            kultur = self.kulturen[self.ui.cbKultur.currentIndex()-1]
            CharakterMerger.xmlLesen(kultur.path, False, True)
            CharakterMerger.handleChoices(kultur, geschlecht, False, True, False)

        if self.ui.cbProfessionKategorie.currentText() != "Überspringen":
            professionKategorie = regeln.professionen[self.ui.cbProfessionKategorie.currentText()]

            if self.ui.cbProfession.currentText() != "Überspringen":
                profession = self.professionen[self.ui.cbProfession.currentIndex()-1]
                CharakterMerger.xmlLesen(profession.path, False, False)
                CharakterMerger.handleChoices(profession, geschlecht, False, False, True)

        Wolke.Char.aktualisieren()

        self.formMain.hide()