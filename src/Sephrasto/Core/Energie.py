from EventBus import EventBus

# Implementation for Energien (Karma, AsP, GuP). Using the type object pattern.
# EnergieDefinition: type object, initialized with database values
# Energie: character editor values, initialised with definition but supports overrides
class EnergieDefinition:
    displayName = "Energie"

    def __init__(self):
        # Serialized properties
        self.name = ""
        self.anzeigename = ""
        self.text = ""
        self.steigerungsfaktor = 1
        self.voraussetzungen = []
        self.sortorder = 0

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        pass

    def details(self, db):
        return f"SF {self.steigerungsfaktor}. {self.text}"

class Energie:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter
        self.basiswert = 0
        self.wert = 0
        self.mod = 0

    def __deepcopy__(self, memo=""):
        E = Energie(self.definition, self.charakter)
        E.basiswert = self.basiswert
        E.wert = self.wert
        E.mod = self.mod
        return E

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
    def voraussetzungen(self):
        return self.definition.voraussetzungen

    @property
    def sortorder(self):
        return self.definition.sortorder

    @property
    def gesamtwert(self):
        return self.basiswert + self.wert + self.mod

    def steigerungskosten(self, numSteigerungen = 1):
        if numSteigerungen < 1:
           return 0
        kosten = 0
        nextWert = self.wert +1
        for i in range(numSteigerungen):
            kosten += nextWert * self.steigerungsfaktor
            nextWert += 1
        return EventBus.applyFilter("energie_kosten", kosten, { "charakter" : self.charakter, "energie" : self.name, "wertVon" : self.wert, "wertAuf" : self.wert + numSteigerungen })

    def kosten(self):
        kosten = sum(range(self.wert+1)) * self.steigerungsfaktor
        return EventBus.applyFilter("energie_kosten", kosten, { "charakter" : self.charakter, "energie" : self.name, "wertVon" : 0, "wertAuf" : self.wert })

    def aktualisieren(self):
        self.basiswert = 0
        self.mod = 0