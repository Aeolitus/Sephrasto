from Wolke import Wolke
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden

# Implementation for freie Fertigkeiten. Using the type object pattern.
# FreieFertigkeitDefinition: type object, initialized with database values
# FreieFertigkeit: character editor values, initialised with definition but supports overrides.
# Since users can enter these freely, definitions may be created on the fly.

class FreieFertigkeitDefinition:
    displayName = "Freie Fertigkeit"
    steigerungskosten = None
    gesamtkosten = None

    def __init__(self):
        # Serialized properties
        self.name = ""
        self.kategorie = ""
        self.voraussetzungen = []

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        if FreieFertigkeitDefinition.steigerungskosten is None:
            FreieFertigkeitDefinition.steigerungskosten = [
                0,
                db.einstellungen["FreieFertigkeiten: Kosten Stufe1"].wert, 
                db.einstellungen["FreieFertigkeiten: Kosten Stufe2"].wert, 
                db.einstellungen["FreieFertigkeiten: Kosten Stufe3"].wert
            ]

            FreieFertigkeitDefinition.gesamtkosten = FreieFertigkeitDefinition.steigerungskosten.copy()
            FreieFertigkeitDefinition.gesamtkosten[2] += FreieFertigkeitDefinition.gesamtkosten[1]
            FreieFertigkeitDefinition.gesamtkosten[3] += FreieFertigkeitDefinition.gesamtkosten[2]

    def typname(self, db):
        return self.kategorie

    def details(self, db):
        return Hilfsmethoden.VorArray2Str(self.voraussetzungen)

class FreieFertigkeit:
    def __init__(self, definition, charakter):
        super().__init__()
        self.definition = definition
        self.charakter = charakter
        self.wert = 0

    def __deepcopy__(self, memo=""):
        F = FreieFertigkeit(self.definition, self.charakter)
        F.wert = self.wert
        return F

    @property
    def name(self):
        return self.definition.name

    @property
    def kategorie(self):
        return self.definition.kategorie

    @property
    def voraussetzungen(self):
        return self.definition.voraussetzungen

    def typname(self, db):
        return self.definition.typname(db)

    def steigerungskosten(self, numSteigerungen = 1):
        if numSteigerungen < 1 or self.wert == 3:
           return 0
        numSteigerungen = min(numSteigerungen, 3 - self.wert)
        kosten = FreieFertigkeitDefinition.gesamtkosten[self.wert+numSteigerungen] - FreieFertigkeitDefinition.gesamtkosten[self.wert]
        return EventBus.applyFilter("freiefertigkeit_kosten", kosten, { "charakter" : self.charakter, "name" : self.name, "wertVon" : self.wert, "wertAuf" : self.wert+numSteigerungen })

    def kosten(self):
        if self.wert == 0:
            return 0
        kosten = FreieFertigkeitDefinition.gesamtkosten[self.wert]
        return EventBus.applyFilter("freiefertigkeit_kosten", kosten, { "charakter" : self.charakter, "name" : self.name, "wertVon" : 0, "wertAuf" : self.wert })
