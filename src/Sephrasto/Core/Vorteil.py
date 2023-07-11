from Wolke import Wolke
import logging
from EventBus import EventBus

# Implementation for Vorteile. Using the type object pattern.
# VorteilDefinition: type object, initialized with database values
# Vorteil: character editor values, initialised with definition but supports overrides.

class VorteilLinkKategorie:
   NichtVerknüpfen = 0
   Regel = 1
   ÜberTalent = 2
   Vorteil = 3

class VorteilDefinition():
    displayName = "Vorteil"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.info = ''
        self.bedingungen = ''
        self.kosten = 0
        self.variableKosten = False
        self.kommentarErlauben = False
        self.typ = 0
        self.voraussetzungen = []
        self.nachkauf = ''
        self.cheatsheetAuflisten = True
        self.cheatsheetBeschreibung = ''
        self.linkKategorie = VorteilLinkKategorie.NichtVerknüpfen
        self.linkElement = ''
        self.script = ''
        self.scriptPrio = 0
        self.querverweise = []

        # Derived properties after deserialization
        self.querverweiseResolved = {}
        self.scriptCompiled = ''

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        self.scriptCompiled = compile(self.script or "", self.name + " Script", "exec")

        for ref in self.querverweise:
            if ref.startswith("Regel:"):
                regel = ref[len("Regel:"):]
                if regel not in db.regeln:
                    continue
                regel = db.regeln[regel]
                text = regel.anzeigename
                if regel.probe:
                    text += f" ({regel.probe})"
                self.querverweiseResolved[text] = regel.text
            elif ref.startswith("Vorteil:"):
                vorteil = ref[len("Vorteil:"):]
                if vorteil not in db.vorteile:
                    continue
                vorteil = db.vorteile[vorteil]
                self.querverweiseResolved[vorteil.name] = vorteil.text
            elif ref.startswith("Talent:"):
                talent = ref[len("Talent:"):]
                if talent not in db.talente:
                    continue
                talent = db.talente[talent]
                self.querverweiseResolved[talent.anzeigename] = talent.text
            elif ref.startswith("Waffeneigenschaft:"):
                we = ref[len("Waffeneigenschaft:"):]
                if we not in db.waffeneigenschaften:
                    continue
                we = db.waffeneigenschaften[we]
                self.querverweiseResolved[we.name] = we.text
            elif ref.startswith("Abgeleiteter Wert:"):
                wert = ref[len("Abgeleiteter Wert:"):]
                if wert not in db.abgeleiteteWerte:
                    continue
                wert = db.abgeleiteteWerte[wert]
                titel = f"{wert.anzeigename} ({wert.name})" if wert.anzeigename else wert.name
                self.querverweiseResolved[titel] = wert.text
            elif ref == "Finanzen":
                self.querverweiseResolved["Finanzen"] = db.einstellungen["Finanzen: Beschreibung"].wert
            elif ref == "Statusse":
                self.querverweiseResolved["Statusse"] = db.einstellungen["Statusse: Beschreibung"].wert

    def executeScript(self, api):
        exec(self.scriptCompiled, api)

    def typname(self, db):
        typ = min(self.typ, len(db.einstellungen['Vorteile: Typen'].wert) - 1)
        return db.einstellungen['Vorteile: Typen'].wert[typ]

    def details(self, db):
        text = f"{self.kosten} EP. {self.text}"
        if self.script:
            text += f"\nScript: {self.script}"
        return text

class Vorteil:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter
        self._kostenOverride = None
        self._voraussetzungenOverride = None
        self._kommentar = ""
        self.anzeigenameExt = self.definition.name
        self._updateAnzeigenameExt()

    def __deepcopy__(self, memo=""):
        V = Vorteil(self.definition, self.charakter)
        V._kostenOverride = self._kostenOverride
        if self._voraussetzungenOverride:
            V._voraussetzungenOverride = self._voraussetzungenOverride.copy()
        V._kommentar = self._kommentar
        V.anzeigenameExt = self.anzeigenameExt
        return V

    def executeScript(self):
        self.definition.executeScript(self.charakter.charakterScriptAPI)

    @property
    def name(self):
        return self.definition.name

    @property
    def kosten(self):
        kosten = self.definition.kosten
        if self._kostenOverride is not None:
            kosten = self._kostenOverride
        return EventBus.applyFilter("vorteil_kosten", kosten, { "charakter" : self.charakter, "vorteil" : self.name })

    @kosten.setter
    def kosten(self, kosten):
        self._kostenOverride = kosten
        self._updateAnzeigenameExt()

    @property
    def variableKosten(self):
        return self.definition.variableKosten

    @property
    def kommentarErlauben(self):
        return self.definition.kommentarErlauben

    @property
    def typ(self):
        return self.definition.typ

    @property
    def voraussetzungen(self):
        if self._voraussetzungenOverride is not None:
            return self._voraussetzungenOverride
        return self.definition.voraussetzungen

    @voraussetzungen.setter
    def voraussetzungen(self, voraussetzungen):
        self._voraussetzungenOverride = voraussetzungen

    @property
    def nachkauf(self):
        return self.definition.nachkauf

    @property
    def text(self):
        return self.definition.text

    @property
    def info(self):
        return self.definition.info
    
    @property
    def bedingungen(self):
        return self.definition.bedingungen

    @property
    def cheatsheetAuflisten(self):
        return self.definition.cheatsheetAuflisten

    @property
    def cheatsheetBeschreibung(self):
        return self.definition.cheatsheetBeschreibung

    @property
    def linkKategorie(self):
        return self.definition.linkKategorie

    @property
    def linkElement(self):
        return self.definition.linkElement

    @property
    def script(self):
        return self.definition.script

    @property
    def scriptPrio(self):
        return self.definition.scriptPrio

    @property
    def querverweise(self):
        return self.definition.querverweise

    @property
    def querverweiseResolved(self):
        return self.definition.querverweiseResolved

    @property
    def kommentar(self):
        return self._kommentar

    @kommentar.setter
    def kommentar(self, kommentar):
        self._kommentar = kommentar
        self._updateAnzeigenameExt()

    def typname(self, db):
        return self.definition.typname(db)

    def _updateAnzeigenameExt(self):
        self.anzeigenameExt = self.definition.name    
        ep = None
        kommentar = None
        if self.variableKosten:
            ep = str(self.kosten)

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
