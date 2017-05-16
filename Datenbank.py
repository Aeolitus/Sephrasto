import Fertigkeiten
import lxml.etree as etree
from Hilfsmethoden import Hilfsmethoden
import os.path
import Objekte

class Datenbank():
    def __init__(self):
        self.vorteile = {}
        self.fertigkeiten = {}
        self.talente = {}
        self.übernatürlicheFertigkeiten = {}
        self.waffen = {}

        self.datei = 'datenbank.xml'
        self.root = None
        if os.path.isfile(self.datei):
            self.xmlLaden()
        elif os.path.isfile("regelbasis.xml"):
            self.datei = "regelbasis.xml"
            self.xmlLaden()

    def xmlSchreiben(self):
        
        self.root = etree.Element('Datenbank')
        
        #Vorteile
        for vort in self.vorteile:
            v = etree.SubElement(self.root,'Vorteil')
            v.set('name',self.vorteile[vort].name)
            v.set('kosten',str(self.vorteile[vort].kosten))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(self.vorteile[vort].voraussetzungen, None))
            v.set('nachkauf',self.vorteile[vort].nachkauf)
            v.set('typ', str(self.vorteile[vort].typ))
            v.set('variable', str(self.vorteile[vort].variable))
            v.text = self.vorteile[vort].text

        #Talente
        for tal in self.talente:
            v = etree.SubElement(self.root,'Talent')
            v.set('name',self.talente[tal].name)
            v.set('kosten',str(self.talente[tal].kosten))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(self.talente[tal].voraussetzungen, None))
            v.set('verbilligt',str(self.talente[tal].verbilligt))
            v.set('fertigkeiten',Hilfsmethoden.FertArray2Str(self.talente[tal].fertigkeiten, None))
            v.text = self.talente[tal].text
            
        #Fertigkeiten
        for fer in self.fertigkeiten:
            v = etree.SubElement(self.root,'Fertigkeit')
            v.set('name',self.fertigkeiten[fer].name)
            v.set('steigerungsfaktor',str(self.fertigkeiten[fer].steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(self.fertigkeiten[fer].voraussetzungen, None))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(self.fertigkeiten[fer].attribute))
            v.set('kampffertigkeit',str(self.fertigkeiten[fer].kampffertigkeit))
            v.text = self.fertigkeiten[fer].text

        for fer in self.übernatürlicheFertigkeiten:
            v = etree.SubElement(self.root,'Übernatürliche-Fertigkeit')
            v.set('name',self.übernatürlicheFertigkeiten[fer].name)
            v.set('steigerungsfaktor',str(self.übernatürlicheFertigkeiten[fer].steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(self.übernatürlicheFertigkeiten[fer].voraussetzungen, None))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(self.übernatürlicheFertigkeiten[fer].attribute))
            v.text = self.übernatürlicheFertigkeiten[fer].text
                                                    
        #Waffen
        for wa in self.waffen:
            w = etree.SubElement(self.root,'Waffe')
            w.set('name', self.waffen[wa].name)
            w.set('W6', str(self.waffen[wa].W6))
            w.set('plus', str(self.waffen[wa].plus))
            w.set('haerte', str(self.waffen[wa].haerte))
            w.text = self.waffen[wa].eigenschaften
            w.set('fertigkeit', self.waffen[wa].fertigkeit)
            w.set('talent', self.waffen[wa].talent)
            w.set('beid', str(self.waffen[wa].beid))
            w.set('pari', str(self.waffen[wa].pari))
            w.set('reit', str(self.waffen[wa].reit))
            w.set('schi', str(self.waffen[wa].schi))
            w.set('kraf', str(self.waffen[wa].kraf))
            w.set('schn', str(self.waffen[wa].schn))
            w.set('rw', str(self.waffen[wa].rw))
            if type(self.waffen[wa]) == Objekte.Fernkampfwaffe:
                w.set('lz', str(self.waffen[wa].lz))
                w.set('fk', '1')
            else:
                w.set('wm', str(self.waffen[wa].wm))
                w.set('fk', '0')

        #Write XML to file
        doc = etree.ElementTree(self.root)
        with open(self.datei,'wb') as file:
            file.seek(0)
            file.truncate()
            doc.write(file, encoding='UTF-8', pretty_print=True)
            file.truncate()
        
    def xmlLaden(self):
        self.root = etree.parse(self.datei).getroot()
        self.vorteile = {}
        self.fertigkeiten = {}
        self.talente = {}
        self.übernatürlicheFertigkeiten = {}
        self.waffen = {}
        
        #Vorteile
        for vort in self.root.findall('Vorteil'):
            V = Fertigkeiten.Vorteil()
            V.name = vort.get('name')
            V.kosten = int(vort.get('kosten'))
            V.voraussetzungen = Hilfsmethoden.VorStr2Array(vort.get('voraussetzungen'), None)
            V.nachkauf = vort.get('nachkauf')
            V.typ = int(vort.get('typ'))
            V.text = vort.text
            try:
                V.variable = int(vort.get('variable'))
            except:
                V.variable = 0
            self.vorteile.update({V.name: V})

        #Talente
        for tal in self.root.findall('Talent'):
            T = Fertigkeiten.Talent()
            T.name = tal.get('name')
            T.kosten = int(tal.get('kosten'))
            T.verbilligt = int(tal.get('verbilligt'))
            T.text = tal.text
            T.fertigkeiten = Hilfsmethoden.FertStr2Array(tal.get('fertigkeiten'), None)
            T.voraussetzungen = Hilfsmethoden.VorStr2Array(tal.get('voraussetzungen'), None)
            self.talente.update({T.name: T})
            
        #Fertigkeiten
        for fer in self.root.findall('Fertigkeit'):
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))
            F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'),None)
            F.kampffertigkeit = int(fer.get('kampffertigkeit'))
            self.fertigkeiten.update({F.name: F})

        for fer in self.root.findall('Übernatürliche-Fertigkeit'):
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))
            F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'),None)
            self.übernatürlicheFertigkeiten.update({F.name: F})
            
        #Waffen
        for wa in self.root.findall('Waffe'):
            if wa.get('fk') == '1':
                w = Objekte.Fernkampfwaffe()
                w.lz = int(wa.get('lz'))
            else:
                w = Objekte.Nahkampfwaffe()
                w.wm = int(wa.get('wm'))
            w.name = wa.get('name')
            w.rw = int(wa.get('rw'))
            w.W6 = int(wa.get('W6'))
            w.plus = int(wa.get('plus'))
            w.haerte = int(wa.get('haerte'))
            w.eigenschaften = wa.text
            w.fertigkeit = wa.get('fertigkeit')
            w.talent = wa.get('talent')
            w.beid = int(wa.get('beid'))
            w.pari = int(wa.get('pari'))
            w.reit = int(wa.get('reit'))
            w.schi = int(wa.get('schi'))
            w.kraf = int(wa.get('kraf'))
            w.schn = int(wa.get('schn'))
            self.waffen.update({w.name: w})