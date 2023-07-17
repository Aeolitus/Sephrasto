from Wolke import Wolke
from EventBus import EventBus

# Implementation for Attribute. Using the type object pattern.
# AttributDefinition: type object, initialized with database values
# Attribut: character editor values, initialised with definition but supports overrides
class AttributDefinition:
    displayName = "Attribut"

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

class Attribut:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter
        self.wert = 0
        self.probenwert = 0

    def __deepcopy__(self, memo=""):
        A = Attribut(self.definition, self.charakter)
        A.wert = self.wert
        A.probenwert = self.probenwert
        return A

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
