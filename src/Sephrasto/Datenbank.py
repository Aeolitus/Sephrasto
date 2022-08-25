import Fertigkeiten
import lxml.etree as etree
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException, WaffeneigenschaftException
import os.path
import Objekte
from PySide6 import QtWidgets
from Wolke import Wolke
import logging
from DatenbankEinstellung import DatenbankEinstellung
from EventBus import EventBus
import re

class DatabaseException(Exception):
    pass

class Datenbank():
    def __init__(self, hausregeln = None):    
        self.datei = None
        
        if hausregeln is not None:
            if hausregeln != "":
                tmp = os.path.join(Wolke.Settings['Pfad-Regeln'], hausregeln)
                if os.path.isfile(tmp):
                    self.datei = tmp
        elif Wolke.Settings['Datenbank']:
            tmp = os.path.join(Wolke.Settings['Pfad-Regeln'], Wolke.Settings['Datenbank'])
            if os.path.isfile(tmp):
                self.datei = tmp
        self.userDbXml = None
        self.loaded = False
        self.enabledPlugins = []

        #Versionierung
        #Wenn sich das Schema der Ref-DB ändert müssen bestehende user dbs aktualisiert werden.
        #Hier kann die Datenbank Code Version inkrementiert werden und in der Migrationen-Map eine Migrationsfunktion für die neue Version angelegt werden.
        #In dieser Funktion kann dann die UserDB-XML-Datei angepasst werden, bevor sie geladen wird.
        #Da Migrationen hier im Gegensatz zur Charaktermigration nur bei Schema-Änderungen nötig sind, gibt es nichts was wir dem User in einer messagebox zeigen müssten
        #Die Funktionen werden inkrementell ausgeführt, bspw. bei UserDB-Version '0' und DB-Code-Version '2' wird zuerst die Funktion für 1, dann die Funktion für 2 aufgerufen
        self.datenbankCodeVersion = 3
        self.migrationen = [
            lambda xmlRoot: None, #nichts zu tun, initiale db version
            self.migriere0zu1,    
            self.migriere1zu2,
            self.migriere2zu3
        ]
        if not self.migrationen[self.datenbankCodeVersion]:
            raise Exception("Migrations-Code vergessen.")

        self.xmlLaden()              

    def xmlSchreiben(self):
        root = etree.Element('Datenbank')
        
        versionXml = etree.SubElement(root, 'Version')
        versionXml.text = str(self.datenbankCodeVersion)
        etree.SubElement(root, 'Plugins').text = ",".join(self.enabledPlugins)

        #Vorteile
        for vort in self.vorteile:
            vorteil = self.vorteile[vort]
            if not vorteil.isUserAdded: continue
            v = etree.SubElement(root,'Vorteil')
            v.set('name',vorteil.name)
            v.set('kosten',str(vorteil.kosten))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(vorteil.voraussetzungen, None))
            v.set('nachkauf',vorteil.nachkauf)
            v.set('typ', str(vorteil.typ))
            v.set('variable', str(1 if vorteil.variableKosten else 0))
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

        #Talente
        for tal in self.talente:
            talent = self.talente[tal]
            if not talent.isUserAdded: continue
            v = etree.SubElement(root,'Talent')
            v.set('name',talent.name)
            v.set('kosten',str(talent.kosten))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(talent.voraussetzungen, None))
            v.set('verbilligt',str(talent.verbilligt))
            v.set('fertigkeiten',Hilfsmethoden.FertArray2Str(talent.fertigkeiten, None))
            v.set('variable', str(1 if talent.variableKosten else 0))
            v.set('kommentar', str(1 if talent.kommentarErlauben else 0))
            v.set('referenzbuch', str(talent.referenzBuch))
            v.set('referenzseite', str(talent.referenzSeite))
            v.text = talent.text

            if not talent.cheatsheetAuflisten:
                v.set('csAuflisten', "0")
            
        #Fertigkeiten
        for fer in self.fertigkeiten:
            fertigkeit = self.fertigkeiten[fer]
            if not fertigkeit.isUserAdded: continue
            v = etree.SubElement(root,'Fertigkeit')
            v.set('name',fertigkeit.name)
            v.set('steigerungsfaktor',str(fertigkeit.steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen, None))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(fertigkeit.attribute))
            v.set('kampffertigkeit',str(fertigkeit.kampffertigkeit))
            v.set('printclass',str(fertigkeit.printclass))
            v.text = fertigkeit.text

        for fer in self.übernatürlicheFertigkeiten:
            fertigkeit = self.übernatürlicheFertigkeiten[fer]
            if not fertigkeit.isUserAdded: continue
            v = etree.SubElement(root,'Übernatürliche-Fertigkeit')
            v.set('name',fertigkeit.name)
            v.set('steigerungsfaktor',str(fertigkeit.steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen, None))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(fertigkeit.attribute))
            v.set('printclass',str(fertigkeit.printclass))
            v.set('talentegruppieren',str(1 if fertigkeit.talenteGruppieren else 0))
            v.text = fertigkeit.text
              
        #Waffeneigenschaften
        for we in self.waffeneigenschaften:
            eigenschaft = self.waffeneigenschaften[we]
            if not eigenschaft.isUserAdded: continue
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
            if not waffe.isUserAdded: continue
            w = etree.SubElement(root,'Waffe')
            w.set('name', waffe.name)
            w.set('W6', str(waffe.W6))
            w.set('plus', str(waffe.plus))
            w.set('haerte', str(waffe.haerte))
            w.text = ", ".join(waffe.eigenschaften)
            w.set('fertigkeit', waffe.fertigkeit)
            w.set('talent', waffe.talent)
            w.set('kampfstile', ", ".join(waffe.kampfstile))
            w.set('rw', str(waffe.rw))
            if type(waffe) == Objekte.Fernkampfwaffe:
                w.set('lz', str(waffe.lz))
                w.set('fk', '1')
            else:
                w.set('wm', str(waffe.wm))
                w.set('fk', '0')

        #Rüstungen
        for rue in self.rüstungen:
            ruestung = self.rüstungen[rue]
            if not ruestung.isUserAdded: continue
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

        #Manöver
        for ma in self.manöver:
            manöver = self.manöver[ma]
            if not manöver.isUserAdded: continue
            m = etree.SubElement(root, 'Manöver')
            m.set('name', manöver.name)
            m.set('typ', str(manöver.typ))
            m.set('voraussetzungen', Hilfsmethoden.VorArray2Str(manöver.voraussetzungen, None))
            m.set('probe', manöver.probe)
            m.set('gegenprobe', manöver.gegenprobe)
            m.text = manöver.text
            
        #Freie Fertigkeiten
        for ff in self.freieFertigkeiten:
            fert = self.freieFertigkeiten[ff]
            if not fert.isUserAdded: continue
            f = etree.SubElement(root, 'FreieFertigkeit')
            f.set('kategorie', fert.kategorie)
            f.set('voraussetzungen', Hilfsmethoden.VorArray2Str(fert.voraussetzungen, None))
            f.text = fert.name

        #Einstellungen
        for de in self.einstellungen:
            einstellung = self.einstellungen[de]
            if not einstellung.isUserAdded: continue
            e = etree.SubElement(root, 'Einstellung')
            e.set('name', einstellung.name)
            e.text = einstellung.wert

        #Remove list
        for typ in self.removeList:
            for name in self.removeList[typ]:
                r = etree.SubElement(root,'Remove')
                r.set('name', name)
                r.set('typ', typ)

        root = EventBus.applyFilter("datenbank_xml_schreiben", root, { "datenbank" : self })

        #Write XML to file
        doc = etree.ElementTree(root)
        with open(self.datei,'wb') as file:
            file.seek(0)
            file.truncate()
            doc.write(file, encoding='UTF-8', pretty_print=True)
            file.truncate()

    def xmlLaden(self):
        self.vorteile = {}
        self.fertigkeiten = {}
        self.talente = {}
        self.übernatürlicheFertigkeiten = {}
        self.waffen = {}
        self.rüstungen = {}
        self.manöver = {}
        self.waffeneigenschaften = {}
        self.freieFertigkeiten = {}
        self.einstellungen = {}
        self.removeList = {}
        self.tablesByName = {
            'Vorteil' : self.vorteile,
            'Fertigkeit' : self.fertigkeiten,
            'Talent' : self.talente,
            'Übernatürliche Fertigkeit' : self.übernatürlicheFertigkeiten,
            'Waffeneigenschaft' : self.waffeneigenschaften,
            'Waffe' : self.waffen,
            'Rüstung' : self.rüstungen,
            'Manöver / Modifikation' : self.manöver,
            'Freie Fertigkeit' : self.freieFertigkeiten,
            'Einstellung' : self.einstellungen
        }

        databasePath = os.path.join('Data', 'datenbank.xml')
        if os.path.isfile(databasePath):
            self.xmlLadenInternal(databasePath, refDB=True)
            self.loaded = True
            EventBus.doAction("basisdatenbank_geladen", { "datenbank" : self })

        try:   
            if self.datei and os.path.isfile(self.datei):
                self.xmlLadenInternal(self.datei, refDB=False) 
                EventBus.doAction("datenbank_geladen", { "datenbank" : self })
        except DatabaseException:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Fehler!")
            messagebox.setText(self.datei + " ist keine valide Datenbank-Datei!")
            messagebox.setIcon(QtWidgets.QMessageBox.Critical)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec()

    def userDBMigrieren(self, xmlRoot, userDBVersion, datenbankCodeVersion):
        dbChanged = userDBVersion < datenbankCodeVersion
        while userDBVersion < datenbankCodeVersion:
            logging.warning("Migriere UserDB von Version " + str(userDBVersion ) + " zu " + str(userDBVersion + 1))
            userDBVersion +=1
            self.migrationen[userDBVersion](xmlRoot)

    def migriere0zu1(self, root):
        for wa in root.findall('Waffe'):
            kampfstile = []
            if int(wa.get('beid')) == 1:
                kampfstile.append("Beidhändiger Kampf")
            if int(wa.get('pari')) == 1:
                kampfstile.append("Parierwaffenkampf")
            if int(wa.get('reit')) == 1:
                kampfstile.append("Reiterkampf")
            if int(wa.get('schi')) == 1:
                kampfstile.append("Schildkampf")
            if int(wa.get('kraf')) == 1:
                kampfstile.append("Kraftvoller Kampf")
            if int(wa.get('schn')) == 1:
                kampfstile.append("Schneller Kampf")

            wa.attrib.pop('beid')
            wa.attrib.pop('pari')
            wa.attrib.pop('reit')
            wa.attrib.pop('schi')
            wa.attrib.pop('kraf')
            wa.attrib.pop('schn')
            wa.set('kampfstile', ", ".join(kampfstile))

    def migriere1zu2(self, root):
        # Apply the added attributes to the user database to make their life easier
        for ta in root.findall('Talent'):
            name = ta.get('name')
            if name in self.talente:
                ta.set('referenzbuch', '0')
                ta.set('referenzseite', str(self.talente[name].referenzSeite))
        for fe in root.findall('Übernatürliche-Fertigkeit'):
            name = fe.get('name')
            if name in self.übernatürlicheFertigkeiten and self.übernatürlicheFertigkeiten[name].talenteGruppieren:
                fe.set('talentegruppieren', '1')

    def migriere2zu3(self, root):
        def fixTalentVoraussetzungen(type):
            for node in root.findall(type):
                vor = node.get('voraussetzungen')
                if not vor:
                    continue
                node.set('voraussetzungen', re.sub(r"Talent \s*(.*?)\s*(,| ODER |$)", r"Talent '\1'\2", vor))

        fixTalentVoraussetzungen('Talent')
        fixTalentVoraussetzungen('Vorteil')
        fixTalentVoraussetzungen('Manöver')
        fixTalentVoraussetzungen('Waffeneigenschaft')
        fixTalentVoraussetzungen('FreieFertigkeit')
        fixTalentVoraussetzungen('Fertigkeit')
        fixTalentVoraussetzungen('Übernatürliche-Fertigkeit')

    def xmlLadenAdditiv(self, file, conflictCB):
        self.xmlLadenInternal(file, False, conflictCB)

    def xmlLadenInternal(self, file, refDB, conflictCB = None):
        root = etree.parse(file).getroot()

        if root.tag != 'Datenbank':
            raise DatabaseException('Not a valid database file')

        if not refDB:
            self.userDbXml = root

            #Versionierung
            versionXml = root.find('Version')
            userDBVersion = 0
            if versionXml is not None:
                logging.debug("User DB: VersionXML found")
                userDBVersion = int(versionXml.text)

            logging.debug("Starting User DB Migration")
            self.userDBMigrieren(root, userDBVersion, self.datenbankCodeVersion)

            if root.find('Plugins') is not None and root.find('Plugins').text:
                if conflictCB is None:
                    self.enabledPlugins = root.find('Plugins').text.split(",")
                else:
                    self.enabledPlugins += root.find('Plugins').text.split(",")

        numLoaded = 0

        root = EventBus.applyFilter("datenbank_xml_laden", root, { "datenbank" : self, "basisdatenbank" : refDB, "conflictCallback" : conflictCB })
        
        #Remove existing entries (should be used in database_user only)
        #Also check if the entries exist at all (might have been removed/renamed due to a ref db update)
        for rem in root.findall('Remove'):
            typ = rem.get('typ')
            name = rem.get('name')
            removed = None

            if not typ in self.tablesByName:
                continue

            table = self.tablesByName[typ]
            if not name in table:
                continue

            if not typ in self.removeList:
                self.removeList[typ] = {}
            if name in self.removeList[typ]:
                continue # loading another user db, ignore if the same element has been removed in both
            removed = table.pop(name)
            self.removeList[typ][name] = removed

        #Vorteile
        vorteilNodes = root.findall('Vorteil')
        for vort in vorteilNodes:
            numLoaded += 1
            V = Fertigkeiten.Vorteil()
            V.name = vort.get('name')
            V.kosten = int(vort.get('kosten'))
            V.nachkauf = vort.get('nachkauf')
            V.typ = int(vort.get('typ'))
            V.text = vort.text or ''
            V.script = vort.get('script')
            prio = vort.get('scriptPrio')
            if prio:
                V.scriptPrio = int(prio)

            V.isUserAdded = not refDB
            if vort.get('variable'):
                V.variableKosten = int(vort.get('variable')) == 1
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

            if conflictCB and V.name in self.vorteile:
                V = conflictCB('Vorteil', self.vorteile[V.name], V)
            self.vorteile.update({V.name: V})
            
        #Talente
        talentNodes = root.findall('Talent')
        for tal in talentNodes:
            numLoaded += 1
            T = Fertigkeiten.Talent()
            T.name = tal.get('name')
            T.kosten = int(tal.get('kosten'))
            T.verbilligt = int(tal.get('verbilligt'))
            T.text = tal.text or ''
            T.fertigkeiten = Hilfsmethoden.FertStr2Array(tal.get('fertigkeiten'), None)
            T.variableKosten = int(tal.get('variable')) == 1
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

            T.isUserAdded = not refDB

            if conflictCB and T.name in self.talente:
                T = conflictCB('Talent', self.talente[T.name], T)

            self.talente.update({T.name: T})
            
        #Fertigkeiten
        fertigkeitNodes = root.findall('Fertigkeit')
        for fer in fertigkeitNodes:
            numLoaded += 1
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text or ''
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))
            F.kampffertigkeit = int(fer.get('kampffertigkeit'))
            F.isUserAdded = not refDB

            printClass = fer.get('printclass')
            if printClass:
                F.printclass = int(printClass)
            else:
                F.printclass = -1

            if conflictCB and F.name in self.fertigkeiten:
                F = conflictCB('Fertigkeit', self.fertigkeiten[F.name], F)

            self.fertigkeiten.update({F.name: F})

        überFertigkeitNodes = root.findall('Übernatürliche-Fertigkeit')
        for fer in überFertigkeitNodes:
            numLoaded += 1
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text or ''
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))
            F.isUserAdded = not refDB

            printClass = fer.get('printclass')
            if printClass:
                F.printclass = int(printClass)
            else:
                F.printclass = -1

            if fer.get('talentegruppieren'):
                F.talenteGruppieren = int(fer.get('talentegruppieren')) == 1

            if conflictCB and F.name in self.übernatürlicheFertigkeiten:
                F = conflictCB('Übernatürliche Fertigkeit', self.übernatürlicheFertigkeiten[F.name], F)

            self.übernatürlicheFertigkeiten.update({F.name: F})
          
        #Waffeneigenschaften
        eigenschaftNodes = root.findall('Waffeneigenschaft')
        for eigenschaft in eigenschaftNodes:
            numLoaded += 1
            W = Objekte.Waffeneigenschaft()
            W.name = eigenschaft.get('name')
            W.text = eigenschaft.text or ''
            W.script = eigenschaft.get('script')
            prio = eigenschaft.get('scriptPrio')
            if prio:
                W.scriptPrio = int(prio)

            W.isUserAdded = not refDB

            if conflictCB and W.name in self.waffeneigenschaften:
                W = conflictCB('Waffeneigenschaft', self.waffeneigenschaften[W.name], W)
            self.waffeneigenschaften.update({W.name: W})

        #Waffen
        for wa in root.findall('Waffe'):
            numLoaded += 1
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
            if wa.text:
                w.eigenschaften = list(map(str.strip, wa.text.split(",")))
            w.fertigkeit = wa.get('fertigkeit')
            w.talent = wa.get('talent')
            if w.name and w.talent:
                w.anzeigename = w.name.replace(" (" + w.talent + ")", "")
            kampfstile = wa.get('kampfstile')
            if kampfstile:
                w.kampfstile = list(map(str.strip, kampfstile.split(",")))
            w.isUserAdded = not refDB

            if conflictCB and w.name in self.waffen:
                w = conflictCB('Waffe', self.waffen[w.name], w)
            self.waffen.update({w.name: w})

        #Rüstungen
        for rue in root.findall('Rüstung'):
            numLoaded += 1
            r = Objekte.Ruestung()
            r.name = rue.get('name')
            r.typ = int(rue.get('typ'))
            r.system = int(rue.get('system'))
            r.rs[0] = int(rue.get('rsBeine'))
            r.rs[1] = int(rue.get('rsLArm'))
            r.rs[2] = int(rue.get('rsRArm'))
            r.rs[3] = int(rue.get('rsBauch'))
            r.rs[4] = int(rue.get('rsBrust'))
            r.rs[5] = int(rue.get('rsKopf'))
            r.be = r.getRSGesamtInt()
            r.text = rue.text
            r.isUserAdded = not refDB

            if conflictCB and r.name in self.rüstungen:
                r = conflictCB('Rüstung', self.rüstungen[r.name], r)
            self.rüstungen.update({r.name : r})
        
        #Manöver
        manöverNodes = root.findall('Manöver')
        for ma in manöverNodes:
            numLoaded += 1
            m = Fertigkeiten.Manoever()
            m.name = ma.get('name')
            m.probe = ma.get('probe')
            m.gegenprobe = ma.get('gegenprobe')
            m.typ = int(ma.get('typ'))
            m.text = ma.text or ''
            m.isUserAdded = not refDB

            if conflictCB and m.name in self.manöver:
                m = conflictCB('Manöver / Modifikation', self.manöver[m.name], m)

            self.manöver.update({m.name: m})

        #Freie Fertigkeiten
        ffNodes = root.findall('FreieFertigkeit')
        for ffNode in ffNodes:
            numLoaded += 1
            ff = Fertigkeiten.FreieFertigkeitDB()
            ff.name = ffNode.text
            ff.kategorie = ffNode.get('kategorie')
            ff.isUserAdded = not refDB

            if conflictCB and ff.name in self.freieFertigkeiten:
                ff = conflictCB('Freie Fertigkeit', self.freieFertigkeiten[ff.name], ff)

            self.freieFertigkeiten.update({ff.name: ff})

        #Einstellungen
        eNodes = root.findall('Einstellung')
        for eNode in eNodes:
            numLoaded += 1
            de = DatenbankEinstellung()
            de.name = eNode.get('name')
            if refDB:
                de.typ = eNode.get('typ')
                de.beschreibung = eNode.get('beschreibung')
            elif 'Einstellung' in self.removeList:
                for name in self.removeList['Einstellung']:
                    if de.name == name:
                        de.typ = self.removeList['Einstellung'][name].typ
                        de.beschreibung = self.removeList['Einstellung'][name].beschreibung
                        break

            de.wert = eNode.text or ''
            de.isUserAdded = not refDB

            if conflictCB and de.name in self.einstellungen:
                de = conflictCB('Einstellung', self.einstellungen[de.name], de)

            self.einstellungen.update({de.name: de})

        # Step 2: Voraussetzungen - requires everything else to be loaded for cross validation
        notifyError = False # For testing of manual db changes

        #Vorteile
        for vort in vorteilNodes:
            V = self.vorteile[vort.get('name')]
            try:
                V.voraussetzungen = Hilfsmethoden.VorStr2Array(vort.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Vorteil " + V.name + ": " + str(e)
                if notifyError:
                    assert False, errorStr
                logging.warning(errorStr)
            
        #Talente
        for tal in talentNodes:
            T = self.talente[tal.get('name')] 
            try:
                T.voraussetzungen = Hilfsmethoden.VorStr2Array(tal.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Talent " + T.name + ": " + str(e)
                if notifyError:
                    assert False, errorStr
                logging.warning(errorStr)

            if len(T.fertigkeiten) == 0:
                errorStr = "Talent " + T.name + " has no Fertigkeiten."
                if notifyError:
                    assert False, errorStr
                logging.debug("Talent " + T.name + " has no Fertigkeiten.")
            for fert in T.fertigkeiten:
                if not fert in self.fertigkeiten and not fert in self.übernatürlicheFertigkeiten:
                    errorStr = "Talent is referencing non-existing Fertigkeit " + T.name + ": " + fert
                    if notifyError:
                        assert False, errorStr
                    logging.warning(errorStr)

        #Fertigkeiten
        for fer in fertigkeitNodes:
            F = self.fertigkeiten[fer.get('name')]
            try:
                F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Fertigkeit " + F.name + ": " + str(e)
                if notifyError:
                    assert False, errorStr
                logging.warning(errorStr)

        for fer in überFertigkeitNodes:
            F = self.übernatürlicheFertigkeiten[fer.get('name')]
            try:
                F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Übernatürliche Fertigkeit " + F.name + ": " + str(e)
                if notifyError:
                    assert False, errorStr
                logging.warning(errorStr)
      
        #Manöver
        for ma in manöverNodes:
            m = self.manöver[ma.get('name')]
            try:
                m.voraussetzungen = Hilfsmethoden.VorStr2Array(ma.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Manöver " + m.name + ": " + str(e)
                if notifyError:
                    assert False, errorStr
                logging.warning(errorStr)
               
        #Freie Fertigkeiten
        for ffNode in ffNodes:
            ff = self.freieFertigkeiten[ffNode.text]
            try:
                if ffNode.get('voraussetzungen'):
                    ff.voraussetzungen = Hilfsmethoden.VorStr2Array(ffNode.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of FreieFertigkeit " + ff.name + ": " + str(e)
                if notifyError:
                    assert False, errorStr
                logging.warning(errorStr)

        #Further verifications
        for wa in self.waffen.values():
            for eig in wa.eigenschaften:
                try:
                    Hilfsmethoden.VerifyWaffeneigenschaft(eig, self)
                except WaffeneigenschaftException as e:
                    errorStr = "Error in Eigenschaften of Waffe " + wa.name + ": " + str(e)
                    if notifyError:
                        assert False, errorStr
                    logging.warning(errorStr)

        if not refDB:
            for dbType in [self.vorteile, self.talente, self.fertigkeiten, self.übernatürlicheFertigkeiten, self.manöver, self.freieFertigkeiten]:
                for elem in dbType.values():
                    try:
                        Hilfsmethoden.VorStr2Array(Hilfsmethoden.VorArray2Str(elem.voraussetzungen), self)
                    except VoraussetzungException as e:
                        logging.warning("Error in Voraussetzungen of " + elem.name + ": " + str(e)) 

        if numLoaded <1 and refDB:
            raise Exception('The selected database file is empty!')
        
        return True
    
    def findKampfstile(self):
        kampfstilVorteile = [vort for vort in self.vorteile.values() if vort.typ == 3 and vort.name.endswith(" I")]

        kampfstile = []
        for vort in kampfstilVorteile:
            kampfstile.append(vort.name[:-2])
        return kampfstile

    def findHeimaten(self):
        return sorted(self.einstellungen["Heimaten"].toTextList())