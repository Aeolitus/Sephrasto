from Core.Attribut import AttributDefinition
from Core.AbgeleiteterWert import AbgeleiteterWertDefinition
from Core.Energie import EnergieDefinition
from Core.Fertigkeit import FertigkeitDefinition, UeberFertigkeitDefinition
from Core.FreieFertigkeit import FreieFertigkeitDefinition
from Core.Regel import Regel
from Core.Ruestung import RuestungDefinition
from Core.Talent import TalentDefinition
from Core.Vorteil import VorteilDefinition, VorteilLinkKategorie
from Core.Waffe import WaffeDefinition
from Core.Waffeneigenschaft import Waffeneigenschaft
from Core.DatenbankEinstellung import DatenbankEinstellung
import lxml.etree as etree
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException, WaffeneigenschaftException
import os.path
from Wolke import Wolke
import logging
from EventBus import EventBus
import re
from Migrationen import Migrationen

class Datenbank():
    def __init__(self):
        self.datei = None
        self.hausregelDatei = None
        self.enabledPlugins = []
        self.loadingErrors = []
        
    @property
    def hausregelnAnzeigeName(self):
        return os.path.basename(self.hausregelDatei) if self.hausregelDatei else "Keine"

    def xmlSchreiben(self, merge = False):
        root = etree.Element('Datenbank')
        
        versionXml = etree.SubElement(root, 'Version')
        versionXml.text = str(Migrationen.datenbankCodeVersion)
        etree.SubElement(root, 'Plugins').text = ",".join(self.enabledPlugins)

        #Attribute
        for attribut in self.attribute.values():
            if not merge and not self.isChangedOrNew(attribut): continue
            a = etree.SubElement(root, 'Attribut')
            a.set('name', attribut.name)
            a.set('anzeigename', attribut.anzeigename)
            a.set('steigerungsfaktor', str(attribut.steigerungsfaktor))
            a.set('sortorder', str(attribut.sortorder))
            a.text = attribut.text

        #Abgeleitete Werte
        for abgeleiteterWert in self.abgeleiteteWerte.values():
            if not merge and not self.isChangedOrNew(abgeleiteterWert): continue
            a = etree.SubElement(root, 'AbgeleiteterWert')
            a.set('name', abgeleiteterWert.name)
            a.set('anzeigename', abgeleiteterWert.anzeigename)
            a.set('anzeigen', "1" if abgeleiteterWert.anzeigen else "0")
            a.set('formel', abgeleiteterWert.formel)
            if abgeleiteterWert.script:
                a.set('script', abgeleiteterWert.script)
            if abgeleiteterWert.finalscript:
                a.set('finalscript', abgeleiteterWert.finalscript)
            a.set('sortorder', str(abgeleiteterWert.sortorder))
            a.text = abgeleiteterWert.text

        # Energien
        for energie in self.energien.values():
            if not merge and not self.isChangedOrNew(energie): continue
            a = etree.SubElement(root, 'Energie')
            a.set('name', energie.name)
            a.set('anzeigename', energie.anzeigename)
            a.set('steigerungsfaktor', str(energie.steigerungsfaktor))
            a.set('voraussetzungen', Hilfsmethoden.VorArray2Str(energie.voraussetzungen))
            a.set('sortorder', str(energie.sortorder))
            a.text = energie.text
            
        #Vorteile
        for vort in self.vorteile:
            vorteil = self.vorteile[vort]
            if not merge and not self.isChangedOrNew(vorteil): continue
            v = etree.SubElement(root,'Vorteil')
            v.set('name',vorteil.name)
            v.set('kosten',str(vorteil.kosten))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(vorteil.voraussetzungen))
            v.set('nachkauf',vorteil.nachkauf)
            v.set('typ', str(vorteil.typ))
            v.set('variableKosten', str(1 if vorteil.variableKosten else 0))
            v.set('kommentar', str(1 if vorteil.kommentarErlauben else 0))
            v.text = vorteil.text
            if vorteil.script:
                v.set('script', vorteil.script)
            if vorteil.scriptPrio != 0:
                v.set('scriptPrio', str(vorteil.scriptPrio))

            if not vorteil.cheatsheetAuflisten:
                v.set('csAuflisten', "0")
            if vorteil.cheatsheetBeschreibung:
                v.set('csBeschreibung', vorteil.cheatsheetBeschreibung)
            if vorteil.linkKategorie > 0:
                v.set('linkKategorie', str(vorteil.linkKategorie))
            if vorteil.linkElement:
                v.set('linkElement', vorteil.linkElement)
            if len(vorteil.querverweise) > 0:
                v.set('querverweise', " | ".join(vorteil.querverweise))
            if vorteil.info:
                v.set('info', vorteil.info)
            if vorteil.bedingungen:
                v.set('bedingungen', vorteil.bedingungen)

        #Talente
        for tal in self.talente:
            talent = self.talente[tal]
            if not merge and not self.isChangedOrNew(talent): continue
            v = etree.SubElement(root,'Talent')
            v.set('name',talent.name)
            if talent.spezialTalent:
                v.set('kosten',str(talent.kosten))
                v.set('spezialTyp',str(talent.spezialTyp))
            else:
                v.set('kosten',"-1")                
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(talent.voraussetzungen))
            v.set('verbilligt', "1" if talent.verbilligt else "0")
            v.set('fertigkeiten',Hilfsmethoden.FertArray2Str(talent.fertigkeiten, None))
            v.set('variableKosten', str(1 if talent.variableKosten else 0))
            v.set('kommentar', str(1 if talent.kommentarErlauben else 0))
            v.set('referenzbuch', str(talent.referenzBuch))
            v.set('referenzseite', str(talent.referenzSeite))
            v.text = talent.text
            if not talent.cheatsheetAuflisten:
                v.set('csAuflisten', "0")
            if talent.info:
                v.set('info', talent.info)
            
        #Fertigkeiten
        for fer in self.fertigkeiten:
            fertigkeit = self.fertigkeiten[fer]
            if not merge and not self.isChangedOrNew(fertigkeit): continue
            v = etree.SubElement(root,'Fertigkeit')
            v.set('name',fertigkeit.name)
            v.set('steigerungsfaktor',str(fertigkeit.steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(fertigkeit.attribute))
            v.set('kampffertigkeit',str(fertigkeit.kampffertigkeit))
            v.set('typ',str(fertigkeit.typ))
            v.text = fertigkeit.text

        for fer in self.übernatürlicheFertigkeiten:
            fertigkeit = self.übernatürlicheFertigkeiten[fer]
            if not merge and not self.isChangedOrNew(fertigkeit): continue
            v = etree.SubElement(root,'ÜbernatürlicheFertigkeit')
            v.set('name',fertigkeit.name)
            v.set('steigerungsfaktor',str(fertigkeit.steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(fertigkeit.attribute))
            v.set('typ',str(fertigkeit.typ))
            v.set('talentegruppieren',str(1 if fertigkeit.talenteGruppieren else 0))
            v.text = fertigkeit.text

        #Waffeneigenschaften
        for we in self.waffeneigenschaften:
            eigenschaft = self.waffeneigenschaften[we]
            if not merge and not self.isChangedOrNew(eigenschaft): continue
            w = etree.SubElement(root, 'Waffeneigenschaft')
            w.set('name', eigenschaft.name)
            if eigenschaft.script:
                w.set('script', eigenschaft.script)
            if eigenschaft.scriptPrio != 0:
                w.set('scriptPrio', str(eigenschaft.scriptPrio))
            w.text = eigenschaft.text

        #Waffen
        for wa in self.waffen:
            waffe = self.waffen[wa]
            if not merge and not self.isChangedOrNew(waffe): continue
            w = etree.SubElement(root,'Waffe')
            w.set('name', waffe.name)
            w.set('würfel', str(waffe.würfel))
            w.set('würfelSeiten', str(waffe.würfelSeiten))
            w.set('plus', str(waffe.plus))
            w.set('härte', str(waffe.härte))
            w.text = ", ".join(waffe.eigenschaften)
            w.set('fertigkeit', waffe.fertigkeit)
            w.set('talent', waffe.talent)
            w.set('kampfstile', ", ".join(waffe.kampfstile))
            w.set('rw', str(waffe.rw))
            w.set('wm', str(waffe.wm))
            if waffe.fernkampf:
                w.set('lz', str(waffe.lz))
                w.set('fk', '1')
            else:
                w.set('fk', '0')

        #Rüstungen
        for rue in self.rüstungen:
            ruestung = self.rüstungen[rue]
            if not merge and not self.isChangedOrNew(ruestung): continue
            r = etree.SubElement(root, 'Rüstung')
            r.set('name', ruestung.name)
            r.set('typ', str(ruestung.typ))
            r.set('system', str(ruestung.system))
            r.set('rsBeine', str(ruestung.rs[0]))
            r.set('rsLArm', str(ruestung.rs[1]))
            r.set('rsRArm', str(ruestung.rs[2]))
            r.set('rsBauch', str(ruestung.rs[3]))
            r.set('rsBrust', str(ruestung.rs[4]))
            r.set('rsKopf', str(ruestung.rs[5]))
            r.text = ruestung.text

        #Regeln
        for r in self.regeln:
            regel = self.regeln[r]
            if not merge and not self.isChangedOrNew(regel): continue
            regelNode = etree.SubElement(root, 'Regel')
            regelNode.set('name', regel.name)
            regelNode.set('typ', str(regel.typ))
            regelNode.set('voraussetzungen', Hilfsmethoden.VorArray2Str(regel.voraussetzungen))
            regelNode.set('probe', regel.probe)
            regelNode.text = regel.text
            
        #Freie Fertigkeiten
        for ff in self.freieFertigkeiten:
            fert = self.freieFertigkeiten[ff]
            if not merge and not self.isChangedOrNew(fert): continue
            f = etree.SubElement(root, 'FreieFertigkeit')
            f.set('name', fert.name)
            f.set('kategorie', fert.kategorie)
            f.set('voraussetzungen', Hilfsmethoden.VorArray2Str(fert.voraussetzungen))

        #Einstellungen
        for de in self.einstellungen:
            einstellung = self.einstellungen[de]
            if not merge and not self.isChangedOrNew(einstellung): continue
            e = etree.SubElement(root, 'Einstellung')
            e.set('name', einstellung.name)
            e.text = einstellung.text

        #Remove list
        if not merge:
            for type in self.referenceDB:
                for name in self.getRemoved(type):
                    r = etree.SubElement(root,'Remove')
                    r.set('name', name)
                    r.set('typ', type.__name__)

        root = EventBus.applyFilter("datenbank_xml_schreiben", root, { "datenbank" : self, "merge" : merge })

        #Write XML to file
        doc = etree.ElementTree(root)
        with open(self.hausregelDatei,'wb') as file:
            file.seek(0)
            file.truncate()
            doctype = """<!DOCTYPE xsl:stylesheet [
   <!ENTITY nbsp "&#160;">
]>"""
            doc.write(file, xml_declaration=True, encoding='UTF-8', pretty_print=True, doctype=doctype)
            file.truncate()

    def insertTable(self, type, table):
        self.tablesByType[type] = table
        self.referenceDB[type] = {}

    def loadElement(self, element, refDB = True, conflictCB = None):
        dbKey = element.__class__
        if refDB:
            self.referenceDB[dbKey][element.name] = element
        elif conflictCB and element.name in self.tablesByType[dbKey] and not element.deepequals(self.tablesByType[dbKey][element.name]):
            element = conflictCB(dbKey, self.tablesByType[dbKey][element.name], element)
        self.tablesByType[dbKey][element.name] = element

    def isNew(self, element):
        return element.name not in self.referenceDB[element.__class__]

    def isChanged(self, element):
        if self.isNew(element):
            return False
        return self.tablesByType[element.__class__][element.name] != self.referenceDB[element.__class__][element.name]

    def isChangedOrNew(self, element):
        if self.isNew(element):
            return True
        return self.tablesByType[element.__class__][element.name] != self.referenceDB[element.__class__][element.name]

    def isRemoved(self, element):
        return element.name not in self.tablesByType[element.__class__] and element.name in self.referenceDB[element.__class__]

    def getRemoved(self, type):
        return set(self.referenceDB[type].keys()) - set(self.tablesByType[type].keys())

    def isOverriddenByOther(self, element):
        return self.isChanged(element) and element == self.referenceDB[element.__class__][element.name]

    def xmlLaden(self, datei = os.path.join('Data', 'datenbank.xml'), hausregeln = None, isCharakterEditor = False):
        self.datei = datei
        self.hausregelDatei = None
        
        if hausregeln is not None:
            if os.path.isfile(hausregeln):
                self.hausregelDatei = hausregeln
            elif hausregeln and hausregeln != "Keine":
                tmp = os.path.join(Wolke.Settings['Pfad-Regeln'], hausregeln)
                if os.path.isfile(tmp):
                    self.hausregelDatei = tmp

        self.attribute = {}
        self.abgeleiteteWerte = {}
        self.energien = {}
        self.vorteile = {}
        self.fertigkeiten = {}
        self.talente = {}
        self.übernatürlicheFertigkeiten = {}
        self.waffen = {}
        self.rüstungen = {}
        self.regeln = {}
        self.waffeneigenschaften = {}
        self.freieFertigkeiten = {}
        self.einstellungen = {}
        self.tablesByType = {}
        self.referenceDB = {}

        # the order in this table is also the order in which the elements get their finalize call
        # this is important espacially for vorteile which require many other types to be finalized first
        self.insertTable(DatenbankEinstellung, self.einstellungen) 
        self.insertTable(AttributDefinition, self.attribute) 
        self.insertTable(AbgeleiteterWertDefinition, self.abgeleiteteWerte) 
        self.insertTable(EnergieDefinition, self.energien) 
        self.insertTable(FertigkeitDefinition, self.fertigkeiten) 
        self.insertTable(TalentDefinition, self.talente) 
        self.insertTable(UeberFertigkeitDefinition, self.übernatürlicheFertigkeiten) 
        self.insertTable(Waffeneigenschaft, self.waffeneigenschaften) 
        self.insertTable(WaffeDefinition, self.waffen) 
        self.insertTable(RuestungDefinition, self.rüstungen) 
        self.insertTable(Regel, self.regeln) 
        self.insertTable(FreieFertigkeitDefinition, self.freieFertigkeiten)  
        self.insertTable(VorteilDefinition, self.vorteile)

        if os.path.isfile(self.datei):
            refDB = True
            if not self.xmlLadenInternal(self.datei, refDB):
                self.datei = None
                return False

            EventBus.doAction("basisdatenbank_geladen", { "datenbank" : self, "isCharakterEditor" : isCharakterEditor })

        hausregelnValid = True
        if self.hausregelDatei and os.path.isfile(self.hausregelDatei):
            refDB = False
            hausregelnValid = self.xmlLadenInternal(self.hausregelDatei, refDB)
            if not hausregelnValid:
                self.hausregelDatei = None

        self.verify(isCharakterEditor)

        for table in self.tablesByType.values():
            for element in table.values():
                element.finalize(self)

        EventBus.doAction("datenbank_geladen", { "datenbank" : self, "isCharakterEditor" : isCharakterEditor })
        return hausregelnValid

    def xmlLadenAdditiv(self, file, conflictCB):
        if not self.xmlLadenInternal(file, refDB = False, conflictCB = conflictCB):
            return False
        for table in self.tablesByType.values():
            for element in table.values():
                element.finalize(self)
        return True

    def xmlLadenInternal(self, file, refDB, conflictCB = None):
        root = etree.parse(file).getroot()

        if root.tag != 'Datenbank':
            return False

        if not refDB:
            #Versionierung
            versionXml = root.find('Version')
            hausregelnVersion = 0
            if versionXml is not None:
                logging.debug("User DB: VersionXML found")
                hausregelnVersion = int(versionXml.text)

            logging.debug("Start Hausregeln Migration")
            Migrationen.hausregelnMigrieren(root, hausregelnVersion)

            loadAdditive = conflictCB is not None
            if root.find('Plugins') is not None and root.find('Plugins').text:         
                if loadAdditive:
                    self.enabledPlugins += root.find('Plugins').text.split(",")
                else:
                    self.enabledPlugins = root.find('Plugins').text.split(",")
            elif not loadAdditive:
                self.enabledPlugins = []

        numLoaded = 0

        #Remove existing entries (should be used in database_user only)
        #Also check if the entries exist at all (might have been removed/renamed due to a ref db update)
        nameToType = {t.__name__ : t for t in self.tablesByType}

        for rem in root.findall('Remove'):
            typ = rem.get('typ')
            name = rem.get('name')
            if typ not in nameToType:
                continue
            table = self.tablesByType[nameToType[typ]]
            if not name in table:
                continue
            table.pop(name)

        #Attribute
        attributNodes = root.findall('Attribut')
        for node in attributNodes:
            numLoaded += 1
            A = AttributDefinition()
            A.name = node.get('name')
            A.text = node.text or ''
            A.anzeigename = node.get('anzeigename')
            A.steigerungsfaktor = int(node.get('steigerungsfaktor'))
            A.sortorder = int(node.get('sortorder'))
            self.loadElement(A, refDB, conflictCB)

        #Abgeleitete Werte
        abNodes = root.findall('AbgeleiteterWert')
        for node in abNodes:
            numLoaded += 1
            A = AbgeleiteterWertDefinition()
            A.name = node.get('name')
            A.text = node.text or ''
            A.anzeigename = node.get('anzeigename')
            A.anzeigen = node.get('anzeigen') == "1"
            A.formel = node.get('formel')
            A.script = node.get('script') or ""
            A.finalscript = node.get('finalscript') or ""
            A.sortorder = int(node.get('sortorder'))
            self.loadElement(A, refDB, conflictCB)

        # Energien
        energieNodes = root.findall('Energie')
        for node in energieNodes:
            numLoaded += 1
            E = EnergieDefinition()
            E.name = node.get('name')
            if 'voraussetzungen' in node.attrib:
                E.voraussetzungen = Hilfsmethoden.VorStr2Array(node.get('voraussetzungen'))
            E.text = node.text or ''
            E.anzeigename = node.get('anzeigename')
            E.steigerungsfaktor = int(node.get('steigerungsfaktor'))
            E.sortorder = int(node.get('sortorder'))
            self.loadElement(E, refDB, conflictCB)

        #Vorteile
        vorteilNodes = root.findall('Vorteil')
        for vort in vorteilNodes:
            numLoaded += 1
            V = VorteilDefinition()
            V.name = vort.get('name')
            V.kosten = int(vort.get('kosten'))
            V.nachkauf = vort.get('nachkauf')
            V.typ = int(vort.get('typ'))
            if 'voraussetzungen' in vort.attrib:
                V.voraussetzungen = Hilfsmethoden.VorStr2Array(vort.get('voraussetzungen'))
            V.text = vort.text or ''
            V.script = vort.get('script') or ""
            prio = vort.get('scriptPrio')
            if prio:
                V.scriptPrio = int(prio)

            if vort.get('querverweise'):
                V.querverweise = list(map(str.strip, vort.get('querverweise').split("|")))

            if vort.get('variableKosten'):
                V.variableKosten = int(vort.get('variableKosten')) == 1
            else:
                V.variableKosten = False

            if vort.get('kommentar'):
                V.kommentarErlauben = V.variableKosten or int(vort.get('kommentar')) == 1
            else:
                V.kommentarErlauben = V.variableKosten

            if vort.get('csAuflisten'):
                V.cheatsheetAuflisten = int(vort.get('csAuflisten')) == 1
            if vort.get('csBeschreibung'):
                V.cheatsheetBeschreibung = vort.get('csBeschreibung')
            if vort.get('linkKategorie'):
                V.linkKategorie = int(vort.get('linkKategorie'))
            if vort.get('linkElement'):
                V.linkElement = vort.get('linkElement')
            if vort.get('info'):
                V.info = vort.get('info')
            if vort.get('bedingungen'):
                V.bedingungen = vort.get('bedingungen')

            self.loadElement(V, refDB, conflictCB)
            
        #Fertigkeiten
        fertigkeitNodes = root.findall('Fertigkeit')
        for fer in fertigkeitNodes:
            numLoaded += 1
            F = FertigkeitDefinition()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            if 'voraussetzungen' in fer.attrib:
                F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'))
            F.text = fer.text or ''
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))
            F.kampffertigkeit = int(fer.get('kampffertigkeit'))

            typ = fer.get('typ')
            if typ:
                F.typ = int(typ)
            else:
                F.typ = -1

            self.loadElement(F, refDB, conflictCB)

        überFertigkeitNodes = root.findall('ÜbernatürlicheFertigkeit')
        for fer in überFertigkeitNodes:
            numLoaded += 1
            F = UeberFertigkeitDefinition()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            if 'voraussetzungen' in fer.attrib:
                F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'))
            F.text = fer.text or ''
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))

            typ = fer.get('typ')
            if typ:
                F.typ = int(typ)
            else:
                F.typ = -1

            if fer.get('talentegruppieren'):
                F.talenteGruppieren = int(fer.get('talentegruppieren')) == 1

            self.loadElement(F, refDB, conflictCB)

        #Talente
        talentNodes = root.findall('Talent')
        for tal in talentNodes:
            numLoaded += 1
            T = TalentDefinition()
            T.name = tal.get('name') 
            T.kosten = int(tal.get('kosten'))
            if 'spezialTyp' in tal.attrib:
                T.spezialTyp = int(tal.get('spezialTyp'))
            T.verbilligt = int(tal.get('verbilligt')) == 1
            if 'voraussetzungen' in tal.attrib:
                T.voraussetzungen = Hilfsmethoden.VorStr2Array(tal.get('voraussetzungen'))
            T.text = tal.text or ''
            T.fertigkeiten = Hilfsmethoden.FertStr2Array(tal.get('fertigkeiten'), None)
            T.variableKosten = int(tal.get('variableKosten')) == 1
            if tal.get('kommentar'):
                T.kommentarErlauben = T.variableKosten or int(tal.get('kommentar')) == 1
            else:
                T.kommentarErlauben = T.variableKosten

            if tal.get('csAuflisten'):
                T.cheatsheetAuflisten = int(tal.get('csAuflisten')) == 1
            if tal.get('referenzbuch'):
                T.referenzBuch = int(tal.get('referenzbuch'))
            if tal.get('referenzseite'):
                T.referenzSeite = int(tal.get('referenzseite'))
            if tal.get('info'):
                T.info = tal.get('info')

            self.loadElement(T, refDB, conflictCB)
          
        #Waffeneigenschaften
        eigenschaftNodes = root.findall('Waffeneigenschaft')
        for eigenschaft in eigenschaftNodes:
            numLoaded += 1
            W = Waffeneigenschaft()
            W.name = eigenschaft.get('name')
            W.text = eigenschaft.text or ''
            W.script = eigenschaft.get('script') or ""
            prio = eigenschaft.get('scriptPrio')
            if prio:
                W.scriptPrio = int(prio)

            self.loadElement(W, refDB, conflictCB)

        #Waffen
        for wa in root.findall('Waffe'):
            numLoaded += 1
            w = WaffeDefinition()
            w.fernkampf = wa.get('fk') == '1'
            if w.fernkampf:
                w.lz = int(wa.get('lz'))
            w.wm = int(wa.get('wm'))
            w.name = wa.get('name')
            w.rw = int(wa.get('rw'))
            w.würfel = int(wa.get('würfel'))
            w.würfelSeiten = int(wa.get('würfelSeiten'))
            w.plus = int(wa.get('plus'))
            w.härte = int(wa.get('härte'))
            if wa.text:
                w.eigenschaften = list(map(str.strip, wa.text.split(",")))
            w.fertigkeit = wa.get('fertigkeit')
            w.talent = wa.get('talent')
            kampfstile = wa.get('kampfstile')
            if kampfstile:
                w.kampfstile = sorted(list(map(str.strip, kampfstile.split(","))))

            self.loadElement(w, refDB, conflictCB)

        #Rüstungen
        for rue in root.findall('Rüstung'):
            numLoaded += 1
            r = RuestungDefinition()
            r.name = rue.get('name')
            r.typ = int(rue.get('typ'))
            r.system = int(rue.get('system'))
            r.rs[0] = int(rue.get('rsBeine'))
            r.rs[1] = int(rue.get('rsLArm'))
            r.rs[2] = int(rue.get('rsRArm'))
            r.rs[3] = int(rue.get('rsBauch'))
            r.rs[4] = int(rue.get('rsBrust'))
            r.rs[5] = int(rue.get('rsKopf'))
            r.text = rue.text or ''

            self.loadElement(r, refDB, conflictCB)
        
        #Regeln
        regelNodes = root.findall('Regel')
        for regelNode in regelNodes:
            numLoaded += 1
            r = Regel()
            r.name = regelNode.get('name')
            r.probe = regelNode.get('probe')
            r.typ = int(regelNode.get('typ'))
            if 'voraussetzungen' in regelNode.attrib:
                r.voraussetzungen = Hilfsmethoden.VorStr2Array(regelNode.get('voraussetzungen'))
            r.text = regelNode.text or ''

            self.loadElement(r, refDB, conflictCB)

        #Freie Fertigkeiten
        ffNodes = root.findall('FreieFertigkeit')
        for ffNode in ffNodes:
            numLoaded += 1
            ff = FreieFertigkeitDefinition()
            ff.name = ffNode.get('name')
            ff.kategorie = ffNode.get('kategorie')
            if 'voraussetzungen' in ffNode.attrib:
                ff.voraussetzungen = Hilfsmethoden.VorStr2Array(ffNode.get('voraussetzungen'))

            self.loadElement(ff, refDB, conflictCB)

        #Einstellungen
        eNodes = root.findall('Einstellung')
        for eNode in eNodes:
            numLoaded += 1
            de = DatenbankEinstellung()
            de.name = eNode.get('name')
            if refDB:
                de.typ = eNode.get('typ')
                de.beschreibung = eNode.get('beschreibung')
                de.split = eNode.get('split') == "1"
                de.separator = eNode.get('separator') or "\n"
                de.strip = eNode.get('strip') == "1"
            elif de.name in self.referenceDB[DatenbankEinstellung]:
                removed = self.referenceDB[DatenbankEinstellung][de.name]
                de.typ = removed.typ
                de.beschreibung = removed.beschreibung
                de.strip = removed.strip
                de.separator = removed.separator

            de.text = eNode.text or ""
            self.loadElement(de, refDB, conflictCB)

        # Done
        if numLoaded <1 and refDB:
            raise Exception('The selected database file is empty!')

        root = EventBus.applyFilter("datenbank_xml_laden", root, { "datenbank" : self, "basisdatenbank" : refDB, "conflictCallback" : conflictCB })      
        return True

    def verify(self, isCharakterEditor = False):
        self.loadingErrors = [] 

        # Voraussetzungen
        voraussetzungenKeys = [EnergieDefinition, VorteilDefinition, TalentDefinition, FertigkeitDefinition, UeberFertigkeitDefinition, Regel, FreieFertigkeitDefinition]
        for dbKey in self.tablesByType:
            if dbKey not in voraussetzungenKeys:
                continue
            for el in self.tablesByType[dbKey].values():
                try:
                    Hilfsmethoden.VerifyVorArray(el.voraussetzungen, self)
                except VoraussetzungException as e:
                    if isCharakterEditor:
                        el.voraussetzungen = []
                    errorStr = f"{dbKey.displayName} {el.name} hat fehlerhafte Voraussetzungen: {str(e)}"
                    self.loadingErrors.append([el, errorStr])
                    logging.warning(errorStr)

        #Vorteile
        for V in self.vorteile.values():
            errorStr = ""
            if V.linkKategorie == VorteilLinkKategorie.Regel and not V.linkElement in self.regeln:
                errorStr = f"Vorteil {V.name} ist mit einer nicht-existierenden Regel verknüpft: {V.linkElement}"
            elif V.linkKategorie == VorteilLinkKategorie.ÜberTalent and not V.linkElement in self.talente:
                errorStr = f"Vorteil {V.name} ist mit einem nicht-existierenden Talent verknüpft: {V.linkElement}"
            elif V.linkKategorie == VorteilLinkKategorie.Vorteil and not V.linkElement in self.vorteile:
                errorStr = f"Vorteil {V.name} ist mit einem nicht-existierenden Vorteil verknüpft: {V.linkElement}"
            if errorStr:
                if isCharakterEditor:
                    V.linkKategorie = VorteilLinkKategorie.NichtVerknüpfen
                    V.linkElement = ""
                self.loadingErrors.append([V, errorStr])
                logging.warning(errorStr)

            for ref in V.querverweise:
                if ref.startswith("Regel:"):
                    regel = ref[len("Regel:"):]
                    if regel not in self.regeln:
                        errorStr = f"Vorteil {V.name} hat einen Querverweis auf eine nicht-existierende Regel: {regel}"
                        self.loadingErrors.append([V, errorStr])
                        logging.warning(errorStr)
                elif ref.startswith("Vorteil:"):
                    vorteil = ref[len("Vorteil:"):]
                    if vorteil not in self.vorteile:
                        errorStr = f"Vorteil {V.name} hat einen Querverweis auf einen nicht-existierenden Vorteil: {vorteil}"
                        self.loadingErrors.append([V, errorStr])
                        logging.warning(errorStr)
                elif ref.startswith("Talent:"):
                    talent = ref[len("Talent:"):]
                    if talent not in self.talente:
                        errorStr = f"Vorteil {V.name} hat einen Querverweis auf ein nicht-existierendes Talent: {talent}"
                        self.loadingErrors.append([V, errorStr])
                        logging.warning(errorStr)
                elif ref.startswith("Waffeneigenschaft:"):
                    we = ref[len("Waffeneigenschaft:"):]
                    if we not in self.waffeneigenschaften:
                        errorStr = f"Vorteil {V.name} hat einen Querverweis auf eine nicht-existierende Waffeneigenschaft: {we}"
                        self.loadingErrors.append([V, errorStr])
                        logging.warning(errorStr)
                        continue
                elif ref.startswith("Abgeleiteter Wert:"):
                    wert = ref[len("Abgeleiteter Wert:"):]
                    if wert not in self.abgeleiteteWerte:
                        errorStr = f"Vorteil {V.name} hat einen Querverweis auf einen nicht-existierenden abgeleiteten Wert: {wert}"
                        self.loadingErrors.append([V, errorStr])
                        logging.warning(errorStr)
                elif ref != "Finanzen" and ref != "Statusse":
                    errorStr = f"Vorteil {V.name} hat einen Querverweis mit falscher Syntax: {ref}. Unterstützt werden nur Regel, Vorteil, Talent, Waffeneigenschaft, Abgeleiteter Wert, Finanzen und Statusse."
                    self.loadingErrors.append([V, errorStr])
                    logging.warning(errorStr)
            
        #Talente
        for T in self.talente.values():
            if len(T.fertigkeiten) == 0:
                logging.debug(f"Talent {T.name} hat keine Fertigkeiten.")
            ferts = self.fertigkeiten
            if T.spezialTalent:
                ferts = self.übernatürlicheFertigkeiten
            tmp = T.fertigkeiten
            T.fertigkeiten = []
            for fert in tmp:
                if fert not in ferts:
                    errorStr = f"Talent {T.name} referenziert eine nicht-existierende Fertigkeit: {fert}"
                    self.loadingErrors.append([T, errorStr])
                    logging.warning(errorStr)
                    if isCharakterEditor:
                        continue
                T.fertigkeiten.append(fert)

        #Fertigkeiten     
        attributeKeys = [FertigkeitDefinition, UeberFertigkeitDefinition]
        for dbKey in self.tablesByType:
            if dbKey not in attributeKeys:
                continue
            for el in self.tablesByType[dbKey].values():
                idx = -1
                for attribut in el.attribute:
                    idx += 1
                    if not attribut in self.attribute:
                        errorStr = f"{dbKey.displayName} {el.name} referenziert ein nicht-existierendes Attribut: {attribut}"
                        self.loadingErrors.append([el, errorStr])
                        logging.warning(errorStr)
                        if isCharakterEditor:
                            el.attribute[idx] = next(iter(self.attribute.values())).name

        #Waffen:
        alleKampfstile = self.findKampfstile()
        for wa in self.waffen.values():
            for eig in wa.eigenschaften:
                try:
                    Hilfsmethoden.VerifyWaffeneigenschaft(eig, self)
                except WaffeneigenschaftException as e:
                    errorStr = "Waffe " + wa.name + " hat fehlerhafte Eigenschaften: " + str(e)
                    self.loadingErrors.append([wa, errorStr])
                    logging.warning(errorStr)

            for kampfstil in wa.kampfstile:
                if kampfstil not in alleKampfstile:
                    errorStr = f"Waffe {wa.name} referenziert einen nicht-existierenden Kampfstil: {kampfstil}"
                    self.loadingErrors.append([wa, errorStr])
                    logging.warning(errorStr)

        self.loadingErrors = EventBus.applyFilter("datenbank_verify", self.loadingErrors, { "datenbank" : self, "isCharakterEditor" : isCharakterEditor })   
    
    def findKampfstile(self):
        # we are accessing einstellung.text instead of .wert because the function is called before finalize...
        kampfstilVorteile = [vort for vort in self.vorteile.values() if str(vort.typ) == self.einstellungen["Vorteile: Kampfstil Typ"].text and vort.name.endswith(" I")]

        kampfstile = []
        for vort in kampfstilVorteile:
            kampfstile.append(vort.name[:-2])
        return kampfstile