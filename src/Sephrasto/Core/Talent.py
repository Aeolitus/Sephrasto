import re
from EventBus import EventBus

# Implementation for Talente. Using the type object pattern.
# TalentDefinition: type object, initialized with database values
# Talent: character editor values, initialised with definition but supports overrides.
class TalentDefinition:
    displayName = "Talent"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.info = ''
        self.spezialTyp = -1
        self.kosten = 0
        self.verbilligt = False
        self.fertigkeiten = []
        self.voraussetzungen = []
        self.variableKosten = False
        self.kommentarErlauben = False
        self.cheatsheetAuflisten = True
        self.referenzBuch = 0
        self.referenzSeite = 0

        # Derived properties after deserialization
        self.hauptfertigkeit = None
        self.anzeigename = ''
        self.vorbereitungszeit = ""
        self.reichweite = ""
        self.wirkungsdauer = ""
        self.energieKosten = ""
        self.referenz = ""

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        fertigkeitenResolved = []
        ferts = db.fertigkeiten
        if self.spezialTalent:
            ferts = db.übernatürlicheFertigkeiten
        for fert in self.fertigkeiten:
            fertigkeitenResolved.append(ferts[fert])

        for fert in fertigkeitenResolved:
            if self.hauptfertigkeit is None:
                self.hauptfertigkeit = fert
            elif not self.hauptfertigkeit.talenteGruppieren and fert.talenteGruppieren:
                self.hauptfertigkeit = fert

        if self.spezialTalent:
            def findStat(stat):
                res = re.findall('<b>' + stat + ':</b>(.*?)(?:$|\n)', self.text, re.UNICODE)
                if len(res) == 0:
                    res = re.findall(stat + ':(.*?)(?:$|\n)', self.text, re.UNICODE)
                if len(res) == 1:
                    return res[0].strip()
                return ""
        
            self.vorbereitungszeit = findStat("Vorbereitungszeit")
            self.reichweite = findStat("Reichweite")
            self.wirkungsdauer = findStat("Wirkungsdauer")
            self.energieKosten = findStat("Kosten")
        else:
            steigerungsfaktor = 1
            for fert in fertigkeitenResolved:
                steigerungsfaktor = max(steigerungsfaktor, fert.steigerungsfaktor)

            if self.verbilligt:
                self.kosten = db.einstellungen["Talente: SteigerungsfaktorMulti Verbilligt"].wert*steigerungsfaktor
            else:
                self.kosten = db.einstellungen["Talente: SteigerungsfaktorMulti"].wert*steigerungsfaktor
        
        if self.referenzSeite > 0:
            referenzBücher = db.einstellungen["Referenzbücher"].wert
            if self.referenzBuch >= len(referenzBücher) or referenzBücher[self.referenzBuch] == "Ilaris":
                self.referenz = "S. " + str(self.referenzSeite)
            else:
                self.referenz = referenzBücher[self.referenzBuch] + " S. " + str(self.referenzSeite)
        
        self.anzeigename = self.name
        for fert in fertigkeitenResolved:
            self.anzeigename = self.anzeigename.replace(fert.name + ": ", "")

    @property
    def spezialTalent(self):
        return self.spezialTyp != -1

    def typname(self, db):
        typ = "Profan"
        if self.spezialTalent:
            typen = list(db.einstellungen["Talente: Spezialtalent Typen"].wert.keys())
            spezialTyp = min(self.spezialTyp, len(typen) - 1)
            typ = typen[spezialTyp]
        return typ

    def details(self, db):
        return f"{self.kosten} EP{' (verbilligt)' if self.verbilligt else ''}. {self.text}"

