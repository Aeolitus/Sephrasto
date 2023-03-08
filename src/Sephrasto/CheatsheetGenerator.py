from Wolke import Wolke
import re
import math
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import Objekte
from Fertigkeiten import VorteilLinkKategorie
from CharakterPrintUtility import CharakterPrintUtility
from EventBus import EventBus

# The qt web engine then doesnt handle column-break in print layout properly,
# so we have to hack around a bit by placing titles and categories inside the individual articles before the actual rule element header.
# Maybe in the future qt will upgrade to a newer chromium that supports that css property...
class CheatsheetGenerator(object):

    def __init__(self):
        self.reihenfolge = Wolke.DB.einstellungen["Regelanhang: Reihenfolge"].toTextList()
        self.aktiveRegelTypen = [int(r[2:]) for r in self.reihenfolge if r[0] == "R" and len(r) > 2 and r[2:].isnumeric()]
        self.aktiveVorteilTypen = [int(r[2:]) for r in self.reihenfolge if r[0] == "V" and len(r) > 2 and r[2:].isnumeric()]

    @staticmethod
    def categoryHeading(title, category):
        return title + "<span class='ruleCategoryHeading'>" + category + "</span><br>"

    @staticmethod
    def ruleHeading(text):
        return "<span class='ruleHeading'>" + text + "</span><br>"

    def appendWaffeneigenschaften(self, rules, category, eigenschaften):
        if not eigenschaften or (len(eigenschaften) == 0):
            return
        rules.append("<article>" + category)
        count = 0
        for weName, waffen in sorted(eigenschaften.items()):
            we = Wolke.DB.waffeneigenschaften[weName]
            if not we.text:
                continue
            count += 1
            if count != 1:
                rules.append("<article>")
            rules.append(CheatsheetGenerator.ruleHeading(we.name + " (" + ", ".join(waffen) + ")") + we.text + "</article>")

        if count == 0:
            rules.pop()
            return False
        return True

    def isLinkedToAny(self, vorteil):
        if vorteil.linkKategorie == VorteilLinkKategorie.Regel:
            return vorteil.linkElement in Wolke.DB.regeln and Wolke.DB.regeln[vorteil.linkElement].typ in self.aktiveRegelTypen
        elif vorteil.linkKategorie == VorteilLinkKategorie.ÜberTalent:
            for fer in Wolke.Char.übernatürlicheFertigkeiten:
                if vorteil.linkElement in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                    return True
        elif vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if vorteil.linkElement in Wolke.Char.vorteile and Wolke.DB.vorteile[vorteil.linkElement].typ in self.aktiveVorteilTypen:
                return True
            return self.isLinkedToAny(Wolke.DB.vorteile[vorteil.linkElement])

        return False

    def appendVorteile(self, rules, category, vorteile):
        if not vorteile or (len(vorteile) == 0):
            return
        rules.append("<article>" + category)
        count = 0
        for vor in vorteile:
            vorteil = Wolke.DB.vorteile[vor]
            if not vorteil.cheatsheetAuflisten or self.isLinkedToAny(vorteil):
                continue

            text = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
            if not text:
                continue

            count += 1
            result = []
            if count != 1:
                result.append("<article>")
            result.append(CheatsheetGenerator.ruleHeading(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil)))

            if "\n" in text:
                text = "<ul><li> " + text.replace("\n", "</li><li>") + "</ul>"
            result.append(text)
            result.append("</article>")
            rules.append("".join(result))
        
        if count == 0:
            rules.pop()
            return False
        return True
    
    def appendRegeln(self, rules, category, regelList):
        if not regelList or (len(regelList) == 0):
            return
        rules.append("<article>" + category)
        count = 0
        for man in regelList:
            regel = Wolke.DB.regeln[man]
            if not Wolke.Char.voraussetzungenPrüfen(regel.voraussetzungen):
                continue
            count += 1
            result = []
            if count != 1:
                result.append("<article>")
            name = regel.name
            for trim in [" (M)", " (L)", "(D)", " (FK)"]:
                if name.endswith(trim):
                    name = name[:-len(trim)]
            if regel.probe:
                name += " (" + regel.probe + ")"
            result.append(CheatsheetGenerator.ruleHeading(name))
            result.append(regel.text)
           
            linkedText = []
            for vor in Wolke.Char.vorteile:
                vorteil = Wolke.DB.vorteile[vor]
                if CharakterPrintUtility.isLinkedTo(Wolke.Char, vorteil, VorteilLinkKategorie.Regel, man):
                    beschreibung = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
                    if not beschreibung:
                        continue
                    linkedText.append("<li class='checkbox'>")
                    linkedText.append(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil))
                    linkedText.append(": ")
                    linkedText.append(beschreibung.replace("\n", " "))
                    linkedText.append("</li>")
            if len(linkedText) > 0:
                result.append("<ul>" + "".join(linkedText) + "</ul>")

            result.append("</article>")
            rules.append("".join(result))

        if count == 0:
            rules.pop()
            return False
        return True

    def appendTalente(self, rules, category, talente):
        if not talente or (len(talente) == 0):
            return
        rules.append("<article>" + category)
        count = 0
        for tal in talente:       
            if not tal.cheatsheetAuflisten or not tal.text:
                continue
            count += 1
            result = []
            if count != 1:
                result.append("<article>")
            result.append(CheatsheetGenerator.ruleHeading(tal.anzeigeName + " (PW " + str(tal.pw) + ")"))
            text = Wolke.DB.talente[tal.na].text
            
            #Remove everything from Sephrasto on
            index = text.find('\n<b>Sephrasto')
            if index != -1:
                text = text[:index]

            #Remove everything from Anmerkung on but keep the text and append it later
            index = text.find('\n<b>Anmerkung')
            anmerkung = ""
            if index != -1:
                anmerkung = text[index:]
                text = text[:index]

            #Remove everything from Fertigkeiten on
            index = text.find('\n<b>Fertigkeiten')
            if index != -1:
                text = text[:index]

            #Remove everything from Erlernen on (some talents don't have a Fertigkeiten list)
            index = text.find('\n<b>Erlernen')
            if index != -1:
                text = text[:index]

            result.append(text)
            if anmerkung:
                result.append(anmerkung)

            linkedText = []
            for vor in Wolke.Char.vorteile:
                vorteil = Wolke.DB.vorteile[vor]
                if CharakterPrintUtility.isLinkedTo(Wolke.Char, vorteil, VorteilLinkKategorie.ÜberTalent, tal.na):
                    beschreibung = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
                    if not beschreibung:
                        continue
                    linkedText.append("<li class='checkbox'>")
                    linkedText.append(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil))
                    linkedText.append(": ")
                    linkedText.append(beschreibung.replace("\n", " "))
                    linkedText.append("</li>")
            if len(linkedText) > 0:
                result.append("<ul>" + "".join(linkedText) + "</ul>")

            result.append("</article>")
            rules.append("".join(result))

        if count == 0:
            rules.pop()
            return False
        return True

    def generateRules(self):
        voraussetzungenPruefen = Wolke.Char.voraussetzungenPruefen
        Wolke.Char.voraussetzungenPruefen = True

        sortV = Wolke.Char.vorteile.copy()
        sortV = sorted(sortV, key=str.lower)

        sortR = list(Wolke.DB.regeln.keys())
        sortR = sorted(sortR, key=str.lower)

        waffeneigenschaften = {}
        for waffe in Wolke.Char.waffen:
            for el in waffe.eigenschaften:
                try:
                    we = Hilfsmethoden.GetWaffeneigenschaft(el, Wolke.DB)
                    if not we.name in waffeneigenschaften:
                        waffeneigenschaften[we.name] = [waffe.anzeigename]
                    else:
                        waffeneigenschaften[we.name].append(waffe.anzeigename)
                except WaffeneigenschaftException:
                    pass      
        
        fertigkeitsTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen übernatürlich"].toTextList()
        talentboxList = CharakterPrintUtility.getÜberTalente(Wolke.Char)
        (zauber, liturgien, anrufungen) = CharakterPrintUtility.groupUeberTalente(talentboxList)

        rules = []

        regelMergeScript = Wolke.DB.einstellungen["Regelanhang: Regel Mergescript"].toText()
        vorteilTypen = Wolke.DB.einstellungen["Vorteile: Typen"].toTextList()
        regelTypen = Wolke.DB.einstellungen["Regeln: Typen"].toTextList()

        vorteileGruppiert = []
        for i in range(len(vorteilTypen)):
            vorteileGruppiert.append([el for el in sortV if Wolke.DB.vorteile[el].typ == i])

        regelnGruppiert = []
        for i in range(len(regelTypen)):
            regelnGruppiert.append([])
        for i in range(len(regelTypen)):
            scriptVariables = { "char" : Wolke.Char, "typ" : i, "mergeTo" : i }
            exec(regelMergeScript, scriptVariables)
            mergeTo = scriptVariables["mergeTo"]
            if mergeTo >= len(regelTypen):
                mergeTo = i
            empty = len(regelnGruppiert[mergeTo]) == 0
            regelnGruppiert[mergeTo].extend([el for el in sortR if (Wolke.DB.regeln[el].typ == i)])
            if not empty:
                regelnGruppiert[mergeTo] = sorted(regelnGruppiert[mergeTo])

        lastTitle = ""
        title = ""
        for r in self.reihenfolge:
            if r[0] == "T" and len(r) > 2:
                if lastTitle and len(rules) > 0 and rules[-1] == lastTitle:
                    rules.pop()
                title = "<h1 class='title'>" + r[2:] + "</h1>"
                lastTitle = title
            if not r in Wolke.Char.regelnKategorien:
                continue
            if r[0] == "V" and len(r) > 2 and r[2:].isnumeric():
                typ = int(r[2:])
                if typ >= len(vorteileGruppiert):
                    continue
                if self.appendVorteile(rules, CheatsheetGenerator.categoryHeading(title, vorteilTypen[typ]), vorteileGruppiert[typ]):
                    title = ""
            elif r[0] == "R" and len(r) > 2 and r[2:].isnumeric():
                typ = int(r[2:])
                if typ >= len(regelnGruppiert):
                    continue
                if self.appendRegeln(rules, CheatsheetGenerator.categoryHeading(title, regelTypen[typ]), regelnGruppiert[typ]):
                    title = ""
            elif r[0] == "W":
                if self.appendWaffeneigenschaften(rules, CheatsheetGenerator.categoryHeading(title, "Waffeneigenschaften"), waffeneigenschaften):
                    title = ""
            elif r[0] == "Z":
                if self.appendTalente(rules, CheatsheetGenerator.categoryHeading(title, "Zauber"), zauber):
                    title = ""
            elif r[0] == "L":
                if self.appendTalente(rules, CheatsheetGenerator.categoryHeading(title, "Liturgien"), liturgien):
                    title = ""
            elif r[0] == "A":
                if self.appendTalente(rules, CheatsheetGenerator.categoryHeading(title, "Anrufungen"), anrufungen):
                    title = ""
            
            EventBus.doAction("regelanhang_anfuegen", { "reihenfolge" : r, "appendCallback" : lambda text: rules.append(text) })

        if lastTitle and len(rules) > 0 and rules[-1] == lastTitle:
            rules.pop()

        Wolke.Char.voraussetzungenPruefen = voraussetzungenPruefen
        rules = Hilfsmethoden.fixHtml("".join(rules))
        return rules