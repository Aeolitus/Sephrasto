from Wolke import Wolke
import logging
from EventBus import EventBus
from VoraussetzungenListe import VoraussetzungenListe
import copy

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
    serializationName = "Vorteil"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.info = ''
        self.bedingungen = ''
        self.kosten = 0
        self.variableKosten = False
        self.kommentarErlauben = False
        self.kategorie = 0
        self.voraussetzungen = VoraussetzungenListe()
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

    def kategorieName(self, db):
        kategorie = min(self.kategorie, len(db.einstellungen['Vorteile: Kategorien'].wert) - 1)
        return db.einstellungen['Vorteile: Kategorien'].wert.keyAtIndex(kategorie)

    def details(self, db):
        text = f"{self.kosten} EP. {self.text}"
        if self.script:
            text += f"\nScript: {self.script}"
        return text

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('voraussetzungen', self.voraussetzungen.text)
        ser.set('kosten', self.kosten)
        ser.set('nachkauf', self.nachkauf)
        ser.set('kategorie', self.kategorie)
        if self.script:
            ser.set('script', self.script)
        if self.scriptPrio != 0:
            ser.set('scriptPrio', self.scriptPrio)
        if len(self.querverweise) > 0:
            ser.set('querverweise', " | ".join(self.querverweise))    
        ser.set('variableKosten', self.variableKosten)
        ser.set('kommentar', self.kommentarErlauben)
        if not self.cheatsheetAuflisten:
            ser.set('csAuflisten', False)
        if self.cheatsheetBeschreibung:
            ser.set('csBeschreibung', self.cheatsheetBeschreibung)
        if self.linkKategorie > 0:
            ser.set('linkKategorie', self.linkKategorie)
        if self.linkElement:
            ser.set('linkElement', self.linkElement)
        if self.info:
            ser.set('info', self.info)
        if self.bedingungen:
            ser.set('bedingungen', self.bedingungen)
        EventBus.doAction("vorteildefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.voraussetzungen.compile(ser.get('voraussetzungen', ''))
        self.kosten = ser.getInt('kosten')
        self.nachkauf = ser.get('nachkauf')
        self.kategorie = ser.getInt('kategorie')
        self.script = ser.get('script', "")
        self.scriptPrio = ser.getInt('scriptPrio', self.scriptPrio)
        querverweise = ser.get('querverweise', '')
        if querverweise:
            self.querverweise = list(map(str.strip, querverweise.split("|")))
        self.variableKosten = ser.getBool('variableKosten', self.variableKosten)
        self.kommentarErlauben = ser.getBool('kommentar', self.kommentarErlauben)
        if self.variableKosten:
            self.kommentarErlauben = True
        self.cheatsheetAuflisten = ser.getBool('csAuflisten', self.cheatsheetAuflisten)
        self.cheatsheetBeschreibung = ser.get('csBeschreibung', self.cheatsheetBeschreibung)
        self.linkKategorie = ser.getInt('linkKategorie', self.linkKategorie)
        self.linkElement = ser.get('linkElement', self.linkElement)
        self.info = ser.get('info', self.info)
        self.bedingungen = ser.get('bedingungen', self.bedingungen)
        EventBus.doAction("vorteildefinition_deserialisiert", { "object" : self, "deserializer" : ser})

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
    def kategorie(self):
        return self.definition.kategorie

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

    def kategorieName(self, db):
        return self.definition.kategorieName(db)

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

    def serialize(self, ser):
        ser.set('name', self.name)
        if self.variableKosten:
            ser.set('variableKosten', self.kosten)
        if self.kommentarErlauben:
            ser.set('kommentar', self.kommentar)
        EventBus.doAction("vorteil_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, db, char):
        name = ser.get('name')
        if name not in db:
            self.definition = VorteilDefinition()
            self.definition.name = name
            return False
        self.__init__(db[name], char)
        if self.variableKosten:
            self.kosten = ser.getInt('variableKosten', self.kosten)
        if self.kommentarErlauben:
            self.kommentar = ser.get('kommentar', self.kommentar)
        EventBus.doAction("vorteil_deserialisiert", { "object" : self, "deserializer" : ser})
        return True