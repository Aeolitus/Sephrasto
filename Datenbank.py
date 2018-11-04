import Fertigkeiten
import lxml.etree as etree
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import os.path
import Objekte
from PyQt5 import QtWidgets
from Wolke import Wolke
import logging

class DatabaseException(Exception):
    pass

class Datenbank():
    def __init__(self):
        self.vorteile = {}
        self.fertigkeiten = {}
        self.talente = {}
        self.übernatürlicheFertigkeiten = {}
        self.waffen = {}
        self.manöver = {}
        self.removeList = []
        
        self.datei = None
        if Wolke.Settings['Datenbank']:
            tmp = os.path.join(Wolke.Settings['Pfad-Regeln'], 
                               Wolke.Settings['Datenbank'])
            if os.path.isfile(tmp):
                self.datei = tmp
        self.userDbXml = None
        self.loaded = False

        #Versionierung
        #Wenn sich das Schema der Ref-DB ändert müssen bestehende user dbs aktualisiert werden.
        #Hier kann die Datenbank Code Version inkrementiert werden und in der Migrationen-Map eine Migrationsfunktion für die neue Version angelegt werden.
        #In dieser Funktion kann dann die UserDB-XML-Datei angepasst werden, bevor sie geladen wird.
        #Da Migrationen hier im Gegensatz zur Charaktermigration nur bei Schema-Änderungen nötig sind, gibt es nichts was wir dem User in einer messagebox zeigen müssten
        #Die Funktionen werden inkrementell ausgeführt, bspw. bei UserDB-Version '0' und DB-Code-Version '2' wird zuerst die Funktion für 1, dann die Funktion für 2 aufgerufen
        self.datenbankCodeVersion = 0
        self.migrationen = [
            lambda xmlRoot: None, #nichts zu tun, initiale db version   
        ]
        if not self.migrationen[self.datenbankCodeVersion]:
            raise Exception("Migrations-Code vergessen.")

        self.xmlLaden()              

    def xmlSchreiben(self):
        Wolke.Fehlercode = -26
        root = etree.Element('Datenbank')
        
        etree.SubElement(root, 'Version').text = str(self.datenbankCodeVersion)

        #Vorteile
        Wolke.Fehlercode = -27
        for vort in self.vorteile:
            vorteil = self.vorteile[vort]
            if not vorteil.isUserAdded: continue
            v = etree.SubElement(root,'Vorteil')
            v.set('name',vorteil.name)
            v.set('kosten',str(vorteil.kosten))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(vorteil.voraussetzungen, None))
            v.set('nachkauf',vorteil.nachkauf)
            v.set('typ', str(vorteil.typ))
            v.set('variable', str(vorteil.variable))
            v.text = vorteil.text
            if len(vorteil.script) > 0:
                v.set('script', "; ".join(vorteil.script))
            if vorteil.scriptPrio != 0:
                v.set('scriptPrio', str(vorteil.scriptPrio))

        #Talente
        Wolke.Fehlercode = -28
        for tal in self.talente:
            talent = self.talente[tal]
            if not talent.isUserAdded: continue
            v = etree.SubElement(root,'Talent')
            v.set('name',talent.name)
            v.set('kosten',str(talent.kosten))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(talent.voraussetzungen, None))
            v.set('verbilligt',str(talent.verbilligt))
            v.set('fertigkeiten',Hilfsmethoden.FertArray2Str(talent.fertigkeiten, None))
            v.set('variable',str(talent.variable))
            v.set('printclass',str(talent.printclass))
            v.text = talent.text
            
        #Fertigkeiten
        Wolke.Fehlercode = -29
        for fer in self.fertigkeiten:
            fertigkeit = self.fertigkeiten[fer]
            if not fertigkeit.isUserAdded: continue
            v = etree.SubElement(root,'Fertigkeit')
            v.set('name',fertigkeit.name)
            v.set('steigerungsfaktor',str(fertigkeit.steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen, None))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(fertigkeit.attribute))
            v.set('kampffertigkeit',str(fertigkeit.kampffertigkeit))
            v.text = fertigkeit.text

        Wolke.Fehlercode = -30
        for fer in self.übernatürlicheFertigkeiten:
            fertigkeit = self.übernatürlicheFertigkeiten[fer]
            if not fertigkeit.isUserAdded: continue
            v = etree.SubElement(root,'Übernatürliche-Fertigkeit')
            v.set('name',fertigkeit.name)
            v.set('steigerungsfaktor',str(fertigkeit.steigerungsfaktor))
            v.set('voraussetzungen',Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen, None))
            v.set('attribute',Hilfsmethoden.AttrArray2Str(fertigkeit.attribute))
            v.text = fertigkeit.text
                                                    
        #Waffen
        Wolke.Fehlercode = -31
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
            w.set('beid', str(waffe.beid))
            w.set('pari', str(waffe.pari))
            w.set('reit', str(waffe.reit))
            w.set('schi', str(waffe.schi))
            w.set('kraf', str(waffe.kraf))
            w.set('schn', str(waffe.schn))
            w.set('rw', str(waffe.rw))
            if type(waffe) == Objekte.Fernkampfwaffe:
                w.set('lz', str(waffe.lz))
                w.set('fk', '1')
            else:
                w.set('wm', str(waffe.wm))
                w.set('fk', '0')

        #Manöver
        Wolke.Fehlercode = -34
        for ma in self.manöver:
            manöver = self.manöver[ma]
            if not manöver.isUserAdded: continue
            m = etree.SubElement(root, 'Manoever')
            m.set('name', manöver.name)
            m.set('typ', str(manöver.typ))
            m.set('voraussetzungen', Hilfsmethoden.VorArray2Str(manöver.voraussetzungen, None))
            m.set('probe', manöver.probe)
            m.set('gegenprobe', manöver.gegenprobe)
            m.text = manöver.text

        #Remove list
        for rm in self.removeList:
            r = etree.SubElement(root,'Remove')
            r.set('name', rm[0])
            r.set('typ', rm[1])

        #Write XML to file
        Wolke.Fehlercode = -26
        doc = etree.ElementTree(root)
        Wolke.Fehlercode = -32
        with open(self.datei,'wb') as file:
            file.seek(0)
            file.truncate()
            doc.write(file, encoding='UTF-8', pretty_print=True)
            file.truncate()
            
        Wolke.Fehlercode = 0

    def xmlLaden(self):
        self.vorteile = {}
        self.fertigkeiten = {}
        self.talente = {}
        self.übernatürlicheFertigkeiten = {}
        self.waffen = {}
        self.manöver = {}
        self.removeList = []

        if os.path.isfile('datenbank.xml'):
            self.xmlLadenInternal('datenbank.xml', refDB=True)
            self.loaded = True

        try:   
            if self.datei and os.path.isfile(self.datei):
                self.xmlLadenInternal(self.datei, refDB=False) 
        except DatabaseException:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Fehler!")
            messagebox.setText(self.datei + " ist keine valide Datenbank-Datei!")
            messagebox.setIcon(QtWidgets.QMessageBox.Critical)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec_()

    def userDBMigrieren(self, xmlRoot, userDBVersion, datenbankCodeVersion):
        dbChanged = userDBVersion < datenbankCodeVersion
        while userDBVersion < datenbankCodeVersion:
            logging.warning("Migriere UserDB von Version " + str(userDBVersion ) + " zu " + str(userDBVersion + 1))
            userDBVersion +=1
            self.migrationen[userDBVersion](xmlRoot)

    def xmlLadenInternal(self, file, refDB):
        Wolke.Fehlercode = -20
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

        numLoaded = 0
        
        #Remove existing entries (should be used in database_user only)
        #Also check if the entries exist at all (might have been removed/renamed due to a ref db update)
        for rem in root.findall('Remove'):
            typ = rem.get('typ')
            name = rem.get('name')
            removed = None
            if typ == 'Vorteil' and name in self.vorteile:
                removed = self.vorteile.pop(name)
            elif typ == 'Fertigkeit' and name in self.fertigkeiten:
                removed = self.fertigkeiten.pop(name)
            elif typ == 'Talent' and name in self.talente:
                removed = self.talente.pop(name)
            elif typ == 'Übernatürliche Fertigkeit' and name in self.übernatürlicheFertigkeiten:
                removed = self.übernatürlicheFertigkeiten.pop(name)
            elif typ == 'Waffe' and name in self.waffen:
                removed = self.waffen.pop(name)
            elif typ == 'Manöver / Modifikation' and name in self.manöver:
                removed = self.manöver.pop(name)
            if removed:
                self.removeList.append((name, typ, removed))

        #Vorteile
        Wolke.Fehlercode = -21
        vorteilNodes = root.findall('Vorteil')
        for vort in vorteilNodes:
            numLoaded += 1
            V = Fertigkeiten.Vorteil()
            V.name = vort.get('name')
            V.kosten = int(vort.get('kosten'))
            V.nachkauf = vort.get('nachkauf')
            V.typ = int(vort.get('typ'))
            V.text = vort.text
            script = vort.get('script')
            if script:
                V.script = list(map(str.strip, script.split(";")))
            prio = vort.get('scriptPrio')
            if prio:
                V.scriptPrio = int(prio)

            V.isUserAdded = not refDB
            try:
                V.variable = int(vort.get('variable'))
            except:
                V.variable = -1
            self.vorteile.update({V.name: V})
            
        #Talente
        Wolke.Fehlercode = -22
        talentNodes = root.findall('Talent')
        for tal in talentNodes:
            numLoaded += 1
            T = Fertigkeiten.Talent()
            T.name = tal.get('name')
            T.kosten = int(tal.get('kosten'))
            T.verbilligt = int(tal.get('verbilligt'))
            T.text = tal.text
            T.fertigkeiten = Hilfsmethoden.FertStr2Array(tal.get('fertigkeiten'), None)
            T.variable = int(tal.get('variable'))
            T.isUserAdded = not refDB

            printClass = tal.get('printclass')
            if printClass:
                T.printclass = int(printClass)
            else:
                T.printclass = -1
            self.talente.update({T.name: T})
            
        #Fertigkeiten
        Wolke.Fehlercode = -23
        fertigkeitNodes = root.findall('Fertigkeit')
        for fer in fertigkeitNodes:
            numLoaded += 1
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))
            F.kampffertigkeit = int(fer.get('kampffertigkeit'))
            F.isUserAdded = not refDB
            self.fertigkeiten.update({F.name: F})

        Wolke.Fehlercode = -24
        überFertigkeitNodes = root.findall('Übernatürliche-Fertigkeit')
        for fer in überFertigkeitNodes:
            numLoaded += 1
            F = Fertigkeiten.Fertigkeit()
            F.name = fer.get('name')
            F.steigerungsfaktor = int(fer.get('steigerungsfaktor'))
            F.text = fer.text
            F.attribute = Hilfsmethoden.AttrStr2Array(fer.get('attribute'))
            F.isUserAdded = not refDB
            self.übernatürlicheFertigkeiten.update({F.name: F})
            
        #Waffen
        Wolke.Fehlercode = -25
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
            w.beid = int(wa.get('beid'))
            w.pari = int(wa.get('pari'))
            w.reit = int(wa.get('reit'))
            w.schi = int(wa.get('schi'))
            w.kraf = int(wa.get('kraf'))
            w.schn = int(wa.get('schn'))
            w.isUserAdded = not refDB
            self.waffen.update({w.name: w})
        
        #Manöver
        Wolke.Fehlercode = -26
        manöverNodes = root.findall('Manöver')
        for ma in manöverNodes:
            numLoaded += 1
            m = Fertigkeiten.Manoever()
            m.name = ma.get('name')
            m.probe = ma.get('probe')
            m.gegenprobe = ma.get('gegenprobe')
            m.typ = int(ma.get('typ'))
            m.text = ma.text
            m.isUserAdded = not refDB
            self.manöver.update({m.name: m})

        # Step 2: Voraussetzungen - requires everything else to be loaded for cross validation

        #Vorteile
        Wolke.Fehlercode = -21
        for vort in vorteilNodes:
            V = self.vorteile[vort.get('name')]
            try:
                V.voraussetzungen = Hilfsmethoden.VorStr2Array(vort.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Vorteil " + V.name + ": " + str(e)
                assert False, errorStr
                logging.warning(errorStr)
            
        #Talente
        Wolke.Fehlercode = -22
        for tal in talentNodes:
            T = self.talente[tal.get('name')] 
            try:
                T.voraussetzungen = Hilfsmethoden.VorStr2Array(tal.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Talent " + T.name + ": " + str(e)
                assert False, errorStr
                logging.warning(errorStr)
        #Fertigkeiten
        Wolke.Fehlercode = -23
        for fer in fertigkeitNodes:
            F = self.fertigkeiten[fer.get('name')]
            try:
                F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Fertigkeit " + F.name + ": " + str(e)
                assert False, errorStr
                logging.warning(errorStr)

        Wolke.Fehlercode = -24
        for fer in überFertigkeitNodes:
            F = self.übernatürlicheFertigkeiten[fer.get('name')]
            try:
                F.voraussetzungen = Hilfsmethoden.VorStr2Array(fer.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Übernatürliche Fertigkeit " + F.name + ": " + str(e)
                assert False, errorStr
                logging.warning(errorStr)
      
        #Manöver
        Wolke.Fehlercode = -26
        for ma in manöverNodes:
            m = self.manöver[ma.get('name')]
            try:
                m.voraussetzungen = Hilfsmethoden.VorStr2Array(ma.get('voraussetzungen'), self)
            except VoraussetzungException as e:
                errorStr = "Error in Voraussetzungen of Manöver " + m.name + ": " + str(e)
                assert False, errorStr
                logging.warning(errorStr)

        if numLoaded <1 and refDB:
            Wolke.Fehlercode = -33
            raise Exception('The selected database file is empty!')
        
        # Reset 
        Wolke.Fehlercode = 0

        return True