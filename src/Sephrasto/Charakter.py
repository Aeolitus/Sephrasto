from Core.Attribut import Attribut
from Core.AbgeleiteterWert import AbgeleiteterWert
from Core.Energie import Energie
from Core.Fertigkeit import Fertigkeit, KampffertigkeitTyp
from Core.FreieFertigkeit import FreieFertigkeit, FreieFertigkeitDefinition
from Core.Ruestung import Ruestung, RuestungDefinition
from Core.Talent import Talent
from Core.Vorteil import Vorteil
from Core.Waffe import Waffe, WaffeDefinition
import lxml.etree as etree
import re
import copy
import logging
import collections
from EventBus import EventBus
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from PySide6 import QtWidgets, QtCore, QtGui
import os.path
import base64
from Migrationen import Migrationen
from VoraussetzungenListe import VoraussetzungenListe

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

        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.fertigkeiten = {}
        self.freieFertigkeiten = []
        self.freieFertigkeitenNumKostenlos = Wolke.DB.einstellungen["FreieFertigkeiten: Anzahl Kostenlos"].wert
        self.talente = {}

        #Fünfter Block: Ausrüstung etc
        self.rüstung = []
        self.waffen = []
        self.waffenwerte = []
        self.ausrüstung = []
        self.zonenSystemNutzen = False

        #Sechster Block: Übernatürliches
        self.übernatürlicheFertigkeiten = {}

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
        heimaten = sorted(Wolke.DB.einstellungen["Heimaten"].wert)
        if "Mittelreich" in heimaten:
            self.heimat = "Mittelreich"
        else:
            self.heimat = heimaten[0] if len(heimaten) > 0 else ""

        #Script API
        #Bei Änderungen nicht vergessen die script docs in ScriptAPI.md anzupassen
        self.currentVorteil = None #used by vorteilScriptAPI during iteration
        self.currentEigenschaft = None #used by waffenScriptAPI during iteration
        self.currentWaffenwerte = None #used by waffenScriptAPI during iteration
        self.waffenEigenschaftenUndo = [] #For undoing changes made by Vorteil scripts

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
            'getFertigkeit' : lambda name: copy.deepcopy(self.fertigkeiten[name]) if name in self.fertigkeiten else None, 
            'getÜbernatürlicheFertigkeit' : lambda name: copy.deepcopy(self.übernatürlicheFertigkeiten[name]) if name in self.übernatürlicheFertigkeiten else None, 
            'getFreieFertigkeiten' : lambda: copy.deepcopy(self.freieFertigkeiten), 
            'getVorteil' : lambda name: copy.deepcopy(self.vorteile[name]) if name in self.vorteile else None, 
            'getRüstung' : lambda: copy.deepcopy(self.rüstung), 
            'getWaffen' : lambda: copy.deepcopy(self.waffen), 
            'getAusrüstung' : lambda: copy.deepcopy(self.ausrüstung), 
            'modifyFertigkeitBasiswert' : lambda name, mod: setattr(self.fertigkeiten[name], 'basiswertMod', self.fertigkeiten[name].basiswertMod + mod) if name in self.fertigkeiten else None, 
            'modifyÜbernatürlicheFertigkeitBasiswert' : lambda name, mod: setattr(self.übernatürlicheFertigkeiten[name], 'basiswertMod', self.übernatürlicheFertigkeiten[name].basiswertMod + mod) if name in self.übernatürlicheFertigkeiten else None, 
            'modifyTalent' : self.API_modifyTalent, 
            'addTalent' : self.API_addTalent, 

            #Kampfstil
            'getKampfstil' : lambda kampfstil: copy.copy(self.kampfstilMods[kampfstil]) if kampfstil in self.kampfstilMods else KampfstilMod(), 
            'setKampfstil' : self.API_setKampfstil, 
            'modifyKampfstil' : self.API_modifyKampfstil, 

            #Attribute
            'getAttribut' : lambda attribut: self.attribute[attribut].wert,

            #Misc
            'addWaffeneigenschaft' : self.API_addWaffeneigenschaft, 
            'removeWaffeneigenschaft' : self.API_removeWaffeneigenschaft
        }

        #Add Attribute to API (readonly)
        for attribut in self.attribute:
            self.charakterScriptAPI["get" + attribut] = lambda attribut=attribut: self.attribute[attribut].wert
        
        #Add abgeleitete Werte to API
        for ab in self.abgeleiteteWerte:
            self.charakterScriptAPI['get' + ab + 'Basis'] = lambda ab=ab: self.abgeleiteteWerte[ab].basiswert
            self.charakterScriptAPI['get' + ab] = lambda ab=ab: self.abgeleiteteWerte[ab].wert
            self.charakterScriptAPI['set' + ab] = lambda wert, ab=ab: setattr(self.abgeleiteteWerte[ab], 'mod', wert - self.abgeleiteteWerte[ab].basiswert)
            self.charakterScriptAPI['modify' + ab] = lambda wert, ab=ab: setattr(self.abgeleiteteWerte[ab], 'mod', self.abgeleiteteWerte[ab].mod + wert)

        #Add Energien to API
        for en in Wolke.DB.energien:
            self.charakterScriptAPI['get' + en + 'Basis'] = lambda en=en: self.energien[en].basiswert if en in self.energien else 0
            self.charakterScriptAPI['set' + en + 'Basis'] = lambda basis, en=en: setattr(self.energien[en], "basiswert", basis) if en in self.energien else None
            self.charakterScriptAPI['modify' + en + 'Basis'] = lambda basis, en=en: setattr(self.energien[en], "basiswert", self.energien[en].basiswert + basis) if en in self.energien else None
            self.charakterScriptAPI['get' + en + 'Mod'] = lambda en=en: self.energien[en].mod if en in self.energien else 0
            self.charakterScriptAPI['set' + en + 'Mod'] = lambda mod, en=en: setattr(self.energien[en], "mod", mod) if en in self.energien else None
            self.charakterScriptAPI['modify' + en + 'Mod'] = lambda mod, en=en: setattr(self.energien[en], "mod", self.energien[en].mod + mod) if en in self.energien else None

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

        filter = ['setSB', 'modifySB', 'setBE', 'modifyBE', 'setRS', 'modifyRS',
                  'modifyFertigkeitBasiswert', 'setKampfstil', 'modifyKampfstil', 
                  'addWaffeneigenschaft', 'removeWaffeneigenschaft']
        for k, v in self.charakterScriptAPI.items():
            if k in self.waffenScriptAPI:
                assert False, "Duplicate entry"
            if k in filter:
                continue
            self.waffenScriptAPI[k] = v

        EventBus.doAction("charakter_instanziiert", { "charakter" : self })

    @property
    def heimat(self):
        return self._heimat

    @heimat.setter
    def heimat(self, heimat):
        if heimat == self._heimat:
            return
        script = Wolke.DB.einstellungen["Heimaten: Heimat geändert Script"].wert
        scriptAPI = {
            "heimatAlt" : self._heimat,
            "heimatNeu" : heimat,
            "addTalent" : lambda talent: self.addTalent(talent),
            "removeTalent" : lambda talent: self.removeTalent(talent)
          }
        exec(script, scriptAPI)
        self._heimat = heimat

    def API_modifyTalent(self, fertigkeit, talent, condition, mod):
        fert = self.fertigkeiten[fertigkeit]
        if not talent in fert.talentMods:
            fert.talentMods[talent] = {}

        if not condition in fert.talentMods[talent]:
            fert.talentMods[talent][condition] = mod
        else:
            fert.talentMods[talent][condition] += mod

    def API_addTalent(self, talent, kosten = -1, requiredÜberFert = None):
        fertVoraussetzungen = ""
        if requiredÜberFert:
            if requiredÜberFert in self.übernatürlicheFertigkeiten:
                fertVoraussetzungen = "Übernatürliche-Fertigkeit '" + requiredÜberFert + "'"
            else:
                return
        talent = self.addTalent(talent)
        talent.voraussetzungen = talent.voraussetzungen.add("Vorteil " + self.currentVorteil, Wolke.DB)
        talent.voraussetzungen = talent.voraussetzungen.add(fertVoraussetzungen, Wolke.DB)

        if kosten != -1:
            talent.kosten = kosten

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
            raise Exception("Die Waffeneigenschaft '" + self.currentEigenschaft + "' erfordert einen Parameter, beispielsweise Schwer (4), aber es wurde keiner gefunden.")
        parameters = list(map(str.strip, match.group(1).split(";")))
        if not len(parameters) >= paramNb:
            raise Exception("Die Waffeneigenschaft '" + self.currentEigenschaft + "' erfordert " + paramNb + " Parameter, aber es wurde(n) nur " + len(parameters) + " gefunden. Parameter müssen mit Semikolon getrennt werden")
        return parameters[paramNb-1]

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

        for fert in self.fertigkeiten:
            self.fertigkeiten[fert].basiswertMod = 0
            self.fertigkeiten[fert].talentMods = {}

        for fert in self.übernatürlicheFertigkeiten:
            self.übernatürlicheFertigkeiten[fert].basiswertMod = 0
            self.übernatürlicheFertigkeiten[fert].talentMods = {}

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
            if not vorteil.script:
                continue
            vorteileByPrio[vorteil.scriptPrio].append(vorteil)

        for key in sorted(vorteileByPrio):
            for vort in vorteileByPrio[key]:
                logging.info("Character: applying script for Vorteil " + vort.name)
                self.currentVorteil = vort.name
                vort.executeScript()
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
        self.waffenwerte = []

        error = []
        for el in self.waffen:
            waffenwerte = Waffenwerte()
            self.waffenwerte.append(waffenwerte)
            waffenwerte.kampfstil = el.kampfstil
            waffenwerte.härte = el.härte
            if "WS" in self.abgeleiteteWerte and el.name in Wolke.DB.einstellungen["Waffen: Härte WSStern"].wert:
                waffenwerte.härte = self.abgeleiteteWerte["WS"].finalwert
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
                if el.kampfstil != WaffeDefinition.keinKampfstil:
                    logging.warn("Waffe " + el.name + " referenziert einen nicht existierenden Kampfstil: " + el.kampfstil)

            # Execute script to calculate weapon stats
            scriptAPI = {
                'getAttribut' : lambda attribut: self.attribute[attribut].wert,
                'getWaffe' : lambda: copy.deepcopy(el),
                'getPW' : lambda: pw,
                'getKampfstil' : lambda: copy.deepcopy(kampfstilMods),
                'setWaffenwerte' : lambda at, vt, plus, rw: setattr(waffenwerte, 'at', at) or setattr(waffenwerte, 'vt', vt) or setattr(waffenwerte, 'plus', plus) or setattr(waffenwerte, 'rw', rw)
            }
            for ab in self.abgeleiteteWerte:
                scriptAPI['get' + ab + 'Basis'] = lambda ab=ab: self.abgeleiteteWerte[ab].basiswert
                scriptAPI['get' + ab] = lambda ab=ab: self.abgeleiteteWerte[ab].wert
                scriptAPI['get' + ab + 'Mod'] = lambda ab=ab: self.abgeleiteteWerte[ab].mod

        
            scriptAPI['getBEBySlot'] = lambda rüstungsNr: 0 if rüstungsNr < 1 or len(self.rüstung) < rüstungsNr else self.rüstung[rüstungsNr-1].getBEFinal(self.abgeleiteteWerte)

            try:
                # Execute global script
                exec(Wolke.DB.einstellungen["Waffen: Waffenwerte Script"].wert, scriptAPI)

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
                        we.executeScript(self.waffenScriptAPI)

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

        vorteile = copy.deepcopy(vorteile or self.vorteile)
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
    
    def xmlSchreiben(self, filename):
        '''Speichert dieses Charakter-Objekt in einer XML Datei, deren 
        Dateiname inklusive Pfad als Argument übergeben wird'''
        #Document Root
        root = etree.Element('Charakter')

        versionXml = etree.SubElement(root, 'Version')
        etree.SubElement(versionXml, 'CharakterVersion').text = str(Migrationen.charakterCodeVersion)
        etree.SubElement(versionXml, 'Plugins').text = ", ".join(self.enabledPlugins)

        if self.neueHausregeln is not None:
            etree.SubElement(versionXml, 'Hausregeln').text = self.neueHausregeln
        else:
            etree.SubElement(versionXml, 'Hausregeln').text = Wolke.DB.hausregelnAnzeigeName

        #Erster Block
        sub =  etree.SubElement(root, 'Beschreibung')
        etree.SubElement(sub, 'Name').text = self.name
        etree.SubElement(sub, 'Spezies').text = self.spezies
        etree.SubElement(sub, 'Status').text = str(self.status)
        etree.SubElement(sub, 'Kurzbeschreibung').text = self.kurzbeschreibung
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
        for energie in self.energien:
            etree.SubElement(en, energie).set('wert', str(self.energien[energie].wert))
        #Dritter Block    
        vor = etree.SubElement(root, 'Vorteile')
        for vorteil in self.vorteile.values():
            v = etree.SubElement(vor, 'Vorteil')
            v.set('name', vorteil.name)
            if vorteil.variableKosten:
                v.set('variableKosten', str(vorteil.kosten))
            if vorteil.kommentarErlauben:
                v.set('kommentar', vorteil.kommentar)

        #Vierter Block
        fer = etree.SubElement(root, 'Fertigkeiten')
        for fert in self.fertigkeiten:
            fertNode = etree.SubElement(fer, 'Fertigkeit')
            fertNode.set('name', self.fertigkeiten[fert].name)
            fertNode.set('wert', str(self.fertigkeiten[fert].wert))

        tal = etree.SubElement(root, 'Talente')
        for talent in self.talente.values():
            talNode = etree.SubElement(tal, 'Talent')
            talNode.set('name', talent.name)
            if talent.variableKosten:
                talNode.set('variableKosten', str(talent.kosten))
            if talent.kommentarErlauben:
                talNode.set('kommentar', talent.kommentar)

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
            wafNode.set('beSlot', str(waff.beSlot))
            wafNode.set('kampfstil', waff.kampfstil)
            wafNode.set('wm', str(waff.wm))
            if waff.fernkampf:
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
        etree.SubElement(einstellungen, 'DetailsAnzeigen').text = "1" if self.detailsAnzeigen else "0"
        etree.SubElement(einstellungen, 'RegelnAnhängen').text = "1" if self.regelnAnhaengen else "0"
        etree.SubElement(einstellungen, 'RegelnGrösse').text = str(self.regelnGroesse)
        etree.SubElement(einstellungen, 'DeaktivierteRegelKategorien').text = str(",".join(self.deaktivierteRegelKategorien))
        etree.SubElement(einstellungen, 'FormularEditierbarkeit').text = "1" if self.formularEditierbar else "0"

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
        for i in range(6):
            etree.SubElement(sub, 'Aussehen' + str(i+1)).text = self.aussehen[i]
        for i in range(9):
            etree.SubElement(sub, 'Hintergrund' + str(i)).text = self.hintergrund[i]
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
        # NutzerDatenbankName and basename are for legacy reasons - this code runs without migration
        for event, element in etree.iterparse(filename, tag=["Hausregeln", "NutzerDatenbankName"]):
            return os.path.basename(element.text) or "Keine"
        return "Keine"

    def xmlLesen(self, filename):
        '''Läd ein Charakter-Objekt aus einer XML Datei, deren Dateiname 
        inklusive Pfad als Argument übergeben wird'''
        #Alles bisherige löschen
        self.__init__()
        root = etree.parse(filename).getroot()
        logging.debug("Starting Character Migration")
        Migrationen.charakterMigrieren(root)
        if len(Migrationen.charakterUpdates) > 0:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setWindowTitle("Charakter wurde aktualisiert")
            messageBox.setText(Migrationen.charakterUpdates[0])
            if len(Migrationen.charakterUpdates) > 1:
                messageBox.setInformativeText("Weitere Informationen:\n- " + "\n- ".join(Migrationen.charakterUpdates[1:]))
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec()
        
        #Erster Block
        versionXml = root.find('Version')
        if versionXml.find('Plugins').text:
            self.enabledPlugins = list(map(str.strip, versionXml.find('Plugins').text.split(",")))
        letzteHausregeln = versionXml.find("Hausregeln").text or "Keine"

        root = EventBus.applyFilter("charakter_xml_laden", root, { "charakter" : self })

        alg = root.find('Beschreibung')
        self.name = alg.find('Name').text or ''
        self.spezies = alg.find('Spezies').text or ''
        self.status = int(alg.find('Status').text)
        self.kurzbeschreibung = alg.find('Kurzbeschreibung').text or ''
        self.finanzen = int(alg.find('Finanzen').text)
        self.heimat = alg.find('Heimat').text
        heimaten = sorted(Wolke.DB.einstellungen["Heimaten"].wert)
        if not self.heimat in heimaten:
            if "Mittelreich" in heimaten:
                self.heimat = "Mittelreich"
            else:
                self.heimat = heimaten[0] if len(heimaten) > 0 else ""
        for eig in alg.findall('Eigenheiten/*'):
            self.eigenheiten.append(eig.text or "")

        aIgnored = []
        eIgnored = []
        vIgnored = []
        tIgnored = []
        fIgnored = []
        übIgnored = []
        wIgnored = []

        #Zweiter Block
        for atr in root.findall('Attribute/*'):
            if not atr.tag in Wolke.DB.attribute:
                aIgnored.append(atr.tag)
                continue
            self.attribute[atr.tag].wert = int(atr.text)
            self.attribute[atr.tag].aktualisieren()
        for ene in root.findall('Energien/*'):
            if not ene.tag in Wolke.DB.energien:
                eIgnored.append(atr.tag)
                continue
            self.energien[ene.tag] = Energie(Wolke.DB.energien[ene.tag], self)
            self.energien[ene.tag].wert = int(ene.attrib['wert'])
        #Dritter Block
        for vor in root.findall('Vorteile/Vorteil'):
            name = vor.attrib['name']
            if not name in Wolke.DB.vorteile:
                vIgnored.append(name)
                continue
            vorteil = self.addVorteil(name)
            if vorteil.variableKosten and 'variableKosten' in vor.attrib:
                vorteil.kosten = int(vor.get('variableKosten'))
            if vorteil.kommentarErlauben and 'kommentar' in vor.attrib:
                vorteil.kommentar = vor.get('kommentar')

        if "Minderpakt" in self.vorteile:
            minderpakt = self.vorteile["Minderpakt"]
            if not minderpakt.kommentar in Wolke.DB.vorteile:
                vIgnored.append("Minderpakt")
                self.removeVorteil(minderpakt)
            else:
                minderpakt.voraussetzungen = VoraussetzungenListe().compile("Vorteil " + minderpakt.kommentar, Wolke.DB)
                vorteil = self.addVorteil(minderpakt.kommentar)
                vorteil.voraussetzungen = VoraussetzungenListe().compile("Vorteil Minderpakt", Wolke.DB)
                vorteil.kosten = 20

        #Vierter Block
        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            name = fer.attrib['name']
            if not name in Wolke.DB.fertigkeiten:
                fIgnored.append(name)
                continue

            fert = Fertigkeit(Wolke.DB.fertigkeiten[name], self)
            fert.wert = int(fer.attrib['wert'])
            fert.aktualisieren()
            self.fertigkeiten.update({fert.name: fert})

        for fer in root.findall('Fertigkeiten/FreieFertigkeit'):
            name = fer.attrib['name']
            definition = None
            if name in Wolke.DB.freieFertigkeiten:
                definition = Wolke.DB.freieFertigkeiten[name]
            else:
                definition = FreieFertigkeitDefinition()
                definition.name = name
            fert = FreieFertigkeit(definition, self)
            fert.wert = int(fer.attrib['wert'])
            self.freieFertigkeiten.append(fert)

        #Fünfter Block
        objekte = root.find('Objekte');
        self.zonenSystemNutzen = objekte.find('Zonensystem').text == "1"

        for rüs in objekte.findall('Rüstungen/Rüstung'):
            name = rüs.attrib['name']
            definition = None
            if name in Wolke.DB.rüstungen:
                definition = Wolke.DB.rüstungen[name]
            else:
                definition = RuestungDefinition()
                definition.name = name
            rüst = Ruestung(definition)
            rüst.name = rüs.attrib['name']
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = Hilfsmethoden.RsStr2Array(rüs.attrib['rs'])
            self.rüstung.append(rüst)

        for waf in objekte.findall('Waffen/Waffe'):
            nam = waf.attrib['id']
            if not nam in Wolke.DB.waffen:
                self.waffen.append(Waffe(WaffeDefinition()))
                if nam:
                    wIgnored.append(nam)
                continue
            waff = Waffe(Wolke.DB.waffen[nam])
            if waff.fernkampf:
                waff.lz = int(waf.attrib['lz']) 
            waff.wm = int(waf.get('wm'))
            waff.anzeigename = waf.attrib['name']
            waff.rw = int(waf.attrib['rw'])
            waff.würfel = int(waf.attrib['würfel'])
            waff.würfelSeiten = int(waf.attrib['würfelSeiten'])
            waff.plus = int(waf.attrib['plus'])
            if waf.attrib['eigenschaften']:
                waff.eigenschaften = list(map(str.strip, waf.attrib['eigenschaften'].split(", ")))
            waff.härte = int(waf.attrib['härte'])
            waff.beSlot = int(waf.attrib['beSlot'])
            waff.kampfstil = waf.attrib['kampfstil']
            self.waffen.append(waff)

        for aus in objekte.findall('Ausrüstung/Ausrüstungsstück'):
            self.ausrüstung.append(aus.text or "")

        #Sechster Block 
        for fer in root.findall('ÜbernatürlicheFertigkeiten/ÜbernatürlicheFertigkeit'):
            nam = fer.attrib['name']
            if not nam in Wolke.DB.übernatürlicheFertigkeiten:
                übIgnored.append(nam)
                continue

            fert = Fertigkeit(Wolke.DB.übernatürlicheFertigkeiten[nam], self)
            fert.wert = int(fer.attrib['wert'])
            fert.addToPDF = fer.attrib['exportieren'] == "1"
            fert.aktualisieren()
            self.übernatürlicheFertigkeiten.update({fert.name: fert})

        for tal in root.findall('Talente/Talent'):
            nam = tal.attrib['name']
            if not nam in Wolke.DB.talente:
                tIgnored.append(nam)
                continue
            
            talent = self.addTalent(nam)
            if talent.variableKosten and 'variableKosten' in tal.attrib:
                talent.kosten = int(tal.attrib['variableKosten'])
            if talent.kommentarErlauben and 'kommentar' in tal.attrib:
                talent.kommentar = tal.attrib['kommentar']

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
        self.detailsAnzeigen = einstellungen.find('DetailsAnzeigen').text == "1"
        self.regelnAnhaengen = einstellungen.find('RegelnAnhängen').text == "1"
        self.regelnGroesse = int(einstellungen.find('RegelnGrösse').text)
        self.formularEditierbar = einstellungen.find('FormularEditierbarkeit').text == "1"
        if einstellungen.find('DeaktivierteRegelKategorien').text:
            self.deaktivierteRegelKategorien = list(map(str.strip, einstellungen.find('DeaktivierteRegelKategorien').text.split(",")))

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
        for i in range(6):
            self.aussehen[i] = alg.find('Aussehen' + str(i+1)).text or ''
        for i in range(9):
            self.hintergrund[i] = alg.find('Hintergrund' + str(i)).text or ''

        if alg.find('Bild') is not None:
            byteArray = bytes(alg.find('Bild').text, 'utf-8')
            self.bild = base64.b64decode(byteArray)

        EventBus.doAction("charakter_xml_geladen", { "charakter" : self , "xmlRoot" : root })
        hausregelMissmatch = Wolke.DB.hausregelnAnzeigeName != letzteHausregeln
        anyIgnored = aIgnored or eIgnored or vIgnored or fIgnored or tIgnored or übIgnored or wIgnored
        if hausregelMissmatch or anyIgnored:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowTitle("Charakter laden - Hausregeln wurden geändert.")

            strArr = ["Achtung, die Hausregeln haben sich geändert!"]

            if hausregelMissmatch:
                strArr.append(f"\n- Vorher: ")
                strArr.append(letzteHausregeln)
                strArr.append("\n- Jetzt: ")
                strArr.append(Wolke.DB.hausregelnAnzeigeName)

            strArr.append("\n\nDein Charakter wurde an die neuen Regeln angepasst. Überspeichere ihn nur wenn du dir sicher bist, dass alles in Ordnung ist.")
            text = "".join(strArr)
            messageBox.setText(text)
            logging.warning(text)

            strArr = []
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

            text = "".join(strArr)
            messageBox.setInformativeText(text)
            logging.warning(text)
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            messageBox.exec()