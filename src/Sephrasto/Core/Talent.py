import re
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden
from VoraussetzungenListe import VoraussetzungenListe
import copy

# Implementation for Talente. Using the type object pattern.
# TalentDefinition: type object, initialized with database values
# Talent: character editor values, initialised with definition but supports overrides.
class TalentDefinition:
    displayName = "Talent"
    serializationName = "Talent"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.info = ''
        self.spezialTyp = -1
        self.kosten = 0
        self.verbilligt = False
        self.fertigkeiten = []
        self.voraussetzungen = VoraussetzungenListe()
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
        self.erlernen = ""
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
            if fert in ferts:
                fertigkeitenResolved.append(ferts[fert])

        for fert in fertigkeitenResolved:
            if self.hauptfertigkeit is None:
                self.hauptfertigkeit = fert
            elif not self.hauptfertigkeit.talenteGruppieren and fert.talenteGruppieren:
                self.hauptfertigkeit = fert

        if self.spezialTalent:
            # this is called A LOT so no regex here for perf reasons
            split = self.text.split("\n")[1:]
            for s in split:
                if s.startswith("Vorbereitungszeit:"):
                    self.vorbereitungszeit = s[len("Vorbereitungszeit:"):].strip()
                elif s.startswith("<b>Vorbereitungszeit:</b>"):
                    self.vorbereitungszeit = s[len("<b>Vorbereitungszeit:</b>"):].strip()
                elif s.startswith("Reichweite:"):
                    self.reichweite = s[len("Reichweite:"):].strip()
                elif s.startswith("<b>Reichweite:</b>"):
                    self.reichweite = s[len("<b>Reichweite:</b>"):].strip() 
                elif s.startswith("Wirkungsdauer:"):
                    self.wirkungsdauer = s[len("Wirkungsdauer:"):].strip()
                elif s.startswith("<b>Wirkungsdauer:</b>"):
                    self.wirkungsdauer = s[len("<b>Wirkungsdauer:</b>"):].strip() 
                elif s.startswith("Kosten:"):
                    self.energieKosten = s[len("Kosten:"):].strip()
                elif s.startswith("<b>Kosten:</b>"):
                    self.energieKosten = s[len("<b>Kosten:</b>"):].strip() 
                elif s.startswith("Erlernen:"):
                    self.erlernen = s[len("Erlernen:"):].strip()
                elif s.startswith("<b>Erlernen:</b>"):
                    self.erlernen = s[len("<b>Erlernen:</b>"):].strip() 
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
        if self.hauptfertigkeit is not None:
            typ += f" ({self.hauptfertigkeit.name})"
        return typ

    def details(self, db):
        return f"{self.kosten} EP{' (verbilligt)' if self.verbilligt else ''}. {self.text}"

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('voraussetzungen', self.voraussetzungen.text)
        if self.spezialTalent:
            ser.set('kosten', self.kosten)
            ser.set('spezialTyp', self.spezialTyp)
        else:
            ser.set('kosten', -1)                
        ser.set('verbilligt', self.verbilligt)
        ser.set('fertigkeiten', Hilfsmethoden.FertArray2Str(self.fertigkeiten, None))
        ser.set('variableKosten', self.variableKosten)
        ser.set('kommentar', self.kommentarErlauben)
        ser.set('referenzbuch', self.referenzBuch)
        ser.set('referenzseite', self.referenzSeite)
        if not self.cheatsheetAuflisten:
            ser.set('csAuflisten', False)
        if self.info:
            ser.set('info', self.info)
        EventBus.doAction("talentdefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.voraussetzungen.compile(ser.get('voraussetzungen', ''))
        self.kosten = ser.getInt('kosten')
        self.spezialTyp = ser.getInt('spezialTyp', self.spezialTyp)
        self.verbilligt = ser.getInt('verbilligt')
        self.fertigkeiten = Hilfsmethoden.FertStr2Array(ser.get('fertigkeiten'), None)
        self.variableKosten = ser.getBool('variableKosten')
        self.kommentarErlauben = ser.getBool('kommentar', self.kommentarErlauben)
        if self.variableKosten:
            self.kommentarErlauben = True
        self.referenzBuch = ser.getInt('referenzbuch', self.referenzBuch)
        self.referenzSeite = ser.getInt('referenzseite', self.referenzSeite)
        self.cheatsheetAuflisten = ser.getBool('csAuflisten', self.cheatsheetAuflisten)
        self.info = ser.get('info', self.info)
        EventBus.doAction("talentdefinition_deserialisiert", { "object" : self, "deserializer" : ser})

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
        self._voraussetzungenOverride = None

    def __deepcopy__(self, memo=""):
        # create new object
        cls = self.__class__
        result = cls.__new__(cls)
        # deepcopy everything except for self, charakter and definition
        memo[id(self)] = result
        memo[id(self.charakter)] = self.charakter
        memo[id(self.definition)] = self.definition
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

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
    def voraussetzungen(self):
        if self._voraussetzungenOverride is not None:
            return self._voraussetzungenOverride
        return self.definition.voraussetzungen

    @voraussetzungen.setter
    def voraussetzungen(self, voraussetzungen):
        self._voraussetzungenOverride = voraussetzungen

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
    def erlernen(self):
        return self.definition.erlernen

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
