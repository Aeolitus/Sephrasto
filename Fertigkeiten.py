'''
In dieser Datei wird das Backend für Fertigkeiten und Attribute gelegt.
Alle steigerbaren Traits verfügen über die Funktionen steigern() und senken()
'''

from Definitionen import FreieFertigkeitKosten, Attribute

# Allgemeine Implementation für steigerbare Traits
class Steigerbar:
    def __init__(self):
        self.name = ''
        self.wert = 0
        self.steigerungsfaktor = 0
        self.lernkosten = 0
        self.verlernkosten = 0
        self.text = ''
    def aktualisieren(self):
        self.lernkosten = (self.wert+1)*self.steigerungsfaktor
        self.verlernkosten = self.wert*self.steigerungsfaktor
    def steigern(self):
        self.wert += 1
        self.aktualisieren()
        return 1
    def senken(self):
        if self.wert > 0:
            self.wert -=1
            self.aktualisieren()
            return 1
        return 0

# Implementation für Attribute: SF ist 16, PW ist 2x Wert
class Attribut(Steigerbar):
    def __init__(self, Key):
        super().__init__()
        self.steigerungsfaktor = 16
        self.probenwert = 0
        self.name = Attribute[Key]
        self.key = Key
    def aktualisieren(self):
        super().aktualisieren()
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
    def aktualisieren(self):
        if self.wert < 3:
            self.lernkosten = FreieFertigkeitKosten[self.wert]
        else:
            self.lernkosten = -1
        if self.wert > 0:
            self.verlernkosten = FreieFertigkeitKosten[self.wert-1]
        else:
            self.verlernkosten = -1
    def steigern(self):
        if self.wert == 3:
            return 0
        self.wert += 1
        self.aktualisieren()
        return 1
    def senken(self):
        if self.wert == 0:
            return 0
        self.wert -= 1
        self.aktualisieren()

# Implementation für Fertigkeiten im Allgemeinen
class Fertigkeit(Steigerbar):
    def __init__(self):
        super().__init__()
        self.gekaufteTalente = []
        self.talentkosten = 0
        self.kampffertigkeit = 0;
        self.attribute = ['KO','KO','KO']
        self.attributswerte = [-1,-1,-1]
        self.basiswert = -1
        self.probenwert = -1
        self.probenwertTalent = -1
        self.voraussetzungen = []
    def aktualisieren(self, attribute):
        # Charakter �bergibt sein Dict
        super().aktualisieren()
        self.attributswerte = [attribute[self.attribute[0]], 
                               attribute[self.attribute[1]],
                               attribute[self.attribute[2]]]
        if self.wert == max(self.attributswerte)+2:
            self.lernkosten = -1
        self.basiswert = round(sum(self.attributswerte)/3)
        self.probenwert = self.basiswert + round(self.wert/2)
        self.probenwertTalent = self.basiswert + self.wert
        self.talentkosten = 20*self.steigerungsfaktor
    def steigern(self):
        if self.wert < max(self.attributswerte)+2:
            super().steigern()
            return 1
        return 0
    def talentKauf(self,talent):
        if talent in self.gekaufteTalente or self.name not in talent.fertigkeiten:
            return 0
        self.gekaufteTalente.append(Talent)
        return 1
    def talentVerlernen(self,talent):
        if talent not in self.gekaufteTalente:
            return 0
        self.gekaufteTalente.remove(talent)
        return 1

class Talent():
    def __init__(self):
        self.name = ''
        self.kosten = -1
        self.verbilligt = 0
        self.fertigkeiten = []
        self.voraussetzungen = []
        self.text = ''

class Vorteil():
    def __init__(self):
        self.name = ''
        self.kosten = -1
        self.voraussetzungen = []
        self.nachkauf = ''
        self.text = '' 