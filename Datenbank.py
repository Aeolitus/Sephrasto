import Fertigkeiten
import lxml.etree as etree

class Datenbank():
    def __init__(self):
        self.vorteile = {}
        self.fertigkeiten = {}
        self.talente = {}
        self.übernatürlicheFertigkeiten = {}

        self.datei = 'datenbank.xml'
        self.root = None
        self.xmlLaden()

    def xmlSchreiben(self):
        
        self.root = etree.Element('Datenbank')
        
        #Vorteile
        for vort in self.vorteile:
            v = etree.SubElement(self.root,'Vorteil')
            v.set('name',self.vorteile[vort].name)
            v.set('kosten',str(self.vorteile[vort].kosten))
            v.set('voraussetzungen',repr(self.vorteile[vort].voraussetzungen))
            v.set('nachkauf',self.vorteile[vort].nachkauf)
            v.text = self.vorteile[vort].text

        #Talente
        for tal in self.talente:
            v = etree.SubElement(self.root,'Talent')
            v.set('name',self.talente[tal].name)
            v.set('kosten',str(self.talente[tal].kosten))
            v.set('voraussetzungen',repr(self.talente[tal].voraussetzungen))
            v.set('verbilligt',str(self.talente[tal].verbilligt))
            v.set('fertigkeiten',repr(self.talente[tal].fertigkeiten))
            v.text = self.talente[tal].text
            
        #Fertigkeiten
        for fer in self.fertigkeiten:
            v = etree.SubElement(self.root,'Fertigkeit')
            v.set('name',self.fertigkeiten[fer].name)
            v.set('steigerungsfaktor',str(self.fertigkeiten[fer].steigerungsfaktor))
            v.set('voraussetzungen',repr(self.fertigkeiten[fer].voraussetzungen))
            v.set('attribute',repr(self.fertigkeiten[fer].attribute))
            v.text = self.fertigkeiten[fer].text

        for fer in self.übernatürlicheFertigkeiten:
            v = etree.SubElement(self.root,'Übernatürliche-Fertigkeit')
            v.set('name',self.übernatürlicheFertigkeiten[fer].name)
            v.set('steigerungsfaktor',str(self.übernatürlicheFertigkeiten[fer].steigerungsfaktor))
            v.set('voraussetzungen',repr(self.übernatürlicheFertigkeiten[fer].voraussetzungen))
            v.set('attribute',repr(self.übernatürlicheFertigkeiten[fer].attribute))
            v.text = self.übernatürlicheFertigkeiten[fer].text

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
        
        #Vorteile
        for vort in self.root.findall('Vorteil'):
            V = Fertigkeiten.Vorteil()
            V.name = vort.get('name')
            V.kosten = int(vort.get('kosten'))
            V.voraussetzungen = eval(vort.get('voraussetzungen'))
            V.nachkauf = vort.get('nachkauf')
            V.text = vort.text
            self.vorteile.update({V.name: V})

        #Talente
        for tal in self.root.findall('Talent'):
            T = Fertigkeiten.Talent()
            T.name = tal.get('name')
            T.kosten = int(tal.get('kosten'))
            T.verbilligt = int(tal.get('verbilligt'))
            T.text = tal.text
            T.fertigkeiten = eval(tal.get('fertigkeiten'))
            T.voraussetzungen = eval(tal.get('voraussetzungen'))
            self.talente.update({T.name: T})
            
        #Fertigkeiten
        for fer in self.root.findall('Fertigkeit'):
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text
            F.attribute = eval(fer.get('attribute'))
            F.voraussetzungen = eval(fer.get('voraussetzungen'))
            self.fertigkeiten.update({F.name: F})

        for fer in self.root.findall('Übernatürliche-Fertigkeit'):
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text
            F.attribute = eval(fer.get('attribute'))
            F.voraussetzungen = eval(fer.get('voraussetzungen'))
            self.übernatürlicheFertigkeiten.update({F.name: F})
            