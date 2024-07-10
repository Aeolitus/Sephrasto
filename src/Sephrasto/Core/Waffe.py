from EventBus import EventBus
import copy

# Implementation for Waffen. Using the type object pattern.
# WaffeDefinition: type object, initialized with database values
# Waffe: character editor values, initialised with definition but supports overrides.

class WaffeDefinition:
    displayName = "Waffe"
    serializationName = "Waffe"
    keinKampfstil = "Kein Kampfstil"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.würfel = 0
        self.würfelSeiten = 6
        self.plus = 0
        self.eigenschaften = []
        self.härte = 6
        self.rw = 0
        self.wm = 0
        self.fertigkeit = ''
        self.talent = ''
        self.kampfstile = []
        self.lz = 0
        self.fernkampf = False

        # Derived properties after deserialization
        self.anzeigename = ''

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.name == other.name and \
            self.würfel == other.würfel and \
            self.würfelSeiten == other.würfelSeiten and \
            self.plus == other.plus and \
            self.eigenschaften == other.eigenschaften and \
            self.härte == other.härte and \
            self.rw == other.rw and \
            self.wm == other.wm and \
            self.fertigkeit == other.fertigkeit and \
            self.talent == other.talent and \
            self.kampfstile == other.kampfstile and \
            self.lz == other.lz and \
            self.fernkampf == other.fernkampf
    
    def finalize(self, db):
        self.anzeigename = self.name
        for trim in [f" ({self.talent})", " (NK)", " (FK)"]:
            if self.anzeigename.endswith(trim):
                self.anzeigename = self.anzeigename[:-len(trim)]

    @property
    def nahkampf(self):
        return not self.fernkampf

    def kategorieName(self, db):
        return self.talent

    def details(self, db):
        lz = ""
        if self.fernkampf:
            lz = f"| LZ {self.lz} "
        eigenschaften = " -"
        if len(self.eigenschaften) > 0:
            eigenschaften = ', '.join(self.eigenschaften)

        return f"TP {self.würfel}W{self.würfelSeiten}{'+' if self.plus >= 0 else ''}{self.plus} | WM {self.wm} | RW {self.rw} {lz}| Härte {self.härte} | {eigenschaften}"

    def isATVerboten(self, db):
        return self.talent in db.einstellungen["Waffen: Talente AT verboten"].wert or \
            self.name in db.einstellungen["Waffen: Talente AT verboten"].wert

    def isVTVerboten(self, db):
        return self.talent in db.einstellungen["Waffen: Talente VT verboten"].wert or \
            self.name in db.einstellungen["Waffen: Talente VT verboten"].wert

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', ", ".join(self.eigenschaften))
        ser.set('würfel', self.würfel)
        ser.set('würfelSeiten', self.würfelSeiten)
        ser.set('plus', self.plus)
        ser.set('härte', self.härte)
        ser.set('fertigkeit', self.fertigkeit)
        ser.set('talent', self.talent)
        ser.set('kampfstile', ", ".join(self.kampfstile))
        ser.set('rw', self.rw)
        ser.set('wm', self.wm)
        if self.fernkampf:
            ser.set('fk', True)
            ser.set('lz', self.lz)
        else:
            ser.set('fk', False)
        EventBus.doAction("waffedefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, referenceDB = None):
        self.name = ser.get('name')
        eigenschaften = ser.get('text')
        if eigenschaften:
            self.eigenschaften = list(map(str.strip, eigenschaften.split(",")))
        self.würfel = ser.getInt('würfel')
        self.würfelSeiten = ser.getInt('würfelSeiten')
        self.plus = ser.getInt('plus')
        self.härte = ser.getInt('härte')
        self.fertigkeit = ser.get('fertigkeit')
        self.talent = ser.get('talent')
        kampfstile = ser.get('kampfstile', '')
        if kampfstile:
            self.kampfstile = sorted(list(map(str.strip, kampfstile.split(","))))
        self.rw = ser.getInt('rw')
        self.wm = ser.getInt('wm')
        self.fernkampf = ser.getBool('fk')
        if self.fernkampf:
            self.lz = ser.getInt('lz')
        EventBus.doAction("waffedefinition_deserialisiert", { "object" : self, "deserializer" : ser})

class Waffe:
    def __init__(self, definition):
        self.definition = definition
        self._lzOverride = None
        self._wmOverride = None
        self._rwOverride = None
        self._würfelOverride = None
        self._würfelSeitenOverride = None
        self._plusOverride = None
        self._eigenschaftenOverride = None
        self._härteOverride = None
        self._anzeigenameOverride = None
        self.kampfstil = WaffeDefinition.keinKampfstil
        self.beSlot = 1
        
        self.resetScriptValues()

    def __deepcopy__(self, memo=""):
        # create new object
        cls = self.__class__
        result = cls.__new__(cls)
        # deepcopy everything except for self and definition
        memo[id(self)] = result
        memo[id(self.definition)] = self.definition
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def resetScriptValues(self):
        self.at = 0
        self.vt = 0
        self.lzMod = 0
        self.rwMod = 0
        self.würfelMod = 0
        self.plusMod = 0
        self.härteMod = 0

    @property
    def name(self):
        return self.definition.name

    @property
    def würfel(self):
        if self._würfelOverride is not None:
            return self._würfelOverride
        return self.definition.würfel

    @würfel.setter
    def würfel(self, würfel):
        self._würfelOverride = würfel

    @property
    def würfelFinal(self):
        return max(self.würfel + self.würfelMod, 0)

    @property
    def würfelSeiten(self):
        if self._würfelSeitenOverride is not None:
            return self._würfelSeitenOverride
        return self.definition.würfelSeiten

    @würfelSeiten.setter
    def würfelSeiten(self, würfelSeiten):
        self._würfelSeitenOverride = würfelSeiten

    @property
    def plus(self):
        if self._plusOverride is not None:
            return self._plusOverride
        return self.definition.plus

    @plus.setter
    def plus(self, plus):
        self._plusOverride = plus

    @property
    def plusFinal(self):
        return self.plus + self.plusMod

    @property
    def eigenschaften(self):
        if self._eigenschaftenOverride is not None:
            return self._eigenschaftenOverride
        return self.definition.eigenschaften

    @eigenschaften.setter
    def eigenschaften(self, eigenschaften):
        self._eigenschaftenOverride = eigenschaften

    @property
    def härte(self):
        if self._härteOverride is not None:
            return self._härteOverride
        return self.definition.härte

    @härte.setter
    def härte(self, härte):
        self._härteOverride = härte

    @property
    def härteFinal(self):
        return max(self.härte + self.härteMod, 1)

    @property
    def rw(self):
        if self._rwOverride is not None:
            return self._rwOverride
        return self.definition.rw

    @rw.setter
    def rw(self, rw):
        self._rwOverride = rw

    @property
    def rwFinal(self):
        return max(self.rw + self.rwMod, 0)

    @property
    def wm(self):
        if self._wmOverride is not None:
            return self._wmOverride
        return self.definition.wm

    @wm.setter
    def wm(self, wm):
        self._wmOverride = wm

    @property
    def fertigkeit(self):
        return self.definition.fertigkeit

    @property
    def talent(self):
        return self.definition.talent

    @property
    def kampfstile(self):
        return self.definition.kampfstile

    @property
    def lz(self):
        if self._lzOverride is not None:
            return self._lzOverride
        return self.definition.lz

    @lz.setter
    def lz(self, lz):
        self._lzOverride = lz

    @property
    def lzFinal(self):
        return max(self.lz + self.lzMod, 0)

    @property
    def fernkampf(self):
        return self.definition.fernkampf

    @property
    def nahkampf(self):
        return self.definition.nahkampf

    @property
    def anzeigename(self):
        if self._anzeigenameOverride is not None:
            return self._anzeigenameOverride
        return self.definition.anzeigename

    @anzeigename.setter
    def anzeigename(self, anzeigename):
        self._anzeigenameOverride = anzeigename

    def kategorieName(self, db):
        return self.definition.kategorieName(db)

    def isATVerboten(self, db):
        return self.definition.isATVerboten(db)

    def isVTVerboten(self, db):
        return self.definition.isVTVerboten(db)

    def serialize(self, ser):
        ser.set('name', self.anzeigename)
        ser.set('id', self.name)
        ser.set('würfel', self.würfel)
        ser.set('würfelSeiten', self.würfelSeiten)
        ser.set('plus', self.plus)
        ser.set('eigenschaften', ", ".join(self.eigenschaften))
        ser.set('härte', self.härte)
        ser.set('rw', self.rw)
        ser.set('beSlot', self.beSlot)
        ser.set('kampfstil', self.kampfstil)
        ser.set('wm', self.wm)
        if self.fernkampf:
            ser.set('lz', self.lz)
        EventBus.doAction("waffe_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, db, char):
        name = ser.get('id')
        if name not in db:
            self.definition = WaffeDefinition()
            self.definition.name = name
            return False
        self.__init__(db[name])

        if self.fernkampf:
            self.lz = ser.getInt('lz', self.lz)
        self.wm = ser.getInt('wm', self.wm)
        self.anzeigename = ser.get('name', self.anzeigename)
        self.rw = ser.getInt('rw', self.rw)
        self.würfel = ser.getInt('würfel', self.würfel)
        self.würfelSeiten = ser.getInt('würfelSeiten', self.würfelSeiten)
        self.plus = ser.getInt('plus', self.plus)
        eigenschaften = ser.get('eigenschaften')
        if eigenschaften:
            self.eigenschaften = list(map(str.strip, eigenschaften.split(", ")))
        self.härte = ser.getInt('härte', self.härte)
        self.beSlot = ser.getInt('beSlot', self.beSlot)
        self.kampfstil = ser.get('kampfstil', self.kampfstil)
        EventBus.doAction("waffe_deserialisiert", { "object" : self, "deserializer" : ser})
        return True