class Talent:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter

        # Serialized
        self._kommentar = ""
        self._kostenOverride = None

        # Nonserialized
        self.anzeigenameExt = definition.anzeigename
        self._updateAnzeigenameExt()
        self.probenwert = -1
        self._hauptfertigkeitOverride = None

    def __deepcopy__(self, memo=""):
        T = Talent(self.definition, self.charakter)
        T._kommentar = self._kommentar
        T._kostenOverride = self._kostenOverride
        T.anzeigenameExt = self.anzeigenameExt
        T.probenwert = self.probenwert
        T._hauptfertigkeitOverride = self._hauptfertigkeitOverride
        return T

    @property
    def name(self):
        return self.definition.name

    @property
    def text(self):
        return self.definition.text

    @property
    def info(self):
        return self.definition.info

    @property
    def kosten(self):
        kosten = self.definition.kosten
        if self._kostenOverride is not None:
            kosten = self._kostenOverride
        return EventBus.applyFilter("talent_kosten", kosten, { "charakter" : self.charakter, "talent" : self.name })

    @kosten.setter
    def kosten(self, kosten):
        self._kostenOverride = kosten
        self._updateAnzeigenameExt()

    @property
    def verbilligt(self):
        return self.definition.verbilligt

    @property
    def fertigkeiten(self):
        return self.definition.fertigkeiten

    @property
    def voraussetzungen(self):
        return self.definition.voraussetzungen

    @property
    def variableKosten(self):
        return self.definition.variableKosten

    @property
    def kommentarErlauben(self):
        return self.definition.kommentarErlauben

    @property
    def cheatsheetAuflisten(self):
        return self.definition.cheatsheetAuflisten
    
    @property
    def anzeigename(self):
        return self.definition.anzeigename

    @property
    def vorbereitungszeit(self):
        return self.definition.vorbereitungszeit

    @property
    def reichweite(self):
        return self.definition.reichweite

    @property
    def wirkungsdauer(self):
        return self.definition.wirkungsdauer

    @property
    def energieKosten(self):
        return self.definition.energieKosten

    @property
    def referenz(self):
        return self.definition.referenz

    @property
    def spezialTalent(self):
        return self.definition.spezialTalent

    @property
    def spezialTyp(self):
        return self.definition.spezialTyp

    @property
    def kommentar(self):
        return self._kommentar

    @kommentar.setter
    def kommentar(self, kommentar):
        self._kommentar = kommentar
        self._updateAnzeigenameExt()

    @property
    def hauptfertigkeit(self):
        if self._hauptfertigkeitOverride is not None:
            return self._hauptfertigkeitOverride
        return self.definition.hauptfertigkeit

    def typname(self, db):
        return self.definition.typname(db)

    def aktualisieren(self):
        # PW und Hauptferigkeit
        self.probenwert = -1
        self._hauptfertigkeitOverride = None
        fertigkeiten = self.charakter.fertigkeiten
        if self.spezialTalent:
            fertigkeiten = self.charakter.übernatürlicheFertigkeiten

        for fertName in self.fertigkeiten:
            if not fertName in fertigkeiten:
                continue
            nextFert = fertigkeiten[fertName]
            self.probenwert = max(self.probenwert, nextFert.probenwertTalent + nextFert.basiswertMod)
            if self._hauptfertigkeitOverride is None or self._hauptfertigkeitOverride.name not in fertigkeiten:
                self._hauptfertigkeitOverride = nextFert.definition
            elif not self._hauptfertigkeitOverride.talenteGruppieren and nextFert.talenteGruppieren:
                self._hauptfertigkeitOverride = nextFert.definition
            elif self._hauptfertigkeitOverride.talenteGruppieren and nextFert.talenteGruppieren:
                if fertigkeiten[self._hauptfertigkeitOverride.name].probenwertTalent <= nextFert.probenwertTalent:
                    self._hauptfertigkeitOverride = nextFert.definition

    def _updateAnzeigenameExt(self):
        self.anzeigenameExt = self.definition.anzeigename
        ep = None
        if self.variableKosten:
            ep = str(self.kosten)
        
        kommentar = None
        if self.kommentarErlauben and self.kommentar != "":
            kommentar = self.kommentar

        if kommentar or ep:
            self.anzeigenameExt += " ("
        if kommentar:
            self.anzeigenameExt += kommentar
        if kommentar and ep:
            self.anzeigenameExt += "; "
        if ep:
            self.anzeigenameExt += ep + " EP"
        if kommentar or ep:
            self.anzeigenameExt += ")"
