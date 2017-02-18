import Definitionen
import Fertigkeiten
import Objekte
import lxml.etree as etree
import re

class Char():
    def __init__(self):
        '''Initialisiert alle Variablen und füllt die Listen'''
        #Erster Block: Allgemeine Infos
        self.name = ''
        self.rasse = ''
        self.status = -1
        self.kurzbeschreibung = ''
        self.schips = 3
        self.finanzen = 2;
        self.eigenheiten = []

        #Zweiter Block: Attribute und Abgeleitetes
        self.attribute = {}
        for key in Definitionen.Attribute.keys():
            self.attribute[key] = Fertigkeiten.Attribut(key)
        self.ws = -1
        self.mr = -1
        self.gs = -1
        self.dh = -1
        self.schadensbonus = -1
        self.ini = -1
        
        #Dritter Block: Vorteile
        self.vorteile = []

        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.fertigkeiten = {}
        self.freieFertigkeiten = []

        #Fünfter Block: Ausrüstung etc
        self.rüstung = []
        self.waffen = []
        self.ausrüstung = []

        #Sechster Block: Übernatürliches
        self.übernatürlicheFertigkeiten = {}

        #Siebter Block: EP
        self.EPtotal = 0
        self.EPspent = 0

        #Achter Block: Flags etc
        self.höchsteKampfF = -1

    def aktualisieren(self):
        '''Berechnet alle abgeleiteten Werte neu'''
        self.ws = 4 + int(self.attribute['KO'].wert/4)
        self.mr = 4 + int(self.attribute['MU'].wert/4)
        self.gs = 4 + int(self.attribute['GE'].wert/4)
        self.ini = self.attribute['IN'].wert
        self.schadensbonus = int(self.attribute['KK'].wert/4)
        for fert in self.fertigkeiten:
            if fert.wert > self.höchsteKampfF:
                self.höchsteKampfF = fert.wert
        self.schips = self.finanzen+1

    def epAusgeben(self,EP):
        '''Versucht, EP Erfahrungspunkte auszugeben. Returned 1 wenn erfolgreich und 0 wenn nicht genug vorhanden.'''
        if self.EPtotal-self.EPspent>EP:
            self.EPspent += EP
            return 1
        return 0

    def voraussetzungenPrüfen(self,Vor,Or=False):
        '''
        Prüft, ob ein Array von Voraussetzungen erfüllt ist.
        Format: ['L:Str:W', 'L:Str:W']
        Dabei ist L:
            V für Vorteil - prüft, ob ein Vorteil vorhanden ist. W = 1 bedeutet, der
                Vorteil muss vorhanden sein. W=0 bedeutet, der Vorteil darf nicht vorhanden sein.
            A für Attribut - prüft, ob das Attribut mit Key Str mindestens auf Wert W ist
        Einträge im Array können auch weitere Arrays and Voraussetzungen sein.
        Aus diesen Arrays muss nur ein Eintrag erfüllt sein.
        '''
        #Gehe über alle Elemente in der Liste
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
                #Attribute:
                elif arr[0] is 'A':
                    #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                    if self.attribute[arr[1]].wert >= int(arr[2]):
                        erfüllt = True            
            if not Or and not erfüllt:
                return False
            elif Or and erfüllt:
                return True
        # Alle Voraussetzungen sind gecheckt und wir sind nirgendwo gefailt.
        return True
    
    def xmlSchreiben(self,filename):
        '''Speichert dieses Charakter-Objekt in einer XML Datei, deren Dateiname inklusive Pfad als Argument übergeben wird'''
        #Document Root
        root = etree.Element('Charakter')
        #Erster Block
        sub =  etree.SubElement(root,'AllgemeineInfos')
        etree.SubElement(sub,'name').text = self.name
        etree.SubElement(sub,'rasse').text = self.rasse
        etree.SubElement(sub,'status').text = str(self.status)
        etree.SubElement(sub,'kurzbeschreibung').text = self.kurzbeschreibung
        etree.SubElement(sub,'schips').text = str(self.schips)
        etree.SubElement(sub,'finanzen').text = str(self.finanzen)
        eigs = etree.SubElement(sub,'eigenheiten')
        for eigenh in self.eigenheiten:
            etree.SubElement(eigs,'Eigenheit').text = eigenh
        #Zweiter Block - abgeleitete nicht notwendig da automatisch neu berechnet
        atr = etree.SubElement(root,'Attribute')
        for attr in self.attribute:
            etree.SubElement(atr,attr).text = str(self.attribute[attr].wert)
        #Dritter Block    
        vor = etree.SubElement(root,'Vorteile')
        for vort in self.vorteile:
            etree.SubElement(vor,'Vorteil').text = vort
        #Vierter Block
        fer = etree.SubElement(root,'Fertigkeiten')
        for fert in self.fertigkeiten:
            fertNode = etree.SubElement(fer,'Fertigkeit')
            fertNode.set('name',self.fertigkeiten[fert].name)
            fertNode.set('wert',str(self.fertigkeiten[fert].wert))
            talentNode = etree.SubElement(fertNode,'Talente')
            for talent in self.fertigkeiten[fert].gekaufteTalente:
                etree.SubElement(talentNode,'Talent').set('name',talent.name)
        for fert in self.freieFertigkeiten:
            freiNode = etree.SubElement(fer,'Freie-Fertigkeit')
            freiNode.set('name',fert.name)
            freiNode.set('wert',str(fert.wert))
        #Fünfter Block
        aus = etree.SubElement(root,'Objekte')
        rüs = etree.SubElement(aus,'Rüstungen')
        for rüst in self.rüstung:
            rüsNode = etree.SubElement(rüs,'Rüstung')
            rüsNode.set('name',rüst.name)
            rüsNode.set('be',str(rüst.be))
            rüsNode.set('rs',repr(rüst.rs))
        waf = etree.SubElement(aus,'Waffen')
        for waff in self.waffen:
            wafNode = etree.SubElement(waf,'Waffe')
            wafNode.set('name',waff.name)
            wafNode.set('W6',str(waff.w6))
            wafNode.set('plus',str(waff.plus))
            wafNode.set('eigenschaften',waff.eigenschaften)
            wafNode.set('härte',str(waff.härte))
            if waff is Objekte.Nahkampfwaffe:
                wafNode.set('Typ','Nah')
                wafNode.set('rw',str(waff.rw))
                wafNode.set('wm',str(waff.wm))
            elif waff is Objekte.Fernkampfwaffe:
                wafNode.set('Typ','Fern')
                wafNode.set('rwnah',str(waff.rwnah))
                wafNode.set('rwfern',str(waff.rwfern))
                wafNode.set('lz',str(waff.lz))
        ausrüst = etree.SubElement(aus,'Ausrüstung')
        for ausr in self.ausrüstung:
            etree.SubElement(ausrüst,'Ausrüstungsstück').text = ausr
        #Sechster Block
        üfer = etree.SubElement(root,'Übernatürliche-Fertigkeiten')
        for fert in self.übernatürlicheFertigkeiten:
            fertNode = etree.SubElement(üfer,'Übernatürliche-Fertigkeit')
            fertNode.set('name',self.fertigkeiten[fert].name)
            fertNode.set('wert',str(self.fertigkeiten[fert].wert))
            talentNode = etree.SubElement(fertNode,'Talente')
            for talent in self.fertigkeiten[fert].gekaufteTalente:
                etree.SubElement(talentNode,'Talent').set('name',talent.name)
        #Siebter Block
        epn = etree.SubElement(root,'Erfahrung')
        etree.SubElement(epn,'EPtotal').text = str(self.EPtotal)
        etree.SubElement(epn,'EPspent').text = str(self.EPspent)
        
        #Write XML to file
        doc = etree.ElementTree(root)
        with open(filename,'wb') as file:
            file.seek(0)
            file.truncate()
            doc.write(file, encoding='UTF-8', pretty_print=True)
            file.truncate()

    def xmlLesen(self,filename):
        '''Läd ein Charakter-Objekt aus einer XML Datei, deren Dateiname inklusive Pfad als Argument übergeben wird'''
        #Alles bisherige löschen
        self.__init__()
        root = etree.parse(filename).getroot()
        #Erster Block
        alg = root.find('AllgemeineInfos')
        self.name = alg.find('name').text
        self.rasse = alg.find('rasse').text
        self.status = int(alg.find('status').text)
        self.kurzbeschreibung = alg.find('kurzbeschreibung').text
        self.schips = int(alg.find('schips').text)
        self.finanzen = int(alg.find('finanzen').text)
        for eig in alg.findall('eigenheiten/*'):
            self.eigenheiten.append(eig.text)
        #Zweiter Block
        for atr in root.findall('Attribute/*'):
            self.attribute[atr.tag].wert = int(atr.text)
            self.attribute[atr.tag].aktualisieren()
        #Dritter Block
        for vor in root.findall('Vorteile/*'):
            self.vorteile.append(vor.text)
        #Vierter Block
        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            fert = Fertigkeiten.Fertigkeit()
            fert.name = fer.attrib['name']
            fert.wert = int(fer.attrib)
            for tal in fer.findall('Talente/Talent'):
                fert.gekaufteTalente.append(tal.attrib['name'])
            #TODO: Fertigkeit aus Datenbank laden
            fert.aktualisieren()
            self.fertigkeiten.update({fert.name: fert})
        for fer in root.findall('Fertigkeiten/Freie-Fertigkeit'):
            fert = Fertigkeiten.FreieFertigkeit()            
            fert.name = fer.attrib['name']
            fert.wert = int(fer.attrib['wert'])
            fert.aktualisieren()
            self.freieFertigkeiten.append(fert)
        #Fünfter Block
        for rüs in root.findall('Objekte/Rüstungen/Rüstung'):
            rüst = Objekte.Rüstung()
            rüst.name = rüs.attrib['name']
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = eval(rüs.attrib['rs'])
            self.rüstung.append(rüst)
        for waf in root.findall('Objekte/Waffen/Waffe'):
            if waf.attrib['Typ'] is 'Nah':
                waff = Objekte.Nahkampfwaffe()
                waff.rw = int(waf.attrib['rw'])
                waff.wm = int(waf.attrib['wm'])
            else:
                waff = Objekte.Fernkampfwaffe()
                waff.rwnah = int(waf.attrib['rwnah'])
                waff.rwfern = int(waf.attrib['rwfern'])
                waff.lz = int(waf.attrib['lz'])
            waff.name = waf.attrib['name']
            waff.W6 = int(waf.attrib['W6'])
            waff.plus = int(waf.attrib['plus'])
            waff.eigenschaften = waf.attrib['eigenschaften']
            waff.härte = int(waf.attrib['härte'])
            self.waffen.append(waff)
        for aus in root.findall('Objekte/Ausrüstung/Ausrüstungsstück'):
            self.ausrüstung.append(aus.text)
        #Sechster Block 
        for fer in root.findall('Übernatürliche-Fertigkeiten/Übernatürliche-Fertigkeit'):
            fert = Fertigkeiten.Fertigkeit()
            fert.name = fer.attrib['name']
            fert.wert = int(fer.attrib)
            for tal in fer.findall('Talente/Talent'):
                fert.gekaufteTalente.append(tal.attrib['name'])
            #TODO: Fertigkeit aus Datenbank laden
            fert.aktualisieren()
            self.übernatürlicheFertigkeiten.update({fert.name: fert})
        #Siebter Block
        self.EPtotal = int(root.find('Erfahrung/EPtotal').text)
        self.EPspent = int(root.find('Erfahrung/EPspent').text)