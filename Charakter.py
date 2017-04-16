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

        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        self.fertigkeiten = copy.deepcopy(Wolke.DB.fertigkeiten)
        self.freieFertigkeiten = []

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
            self.mr += self.attribute['MU'].wert/2
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
            if Wolke.DB.vorteile[vor].kosten != -1:
                spent += Wolke.DB.vorteile[vor].kosten
        #Vierter Block: Fertigkeiten und Freie Fertigkeiten
        paidTalents = []
        for fer in self.fertigkeiten:
            spent += sum(range(self.fertigkeiten[fer].wert+1))*self.fertigkeiten[fer].steigerungsfaktor
            skip = False
            for tal in self.fertigkeiten[fer].gekaufteTalente:
                if fer == "Gebräuche" and not skip:
                    skip = True
                    continue
                if tal in paidTalents:
                    continue
                paidTalents.append(tal)
                if Wolke.DB.talente[tal].kosten != -1:
                    spent += Wolke.DB.talente[tal].kosten
                elif Wolke.DB.talente[tal].verbilligt:
                    spent += 10*self.fertigkeiten[fer].steigerungsfaktor
                else:
                    spent += 20*self.fertigkeiten[fer].steigerungsfaktor
        for fer in self.freieFertigkeiten:
            if fer.name != "Muttersprache":
                spent += Definitionen.FreieFertigkeitKosten[fer.wert-1]
        #Fünfter Block ist gratis
        #Sechster Block: Übernatürliches
        for fer in self.übernatürlicheFertigkeiten:
            spent += sum(range(self.übernatürlicheFertigkeiten[fer].wert+1))*self.übernatürlicheFertigkeiten[fer].steigerungsfaktor
            for tal in self.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                if tal in paidTalents:
                    continue
                paidTalents.append(tal)
                if Wolke.DB.talente[tal].kosten != -1:
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
        remove = []
        for vor in self.vorteile:
            if not self.voraussetzungenPrüfen(Wolke.DB.vorteile[vor].voraussetzungen):
                remove.append(vor)
        for el in remove:
            self.vorteile.remove(el)

    def updateFerts(self):
        remove = []
        self.höchsteKampfF = -1
        for fert in self.fertigkeiten:
            if not self.voraussetzungenPrüfen(self.fertigkeiten[fert].voraussetzungen):
                remove.append(fert)
                continue
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
        for el in remove:
            self.fertigkeiten.pop(el,None)
        remove = []
        for fert in self.übernatürlicheFertigkeiten:
            if not self.voraussetzungenPrüfen(self.übernatürlicheFertigkeiten[fert].voraussetzungen):
                remove.append(fert)
                continue
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
        for el in remove:
            self.übernatürlicheFertigkeiten.pop(el,None)

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
            etree.SubElement(vor,'Vorteil').text = vort
        #Vierter Block
        fer = etree.SubElement(root,'Fertigkeiten')
        for fert in self.fertigkeiten:
            fertNode = etree.SubElement(fer,'Fertigkeit')
            fertNode.set('name',self.fertigkeiten[fert].name)
            fertNode.set('wert',str(self.fertigkeiten[fert].wert))
            talentNode = etree.SubElement(fertNode,'Talente')
            for talent in self.fertigkeiten[fert].gekaufteTalente:
                etree.SubElement(talentNode,'Talent').set('name',talent)
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
            if type(waff) is Objekte.Nahkampfwaffe:
                wafNode.set('typ','Nah')
                wafNode.set('rw',str(waff.rw))
                wafNode.set('wm',str(waff.wm))
            elif type(waff) is Objekte.Fernkampfwaffe:
                wafNode.set('typ','Fern')
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
            fertNode.set('name',self.übernatürlicheFertigkeiten[fert].name)
            fertNode.set('wert',str(self.übernatürlicheFertigkeiten[fert].wert))
            talentNode = etree.SubElement(fertNode,'Talente')
            for talent in self.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                etree.SubElement(talentNode,'Talent').set('name',talent)
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
        for ene in root.findall('Energien/AsP'):
            self.asp.wert = int(ene.attrib['wert'])
        for ene in root.findall('Energien/KaP'):
            self.kap.wert = int(ene.attrib['wert'])
        #Dritter Block
        for vor in root.findall('Vorteile/*'):
            self.vorteile.append(vor.text)
        #Vierter Block
        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            nam = fer.attrib['name']
            fert = Wolke.DB.fertigkeiten[nam].__deepcopy__()
            fert.wert = int(fer.attrib['wert'])
            for tal in fer.findall('Talente/Talent'):
                fert.gekaufteTalente.append(tal.attrib['name'])
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
            waff.haerte = int(waf.attrib['haerte'])
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
        for key in Definitionen.Attribute:
            fields[key] = self.attribute[key].wert
            fields[key + '2'] = self.attribute[key].probenwert    
        fields['Wundschwelle'] = self.ws
        fields['WS'] = self.ws
        fields['Magieresistenz'] = self.mr
        fields['Geschwindigkeit'] = self.gs
        fields['Schadensbonus'] = self.schadensbonus
        fields['Initiative'] = self.ini
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
            fields['Energie'] = "AsP"
            fields['EN'] = self.asp.wert + aspMod
            fields['Energieg'] = "gAsP"   
            fields['Text83'] = "0"
            fields['Energiem'] = "AsP"
        elif aspMod == 0 and kapMod > 0:
            fields['Energie'] = "KaP"
            fields['EN'] = self.kap.wert + kapMod
            fields['Energieg'] = "gKaP"   
            fields['Text83'] = "0"
            fields['Energiem'] = "KaP"
        # Wenn sowohl AsP als auch KaP vorhanden sind, muss der Spieler ran..
        trueBE = max(self.be-self.rüstungsgewöhnung,0)
        fields['DHm'] = max(self.dh - 2*trueBE,1)
        fields['GSm'] = max(self.gs-trueBE,1)
        wsmod = self.rsmod + self.ws
        if len(self.rüstung) > 0:    
            wsmod += int(sum(self.rüstung[0].rs)/6+0.5)
        fields['WSm'] = wsmod
                      
        return fields
    
    def pdfDritterBlock(self, fields):    
        sortV = self.vorteile.copy()
        for vort in sortV:
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
                        sortV.remove(basename+el)
                        fullenum += "," + el[1:]
                sortV.append(basename + " " + fullenum[1:])
        sortV = sorted(sortV, key=str.lower)
        for i in range(1,9):
            if len(sortV)<i: break
            fields['Vorteil' + str(i)] = sortV[i-1]
        for i in range(1,14):
            if len(sortV)-8<i: break
            fields['Weite' + str(i)] = sortV[i-1+8]
        return fields
    
    def pdfVierterBlock(self, fields):
        count = 1
        for el in self.freieFertigkeiten:
            if el.wert < 1 or el.wert > 3:
                continue
            resp = el.name + " "
            for i in range(el.wert):
                resp += "I"
            fields['Frei' + str(count)] = resp
            count += 1
        # Standardfertigkeiten
        #TODO: Weitere Fertigkeiten? 
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
                talStr += el2
            talStr = talStr[2:]
            fields[base + "TA"] = talStr
            fields[base + "PW"] = self.fertigkeiten[el].probenwert
            fields[base + "PWT"] = self.fertigkeiten[el].probenwertTalent
                  
        
        return fields
    
    def pdfFünfterBlock(self, fields):
        count = 0
        for el in self.rüstung:
            fields['Text53.' + str(count)] = el.name
            fields['Text55.' + str(count)] = int(sum(el.rs)/6+0.5)+self.rsmod
            fields['Text56.' + str(count)] = max(el.be-self.rüstungsgewöhnung,0)
            fields['Text57.' + str(count)] = int(sum(el.rs)/6+self.ws+0.5+self.rsmod)
            fields['Text58.' + str(count)] = el.rs[0]+self.rsmod
            fields['Text59.' + str(count)] = el.rs[1]+self.rsmod
            fields['Text60.' + str(count)] = el.rs[2]+self.rsmod
            fields['Text61.' + str(count)] = el.rs[3]+self.rsmod
            fields['Text62.' + str(count)] = el.rs[4]+self.rsmod
            fields['Text63.' + str(count)] = el.rs[5]+self.rsmod
            if count >= 1:
                break
            count += 1
                      
        count = 0
        for el in self.waffen:
            fields['Text65.' + str(count)] = el.name
            sg = ""
            if el.plus >= 0:
                sg = "+"
            fields['Text66.' + str(count)] = str(el.W6) + "W6" + sg + str(el.plus)
            fields['Text69.' + str(count)] = str(el.haerte)
            fields['Text70.' + str(count)] = el.eigenschaften
            if type(el) == Objekte.Fernkampfwaffe:
                fields['Text67.' + str(count)] = str(el.rwnah) + "/" + str(el.rwfern)
                fields['Text68.' + str(count)] = str(el.lz)
            else:
                fields['Text67.' + str(count)] = str(el.rw)
                fields['Text68.' + str(count)] = str(el.wm)
            #TODO: Calculate AT*, PA*, TP*?
            if count >= 4:
                break
            count += 1
        
        count = 0
        te = 'Text76.'
        for el in self.ausrüstung:
            fields[te+str(count)] = el
            if count >= 12 and te == 'Text76.':
                count = -1
                te = 'Text77.'
            elif count >= 12:
                break
            count += 1
        return fields
    
    def pdfSechsterBlock(self, fields):
        count = 0
        for el in self.übernatürlicheFertigkeiten:
            if self.übernatürlicheFertigkeiten[el].wert <= 0:
                continue
            fields['Text86.'+str(count)] = self.übernatürlicheFertigkeiten[el].name
            fields['Text87.'+str(count)] = str(self.übernatürlicheFertigkeiten[el].steigerungsfaktor)       
            attr = str(self.übernatürlicheFertigkeiten[el].attribute[0]) + "/" + str(self.übernatürlicheFertigkeiten[el].attribute[1]) + "/" + str(self.übernatürlicheFertigkeiten[el].attribute[2])
            fields['Text88.'+str(count)] = attr
            fields['Text89.'+str(count)] = self.übernatürlicheFertigkeiten[el].basiswert       
            fields['Text90.'+str(count)] = self.übernatürlicheFertigkeiten[el].wert
            tal = ""
            for el2 in self.übernatürlicheFertigkeiten[el].gekaufteTalente:
                tal += ", "
                tal += el2
            tal = tal[2:]
            fields['Text91.'+str(count)] = tal
            fields['Text92.'+str(count)] = self.übernatürlicheFertigkeiten[el].probenwertTalent
            count += 1
            if count >= 7:
                break
        return fields
    
    def pdfSiebterBlock(self, fields):
        fields['ErfahGE'] = self.EPtotal
        fields['ErfahEI'] = self.EPspent
        fields['ErfahVE'] = self.EPtotal - self.EPspent
        return fields
    
