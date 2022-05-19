from Wolke import Wolke
import re
import math
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import Objekte
from Fertigkeiten import VorteilLinkKategorie
from CharakterPrintUtility import CharakterPrintUtility
from EventBus import EventBus

class CheatsheetGenerator(object):

    def __init__(self):
        self.ruleCategories = []

        self.rulesLineCount = 100
        self.rulesCharCount = 80

        self.reihenfolge = Wolke.DB.einstellungen["Regelanhang: Reihenfolge"].toTextList()
        self.aktiveManöverTypen = [int(m[1:]) for m in self.reihenfolge if m[0] == "M"]
        self.aktiveVorteilTypen = [int(v[1:]) for v in self.reihenfolge if v[0] == "V"]

    def formatCategory(self, category):
        return "===== " + category.upper() + " ====="

    def updateFontSize(self):
        self.rulesLineCount = 100
        self.rulesCharCount = 80
        fontSize = Wolke.Char.regelnGroesse
        if fontSize == 1:
            self.rulesLineCount = 80
            self.rulesCharCount = 55
        elif fontSize == 2:
            self.rulesLineCount = 60
            self.rulesCharCount = 45

    def getLineCount(self, text):
        lines = text.split("\n")
        lineCount = 0
        for line in lines:
            lineCount += max(int(math.ceil(len(line) / self.rulesCharCount)), 1)
        lineCount = lineCount - 1 #every text ends with two newlines, the second doesnt count, subtract 1

        #the largest fontsize tends to generate more lines because of missing hyphenation
        if Wolke.Char.regelnGroesse > 1:
            lineCount += int(lineCount * 0.2)

        return lineCount

    def appendWaffeneigenschaften(self, rules, lineCounts, category, eigenschaften):
        if not eigenschaften or (len(eigenschaften) == 0):
            return
        rules.append(category + "\n\n")
        lineCounts.append(self.getLineCount(rules[-1]))
        count = 0
        for weName, waffen in sorted(eigenschaften.items()):
            we = Wolke.DB.waffeneigenschaften[weName]
            if not we.text:
                continue
            count += 1
            rules.append(we.name + " (" + ", ".join(waffen) + ")\n" + we.text + "\n\n")
            lineCounts.append(self.getLineCount(rules[-1]))

        if count == 0:
            rules.pop()
            lineCounts.pop()

    def isLinkedToAny(self, vorteil):
        if vorteil.linkKategorie == VorteilLinkKategorie.ManöverMod:
            return vorteil.linkElement in Wolke.DB.manöver and Wolke.DB.manöver[vorteil.linkElement].typ in self.aktiveManöverTypen
        elif vorteil.linkKategorie == VorteilLinkKategorie.ÜberTalent:
            for fer in Wolke.Char.übernatürlicheFertigkeiten:
                if vorteil.linkElement in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                    return True
        elif vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if vorteil.linkElement in Wolke.Char.vorteile and Wolke.DB.vorteile[vorteil.linkElement].typ in self.aktiveVorteilTypen:
                return True
            return self.isLinkedToAny(Wolke.DB.vorteile[vorteil.linkElement])

        return False

    def appendVorteile(self, rules, lineCounts, category, vorteile):
        if not vorteile or (len(vorteile) == 0):
            return
        rules.append(category + "\n\n")
        lineCounts.append(self.getLineCount(rules[-1]))
        count = 0
        for vor in vorteile:
            vorteil = Wolke.DB.vorteile[vor]
            if not vorteil.cheatsheetAuflisten or self.isLinkedToAny(vorteil):
                continue

            beschreibung = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
            if not beschreibung:
                continue
            if "\n" in beschreibung:
                beschreibung = "- " + beschreibung.replace("\n", "\n- ")

            count += 1
            result = []
            result.append(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil))
            result.append("\n")
            result.append(beschreibung)
            result.append("\n\n")
            rules.append("".join(result))
            lineCounts.append(self.getLineCount(rules[-1]))
        
        if count == 0:
            rules.pop()
            lineCounts.pop()
    
    def appendManöver(self, rules, lineCounts, category, manöverList):
        if not manöverList or (len(manöverList) == 0):
            return
        rules.append(category + "\n\n")
        lineCounts.append(self.getLineCount(rules[-1]))
        count = 0
        for man in manöverList:
            manöver = Wolke.DB.manöver[man]
            if not Wolke.Char.voraussetzungenPrüfen(manöver.voraussetzungen):
                continue
            count += 1
            result = []
            if manöver.name.endswith(" (M)") or manöver.name.endswith(" (L)") or manöver.name.endswith(" (D)"):
                result.append(manöver.name[:-4])
            elif manöver.name.endswith(" (FK)"):
                result.append(manöver.name[:-5])
            else:
                result.append(manöver.name)
            if manöver.probe:
                result.append(" (" + manöver.probe + ")")
            result.append("\n")
            if manöver.gegenprobe:
                result.append("Gegenprobe: " + manöver.gegenprobe + "\n")

            result.append(manöver.text)
           
            for vor in Wolke.Char.vorteile:
                vorteil = Wolke.DB.vorteile[vor]
                if CharakterPrintUtility.isLinkedTo(Wolke.Char, vorteil, VorteilLinkKategorie.ManöverMod, man):
                    beschreibung = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
                    if not beschreibung:
                        continue
                    result.append("\n=> ")
                    result.append(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil))
                    result.append(": ")
                    result.append(beschreibung.replace("\n", " "))

            result.append("\n\n")
            rules.append("".join(result))
            lineCounts.append(self.getLineCount(rules[-1]))

        if count == 0:
            rules.pop()
            lineCounts.pop()

    def appendTalente(self, rules, lineCounts, category, talente):
        if not talente or (len(talente) == 0):
            return
        rules.append(category + "\n\n")
        lineCounts.append(self.getLineCount(rules[-1]))
        count = 0
        for tal in talente:
            result = []
            if not tal.cheatsheetAuflisten or not tal.text:
                continue
            count += 1
            result.append(tal.anzeigeName)
            result.append(" (PW " + str(tal.pw) + ")")
            result.append("\n")
            text = tal.text
            
            #Remove everything from Sephrasto on
            index = text.find('\nSephrasto')
            if index != -1:
                text = text[:index]

            #Remove everything from Anmerkung on but keep the text and append it later
            index = text.find('\nAnmerkung')
            anmerkung = ""
            if index != -1:
                anmerkung = text[index:]
                text = text[:index]

            #Remove everything from Fertigkeiten on
            index = text.find('\nFertigkeiten')
            if index != -1:
                text = text[:index]

            #Remove everything from Erlernen on (some talents don't have a Fertigkeiten list)
            index = text.find('\nErlernen')
            if index != -1:
                text = text[:index]

            result.append(text)
            if anmerkung:
                result.append(anmerkung)

            for vor in Wolke.Char.vorteile:
                vorteil = Wolke.DB.vorteile[vor]
                if CharakterPrintUtility.isLinkedTo(Wolke.Char, vorteil, VorteilLinkKategorie.ÜberTalent, tal.na):
                    beschreibung = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
                    if not beschreibung:
                        continue
                    result.append("\n=> ")
                    result.append(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil))
                    result.append(": ")
                    result.append(beschreibung.replace("\n", " "))

            result.append("\n\n")
            rules.append("".join(result))
            lineCounts.append(self.getLineCount(rules[-1]))

        if count == 0:
            rules.pop()
            lineCounts.pop()

    def appendGeneric(self, category, text, rules, lineCounts):
        if category:
            formattedCategory = self.formatCategory(category)
            self.ruleCategories.append(formattedCategory)
            rules.append(formattedCategory + "\n\n")
            lineCounts.append(self.getLineCount(rules[-1]))
        rules.append(text)
        lineCounts.append(self.getLineCount(rules[-1]))

    def prepareRules(self):
        voraussetzungenPruefen = Wolke.Char.voraussetzungenPruefen
        Wolke.Char.voraussetzungenPruefen = True

        self.updateFontSize()
        self.ruleCategories = []
        sortV = Wolke.Char.vorteile.copy()
        sortV = sorted(sortV, key=str.lower)

        sortM = list(Wolke.DB.manöver.keys())
        sortM = sorted(sortM, key=str.lower)

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
        ruleLineCounts = []

        manöverMergeScript = Wolke.DB.einstellungen["Regelanhang: Manöver Mergescript"].toText()
        vorteilTypen = Wolke.DB.einstellungen["Vorteile: Typen"].toTextList()
        manöverTypen = Wolke.DB.einstellungen["Manöver: Typen"].toTextList()

        vorteileGruppiert = []
        for i in range(len(vorteilTypen)):
            vorteileGruppiert.append([el for el in sortV if Wolke.DB.vorteile[el].typ == i])

        manöverGruppiert = []
        for i in range(len(manöverTypen)):
            manöverGruppiert.append([])
        for i in range(len(manöverTypen)):
            scriptVariables = { "char" : Wolke.Char, "typ" : i, "mergeTo" : i }
            exec(manöverMergeScript, scriptVariables)
            mergeTo = scriptVariables["mergeTo"]
            if mergeTo >= len(manöverTypen):
                mergeTo = i
            empty = len(manöverGruppiert[mergeTo]) == 0
            manöverGruppiert[mergeTo].extend([el for el in sortM if (Wolke.DB.manöver[el].typ == i)])
            if not empty:
                manöverGruppiert[mergeTo] = sorted(manöverGruppiert[mergeTo])

        for r in self.reihenfolge:
            if not r in Wolke.Char.regelnKategorien:
                continue

            if r[0] == "V":
                typ = int(r[1:])
                if typ >= len(vorteileGruppiert):
                    continue
                self.ruleCategories.append(self.formatCategory(vorteilTypen[typ]))
                self.appendVorteile(rules, ruleLineCounts, self.ruleCategories[-1], vorteileGruppiert[typ])
            elif r[0] == "M":
                typ = int(r[1:])
                if typ >= len(manöverGruppiert):
                    continue
                self.ruleCategories.append(self.formatCategory(manöverTypen[typ]))
                self.appendManöver(rules, ruleLineCounts, self.ruleCategories[-1], manöverGruppiert[typ])
            elif r[0] == "W":
                self.ruleCategories.append(self.formatCategory("Waffeneigenschaften"))
                self.appendWaffeneigenschaften(rules, ruleLineCounts, self.ruleCategories[-1], waffeneigenschaften)
            elif r[0] == "Z":
                self.ruleCategories.append(self.formatCategory("Zauber"))
                self.appendTalente(rules, ruleLineCounts, self.ruleCategories[-1], zauber)
            elif r[0] == "L":
                self.ruleCategories.append(self.formatCategory("Liturgien"))
                self.appendTalente(rules, ruleLineCounts, self.ruleCategories[-1], liturgien)
            elif r[0] == "A":
                self.ruleCategories.append(self.formatCategory("Anrufungen"))
                self.appendTalente(rules, ruleLineCounts, self.ruleCategories[-1], anrufungen)
            
            EventBus.doAction("regelanhang_anfuegen", { "reihenfolge" : r, "appendCallback" : lambda category, text, r=rules, l=ruleLineCounts: self.appendGeneric(category, text, r, l) })

        Wolke.Char.voraussetzungenPruefen = voraussetzungenPruefen
        return rules, ruleLineCounts
        

    def writeRules(self, rules, ruleLineCounts, start):
        lineCount = 0
        endIndex = start

        while lineCount < self.rulesLineCount and endIndex < len(ruleLineCounts):
            nextLineCount = ruleLineCounts[endIndex] - 1 #subtract one because every entry ends with a newline
            leeway = int(nextLineCount * 0.3) #give big texts some leeway on the target line count to avoid big empty spaces
            if lineCount + nextLineCount > self.rulesLineCount + leeway:
                break
            lineCount = lineCount + ruleLineCounts[endIndex]
            endIndex = endIndex + 1

        if endIndex <= start:
            return "", -1

        #Make sure a category is never the last line on the page
        category = rules[endIndex-1][:-2]
        if category in self.ruleCategories:
            lineCount -= ruleLineCounts[endIndex-1]
            endIndex = endIndex - 1

        #Remove the trailing new line from the last entry
        rules[endIndex-1] = rules[endIndex-1][:-2]
        lineCount -= 1

        result = ''.join(rules[start:endIndex])

        # Append newlines to make the auto-fontsize about same as large as the other pages
        if self.rulesLineCount - lineCount > 0:
            result += '\n' * (self.rulesLineCount - lineCount)

        if len(rules) == endIndex:
            #return -1 to signal that we are done
            return result, -1
        return result, endIndex