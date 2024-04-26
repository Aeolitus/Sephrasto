from Core.Attribut import Attribut
from Core.AbgeleiteterWert import AbgeleiteterWert
from Core.Energie import Energie
from Core.Fertigkeit import Fertigkeit, KampffertigkeitTyp
from Core.FreieFertigkeit import FreieFertigkeit, FreieFertigkeitDefinition
from Core.Ruestung import Ruestung, RuestungDefinition
from Core.Talent import Talent
from Core.Vorteil import Vorteil
from Core.Waffe import Waffe, WaffeDefinition
import re
import copy
import logging
import collections
from EventBus import EventBus
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import os.path
import base64
from Migrationen import Migrationen
from VoraussetzungenListe import VoraussetzungenListe
from Serialization import Serialization

class KampfstilMod():
    def __init__(self):
        self.at = 0
        self.vt = 0
        self.plus = 0
        self.rw = 0
        self.be = 0

class Char():
    ''' 
    Main Workhorse Class. Contains all information about a charakter, performs
    calculations of EP-Costs and MR and such, checks requirements, reads and 
    writes xml. Probably should refactor this into multiple
    subclasses someday. 
    
    Someday.
    '''
    def __init__(self):
        '''Initialisiert alle Variablen und füllt die Listen'''
        #Erster Block: Allgemeine Infos
        self.enabledPlugins = []
        self.name = ''
        self.spezies = ''
        self.status = 2
        self.kurzbeschreibung = ''

        self.finanzen = 2;
        self.eigenheiten = []

        #Zweiter Block: Attribute und Abgeleitetes
        self.attribute = {}
        for el in Wolke.DB.attribute:
            self.attribute[el] = Attribut(Wolke.DB.attribute[el], self)

        self.abgeleiteteWerte = {}
        for el in Wolke.DB.abgeleiteteWerte:
            self.abgeleiteteWerte[el] = AbgeleiteterWert(Wolke.DB.abgeleiteteWerte[el], self)

        self.energien = {}
        
        #Dritter Block: Vorteile, gespeichert als String
        self.vorteile = {} #Important: use addVorteil and addRemove functions for modification
        self.kampfstilMods = {}
        self.vorteilFavoriten = []

        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.fertigkeiten = {}
        self.freieFertigkeiten = []
        self.freieFertigkeitenNumKostenlos = Wolke.DB.einstellungen["FreieFertigkeiten: Anzahl Kostenlos"].wert
        self.talente = {}
        self.talentMods = {}  # for scripts, only used in export { talentnname1 : mod, talentname2 : mod, ... 
        self.talentInfos = {} # for scripts, only used in export { talentnname1 : ["Info1", "Info2"], talentname2 : ["Info3"], ... 
        self.regelInfos = {}

        #Fünfter Block: Ausrüstung etc
        self.rüstung = []
        self.waffen = []
        self.ausrüstung = []
        self.zonenSystemNutzen = False

        #Sechster Block: Übernatürliches
        self.übernatürlicheFertigkeiten = {}

        #Siebter Block: EP
        self._epGesamt = 0
        self.epAusgegeben = 0
        
        self.epAttribute = 0
        self.epVorteile = 0
        self.epFertigkeiten = 0
        self.epFertigkeitenTalente = 0
        self.epFreieFertigkeiten = 0
        self.epÜbernatürlich = 0
        self.epÜbernatürlichTalente = 0

        #Achter Block: Infos
        self.voraussetzungenPruefen = True
        self.notiz = ""
        self.charakterbogen = Wolke.Settings["Bogen"]
        self.finanzenAnzeigen = True
        self.ueberPDFAnzeigen = False
        self.detailsAnzeigen = False
        self.regelnAnhaengen = Wolke.Settings["Cheatsheet"]
        self.regelnGroesse = Wolke.Settings["Cheatsheet-Fontsize"]
        self.deaktivierteRegelKategorien = []
        self.formularEditierbar = Wolke.Settings["Formular-Editierbarkeit"]
        self.neueHausregeln = None # only set if changed via info tab and used when saving

        #Neunter Block: Beschreibung Details
        self.kultur = ""
        self.profession = ""
        self.geschlecht = ""
        self.geburtsdatum = ""
        self.groesse = ""
        self.gewicht = ""
        self.haarfarbe = ""
        self.augenfarbe = ""
        self.titel = ""
        self.aussehen = [""]*6
        self.hintergrund = [""]*9
        self.bild = None
        self._heimat = ""

        #Script API
        #Bei Änderungen nicht vergessen die script docs in ScriptAPI.md anzupassen
        self.currentVorteil = None #used by vorteilScriptAPI during iteration
        self.currentEigenschaft = None #used by waffenScriptAPI during iteration
        self.currentWaffeIndex = None
        self.waffenEigenschaftenUndo = [] #For undoing changes made by Vorteil scripts

        self.charakterScriptAPI = Hilfsmethoden.createScriptAPI()
        self.charakterScriptAPI.update({
            #Hintergrund
            'getName' : lambda: self.name, 
            'getSpezies' : lambda: self.spezies, 
            'getStatus' : lambda: Wolke.DB.einstellungen["Statusse"].wert[self.status], 
            'getStatusIndex' : lambda: self.status, 
            'getKurzbeschreibung' : lambda: self.kurzbeschreibung, 
            'getHeimat' : lambda: self.heimat, 
            'getFinanzen' : lambda: Wolke.DB.einstellungen["Statusse"].wert[self.finanzen], 
            'getFinanzenIndex' : lambda: self.finanzen, 
            'getEigenheit' : lambda index: self.eigenheiten[index], 
            'getEPGesamt' : lambda: self.epGesamt,
            'getEPAusgegeben' : lambda: self.epAusgegeben, 

            #Fertigkeiten
            'hasFertigkeit' : lambda name: name in self.fertigkeiten,
            'getFertigkeitBasiswert' : lambda name: self.fertigkeiten[name].basiswert if name in self.fertigkeiten else None, 
            'getFertigkeitProbenwert' : lambda name: self.fertigkeiten[name].probenwert if name in self.fertigkeiten else None, 
            'getFertigkeitProbenwertTalent' : lambda name: self.fertigkeiten[name].probenwertTalent if name in self.fertigkeiten else None, 
            'modifyFertigkeitBasiswert' : lambda name, mod: setattr(self.fertigkeiten[name], 'basiswertMod', self.fertigkeiten[name].basiswertMod + mod) if name in self.fertigkeiten else None, 

            'hasÜbernatürlicheFertigkeit' : lambda name: name in self.übernatürlicheFertigkeiten,
            'getÜbernatürlicheFertigkeitBasiswert' :lambda name: self.übernatürlicheFertigkeiten[name].basiswert if name in self.übernatürlicheFertigkeiten else None, 
            'getÜbernatürlicheFertigkeitProbenwert' : lambda name: self.übernatürlicheFertigkeiten[name].probenwert if name in self.übernatürlicheFertigkeiten else None, 
            'getÜbernatürlicheFertigkeitProbenwertTalent' : lambda name: self.übernatürlicheFertigkeiten[name].probenwertTalent if name in self.übernatürlicheFertigkeiten else None, 
            'modifyÜbernatürlicheFertigkeitBasiswert' : lambda name, mod: setattr(self.übernatürlicheFertigkeiten[name], 'basiswertMod', self.übernatürlicheFertigkeiten[name].basiswertMod + mod) if name in self.übernatürlicheFertigkeiten else None, 

            'getFreieFertigkeit' : lambda index: self.freieFertigkeiten[i].name if index >= 0 and index < len(self.freieFertigkeiten) else None,
            'getFreieFertigkeitWert' : lambda index: self.freieFertigkeiten[i].wert if index >= 0 and index < len(self.freieFertigkeiten) else None,
            'freieFertigkeitenCount' : lambda: len(self.freieFertigkeiten),
            
            #Talente
            'hasTalent' : lambda name: name in self.talente,
            'addTalent' : self.API_addTalent,
            "removeTalent" : lambda talent: self.removeTalent(talent),
            'modifyTalentProbenwert' : self.API_modifyTalentProbenwert, 
            'addTalentInfo' : self.API_addTalentInfo, 

            #Vorteile
            'hasVorteil' : lambda name: name in self.vorteile,
            'addVorteil' : self.API_addVorteil,
            'removeVorteil' : lambda vorteil: self.removeVorteil(vorteil),

            #Kampfstile
            'getKampfstilAT' : lambda kampfstil: self.kampfstilMods[kampfstil].at if kampfstil in self.kampfstilMods else 0, 
            'getKampfstilVT' : lambda kampfstil: self.kampfstilMods[kampfstil].vt if kampfstil in self.kampfstilMods else 0, 
            'getKampfstilTPPlus' : lambda kampfstil: self.kampfstilMods[kampfstil].plus if kampfstil in self.kampfstilMods else 0, 
            'getKampfstilRW' : lambda kampfstil: self.kampfstilMods[kampfstil].rw if kampfstil in self.kampfstilMods else 0, 
            'getKampfstilBE' : lambda kampfstil: self.kampfstilMods[kampfstil].be if kampfstil in self.kampfstilMods else 0, 
            'setKampfstil' : self.API_setKampfstil, 
            'modifyKampfstil' : self.API_modifyKampfstil, 

            #Ausrüstung
            'inventarCount' : lambda: len(self.ausrüstung),
            'getInventar' : lambda index: self.ausrüstung[index] if index >= 0 and index < len(self.ausrüstung) else None, 

            'rüstungenCount' : lambda: len(self.rüstung),
            'getRüstung' : lambda index: self.rüstung[index].name if index >= 0 and index < len(self.rüstung) else None, 
            'getRüstungRS' : lambda index: self.rüstung[index].getRSGesamtInt() if index >= 0 and index < len(self.rüstung) else None, 
            'getRüstungBE' : lambda index: self.rüstung[index].be if index >= 0 and index < len(self.rüstung) else None, 

            'waffenCount' : lambda:len(self.waffen),
            'getWaffe' : lambda index: self.API_getWaffeValue(index, "name"), 
            'isWaffeNahkampf' : lambda index: self.API_getWaffeValue(index, "nahkampf"), 
            'isWaffeFernkampf' : lambda index: self.API_getWaffeValue(index, "fernkampf"), 
            'getWaffeEigenschaften' : lambda index: self.waffen[index].eigenschaften.copy() if index >= 0 and index < len(self.waffen) else None, 
            'getWaffeKampfstil' : lambda index: self.API_getWaffeValue(index, "kampfstil"), 
            'getWaffeFertigkeit' : lambda index: self.API_getWaffeValue(index, "fertigkeit"), 
            'getWaffeTalent' : lambda index: self.API_getWaffeValue(index, "talent"), 
            'getWaffeWM' : lambda index: self.API_getWaffeValue(index, "wm"), 
            'getWaffeTPWürfelSeiten' : lambda index: self.API_getWaffeValue(index, "würfelSeiten"), 

            'getWaffeATMod' : lambda index: self.API_getWaffeValue(index, "at"), 
            'setWaffeAT' : lambda index, at: self.API_setWaffeValue(index, "at", at),
            'modifyWaffeAT' : lambda index, atMod: self.API_modifyWaffeValue(index, "at", atMod),

            'getWaffeVTMod' : lambda index: self.API_getWaffeValue(index, "vt"), 
            'setWaffeVT' : lambda index, vt: self.API_setWaffeValue(index, "vt", vt), 
            'modifyWaffeVT' : lambda index, vtMod: self.API_modifyWaffeValue(index, "vt", vtMod),  

            'getWaffeLZ' : lambda index: self.API_getWaffeValue(index, "lz"), 
            'getWaffeLZMod' : lambda index: self.API_getWaffeValue(index, "lzMod"), 
            'setWaffeLZ' : lambda index, lz: self.API_setWaffeValue(index, "lzMod", lz), 
            'modifyWaffeLZ' : lambda index, lzMod: self.API_modifyWaffeValue(index, "lzMod", lzMod),  

            'getWaffeTPWürfel' : lambda index: self.API_getWaffeValue(index, "würfel"), 
            'getWaffeTPWürfelMod' : lambda index: self.API_getWaffeValue(index, "würfelMod"), 
            'setWaffeTPWürfel' : lambda index, würfel: self.API_setWaffeValue(index, "würfelMod", würfel), 
            'modifyWaffeTPWürfel' : lambda index, würfelMod: self.API_modifyWaffeValue(index, "würfelMod", würfelMod),

            'getWaffeTPPlus' : lambda index: self.API_getWaffeValue(index, "plus"), 
            'getWaffeTPPlusMod' : lambda index: self.API_getWaffeValue(index, "plusMod"), 
            'setWaffeTPPlus' : lambda index, plus: self.API_setWaffeValue(index, "plusMod", plus),
            'modifyWaffeTPPlus' : lambda index, plusMod: self.API_modifyWaffeValue(index, "plusMod", plusMod), 

            'getWaffeHärte' : lambda index: self.API_getWaffeValue(index, "härte"), 
            'getWaffeHärteMod' : lambda index: sself.API_getWaffeValue(index, "härteMod"), 
            'setWaffeHärte' : lambda index, härte: self.API_setWaffeValue(index, "härteMod", härte),
            'modifyWaffeHärte' : lambda index, härteMod: self.API_modifyWaffeValue(index, "härteMod", härteMod), 

            'getWaffeRW' : lambda index: self.API_getWaffeValue(index, "rw"), 
            'getWaffeRWMod' : lambda index: self.API_getWaffeValue(index, "rwMod"), 
            'setWaffeRW' : lambda index, rw: self.API_setWaffeValue(index, "rwMod", rw),
            'modifyWaffeRW' : lambda index, rwMod: self.API_modifyWaffeValue(index, "rwMod", rwMod),

            'addWaffeneigenschaft' : self.API_addWaffeneigenschaft, 
            'removeWaffeneigenschaft' : self.API_removeWaffeneigenschaft,

            #Regeln
            'addRegelInfo' : self.API_addRegelInfo,

            #Attribute
            'getAttribut' : lambda attribut: self.attribute[attribut].wert,
            'getAttributProbenwert' : lambda attribut: self.attribute[attribut].probenwert,
        })

        #Add Attribute to API (readonly)
        for attribut in self.attribute:
            self.charakterScriptAPI["get" + attribut] = lambda attribut=attribut: self.attribute[attribut].wert
            self.charakterScriptAPI["get" + attribut + "Probenwert"] = lambda attribut=attribut: self.attribute[attribut].probenwert
        
        #Add abgeleitete Werte to API
        for ab in self.abgeleiteteWerte:
            self.charakterScriptAPI['get' + ab + 'Basis'] = lambda ab=ab: self.abgeleiteteWerte[ab].basiswert
            self.charakterScriptAPI['get' + ab + 'Mod'] = lambda ab=ab: self.abgeleiteteWerte[ab].mod
            self.charakterScriptAPI['set' + ab + 'Mod'] = lambda wert, ab=ab: setattr(self.abgeleiteteWerte[ab], 'mod', wert)
            self.charakterScriptAPI['modify' + ab] = lambda wert, ab=ab: setattr(self.abgeleiteteWerte[ab], 'mod', self.abgeleiteteWerte[ab].mod + wert)
            self.charakterScriptAPI['get' + ab] = lambda ab=ab: self.abgeleiteteWerte[ab].wert
            

        #Add Energien to API
        for en in Wolke.DB.energien:
            self.charakterScriptAPI['get' + en + 'Basis'] = lambda en=en: self.energien[en].basiswert if en in self.energien else 0
            self.charakterScriptAPI['set' + en + 'Basis'] = lambda basis, en=en: setattr(self.energien[en], "basiswert", basis) if en in self.energien else None
            self.charakterScriptAPI['modify' + en + 'Basis'] = lambda basis, en=en: setattr(self.energien[en], "basiswert", self.energien[en].basiswert + basis) if en in self.energien else None
            self.charakterScriptAPI['get' + en + 'Mod'] = lambda en=en: self.energien[en].mod if en in self.energien else 0
            self.charakterScriptAPI['set' + en + 'Mod'] = lambda mod, en=en: setattr(self.energien[en], "mod", mod) if en in self.energien else None
            self.charakterScriptAPI['modify' + en] = lambda mod, en=en: setattr(self.energien[en], "mod", self.energien[en].mod + mod) if en in self.energien else None
            self.charakterScriptAPI['get' + en] = lambda en=en: self.energien[en].wert if en in self.energien else 0
            self.charakterScriptAPI['get' + en + 'Final'] = lambda en=en: self.energien[en].wertFinal if en in self.energien else 0

        self.waffenScriptAPI = {
            'getEigenschaftParam' : lambda paramNb: self.API_getWaffeneigenschaftParam(paramNb),
            'getWaffeIndex' : lambda: self.currentWaffeIndex,
        }

        for k, v in self.charakterScriptAPI.items():
            if k in self.waffenScriptAPI:
                assert False, "Duplicate entry"
            self.waffenScriptAPI[k] = v

        #Init values that require script API
        heimaten = sorted(Wolke.DB.einstellungen["Heimaten"].wert)
        if "Mittelreich" in heimaten:
            self.heimat = "Mittelreich"
        else:
            self.heimat = heimaten[0] if len(heimaten) > 0 else ""

        EventBus.doAction("charakter_instanziiert", { "charakter" : self })

    def __deepcopy__(self, memo=""):
        # regular deep copy is way too error prone, ".charakter"-references would have to be fixed
        # for all core classes (because they override the id in the memo) and plugin support would be annoying
        # so we just serialize-deserialize in memory
        result = self.__class__()
        serializer = Serialization.getSerializer(".xml", 'Charakter') #todo: switch to .json once we have a deserializer for it
        self.serialize(serializer)
        deserializer = Serialization.getDeserializer(".xml", 'Charakter')
        deserializer.initFromSerializer(serializer)
        result.deserialize(deserializer)
        return result

    @property
    def epGesamt(self):
        return self._epGesamt

    @epGesamt.setter
    def epGesamt(self, value):
        oldVal = self._epGesamt
        self._epGesamt = value
        EventBus.doAction("charakter_epgesamt_geändert", { "charakter" : self, "epAlt" : oldVal, "epNeu" : value })

    @property
    def heimat(self):
        return self._heimat

    @heimat.setter
    def heimat(self, heimat):
        if heimat == self._heimat:
            return

        self.charakterScriptAPI["heimatAlt"] = self._heimat
        self.charakterScriptAPI["heimatNeu"] = heimat
        script = Wolke.DB.einstellungen["Heimaten: Heimat geändert Script"].wert
        exec(script, self.charakterScriptAPI)
        del self.charakterScriptAPI["heimatAlt"]
        del self.charakterScriptAPI["heimatNeu"]

        self._heimat = heimat

    def API_getWaffeValue(self, index, attrib):
        if index < 0 or index >= len(self.waffen):
            return None
        return getattr(self.waffen[index], attrib)
    
    def API_setWaffeValue(self, index, attrib, value):
        if index < 0 or index >= len(self.waffen):
            return
        setattr(self.waffen[index], attrib, value)

    def API_modifyWaffeValue(self, index, attrib, value):
        if index < 0 or index >= len(self.waffen):
            return
        prevValue = getattr(self.waffen[index], attrib)
        setattr(self.waffen[index], attrib, prevValue + value)

    def API_modifyTalentProbenwert(self, talent, mod):
        if talent not in Wolke.DB.talente:
            return
        if talent not in self.talentMods:
            self.talentMods[talent] = 0      
        self.talentMods[talent] += mod
        if self.talentMods[talent] == 0:
            del self.talentMods[talent]

    def API_addTalentInfo(self, talent, info):
        if talent not in Wolke.DB.talente:
            return
        if talent not in self.talentInfos:
            self.talentInfos[talent] = []
        self.talentInfos[talent].append(info)

    def API_addTalent(self, talent, kosten = -1, requiredÜberFert = None, kommentar=""):
        fertVoraussetzungen = ""
        if requiredÜberFert:
            if requiredÜberFert in self.übernatürlicheFertigkeiten:
                fertVoraussetzungen = "Übernatürliche-Fertigkeit '" + requiredÜberFert + "'"
            else:
                return
        talent = self.addTalent(talent)
        if self.currentVorteil:
            talent.voraussetzungen = talent.voraussetzungen.add("Vorteil " + self.currentVorteil, Wolke.DB)
        talent.voraussetzungen = talent.voraussetzungen.add(fertVoraussetzungen, Wolke.DB)

        if kosten != -1:
            talent.kosten = kosten
        if talent.kommentarErlauben and kommentar:
            talent.kommentar = kommentar

    def API_addVorteil(self, vorteil, kosten = -1, kommentar=""):
        vorteil = self.addVorteil(vorteil)
        if self.currentVorteil:
            vorteil.voraussetzungen = vorteil.voraussetzungen.add("Vorteil " + self.currentVorteil, Wolke.DB)
        if kosten != -1:
            vorteil.kosten = kosten
        if vorteil.kommentarErlauben and kommentar:
            vorteil.kommentar = kommentar

    def API_setKampfstil(self, kampfstil, at, vt, plus, rw, be = 0):
        k = self.kampfstilMods[kampfstil]
        k.at = at
        k.vt = vt
        k.plus = plus
        k.rw = rw
        k.be = (be or 0)
    
    def API_modifyKampfstil(self, kampfstil, at, vt, plus, rw, be = 0):
        k = self.kampfstilMods[kampfstil]
        self.API_setKampfstil(kampfstil, k.at + at, k.vt + vt, k.plus + plus, k.rw + rw, k.be + be)

    def API_addWaffeneigenschaft(self, waffenName, eigenschaft):
        for waffe in self.waffen:
            if waffe.name != waffenName:
                continue
            if eigenschaft in waffe.eigenschaften:
                continue
            self.waffenEigenschaftenUndo.append([waffe, eigenschaft, False])
            waffe.eigenschaften.append(eigenschaft)

    def API_removeWaffeneigenschaft(self, waffenName, eigenschaft):
        for waffe in self.waffen:
            if waffe.name != waffenName:
                continue
            if eigenschaft not in waffe.eigenschaften:
                continue
            self.waffenEigenschaftenUndo.append([waffe, eigenschaft, True])
            waffe.eigenschaften.remove(eigenschaft)

    def API_getWaffeneigenschaftParam(self, paramNb):
        match = re.search(r"\((.+?)\)", self.currentEigenschaft, re.UNICODE)
        if not match:
            raise Exception(f"Die Waffeneigenschaft '{self.currentEigenschaft}' erfordert einen Parameter, beispielsweise Schwer (4), aber es wurde keiner gefunden.")
        parameters = list(map(str.strip, match.group(1).split(";")))
        if paramNb >= len(parameters):
            raise Exception(f"Die Waffeneigenschaft '{self.currentEigenschaft}' erfordert {paramNb+1} Parameter, aber es wurde(n) nur {len(parameters)} gefunden. Parameter müssen mit Semikolon getrennt werden")
        return parameters[paramNb]

    def API_addRegelInfo(self, regel, info):
        if regel not in self.regelInfos:
            self.regelInfos[regel] = []
        self.regelInfos[regel].append(info)

    def addTalent(self, name):
        if name in self.talente:
            return self.talente[name]
        if not name in Wolke.DB.talente:
            return None

        talent = Talent(Wolke.DB.talente[name], self)
        self.talente[name] = talent

        fertigkeiten = self.fertigkeiten
        if talent.spezialTalent:
            fertigkeiten = self.übernatürlicheFertigkeiten
        for fertName in talent.fertigkeiten:
            if not fertName in fertigkeiten:
                continue
            fert = fertigkeiten[fertName]
            if name in fert.gekaufteTalente:
                continue
            fert.gekaufteTalente.append(name)
        return talent

    def removeTalent(self, name):
        if not name in self.talente:
            return

        fertigkeiten = self.fertigkeiten
        if self.talente[name].spezialTalent:
            fertigkeiten = self.übernatürlicheFertigkeiten
        for fertName in self.talente[name].fertigkeiten:
            if not fertName in fertigkeiten:
                continue
            fert = fertigkeiten[fertName]
            if not name in fert.gekaufteTalente:
                continue
            fert.gekaufteTalente.remove(name)

        self.talente.pop(name)

    def addVorteil(self, name):
        if name in self.vorteile:
           return self.vorteile[name]
        if not name in Wolke.DB.vorteile:
           return None
        vorteil = Vorteil(Wolke.DB.vorteile[name], self)
        self.vorteile[name] = vorteil
        EventBus.doAction("vorteil_gekauft", { "charakter" : self, "name" : name })
        return vorteil

    def removeVorteil(self, name):
        if not name in self.vorteile:
            return
        self.vorteile.pop(name)
        EventBus.doAction("vorteil_entfernt", { "charakter" : self, "name" : name })

    def aktualisieren(self):
        EventBus.doAction("pre_charakter_aktualisieren", { "charakter" : self })

        # Undo previous changes by Vorteil scripts before executing them again
        self.kampfstilMods = {}
        for ks in Wolke.DB.findKampfstile():
            self.kampfstilMods[ks] = KampfstilMod()

        for value in self.waffenEigenschaftenUndo:
            waffe = value[0]
            wEigenschaft = value[1]
            remove = value[2]
            if (not remove) and (wEigenschaft in waffe.eigenschaften):
                waffe.eigenschaften.remove(wEigenschaft)
            elif remove and (not (wEigenschaft in waffe.eigenschaften)):
                waffe.eigenschaften.append(wEigenschaft)
        self.waffenEigenschaftenUndo = []

        for fert in self.fertigkeiten.values():
            fert.resetScriptValues()

        for fert in self.übernatürlicheFertigkeiten.values():
            fert.resetScriptValues()

        for waffe in self.waffen:
            waffe.resetScriptValues()

        self.talentMods = {}
        self.talentInfos = {}
        self.regelInfos = {}

        # Update attribute, abegeleitet werte, energien
        for attribut in self.attribute.values():
            attribut.aktualisieren()

        for ab in self.abgeleiteteWerte.values():
            ab.aktualisieren()

        for en in self.energien.values():
            en.aktualisieren()

        EventBus.doAction("charakter_aktualisieren_fertigkeiten", { "charakter" : self })

        # Update fertigkeiten
        for fert in self.fertigkeiten.values():
            fert.aktualisieren()

        for fert in self.übernatürlicheFertigkeiten.values():
            fert.aktualisieren()

        # Requirements check - add automatically unlocked stuff and remove stuff not available anymore
        self.checkVoraussetzungen()

        # Execute Vorteil scripts to modify character stats
        EventBus.doAction("charakter_aktualisieren_vorteilscripts", { "charakter" : self })
        vorteileByPrio = collections.defaultdict(list)
        for vorteil in self.vorteile.values():
            if not (vorteil.script or vorteil.editorScript):
                continue
            vorteileByPrio[vorteil.scriptPrio].append(vorteil)

        for key in sorted(vorteileByPrio):
            for vort in vorteileByPrio[key]:
                self.currentVorteil = vort.name
                if vort.script:
                    logging.info(f"Character: applying script for Vorteil {vort.name} ({vort.script})")
                    vort.executeScript()
                if vort.editorScript:
                    logging.info(f"Character: applying editor script for Vorteil {vort.name} ({vort.editorScript})")
                    vort.executeEditorScript()
        self.currentVorteil = None

        # Update talente - this only updates values relevant for display purposes (cached probenwert, hauptfertigkeit),
        # so its safe to do this late and allows for modifications via vorteil scripts
        for tal in self.talente.values():
            tal.aktualisieren()

        # Update abgeleitete werte "*" values - they might have been modified by Vorteil scripts
        for ab in self.abgeleiteteWerte.values():
            ab.aktualisierenFinal() #WS*, GS*, DH*, SchiP*

        # Update weapon stats last because they might depend on everything else but do not change other things
        EventBus.doAction("charakter_aktualisieren_waffenwerte", { "charakter" : self })
        self.updateWaffenwerte()

        EventBus.doAction("post_charakter_aktualisieren", { "charakter" : self })
        self.epZaehlen()


    def updateWaffenwerte(self):
        for i in range(len(self.waffen)):
            waffe = self.waffen[i]
            if "WS" in self.abgeleiteteWerte and waffe.name in Wolke.DB.einstellungen["Waffen: Härte WSStern"].wert:
                waffe.härte = self.abgeleiteteWerte["WS"].finalwert

            if not waffe.fertigkeit in self.fertigkeiten:
                continue

            if waffe.talent in self.fertigkeiten[waffe.fertigkeit].gekaufteTalente:
                pw = self.fertigkeiten[waffe.fertigkeit].probenwertTalent
            else:
                pw = self.fertigkeiten[waffe.fertigkeit].probenwert
                
            kampfstilMods = self.kampfstilMods.get(waffe.kampfstil, KampfstilMod())

            # Execute script to calculate weapon stats
            scriptAPI = Hilfsmethoden.createScriptAPI()
            scriptAPI.update({
                'getAttribut' : lambda attribut: self.attribute[attribut].wert,
                'getWaffe' : lambda: copy.deepcopy(waffe),
                'getPW' : lambda: pw,
                'getKampfstil' : lambda: copy.copy(kampfstilMods),
                'getRüstungBE' : lambda: 0 if waffe.beSlot < 1 or len(self.rüstung) < waffe.beSlot else self.rüstung[waffe.beSlot-1].getBEFinal(self.abgeleiteteWerte),
                'modifyWaffenwerte' : lambda at, vt, plus, rw: setattr(waffe, 'at', waffe.at + at) or setattr(waffe, 'vt', waffe.vt + vt) or setattr(waffe, 'plusMod', waffe.plusMod + plus) or setattr(waffe, 'rwMod', waffe.rwMod + rw)
            })
            for ab in self.abgeleiteteWerte:
                scriptAPI['get' + ab + 'Basis'] = lambda ab=ab: self.abgeleiteteWerte[ab].basiswert
                scriptAPI['get' + ab] = lambda ab=ab: self.abgeleiteteWerte[ab].wert
                scriptAPI['get' + ab + 'Mod'] = lambda ab=ab: self.abgeleiteteWerte[ab].mod

            # Execute global script
            logging.info("Character: executing Waffenwerte script for " + waffe.anzeigename)
            exec(Wolke.DB.einstellungen["Waffen: Waffenwerte Script"].wert, scriptAPI)

            #Execute Waffeneigenschaft scripts
            self.currentWaffeIndex = i
            eigenschaftenByPrio = collections.defaultdict(list)
            for weName in waffe.eigenschaften:
                try:
                    we = Hilfsmethoden.GetWaffeneigenschaft(weName, Wolke.DB)
                except WaffeneigenschaftException:
                    continue #Manually added Eigenschaften are allowed
                if not we.script:
                    continue
                eigenschaftenByPrio[we.scriptPrio].append(weName)

            for key in sorted(eigenschaftenByPrio):
                for weName in eigenschaftenByPrio[key]:
                    self.currentEigenschaft = weName
                    logging.info("Character: applying script for Waffeneigenschaft " + weName)
                    we = Hilfsmethoden.GetWaffeneigenschaft(weName, Wolke.DB)
                    we.executeScript(self.waffenScriptAPI)

            self.currentWaffeIndex = None
            self.currentEigenschaft = None

    def epZaehlen(self):
        '''Berechnet die bisher ausgegebenen EP'''
        spent = 0
        #Erster Block ist gratis
        #Zweiter Block: Attribute und Abgeleitetes
        for attribut in self.attribute.values():
            spent += attribut.kosten()
            
        for energie in self.energien.values():
            spent += energie.kosten()

        self.epAttribute = spent
        #Dritter Block: Vorteile
        for vorteil in self.vorteile.values():
            spent += vorteil.kosten
        
        self.epVorteile = spent - self.epAttribute
        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.epFertigkeiten = 0
        self.epFertigkeitenTalente = 0
        self.epFreieFertigkeiten = 0
        for fer in self.fertigkeiten.values():     
            val = fer.kosten()
            spent += val
            self.epFertigkeiten += val

        numKostenlos = 0
        for fer in self.freieFertigkeiten:
            # Dont count Muttersprache
            if fer.wert == 3 and numKostenlos < self.freieFertigkeitenNumKostenlos:
                numKostenlos += 1
                continue
            if not fer.name:
                continue
            val = fer.kosten()
            spent += val
            self.epFreieFertigkeiten += val

        #Fünfter Block ist gratis
        #Sechster Block: Übernatürliches
        self.epÜbernatürlich = 0
        self.epÜbernatürlichTalente = 0
        for fer in self.übernatürlicheFertigkeiten.values():
            val = fer.kosten()
            spent += val
            self.epÜbernatürlich += val

        #Siebter Block ist gratis
        #Talente
        for tal in self.talente:
            kosten = self.talente[tal].kosten
            spent += kosten
            if self.talente[tal].spezialTalent:
                self.epÜbernatürlichTalente += kosten
            else:
                self.epFertigkeitenTalente += kosten

        #Store
        self.epAusgegeben = spent

    def checkVoraussetzungen(self):
        ''' 
        Checks for all elements with requirements if they are still met until in one 
        run, all of them meet the requirements. This gets rid of stacks of them
        that all depend onto each other, like Zauberer I-IV when removing I
        '''
        done = False
        while not done:
            done = True

            # Energien
            remove = []
            for en in self.energien.values():
                if not self.voraussetzungenPrüfen(en):
                    remove.append(en.name)
            for el in remove:
                self.energien.pop(el)
            for name, energie in Wolke.DB.energien.items():
                if name in self.energien:
                    continue
                if self.voraussetzungenPrüfen(energie):
                    self.energien[name] = Energie(energie, self)

            # Vorteile
            remove = []
            for vorteil in self.vorteile.values():
                if not self.voraussetzungenPrüfen(vorteil):
                    remove.append(vorteil.name)
                    done = False
            for el in remove:
                self.removeVorteil(el)

            # Fertigkeiten
            remove = []
            for fertigkeit in self.fertigkeiten.values():
                if not self.voraussetzungenPrüfen(fertigkeit):
                    remove.append(fertigkeit.name)
                    done = False
            for el in remove:
                self.fertigkeiten.pop(el)

            for name, fertigkeitDefinition in Wolke.DB.fertigkeiten.items():
                if name in self.fertigkeiten:
                    continue
                if self.voraussetzungenPrüfen(fertigkeitDefinition):
                    self.fertigkeiten[name] = Fertigkeit(fertigkeitDefinition, self)
                    self.fertigkeiten[name].aktualisieren()
                    done = False

            # Übernatürliche Fertigkeiten
            remove = []
            for fertigkeit in self.übernatürlicheFertigkeiten.values():
                if not self.voraussetzungenPrüfen(fertigkeit):
                    remove.append(fertigkeit.name)
                    done = False
            for el in remove:
                self.übernatürlicheFertigkeiten.pop(el)

            for name, fertigkeitDefinition in Wolke.DB.übernatürlicheFertigkeiten.items():
                if name in self.übernatürlicheFertigkeiten:
                    continue
                if self.voraussetzungenPrüfen(fertigkeitDefinition):
                    self.übernatürlicheFertigkeiten[name] = Fertigkeit(fertigkeitDefinition, self)
                    self.übernatürlicheFertigkeiten[name].aktualisieren()
                    done = False

            # Talente
            remove = []
            for talent in self.talente.values():
                fertigkeiten = self.fertigkeiten
                if talent.spezialTalent:
                    fertigkeiten = self.übernatürlicheFertigkeiten

                doRemove = not self.voraussetzungenPrüfen(talent)
                if not doRemove:
                    doRemove = sum(1 for f in talent.fertigkeiten if f in fertigkeiten) == 0

                if doRemove:
                    remove.append(talent.name)
                    done = False

                for fertName in talent.fertigkeiten:
                    if not fertName in fertigkeiten:
                        continue
                    fert = fertigkeiten[fertName]
                    if doRemove:
                        if talent.name in fert.gekaufteTalente:
                            fert.gekaufteTalente.remove(talent.name) 
                    elif talent.name not in fert.gekaufteTalente:
                        fert.gekaufteTalente.append(talent.name)

            for el in remove:
                self.talente.pop(el)

    def findUnerfüllteVorteilVoraussetzungen(self, vorteile = None, waffen = None, attribute = None, übernatürlicheFertigkeiten = None, fertigkeiten = None, talente = None):
        ''' 
        Checks for all Vorteile if the requirements are still met until in one 
        run, all of them meet the requirements. This gets rid of stacks of them
        that all depend onto each other, like Zauberer I-IV when removing I.
        The parameters can be used to override character values. If None is specified, the character values are used.
        '''
        if not self.voraussetzungenPruefen:
            return []

        vorteile = copy.copy(vorteile or self.vorteile)
        waffen = waffen or self.waffen
        attribute = attribute or self.attribute
        übernatürlicheFertigkeiten = übernatürlicheFertigkeiten or self.übernatürlicheFertigkeiten
        fertigkeiten = fertigkeiten or self.fertigkeiten
        talente = talente or self.talente
        allRemoved = []
        while True:
            contFlag = True
            remove = []
            for vor in vorteile.values():
                if not Hilfsmethoden.voraussetzungenPrüfen(vor, vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, talente):
                    remove.append(vor.name)
                    allRemoved.append(vor.name)
                    contFlag = False
            for el in remove:
                vorteile.pop(el)
            if contFlag:
                break

        return allRemoved

    def voraussetzungenPrüfen(self, dbElement):
        if not self.voraussetzungenPruefen:
            return True

        return Hilfsmethoden.voraussetzungenPrüfen(dbElement, self.vorteile, self.waffen, self.attribute, self.übernatürlicheFertigkeiten, self.fertigkeiten, self.talente)
    
    def saveFile(self, filename):
        _, fileExtension = os.path.splitext(filename)
        serializer = Serialization.getSerializer(fileExtension, 'Charakter')
        self.serialize(serializer)
        serializer.writeFile(filename)
        EventBus.doAction("charakter_geschrieben", { "charakter" : self, "serializer" : serializer, "filepath" : filename })

    def serialize(self, serializer):   
        ser = EventBus.applyFilter("charakter_serialisieren", serializer, { "charakter" : self })

        ser.begin('Version')
        ser.setNested('CharakterVersion', Migrationen.charakterCodeVersion)
        ser.setNested('Plugins', ", ".join(self.enabledPlugins))
        if self.neueHausregeln is not None:
            ser.setNested('Hausregeln', self.neueHausregeln)
        else:
            ser.setNested('Hausregeln', Wolke.DB.hausregelnAnzeigeName)
        ser.end() #version

        #Erster Block
        ser.begin('Beschreibung')
        ser.setNested('Name', self.name)
        ser.setNested('Spezies', self.spezies)
        ser.setNested('Status', self.status)
        ser.setNested('Kurzbeschreibung', self.kurzbeschreibung)
        ser.setNested('Finanzen', self.finanzen)
        ser.setNested('Heimat', self.heimat)
        ser.beginList('Eigenheiten')
        for eigenh in self.eigenheiten:
            ser.setNested('Eigenheit', eigenh)
        ser.end() #eigenheiten
        ser.end() #beschreibung

        ser.beginList('Attribute')
        for attribut in self.attribute.values():
            ser.begin('Attribut')
            attribut.serialize(ser)
            ser.end() #attribut
        ser.end() #attribute

        ser.beginList('Energien')
        for energie in self.energien.values():
            ser.begin('Energie')
            energie.serialize(ser)
            ser.end() #energie
        ser.end() #energien
        
        ser.beginList('Vorteile')
        for vorteil in self.vorteile.values():
            ser.begin('Vorteil')
            vorteil.serialize(ser)
            ser.end() #vorteil
        ser.end() #vorteile

        ser.beginList('Fertigkeiten')
        for fert in self.fertigkeiten.values():
            ser.begin('Fertigkeit')
            fert.serialize(ser)
            ser.end() #fertigkeit
        ser.end() #fertigkeiten

        ser.beginList('FreieFertigkeiten')
        for fert in self.freieFertigkeiten:
            ser.begin('FreieFertigkeit')
            fert.serialize(ser)
            ser.end() #freiefertigkeit
        ser.end() #freiefertigkeiten

        ser.beginList('Talente')
        for talent in self.talente.values():
            ser.begin('Talent')
            talent.serialize(ser)
            ser.end() #talent
        ser.end() #talente

        ser.begin('Objekte')
        ser.setNested('Zonensystem', self.zonenSystemNutzen)
        ser.beginList('Rüstungen')
        for rüstung in self.rüstung:
            ser.begin('Rüstung')
            rüstung.serialize(ser)
            ser.end() #rüstung
        ser.end() #rüstungen

        ser.beginList('Waffen')
        for waffe in self.waffen:
            ser.begin('Waffe')
            waffe.serialize(ser)
            ser.end() #waffe
        ser.end() #waffen   

        ser.beginList('Ausrüstung')
        for ausr in self.ausrüstung:
            ser.setNested('Ausrüstungsstück', ausr)
        ser.end() #ausrüstung
        ser.end() #objekte
        
        ser.beginList('ÜbernatürlicheFertigkeiten')
        for fert in self.übernatürlicheFertigkeiten.values():
            ser.begin('ÜbernatürlicheFertigkeit')
            fert.serialize(ser)
            ser.end() #übernatürlichefertigkeit
        ser.end() #übernatürlichefertigkeiten

        ser.begin('Erfahrung')
        ser.setNested('Gesamt', self.epGesamt)
        ser.setNested('Ausgegeben', self.epAusgegeben)
        ser.end() #erfahrung

        ser.setNested('Notiz', self.notiz)

        ser.begin('Einstellungen')
        ser.setNested('VoraussetzungenPrüfen', self.voraussetzungenPruefen)
        ser.setNested('Charakterbogen', self.charakterbogen)
        ser.setNested('FinanzenAnzeigen', self.finanzenAnzeigen)
        ser.setNested('ÜbernatürlichesPDFSpalteAnzeigen', self.ueberPDFAnzeigen)
        ser.setNested('DetailsAnzeigen', self.detailsAnzeigen)
        ser.setNested('RegelnAnhängen', self.regelnAnhaengen)
        ser.setNested('RegelnGrösse', self.regelnGroesse)
        ser.setNested('DeaktivierteRegelKategorien', ",".join(self.deaktivierteRegelKategorien))
        ser.setNested('FormularEditierbarkeit', self.formularEditierbar)
        ser.setNested('VorteilFavoriten', ",".join(self.vorteilFavoriten))
        ser.end() #einstellungen

        ser.begin('BeschreibungDetails')
        ser.setNested('Kultur', self.kultur)
        ser.setNested('Profession', self.profession)
        ser.setNested('Geschlecht', self.geschlecht)
        ser.setNested('Geburtsdatum', self.geburtsdatum)
        ser.setNested('Grösse', self.groesse)
        ser.setNested('Gewicht', self.gewicht)
        ser.setNested('Haarfarbe', self.haarfarbe)
        ser.setNested('Augenfarbe', self.augenfarbe)
        ser.setNested('Titel', self.titel)
        for i in range(6):
            ser.setNested('Aussehen' + str(i+1), self.aussehen[i])
        for i in range(9):
            ser.setNested('Hintergrund' + str(i), self.hintergrund[i])
        if self.bild:
            ser.setNested('Bild', base64.b64encode(self.bild))
        ser.end() #beschreibungdetails
        
        EventBus.doAction("charakter_serialisiert", { "charakter" : self, "serializer" : ser })

    @staticmethod
    def hausregelnLesen(filename):
        _, fileExtension = os.path.splitext(filename)
        options = { "useCache" : False }
        deserializer = Serialization.getDeserializer(fileExtension, options)

        # NutzerDatenbankName and basename are for legacy reasons - this code runs without migration
        for tag in deserializer.readFileStream(filename, ["Hausregeln", "NutzerDatenbankName"]):
            text = deserializer.get("text")
            if text:
                return os.path.basename(text)
            break
        return "Keine"

    LoadResultNone = 0
    LoadResultInfo = 1
    LoadResultWarning = 2
    LoadResultCritical = 3

    def loadFile(self, filename):
        '''Läd ein Charakter-Objekt aus einer XML Datei, deren Dateiname 
        inklusive Pfad als Argument übergeben wird'''
        _, fileExtension = os.path.splitext(filename)
        options = { "useCache" : False }
        deserializer = Serialization.getDeserializer(fileExtension, options)
        if not deserializer.readFile(filename):
            result = [Char.LoadResultCritical, "Veraltetes Sephrasto", "Du hast den Charakter mit einer neueren Sephrasto-Version erstellt, diese Version kann ihn nicht öffnen"]
            return False, result

        success, loadResult = self.deserialize(deserializer)
        if not success:
            return False, loadResult

        if len(Migrationen.charakterUpdates) > 0:
            text = Migrationen.charakterUpdates[0]
            if len(Migrationen.charakterUpdates) > 1:
                   text = "\n\nWeitere Informationen:\n- " + "\n- ".join(Migrationen.charakterUpdates[1:])

            if loadResult[0] == Char.LoadResultNone:
                loadResult = [Char.LoadResultInfo, "Charakter wurde aktualisiert", text]
            else:
                loadResult[2] += "\n\nDer Charakter wurde außerdem aktualisert: " + text
        return True, loadResult

    def deserialize(self, deserializer):
        ser = EventBus.applyFilter("charakter_deserialisieren", deserializer, { "charakter" : self })

        if ser.currentTag != "Charakter":
            return False, [Char.LoadResultCritical, "Charakter laden nicht möglich", "Es handelt sich um keinen validen Charakter."]

        #Alles bisherige löschen
        self.__init__()

        aIgnored = []
        eIgnored = []
        vIgnored = []
        tIgnored = []
        fIgnored = []
        übIgnored = []
        wIgnored = []

        letzteHausregeln = "Keine"
        if ser.find('Version'):
            plugins = ser.getNested('Plugins')
            if plugins:
                self.enabledPlugins = list(map(str.strip, plugins.split(",")))
            hausregeln = ser.getNested("Hausregeln")
            if hausregeln:
                letzteHausregeln = hausregeln
            ser.end() #version

        if ser.find("Beschreibung"):
            self.name = ser.getNested('Name', self.name)
            self.spezies = ser.getNested('Spezies', self.spezies)
            self.status = ser.getNestedInt("Status", self.status)
            self.kurzbeschreibung = ser.getNested('Kurzbeschreibung', self.kurzbeschreibung)
            self.finanzen = ser.getNestedInt('Finanzen', self.finanzen)
            self.heimat = ser.getNested('Heimat', self.heimat)
            heimaten = sorted(Wolke.DB.einstellungen["Heimaten"].wert)
            if not self.heimat in heimaten:
                if "Mittelreich" in heimaten:
                    self.heimat = "Mittelreich"
                else:
                    self.heimat = heimaten[0] if len(heimaten) > 0 else ""

            if ser.find('Eigenheiten'):
                for tag in ser.listTags():
                    eigenheit = ser.getNested(tag)
                    if eigenheit:
                        self.eigenheiten.append(eigenheit)
                ser.end() #eigenheiten
            ser.end() #beschreibung

        if ser.find('Attribute'):
            for tag in ser.listTags():
                attribut = Attribut.__new__(Attribut)
                if not attribut.deserialize(ser, Wolke.DB.attribute, self):
                    aIgnored.append(attribut.name)
                    continue
                self.attribute[attribut.name] = attribut
            ser.end() #attribute

        if ser.find('Energien'):
            for tag in ser.listTags():
                energie = Energie.__new__(Energie)
                if not energie.deserialize(ser, Wolke.DB.energien, self):
                    eIgnored.append(energie.name)
                    continue
                self.energien[energie.name] = energie
            ser.end() #energien

        if ser.find('Vorteile'):
            for tag in ser.listTags():
                vorteil = Vorteil.__new__(Vorteil)
                if not vorteil.deserialize(ser, Wolke.DB.vorteile, self):
                    vIgnored.append(vorteil.name)
                    continue
                self.vorteile[vorteil.name] = vorteil
            ser.end() #vorteile

        if "Minderpakt" in self.vorteile:
            minderpakt = self.vorteile["Minderpakt"]
            if not minderpakt.kommentar in Wolke.DB.vorteile:
                vIgnored.append("Minderpakt")
                self.removeVorteil(minderpakt)
            else:
                minderpakt.voraussetzungen = VoraussetzungenListe().compile("Vorteil " + minderpakt.kommentar, Wolke.DB)
                if minderpakt.kommentar in self.vorteile:
                    vorteil = self.vorteile[minderpakt.kommentar]
                    vorteil.voraussetzungen = VoraussetzungenListe().compile("Vorteil Minderpakt", Wolke.DB)
                    vorteil.kosten = 20

        if ser.find('Fertigkeiten'):
            for tag in ser.listTags():
                fert = Fertigkeit.__new__(Fertigkeit)
                if not fert.deserialize(ser, Wolke.DB.fertigkeiten, self):
                    fIgnored.append(fert.name)
                    continue
                self.fertigkeiten[fert.name] = fert
            ser.end() #fertigkeiten

        if ser.find('FreieFertigkeiten'):
            for tag in ser.listTags():
                fert = FreieFertigkeit.__new__(FreieFertigkeit)
                if not fert.deserialize(ser, Wolke.DB.freieFertigkeiten, self):
                    continue
                self.freieFertigkeiten.append(fert)
            ser.end() #freiefertigkeiten

        if ser.find('Objekte'):
            self.zonenSystemNutzen = ser.getNestedBool('Zonensystem')
            if ser.find('Rüstungen'):
                for tag in ser.listTags():
                    rüstung = Ruestung.__new__(Ruestung)
                    if not rüstung.deserialize(ser, Wolke.DB.rüstungen, self):
                        continue
                    self.rüstung.append(rüstung)
                ser.end() #rüstungen

            if ser.find('Waffen'):
                for tag in ser.listTags():
                    waffe = Waffe.__new__(Waffe)
                    if not waffe.deserialize(ser, Wolke.DB.waffen, self):
                        self.waffen.append(Waffe(WaffeDefinition()))
                        if waffe.name:
                            wIgnored.append(waffe.name)
                        continue
                    self.waffen.append(waffe)
                ser.end() #waffen

            if ser.find('Ausrüstung'):
                for tag in ser.listTags():
                    self.ausrüstung.append(ser.getNested(tag, ""))
                ser.end() #ausrüstung

            ser.end() #objekte

        if ser.find('ÜbernatürlicheFertigkeiten'):
            for tag in ser.listTags():
                fert = Fertigkeit.__new__(Fertigkeit)
                if not fert.deserialize(ser, Wolke.DB.übernatürlicheFertigkeiten, self):
                    übIgnored.append(fert.name)
                    continue
                self.übernatürlicheFertigkeiten[fert.name] = fert
            ser.end() #übernatürlichefertigkeiten

        if ser.find('Talente'):
            for tag in ser.listTags():
                talent = Talent.__new__(Talent)
                if not talent.deserialize(ser, Wolke.DB.talente, self):
                    tIgnored.append(talent.name)
                    continue
                if talent.name in self.talente: #heimat...
                    continue
                self.talente[talent.name] = talent
            ser.end() #talente

        if ser.find('Erfahrung'):
            self._epGesamt = ser.getNestedInt('Gesamt', self.epGesamt)
            self.epAusgegeben = ser.getNestedInt('Ausgegeben', self.epAusgegeben)
            ser.end() #erfahrung
  
        self.notiz = ser.getNested('Notiz', self.notiz)

        if ser.find('Einstellungen'):          
            self.charakterbogen = ser.getNested('Charakterbogen', self.charakterbogen)
            self.voraussetzungenPruefen = ser.getNestedBool('VoraussetzungenPrüfen', self.voraussetzungenPruefen)
            self.finanzenAnzeigen = ser.getNestedBool('FinanzenAnzeigen', self.finanzenAnzeigen)
            self.ueberPDFAnzeigen = ser.getNestedBool('ÜbernatürlichesPDFSpalteAnzeigen', self.ueberPDFAnzeigen)
            self.detailsAnzeigen = ser.getNestedBool('DetailsAnzeigen', self.detailsAnzeigen)
            self.regelnAnhaengen = ser.getNestedBool('RegelnAnhängen', self.regelnAnhaengen)
            self.regelnGroesse = ser.getNestedInt('RegelnGrösse', self.regelnGroesse)
            self.formularEditierbar = ser.getNestedBool('FormularEditierbarkeit', self.formularEditierbar)
            deaktivierteRegelKategorien = ser.getNested('DeaktivierteRegelKategorien')
            if deaktivierteRegelKategorien:
                self.deaktivierteRegelKategorien = list(map(str.strip, deaktivierteRegelKategorien.split(",")))
            vorteilFavoriten = ser.getNested('VorteilFavoriten', self.vorteilFavoriten)
            if vorteilFavoriten:
                self.vorteilFavoriten = list(map(str.strip, vorteilFavoriten.split(",")))
            ser.end() #einstellungen

        if ser.find('BeschreibungDetails'):
            self.kultur = ser.getNested('Kultur', self.kultur)
            self.profession = ser.getNested('Profession', self.profession)
            self.geschlecht = ser.getNested('Geschlecht', self.geschlecht)
            self.geburtsdatum = ser.getNested('Geburtsdatum', self.geburtsdatum)
            self.groesse = ser.getNested('Grösse', self.groesse)
            self.gewicht = ser.getNested('Gewicht', self.gewicht)
            self.haarfarbe = ser.getNested('Haarfarbe', self.haarfarbe)
            self.augenfarbe = ser.getNested('Augenfarbe', self.augenfarbe)
            self.titel = ser.getNested('Titel', self.titel)
            for i in range(6):
                self.aussehen[i] = ser.getNested('Aussehen' + str(i+1), self.aussehen[i])
            for i in range(9):
                self.hintergrund[i] = ser.getNested('Hintergrund' + str(i), self.hintergrund[i])

            bild = ser.getNested('Bild')
            if bild is not None:
                byteArray = bytes(bild, 'utf-8')
                self.bild = base64.b64decode(byteArray)

            ser.end() #beschreibungdetails

        EventBus.doAction("charakter_deserialisiert", { "charakter" : self , "deserializer" : ser })

        hausregelMissmatch = Wolke.DB.hausregelnAnzeigeName != letzteHausregeln
        anyIgnored = aIgnored or eIgnored or vIgnored or fIgnored or tIgnored or übIgnored or wIgnored
        if hausregelMissmatch or anyIgnored:
            strArr = ["Achtung, die Hausregeln haben sich geändert!"]

            if hausregelMissmatch:
                strArr.append(f"\n- Vorher: ")
                strArr.append(letzteHausregeln)
                strArr.append("\n- Jetzt: ")
                strArr.append(Wolke.DB.hausregelnAnzeigeName)

            strArr.append("\n\nDein Charakter wurde an die neuen Regeln angepasst. Überspeichere ihn nur wenn du dir sicher bist, dass alles in Ordnung ist.\n\n")
            if anyIgnored:           
                strArr.append("Das Folgende war charakterrelevant und wurde aus den Regeln gelöscht:")
                if aIgnored:
                    strArr.append("\n- Attribute: ")
                    strArr.append(", ".join(aIgnored))
                if eIgnored:
                    strArr.append("\n- Energien: ")
                    strArr.append(", ".join(eIgnored))
                if vIgnored:
                    strArr.append("\n- Vorteile: ")
                    strArr.append(", ".join(vIgnored))
                if fIgnored:
                    strArr.append("\n- Fertigkeiten: ")
                    strArr.append(", ".join(fIgnored))
                if tIgnored:
                    strArr.append("\n- Talente: ")
                    strArr.append(", ".join(tIgnored))
                if übIgnored:
                    strArr.append("\n- Übernatürliche Fertigkeiten: ")
                    strArr.append(", ".join(übIgnored))
                if wIgnored:
                    strArr.append("\n- Waffen: ")
                    strArr.append(", ".join(wIgnored))
            else:
                strArr.append("Es ist nichts verloren gegangen, alle Vorteile, Talente etc. sind in den neuen Regeln noch vorhanden.")

            text = "\n" + "".join(strArr)
            logging.warning(text)
            return True, [Char.LoadResultWarning, "Charakter laden - Hausregeln wurden geändert.", text]
        return True, [Char.LoadResultNone, "", ""]