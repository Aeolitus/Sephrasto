import Definitionen
import Fertigkeiten
import Objekte
import lxml.etree as etree
import re
import pdf
import copy
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden

class Char():
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
        self.ws = -1
        self.mr = -1
        self.gs = -1
        self.dh = -1
        self.schadensbonus = -1
        self.ini = -1
        self.asp = Fertigkeiten.Energie()
        self.kap = Fertigkeiten.Energie()
        
        #Dritter Block: Vorteile, gespeichert als String
        self.vorteile = []
        self.vorteileVariable = {} #Contains Name: Cost

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
        self.übernatürlicheFertigkeiten = copy.deepcopy(Wolke.DB.übernatürlicheFertigkeiten)

        #Siebter Block: EP
        self.EPtotal = 0
        self.EPspent = 0

        #Achter Block: Flags etc
        self.höchsteKampfF = -1
        
        self.CharakterBogen = "Charakterbogen.pdf"

    def aktualisieren(self):
        '''Berechnet alle abgeleiteten Werte neu'''
        for key in Definitionen.Attribute:
            self.attribute[key].aktualisieren()
        self.ws = 4 + int(self.attribute['KO'].wert/4)
        if "Unverwüstlich" in self.vorteile:
            self.ws += 1
        self.mr = 4 + int(self.attribute['MU'].wert/4)
        if "Willensstark I" in self.vorteile:
            self.mr += 4
        if "Willensstark II" in self.vorteile:
            self.mr += 4
        if "Unbeugsamkeit" in self.vorteile:
            self.mr += round(self.attribute['MU'].wert/2+0.0001)
        self.gs = 4 + int(self.attribute['GE'].wert/4)
        if "Flink I" in self.vorteile:
            self.gs += 1
        if "Flink II" in self.vorteile:
            self.gs += 1
        self.ini = self.attribute['IN'].wert
        if "Kampfreflexe" in self.vorteile:
            self.ini += 4                                 
        self.schadensbonus = int(self.attribute['KK'].wert/4)
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
            spent += sum(range(self.attribute[key].wert+1))*self.attribute[key].steigerungsfaktor
        spent += sum(range(self.asp.wert+1))*self.asp.steigerungsfaktor
        spent += sum(range(self.kap.wert+1))*self.kap.steigerungsfaktor   
        #Dritter Block: Vorteile
        for vor in self.vorteile:
            if vor in self.vorteileVariable:
                spent += self.vorteileVariable[vor]
            elif Wolke.DB.vorteile[vor].kosten != -1:
                spent += Wolke.DB.vorteile[vor].kosten
        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        paidTalents = []
        for fer in self.fertigkeiten:
            spent += sum(range(self.fertigkeiten[fer].wert+1))*self.fertigkeiten[fer].steigerungsfaktor
            for tal in self.fertigkeiten[fer].gekaufteTalente:
                if tal in paidTalents:
                    continue
                if fer == "Gebräuche" and tal[11:] == self.heimat:
                    continue
                paidTalents.append(tal)
                if tal in self.talenteVariable:
                    spent += self.talenteVariable[tal]
                elif Wolke.DB.talente[tal].kosten != -1:
                    spent += Wolke.DB.talente[tal].kosten
                elif Wolke.DB.talente[tal].verbilligt:
                    spent += 10*self.fertigkeiten[fer].steigerungsfaktor
                else:
                    spent += 20*self.fertigkeiten[fer].steigerungsfaktor
        skip = False                                                 
        for fer in self.freieFertigkeiten:
            # Dont count Muttersprache
            if fer.wert == 3 and not skip:
                skip = True
                continue
            spent += Definitionen.FreieFertigkeitKosten[fer.wert-1]
        #Fünfter Block ist gratis
        #Sechster Block: Übernatürliches
        for fer in self.übernatürlicheFertigkeiten:
            spent += sum(range(self.übernatürlicheFertigkeiten[fer].wert+1))*self.übernatürlicheFertigkeiten[fer].steigerungsfaktor
            for tal in self.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                if tal in paidTalents:
                    continue
                paidTalents.append(tal)
                if tal in self.talenteVariable:
                    spent += self.talenteVariable[tal]
                elif Wolke.DB.talente[tal].kosten != -1:
                    spent += Wolke.DB.talente[tal].kosten
                elif Wolke.DB.talente[tal].verbilligt:
                    spent += 10*self.übernatürlicheFertigkeiten[fer].steigerungsfaktor
                else:
                    spent += 20*self.übernatürlicheFertigkeiten[fer].steigerungsfaktor
        #Siebter Block ist gratis
        #Achter Block: Fix für höchste Kampffertigkeit
        spent += max(0,2*sum(range(self.höchsteKampfF+1)))
        #Store
        self.EPspent = spent

    def updateVorts(self):
        while True:
            contFlag = True
            remove = []
            for vor in self.vorteile:
                if not self.voraussetzungenPrüfen(Wolke.DB.vorteile[vor].voraussetzungen):
                    remove.append(vor)
                    contFlag = False
            for el in remove:
                self.vorteile.remove(el)
            if contFlag:
                break

    def updateFerts(self):
        # Remover 
        while True:
            remove = []
            contFlag = True
            for fert in self.fertigkeiten:
                if not self.voraussetzungenPrüfen(self.fertigkeiten[fert].voraussetzungen):
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
                if not self.voraussetzungenPrüfen(self.übernatürlicheFertigkeiten[fert].voraussetzungen):
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
            if self.fertigkeiten[fert].kampffertigkeit and self.fertigkeiten[fert].wert > self.höchsteKampfF:
                self.höchsteKampfF = self.fertigkeiten[fert].wert
            for tal in self.fertigkeiten[fert].gekaufteTalente:
                if not self.voraussetzungenPrüfen(Wolke.DB.talente[tal].voraussetzungen):
                    self.fertigkeiten[fert].gekaufteTalente.remove(tal)
                else:
                    for el in self.fertigkeiten[fert].gekaufteTalente:
                        for f in Wolke.DB.talente[el].fertigkeiten:
                            if f in self.fertigkeiten:
                                if el not in self.fertigkeiten[f].gekaufteTalente:
                                    self.fertigkeiten[f].gekaufteTalente.append(el)
        for fert in self.übernatürlicheFertigkeiten:
            self.übernatürlicheFertigkeiten[fert].aktualisieren()
            if self.übernatürlicheFertigkeiten[fert].wert > self.übernatürlicheFertigkeiten[fert].maxWert:
                self.übernatürlicheFertigkeiten[fert].wert = self.übernatürlicheFertigkeiten[fert].maxWert
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
        etree.SubElement(sub,'heimat').text = self.heimat
        eigs = etree.SubElement(sub,'eigenheiten')
        for eigenh in self.eigenheiten:
            etree.SubElement(eigs,'Eigenheit').text = eigenh
        #Zweiter Block - abgeleitete nicht notwendig da automatisch neu berechnet
        atr = etree.SubElement(root,'Attribute')
        for attr in self.attribute:
            etree.SubElement(atr,attr).text = str(self.attribute[attr].wert)
        en = etree.SubElement(root,'Energien')
        etree.SubElement(en,'AsP').set('wert',str(self.asp.wert))
        etree.SubElement(en,'KaP').set('wert',str(self.kap.wert))
        #Dritter Block    
        vor = etree.SubElement(root,'Vorteile')
        for vort in self.vorteile:
            v = etree.SubElement(vor,'Vorteil')
            v.text = vort
            if vort in self.vorteileVariable:
                v.set('variable',str(self.vorteileVariable[vort]))
            else:
                v.set('variable','-1')
        #Vierter Block
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
            rüsNode.set('rs',Hilfsmethoden.RsArray2Str(rüst.rs))
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
        ausrüst = etree.SubElement(aus,'Ausrüstung')
        for ausr in self.ausrüstung:
            etree.SubElement(ausrüst,'Ausrüstungsstück').text = ausr
        #Sechster Block
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
        tmp = alg.find('heimat')
        if tmp is None: 
            self.heimat = 'Mittelreich'
        else:
            self.heimat = tmp.text
        for eig in alg.findall('eigenheiten/*'):
            self.eigenheiten.append(eig.text)
        #Zweiter Block
        for atr in root.findall('Attribute/*'):
            self.attribute[atr.tag].wert = int(atr.text)
            self.attribute[atr.tag].aktualisieren()
        for ene in root.findall('Energien/AsP'):
            self.asp.wert = int(ene.attrib['wert'])
        for ene in root.findall('Energien/KaP'):
            self.kap.wert = int(ene.attrib['wert'])
        #Dritter Block
        for vor in root.findall('Vorteile/*'):
            self.vorteile.append(vor.text)
            var = int(vor.get('variable'))
            if var != -1:
                self.vorteileVariable[vor.text] = var
        #Vierter Block
        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            nam = fer.attrib['name']
            fert = Wolke.DB.fertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            for tal in fer.findall('Talente/Talent'):
                fert.gekaufteTalente.append(tal.attrib['name'])
                if tal.attrib['variable'] != '-1':
                    self.talenteVariable[tal] = int(tal.attrib['variable'])
            fert.aktualisieren()
            self.fertigkeiten.update({fert.name: fert})
        for fer in root.findall('Fertigkeiten/Freie-Fertigkeit'):
            fert = Fertigkeiten.FreieFertigkeit()            
            fert.name = fer.attrib['name']
            fert.wert = int(fer.attrib['wert'])
            self.freieFertigkeiten.append(fert)
        #Fünfter Block
        for rüs in root.findall('Objekte/Rüstungen/Rüstung'):
            rüst = Objekte.Ruestung()
            rüst.name = rüs.attrib['name']
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = Hilfsmethoden.RsStr2Array(rüs.attrib['rs'])
            self.rüstung.append(rüst)
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
        for aus in root.findall('Objekte/Ausrüstung/Ausrüstungsstück'):
            self.ausrüstung.append(aus.text)
        #Sechster Block 
        for fer in root.findall('Übernatürliche-Fertigkeiten/Übernatürliche-Fertigkeit'):
            nam = fer.attrib['name']
            fert = Wolke.DB.übernatürlicheFertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            for tal in fer.findall('Talente/Talent'):
                fert.gekaufteTalente.append(tal.attrib['name'])
                if tal.attrib['variable'] != '-1':
                    self.talenteVariable[tal.attrib['name']] = int(tal.attrib['variable'])
            fert.aktualisieren()
            self.übernatürlicheFertigkeiten.update({fert.name: fert})
        #Siebter Block
        self.EPtotal = int(root.find('Erfahrung/EPtotal').text)
        self.EPspent = int(root.find('Erfahrung/EPspent').text)
    
    def pdfErstellen(self, filename):
        self.aktualisieren()
        fields = pdf.get_fields(self.CharakterBogen)
        fields = self.pdfErsterBlock(fields)
        fields = self.pdfZweiterBlock(fields)
        fields = self.pdfDritterBlock(fields)
        fields = self.pdfVierterBlock(fields)
        fields = self.pdfFünfterBlock(fields)
        fields = self.pdfSechsterBlock(fields)
        fields = self.pdfSiebterBlock(fields)
        
        #PDF erstellen - Felder bleiben bearbeitbar
        pdf.write_pdf(self.CharakterBogen, fields, filename, False)
    
    def pdfErsterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 1")
        fields['Name'] = self.name
        fields['Rasse'] = self.rasse
        fields['Statu'] = Definitionen.Statusse[self.status]
        fields['Kurzb'] = self.kurzbeschreibung
        glMod = 0
        if "Glück I" in self.vorteile:
            glMod += 1
        if "Glück II" in self.vorteile:
            glMod += 1
        fields['Schip'] = 4 + glMod
        fields['Schipm'] = self.schips + glMod
        # Erste Acht Eigenheiten
        count = 0;
        eigFields = [1, 5, 2, 6, 3, 7, 4, 8]
        for el in self.eigenheiten:
            fields['Eigen' + str(eigFields[count])] = el
            if count == 8:
                break
            count += 1
        return fields
    
    def pdfZweiterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 2")
        for key in Definitionen.Attribute:
            fields[key] = self.attribute[key].wert
            fields[key + '2'] = self.attribute[key].probenwert    
            fields[key + '3'] = self.attribute[key].probenwert    
        fields['Wundschwelle'] = self.ws
        fields['WS'] = self.ws
        fields['Magieresistenz'] = self.mr
        fields['Geschwindigkeit'] = self.gs
        fields['Schadensbonus'] = self.schadensbonus
        fields['Initiative'] = self.ini
        fields['INIm'] = self.ini
        aspMod = 0
        if "Zauberer I" in self.vorteile:
            aspMod += 8
        if "Zauberer II" in self.vorteile:
            aspMod += 8
        if "Zauberer III" in self.vorteile:
            aspMod += 8
        if "Zauberer IV" in self.vorteile:
            aspMod += 8
        if "Gefäß der Sterne" in self.vorteile:
            aspMod += self.attribute['CH']+4
        if aspMod > 0:    
            fields['Astralenergie'] = self.asp.wert + aspMod    
        kapMod = 0
        if "Geweiht I" in self.vorteile:
            kapMod += 8
        if "Geweiht II" in self.vorteile:
            kapMod += 8
        if "Geweiht III" in self.vorteile:
            kapMod += 8
        if "Geweiht IV" in self.vorteile:
            kapMod += 8
        if kapMod > 0:
            fields['Karmaenergie'] = self.kap.wert + kapMod
        if aspMod > 0 and kapMod == 0:
            #fields['Energie'] = "AsP"
            fields['EN'] = self.asp.wert + aspMod
            #fields['Energieg'] = "gAsP"   
            fields['gEN'] = "0"
            #fields['Energiem'] = "AsP"
        elif aspMod == 0 and kapMod > 0:
            #fields['Energie'] = "KaP"
            fields['EN'] = self.kap.wert + kapMod
            #fields['Energieg'] = "gKaP"   
            fields['gEN'] = "0"
            #fields['Energiem'] = "KaP"
        # Wenn sowohl AsP als auch KaP vorhanden sind, muss der Spieler ran..
        trueBE = max(self.be-self.rüstungsgewöhnung,0)
        fields['DHm'] = max(self.dh - 2*trueBE,1)
        fields['GSm'] = max(self.gs-trueBE,1)
        wsmod = self.rsmod + self.ws
        if len(self.rüstung) > 0:    
            wsmod += int(sum(self.rüstung[0].rs)/6+0.5+0.0001)
        fields['WSm'] = wsmod
                      
        return fields
    
    def pdfDritterBlock(self, fields):    
        if Wolke.Debug:
            print("PDF Block 3")
        sortV = self.vorteile.copy()
        typeDict = {}
        assembled = []
        removed = []
        # Collect a list of Vorteils, where different levels of the same are
        # combined into one entry and the type of Vorteil is preserved
        for vort in sortV:
            if vort in removed:
                continue
            flag = False
            if vort.endswith(" I"):
                basename = vort[:-2]
                flag = True
            elif vort.endswith(" II") or vort.endswith(" IV"):
                basename = vort[:-3]
                flag = True
            elif vort.endswith(" III"):
                basename = vort[:-4]
                flag = True
            if flag:
                fullset = [" I", " II", " III", " IV"]
                fullenum = ""
                for el in fullset:
                    if basename+el in sortV:
                        removed.append(basename+el)
                        fullenum += "," + el[1:]
                vname = basename + " " + fullenum[1:]
                #sortV.append(vname)
                typeDict[vname] = Wolke.DB.vorteile[vort].typ
                assembled.append(vname)
                if "Zauberer" in vname or "Geweiht" in vname:
                    typeDict[vname] = 4
            else:
                typeDict[vort] = Wolke.DB.vorteile[vort].typ
        for el in removed:
            if el in sortV:
                sortV.remove(el)
        for el in assembled:
            sortV.append(el)
        removed = []
        added = []
        
        # Add the cost for Vorteils with variable costs
        for el in sortV: #This is only going to be general Vorteile anyways, so type doesnt matter
            if el in self.vorteileVariable:
                removed.append(el)
                nname = el + " (" + str(self.vorteileVariable[el]) + " EP)"
                added.append(nname)
                typeDict[nname] = typeDict[el]
        for el in removed:
            sortV.remove(el)
        for el in added:
            sortV.append(el)
            
        # Sort and split the Vorteile into the three categories
        sortV = sorted(sortV, key=str.lower)       
        tmpVorts = [el for el in sortV if typeDict[el] < 2]
        tmpKampf = [el for el in sortV if (typeDict[el] < 4 and typeDict[el] >= 2)]
        tmpUeber = [el for el in sortV if typeDict[el] >= 4]
        tmpOverflow = []
        
        # Fill up categories that are not full with the other categories overflow
        if len(tmpVorts) > 8:
            tmpOverflow.extend(tmpVorts[8:])
            tmpVorts = tmpVorts[:8]
        if len(tmpKampf) > 16:
            tmpOverflow.extend(tmpKampf[16:])
            tmpKampf = tmpKampf[:16]
        if len(tmpUeber) > 12:
            tmpOverflow.extend(tmpUeber[12:])
            tmpUeber = tmpUeber[:12]
        counter = 0
        for i in range(len(tmpVorts),8):
            if len(tmpOverflow) > counter:
                tmpVorts.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(tmpKampf),16):
            if len(tmpOverflow) > counter:
                tmpKampf.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(tmpUeber),12):
            if len(tmpOverflow) > counter:
                tmpUeber.append(tmpOverflow[counter])
                counter += 1
                
        # Fill fields
        for i in range(1,9):
            if i < len(tmpVorts):
                fields['Vorteil' + str(i)] = tmpVorts[i-1]
        for i in range(1,9):
            if i < len(tmpKampf):
                fields['Kampfvorteil' + str(i)] = tmpKampf[i-1]
        for i in range(1,9):
            if i < len(tmpUeber):
                fields['Uebervorteil' + str(i)] = tmpUeber[i-1]
        
        return fields
    
    def pdfVierterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 4")
        # Freie Fertigkeiten
        count = 1
        for el in self.freieFertigkeiten:
            if el.wert < 1 or el.wert > 3:
                continue
            resp = el.name + " "
            for i in range(el.wert):
                resp += "I"
            fields['Frei' + str(count)] = resp
            count += 1
            if count > 12:
                break
            
        # Standardfertigkeiten
        for el in Definitionen.StandardFerts:
            if el not in self.fertigkeiten:
                continue
            base = el[0:5]
            # Fix Umlaute
            if el == "Gebräuche":
                base = "Gebra"
            elif el == "Überleben":
                base = "Ueber"
            fields[base + "BA"] = self.fertigkeiten[el].basiswert
            fields[base + "FW"] = self.fertigkeiten[el].wert
            talStr = ""
            for el2 in self.fertigkeiten[el].gekaufteTalente:
                talStr += ", "
                if el2.startswith("Gebräuche: "):
                    talStr += el2[11:]
                elif el2.startswith("Mythen: "):
                    talStr += el2[8:]
                elif el2.startswith("Überleben: "):
                    talStr += el2[11:]
                else:
                    talStr += el2
                if el2 in self.talenteVariable:
                    talStr += " (" + str(self.talenteVariable[el2]) + " EP)"
            talStr = talStr[2:]
            fields[base + "TA"] = talStr
            fields[base + "PW"] = self.fertigkeiten[el].probenwert
            fields[base + "PWT"] = self.fertigkeiten[el].probenwertTalent
                  
        # Nonstandard Ferts
        count = 1
        for el in self.fertigkeiten:
            if el in Definitionen.StandardFerts:
                continue
            if count > 2:
                continue
            fields['Indi' + str(count) + 'NA'] = self.fertigkeiten[el].name
            fields['Indi' + str(count) + 'FA'] = self.fertigkeiten[el].steigerungsfaktor
            fields['Indi' + str(count) + 'AT'] = \
                   self.fertigkeiten[el].attribute[0] + '/' + \
                   self.fertigkeiten[el].attribute[1] + '/' + \
                   self.fertigkeiten[el].attribute[2]
            fields['Indi' + str(count) + 'BA'] = self.fertigkeiten[el].basiswert
            fields['Indi' + str(count) + 'FW'] = self.fertigkeiten[el].wert
            fields['Indi' + str(count) + 'PW'] = self.fertigkeiten[el].probenwert
            fields['Indi' + str(count) + 'PWT'] = self.fertigkeiten[el].probenwertTalent
            talStr = ""
            for el2 in self.fertigkeiten[el].gekaufteTalente:
                talStr += ", "
                talStr += el2
                if el2 in self.talenteVariable:
                    talStr += " (" + str(self.talenteVariable[el2]) + " EP)"
            talStr = talStr[2:]
            fields['Indi' + str(count) + 'TA'] = talStr
            count += 1
        return fields
    
    def pdfFünfterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 5")
        # Fill three rows of Rüstung
        count = 1
        for el in self.rüstung:
            base = 'Ruest' + str(count)
            fields[base + 'NA'] = el.name
            fields[base + 'RS'] = int(sum(el.rs)/6+0.5+0.0001)+self.rsmod
            fields[base + 'BE'] = max(el.be-self.rüstungsgewöhnung,0)
            fields[base + 'WS'] = int(sum(el.rs)/6+self.ws+0.5+self.rsmod+0.0001)
            base += 'RS'
            fields[base + 'Bein'] = el.rs[0]+self.rsmod
            fields[base + 'lArm'] = el.rs[1]+self.rsmod
            fields[base + 'rArm'] = el.rs[2]+self.rsmod
            fields[base + 'Bauch'] = el.rs[3]+self.rsmod
            fields[base + 'Brust'] = el.rs[4]+self.rsmod
            fields[base + 'Kopf'] = el.rs[5]+self.rsmod
            count += 1
            if count > 3:
                break
            
        # Fill eight rows of weapons
        count = 1
        for el in self.waffen:
            base = 'Waffe' + str(count)
            fields[base + 'NA'] = el.name
            sg = ""
            if el.plus >= 0:
                sg = "+"
            fields[base + 'TP'] = str(el.W6) + "W6" + sg + str(el.plus)
            fields[base + 'HA'] = str(el.haerte)
            fields[base + 'EI'] = el.eigenschaften
            fields[base + 'RW'] = str(el.rw)
            if type(el) == Objekte.Fernkampfwaffe:
                fields[base + 'WM'] = str(el.lz)
            else:
                fields[base + 'WM'] = str(el.wm)
                
            # Calculate modifiers for AT, PA, TP from Kampfstil
            if el.name in Wolke.DB.waffen:    
                fertig = Wolke.DB.waffen[el.name].fertigkeit
                tale = Wolke.DB.waffen[el.name].talent
            else:
                fertig = ""
                tale = ""
            if fertig in Wolke.Char.fertigkeiten:
                if tale in Wolke.Char.fertigkeiten[fertig].gekaufteTalente:
                    bwert = Wolke.Char.fertigkeiten[fertig].probenwertTalent
                else:
                    bwert = Wolke.Char.fertigkeiten[fertig].probenwert
                at = bwert
                vt = bwert
                sp = 0
                # 0 is no Kampfstil, no Effect
                # 1 is Beidhändig
                if el.kampfstil == 1:
                    levelC = 0
                    for vor in self.vorteile:
                        if Definitionen.Kampfstile[1] in vor:
                            levelC += 1
                    at += min(levelC,3)
                # 2 is Parierwaffenkampf which does nothing
                # 3 is Reiterkampf
                elif el.kampfstil == 3:
                    levelC = 0
                    for vor in self.vorteile:
                        if Definitionen.Kampfstile[3] in vor:
                            levelC += 1
                    at += min(levelC,3)
                    vt += min(levelC,3)
                    sp += min(levelC,3)
                # 4 is Schildkampf
                elif el.kampfstil == 4:
                    levelC = 0
                    for vor in self.vorteile:
                        if Definitionen.Kampfstile[4] in vor:
                            levelC += 1
                    vt += min(levelC,3)
                # 5 is Kraftvoller Kampf
                elif el.kampfstil == 5:
                    levelC = 0
                    for vor in self.vorteile:
                        if Definitionen.Kampfstile[5] in vor:
                            levelC += 1
                    sp += min(levelC,3)
                # 6 is Schneller Kampf
                elif el.kampfstil == 6:
                    levelC = 0
                    for vor in self.vorteile:
                        if Definitionen.Kampfstile[6] in vor:
                            levelC += 1
                    at += min(levelC,3)
                
                if "Kopflastig" in el.eigenschaften:
                    sp += self.schadensbonus*2
                else:
                    sp += self.schadensbonus
                fields[base + 'ATm'] = at
                fields[base + 'VTm'] = vt
                sg = ""
                if el.plus+sp >= 0:
                    sg = "+"
                fields[base + 'TPm'] = str(el.W6) + "W6" + sg + str(el.plus+sp)
            
            if count >= 8:
                break
            count += 1
        
        # Fill 20 Cells of Ausrüstung
        count = 1
        for el in self.ausrüstung:
            fields['Ausruestung' + str(count)] = el
            if count >= 20:
                break
            count += 1
        return fields
    
    def pdfSechsterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 6")
            
        addedTals = {} # Name: (PWT, base)
            
        countF = 1
        countT = 1
        for f in self.übernatürlicheFertigkeiten:
            if self.übernatürlicheFertigkeiten[f].wert <= 0:
                continue
            fe = self.übernatürlicheFertigkeiten[f]
            
            if countF < 13:
                # Fill Fertigkeitsslots
                base = 'Ueberfer' + str(countF)
                fields[base + 'NA'] = fe.name
                fields[base + 'FA'] = fe.steigerungsfaktor
                fields[base + 'AT'] = fe.attribute[0] + '/' + \
                      fe.attribute[1] + '/' + fe.attribute[2]
                fields[base + 'BA'] = fe.basiswert
                fields[base + 'FW'] = fe.wert
                fields[base + 'PW'] = fe.probenwertTalent
                countF += 1
            
            # Fill Talente
            for t in fe.gekaufteTalente:
                if countT < 30:
                    base = 'Uebertal' + str(countT)
                    mod = ""
                    if t in self.talenteVariable:
                        mod += " (" + str(self.talenteVariable[t]) + " EP)"
                    
                    if t+mod in addedTals:
                        if fe.probenwertTalent > addedTals[t+mod][0]:
                            fields[addedTals[t+mod][1] + 'PW'] = fe.probenwertTalent
                            addedTals[t+mod] = (fe.probenwertTalent,addedTals[t+mod][1])
                    else:
                        addedTals[t+mod] = (fe.probenwertTalent, base)
                        fields[base + 'NA'] = t + mod
                        fields[base + 'PW'] = fe.probenwertTalent
                        # Get Spellinfo from text
                        if t in Wolke.DB.talente:
                            txt = Wolke.DB.talente[t].text
                            res = re.findall('Vorbereitungszeit:(.*?)\n', txt, re.UNICODE)
                            if len(res) == 1:
                                fields[base + 'VO'] = res[0].strip()
                            res = re.findall('Reichweite:(.*?)\n', txt, re.UNICODE)
                            if len(res) == 1:
                                fields[base + 'RE'] = res[0].strip()
                            res = re.findall('Wirkungsdauer:(.*?)\n', txt, re.UNICODE)
                            if len(res) == 1:
                                fields[base + 'WD'] = res[0].strip()
                            res = re.findall('Kosten:(.*?)\n', txt, re.UNICODE)
                            if len(res) == 1:
                                fields[base + 'KO'] = res[0].strip()
                        countT += 1
                    
        return fields
    
    def pdfSiebterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 7")
        fields['ErfahGE'] = self.EPtotal
        fields['ErfahEI'] = self.EPspent
        fields['ErfahVE'] = self.EPtotal - self.EPspent
        return fields
    
