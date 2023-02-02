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
        scriptAPI = { 'getWert' : lambda: self.wert }
        self.probenwert = eval(Wolke.DB.einstellungen["Attribute: PW Script"].toText(), scriptAPI)    

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

# Implementation für freie Fertigkeiten in der Datenbank und für den Freie Fertigkeiten Picker
# Es werden komplett andere Attribute benötigt, daher separat
class FreieFertigkeitDB(object):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.kategorie = ""
        self.voraussetzungen = []
        self.isUserAdded = True

    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def __deepcopy__(self, memo=""):
        F = FreieFertigkeitDB()
        F.name = self.name
        F.kategorie = self.kategorie
        F.voraussetzungen = self.voraussetzungen.copy()
        F.isUserAdded = self.isUserAdded
        return F

# Implementation für Fertigkeiten im Allgemeinen
class KampffertigkeitTyp():
   Keine = 0
   Nahkampf = 1 #sf 4/2
   Sonstige = 2 #fernkampf, athletik

class Fertigkeit(Steigerbar):
    def __init__(self):
        super().__init__()
        self.gekaufteTalente = []
        self.talentMods = {} # for vorteil scripts, only used in export { talentnname1 : { condition1 : mod1, condition2 : mod2, ... }, talentname2 : {}, ... }
        self.kampffertigkeit = KampffertigkeitTyp.Keine
        self.attribute = ['KO','KO','KO']
        self.attributswerte = [-1,-1,-1]
        self.basiswert = -1
        self.basiswertMod = 0 # for vorteil scripts, only used in export
        self.probenwert = -1
        self.probenwertTalent = -1
        self.voraussetzungen = []
        self.maxWert = -1
        self.typ = -1
        self.talenteGruppieren = False
        self.isUserAdded = True
        self.addToPDF = False

    def aktualisieren(self, attribute):
        self.attributswerte = [attribute[self.attribute[0]].wert, 
                               attribute[self.attribute[1]].wert,
                               attribute[self.attribute[2]].wert]
        scriptAPI = { 'getAttribute' : lambda: self.attributswerte, 'getWert' : lambda: self.wert }
        self.maxWert = eval(Wolke.DB.einstellungen["Fertigkeiten: Maximalwert Script"].toText(), scriptAPI)
        self.basiswert = eval(Wolke.DB.einstellungen["Fertigkeiten: BW Script"].toText(), scriptAPI)
        scriptAPI['getBasiswert'] = lambda: self.basiswert
        self.probenwert = eval(Wolke.DB.einstellungen["Fertigkeiten: PW Script"].toText(), scriptAPI)
        self.probenwertTalent = eval(Wolke.DB.einstellungen["Fertigkeiten: PWT Script"].toText(), scriptAPI)

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
        F.talentMods = self.talentMods.copy()
        F.attributswerte = self.attributswerte.copy()
        F.basiswert = self.basiswert
        F.basiswertMod = self.basiswertMod
        F.probenwert = self.probenwert
        F.probenwertTalent = -self.probenwertTalent
        F.maxWert = self.maxWert
        F.typ = self.typ
        F.talenteGruppieren = self.talenteGruppieren
        F.isUserAdded = self.isUserAdded
        F.addToPDF = self.addToPDF
        return F

class Talent():
    def __init__(self):
        self.name = ''
        self.kosten = -1
        self.verbilligt = 0
        self.fertigkeiten = []
        self.voraussetzungen = []
        self.variableKosten = False
        self.kommentarErlauben = False
        self.text = ''
        self.cheatsheetAuflisten = True
        self.referenzBuch = 0
        self.referenzSeite = 0
        self.isUserAdded = True
    
    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__  
    
    def isSpezialTalent(self):
        return self.kosten != -1
    
    def getFullName(self, char):
        variable = ""
        ep = None
        kommentar = None

        if self.variableKosten and self.name in char.talenteVariableKosten:
            ep = str(char.talenteVariableKosten[self.name])

        if self.kommentarErlauben and self.name in char.talenteKommentare and char.talenteKommentare[self.name] != "":
            kommentar = char.talenteKommentare[self.name]

        if kommentar or ep:
            variable += "("
        if kommentar:
            variable += kommentar
        if kommentar and ep:
            variable += "; "
        if ep:
            variable += ep + " EP"
        if kommentar or ep:
            variable += ")"

        if variable:
            return self.name + " " + variable
        else:
            return self.name

class VorteilLinkKategorie():
   NichtVerknüpfen = 0
   ManöverMod = 1
   ÜberTalent = 2
   Vorteil = 3

class Vorteil():
    def __init__(self):
        self.name = ''
        self.kosten = -1
        self.variableKosten = False
        self.kommentarErlauben = False
        self.typ = 0
        self.voraussetzungen = []
        self.nachkauf = ''
        self.text = ''
        self.cheatsheetAuflisten = True
        self.cheatsheetBeschreibung = ''
        self.linkKategorie = VorteilLinkKategorie.NichtVerknüpfen
        self.linkElement = ''
        self.script = None
        self.scriptPrio = 0
        self.isUserAdded = True

    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        if self.__dict__ == other.__dict__: return True

    def getFullName(self, char, forceKommentar = False):
        if self.name == "Minderpakt" and char.minderpakt is not None:
            return self.name + " (" + Wolke.Char.minderpakt + ")"
        
        variable = ""
        ep = None
        kommentar = None
        if self.variableKosten and self.name in char.vorteileVariableKosten:
            ep = str(char.vorteileVariableKosten[self.name])

        if self.kommentarErlauben and self.name in char.vorteileKommentare and \
            char.vorteileKommentare[self.name] != "" and (forceKommentar or not ("$kommentar$" in self.cheatsheetBeschreibung)):
            kommentar = char.vorteileKommentare[self.name]

        if kommentar or ep:
            variable += "("
        if kommentar:
            variable += kommentar
        if kommentar and ep:
            variable += "; "
        if ep:
            variable += ep + " EP"
        if kommentar or ep:
            variable += ")"

        if variable:
            return self.name + " " + variable
        else:
            return self.name

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