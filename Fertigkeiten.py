'''
In dieser Datei wird das Backend für Fertigkeiten und Attribute gelegt.
Alle steigerbaren Traits verfügen über die Funktionen steigern() und senken()
'''

from Definitionen import Attribute
from Wolke import Wolke

# Allgemeine Implementation für steigerbare Traits
class Steigerbar(object):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.wert = 0
        self.steigerungsfaktor = 0
        self.text = ''
    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

# Implementation für Attribute: SF ist 16, PW ist 2x Wert
class Attribut(Steigerbar):
    def __init__(self, Key):
        super().__init__()
        self.steigerungsfaktor = 16
        self.probenwert = 0
        self.name = Attribute[Key]
        self.key = Key
    def aktualisieren(self):
        self.probenwert = self.wert*2
    

# Implementation für Steigerbare Energien (Karma und AsP). SF ist 1, kein Limit.
class Energie(Steigerbar):
    def __init__(self):
        super().__init__()
        self.steigerungsfaktor = 1

# Implementation für freie Fertigkeiten
class FreieFertigkeit(Steigerbar):
    def __init__(self):
        super().__init__()
        self.steigerungsfaktor = -1
    def __deepcopy__(self, memo=""):
        F = FreieFertigkeit()
        F.name = self.name
        F.steigerungsfaktor = -1
        F.wert = self.wert
        return F

# Implementation für Fertigkeiten im Allgemeinen
class Fertigkeit(Steigerbar):
    def __init__(self):
        super().__init__()
        self.gekaufteTalente = []
        self.kampffertigkeit = 0; #0 = nein, 1 = nahkampffertigkeit, 2 = sonstige kampffertigkeit
        self.attribute = ['KO','KO','KO']
        self.attributswerte = [-1,-1,-1]
        self.basiswert = -1
        self.probenwert = -1
        self.probenwertTalent = -1
        self.voraussetzungen = []
        self.maxWert = -1
        self.isUserAdded = True

    def aktualisieren(self):
        self.attributswerte = [Wolke.Char.attribute[self.attribute[0]].wert, 
                               Wolke.Char.attribute[self.attribute[1]].wert,
                               Wolke.Char.attribute[self.attribute[2]].wert]
        self.maxWert = max(self.attributswerte)+2
        # Python Round does mess up sometimes
        self.basiswert = round(sum(self.attributswerte)/3+0.0001)
        self.probenwert = self.basiswert + round(self.wert/2+0.0001)
        self.probenwertTalent = self.basiswert + self.wert
    def __deepcopy__(self, memo=""):
        F = Fertigkeit()
        F.name = self.name
        F.wert = self.wert
        F.steigerungsfaktor = self.steigerungsfaktor
        F.text = self.text
        F.voraussetzungen = self.voraussetzungen.copy()
        F.attribute = self.attribute.copy()
        F.kampffertigkeit = self.kampffertigkeit
        F.gekaufteTalente = self.gekaufteTalente.copy()
        F.attributswerte = self.attributswerte.copy()
        F.basiswert = self.basiswert
        F.probenwert = self.probenwert
        F.probenwertTalent = -self.probenwertTalent
        F.maxWert = self.maxWert
        F.isUserAdded = self.isUserAdded
        return F

class Talent():
    def __init__(self):
        self.name = ''
        self.kosten = -1
        self.verbilligt = 0
        self.fertigkeiten = []
        self.voraussetzungen = []
        self.variable = 0
        self.text = ''
        self.printclass = -1
        self.isUserAdded = True
    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__  
    def isSpezialTalent(self):
        return self.kosten != -1

class Vorteil():
    def __init__(self):
        self.name = ''
        self.kosten = -1
        self.variable = 0
        self.typ = 0
        self.voraussetzungen = []
        self.nachkauf = ''
        self.text = ''
        self.script = None
        self.scriptPrio = 0
        self.isUserAdded = True
    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        if self.__dict__ == other.__dict__: return True

class Manoever():
    def __init__(self):
        self.name = ''
        self.typ = 0
        self.voraussetzungen = []
        self.probe = ''
        self.gegenprobe = ''
        self.text = ''
        self.isUserAdded = True
    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        if self.__dict__ == other.__dict__: return True