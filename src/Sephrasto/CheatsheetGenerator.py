from Wolke import Wolke
import re
import math
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import Objekte
from Fertigkeiten import VorteilLinkKategorie
from CharakterPrintUtility import CharakterPrintUtility

class CheatsheetGenerator(object):

    def __init__(self):
        self.RuleCategories = []

        self.RulesLineCount = 100
        self.RulesCharCount = 80

        self.reihenfolge = Wolke.DB.einstellungen["Regelanhang: Reihenfolge"].toTextList()
        self.aktiveManöverTypen = [int(m[1:]) for m in self.reihenfolge if m[0] == "M"]
        self.aktiveVorteilTypen = [int(v[1:]) for v in self.reihenfolge if v[0] == "V"]

    def formatCategory(self, category):
        return "===== " + category.upper() + " ====="

    def updateFontSize(self):
        self.RulesLineCount = 100
        self.RulesCharCount = 80
        fontSize = Wolke.Char.regelnGroesse
        if fontSize == 1:
            self.RulesLineCount = 80
            self.RulesCharCount = 55
        elif fontSize == 2:
            self.RulesLineCount = 60
            self.RulesCharCount = 45

    def getLineCount(self, text):
        lines = text.split("\n")
        lineCount = 0
        for line in lines:
            lineCount += max(int(math.ceil(len(line) / self.RulesCharCount)), 1)
        lineCount = lineCount - 1 #every text ends with two newlines, the second doesnt count, subtract 1

        #the largest fontsize tends to more lines beause of missing hyphenation
        if Wolke.Settings["Cheatsheet-Fontsize"] > 1:
            lineCount += int(lineCount * 0.2)

        return lineCount

    def appendWaffeneigenschaften(self, strList, lineCounts, category, eigenschaften):
        if not eigenschaften or (len(eigenschaften) == 0):
            return
        strList.append(category + "\n\n")
        lineCounts.append(self.getLineCount(strList[-1]))
        count = 0
        for weName, waffen in sorted(eigenschaften.items()):
            we = Wolke.DB.waffeneigenschaften[weName]
            if not we.text:
                continue
            count += 1
            strList.append(we.name + " (" + ", ".join(waffen) + ")\n" + we.text + "\n\n")
            lineCounts.append(self.getLineCount(strList[-1]))

        if count == 0:
            strList.pop()
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

    def appendVorteile(self, strList, lineCounts, category, vorteile):
        if not vorteile or (len(vorteile) == 0):
            return
        strList.append(category + "\n\n")
        lineCounts.append(self.getLineCount(strList[-1]))
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
            strList.append("".join(result))
            lineCounts.append(self.getLineCount(strList[-1]))
        
        if count == 0:
            strList.pop()
            lineCounts.pop()
    
    def appendManöver(self, strList, lineCounts, category, manöverList):
        if not manöverList or (len(manöverList) == 0):
            return
        strList.append(category + "\n\n")
        lineCounts.append(self.getLineCount(strList[-1]))
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
            strList.append("".join(result))
            lineCounts.append(self.getLineCount(strList[-1]))

        if count == 0:
            strList.pop()
            lineCounts.pop()

    def appendTalente(self, strList, lineCounts, category, talente):
        if not talente or (len(talente) == 0):
            return
        strList.append(category + "\n\n")
        lineCounts.append(self.getLineCount(strList[-1]))
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
            strList.append("".join(result))
            lineCounts.append(self.getLineCount(strList[-1]))

        if count == 0:
            strList.pop()
            lineCounts.pop()

    def prepareRules(self):
        self.updateFontSize()
        self.RuleCategories = []
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
            if r[0] == "V":
                typ = int(r[1:])
                if typ >= len(vorteileGruppiert):
                    continue
                self.RuleCategories.append(self.formatCategory(vorteilTypen[typ]))
                self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[-1], vorteileGruppiert[typ])
            elif r[0] == "M":
                typ = int(r[1:])
                if typ >= len(manöverGruppiert):
                    continue
                self.RuleCategories.append(self.formatCategory(manöverTypen[typ]))
                self.appendManöver(rules, ruleLineCounts, self.RuleCategories[-1], manöverGruppiert[typ])
            elif r[0] == "W":
                self.RuleCategories.append(self.formatCategory("Waffeneigenschaften"))
                self.appendWaffeneigenschaften(rules, ruleLineCounts, self.RuleCategories[-1], waffeneigenschaften)
            elif r[0] == "Z":
                self.RuleCategories.append(self.formatCategory("Zauber"))
                self.appendTalente(rules, ruleLineCounts, self.RuleCategories[-1], zauber)
            elif r[0] == "L":
                self.RuleCategories.append(self.formatCategory("Liturgien"))
                self.appendTalente(rules, ruleLineCounts, self.RuleCategories[-1], liturgien)
            elif r[0] == "A":
                self.RuleCategories.append(self.formatCategory("Anrufungen"))
                self.appendTalente(rules, ruleLineCounts, self.RuleCategories[-1], anrufungen)

        return rules, ruleLineCounts
        

    def writeRules(self, rules, ruleLineCounts, start):
        lineCount = 0
        endIndex = start

        while lineCount < self.RulesLineCount and endIndex < len(ruleLineCounts):
            nextLineCount = ruleLineCounts[endIndex] - 1 #subtract one because every entry ends with a newline
            leeway = int(nextLineCount * 0.3) #give big texts some leeway on the target line count to avoid big empty spaces
            if lineCount + nextLineCount > self.RulesLineCount + leeway:
                break
            lineCount = lineCount + ruleLineCounts[endIndex]
            endIndex = endIndex + 1

        if endIndex <= start:
            return "", -1

        #Make sure a category is never the last line on the page
        category = rules[endIndex-1][:-2]
        if category in self.RuleCategories:
            lineCount -= ruleLineCounts[endIndex-1]
            endIndex = endIndex - 1

        #Remove the trailing new line from the last entry
        rules[endIndex-1] = rules[endIndex-1][:-2]
        lineCount -= 1

        result = ''.join(rules[start:endIndex])

        # Append newlines to make the auto-fontsize about same as large as the other pages
        if self.RulesLineCount - lineCount > 0:
            result += '\n' * (self.RulesLineCount - lineCount)

        if len(rules) == endIndex:
            #return -1 to signal that we are done
            return result, -1
        return result, endIndex