from Wolke import Wolke
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden
from VoraussetzungenListe import VoraussetzungenListe
import copy

# Implementation for Fertigkeiten. Using the type object pattern.
# FertigkeitDefinition: type object, initialized with database values
# Fertigkeit: character editor values, initialised with definition but supports overrides

class KampffertigkeitTyp():
   Keine = 0
   Nahkampf = 1 #sf 4/2
   Sonstige = 2 #fernkampf, athletik

class FertigkeitDefinition:
    displayName = "Fertigkeit (profan)"
    serializationName = "Fertigkeit"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.steigerungsfaktor = 0
        self.text = ''
        self.attribute = ['KO','KO','KO']
        self.kampffertigkeit = KampffertigkeitTyp.Keine
        self.voraussetzungen = VoraussetzungenListe()
        self.kategorie = 0
        self.talenteGruppieren = False

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        pass

    def kategorieName(self, db):
        kategorie = min(self.kategorie, len(db.einstellungen['Fertigkeiten: Kategorien profan'].wert) - 1)
        return db.einstellungen['Fertigkeiten: Kategorien profan'].wert.keyAtIndex(kategorie)

    def details(self, db):
        return f"{'/'.join(self.attribute)}. SF {self.steigerungsfaktor}. {self.text}"

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('voraussetzungen', self.voraussetzungen.text)
        ser.set('steigerungsfaktor', self.steigerungsfaktor)
        ser.set('attribute', Hilfsmethoden.AttrArray2Str(self.attribute))
        ser.set('kampffertigkeit', self.kampffertigkeit)
        ser.set('kategorie', self.kategorie)
        EventBus.doAction("fertigkeitdefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.voraussetzungen.compile(ser.get('voraussetzungen', ''))
        self.steigerungsfaktor = ser.getInt('steigerungsfaktor')
        self.attribute = Hilfsmethoden.AttrStr2Array(ser.get('attribute'))
        self.kampffertigkeit = ser.getInt('kampffertigkeit')
        self.kategorie = ser.getInt('kategorie', self.kategorie)
        EventBus.doAction("fertigkeitdefinition_deserialisiert", { "object" : self, "deserializer" : ser})

class UeberFertigkeitDefinition(FertigkeitDefinition):
    displayName = "Fertigkeit (übernatürlich)"
    serializationName = "ÜbernatürlicheFertigkeit"

    def __init__(self):
        super().__init__()

    def kategorieName(self, db):
        kategorie = min(self.kategorie, len(db.einstellungen['Fertigkeiten: Kategorien übernatürlich'].wert) - 1)
        return db.einstellungen['Fertigkeiten: Kategorien übernatürlich'].wert.keyAtIndex(kategorie)

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('voraussetzungen', self.voraussetzungen.text)
        ser.set('steigerungsfaktor', self.steigerungsfaktor)
        ser.set('attribute', Hilfsmethoden.AttrArray2Str(self.attribute))
        ser.set('kategorie', self.kategorie)
        ser.set('talentegruppieren', self.talenteGruppieren)
        EventBus.doAction("ueberfertigkeitdefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.voraussetzungen.compile(ser.get('voraussetzungen', ''))
        self.steigerungsfaktor = ser.getInt('steigerungsfaktor')
        self.attribute = Hilfsmethoden.AttrStr2Array(ser.get('attribute'))
        self.kategorie = ser.getInt('kategorie', self.kategorie)
        self.talenteGruppieren = ser.getBool('talentegruppieren', self.talenteGruppieren)
        EventBus.doAction("ueberfertigkeitdefinition_deserialisiert", { "object" : self, "deserializer" : ser})

class Fertigkeit:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter
        self.wert = 0
        self.gekaufteTalente = []
        self.talentMods = {} # for vorteil scripts, only used in export { talentnname1 : { condition1 : mod1, condition2 : mod2, ... }, talentname2 : {}, ... 
        self.attributswerte = [-1,-1,-1]
        self.basiswert = -1
        self.basiswertMod = 0 # may be set by vorteil scripts, not used in calculations for bw, pw, pwt, only in ui and pdf (requirements checks would be a nightmare)
        self.probenwert = -1
        self.probenwertTalent = -1
        self.maxWert = -1
        self.addToPDF = False # only used by ueber fert, bit fishy

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
    def steigerungsfaktor(self):
        return self.definition.steigerungsfaktor

    @property
    def text(self):
        return self.definition.text

    @property
    def attribute(self):
        return self.definition.attribute

    @property
    def kampffertigkeit(self):
        return self.definition.kampffertigkeit

    @property
    def voraussetzungen(self):
        return self.definition.voraussetzungen

    @property
    def kategorie(self):
        return self.definition.kategorie

    @property
    def talenteGruppieren(self):
        return self.definition.talenteGruppieren

    def diffBasiswert(self, attribute):
        attributswerte = []
        for attribut in self.attribute:
            attributswerte.append(attribute[attribut].wert)
        scriptAPI = { 'getAttribute' : lambda: attributswerte }
        basiswert = eval(Wolke.DB.einstellungen["Fertigkeiten: BW Script"].wert, scriptAPI)
        return basiswert - self.basiswert

    def aktualisieren(self):
        self.attributswerte = []
        for attribut in self.attribute:
            self.attributswerte.append(self.charakter.attribute[attribut].wert)

        scriptAPI = { 'getAttribute' : lambda: self.attributswerte }
        self.maxWert = eval(Wolke.DB.einstellungen["Fertigkeiten: Maximalwert Script"].wert, scriptAPI)
        self.basiswert = eval(Wolke.DB.einstellungen["Fertigkeiten: BW Script"].wert, scriptAPI)
        self.wert = min(self.wert, self.maxWert)
        scriptAPI['getWert'] = lambda: self.wert
        scriptAPI['getBasiswert'] = lambda: self.basiswert
        self.probenwert = eval(Wolke.DB.einstellungen["Fertigkeiten: PW Script"].wert, scriptAPI)
        self.probenwertTalent = eval(Wolke.DB.einstellungen["Fertigkeiten: PWT Script"].wert, scriptAPI)

    @staticmethod
    def getHöchsteKampffertigkeit(fertigkeiten):
        höchste = None
        for fert in fertigkeiten.values():
            if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf and (höchste is None or fert.wert > höchste.wert):
                höchste = fert
        return höchste

    def steigerungskosten(self, numSteigerungen = 1):
        if numSteigerungen == 0 or (numSteigerungen > 0 and self.wert == self.maxWert):
           return 0

        startWert = self.wert
        multiplier = 1
        if numSteigerungen < 0:
            startWert = max(self.wert + numSteigerungen, 0)
            numSteigerungen = self.wert - startWert
            multiplier = -1

        numSteigerungen = min(numSteigerungen, self.maxWert - startWert)
        sf = self.steigerungsfaktor

        sf4AbWert = None
        if self.kampffertigkeit == KampffertigkeitTyp.Nahkampf:
            höchste = Fertigkeit.getHöchsteKampffertigkeit(self.charakter.fertigkeiten)
            sf4AbWert = höchste.wert + 1

        kosten = 0
        nextWert = startWert + 1
        for i in range(numSteigerungen):
            if (sf4AbWert is not None) and nextWert >= sf4AbWert:
                sf = 4
            kosten += nextWert * sf
            nextWert += 1
        kosten *= multiplier
        return EventBus.applyFilter("fertigkeit_kosten", kosten, { "charakter" : self.charakter, "name" : self.name, "wertVon" : startWert, "wertAuf" : startWert + numSteigerungen })

    def kategorieName(self, db):
        return self.definition.kategorieName(db)

    def kosten(self):
        kosten = sum(range(self.wert+1)) * self.steigerungsfaktor
        if self.kampffertigkeit == KampffertigkeitTyp.Nahkampf:
            höchste = Fertigkeit.getHöchsteKampffertigkeit(self.charakter.fertigkeiten)
            if self == höchste:
                kosten += max(0, 2*sum(range(höchste.wert+1)))
        return EventBus.applyFilter("fertigkeit_kosten", kosten, { "charakter" : self.charakter, "name" : self.name, "wertVon" : 0, "wertAuf" : self.wert })

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('wert', self.wert)
        if isinstance(self.definition, UeberFertigkeitDefinition):
            ser.set('exportieren', self.addToPDF)
        EventBus.doAction("fertigkeit_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, db, char):
        name = ser.get('name')
        if name not in db:
            self.definition = FertigkeitDefinition()
            self.definition.name = name
            return False
        self.__init__(db[name], char)
        self.wert = ser.getInt('wert', self.wert)
        self.addToPDF = ser.getBool('exportieren', self.addToPDF)
        self.aktualisieren()
        EventBus.doAction("fertigkeit_deserialisiert", { "object" : self, "deserializer" : ser})
        return True