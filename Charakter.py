import Definitionen
import Fertigkeiten
import Objekte
import lxml.etree as etree
import re
import copy
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden

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
        self.heimat = 'Mittelreich'
        self.schips = 4
        self.finanzen = 2;
        self.eigenheiten = []

        #Zweiter Block: Attribute und Abgeleitetes
        self.attribute = {}
        for key in Definitionen.Attribute.keys():
            self.attribute[key] = Fertigkeiten.Attribut(key)
        self.wsBasis = -1
        self.ws = -1
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
        self.kap = Fertigkeiten.Energie()
        
        #Dritter Block: Vorteile, gespeichert als String
        self.vorteile = []
        self.vorteileVariable = {} #Contains Name: Cost
        self.minderpakt = None

        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.fertigkeiten = copy.deepcopy(Wolke.DB.fertigkeiten)
        self.freieFertigkeiten = []
        self.talenteVariable = {} #Contains Name: Cost

        #Fünfter Block: Ausrüstung etc
        self.be = 0
        self.rüstung = []
        self.waffen = []
        self.ausrüstung = []
        self.rüstungsgewöhnung = 0
        self.rsmod = 0

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

        #Achter Block: Flags etc
        self.höchsteKampfF = -1
        
        # Diagnostics
        self.fehlercode = 0

    def aktualisieren(self):
        '''Berechnet alle abgeleiteten Werte neu'''
        for key in Definitionen.Attribute:
            self.attribute[key].aktualisieren()
        self.wsBasis = 4 + int(self.attribute['KO'].wert/4)
        self.ws = self.wsBasis
        if "Unverwüstlich" in self.vorteile:
            self.ws += 1
        self.mrBasis = 4 + int(self.attribute['MU'].wert/4)
        self.mr = self.mrBasis
        if "Willensstark I" in self.vorteile:
            self.mr += 4
        if "Willensstark II" in self.vorteile:
            self.mr += 4
        if "Unbeugsamkeit" in self.vorteile:
            self.mr += round(self.attribute['MU'].wert/2+0.0001)
        self.gsBasis = 4 + int(self.attribute['GE'].wert/4+0.0001)
        self.gs = self.gsBasis
        if "Flink I" in self.vorteile:
            self.gs += 1
        if "Flink II" in self.vorteile:
            self.gs += 1
        self.iniBasis = self.attribute['IN'].wert
        self.ini = self.iniBasis
        if "Kampfreflexe" in self.vorteile:
            self.ini += 4                                 
        self.dh = self.attribute['KO'].wert
        if "Abgehärtet II" in self.vorteile:
            self.dh += 2
        self.schadensbonusBasis = int(self.attribute['KK'].wert/4)
        self.schadensbonus = self.schadensbonusBasis
        self.schips = 4
        if self.finanzen >= 2: 
            self.schips += self.finanzen - 2
        else:
            self.schips -= (2-self.finanzen)*2
        self.be = 0
        self.rüstungsgewöhnung = 0
        if len(self.rüstung) > 0:
            self.be = self.rüstung[0].be
        if "Rüstungsgewöhnung I" in self.vorteile:
            self.rüstungsgewöhnung += 1
        if "Rüstungsgewöhnung II" in self.vorteile:
            self.rüstungsgewöhnung += 2
        self.be = max(0,self.be-self.rüstungsgewöhnung)
        self.rsmod = 0
        if "Natürliche Rüstung" in self.vorteile:
            self.rsmod += 1
        self.updateVorts()
        self.updateFerts()
        self.epZaehlen()

    def epZaehlen(self):
        '''Berechnet die bisher ausgegebenen EP'''
        spent = 0
        #Erster Block ist gratis
        #Zweiter Block: Attribute und Abgeleitetes
        for key in Definitionen.Attribute:
            spent += sum(range(self.attribute[key].wert+1)) *\
                        self.attribute[key].steigerungsfaktor
        spent += sum(range(self.asp.wert+1))*self.asp.steigerungsfaktor
        spent += sum(range(self.kap.wert+1))*self.kap.steigerungsfaktor   

        self.EP_Attribute = spent
        #Dritter Block: Vorteile
        for vor in self.vorteile:
            if vor == self.minderpakt:
                if "Minderpakt" in self.vorteile:
                    continue
                else:
                    self.minderpakt = None
            if vor in self.vorteileVariable:
                spent += self.vorteileVariable[vor]
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
                if tal in self.talenteVariable:
                    val = self.talenteVariable[tal]
                elif Wolke.DB.talente[tal].kosten != -1:
                    val = Wolke.DB.talente[tal].kosten
                elif Wolke.DB.talente[tal].verbilligt:
                    val = 10*self.fertigkeiten[fer].steigerungsfaktor
                else:
                    val = 20*self.fertigkeiten[fer].steigerungsfaktor
                spent += val
                self.EP_Fertigkeiten_Talente += val
        skip = False                                                 
        for fer in self.freieFertigkeiten:
            # Dont count Muttersprache
            if fer.wert == 3 and not skip:
                skip = True
                continue
            val = Definitionen.FreieFertigkeitKosten[fer.wert-1]
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
                if tal in self.talenteVariable:
                    val = self.talenteVariable[tal]
                elif Wolke.DB.talente[tal].kosten != -1:
                    val = Wolke.DB.talente[tal].kosten
                elif Wolke.DB.talente[tal].verbilligt:
                    val = 10*self.übernatürlicheFertigkeiten[fer]\
                                                        .steigerungsfaktor
                else:
                    val = 20*self.übernatürlicheFertigkeiten[fer]\
                                                        .steigerungsfaktor
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
            if contFlag:
                break

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
            if self.fertigkeiten[fert].kampffertigkeit and \
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
        '''
        Prüft, ob ein Array von Voraussetzungen erfüllt ist.
        Format: ['L:Str:W', 'L:Str:W']
        Dabei ist L:
            V für Vorteil - prüft, ob ein Vorteil vorhanden ist. W = 1 bedeutet, der
                Vorteil muss vorhanden sein. W=0 bedeutet, der Vorteil darf nicht vorhanden sein.
            W für Waffeneigenschaft - prüft, ob der Charakter eine Waffe mit der angegebenen Eigenschaft besitzt. W ist immer 1.
            A für Attribut - prüft, ob das Attribut mit Key Str mindestens auf Wert W ist
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
                    erfüllt = self.voraussetzungenPrüfen(voraus,True)
                else: 
                    #Split am Separator
                    arr = re.split(':',voraus)
                    #Vorteile:
                    if arr[0] is 'V':
                        if len(arr) > 2:
                            cond = int(arr[2])
                        else: 
                            cond = 1
                        found = 0
                        if arr[1] in self.vorteile:
                            found = 1
                        if found == 1 and cond == 1:
                            erfüllt = True
                        elif found == 0 and cond == 0:
                            erfüllt = True
                    #Waffeneigenschaften:
                    elif arr[0] is 'W':
                        for waffe in self.waffen:
                            if arr[1] in waffe.eigenschaften:
                                erfüllt = True
                                break
                    #Attribute:
                    elif arr[0] is 'A':
                        #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                        if self.attribute[arr[1]].wert >= int(arr[2]):
                            erfüllt = True            
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
                v.set('variable',str(self.vorteileVariable[vort]))
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
                    talNode.set('variable',str(self.talenteVariable[talent]))
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
            wafNode.set('name',waff.name)
            wafNode.set('W6',str(waff.W6))
            wafNode.set('plus',str(waff.plus))
            wafNode.set('eigenschaften',waff.eigenschaften)
            wafNode.set('haerte',str(waff.haerte))
            wafNode.set('rw',str(waff.rw))
            wafNode.set('kampfstil',str(waff.kampfstil))
            if type(waff) is Objekte.Nahkampfwaffe:
                wafNode.set('typ','Nah')
                wafNode.set('wm',str(waff.wm))
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
            talentNode = etree.SubElement(fertNode,'Talente')
            for talent in self.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                talNode = etree.SubElement(talentNode,'Talent')
                talNode.set('name',talent)
                if talent in self.talenteVariable:
                    talNode.set('variable',str(self.talenteVariable[talent]))
                else:
                    talNode.set('variable','-1')
        #Siebter Block
        Wolke.Fehlercode = -63
        epn = etree.SubElement(root,'Erfahrung')
        etree.SubElement(epn,'EPtotal').text = str(self.EPtotal)
        etree.SubElement(epn,'EPspent').text = str(self.EPspent)
        #Write XML to file
        Wolke.Fehlercode = -64
        doc = etree.ElementTree(root)
        with open(filename,'wb') as file:
            file.seek(0)
            file.truncate()
            doc.write(file, encoding='UTF-8', pretty_print=True)
            file.truncate()
        Wolke.Fehlercode = 0

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
        alg = root.find('AllgemeineInfos')
        self.name = alg.find('name').text
        self.rasse = alg.find('rasse').text
        self.status = int(alg.find('status').text)
        self.kurzbeschreibung = alg.find('kurzbeschreibung').text
        self.schips = int(alg.find('schips').text)
        self.finanzen = int(alg.find('finanzen').text)
        tmp = alg.find('heimat')
        if tmp is None: 
            self.heimat = 'Mittelreich'
        else:
            self.heimat = tmp.text
        for eig in alg.findall('eigenheiten/*'):
            self.eigenheiten.append(eig.text)
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
        Wolke.Fehlercode = -45
        for vor in root.findall('Vorteile'):
            if "minderpakt" in vor.attrib:
                self.minderpakt = vor.get('minderpakt')
            else:
                self.minderpakt = None
        for vor in root.findall('Vorteile/*'):
            self.vorteile.append(vor.text)
            var = int(vor.get('variable'))
            if var != -1:
                self.vorteileVariable[vor.text] = var
        #Vierter Block
        Wolke.Fehlercode = -46
        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            nam = fer.attrib['name']
            fert = Wolke.DB.fertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            for tal in fer.findall('Talente/Talent'):
                fert.gekaufteTalente.append(tal.attrib['name'])
                var = int(tal.attrib['variable'])
                if int(tal.attrib['variable']) != -1:
                    self.talenteVariable[tal] = int(tal.attrib['variable'])
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
        for rüs in root.findall('Objekte/Rüstungen/Rüstung'):
            rüst = Objekte.Ruestung()
            rüst.name = rüs.attrib['name']
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = Hilfsmethoden.RsStr2Array(rüs.attrib['rs'])
            self.rüstung.append(rüst)
        Wolke.Fehlercode = -49
        for waf in root.findall('Objekte/Waffen/Waffe'):
            if waf.attrib['typ'] == 'Nah':
                waff = Objekte.Nahkampfwaffe()
                waff.wm = int(waf.attrib['wm'])
            else:
                waff = Objekte.Fernkampfwaffe()
                waff.lz = int(waf.attrib['lz'])
            waff.name = waf.attrib['name']
            waff.rw = int(waf.attrib['rw'])
            waff.W6 = int(waf.attrib['W6'])
            waff.plus = int(waf.attrib['plus'])
            waff.eigenschaften = waf.attrib['eigenschaften']
            waff.haerte = int(waf.attrib['haerte'])
            waff.kampfstil = int(waf.attrib['kampfstil'])
            self.waffen.append(waff)
        Wolke.Fehlercode = -50
        for aus in root.findall('Objekte/Ausrüstung/Ausrüstungsstück'):
            self.ausrüstung.append(aus.text)
        #Sechster Block 
        Wolke.Fehlercode = -51
        for fer in root.findall('Übernatürliche-Fertigkeiten/Übernatürliche-Fertigkeit'):
            nam = fer.attrib['name']
            fert = Wolke.DB.übernatürlicheFertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            for tal in fer.findall('Talente/Talent'):
                fert.gekaufteTalente.append(tal.attrib['name'])
                if int(tal.attrib['variable']) != -1:
                    self.talenteVariable[tal.attrib['name']] = int(tal.attrib['variable'])
            fert.aktualisieren()
            self.übernatürlicheFertigkeiten.update({fert.name: fert})
        #Siebter Block
        Wolke.Fehlercode = -52
        self.EPtotal = int(root.find('Erfahrung/EPtotal').text)
        self.EPspent = int(root.find('Erfahrung/EPspent').text)   
        
        Wolke.Fehlercode = 0