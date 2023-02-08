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
from PySide6 import QtWidgets, QtCore
import os.path
from Fertigkeiten import KampffertigkeitTyp
import base64
from Migrationen import Migrationen

class KampfstilMod():
    def __init__(self):
        self.at = 0
        self.vt = 0
        self.plus = 0
        self.rw = 0
        self.be = 0

class Waffenwerte():
    def __init__(self):
        self.at = 0
        self.vt = 0
        self.rw = 0
        self.würfel = 0
        self.plus = 0
        self.härte = 0
        self.kampfstil = ""

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
        heimaten = Wolke.DB.findHeimaten()
        if "Mittelreich" in heimaten:
            self.heimat = "Mittelreich"
        else:
            self.heimat = heimaten[0] if len(heimaten) > 0 else ""
        self.schipsMax = 4
        self.schips = 4

        self.finanzen = 2;
        self.eigenheiten = []

        #Zweiter Block: Attribute und Abgeleitetes
        self.attribute = {}
        for key in Definitionen.Attribute.keys():
            self.attribute[key] = Fertigkeiten.Attribut(key)
            self.attribute[key].steigerungsfaktor = Wolke.DB.einstellungen["Attribute: Steigerungsfaktor"].toInt()
        self.wsBasis = -1
        self.ws = -1
        self.wsStern = -1
        self.mrBasis = -1
        self.mr = -1
        self.gsBasis = -1
        self.gs = -1
        self.gsStern = -1
        self.dhBasis = -1
        self.dh = -1
        self.dhStern = -1
        self.schadensbonusBasis = -1
        self.schadensbonus = -1
        self.iniBasis = -1
        self.ini = -1
        self.asp = Fertigkeiten.Energie()
        self.asp.steigerungsfaktor = Wolke.DB.einstellungen["Energien: Steigerungsfaktor"].toInt()
        self.aspBasis = 0
        self.aspMod = 0
        self.kap = Fertigkeiten.Energie()
        self.kap.steigerungsfaktor = Wolke.DB.einstellungen["Energien: Steigerungsfaktor"].toInt()
        self.kapBasis = 0
        self.kapMod = 0
        
        #Dritter Block: Vorteile, gespeichert als String
        self.vorteile = [] #Important: use addVorteil and addRemove functions for modification
        self.vorteileVariableKosten = {}
        self.vorteileKommentare = {}
        self.minderpakt = None
        self.kampfstilMods = {}

        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.fertigkeiten = copy.deepcopy(Wolke.DB.fertigkeiten)
        self.freieFertigkeiten = []
        self.freieFertigkeitenNumKostenlos = Wolke.DB.einstellungen["FreieFertigkeiten: Anzahl Kostenlos"].toInt()
        self.freieFertigkeitKosten = [Wolke.DB.einstellungen["FreieFertigkeiten: Kosten Stufe1"].toInt(), 
                                      Wolke.DB.einstellungen["FreieFertigkeiten: Kosten Stufe2"].toInt(), 
                                      Wolke.DB.einstellungen["FreieFertigkeiten: Kosten Stufe3"].toInt()]
        self.freieFertigkeitKosten[1] += self.freieFertigkeitKosten[0]
        self.freieFertigkeitKosten[2] += self.freieFertigkeitKosten[1]
        self.talenteVariableKosten = {}
        self.talenteKommentare = {}

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
        self.epGesamt = 0
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
        self.hausregeln = Wolke.Settings["Datenbank"]
        self.finanzenAnzeigen = True
        self.ueberPDFAnzeigen = False
        self.regelnAnhaengen = Wolke.Settings["Cheatsheet"]
        self.regelnGroesse = Wolke.Settings["Cheatsheet-Fontsize"]
        self.regelnKategorien = Wolke.DB.einstellungen["Regelanhang: Reihenfolge"].toTextList()
        self.formularEditierbarkeit = Wolke.Settings["Formular-Editierbarkeit"]

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
        self.aussehen1 = ""
        self.aussehen2 = ""
        self.aussehen3 = ""
        self.aussehen4 = ""
        self.aussehen5 = ""
        self.aussehen6 = ""
        self.hintergrund0 = ""
        self.hintergrund1 = ""
        self.hintergrund2 = ""
        self.hintergrund3 = ""
        self.hintergrund4 = ""
        self.hintergrund5 = ""
        self.hintergrund6 = ""
        self.hintergrund7 = ""
        self.hintergrund8 = ""
        self.bild = None

        #Bei Änderungen nicht vergessen die script docs in ScriptAPI.md anzupassen
        self.charakterScriptAPI = {
            #Hintergrund
            'getName' : lambda: self.name, 
            'getSpezies' : lambda: self.spezies, 
            'getStatus' : lambda: self.status, 
            'getKurzbeschreibung' : lambda: self.kurzbeschreibung, 
            'getHeimat' : lambda: self.heimat, 
            'getFinanzen' : lambda: self.finanzen, 
            'getEigenheiten' : lambda: copy.deepcopy(self.eigenheiten), 
            'getEPGesamt' : lambda: self.epGesamt, 
            'getEPAusgegeben' : lambda: self.epAusgegeben, 

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

            #MR
            'getMRBasis' : lambda: self.mrBasis, 
            'getMR' : lambda: self.mr, 
            'setMR' : lambda mr: setattr(self, 'mr', mr), 
            'modifyMR' : lambda mr: setattr(self, 'mr', self.mr + mr), 

            #GS
            'getGSBasis' : lambda: self.gsBasis, 
            'getGS' : lambda: self.gs, 
            'setGS' : lambda gs: setattr(self, 'gs', gs), 
            'modifyGS' : lambda gs: setattr(self, 'gs', self.gs + gs), 

            #DH
            'getDHBasis' : lambda: self.dhBasis, 
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
            'modifyWaffeAT' : lambda atmod: setattr(self.currentWaffenwerte, 'at', self.currentWaffenwerte.at + atmod), 
            'modifyWaffeVT' : lambda vtmod: setattr(self.currentWaffenwerte, 'vt', self.currentWaffenwerte.vt + vtmod), 
            'modifyWaffeTPWürfel' : lambda würfelmod: setattr(self.currentWaffenwerte, 'würfel', self.currentWaffenwerte.würfel + würfelmod), 
            'modifyWaffeTPPlus' : lambda plusmod: setattr(self.currentWaffenwerte, 'plus', self.currentWaffenwerte.plus + plusmod), 
            'modifyWaffeHärte' : lambda härtemod: setattr(self.currentWaffenwerte, 'härte', self.currentWaffenwerte.härte + härtemod), 
            'modifyWaffeRW' : lambda rwmod: setattr(self.currentWaffenwerte, 'rw', self.currentWaffenwerte.rw + rwmod), 
            'setWaffeAT' : lambda at: setattr(self.currentWaffenwerte, 'at', at), 
            'setWaffeVT' : lambda vt: setattr(self.currentWaffenwerte, 'vt', vt), 
            'setWaffeTPWürfel' : lambda würfel: setattr(self.currentWaffenwerte, 'würfel', würfel), 
            'setWaffeTPPlus' : lambda plus: setattr(self.currentWaffenwerte, 'plus', plus), 
            'setWaffeHärte' : lambda härte: setattr(self.currentWaffenwerte, 'härte', härte), 
            'setWaffeRW' : lambda rw: setattr(self.currentWaffenwerte, 'rw', rw), 
            'getWaffenWerte' : lambda: copy.deepcopy(self.currentWaffenwerte), 
        }


        filter = ['setSchadensbonus', 'modifySchadensbonus', 
                  'setBEMod', 'modifyBEMod', 'modifyFertigkeitBasiswert', 
                  'setRSMod', 'modifyRSMod',
                  'setKampfstil', 'modifyKampfstil', 
                  'addWaffeneigenschaft', 'removeWaffeneigenschaft']
        for k, v in self.charakterScriptAPI.items():
            if k in self.waffenScriptAPI:
                assert False, "Duplicate entry"

            if k in filter:
                continue

            self.waffenScriptAPI[k] = v

        EventBus.doAction("charakter_instanziiert", { "charakter" : self })

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
        match = re.search(r"\((.+?)\)", self.currentEigenschaft, re.UNICODE)
        if not match:
            raise Exception("Die Waffeneigenschaft '" + self.currentEigenschaft + "' erfordert einen Parameter, beispielsweise Schwer (4), aber es wurde keiner gefunden.")
        parameters = list(map(str.strip, match.group(1).split(";")))
        if not len(parameters) >= paramNb:
            raise Exception("Die Waffeneigenschaft '" + self.currentEigenschaft + "' erfordert " + paramNb + " Parameter, aber es wurde(n) nur " + len(parameters) + " gefunden. Parameter müssen mit Semikolon getrennt werden")
        return parameters[paramNb-1]

    def addVorteil(self, vorteil):
        if not vorteil or vorteil in self.vorteile:
            return
        self.vorteile.append(vorteil)
        EventBus.doAction("vorteil_gekauft", { "charakter" : self, "name" : vorteil })

    def removeVorteil(self, vorteil):
        if not vorteil in self.vorteile:
            return
        self.vorteile.remove(vorteil)
        EventBus.doAction("vorteil_entfernt", { "charakter" : self, "name" : vorteil })

    def aktualisieren(self):
        EventBus.doAction("pre_charakter_aktualisieren", { "charakter" : self })

        '''Berechnet alle abgeleiteten Werte neu'''
        for key in Definitionen.Attribute:
            self.attribute[key].aktualisieren()

        self.updateVorts()

        scriptAPI = { 'getAttribut' : lambda attribut: self.attribute[attribut].wert }
        self.aspBasis = eval(Wolke.DB.einstellungen["Basis AsP Script"].toText(), scriptAPI)
        self.aspMod = 0

        self.kapBasis = eval(Wolke.DB.einstellungen["Basis KaP Script"].toText(), scriptAPI)
        self.kapMod = 0

        self.wsBasis = eval(Wolke.DB.einstellungen["Basis WS Script"].toText(), scriptAPI)
        self.ws = self.wsBasis

        self.mrBasis = eval(Wolke.DB.einstellungen["Basis MR Script"].toText(), scriptAPI)
        self.mr = self.mrBasis

        self.gsBasis = eval(Wolke.DB.einstellungen["Basis GS Script"].toText(), scriptAPI)
        self.gs = self.gsBasis

        self.iniBasis = eval(Wolke.DB.einstellungen["Basis INI Script"].toText(), scriptAPI)
        self.ini = self.iniBasis     
        
        self.dhBasis = eval(Wolke.DB.einstellungen["Basis DH Script"].toText(), scriptAPI)
        self.dh = self.dhBasis

        self.schadensbonusBasis = eval(Wolke.DB.einstellungen["Basis Schadensbonus Script"].toText(), scriptAPI)
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

        # Undo previous changes by Vorteil scripts before executing them again
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

        # Execute Vorteil scripts to modify character stats
        EventBus.doAction("charakter_aktualisieren_vorteilscripts", { "charakter" : self })
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

        # Update BE, Fertigkeiten and Waffenwerte afterwards because they might be modified by Vorteil scripts
        EventBus.doAction("charakter_aktualisieren_fertigkeiten", { "charakter" : self })
        self.updateFertigkeiten(self.fertigkeiten, Wolke.DB.fertigkeiten)
        self.updateFertigkeiten(self.übernatürlicheFertigkeiten, Wolke.DB.übernatürlicheFertigkeiten)
        
        self.be = max(0, self.be-self.rüstungsgewöhnung)
        self.wsStern = self.rsmod + self.ws
        if len(self.rüstung) > 0:
            self.wsStern += self.rüstung[0].getRSGesamtInt()

        scriptAPI = { "getBE" : lambda: self.be, "getDH" : lambda: self.dh }
        self.dhStern = eval(Wolke.DB.einstellungen["DH* Script"].toText(), scriptAPI)

        scriptAPI = { "getBE" : lambda: self.be, "getGS" : lambda: self.gs }
        self.gsStern = eval(Wolke.DB.einstellungen["GS* Script"].toText(), scriptAPI)

        self.schips = self.schipsMax
        if self.finanzen >= 2: 
            self.schips += self.finanzen - 2
        else:
            self.schips -= (2-self.finanzen)*2

        # Update weapon stats last because they might depend on everything else but do not change other things
        EventBus.doAction("charakter_aktualisieren_waffenwerte", { "charakter" : self })
        self.updateWaffenwerte()

        EventBus.doAction("post_charakter_aktualisieren", { "charakter" : self })
        self.epZaehlen()


    def updateWaffenwerte(self):
        self.waffenwerte = []

        error = []
        for el in self.waffen:
            waffenwerte = Waffenwerte()
            self.waffenwerte.append(waffenwerte)
            waffenwerte.kampfstil = el.kampfstil
            waffenwerte.härte = el.härte
            if el.name in Wolke.DB.einstellungen["Waffen: Härte WSStern"].toTextList():
                waffenwerte.härte = self.wsStern
            waffenwerte.würfel = el.würfel

            if not el.fertigkeit in self.fertigkeiten:
                continue

            if el.talent in self.fertigkeiten[el.fertigkeit].gekaufteTalente:
                pw = self.fertigkeiten[el.fertigkeit].probenwertTalent
            else:
                pw = self.fertigkeiten[el.fertigkeit].probenwert
                
            kampfstilMods = None
            if el.kampfstil in self.kampfstilMods:
                kampfstilMods = self.kampfstilMods[el.kampfstil]
            else:
                kampfstilMods = KampfstilMod()
                if el.kampfstil != Definitionen.KeinKampfstil:
                    logging.warn("Waffe " + el.name + " referenziert einen nicht existierenden Kampfstil: " + el.kampfstil)

            # Execute script to calculate weapon stats
            scriptAPI = {
                'getAttribut' : lambda attribut: self.attribute[attribut].wert,
                'getWaffe' : lambda: copy.deepcopy(el),
                'getPW' : lambda: pw,
                'getKampfstil' : lambda: copy.deepcopy(kampfstilMods),
                'getSB' : lambda: self.schadensbonus,
                'getBE' : lambda: self.be,
                'setWaffenwerte' : lambda at, vt, plus, rw: setattr(waffenwerte, 'at', at) or setattr(waffenwerte, 'vt', vt) or setattr(waffenwerte, 'plus', plus) or setattr(waffenwerte, 'rw', rw)
            }
            try:
                # Execute global script
                exec(Wolke.DB.einstellungen["Waffen: Waffenwerte Script"].toText(), scriptAPI)

                #Execute Waffeneigenschaft scripts
                self.currentWaffenwerte = waffenwerte
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

                self.currentWaffenwerte = None
                self.currentEigenschaft = None
            except Exception as e:
                error.append(el.name + ": " + str(e))

        if len(error) > 0:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle("Waffenwerte konnten nicht aktualisiert werden")
            messageBox.setText("\n\n".join(error))
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec()

    def getDefaultTalentCost(self, talent, steigerungsfaktor):
        cost = 0
        if Wolke.DB.talente[talent].kosten != -1:
            cost = Wolke.DB.talente[talent].kosten
        elif Wolke.DB.talente[talent].verbilligt:
            cost = Wolke.DB.einstellungen["Talente: SteigerungsfaktorMulti Verbilligt"].toInt()*steigerungsfaktor
        else:
            cost = Wolke.DB.einstellungen["Talente: SteigerungsfaktorMulti"].toInt()*steigerungsfaktor

        cost = EventBus.applyFilter("talent_kosten", cost, { "charakter" : self, "talent": talent })
        return cost

    def getTalentCost(self, talent, steigerungsfaktor):
        if talent in self.talenteVariableKosten:
            return self.talenteVariableKosten[talent]
        return self.getDefaultTalentCost(talent, steigerungsfaktor)

    def epZaehlen(self):
        '''Berechnet die bisher ausgegebenen EP'''
        spent = 0
        #Erster Block ist gratis
        #Zweiter Block: Attribute und Abgeleitetes
        for key in Definitionen.Attribute:
            val = sum(range(self.attribute[key].wert+1)) * self.attribute[key].steigerungsfaktor
            spent += EventBus.applyFilter("attribut_kosten", val, { "charakter" : self, "attribut" : key, "wert" : self.attribute[key].wert })

        val = sum(range(self.asp.wert+1))*self.asp.steigerungsfaktor
        spent += EventBus.applyFilter("asp_kosten", val, { "charakter" : self, "wert" : self.asp.wert })
        val = sum(range(self.kap.wert+1))*self.kap.steigerungsfaktor   
        spent += EventBus.applyFilter("kap_kosten", val, { "charakter" : self, "wert" : self.kap.wert })

        self.epAttribute = spent
        #Dritter Block: Vorteile
        for vor in self.vorteile:
            if vor == self.minderpakt:
                if "Minderpakt" in self.vorteile:
                    spent += 20
                    continue
                else:
                    self.minderpakt = None
            if vor in self.vorteileVariableKosten:
                spent += self.vorteileVariableKosten[vor]
            elif Wolke.DB.vorteile[vor].kosten != -1:
                spent += Wolke.DB.vorteile[vor].kosten
        
        self.epVorteile = spent - self.epAttribute
        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.epFertigkeiten = 0
        self.epFertigkeitenTalente = 0
        self.epFreieFertigkeiten = 0
        paidTalents = []
        for fer in self.fertigkeiten:
            val = sum(range(self.fertigkeiten[fer].wert+1)) * self.fertigkeiten[fer].steigerungsfaktor
            spent += val
            self.epFertigkeiten += val
            for tal in self.fertigkeiten[fer].gekaufteTalente:
                if tal in paidTalents:
                    continue
                if fer == "Gebräuche" and tal[11:] == self.heimat:
                    continue
                paidTalents.append(tal)
                val = self.getTalentCost(tal, self.fertigkeiten[fer].steigerungsfaktor)
                spent += val
                self.epFertigkeitenTalente += val

        numKostenlos = 0
        for fer in self.freieFertigkeiten:
            # Dont count Muttersprache
            if fer.wert == 3 and numKostenlos < self.freieFertigkeitenNumKostenlos:
                numKostenlos += 1
                continue
            if not fer.name:
                continue
            val = EventBus.applyFilter("freiefertigkeit_kosten", self.freieFertigkeitKosten[fer.wert-1], { "charakter" : self, "name" : fer.name, "wert" : fer.wert })
            spent += val
            self.epFreieFertigkeiten += val
        #Fünfter Block ist gratis
        #Sechster Block: Übernatürliches
        self.epÜbernatürlich = 0
        self.epÜbernatürlichTalente = 0
        for fer in self.übernatürlicheFertigkeiten:
            val = sum(range(self.übernatürlicheFertigkeiten[fer].wert+1)) * self.übernatürlicheFertigkeiten[fer].steigerungsfaktor
            spent += val
            self.epÜbernatürlich += val
            for tal in self.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                if tal in paidTalents:
                    continue
                paidTalents.append(tal)
                val = self.getTalentCost(tal, self.übernatürlicheFertigkeiten[fer].steigerungsfaktor)
                spent += val
                self.epÜbernatürlichTalente += val
        #Siebter Block ist gratis
        #Achter Block: Fix für höchste Kampffertigkeit
        höchsteKampffert = self.getHöchsteKampffertigkeit()
        if höchsteKampffert is not None:
            val = max(0, 2*sum(range(höchsteKampffert.wert+1)))
            spent += val
            self.epFertigkeiten += val
        #Store
        self.epAusgegeben = spent

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
                if not self.voraussetzungenPrüfen(Wolke.DB.vorteile[vor].voraussetzungen):
                    remove.append(vor)
                    contFlag = False
            for el in remove:
                self.removeVorteil(el)
            if contFlag:
                break

    def findUnerfüllteVorteilVoraussetzungen(self, vorteile = None, waffen = None, attribute = None, übernatürlicheFertigkeiten = None, fertigkeiten = None):
        ''' 
        Checks for all Vorteile if the requirements are still met until in one 
        run, all of them meet the requirements. This gets rid of stacks of them
        that all depend onto each other, like Zauberer I-IV when removing I.
        The parameters can be used to override character values. If None is specified, the character values are used.
        '''
        if not self.voraussetzungenPruefen:
            return []

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
                if not Hilfsmethoden.voraussetzungenPrüfen(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, Wolke.DB.vorteile[vor].voraussetzungen):
                    remove.append(vor)
                    allRemoved.append(vor)
                    contFlag = False
            for el in remove:
                vorteile.remove(el)
            if contFlag:
                break

        return allRemoved

    def getHöchsteKampffertigkeit(self):
        höchste = None
        for fert in self.fertigkeiten.values():
            if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf and (höchste is None or fert.wert > höchste.wert):
                höchste = fert
        return höchste

    def updateFertigkeiten(self, fertigkeiten, alleFertigkeiten):
        '''
        Similar to updateVorts, this removes all Fertigkeiten for which the
        requirements are no longer met until all are removed. Furthermore, all
        Fertigkeiten are updated, which recalculates the PW and such.
        Then, all Fertigkeiten are checked against their maximum value from the 
        attributes and if neccessary, reduced to that value. 
        Last, all Talente are iterated through, their requirements are checked, 
        and it is made sure that they appear at all Fertigkeiten where they are
        available. 
        '''
        while True:
            remove = []
            contFlag = True
            for fert in fertigkeiten:
                if not self.voraussetzungenPrüfen(fertigkeiten[fert].voraussetzungen):
                    remove.append(fert)
                    contFlag = False
                fertigkeiten[fert].aktualisieren(self.attribute)
            for el in remove:
                fertigkeiten.pop(el, None)
            if contFlag:
                break

        # Add missing Fertigkeiten
        for name, fert in alleFertigkeiten.items():
            if name in fertigkeiten:
                continue
            if self.voraussetzungenPrüfen(fert.voraussetzungen):
                fertigkeiten.update({name : fert.__deepcopy__()})

        # Update fertigkeiten and add keep talente with multiple fertigkeiten consistent
        talente = set()
        for fert in fertigkeiten.values():
            fert.aktualisieren(self.attribute)

            if fert.wert > fert.maxWert:
                fert.wert = fert.maxWert
                fert.aktualisieren(self.attribute)

            for tal in fert.gekaufteTalente:
                talente.add(tal)

        for tal in talente:
            remove = not self.voraussetzungenPrüfen(Wolke.DB.talente[tal].voraussetzungen)
            for fName in Wolke.DB.talente[tal].fertigkeiten:
                if not fName in fertigkeiten:
                    continue
                fert = fertigkeiten[fName]
                if remove:
                    if tal in fert.gekaufteTalente:
                        fertigkeiten[fName].gekaufteTalente.remove(tal) 
                elif tal not in fert.gekaufteTalente:
                    fertigkeiten[fName].gekaufteTalente.append(tal)

    def voraussetzungenPrüfen(self, voraussetzungen):
        if not self.voraussetzungenPruefen:
            return True

        return Hilfsmethoden.voraussetzungenPrüfen(self.vorteile, self.waffen, self.attribute, self.übernatürlicheFertigkeiten, self.fertigkeiten, voraussetzungen)
    
    def xmlSchreiben(self, filename):
        '''Speichert dieses Charakter-Objekt in einer XML Datei, deren 
        Dateiname inklusive Pfad als Argument übergeben wird'''
        #Document Root
        root = etree.Element('Charakter')

        versionXml = etree.SubElement(root, 'Version')
        etree.SubElement(versionXml, 'CharakterVersion').text = str(Migrationen.charakterCodeVersion)
        etree.SubElement(versionXml, 'NutzerDatenbankCRC').text = str(binascii.crc32(etree.tostring(Wolke.DB.userDbXml))) if Wolke.DB.userDbXml is not None else "0"
        etree.SubElement(versionXml, 'NutzerDatenbankName').text = os.path.basename(Wolke.DB.datei) if Wolke.DB.datei else ""
        etree.SubElement(versionXml, 'Plugins').text = ", ".join(self.enabledPlugins)

        #Erster Block
        sub =  etree.SubElement(root, 'Beschreibung')
        etree.SubElement(sub, 'Name').text = self.name
        etree.SubElement(sub, 'Spezies').text = self.spezies
        etree.SubElement(sub, 'Status').text = str(self.status)
        etree.SubElement(sub, 'Kurzbeschreibung').text = self.kurzbeschreibung
        etree.SubElement(sub, 'SchiP').text = str(self.schips)
        etree.SubElement(sub, 'Finanzen').text = str(self.finanzen)
        etree.SubElement(sub, 'Heimat').text = self.heimat
        eigs = etree.SubElement(sub, 'Eigenheiten')
        for eigenh in self.eigenheiten:
            etree.SubElement(eigs, 'Eigenheit').text = eigenh
        #Zweiter Block - abgeleitete nicht notwendig da automatisch neu berechnet
        atr = etree.SubElement(root, 'Attribute')
        for attr in self.attribute:
            etree.SubElement(atr, attr).text = str(self.attribute[attr].wert)
        en = etree.SubElement(root, 'Energien')
        etree.SubElement(en, 'AsP').set('wert', str(self.asp.wert))
        etree.SubElement(en, 'KaP').set('wert', str(self.kap.wert))
        #Dritter Block    
        vor = etree.SubElement(root, 'Vorteile')
        if self.minderpakt is not None:
            vor.set('minderpakt', self.minderpakt)
        else:
            vor.set('minderpakt', '')
        for vort in self.vorteile:
            v = etree.SubElement(vor, 'Vorteil')
            v.text = vort
            if vort in self.vorteileVariableKosten:
                v.set('variableKosten', str(self.vorteileVariableKosten[vort]))
            if vort in self.vorteileKommentare:
                v.set('kommentar', self.vorteileKommentare[vort])

        #Vierter Block
        fer = etree.SubElement(root, 'Fertigkeiten')
        for fert in self.fertigkeiten:
            fertNode = etree.SubElement(fer, 'Fertigkeit')
            fertNode.set('name', self.fertigkeiten[fert].name)
            fertNode.set('wert', str(self.fertigkeiten[fert].wert))
            talentNode = etree.SubElement(fertNode, 'Talente')
            for talent in self.fertigkeiten[fert].gekaufteTalente:
                talNode = etree.SubElement(talentNode, 'Talent')
                talNode.set('name', talent)
                if talent in self.talenteVariableKosten:
                    talNode.set('variableKosten', str(self.talenteVariableKosten[talent]))
                if talent in self.talenteKommentare:
                    talNode.set('kommentar', self.talenteKommentare[talent])

        for fert in self.freieFertigkeiten:
            freiNode = etree.SubElement(fer, 'FreieFertigkeit')
            freiNode.set('name', fert.name)
            freiNode.set('wert', str(fert.wert))
        #Fünfter Block
        aus = etree.SubElement(root, 'Objekte')

        zonenSystem = etree.SubElement(aus, 'Zonensystem')
        zonenSystem.text = "1" if self.zonenSystemNutzen else "0"

        rüs = etree.SubElement(aus, 'Rüstungen')
        for rüst in self.rüstung:
            rüsNode = etree.SubElement(rüs, 'Rüstung')
            rüsNode.set('name', rüst.name)
            rüsNode.set('be', str(rüst.be))
            rüsNode.set('rs', Hilfsmethoden.RsArray2Str(rüst.rs))

        waf = etree.SubElement(aus, 'Waffen')
        for waff in self.waffen:
            wafNode = etree.SubElement(waf, 'Waffe')
            wafNode.set('name', waff.anzeigename)
            wafNode.set('id', waff.name)
            wafNode.set('würfel', str(waff.würfel))
            wafNode.set('würfelSeiten', str(waff.würfelSeiten))
            wafNode.set('plus', str(waff.plus))
            wafNode.set('eigenschaften', ", ".join(waff.eigenschaften))
            wafNode.set('härte', str(waff.härte))
            wafNode.set('rw', str(waff.rw))
            wafNode.set('kampfstil', waff.kampfstil)
            wafNode.set('wm', str(waff.wm))
            if type(waff) is Objekte.Nahkampfwaffe:
                wafNode.set('typ', 'Nah')
            elif type(waff) is Objekte.Fernkampfwaffe:
                wafNode.set('typ', 'Fern')
                wafNode.set('lz', str(waff.lz))

        ausrüst = etree.SubElement(aus, 'Ausrüstung')
        for ausr in self.ausrüstung:
            etree.SubElement(ausrüst, 'Ausrüstungsstück').text = ausr
        #Sechster Block
        üfer = etree.SubElement(root, 'ÜbernatürlicheFertigkeiten')
        for fert in self.übernatürlicheFertigkeiten:
            fertNode = etree.SubElement(üfer, 'ÜbernatürlicheFertigkeit')
            fertNode.set('name', self.übernatürlicheFertigkeiten[fert].name)
            fertNode.set('wert', str(self.übernatürlicheFertigkeiten[fert].wert))
            fertNode.set('exportieren', "1" if self.übernatürlicheFertigkeiten[fert].addToPDF else "0")
            talentNode = etree.SubElement(fertNode, 'Talente')
            for talent in self.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                talNode = etree.SubElement(talentNode, 'Talent')
                talNode.set('name', talent)
                if talent in self.talenteVariableKosten:
                    talNode.set('variableKosten', str(self.talenteVariableKosten[talent]))
                if talent in self.talenteKommentare:
                    talNode.set('kommentar', self.talenteKommentare[talent])
        #Siebter Block
        epn = etree.SubElement(root, 'Erfahrung')
        etree.SubElement(epn, 'Gesamt').text = str(self.epGesamt)
        etree.SubElement(epn, 'Ausgegeben').text = str(self.epAusgegeben)
        
        #Achter Block
        notiz =  etree.SubElement(root, 'Notiz')
        notiz.text = self.notiz

        einstellungen = etree.SubElement(root, 'Einstellungen')
        etree.SubElement(einstellungen, 'VoraussetzungenPrüfen').text = "1" if self.voraussetzungenPruefen else "0"
        etree.SubElement(einstellungen, 'Charakterbogen').text = str(self.charakterbogen)
        etree.SubElement(einstellungen, 'FinanzenAnzeigen').text = "1" if self.finanzenAnzeigen else "0"
        etree.SubElement(einstellungen, 'ÜbernatürlichesPDFSpalteAnzeigen').text = "1" if self.ueberPDFAnzeigen else "0"
        etree.SubElement(einstellungen, 'RegelnAnhängen').text = "1" if self.regelnAnhaengen else "0"
        etree.SubElement(einstellungen, 'RegelnGrösse').text = str(self.regelnGroesse)
        etree.SubElement(einstellungen, 'RegelnKategorien').text = str(", ".join(self.regelnKategorien))
        etree.SubElement(einstellungen, 'FormularEditierbarkeit').text = str(self.formularEditierbarkeit)
        etree.SubElement(einstellungen, 'Hausregeln').text = str(self.hausregeln or "")

        #Neunter Block
        sub =  etree.SubElement(root, 'BeschreibungDetails')
        etree.SubElement(sub, 'Kultur').text = self.kultur
        etree.SubElement(sub, 'Profession').text = self.profession
        etree.SubElement(sub, 'Geschlecht').text = self.geschlecht
        etree.SubElement(sub, 'Geburtsdatum').text = self.geburtsdatum
        etree.SubElement(sub, 'Grösse').text = self.groesse
        etree.SubElement(sub, 'Gewicht').text = self.gewicht
        etree.SubElement(sub, 'Haarfarbe').text = self.haarfarbe
        etree.SubElement(sub, 'Augenfarbe').text = self.augenfarbe
        etree.SubElement(sub, 'Titel').text = self.titel
        etree.SubElement(sub, 'Aussehen1').text = self.aussehen1
        etree.SubElement(sub, 'Aussehen2').text = self.aussehen2
        etree.SubElement(sub, 'Aussehen3').text = self.aussehen3
        etree.SubElement(sub, 'Aussehen4').text = self.aussehen4
        etree.SubElement(sub, 'Aussehen5').text = self.aussehen5
        etree.SubElement(sub, 'Aussehen6').text = self.aussehen6
        etree.SubElement(sub, 'Hintergrund0').text = self.hintergrund0
        etree.SubElement(sub, 'Hintergrund1').text = self.hintergrund1
        etree.SubElement(sub, 'Hintergrund2').text = self.hintergrund2
        etree.SubElement(sub, 'Hintergrund3').text = self.hintergrund3
        etree.SubElement(sub, 'Hintergrund4').text = self.hintergrund4
        etree.SubElement(sub, 'Hintergrund5').text = self.hintergrund5
        etree.SubElement(sub, 'Hintergrund6').text = self.hintergrund6
        etree.SubElement(sub, 'Hintergrund7').text = self.hintergrund7
        etree.SubElement(sub, 'Hintergrund8').text = self.hintergrund8
        if self.bild:
            etree.SubElement(sub, 'Bild').text = base64.b64encode(self.bild)

        #Plugins
        root = EventBus.applyFilter("charakter_xml_schreiben", root, { "charakter" : self, "filepath" : filename })

        #Write XML to file
        doc = etree.ElementTree(root)
        with open(filename, 'wb') as file:
            file.seek(0)
            file.truncate()
            doc.write(file, encoding='UTF-8', pretty_print=True)
            file.truncate()

    @staticmethod
    def xmlHausregelnLesen(filename):
        root = etree.parse(filename).getroot()

        einstellungen = root.find('Einstellungen')
        if einstellungen is not None:
            return einstellungen.find('Hausregeln').text
        else:
            versionXml = root.find('Version')
            if versionXml is not None:
                userDBXml = versionXml.find('NutzerDatenbankName')
                if userDBXml is not None and userDBXml.text:
                    return os.path.basename(userDBXml.text)
        return None

    def xmlLesen(self, filename):
        '''Läd ein Charakter-Objekt aus einer XML Datei, deren Dateiname 
        inklusive Pfad als Argument übergeben wird'''
        #Alles bisherige löschen
        self.__init__()
        root = etree.parse(filename).getroot()
        #Erster Block
        versionXml = root.find('Version')
        charakterVersion = 0
        userDBChanged = False
        userDBName = "Unbekannt"
        if versionXml is not None:
            logging.debug("Character: VersionXML found")

            if versionXml.find('DatenbankVersion') is not None:
                versionXml.find('DatenbankVersion').tag = 'CharakterVersion'
            charakterVersion = int(versionXml.find('CharakterVersion').text)
            userDBCRC = int(versionXml.find('NutzerDatenbankCRC').text)
            userDBName = versionXml.find('NutzerDatenbankName').text or "Keine"

            if Wolke.DB.userDbXml is not None:
                currentUserDBCRC = binascii.crc32(etree.tostring(Wolke.DB.userDbXml))
                if userDBCRC != 0 and userDBCRC != currentUserDBCRC:
                    userDBChanged = True
            elif userDBCRC != 0:
                userDBChanged = True

            if versionXml.find('Plugins') is not None and versionXml.find('Plugins').text:
                self.enabledPlugins = list(map(str.strip, versionXml.find('Plugins').text.split(",")))
                if "LangerBogenBeschreibung" in self.enabledPlugins:
                    self.enabledPlugins.remove("LangerBogenBeschreibung") # it is now part of Sephrasto, no data will be lost anymore

        logging.debug("Starting Character Migration")
        updates = Migrationen.charakterMigrieren(self, root, charakterVersion)

        if len(updates) > 0:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setWindowTitle("Charakter laden - Datenbank wurde aktualisiert.")
            messageBox.setText("Seit du diesen Charakter das letzte mal bearbeitet hast wurde die offizielle Sephrasto-Datenbank aktualisiert. " \
                              "Dein Charakter ist jetzt auf dem neuesten Stand. " \
                              "Ausnahmen: Waffen werden nicht automatisch angepasst und behalten ihren (eventuell alten) Stand, ebenso alles was in Hausregeln geändert wurde.")
            messageBox.setInformativeText("Weitere Informationen:\n" + "\n".join(updates))
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec()

        #Plugins
        root = EventBus.applyFilter("charakter_xml_laden", root, { "charakter" : self })

        self.hausregeln = os.path.basename(Wolke.DB.datei) if Wolke.DB.datei else None

        alg = root.find('Beschreibung')
        self.name = alg.find('Name').text or ''
        self.spezies = alg.find('Spezies').text or ''
        self.status = int(alg.find('Status').text)
        self.kurzbeschreibung = alg.find('Kurzbeschreibung').text or ''
        self.schips = int(alg.find('SchiP').text)
        self.finanzen = int(alg.find('Finanzen').text)
        self.heimat = alg.find('Heimat').text
        heimaten = Wolke.DB.findHeimaten()
        if not self.heimat in heimaten:
            if "Mittelreich" in heimaten:
                self.heimat = "Mittelreich"
            else:
                self.heimat = heimaten[0] if len(heimaten) > 0 else ""
        for eig in alg.findall('Eigenheiten/*'):
            self.eigenheiten.append(eig.text or "")
        #Zweiter Block
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

        for vor in root.findall('Vorteile'):
            if "minderpakt" in vor.attrib:
                self.minderpakt = vor.get('minderpakt')
            else:
                self.minderpakt = None

        for vor in root.findall('Vorteile/*'):
            if not vor.text in Wolke.DB.vorteile:
                vIgnored.append(vor.text)
                continue
            self.vorteile.append(vor.text)

            if 'variableKosten' in vor.attrib:
                if Wolke.DB.vorteile[vor.text].variableKosten:
                    self.vorteileVariableKosten[vor.text] = int(vor.get('variableKosten'))
                else:
                    self.vorteileVariableKosten[vor.text] = Wolke.DB.vorteile[vor.text].kosten

            if 'kommentar' in vor.attrib:
                self.vorteileKommentare[vor.text] = vor.get('kommentar')

        #Vierter Block
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
                talent = Wolke.DB.talente[nam]
                if not fert.name in talent.fertigkeiten:
                    # talent was probably moved to a different fert
                    tIgnored.add(nam)
                    continue
                fert.gekaufteTalente.append(nam)

                if 'variableKosten' in tal.attrib:
                    #round down to nearest multiple in case of a db cost change
                    if Wolke.DB.talente[nam].variableKosten:
                        defaultKosten = self.getDefaultTalentCost(nam, fert.steigerungsfaktor)
                        kosten = int(tal.attrib['variableKosten'])
                        self.talenteVariableKosten[nam] = max(kosten - (kosten % defaultKosten), defaultKosten)
                    else:
                        self.talenteVariableKosten[nam] = self.getDefaultTalentCost(nam, fert.steigerungsfaktor)

                if 'kommentar' in tal.attrib:
                    self.talenteKommentare[nam] = tal.attrib['kommentar']

            fert.aktualisieren(self.attribute)
            self.fertigkeiten.update({fert.name: fert})

        for fer in root.findall('Fertigkeiten/FreieFertigkeit'):
            fert = Fertigkeiten.FreieFertigkeit()            
            fert.name = fer.attrib['name']
            fert.wert = int(fer.attrib['wert'])
            self.freieFertigkeiten.append(fert)

        #Fünfter Block
        objekte = root.find('Objekte');
        self.zonenSystemNutzen = objekte.find('Zonensystem').text == "1"

        for rüs in objekte.findall('Rüstungen/Rüstung'):
            rüst = Objekte.Ruestung()
            rüst.name = rüs.attrib['name']
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = Hilfsmethoden.RsStr2Array(rüs.attrib['rs'])
            self.rüstung.append(rüst)

        for waf in objekte.findall('Waffen/Waffe'):
            if waf.attrib['typ'] == 'Nah':
                waff = Objekte.Nahkampfwaffe()
            else:
                waff = Objekte.Fernkampfwaffe()
                waff.lz = int(waf.attrib['lz'])
            waff.wm = int(waf.get('wm'))
            waff.anzeigename = waf.attrib['name']
            waff.name = waf.get('id') or waff.anzeigename
            waff.rw = int(waf.attrib['rw'])
            waff.würfel = int(waf.attrib['würfel'])
            waff.würfelSeiten = int(waf.attrib['würfelSeiten'])
            waff.plus = int(waf.attrib['plus'])
            if waf.attrib['eigenschaften']:
                waff.eigenschaften = list(map(str.strip, waf.attrib['eigenschaften'].split(", ")))
            waff.härte = int(waf.attrib['härte'])
            waff.kampfstil = waf.attrib['kampfstil']
            if waff.name in Wolke.DB.waffen:
                dbWaffe = Wolke.DB.waffen[waff.name]
                waff.fertigkeit = dbWaffe.fertigkeit
                waff.talent = dbWaffe.talent
                waff.kampfstile = dbWaffe.kampfstile.copy()

            self.waffen.append(waff)

        for aus in objekte.findall('Ausrüstung/Ausrüstungsstück'):
            self.ausrüstung.append(aus.text or "")
        #Sechster Block 
        for fer in root.findall('ÜbernatürlicheFertigkeiten/ÜbernatürlicheFertigkeit'):
            nam = fer.attrib['name']
            if not nam in Wolke.DB.übernatürlicheFertigkeiten:
                übIgnored.append(nam)
                continue

            fert = Wolke.DB.übernatürlicheFertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            fert.addToPDF = fer.attrib['exportieren'] == "1"

            for tal in fer.findall('Talente/Talent'):
                nam = tal.attrib['name']
                if not nam in Wolke.DB.talente:
                    tIgnored.add(nam)
                    continue
                fert.gekaufteTalente.append(nam)

                if 'variableKosten' in tal.attrib:
                    #round down to nearest multiple in case of a db cost change
                    if Wolke.DB.talente[nam].variableKosten:
                        defaultKosten = self.getDefaultTalentCost(nam, fert.steigerungsfaktor)
                        kosten = int(tal.attrib['variableKosten'])
                        self.talenteVariableKosten[nam] = max(kosten - (kosten % defaultKosten), defaultKosten)
                    else:
                        self.talenteVariableKosten[nam] = self.getDefaultTalentCost(nam, fert.steigerungsfaktor)

                if 'kommentar' in tal.attrib:
                    self.talenteKommentare[nam] = tal.attrib['kommentar']

            fert.aktualisieren(self.attribute)
            self.übernatürlicheFertigkeiten.update({fert.name: fert})
        #Siebter Block
        self.epGesamt = int(root.find('Erfahrung/Gesamt').text)
        self.epAusgegeben = int(root.find('Erfahrung/Ausgegeben').text)   

        #Achter Block
        self.notiz = root.find('Notiz').text

        einstellungen = root.find('Einstellungen')
        self.charakterbogen = einstellungen.find('Charakterbogen').text
        self.voraussetzungenPruefen = einstellungen.find('VoraussetzungenPrüfen').text == "1"
        self.finanzenAnzeigen = einstellungen.find('FinanzenAnzeigen').text == "1"
        self.ueberPDFAnzeigen = einstellungen.find('ÜbernatürlichesPDFSpalteAnzeigen').text == "1"
        self.regelnAnhaengen = einstellungen.find('RegelnAnhängen').text == "1"
        self.regelnGroesse = int(einstellungen.find('RegelnGrösse').text)
        self.formularEditierbarkeit = int(einstellungen.find('FormularEditierbarkeit').text)
        self.regelnKategorien = list(map(str.strip, einstellungen.find('RegelnKategorien').text.split(", ")))

        #Neunter Block
        alg = root.find('BeschreibungDetails')
        self.kultur = alg.find('Kultur').text
        self.profession = alg.find('Profession').text or ''
        self.geschlecht = alg.find('Geschlecht').text or ''
        self.geburtsdatum = alg.find('Geburtsdatum').text or ''
        self.groesse = alg.find('Grösse').text or ''
        self.gewicht = alg.find('Gewicht').text or ''
        self.haarfarbe = alg.find('Haarfarbe').text or ''
        self.augenfarbe = alg.find('Augenfarbe').text or ''
        self.titel = alg.find('Titel').text or ''

        self.aussehen1 = alg.find('Aussehen1').text or ''
        self.aussehen2 = alg.find('Aussehen2').text or ''
        self.aussehen3 = alg.find('Aussehen3').text or ''
        self.aussehen4 = alg.find('Aussehen4').text or ''
        self.aussehen5 = alg.find('Aussehen5').text or ''
        self.aussehen6 = alg.find('Aussehen6').text or ''

        self.hintergrund0 = alg.find('Hintergrund0').text or ''
        self.hintergrund1 = alg.find('Hintergrund1').text or ''
        self.hintergrund2 = alg.find('Hintergrund2').text or ''
        self.hintergrund3 = alg.find('Hintergrund3').text or ''
        self.hintergrund4 = alg.find('Hintergrund4').text or ''
        self.hintergrund5 = alg.find('Hintergrund5').text or ''
        self.hintergrund6 = alg.find('Hintergrund6').text or ''
        self.hintergrund7 = alg.find('Hintergrund7').text or ''
        self.hintergrund8 = alg.find('Hintergrund8').text or ''

        if alg.find('Bild') is not None:
            byteArray = bytes(alg.find('Bild').text, 'utf-8')
            self.bild = base64.b64decode(byteArray)

        EventBus.doAction("charakter_xml_geladen", { "charakter" : self , "xmlRoot" : root })

        if userDBChanged or vIgnored or fIgnored or tIgnored or übIgnored:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle("Charakter laden - Hausregeln wurden geändert.")

            strArr = ["Seit du diesen Charakter das letzte mal bearbeitet hast wurden die Hausregeln aktualisiert. "]
            currentDBName = os.path.basename(Wolke.DB.datei) if Wolke.DB.datei else "Keine"
            if userDBName != currentDBName:
                strArr.append("Auch der Pfad der aktuell geladenen Hausregeln ist ein anderer:\n- Vorher: '")
                strArr.append(userDBName)
                strArr.append("'\n- Jetzt: '")
                strArr.append(currentDBName)
                strArr.append("'")

            strArr.append("\n\nEventuell hat der Charakter Vorteile/Fertigkeiten/Talente verloren und sein EP-Stand könnte sich verändert haben! ")
            strArr.append("Neu hinzugefügte Dinge sind unproblematisch. Waffen werden nicht automatisch angepasst und behalten ihren (eventuell alten) Stand. ")
            strArr.append("Dein Charakter ist jetzt an die aktuellen Hausregeln angepasst, überspeichere den Charakter nur wenn du dir sicher bist.")
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
            messageBox.setInformativeText(text + "\n\nDu kannst diese Nachricht in sephrasto.log nochmal nachlesen.")
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec()