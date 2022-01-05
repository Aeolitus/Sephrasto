import Definitionen
import Fertigkeiten
import Objekte
import lxml.etree as etree
import re
import binascii
import copy
import logging
import collections
from EventBus import EventBus
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from PyQt5 import QtWidgets, QtCore
import os.path

class KampfstilMod():
    def __init__(self):
        self.AT = 0
        self.VT = 0
        self.TP = 0
        self.RW = 0
        self.BE = 0
        self.BEIgnore = [] #Tupel aus Kampffertigkeit und Talent für welche die BE ignoriert wird

    def __deepcopy__(self):
      clone = type(self)()
      clone.__dict__.update(self.__dict__)
      clone.beIgnore = copy.deepcopy(self.beIgnore)
      return clone

class Waffenwerte():
    def __init__(self):
        self.AT = 0
        self.VT = 0
        self.RW = 0
        self.TPW6 = 0
        self.TPPlus = 0
        self.Haerte = 0
        self.Kampfstil = ""

class VariableKosten():
    def __init__(self):
        self.kosten = 0
        self.kommentar = ""

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
        self.name = ''
        self.rasse = ''
        self.status = 2
        self.kurzbeschreibung = ''
        self.heimat = ''
        self.schipsMax = 4
        self.schips = 4

        self.finanzen = 2;
        self.eigenheiten = []

        #Zweiter Block: Attribute und Abgeleitetes
        self.attribute = {}
        for key in Definitionen.Attribute.keys():
            self.attribute[key] = Fertigkeiten.Attribut(key)
        self.wsBasis = -1
        self.ws = -1
        self.wsStern = -1
        self.mrBasis = -1
        self.mr = -1
        self.gsBasis = -1
        self.gs = -1
        self.dh = -1
        self.schadensbonusBasis = -1
        self.schadensbonus = -1
        self.iniBasis = -1
        self.ini = -1
        self.asp = Fertigkeiten.Energie()
        self.aspBasis = 0
        self.aspMod = 0
        self.kap = Fertigkeiten.Energie()
        self.kapBasis = 0
        self.kapMod = 0
        
        #Dritter Block: Vorteile, gespeichert als String
        self.vorteile = []
        self.vorteileVariable = {} #Contains Name: VariableKosten
        self.minderpakt = None
        self.kampfstilMods = {}

        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.fertigkeiten = copy.deepcopy(Wolke.DB.fertigkeiten)
        self.freieFertigkeiten = []
        self.freieFertigkeitenNumKostenlos = EventBus.applyFilter("freiefertigkeit_num_kostenlos", 1)
        self.talenteVariable = {} #Contains Name: VariableKosten

        #Fünfter Block: Ausrüstung etc
        self.be = 0
        self.rüstung = []
        self.waffen = []
        self.waffenwerte = []
        self.currentEigenschaft = None #used by waffenScriptAPI during iteration
        self.currentWaffenwerte = None #used by waffenScriptAPI during iteration
        self.ausrüstung = []
        self.rüstungsgewöhnung = 0
        self.rsmod = 0
        self.waffenEigenschaftenUndo = [] #For undoing changes made by Vorteil scripts
        self.zonenSystemNutzen = False

        #Sechster Block: Übernatürliches
        self.übernatürlicheFertigkeiten = copy.deepcopy(
            Wolke.DB.übernatürlicheFertigkeiten)

        #Siebter Block: EP
        self.EPtotal = 0
        self.EPspent = 0
        
        self.EP_Attribute = 0
        self.EP_Vorteile = 0
        self.EP_Fertigkeiten = 0
        self.EP_Fertigkeiten_Talente = 0
        self.EP_FreieFertigkeiten = 0
        self.EP_Uebernatuerlich = 0
        self.EP_Uebernatuerlich_Talente = 0

        #Achter Block: Notiz
        self.notiz = ""

        #Neunter Block: Flags etc
        self.höchsteKampfF = -1

        # Diagnostics
        self.fehlercode = 0

        #Versionierung
        #Wenn die Ref-DB eine Änderung erhält durch die existierende Charakter-XMLs aktualisiert werden müssen,
        #kann hier die Datenbank Code Version inkrementiert werden und in der Migrationen-Map eine Migrationsfunktion für die neue Version angelegt werden.
        #In dieser Funktion kann dann die Charakter-XML-Datei angepasst werden, bevor sie geladen wird.
        #WICHTIG: Bei Vorteilen/(ÜB-)Fertigkeiten/Talenten nur solche migrieren, bei denen in der aktuell geladenen Datenbasis userAdded == False ist, außer das schema hat sich geändert.
        #Die Migrationsfunktion sollte einen string zurückgeben, der erklärt was geändert wurde - dies wird dem Nutzer in einer Messagebox angezeigt.
        #Die Funktionen werden inkrementell ausgeführt, bspw. bei Charakter-DB-Version '0' und Code-DB-Version '2' wird zuerst die Funktion für 1, dann die Funktion für 2 aufgerufen
        self.datenbankCodeVersion = 2
        self.migrationen = [
            lambda xmlRoot: None, #nichts zu tun, initiale db version
            self.migriere0zu1,
            self.migriere1zu2
        ]

        if not self.migrationen[self.datenbankCodeVersion]:
            raise Exception("Migrations-Code vergessen.")



        #Bei Änderungen nicht vergessen die script docs in ScriptAPI.md anzupassen
        self.charakterScriptAPI = {
            #Hintergrund
            'getName' : lambda: self.name,
            'getRasse' : lambda: self.rasse,
            'getStatus' : lambda: self.status,
            'getKurzbeschreibung' : lambda: self.kurzbeschreibung,
            'getHeimat' : lambda: self.heimat,
            'getFinanzen' : lambda: self.finanzen,
            'getEigenheiten' : lambda: copy.deepcopy(self.eigenheiten),
            'getEPTotal' : lambda: self.EPtotal,
            'getEPSpent' : lambda: self.EPspent,

            #Fertigkeiten, Vorteile & Ausrüstung
            'getFertigkeit' : lambda name: copy.deepcopy(self.fertigkeiten[name]),
            'getÜbernatürlicheFertigkeit' : lambda name: copy.deepcopy(self.übernatürlicheFertigkeiten[name]),
            'getFreieFertigkeiten' : lambda: copy.deepcopy(self.freieFertigkeiten),
            'getVorteile' : lambda: copy.deepcopy([el for el in Wolke.DB.vorteile if el in self.vorteile]),
            'getRüstung' : lambda: copy.deepcopy(self.rüstung),
            'getWaffen' : lambda: copy.deepcopy(self.waffen),
            'getAusrüstung' : lambda: copy.deepcopy(self.ausrüstung),
            'modifyFertigkeitBasiswert' : lambda name, mod: setattr(self.fertigkeiten[name], 'basiswertMod', self.fertigkeiten[name].basiswertMod + mod),
            'modifyÜbernatürlicheFertigkeitBasiswert' : self.API_modifyÜbernatürlicheFertigkeitBasiswert,
            'modifyTalent' : self.API_modifyTalent,

            #Asp
            'getAsPBasis' : lambda: self.aspBasis,
            'setAsPBasis' : lambda aspBasis: setattr(self, 'aspBasis', aspBasis),
            'modifyAsPBasis' : lambda aspBasis: setattr(self, 'aspBasis', self.aspBasis + aspBasis),
            'getAsPMod' : lambda: self.aspMod,
            'setAsPMod' : lambda aspMod: setattr(self, 'aspMod', aspMod),
            'modifyAsPMod' : lambda aspMod: setattr(self, 'aspMod', self.aspMod + aspMod),

            #Kap
            'getKaPBasis' : lambda: self.kapBasis,
            'setKaPBasis' : lambda kapBasis: setattr(self, 'kapBasis', kapBasis),
            'modifyKaPBasis' : lambda kapBasis: setattr(self, 'kapBasis', self.kapBasis + kapBasis),
            'getKaPMod' : lambda: self.kapMod,
            'setKaPMod' : lambda kapMod: setattr(self, 'kapMod', kapMod),
            'modifyKaPMod' : lambda kapMod: setattr(self, 'kapMod', self.kapMod + kapMod),

            #Schip
            'getSchiPMax' : lambda: self.schipsMax,
            'setSchiPMax' : lambda schipsMax: setattr(self, 'schipsMax', schipsMax),
            'modifySchiPMax' : lambda schipsMax: setattr(self, 'schipsMax', self.schipsMax + schipsMax),

            #WS
            'getWSBasis' : lambda: self.wsBasis,
            'getWS' : lambda: self.ws,
            'setWS' : lambda ws: setattr(self, 'ws', ws),
            'modifyWS' : lambda ws: setattr(self, 'ws', self.ws + ws),
            'getWSStern' : lambda: self.wsStern,

            #MR
            'getMRBasis' : lambda: self.mrBasis,
            'getMR' : lambda: self.ws,
            'setMR' : lambda mr: setattr(self, 'mr', mr),
            'modifyMR' : lambda mr: setattr(self, 'mr', self.mr + mr),

            #GS
            'getGSBasis' : lambda: self.gsBasis,
            'getGS' : lambda: self.gs,
            'setGS' : lambda gs: setattr(self, 'gs', gs),
            'modifyGS' : lambda gs: setattr(self, 'gs', self.gs + gs),

            #DH
            'getDH' : lambda: self.dh,
            'setDH' : lambda dh: setattr(self, 'dh', dh),
            'modifyDH' : lambda dh: setattr(self, 'dh', self.dh + dh),

            #Schadensbonus
            'getSchadensbonusBasis' : lambda: self.schadensbonusBasis,
            'getSchadensbonus' : lambda: self.schadensbonus,
            'setSchadensbonus' : lambda schadensbonus: setattr(self, 'schadensbonus', schadensbonus),
            'modifySchadensbonus' : lambda schadensbonus: setattr(self, 'schadensbonus', self.schadensbonus + schadensbonus),

            #INI
            'getINIBasis' : lambda: self.iniBasis,
            'getINI' : lambda: self.ini,
            'setINI' : lambda ini: setattr(self, 'ini', ini),
            'modifyINI' : lambda ini: setattr(self, 'ini', self.ini + ini),

            #RS
            'getRSMod' : lambda: self.rsmod,
            'setRSMod' : lambda rsmod: setattr(self, 'rsmod', rsmod),
            'modifyRSMod' : lambda rsmod: setattr(self, 'rsmod', self.rsmod + rsmod),

            #BE
            'getBEBasis' : lambda: self.be,
            'getBEMod' : lambda: self.rüstungsgewöhnung,
            'setBEMod' : lambda beMod: setattr(self, 'rüstungsgewöhnung', beMod),
            'modifyBEMod' : lambda beMod: setattr(self, 'rüstungsgewöhnung', self.rüstungsgewöhnung + beMod),

            #Kampfstil
             'getKampfstil' : lambda kampfstil: copy.copy(self.kampfstilMods[kampfstil]),
             'setKampfstil' : self.API_setKampfstil,
             'modifyKampfstil' : self.API_modifyKampfstil,
             'setKampfstilBEIgnore' : lambda kampfstil, fertigkeit, talent: self.kampfstilMods[kampfstil].BEIgnore.append([fertigkeit, talent]),

            #Attribute
            'getAttribut' : lambda attribut: self.attribute[attribut].wert,

            #Misc
            'addWaffeneigenschaft' : self.API_addWaffeneigenschaft,
            'removeWaffeneigenschaft' : self.API_removeWaffeneigenschaft
        }

        #Add Attribute to API (readonly)
        for attribut in self.attribute.values():
            self.charakterScriptAPI["get" + attribut.key] = lambda attribut=attribut.key: self.attribute[attribut].wert
        
        self.waffenScriptAPI = {
            'getEigenschaftParam' : lambda paramNb: self.API_getWaffeneigenschaftParam(paramNb),
            'modifyWaffeAT' : lambda atmod: setattr(self.currentWaffenwerte, 'AT', self.currentWaffenwerte.AT + atmod),
            'modifyWaffeVT' : lambda vtmod: setattr(self.currentWaffenwerte, 'VT', self.currentWaffenwerte.VT + vtmod),
            'modifyWaffeTPW6' : lambda tpw6mod: setattr(self.currentWaffenwerte, 'TPW6', self.currentWaffenwerte.TPW6 + tpw6mod),
            'modifyWaffeTPPlus' : lambda tpplusmod: setattr(self.currentWaffenwerte, 'TPPlus', self.currentWaffenwerte.TPPlus + tpplusmod),
            'modifyWaffeHaerte' : lambda haertemod: setattr(self.currentWaffenwerte, 'Haerte', self.currentWaffenwerte.Haerte + haertemod),
            'modifyWaffeRW' : lambda rwmod: setattr(self.currentWaffenwerte, 'RW', self.currentWaffenwerte.RW + rwmod),
            'setWaffeAT' : lambda at: setattr(self.currentWaffenwerte, 'AT', at),
            'setWaffeVT' : lambda vt: setattr(self.currentWaffenwerte, 'VT', vt),
            'setWaffeTPW6' : lambda tpw6: setattr(self.currentWaffenwerte, 'TPW6', tpw6),
            'setWaffeTPPlus' : lambda tpplus: setattr(self.currentWaffenwerte, 'TPPlus', tpplus),
            'setWaffeHaerte' : lambda haerte: setattr(self.currentWaffenwerte, 'Haerte', haerte),
            'setWaffeRW' : lambda rw: setattr(self.currentWaffenwerte, 'RW', rw),
            'getWaffenWerte' : lambda: copy.deepcopy(self.currentWaffenwerte),
        }

        for k,v in self.charakterScriptAPI.items():
            if k in self.waffenScriptAPI:
                assert False, "Duplicate entry"
            self.waffenScriptAPI[k] = v

    def API_modifyTalent(self, fertigkeit, talent, condition, mod):
        fert = self.fertigkeiten[fertigkeit]
        if not talent in fert.talentMods:
            fert.talentMods[talent] = {}

        if not condition in fert.talentMods[talent]:
            fert.talentMods[talent][condition] = mod
        else:
            fert.talentMods[talent][condition] += mod

    def API_modifyÜbernatürlicheFertigkeitBasiswert (self, name, mod):
        if not name in self.übernatürlicheFertigkeiten:
            return

        self.übernatürlicheFertigkeiten[name].basiswertMod += mod

    def API_setKampfstil(self, kampfstil, at, vt, tp, rw, be = 0):
        k = self.kampfstilMods[kampfstil]
        k.AT = at
        k.VT = vt
        k.TP = tp
        k.RW = rw
        k.BE = (be or 0)
    
    def API_modifyKampfstil(self, kampfstil, at, vt, tp, rw, be = 0):
        k = self.kampfstilMods[kampfstil]
        self.API_setKampfstil(kampfstil, k.AT + at, k.VT + vt, k.TP + tp, k.RW + rw, k.BE + be)

    def API_addWaffeneigenschaft(self, talentName, eigenschaft):
        self.modifyWaffeneigenschaft(talentName, eigenschaft, False)

    def API_removeWaffeneigenschaft(self, talentName, eigenschaft):
        self.modifyWaffeneigenschaft(talentName, eigenschaft, True)

    def modifyWaffeneigenschaft(self, talentName, eigenschaft, remove):
        for waffe in self.waffen:
            talent = None
            eigenschaftExists = False
            if waffe.name in Wolke.DB.waffen:
                dbWaffe = Wolke.DB.waffen[waffe.name]
                talent = dbWaffe.talent
                if (not remove) and (eigenschaft in dbWaffe.eigenschaften):
                    continue
                if remove and not (eigenschaft in dbWaffe.eigenschaften):
                    continue
            if talent != talentName:
                continue
            self.waffenEigenschaftenUndo.append([waffe, eigenschaft, remove])
            if remove:
                if not (eigenschaft in waffe.eigenschaften):
                    continue
                waffe.eigenschaften.remove(eigenschaft)
            else:
                if eigenschaft in waffe.eigenschaften:
                    continue
                waffe.eigenschaften.append(eigenschaft)

    def API_getWaffeneigenschaftParam(self, paramNb):
        match = re.search(r"\((.*?)\)", self.currentEigenschaft, re.UNICODE)
        if not match:
            raise Exception("Die Waffeneigenschaft '" + self.currentEigenschaft + "' erfordert einen Parameter, aber es wurde keiner gefunden")
        parameters = list(map(str.strip, match.group(1).split(";")))
        if not len(parameters) >= paramNb:
            raise Exception("Die Waffeneigenschaft '" + self.currentEigenschaft + "' erfordert " + paramNb + " Parameter, aber es wurden nur " + len(parameters) + " gefunden. Parameter müssen mit Semikolon getrennt werden")
        return parameters[paramNb-1]

    def migriere0zu1(self, xmlRoot):
        Kampfstile = ["Kein Kampfstil", "Beidhändiger Kampf", "Parierwaffenkampf", "Reiterkampf", 
              "Schildkampf", "Kraftvoller Kampf", "Schneller Kampf"]

        for waf in xmlRoot.findall('Objekte/Waffen/Waffe'):
            kampfstilIndex = int(waf.attrib['kampfstil'])
            waf.attrib['kampfstil'] = Kampfstile[kampfstilIndex]

        return "Datenbank Schema-Änderung (der selektierte Kampfstil bei Waffen wurde von indexbasiert zu stringbasiert geändert)"

    def migriere1zu2(self, xmlRoot):
        VorteileAlt = ["Angepasst I (Wasser)", "Angepasst I (Wald)", "Angepasst I (Dunkelheit)", "Angepasst I (Schnee)", "Angepasst II (Wasser)", "Angepasst II (Wald)", "Angepasst II (Dunkelheit)", "Angepasst II (Schnee)", "Tieremphatie"]
        VorteileNeu = ["Angepasst (Wasser) I", "Angepasst (Wald) I", "Angepasst (Dunkelheit) I", "Angepasst (Schnee) I", "Angepasst (Wasser) II", "Angepasst (Wald) II", "Angepasst (Dunkelheit) II", "Angepasst (Schnee) II", "Tierempathie"]

        for vort in xmlRoot.findall('Vorteile/Vorteil'):
            if vort.text in VorteileAlt:
                vort.text = VorteileNeu[VorteileAlt.index(vort.text)]

        return "Angepasst I (Dunkelheit) etc. wurde in Angepasst (Dunkelheit) I etc. umbenannt"

    def migriere2zu3(self, xmlRoot):
        #Dies würde aufgerufen werden, wenn datenbankCodeVersion 2 oder höher und Charakter-DatenbankVersion geringer als 2 wäre
        #WICHTIG: bei Vorteilen/(ÜB-)Fertigkeiten/Talenten nur solche migrieren, bei denen in der aktuell geladenen Datenbasis userAdded == False ist, außer das Schema hat sich geändert.
        #Beispiel:
        #if not 'Handgemenge' in Wolke.DB.fertigkeiten or not Wolke.DB.fertigkeiten['Handgemenge'].isUserAdded:
        #    for fer in xmlRoot.findall('Fertigkeiten/Fertigkeit'):
        #        if fer.attrib['name'] == 'Handgemenge':
        #            fer.attrib['name'] = 'Raufen'
        #            return "Handgemenge wurde in Raufen umbenannt"
        #return None
        raise Exception('Not implemented')

    def aktualisieren(self):
        EventBus.doAction("pre_charakter_aktualisieren")

        '''Berechnet alle abgeleiteten Werte neu'''
        for key in Definitionen.Attribute:
            self.attribute[key].aktualisieren()

        self.aspBasis = 0
        self.aspMod = 0
        self.kapBasis = 0
        self.kapMod = 0

        self.wsBasis = 4 + int(self.attribute['KO'].wert/4)
        self.ws = self.wsBasis

        self.mrBasis = 4 + int(self.attribute['MU'].wert/4)
        self.mr = self.mrBasis

        self.gsBasis = 4 + int(self.attribute['GE'].wert/4+0.0001)
        self.gs = self.gsBasis

        self.iniBasis = self.attribute['IN'].wert
        self.ini = self.iniBasis     
        
        self.dh = self.attribute['KO'].wert

        self.schadensbonusBasis = int(self.attribute['KK'].wert/4)
        self.schadensbonus = self.schadensbonusBasis

        self.schipsMax = 4
      
        self.be = 0
        self.rüstungsgewöhnung = 0
        if len(self.rüstung) > 0:
            self.be = self.rüstung[0].be
        self.rsmod = 0

        self.kampfstilMods = {}
        for ks in Wolke.DB.findKampfstile():
            self.kampfstilMods[ks] = KampfstilMod()

        #Undo previous changes by Vorteil scripts before executing them again
        for value in self.waffenEigenschaftenUndo:
            waffe = value[0]
            wEigenschaft = value[1]
            remove = value[2]
            if (not remove) and (wEigenschaft in waffe.eigenschaften):
                waffe.eigenschaften.remove(wEigenschaft)
            elif remove and (not (wEigenschaft in waffe.eigenschaften)):
                waffe.eigenschaften.append(wEigenschaft)
        self.waffenEigenschaftenUndo = []

        for fert in self.fertigkeiten:
            self.fertigkeiten[fert].basiswertMod = 0
            self.fertigkeiten[fert].talentMods = {}

        for fert in self.übernatürlicheFertigkeiten:
            self.übernatürlicheFertigkeiten[fert].basiswertMod = 0
            self.übernatürlicheFertigkeiten[fert].talentMods = {}

        #Execute Vorteil scripts to modify character stats
        vorteileByPrio = collections.defaultdict(list)
        for vortName in self.vorteile:
            if not vortName in Wolke.DB.vorteile:
                continue
            vort = Wolke.DB.vorteile[vortName]
            if not vort.script:
                continue
            vorteileByPrio[vort.scriptPrio].append(vort)

        for key in sorted(vorteileByPrio):
            for vort in vorteileByPrio[key]:
                logging.info("Character: applying script for Vorteil " + vort.name)
                exec(vort.script, self.charakterScriptAPI)

        #Update these values afterwards because values they depend on might be modified by Vorteil scripts
        self.be = max(0,self.be-self.rüstungsgewöhnung)

        self.wsStern = self.rsmod + self.ws
        if len(self.rüstung) > 0:
            self.wsStern += self.rüstung[0].getRSGesamtInt()

        self.schips = self.schipsMax
        if self.finanzen >= 2: 
            self.schips += self.finanzen - 2
        else:
            self.schips -= (2-self.finanzen)*2

        self.updateVorts()
        self.updateFerts()
        self.updateWaffenwerte()

        EventBus.doAction("post_charakter_aktualisieren")
        self.epZaehlen()

    def updateWaffenwerte(self):
        self.waffenwerte = []

        for el in self.waffen:
            waffenwerte = Waffenwerte()
            self.waffenwerte.append(waffenwerte)
            waffenwerte.RW = el.rw
            waffenwerte.TPW6 = el.W6
            waffenwerte.TPPlus = el.plus
            waffenwerte.Haerte = el.haerte
            waffenwerte.Kampfstil = el.kampfstil

            # Calculate modifiers for AT, PA, TP from Kampfstil and Talent
            if el.name in Wolke.DB.waffen:
                fertig = Wolke.DB.waffen[el.name].fertigkeit
                tale = Wolke.DB.waffen[el.name].talent
            else:
                fertig = ""
                tale = ""
            if not fertig in self.fertigkeiten:
                continue

            if tale in self.fertigkeiten[fertig].gekaufteTalente:
                bwert = self.fertigkeiten[fertig].probenwertTalent
            else:
                bwert = self.fertigkeiten[fertig].probenwert
                
            kampfstilMods = None
            if el.kampfstil in self.kampfstilMods:
                kampfstilMods = self.kampfstilMods[el.kampfstil]
            else:
                kampfstilMods = KampfstilMod()
                if el.kampfstil != Definitionen.KeinKampfstil:
                    logging.warn("Waffe " + el.name + " referenziert einen nicht existierenden Kampfstil: " + el.kampfstil)

            waffenwerte.AT = bwert + kampfstilMods.AT
            waffenwerte.VT = bwert + kampfstilMods.VT
            waffenwerte.TPPlus += kampfstilMods.TP
            waffenwerte.RW += kampfstilMods.RW
            waffenwerte.AT += el.wm
            waffenwerte.VT += el.wm

            schadensbonusWirkt = type(el) == Objekte.Nahkampfwaffe or fertig == "Wurfwaffen"
            schadensbonusWirkt = EventBus.applyFilter("waffe_schadensbonus_wirkt", schadensbonusWirkt, { "waffe" : el })
            if schadensbonusWirkt:
                waffenwerte.TPPlus += self.schadensbonus

            ignoreBE = False
            for values in kampfstilMods.BEIgnore:
                if values[0] == fertig and values[1] == tale:
                    ignoreBE = True
                    break
            if not ignoreBE:
                be = max(self.be + kampfstilMods.BE, 0)
                waffenwerte.AT -= be
                waffenwerte.VT -= be

            self.currentWaffenwerte = waffenwerte

            #Execute Waffeneigenschaft scripts to modify character/weapon stats
            eigenschaftenByPrio = collections.defaultdict(list)
            for weName in el.eigenschaften:
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
                    exec(we.script, self.waffenScriptAPI)

            self.currentWaffenwert = None
            self.currentEigenschaft = None

    def getDefaultTalentCost(self, talent, steigerungsfaktor):
        cost = 0
        if Wolke.DB.talente[talent].kosten != -1:
            cost = Wolke.DB.talente[talent].kosten
        elif Wolke.DB.talente[talent].verbilligt:
            cost = 10*steigerungsfaktor
        else:
            cost = 20*steigerungsfaktor

        cost = EventBus.applyFilter("talent_kosten", cost, { "talent": talent })
        return cost

    def getTalentCost(self, talent, steigerungsfaktor):
        if talent in self.talenteVariable:
            return self.talenteVariable[talent].kosten
        return self.getDefaultTalentCost(talent, steigerungsfaktor)

    def epZaehlen(self):
        '''Berechnet die bisher ausgegebenen EP'''
        spent = 0
        #Erster Block ist gratis
        #Zweiter Block: Attribute und Abgeleitetes
        for key in Definitionen.Attribute:
            val = sum(range(self.attribute[key].wert+1)) *\
                        self.attribute[key].steigerungsfaktor
            spent += EventBus.applyFilter("attribut_kosten", val, { "attribut" : key, "wert" : self.attribute[key].wert })

        val = sum(range(self.asp.wert+1))*self.asp.steigerungsfaktor
        spent += EventBus.applyFilter("asp_kosten", val, { "wert" : self.asp.wert })
        val = sum(range(self.kap.wert+1))*self.kap.steigerungsfaktor   
        spent += EventBus.applyFilter("kap_kosten", val, { "wert" : self.kap.wert })

        self.EP_Attribute = spent
        #Dritter Block: Vorteile
        for vor in self.vorteile:
            if vor == self.minderpakt:
                if "Minderpakt" in self.vorteile:
                    spent += 20
                    continue
                else:
                    self.minderpakt = None
            if vor in self.vorteileVariable:
                spent += self.vorteileVariable[vor].kosten
            elif Wolke.DB.vorteile[vor].kosten != -1:
                spent += Wolke.DB.vorteile[vor].kosten
        
        self.EP_Vorteile = spent - self.EP_Attribute
        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.EP_Fertigkeiten = 0
        self.EP_Fertigkeiten_Talente = 0
        self.EP_FreieFertigkeiten = 0
        paidTalents = []
        for fer in self.fertigkeiten:
            val = sum(range(self.fertigkeiten[fer].wert+1))*\
                        self.fertigkeiten[fer].steigerungsfaktor
            spent += val
            self.EP_Fertigkeiten += val
            for tal in self.fertigkeiten[fer].gekaufteTalente:
                if tal in paidTalents:
                    continue
                if fer == "Gebräuche" and tal[11:] == self.heimat:
                    continue
                paidTalents.append(tal)
                val = self.getTalentCost(tal, self.fertigkeiten[fer].steigerungsfaktor)
                spent += val
                self.EP_Fertigkeiten_Talente += val

        numKostenlos = 0
        for fer in self.freieFertigkeiten:
            # Dont count Muttersprache
            if fer.wert == 3 and numKostenlos < self.freieFertigkeitenNumKostenlos:
                numKostenlos += 1
                continue
            if not fer.name:
                continue
            val = EventBus.applyFilter("freiefertigkeit_kosten", Definitionen.FreieFertigkeitKosten[fer.wert-1], { "name" : fer.name, "wert" : fer.wert })
            spent += val
            self.EP_FreieFertigkeiten += val
        #Fünfter Block ist gratis
        #Sechster Block: Übernatürliches
        self.EP_Uebernatuerlich = 0
        self.EP_Uebernatuerlich_Talente = 0
        for fer in self.übernatürlicheFertigkeiten:
            val = sum(range(self.übernatürlicheFertigkeiten[fer].wert+1))*\
                        self.übernatürlicheFertigkeiten[fer].steigerungsfaktor
            spent += val
            self.EP_Uebernatuerlich += val
            for tal in self.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                if tal in paidTalents:
                    continue
                paidTalents.append(tal)
                val = self.getTalentCost(tal, self.übernatürlicheFertigkeiten[fer].steigerungsfaktor)
                spent += val
                self.EP_Uebernatuerlich_Talente += val
        #Siebter Block ist gratis
        #Achter Block: Fix für höchste Kampffertigkeit
        val = max(0,2*sum(range(self.höchsteKampfF+1)))
        spent += val
        self.EP_Fertigkeiten += val
        #Store
        self.EPspent = spent

    def updateVorts(self):
        ''' 
        Checks for all Vorteile if the requirements are still met until in one 
        run, all of them meet the requirements. This gets rid of stacks of them
        that all depend onto each other, like Zauberer I-IV when removing I
        '''
        while True:
            contFlag = True
            remove = []
            for vor in self.vorteile:
                if vor == self.minderpakt:
                    if "Minderpakt" in self.vorteile:
                        continue
                    else:
                        self.minderpakt = None
                if not self.voraussetzungenPrüfen(Wolke.DB.vorteile[vor]\
                                                  .voraussetzungen):
                    remove.append(vor)
                    contFlag = False
            for el in remove:
                self.vorteile.remove(el)
                EventBus.doAction("vorteil_entfernt", { "name" : el})
            if contFlag:
                break

    def findUnerfüllteVorteilVoraussetzungen(self, vorteile = None, waffen = None, attribute = None, übernatürlicheFertigkeiten = None, fertigkeiten = None):
        ''' 
        Checks for all Vorteile if the requirements are still met until in one 
        run, all of them meet the requirements. This gets rid of stacks of them
        that all depend onto each other, like Zauberer I-IV when removing I.
        The parameters can be used to override character values. If None is specified, the character values are used.
        '''
        vorteile = copy.deepcopy(vorteile or self.vorteile)
        waffen = waffen or self.waffen
        attribute = attribute or self.attribute
        übernatürlicheFertigkeiten = übernatürlicheFertigkeiten or self.übernatürlicheFertigkeiten
        fertigkeiten = fertigkeiten or self.fertigkeiten
        minderpakt = self.minderpakt
        allRemoved = []
        while True:
            contFlag = True
            remove = []
            for vor in vorteile:
                if vor == minderpakt:
                    if "Minderpakt" in vorteile:
                        continue
                    else:
                        allRemoved.append(minderpakt)
                        minderpakt = None
                if not Char.voraussetzungenPrüfenInternal(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, Wolke.DB.vorteile[vor].voraussetzungen):
                    remove.append(vor)
                    allRemoved.append(vor)
                    contFlag = False
            for el in remove:
                vorteile.remove(el)
            if contFlag:
                break

        return allRemoved

    def updateFerts(self):
        '''
        Similar to updateVorts, this removes all Fertigkeiten for which the
        requirements are no longer met until all are removed. Furthermore, all
        Fertigkeiten are updated, which recalculates the PW and such.
        Then, all Fertigkeiten are checked against their maximum value from the 
        attributes and if neccessary, reduced to that value. 
        Last, all Talente are iterated through, their requirements are checked, 
        and it is made sure that they appear at all Fertigkeiten where they are
        available. 
        All this is done both for Fertigkeiten and for Übernatürliche.
        '''
        # Remover 
        while True:
            remove = []
            contFlag = True
            for fert in self.fertigkeiten:
                if not self.voraussetzungenPrüfen(self.fertigkeiten[fert]\
                                                  .voraussetzungen):
                    remove.append(fert)
                    contFlag = False
                self.fertigkeiten[fert].aktualisieren()
            for el in remove:
                self.fertigkeiten.pop(el,None)
            if contFlag:
                break
        while True:
            remove = []
            contFlag = True
            for fert in self.übernatürlicheFertigkeiten:
                if not self.voraussetzungenPrüfen(\
                        self.übernatürlicheFertigkeiten[fert].voraussetzungen):
                    remove.append(fert)
                    contFlag = False
                self.übernatürlicheFertigkeiten[fert].aktualisieren()
            for el in remove:
                self.übernatürlicheFertigkeiten.pop(el,None)
            if contFlag:
                break
                
                
        self.höchsteKampfF = -1
        for fert in self.fertigkeiten:
            self.fertigkeiten[fert].aktualisieren()
            if self.fertigkeiten[fert].wert > self.fertigkeiten[fert].maxWert:
                self.fertigkeiten[fert].wert = self.fertigkeiten[fert].maxWert
                self.fertigkeiten[fert].aktualisieren()
            if self.fertigkeiten[fert].kampffertigkeit == 1 and \
                            self.fertigkeiten[fert].wert > self.höchsteKampfF:
                self.höchsteKampfF = self.fertigkeiten[fert].wert
            for tal in self.fertigkeiten[fert].gekaufteTalente:
                if not self.voraussetzungenPrüfen(
                        Wolke.DB.talente[tal].voraussetzungen):
                    self.fertigkeiten[fert].gekaufteTalente.remove(tal)
                else:
                    for el in self.fertigkeiten[fert].gekaufteTalente:
                        for f in Wolke.DB.talente[el].fertigkeiten:
                            if f in self.fertigkeiten:
                                if el not in self.fertigkeiten[f]\
                                                              .gekaufteTalente:
                                    self.fertigkeiten[f].gekaufteTalente\
                                                     .append(el)
        for fert in self.übernatürlicheFertigkeiten:
            self.übernatürlicheFertigkeiten[fert].aktualisieren()
            if self.übernatürlicheFertigkeiten[fert].wert > \
                                self.übernatürlicheFertigkeiten[fert].maxWert:
                self.übernatürlicheFertigkeiten[fert].wert = \
                                self.übernatürlicheFertigkeiten[fert].maxWert
                self.übernatürlicheFertigkeiten[fert].aktualisieren()
            for tal in self.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                if not self.voraussetzungenPrüfen(Wolke.DB.talente[tal].voraussetzungen):
                    self.übernatürlicheFertigkeiten[fert].gekaufteTalente.remove(tal) 
                else:
                    for el in self.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                        for f in Wolke.DB.talente[el].fertigkeiten:
                            if f in self.übernatürlicheFertigkeiten:
                                if el not in self.übernatürlicheFertigkeiten[f].gekaufteTalente:
                                    self.übernatürlicheFertigkeiten[f].gekaufteTalente.append(el)

    def voraussetzungenPrüfen(self,Vor,Or=False):
        return Char.voraussetzungenPrüfenInternal(self.vorteile, self.waffen, self.attribute, self.übernatürlicheFertigkeiten, self.fertigkeiten, Vor, Or)
    
    def voraussetzungenPrüfenInternal(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, Vor, Or=False):
        '''
        Prüft, ob ein Array von Voraussetzungen erfüllt ist.
        Format: ['L:Str:W', 'L:Str:W']
        Dabei ist L:
            V für Vorteil - prüft, ob ein Vorteil vorhanden ist. W = 1 bedeutet, der
                Vorteil muss vorhanden sein. W=0 bedeutet, der Vorteil darf nicht vorhanden sein.
            T für Talent - prüft, ob der Charakter ein Talent mit dem angegebenen Namen besitzt. W ist immer 1.
            W für Waffeneigenschaft - prüft, ob der Charakter eine Waffe mit der angegebenen Eigenschaft besitzt. W ist immer 1.
            A für Attribut - prüft, ob das Attribut mit Key Str mindestens auf Wert W ist
            M für MeisterAttribut - wie Attribut, prüft außerdem ob zwei weitere Attribute auf insg. mindestens 16 sind
            U für Übernatürliche Fertigkeit - prüft, ob für die Übernatürliche Fertigkeit mit Key Str die Voraussetzungen erfüllt sind \
                und sie mindestens auf Wert W ist. W=-1 hat ein spezielle Bedeutung, hier wird an Stelle des Fertigkeitswerts überprüft ob mindestens ein Talent aktiviert ist.
            F für Fertigkeit - prüft, ob für die Übernatürliche Fertigkeit mit Key Str die Voraussetzungen erfüllt sind und sie mindestens auf Wert W ist.
        Einträge im Array können auch weitere Arrays and Voraussetzungen sein.
        Aus diesen Arrays muss nur ein Eintrag erfüllt sein.
        Wenn Wolke.Reqs nicht gesetzt ist, gibt die Methode immer True zurück.
        '''
        if Wolke.Reqs:
            #Gehe über alle Elemente in der Liste
            retNor = True
            retOr = False
            for voraus in Vor:
                erfüllt = False
                if type(voraus) is list:
                    erfüllt = Char.voraussetzungenPrüfenInternal(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, voraus,True)
                else: 
                    #Split am Separator
                    delim = "~"
                    arr = re.split(delim, voraus, re.UNICODE)
                    #Vorteile:
                    if arr[0] is 'V':
                        if len(arr) > 2:
                            cond = int(arr[2])
                        else: 
                            cond = 1
                        found = 0
                        if arr[1] in vorteile:
                            found = 1
                        if found == 1 and cond == 1:
                            erfüllt = True
                        elif found == 0 and cond == 0:
                            erfüllt = True
                    #Talente:
                    elif arr[0] is 'T':
                        for fert in fertigkeiten.values():
                            if arr[1] in fert.gekaufteTalente:
                                erfüllt = True
                                break
                        if not erfüllt:
                            for fert in übernatürlicheFertigkeiten.values():
                                if arr[1] in fert.gekaufteTalente:
                                    erfüllt = True
                                    break
                    #Waffeneigenschaften:
                    elif arr[0] is 'W':
                        for waffe in waffen:
                            if arr[1] in waffe.eigenschaften:
                                erfüllt = True
                                break
                    #Attribute:
                    elif arr[0] is 'A':
                        #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                        if attribute[arr[1]].wert >= int(arr[2]):
                            erfüllt = True
                    #MeisterAttribute:
                    elif arr[0] is 'M':
                        #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                        if attribute[arr[1]].wert >= int(arr[2]):
                            attrSorted = [a.wert for a in attribute.values() if a.key != arr[1]]
                            attr1 = max(attrSorted)
                            attrSorted.remove(attr1)
                            attr2 = max(attrSorted)
                            erfüllt = attr1 + attr2 >= 16  
                    #Übernatürliche Fertigkeiten:
                    elif arr[0] is 'U':
                        if arr[1] in übernatürlicheFertigkeiten:
                            fertigkeit = übernatürlicheFertigkeiten[arr[1]]
                            wert = int(arr[2])
                            if wert == -1:
                                erfüllt = len(fertigkeit.gekaufteTalente) > 0
                            else:
                                erfüllt = fertigkeit.wert >= wert
                    #Fertigkeiten:
                    elif arr[0] is 'F':
                        if arr[1] in fertigkeiten:
                            fertigkeit = fertigkeiten[arr[1]]
                            erfüllt = fertigkeit.wert >= int(arr[2])
                if not erfüllt:
                    retNor = False
                else:
                    retOr = True
            # Alle Voraussetzungen sind gecheckt und wir sind nirgendwo gefailt.
            if Or and (retNor or retOr):
                return retOr
            else:
                return retNor
        else:
            return True
    
    def xmlSchreiben(self,filename):
        '''Speichert dieses Charakter-Objekt in einer XML Datei, deren 
        Dateiname inklusive Pfad als Argument übergeben wird'''
        #Document Root
        Wolke.Fehlercode = -53

        root = etree.Element('Charakter')

        versionXml = etree.SubElement(root, 'Version')
        etree.SubElement(versionXml, 'DatenbankVersion').text = \
            str(self.datenbankCodeVersion)
        etree.SubElement(versionXml, 'NutzerDatenbankCRC').text = \
            str(binascii.crc32(etree.tostring(Wolke.DB.userDbXml))) if \
            Wolke.DB.userDbXml is not None else "0"
        etree.SubElement(versionXml, 'NutzerDatenbankName').text = \
            os.path.basename(Wolke.DB.datei) if Wolke.DB.datei else ""

        #Erster Block
        Wolke.Fehlercode = -54

        sub =  etree.SubElement(root,'AllgemeineInfos')
        etree.SubElement(sub,'name').text = self.name
        etree.SubElement(sub,'rasse').text = self.rasse
        etree.SubElement(sub,'status').text = str(self.status)
        etree.SubElement(sub,'kurzbeschreibung').text = self.kurzbeschreibung
        etree.SubElement(sub,'schips').text = str(self.schips)
        etree.SubElement(sub,'finanzen').text = str(self.finanzen)
        etree.SubElement(sub,'heimat').text = self.heimat
        eigs = etree.SubElement(sub,'eigenheiten')
        for eigenh in self.eigenheiten:
            etree.SubElement(eigs,'Eigenheit').text = eigenh
        #Zweiter Block - abgeleitete nicht notwendig da automatisch neu berechnet
        Wolke.Fehlercode = -55
        atr = etree.SubElement(root,'Attribute')
        for attr in self.attribute:
            etree.SubElement(atr,attr).text = str(self.attribute[attr].wert)
        en = etree.SubElement(root,'Energien')
        etree.SubElement(en,'AsP').set('wert',str(self.asp.wert))
        etree.SubElement(en,'KaP').set('wert',str(self.kap.wert))
        #Dritter Block    
        Wolke.Fehlercode = -56
        vor = etree.SubElement(root,'Vorteile')
        if self.minderpakt is not None:
            vor.set('minderpakt',self.minderpakt)
        else:
            vor.set('minderpakt','')
        for vort in self.vorteile:
            v = etree.SubElement(vor,'Vorteil')
            v.text = vort
            if vort in self.vorteileVariable:
                v.set('variable',str(self.vorteileVariable[vort].kosten) + "," + self.vorteileVariable[vort].kommentar)
            else:
                v.set('variable','-1')
        #Vierter Block
        Wolke.Fehlercode = -57
        fer = etree.SubElement(root,'Fertigkeiten')
        for fert in self.fertigkeiten:
            fertNode = etree.SubElement(fer,'Fertigkeit')
            fertNode.set('name',self.fertigkeiten[fert].name)
            fertNode.set('wert',str(self.fertigkeiten[fert].wert))
            talentNode = etree.SubElement(fertNode,'Talente')
            for talent in self.fertigkeiten[fert].gekaufteTalente:
                talNode = etree.SubElement(talentNode,'Talent')
                talNode.set('name',talent)
                if talent in self.talenteVariable:
                    talNode.set('variable',str(self.talenteVariable[talent].kosten) + "," + self.talenteVariable[talent].kommentar)
                else:
                    talNode.set('variable','-1')
        Wolke.Fehlercode = -58
        for fert in self.freieFertigkeiten:
            freiNode = etree.SubElement(fer,'Freie-Fertigkeit')
            freiNode.set('name',fert.name)
            freiNode.set('wert',str(fert.wert))
        #Fünfter Block
        Wolke.Fehlercode = -59
        aus = etree.SubElement(root,'Objekte')

        zonenSystem = etree.SubElement(aus,'Zonensystem')
        zonenSystem.text = str(self.zonenSystemNutzen)

        rüs = etree.SubElement(aus,'Rüstungen')
        for rüst in self.rüstung:
            rüsNode = etree.SubElement(rüs,'Rüstung')
            rüsNode.set('name',rüst.name)
            rüsNode.set('be',str(rüst.be))
            rüsNode.set('rs',Hilfsmethoden.RsArray2Str(rüst.rs))
        Wolke.Fehlercode = -60
        waf = etree.SubElement(aus,'Waffen')
        for waff in self.waffen:
            wafNode = etree.SubElement(waf,'Waffe')
            wafNode.set('name',waff.anzeigename)
            wafNode.set('id',waff.name)
            wafNode.set('W6',str(waff.W6))
            wafNode.set('plus',str(waff.plus))
            wafNode.set('eigenschaften',", ".join(waff.eigenschaften))
            wafNode.set('haerte',str(waff.haerte))
            wafNode.set('rw',str(waff.rw))
            wafNode.set('kampfstil',waff.kampfstil)
            wafNode.set('wm',str(waff.wm))
            if type(waff) is Objekte.Nahkampfwaffe:
                wafNode.set('typ','Nah')
            elif type(waff) is Objekte.Fernkampfwaffe:
                wafNode.set('typ','Fern')
                wafNode.set('lz',str(waff.lz))
        Wolke.Fehlercode = -61
        ausrüst = etree.SubElement(aus,'Ausrüstung')
        for ausr in self.ausrüstung:
            etree.SubElement(ausrüst,'Ausrüstungsstück').text = ausr
        #Sechster Block
        Wolke.Fehlercode = -62
        üfer = etree.SubElement(root,'Übernatürliche-Fertigkeiten')
        for fert in self.übernatürlicheFertigkeiten:
            fertNode = etree.SubElement(üfer,'Übernatürliche-Fertigkeit')
            fertNode.set('name',self.übernatürlicheFertigkeiten[fert].name)
            fertNode.set('wert',str(self.übernatürlicheFertigkeiten[fert].wert))
            fertNode.set('addToPDF',str(self.übernatürlicheFertigkeiten[fert].addToPDF))
            talentNode = etree.SubElement(fertNode,'Talente')
            for talent in self.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                talNode = etree.SubElement(talentNode,'Talent')
                talNode.set('name',talent)
                if talent in self.talenteVariable:
                    talNode.set('variable',str(self.talenteVariable[talent].kosten) + "," + self.talenteVariable[talent].kommentar)
                else:
                    talNode.set('variable','-1')
        #Siebter Block
        Wolke.Fehlercode = -63
        epn = etree.SubElement(root,'Erfahrung')
        etree.SubElement(epn,'EPtotal').text = str(self.EPtotal)
        etree.SubElement(epn,'EPspent').text = str(self.EPspent)
        
        #Achter Block
        notiz =  etree.SubElement(root,'Notiz')
        notiz.text = self.notiz

        #Plugins
        root = EventBus.applyFilter("charakter_xml_schreiben", root)

        #Write XML to file
        Wolke.Fehlercode = -64
        doc = etree.ElementTree(root)
        with open(filename,'wb') as file:
            file.seek(0)
            file.truncate()
            doc.write(file, encoding='UTF-8', pretty_print=True)
            file.truncate()
        Wolke.Fehlercode = 0

    def charakterMigrieren(self, xmlRoot, charDBVersion, datenbankCodeVersion):
        strArr = ["Weitere Informationen:"]
        dbChanged = charDBVersion < datenbankCodeVersion
        while charDBVersion < datenbankCodeVersion:
            logging.warning("Migriere Charakter von Version " + str(charDBVersion ) + " zu " + str(charDBVersion + 1))
            charDBVersion +=1
            info = self.migrationen[charDBVersion](xmlRoot)
            if info:
                strArr.append(info)

        if dbChanged:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setWindowTitle("Charakter laden - Datenbank wurde aktualisiert.")
            messageBox.setText("Seit du diesen Charakter das letzte mal bearbeitet hast wurde die offizielle Sephrasto-Datenbank aktualisiert. " \
                              "Dein Charakter ist jetzt auf dem neuesten Stand. " \
                              "Ausnahmen: Waffen werden nicht automatisch angepasst und behalten ihren (eventuell alten) Stand, ebenso alles was in der Nutzer-Datenbank geändert wurde.")
            if len(strArr) > 1:
                messageBox.setInformativeText("\n".join(strArr))
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec_()

    def xmlLesen(self,filename):
        '''Läd ein Charakter-Objekt aus einer XML Datei, deren Dateiname 
        inklusive Pfad als Argument übergeben wird'''
        #Alles bisherige löschen
        Wolke.Fehlercode = -41
        self.__init__()
        Wolke.Fehlercode = -42
        root = etree.parse(filename).getroot()
        #Erster Block
        Wolke.Fehlercode = -43

        versionXml = root.find('Version')
        charDBVersion = 0
        userDBChanged = False
        userDBName = "Unbekannt"
        if versionXml is not None:
            logging.debug("Character: VersionXML found")
            charDBVersion = int(versionXml.find('DatenbankVersion').text)
            userDBCRC = int(versionXml.find('NutzerDatenbankCRC').text)
            userDBName = versionXml.find('NutzerDatenbankName').text or 'Keine Nutzer-Regelbasis'
            if Wolke.DB.userDbXml is not None:
                currentUserDBCRC = binascii.crc32(etree.tostring(Wolke.DB.userDbXml))
                if userDBCRC != 0 and userDBCRC != currentUserDBCRC:
                    userDBChanged = True
            elif userDBCRC != 0:
                userDBChanged = True

        logging.debug("Starting Character Migration")
        self.charakterMigrieren(root, charDBVersion, self.datenbankCodeVersion)

        #Plugins
        root = EventBus.applyFilter("charakter_xml_laden", root)

        alg = root.find('AllgemeineInfos')
        self.name = alg.find('name').text or ''
        self.rasse = alg.find('rasse').text or ''
        self.status = int(alg.find('status').text)
        self.kurzbeschreibung = alg.find('kurzbeschreibung').text or ''
        self.schips = int(alg.find('schips').text)
        self.finanzen = int(alg.find('finanzen').text)
        tmp = alg.find('heimat')
        if not tmp is None: 
            self.heimat = tmp.text
        for eig in alg.findall('eigenheiten/*'):
            self.eigenheiten.append(eig.text or "")
        #Zweiter Block
        Wolke.Fehlercode = -44
        for atr in root.findall('Attribute/*'):
            self.attribute[atr.tag].wert = int(atr.text)
            self.attribute[atr.tag].aktualisieren()
        for ene in root.findall('Energien/AsP'):
            self.asp.wert = int(ene.attrib['wert'])
        for ene in root.findall('Energien/KaP'):
            self.kap.wert = int(ene.attrib['wert'])
        #Dritter Block

        vIgnored = []
        tIgnored = set()
        fIgnored = []
        übIgnored = []

        Wolke.Fehlercode = -45
        for vor in root.findall('Vorteile'):
            if "minderpakt" in vor.attrib:
                self.minderpakt = vor.get('minderpakt')
            else:
                self.minderpakt = None

        def parseVariableKosten(variable):
            var = list(map(str.strip, variable.split(",", 1)))
            if int(var[0]) != -1:
                vk = VariableKosten()
                vk.kosten = int(var[0])
                if len(var) > 1:
                    vk.kommentar = var[1]
                return vk
            return None

        for vor in root.findall('Vorteile/*'):
            if not vor.text in Wolke.DB.vorteile:
                vIgnored.append(vor.text)
                continue
            self.vorteile.append(vor.text)
            var = parseVariableKosten(vor.get('variable'))
            if var:
                if not Wolke.DB.vorteile[vor.text].variableKosten:
                    var.kosten = Wolke.DB.vorteile[vor.text].kosten
                self.vorteileVariable[vor.text] = var

        #Vierter Block
        Wolke.Fehlercode = -46
        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            nam = fer.attrib['name']
            if not nam in Wolke.DB.fertigkeiten:
                fIgnored.append(nam)
                continue

            fert = Wolke.DB.fertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            for tal in fer.findall('Talente/Talent'):
                nam = tal.attrib['name']
                if not nam in Wolke.DB.talente:
                    tIgnored.add(nam)
                    continue
                fert.gekaufteTalente.append(nam)
                var = parseVariableKosten(tal.attrib['variable'])
                if var:
                    #round down to nearest multiple in case of a db cost change
                    if Wolke.DB.talente[nam].variableKosten:
                        defaultKosten = self.getDefaultTalentCost(nam, fert.steigerungsfaktor)
                        var.kosten = max(var.kosten - (var.kosten%defaultKosten), defaultKosten)
                    else:
                        var.kosten = self.getDefaultTalentCost(nam, fert.steigerungsfaktor)
                    self.talenteVariable[nam] = var
            fert.aktualisieren()
            self.fertigkeiten.update({fert.name: fert})
        Wolke.Fehlercode = -47
        for fer in root.findall('Fertigkeiten/Freie-Fertigkeit'):
            fert = Fertigkeiten.FreieFertigkeit()            
            fert.name = fer.attrib['name']
            fert.wert = int(fer.attrib['wert'])
            self.freieFertigkeiten.append(fert)
        #Fünfter Block
        Wolke.Fehlercode = -48

        objekte = root.find('Objekte');
        zonenSystem = objekte.find('Zonensystem')
        if zonenSystem != None:
            self.zonenSystemNutzen = zonenSystem.text == "True"

        for rüs in objekte.findall('Rüstungen/Rüstung'):
            rüst = Objekte.Ruestung()
            rüst.name = rüs.attrib['name']
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = Hilfsmethoden.RsStr2Array(rüs.attrib['rs'])
            self.rüstung.append(rüst)
        Wolke.Fehlercode = -49
        for waf in objekte.findall('Waffen/Waffe'):
            if waf.attrib['typ'] == 'Nah':
                waff = Objekte.Nahkampfwaffe()
            else:
                waff = Objekte.Fernkampfwaffe()
                waff.lz = int(waf.attrib['lz'])
            waff.wm = int(waf.get('wm') or 0)
            waff.anzeigename = waf.attrib['name']
            waff.name = waf.get('id') or waff.anzeigename
            waff.rw = int(waf.attrib['rw'])
            waff.W6 = int(waf.attrib['W6'])
            waff.plus = int(waf.attrib['plus'])
            if waf.attrib['eigenschaften']:
                waff.eigenschaften = list(map(str.strip, waf.attrib['eigenschaften'].split(",")))
            waff.haerte = int(waf.attrib['haerte'])
            waff.kampfstil = waf.attrib['kampfstil']
            if waff.name in Wolke.DB.waffen:
                dbWaffe = Wolke.DB.waffen[waff.name]
                waff.fertigkeit = dbWaffe.fertigkeit
                waff.talent = dbWaffe.talent
                waff.kampfstile = dbWaffe.kampfstile.copy()

            self.waffen.append(waff)
        Wolke.Fehlercode = -50
        for aus in objekte.findall('Ausrüstung/Ausrüstungsstück'):
            self.ausrüstung.append(aus.text or "")
        #Sechster Block 
        Wolke.Fehlercode = -51
        for fer in root.findall('Übernatürliche-Fertigkeiten/Übernatürliche-Fertigkeit'):
            nam = fer.attrib['name']
            if not nam in Wolke.DB.übernatürlicheFertigkeiten:
                übIgnored.append(nam)
                continue

            fert = Wolke.DB.übernatürlicheFertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            if 'addToPDF' in fer.attrib:
                fert.addToPDF = fer.attrib['addToPDF'] == "True"
            for tal in fer.findall('Talente/Talent'):
                nam = tal.attrib['name']
                if not nam in Wolke.DB.talente:
                    tIgnored.add(nam)
                    continue
                fert.gekaufteTalente.append(nam)
                var = parseVariableKosten(tal.attrib['variable'])
                if var:
                    #round down to nearest multiple in case of a db cost change
                    defaultKosten = self.getDefaultTalentCost(nam, fert.steigerungsfaktor)
                    var.kosten = max(var.kosten - (var.kosten%defaultKosten), defaultKosten)
                    self.talenteVariable[nam] = var
            fert.aktualisieren()
            self.übernatürlicheFertigkeiten.update({fert.name: fert})
        #Siebter Block
        Wolke.Fehlercode = -52
        self.EPtotal = int(root.find('Erfahrung/EPtotal').text)
        self.EPspent = int(root.find('Erfahrung/EPspent').text)   

        #Achter Block
        notiz = root.find('Notiz')
        if notiz is not None:
            self.notiz = notiz.text
        
        if userDBChanged or vIgnored or fIgnored or tIgnored or übIgnored:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle("Charakter laden - Nutzer-Datenbank wurde geändert.")

            strArr = ["Seit du diesen Charakter das letzte mal bearbeitet hast wurde die Nutzer-Datenbank aktualisiert. "]
            if not userDBName == Wolke.DB.datei:
                strArr.append("Auch der Pfad der aktuell geladenen Nutzer-Datenbank ist ein anderer:\n- Vorher: '")
                strArr.append(userDBName)
                strArr.append("'\n- Jetzt: '")
                strArr.append(Wolke.DB.datei or "Keine Datenbank")
                strArr.append("'")

            strArr.append("\n\nEventuell hat der Charakter Vorteile/Fertigkeiten/Talente verloren und sein EP-Stand könnte sich verändert haben! ")
            strArr.append("Neu zur Datenbank hinzugefügte Dinge sind unproblematisch. Waffen werden nicht automatisch angepasst und behalten ihren (eventuell alten) Stand. ")
            strArr.append("Dein Charakter ist jetzt an die aktuelle Nutzer-Datenbank angepasst, überspeichere den Charakter nur wenn du dir sicher bist.")
            text = "".join(strArr)
            logging.warning(text)
            messageBox.setText(text)

            strArr = ["Weitere Informationen:"]

            if vIgnored or fIgnored or tIgnored or übIgnored:
                strArr.append("\nDas Folgende war charakterrelevant und wurde aus der Regelbasis gelöscht:")
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
            else:
                strArr.append("\nEs wurde nichts charakterrelevantes gelöscht.")

            text = "".join(strArr)
            logging.warning(text)
            messageBox.setInformativeText(text + "\n\nDu kannst diese Nachricht sephrasto.log nochmal nachlesen.")
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec_()

        Wolke.Fehlercode = 0