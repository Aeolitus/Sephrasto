from Wolke import Wolke
from EventBus import EventBus
import copy

# Implementation for Attribute. Using the type object pattern.
# AttributDefinition: type object, initialized with database values
# Attribut: character editor values, initialised with definition but supports overrides
class AttributDefinition:
    displayName = "Attribut"
    serializationName = "Attribut"

    def __init__(self):
        # Serialized properties
        self.name = ""
        self.anzeigename = ""
        self.text = ""
        self.steigerungsfaktor = 16
        self.sortorder = 0

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        pass

    def details(self, db):
        return f"SF {self.steigerungsfaktor}. {self.text}"

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('anzeigename', self.anzeigename)
        ser.set('steigerungsfaktor', self.steigerungsfaktor)
        ser.set('sortorder', self.sortorder)
        EventBus.doAction("attributdefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.anzeigename = ser.get('anzeigename')
        self.steigerungsfaktor = ser.getInt('steigerungsfaktor')
        self.sortorder = ser.getInt('sortorder')
        EventBus.doAction("attributdefinition_deserialisiert", { "object" : self, "deserializer" : ser})

class Attribut:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter
        self.wert = 0
        self.probenwert = 0

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
    def anzeigename(self):
        return self.definition.anzeigename

    @property
    def text(self):
        return self.definition.text
    
    @property
    def steigerungsfaktor(self):
        return self.definition.steigerungsfaktor

    @property
    def sortorder(self):
        return self.definition.sortorder

    def aktualisieren(self):
        scriptAPI = { 'getWert' : lambda: self.wert }
        self.probenwert = eval(Wolke.DB.einstellungen["Attribute: PW Script"].wert, scriptAPI)

    def steigerungskosten(self, numSteigerungen = 1):
        if numSteigerungen == 0:
           return 0
        startWert = self.wert
        multiplier = 1
        if numSteigerungen < 0:
            startWert = max(self.wert + numSteigerungen, 0)
            numSteigerungen = self.wert - startWert
            multiplier = -1

        kosten = 0
        nextWert = startWert +1
        for i in range(numSteigerungen):
            kosten += nextWert * self.steigerungsfaktor
            nextWert += 1
        kosten *= multiplier
        return EventBus.applyFilter("attribut_kosten", kosten, { "charakter" : self.charakter, "attribut" : self.name, "wertVon" : startWert, "wertAuf" : startWert + numSteigerungen })

    def kosten(self):
        kosten = sum(range(self.wert+1)) * self.steigerungsfaktor
        return EventBus.applyFilter("attribut_kosten", kosten, { "charakter" : self.charakter, "attribut" : self.name, "wertVon" : 0, "wertAuf" : self.wert })

    def serialize(self, ser):
        ser.set("name", self.name)
        ser.set("wert", self.wert)
        EventBus.doAction("attribut_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, db, char):
        name = ser.get('name')
        if name not in db:
            self.definition = AttributDefinition()
            self.definition.name = name
            return False
        self.__init__(db[name], char)
        self.wert = ser.getInt("wert", self.wert)
        self.aktualisieren()
        EventBus.doAction("attribut_deserialisiert", { "object" : self, "deserializer" : ser})
        return True