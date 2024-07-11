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
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import os.path
from Wolke import Wolke
import logging
from EventBus import EventBus
import re
from Migrationen import Migrationen
from VoraussetzungenListe import VoraussetzungenListe, VoraussetzungException
from Serialization import Serialization

class Datenbank():
    def __init__(self):
        self.datei = None
        self.hausregelDatei = None
        self.enabledPlugins = []
        self.loadingErrors = []
        
    @property
    def hausregelnAnzeigeName(self):
        return os.path.basename(self.hausregelDatei) if self.hausregelDatei else "Keine"

    def saveFile(self, filepath = None, merge = False):
        if filepath is None:
            filepath = self.hausregelDatei
        else:
            self.hausregelDatei = filepath
        _, fileExtension = os.path.splitext(filepath)
        options = { "isMerge" : merge, "rootIsList" : True }
        serializer = Serialization.getSerializer(fileExtension, "Datenbank", options)
        self.serialize(serializer, merge)
        serializer.writeFile(filepath)

    def serialize(self, serializer, merge = False):
        serializer = EventBus.applyFilter("datenbank_serialisieren", serializer, { "datenbank" : self, "merge" : merge })

        serializer.setNested('Version', Migrationen.datenbankCodeVersion)
        serializer.setNested('Plugins', ",".join(self.enabledPlugins))

        for table in self.tablesByType.values():
            for element in table.values():
                if not merge and not self.isChangedOrNew(element): continue
                serializer.begin(element.serializationName)
                element.serialize(serializer)
                serializer.end() #element.serializationName

        #Remove list
        if not merge:
            for type in self.referenceDB:
                for name in self.getRemoved(type):
                    serializer.begin("Remove")
                    serializer.set("name", name)
                    serializer.set("typ", type.serializationName)
                    serializer.end() #remove

        EventBus.doAction("datenbank_serialisiert", { "datenbank" : self, "serializer" : serializer, "merge" : merge })

    def insertTable(self, type, table):
        self.tablesByType[type] = table
        self.referenceDB[type] = {}

    def loadElement(self, element, refDB = True, conflictCB = None):
        dbKey = element.__class__
        if refDB:
            self.referenceDB[dbKey][element.name] = element
        elif conflictCB:
            isInRefDB = element.name in self.referenceDB[element.__class__]
            isInDB = element.name in self.tablesByType[element.__class__]

            resolvedElement = element
            if not isInDB and isInRefDB:
                resolvedElement = conflictCB(dbKey, None, element) # removed
            elif isInDB:
                existingElement = self.tablesByType[dbKey][element.name]
                if self.isChangedOrNew(existingElement) and not element.deepequals(existingElement): 
                    resolvedElement = conflictCB(dbKey, self.tablesByType[dbKey][element.name], element) # new or changed
                
            if resolvedElement is None:
                return

            if isInDB and resolvedElement.name != element.name:
                self.tablesByType[dbKey].pop(element.name)
            element = resolvedElement

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

    def loadFile(self, datei = os.path.join('Data', 'datenbank.xml'), hausregeln = None, isCharakterEditor = False):
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
        # this is important especially for vorteile which require many other types to be finalized first
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
            if not self.__loadFileInternal(self.datei, refDB, isCharakterEditor):
                self.datei = None
                return False

            EventBus.doAction("basisdatenbank_geladen", { "datenbank" : self, "isCharakterEditor" : isCharakterEditor })

        hausregelnValid = True
        if self.hausregelDatei and os.path.isfile(self.hausregelDatei):
            refDB = False
            hausregelnValid = self.__loadFileInternal(self.hausregelDatei, refDB, isCharakterEditor)
            if not hausregelnValid:
                self.hausregelDatei = None

        if not isCharakterEditor:
            self.verify()

        for elementType, table in self.tablesByType.items():
            if hasattr(elementType, "finalizeStatic"):
                elementType.finalizeStatic(self)
            for element in table.values():
                element.finalize(self)

        EventBus.doAction("datenbank_geladen", { "datenbank" : self, "isCharakterEditor" : isCharakterEditor })
        return hausregelnValid

    def loadFileAdditional(self, file, conflictCB):
        if not self.__loadFileInternal(file, refDB = False, isCharakterEditor = False, conflictCB = conflictCB):
            return False
        for elementType, table in self.tablesByType.items():
            if hasattr(elementType, "finalizeStatic"):
                elementType.finalizeStatic(self)
            for element in table.values():
                element.finalize(self)
        return True

    def __loadFileInternal(self, file, refDB, isCharakterEditor, conflictCB = None):
        _, fileExtension = os.path.splitext(file)
        options = { "useCache" : isCharakterEditor }
        deserializer = Serialization.getDeserializer(fileExtension, options)
        if not deserializer.readFile(file, "Datenbank" if refDB else "HausregelDatenbank"):
            return False
        if not self.deserialize(deserializer, refDB, conflictCB):
            return False
        return True

    def deserialize(self, deserializer, refDB, conflictCB = None):
        deserializer = EventBus.applyFilter("datenbank_deserialisieren", deserializer, { "datenbank" : self, "basisdatenbank" : refDB, "conflictCallback" : conflictCB })

        if deserializer.currentTag != "Datenbank":
            return False
        if not refDB:
            loadAdditive = conflictCB is not None
            if deserializer.find('Plugins'):
                text = deserializer.get('text')
                if text:
                    if loadAdditive:
                        self.enabledPlugins += deserializer.get('text').split(",")
                    else:
                        self.enabledPlugins = deserializer.get('text').split(",")
                deserializer.end()
            elif not loadAdditive:
                self.enabledPlugins = []

        serializationNameToType = {t.serializationName : t for t in self.tablesByType}
        for serializationName in deserializer.listTags():
            t = serializationNameToType.get(serializationName)
            if t is not None:
                dbElement = t()
                dbElement.deserialize(deserializer, None if refDB else self.referenceDB)
                self.loadElement(dbElement, refDB, conflictCB)

            elif serializationName == "Remove" and not refDB:
                #Remove existing entries (should be used in hausregel db only)
                #Also check if the entries exist at all (might have been removed/renamed due to a ref db update)
                typ = deserializer.get("typ")
                if typ not in serializationNameToType:
                    continue
                table = self.tablesByType[serializationNameToType[typ]]
                name = deserializer.get("name")
                if not name in table:
                    continue
                
                if conflictCB:
                    existingElement = table[name]
                    if self.isChangedOrNew(existingElement): 
                        resolvedElement = conflictCB(serializationNameToType[typ], existingElement, None)
                        if resolvedElement is not None:
                            self.loadElement(resolvedElement, False)
                            continue

                table.pop(name)

        EventBus.doAction("datenbank_deserialisiert", { "datenbank" : self, "deserializer" : deserializer, "basisdatenbank" : refDB, "conflictCallback" : conflictCB })    

        return True

    def verify(self):
        self.loadingErrors = [] 

        # Voraussetzungen
        voraussetzungenKeys = [EnergieDefinition, VorteilDefinition, TalentDefinition, FertigkeitDefinition, UeberFertigkeitDefinition, Regel, FreieFertigkeitDefinition]
        for dbKey in self.tablesByType:
            if dbKey not in voraussetzungenKeys:
                continue
            for el in self.tablesByType[dbKey].values():
                try:
                    VoraussetzungenListe().compile(el.voraussetzungen.text, self)
                except VoraussetzungException as e:
                    errorStr = f"{dbKey.displayName} {el.name} hat fehlerhafte Voraussetzungen: {str(e)}"
                    self.loadingErrors.append([el, errorStr])
                    logging.warning(errorStr)

        #Vorteile
        for V in self.vorteile.values():
            errorStr = ""

            if V.kategorie >= len(self.einstellungen['Vorteile: Kategorien'].wert):
                errorStr = "Vorteil {V.name} hat einen unbekannten Typ."
                self.loadingErrors.append([V, errorStr])
                logging.warning(errorStr)

            if V.linkKategorie == VorteilLinkKategorie.Regel and not V.linkElement in self.regeln:
                errorStr = f"Vorteil {V.name} ist mit einer nicht-existierenden Regel verknüpft: {V.linkElement}"
            elif V.linkKategorie == VorteilLinkKategorie.ÜberTalent and not V.linkElement in self.talente:
                errorStr = f"Vorteil {V.name} ist mit einem nicht-existierenden Talent verknüpft: {V.linkElement}"
            elif V.linkKategorie == VorteilLinkKategorie.Vorteil and not V.linkElement in self.vorteile:
                errorStr = f"Vorteil {V.name} ist mit einem nicht-existierenden Vorteil verknüpft: {V.linkElement}"
            if errorStr:
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
            if T.kategorie >= len(self.einstellungen['Talente: Kategorien'].wert):
                errorStr = f"Talent {fert.name} hat eine unbekannte Kategorie."
                self.loadingErrors.append([T, errorStr])
                logging.warning(errorStr)

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
                T.fertigkeiten.append(fert)

        #Freie Fertigkeiten
        for fert in self.freieFertigkeiten.values():
            if fert.kategorie >= len(self.einstellungen['FreieFertigkeiten: Kategorien'].wert):
                errorStr = f"Freie Fertigkeit {fert.name} hat eine unbekannte Kategorie."
                self.loadingErrors.append([fert, errorStr])
                logging.warning(errorStr)

        #Fertigkeiten     
        for fert in self.fertigkeiten.values():
            if fert.kategorie >= len(self.einstellungen['Fertigkeiten: Kategorien profan'].wert):
                errorStr = f"Fertigkeit {fert.name} hat eine unbekannte Kategorie."
                self.loadingErrors.append([fert, errorStr])
                logging.warning(errorStr)

            for attribut in fert.attribute:
                if not attribut in self.attribute:
                    errorStr = f"Fertigkeit {fert.name} referenziert ein nicht-existierendes Attribut: {attribut}"
                    self.loadingErrors.append([fert, errorStr])
                    logging.warning(errorStr)

        for fert in self.übernatürlicheFertigkeiten.values():
            if fert.kategorie >= len(self.einstellungen['Fertigkeiten: Kategorien übernatürlich'].wert):
                errorStr = f"Übernatürliche Fertigkeit {fert.name} hat eine unbekannte Kategorie."
                self.loadingErrors.append([fert, errorStr])
                logging.warning(errorStr)

            for attribut in fert.attribute:
                if not attribut in self.attribute:
                    errorStr = f"Übernatürliche Fertigkeit {fert.name} referenziert ein nicht-existierendes Attribut: {attribut}"
                    self.loadingErrors.append([fert, errorStr])
                    logging.warning(errorStr)

        #Rüstungen:
        for r in self.rüstungen.values():
            errorStr = ""

            if r.kategorie >= len(self.einstellungen['Rüstungen: Kategorien'].wert):
                errorStr = "Rüstung {r.name} hat eine unbekannte Kategorie."
                self.loadingErrors.append([r, errorStr])
                logging.warning(errorStr)

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

        #Regeln:
        for r in self.regeln.values():
            errorStr = ""

            if r.kategorie >= len(self.einstellungen['Regeln: Kategorien'].wert):
                errorStr = "Regel {r.name} hat eine unbekannte Kategorie."
                self.loadingErrors.append([r, errorStr])
                logging.warning(errorStr)

        self.loadingErrors = EventBus.applyFilter("datenbank_verify", self.loadingErrors, { "datenbank" : self })   
    
    def findKampfstile(self):
        kampfstilVorteile = [vort for vort in self.vorteile.values() if vort.kategorie == self.einstellungen["Vorteile: Kampfstil Kategorie"].wert and vort.name.endswith(" I")]

        kampfstile = []
        for vort in kampfstilVorteile:
            kampfstile.append(vort.name[:-2])
        return kampfstile