from PySide6 import QtWidgets, QtCore, QtGui
import os.path
import yaml

class Charakterbogen:
    def __init__(self):
        self.name = ""
        self.filePath = ""
        self.info = ""
        self.seitengrösse = "A4"
        self.seitenorientierung = "Portrait"
        self.seitenbeschreibungen = []
        self.maxVorteile = 0
        self.maxVorteileProFeld = 3
        self.maxKampfVorteile = 0
        self.maxKampfVorteileProFeld = 3
        self.maxÜberVorteile = 0
        self.maxÜberVorteileProFeld = 3
        self.maxFreie = 0
        self.maxFreieProFeld = 3
        self.maxFertigkeiten = 0
        self.maxÜberFertigkeiten = 0
        self.maxÜberTalente = 0
        self.überSeite = 0
        self.überFertigkeitenZuProfan = False
        self.überVorteileZuKampf = False
        self.extraÜberSeiten = True
        self.bild = []
        self.regelanhangPfad = os.path.join("Data", "Charakterbögen", "Regelanhang", "Regelanhang.html")
        self.regelanhangHintergrundPfad = os.path.join("Data", "Charakterbögen", "Regelanhang", "Hintergrund.pdf")
        self.regelanhangSeitengrösse = "A4"
        self.regelanhangSeitenorientierung = "Portrait"
        self.regelanhangSeitenabstände = [70, 36, 70, 36]
        self.regelanhangSeitenzahlPosition = "bottom"
        self.regelanhangSeitenzahlAbstand = 40
        self.formularMappings = {}

    def getPageLayout(self):
        pl = QtGui.QPageLayout()
        pl.setPageSize(getattr(QtGui.QPageSize, self.seitengrösse))
        pl.setOrientation(getattr(QtGui.QPageLayout, self.seitenorientierung))
        return pl

    def getRegelanhangPageLayout(self):
        pl = QtGui.QPageLayout()
        pl.setPageSize(getattr(QtGui.QPageSize, self.regelanhangSeitengrösse))
        pl.setOrientation(getattr(QtGui.QPageLayout, self.regelanhangSeitenorientierung))
        pl.setTopMargin(self.regelanhangSeitenabstände[0])
        pl.setRightMargin(self.regelanhangSeitenabstände[1])
        pl.setBottomMargin(self.regelanhangSeitenabstände[2])
        pl.setLeftMargin(self.regelanhangSeitenabstände[3])
        return pl

    def hasImage(self, index):
        return len(self.bild[index]) == 3

    def getImageSize(self, index, referenceSize):
        sizeMulti = self.bild[index][0]
        return [referenceSize[0]*sizeMulti, referenceSize[1]*sizeMulti]

    def getImageOffset(self, index):
        return self.bild[index][1:]

    def load(self, inifile):
        yamlDict = None
        with open(inifile,'r', encoding='utf8') as file:
            yamlDict = yaml.safe_load(file) 
            
        datei = os.path.splitext(inifile)[0] + ".pdf"
        
        if "Datei" in yamlDict:
            datei = os.path.join(os.path.dirname(inifile), yamlDict["Datei"])

        if not os.path.isfile(datei):
            return False
        self.name = os.path.splitext(os.path.basename(inifile))[0]
        self.filePath = datei

        if "Info" in yamlDict:
            self.info = yamlDict["Info"]
        if "Seitengrösse" in yamlDict:
            self.seitengrösse = yamlDict["Seitengrösse"]
        if "Seitenorientierung" in yamlDict:
            self.seitenorientierung = yamlDict["Seitenorientierung"]
        if "Seitenbeschreibungen" in yamlDict:
            self.seitenbeschreibungen = yamlDict["Seitenbeschreibungen"]
        if "MaxVorteile" in yamlDict:
            self.maxVorteile = yamlDict["MaxVorteile"]
        if "MaxKampfVorteile" in yamlDict:
            self.maxKampfVorteile = yamlDict["MaxKampfVorteile"]
        if "MaxÜbernatürlicheVorteile" in yamlDict:
            self.maxÜberVorteile = yamlDict["MaxÜbernatürlicheVorteile"]
        if "MaxFreieFertigkeiten" in yamlDict:
            self.maxFreie = yamlDict["MaxFreieFertigkeiten"]
        if "MaxFertigkeiten" in yamlDict:
            self.maxFertigkeiten = yamlDict["MaxFertigkeiten"]
        if "MaxÜbernatürlicheFertigkeiten" in yamlDict:
            self.maxÜberFertigkeiten = yamlDict["MaxÜbernatürlicheFertigkeiten"]
        if "MaxÜbernatürlicheTalente" in yamlDict:
            self.maxÜberTalente = yamlDict["MaxÜbernatürlicheTalente"]
        if "ÜberSeite" in yamlDict:
            self.überSeite = yamlDict["ÜberSeite"]
        if "ÜberFertigkeitenZuProfan" in yamlDict:
            self.überFertigkeitenZuProfan = yamlDict["ÜberFertigkeitenZuProfan"]
        if "ÜberVorteileZuKampf" in yamlDict:
            self.überVorteileZuKampf = yamlDict["ÜberVorteileZuKampf"]
        if "MaxVorteileProFeld" in yamlDict:
            self.maxVorteileProFeld = yamlDict["MaxVorteileProFeld"]
        if "MaxKampfVorteileProFeld" in yamlDict:
            self.maxKampfVorteileProFeld = yamlDict["MaxKampfVorteileProFeld"]
        if "MaxÜberVorteileProFeld" in yamlDict:
            self.maxÜberVorteileProFeld = yamlDict["MaxÜberVorteileProFeld"]
        if "MaxFreieProFeld" in yamlDict:
            self.maxFreieProFeld = yamlDict["MaxFreieProFeld"]
        if "ExtraÜberSeiten" in yamlDict:
            self.extraÜberSeiten = yamlDict["ExtraÜberSeiten"]
        if "Bild" in yamlDict:
            for v in yamlDict["Bild"]:
                self.bild.append(v)
        regelAnhang = os.path.splitext(self.filePath)[0] + "_Regelanhang.html"
        if os.path.isfile(regelAnhang):
            self.regelanhangPfad = regelAnhang
            regelAnhangHintergrund = os.path.splitext(self.filePath)[0] + "_Hintergrund.pdf"
            if os.path.isfile(regelAnhangHintergrund):
                self.regelanhangHintergrundPfad = regelAnhangHintergrund
            else:
                self.regelanhangHintergrundPfad = None
        if "RegelanhangSeitengrösse" in yamlDict:
            self.regelanhangSeitengrösse = yamlDict["RegelanhangSeitengrösse"]
        if "RegelanhangSeitenorientierung" in yamlDict:
            self.regelanhangSeitenorientierung = yamlDict["RegelanhangSeitenorientierung"]
        if "RegelanhangSeitenabstände" in yamlDict:
            self.regelanhangSeitenabstände = yamlDict["RegelanhangSeitenabstände"]
        if "RegelanhangSeitenzahlPosition" in yamlDict:
            self.regelanhangSeitenzahlPosition = yamlDict["RegelanhangSeitenzahlPosition"]
        if "RegelanhangSeitenzahlAbstand" in yamlDict:
            self.regelanhangSeitenzahlAbstand = yamlDict["RegelanhangSeitenzahlAbstand"]
        if "FormularMappings" in yamlDict:
            self.formularMappings = yamlDict["FormularMappings"]

        return True