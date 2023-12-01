from Wolke import Wolke
from EventBus import EventBus
import copy

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
        self.typ = 0
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

    def typname(self, db):
        typ = min(self.typ, len(db.einstellungen['Rüstungen: Typen'].wert) - 1)
        return db.einstellungen['Rüstungen: Typen'].wert[typ]

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
        ser.set('typ', self.typ)
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
        self.typ = ser.getInt('typ')
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
        self._typOverride = None
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
    def typ(self):
        if self._typOverride is not None:
            return self._typOverride
        return self.definition.typ

    @typ.setter
    def typ(self, typ):
        self._typOverride = typ

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

    def typname(self, db):
        return self.definition.typname(db)

    def getRSGesamt(self):
        if self._rsOverride is not None:
            return round(sum(self._rsOverride) / 6, 2)
        return self.definition.getRSGesamt()

    def getRSGesamtInt(self):
        if self._rsOverride is not None:
            return int(sum(self._rsOverride) / 6 + 0.5)
        return self.definition.getRSGesamtInt()

    def __getScriptAPI(self, abgeleiteteWerte, zone = -1):
        scriptAPI = {}
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