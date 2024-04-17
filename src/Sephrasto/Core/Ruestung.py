from Wolke import Wolke
from EventBus import EventBus
import copy
from Hilfsmethoden import Hilfsmethoden

# Implementation for Rüstungen. Using the type object pattern.
# RuestungDefinition: type object, initialized with database values
# Ruestung: character editor values, initialised with definition but supports overrides.
# Since users can enter these freely, definitions may be created on the fly.

class RuestungDefinition:
    displayName = "Rüstung"
    serializationName = "Rüstung"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.kategorie = 0
        self.system = 0
        self.rs = [0,0,0,0,0,0] # Bein LArm RArm Bauch Brust Kopf

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        pass

    def getRSGesamt(self):
        return round(sum(self.rs) / 6, 2)

    def getRSGesamtInt(self):
        return int(sum(self.rs) / 6 + 0.5)

    def kategorieName(self, db):
        kategorie = min(self.kategorie, len(db.einstellungen['Rüstungen: Kategorien'].wert) - 1)
        return db.einstellungen['Rüstungen: Kategorien'].wert.keyAtIndex(kategorie)

    def details(self, db):
        system = "Beide Systeme"
        if self.system == 1:
            system = "Einfaches System"
        elif self.system == 2:
            system = "Zonensystem"
        return f"{system} | RS {self.getRSGesamtInt()} (Bein {self.rs[0]} | L. Arm {self.rs[1]} | R. Arm {self.rs[2]} | Bauch {self.rs[3]} | Brust {self.rs[4]} | Kopf {self.rs[5]}).\n{self.text}"

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('kategorie', self.kategorie)
        ser.set('system', self.system)
        ser.set('rsBeine', self.rs[0])
        ser.set('rsLArm', self.rs[1])
        ser.set('rsRArm', self.rs[2])
        ser.set('rsBauch', self.rs[3])
        ser.set('rsBrust', self.rs[4])
        ser.set('rsKopf', self.rs[5])
        EventBus.doAction("ruestungdefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.kategorie = ser.getInt('kategorie')
        self.system = ser.getInt('system')
        self.rs[0] = ser.getInt('rsBeine')
        self.rs[1] = ser.getInt('rsLArm')
        self.rs[2] = ser.getInt('rsRArm')
        self.rs[3] = ser.getInt('rsBauch')
        self.rs[4] = ser.getInt('rsBrust')
        self.rs[5] = ser.getInt('rsKopf')
        EventBus.doAction("ruestungdefinition_deserialisiert", { "object" : self, "deserializer" : ser})

class Ruestung:
    def __init__(self, definition):
        self.definition = definition
        self._nameOverride = None
        self._beOverride = None
        self._kategorieOverride = None
        self._beOverride = None
        self._rsOverride = definition.rs.copy()

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

    @property
    def name(self):
        if self._nameOverride is not None:
            return self._nameOverride
        return self.definition.name

    @name.setter
    def name(self, name):
        self._nameOverride = name

    @property
    def text(self):
        return self.definition.text

    @property
    def kategorie(self):
        if self._kategorieOverride is not None:
            return self._kategorieOverride
        return self.definition.kategorie

    @kategorie.setter
    def kategorie(self, kategorie):
        self._kategorieOverride = kategorie

    @property
    def system(self):
        return self.definition.system

    @property
    def rs(self):
        return self._rsOverride

    @rs.setter
    def rs(self, rs):
        self._rsOverride = rs

    @property
    def be(self):
        if self._beOverride is not None:
            return self._beOverride
        return self.getRSGesamtInt()

    @be.setter
    def be(self, be):
        self._beOverride = be

    def kategorieName(self, db):
        return self.definition.kategorieName(db)

    def getRSGesamt(self):
        if self._rsOverride is not None:
            return round(sum(self._rsOverride) / 6, 2)
        return self.definition.getRSGesamt()

    def getRSGesamtInt(self):
        if self._rsOverride is not None:
            return int(sum(self._rsOverride) / 6 + 0.5)
        return self.definition.getRSGesamtInt()

    def __getScriptAPI(self, abgeleiteteWerte, zone = -1):
        scriptAPI = Hilfsmethoden.createScriptAPI()
        for ab in abgeleiteteWerte:
            scriptAPI['get' + ab + 'Basis'] = lambda ab=ab: abgeleiteteWerte[ab].basiswert
            scriptAPI['get' + ab] = lambda ab=ab: abgeleiteteWerte[ab].wert
            scriptAPI['get' + ab + 'Mod'] = lambda ab=ab: abgeleiteteWerte[ab].mod
        if zone == -1:
            scriptAPI["rs"] = self.getRSGesamtInt()
        else:
            scriptAPI["rs"] = self.rs[zone]
        scriptAPI["be"] = self.be
        return scriptAPI

    def getRSFinal(self, abgeleiteteWerte, zone = -1):
        return eval(Wolke.DB.einstellungen["Rüstungen: RS Script"].wert, self.__getScriptAPI(abgeleiteteWerte, zone))

    def getBEFinal(self, abgeleiteteWerte):
        return eval(Wolke.DB.einstellungen["Rüstungen: BE Script"].wert, self.__getScriptAPI(abgeleiteteWerte))

    def getWSFinal(self, abgeleiteteWerte):
        return eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, self.__getScriptAPI(abgeleiteteWerte))

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('be', self.be)
        ser.set('rs', Hilfsmethoden.RsArray2Str(self.rs))
        EventBus.doAction("ruestung_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, db, char):
        name = ser.get('name')
        if name in db:
            definition = db[name]
        else:
            definition = RuestungDefinition()
            definition.name = name

        self.__init__(definition)
        self.be = ser.getInt('be', self.be)
        self.rs = Hilfsmethoden.RsStr2Array(ser.get('rs'))
        EventBus.doAction("ruestung_deserialisiert", { "object" : self, "deserializer" : ser})
        return True