from Wolke import Wolke
import re
import math
from difflib import SequenceMatcher
from fractions import Fraction
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import Objekte
from Fertigkeiten import VorteilLinkKategorie
from CharakterPrintUtility import CharakterPrintUtility

class CheatsheetGenerator(object):

    def __init__(self):
        self.RuleCategories = []

        self.RulesLineCount = 100
        self.RulesCharCount = 80
        fontSize = Wolke.Settings["Cheatsheet-Fontsize"]
        if fontSize == 1:
            self.RulesLineCount = 80
            self.RulesCharCount = 55
        elif fontSize == 2:
            self.RulesLineCount = 60
            self.RulesCharCount = 45

        #used to abbreviate names when merged
        self.abbreviations = Wolke.DB.einstellungen["CharsheetVerknüpfungsAbkürzungen"].toTextDict('\n', False)

    textToFraction = {
        "ein Achtel" : "1/8",
        "ein Viertel" : "1/4",
        "die Hälfte" : "1/2",
        "drei Viertel" : "3/4",
    }

    def formatCategory(self, category):
        return "===== " + category.upper() + " ====="

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

    def prepareDescription(self, description):
        #convert text to fractions
        for k,v in CheatsheetGenerator.textToFraction.items():
            description = description.replace(k, v)

        #Split by "." or "\n". Match '.' only if not prefixed by S or bzw, alternatively match newline
        strList = re.split(r'(?<!S)(?<!bzw)\.|\n', description, re.UNICODE)
        if strList[-1] == "":
            strList.pop()

        for i in range(len(strList)):
            strList[i] = strList[i].strip()
            if strList[i] == "":
                strList[i] = "\n" #restore newlines
            else:
                strList[i] += ". "

        return strList

    def finalizeDescription(self, strList):
        result = ""
        for text in strList:
            if text == "\n":
                result = result.strip() + "\n"
            else:
                result += text

        #convert fractions back to text
        for k,v in CheatsheetGenerator.textToFraction.items():
            result = result.replace(v, k)

        return result.strip()

    def mergeDescriptions(self, str1, str2):
        #match numbers or fractions, + is ignored, nums with prefix S. are skipped
        reNumbers = re.compile(r'-?\d+/\d+|-?\d+', re.UNICODE)

        lines1 = self.prepareDescription(str1)
        lines2 = self.prepareDescription(str2)

        for i in range(len(lines1)):
            if lines1[i] == "\n":
                continue

            res = reNumbers.findall(lines1[i])

            #case 1: no number contained, just merge duplicate lines
            if len(res) == 0:
                for j in range(len(lines2)):
                    if lines1[i] == lines2[j]:
                        lines2[j] = "" #will be removed later
                continue

            #case 2: number(s) contained, merge similar lines by adding numbers
            values = []
            for val in res:
                values.append(Fraction(val))

            tmpLine1 = reNumbers.sub("", lines1[i]) #remove the number before comparing with other lines
            for j in range(len(lines2)):
                if lines2[j] == "\n":
                    continue
                tmpLine2 = reNumbers.sub("", lines2[j]) #remove the number before comparing with other lines

                if SequenceMatcher(None, tmpLine1, tmpLine2).ratio() > 0.95: #fuzzy compare, 1 in 20 characters may be different
                    res = reNumbers.findall(lines2[j])
                    if len(res) != len(values):
                        continue

                    for k in range(len(res)):
                        values[k] += Fraction(res[k])

                    #Prefer text from str2 in case of ratio < 1, because higher vorteil levels
                    #tend to have higher values which leads to plural forms in the text
                    lines1[i] = lines2[j]
                    lines2[j] = "" #will be removed later

            #now replace the added numbers
            subCount = -1
            def count_repl(mobj):
                nonlocal subCount
                subCount += 1
                return str(values[subCount])

            lines1[i] = reNumbers.sub(count_repl, lines1[i])

        lines2 = [x for x in lines2 if x != ""]
        if len(lines2) > 0:
            lines1.append("\n")
            lines1.extend(lines2)
        return self.finalizeDescription(lines1)

    def isCheatsheetLinkedToAny(self, vorteil):
        if vorteil.linkKategorie == VorteilLinkKategorie.ManöverMod:
            return vorteil.linkElement in Wolke.DB.manöver
        elif vorteil.linkKategorie == VorteilLinkKategorie.ÜberTalent:
            for fer in Wolke.Char.übernatürlicheFertigkeiten:
                if vorteil.linkElement in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                    return True
        elif vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if vorteil.linkElement in Wolke.Char.vorteile:
                return True
            return self.isCheatsheetLinkedToAny(Wolke.DB.vorteile[vorteil.linkElement])

        return False
    
    def isCheatsheetLinkedTo(self, vorteil, kategorie, element):
        if kategorie == VorteilLinkKategorie.ManöverMod and vorteil.linkKategorie == VorteilLinkKategorie.ManöverMod:
            return vorteil.linkElement == element
        elif kategorie == VorteilLinkKategorie.ÜberTalent and vorteil.linkKategorie == VorteilLinkKategorie.ÜberTalent:
            if vorteil.linkElement == element:
                for fer in Wolke.Char.übernatürlicheFertigkeiten:
                    if vorteil.linkElement in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                        return True
        elif vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if kategorie == VorteilLinkKategorie.Vorteil and vorteil.linkElement == element and (vorteil.linkElement in Wolke.Char.vorteile):
                return True
            if vorteil.linkElement in Wolke.Char.vorteile:
                return False
            return self.isCheatsheetLinkedTo(Wolke.DB.vorteile[vorteil.linkElement], kategorie, element)            

        return False

    def getLinkedName(self, vorteil, forceKommentar = False):
        name = vorteil.getFullName(Wolke.Char, forceKommentar)
        vorteilsnamenErsetzen = [int(typ) for typ in Wolke.DB.einstellungen["CharsheetVorteilsnamenErsetzen"].toTextList()]

        for vor2 in Wolke.Char.vorteile:
            vorteil2 = Wolke.DB.vorteile[vor2]
            if self.isCheatsheetLinkedTo(vorteil2, VorteilLinkKategorie.Vorteil, vorteil.name):
                name2 = self.getLinkedName(vorteil2, forceKommentar)

                #allgemeine vorteile, kampfstile and traditionen only keep the last name (except vorteil is variable with a comment)
                if (not (vorteil.name in Wolke.Char.vorteileVariable) or not Wolke.Char.vorteileVariable[vorteil.name].kommentar)\
                   and (vorteil2.typ in vorteilsnamenErsetzen):
                    name = name2
                else:
                    fullset = [" I", " II", " III", " IV", " V", " VI", " VII"]
                    basename = ""
                    for el in fullset:
                        if vorteil.name.endswith(el): #use name without comment/ep cost to find basename
                            basename = vorteil.name[:-len(el)]
                            break
                    if basename and name2.startswith(basename):
                        name += "," + name2[len(basename):]
                    else:
                        name += ", " + name2

        if "," in name:
            nameStart = name[:name.index(",")]
            nameAbbreviate = name[name.index(","):]
            for k,v in self.abbreviations.items():
                nameAbbreviate = nameAbbreviate.replace(k, v)
            name = nameStart + nameAbbreviate
        return name

    def getLinkedDescription(self, vorteil):
        beschreibung = vorteil.cheatsheetBeschreibung.replace("\n\n", "\n")
        if beschreibung:
            if vorteil.name in Wolke.Char.vorteileVariable:
                if "$kommentar$" in beschreibung:
                    beschreibung = beschreibung.replace("$kommentar$", Wolke.Char.vorteileVariable[vorteil.name].kommentar)
        else:
            beschreibung = vorteil.text.replace("\n\n", "\n")

        for vor2 in Wolke.Char.vorteile:
            vorteil2 = Wolke.DB.vorteile[vor2]
            if self.isCheatsheetLinkedTo(vorteil2, VorteilLinkKategorie.Vorteil, vorteil.name):
                beschreibung2 = self.getLinkedDescription(vorteil2)

                if vorteil2.typ == 0:
                    #allgemeine vorteile replace the description of what they link to (except vorteil is variable with a comment)
                    if not (vorteil.name in Wolke.Char.vorteileVariable) or not Wolke.Char.vorteileVariable[vorteil.name].kommentar:
                        beschreibung = beschreibung2
                    else:
                        beschreibung += "\n" + beschreibung2
                else:
                    beschreibung = self.mergeDescriptions(beschreibung, beschreibung2)

        return beschreibung

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

    def appendVorteile(self, strList, lineCounts, category, vorteile):
        if not vorteile or (len(vorteile) == 0):
            return
        strList.append(category + "\n\n")
        lineCounts.append(self.getLineCount(strList[-1]))
        count = 0
        for vor in vorteile:
            vorteil = Wolke.DB.vorteile[vor]
            if not vorteil.cheatsheetAuflisten or self.isCheatsheetLinkedToAny(vorteil):
                continue

            beschreibung = self.getLinkedDescription(vorteil)
            if not beschreibung:
                continue
            if "\n" in beschreibung:
                beschreibung = "- " + beschreibung.replace("\n", "\n- ")

            count += 1
            result = []
            result.append(self.getLinkedName(vorteil))
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
                if self.isCheatsheetLinkedTo(vorteil, VorteilLinkKategorie.ManöverMod, man):
                    beschreibung = self.getLinkedDescription(vorteil)
                    if not beschreibung:
                        continue
                    result.append("\n=> ")
                    result.append(self.getLinkedName(vorteil))
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
            talent = Wolke.DB.talente[tal.na]
            if not talent.cheatsheetAuflisten or not talent.text:
                continue
            count += 1
            name = talent.getFullName(Wolke.Char)
            result.append(name)
            result.append(" (PW " + str(tal.pw) + ")")
            result.append("\n")
            text = talent.text
            
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
                if self.isCheatsheetLinkedTo(vorteil, VorteilLinkKategorie.ÜberTalent, talent.name):
                    beschreibung = self.getLinkedDescription(vorteil)
                    if not beschreibung:
                        continue
                    result.append("\n=> ")
                    result.append(self.getLinkedName(vorteil))
                    result.append(": ")
                    result.append(beschreibung.replace("\n", " "))

            result.append("\n\n")
            strList.append("".join(result))
            lineCounts.append(self.getLineCount(strList[-1]))

        if count == 0:
            strList.pop()
            lineCounts.pop()

    def prepareRules(self):
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
        
        fertigkeitsTypen = Wolke.DB.einstellungen["FertigkeitsTypenÜbernatürlich"].toTextList()
        talentboxList = CharakterPrintUtility.getÜberTalente(Wolke.Char)
        zauber = []
        liturgien = []
        anrufungen = []
        # We don't know which of the above types a talent is, so have have to guess... should work 99.99%
        for tal in talentboxList:
            if " AsP" in tal.ko:
                anrufungen.append(tal)
            elif " KaP" in tal.ko:
                liturgien.append(tal)
            elif " GuP" in tal.ko:
                anrufungen.append(tal)
            else:
                fertTyp = fertigkeitsTypen[tal.groupFert.printclass]
                if "Zauber" in fertTyp or "zauber" in fertTyp:
                    zauber.append(tal)
                elif "Liturgie" in fertTyp or "liturgie" in fertTyp:
                    liturgien.append(tal)
                elif "Anrufung" in fertTyp or "anrufung" in fertTyp:
                    anrufungen.append(tal)
                elif  ("Zauberer I" in Wolke.Char.vorteile) or ("Tradition der Borbaradianer I" in Wolke.Char.vorteile):
                    zauber.append(tal)
                elif "Geweiht I" in Wolke.Char.vorteile:
                    liturgien.append(tal)
                elif "Paktierer I" in Wolke.Char.vorteile:
                    anrufungen.append(tal)
                else:
                    zauber.append(tal)

        rules = []
        ruleLineCounts = []

        reihenfolge = Wolke.DB.einstellungen["RegelanhangReihenfolge"].toTextList()
        vorteileMergeScript = Wolke.DB.einstellungen["RegelanhangVorteileMergeScript"].toText()
        manöverMergeScript = Wolke.DB.einstellungen["RegelanhangManöverMergeScript"].toText()
        vorteilTypen = Wolke.DB.einstellungen["VorteilsTypen"].toTextList()
        manöverTypen = Wolke.DB.einstellungen["ManöverTypen"].toTextList()

        vorteileGruppiert = []
        for i in range(len(vorteilTypen)):
            vorteileGruppiert.append([])
        for i in range(len(vorteilTypen)):
            scriptVariables = { "char" : Wolke.Char, "typ" : i, "mergeTo" : i }
            exec(vorteileMergeScript, scriptVariables)
            mergeTo = scriptVariables["mergeTo"]
            if mergeTo >= len(vorteilTypen):
                mergeTo = i
            empty = len(vorteileGruppiert[mergeTo]) == 0
            vorteileGruppiert[mergeTo].extend([el for el in sortV if Wolke.DB.vorteile[el].typ == i])
            if not empty:
                vorteileGruppiert[mergeTo] = sorted(vorteileGruppiert[mergeTo])

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

        for r in reihenfolge:
            if r[0] == "V":
                typ = int(r[1:])
                if typ >= len(vorteileGruppiert):
                    continue
                self.RuleCategories.append(self.formatCategory(vorteilTypen[typ]))
                self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[-1], vorteileGruppiert[typ])
                pass
            elif r[0] == "M":
                typ = int(r[1:])
                if typ >= len(manöverGruppiert):
                    continue
                self.RuleCategories.append(self.formatCategory(manöverTypen[typ]))
                self.appendManöver(rules, ruleLineCounts, self.RuleCategories[-1], manöverGruppiert[typ])
                pass
            elif r[0] == "W":
                self.RuleCategories.append(self.formatCategory("Waffeneigenschaften"))
                self.appendWaffeneigenschaften(rules, ruleLineCounts, self.RuleCategories[-1], waffeneigenschaften)
                pass
            elif r[0] == "Z":
                self.RuleCategories.append(self.formatCategory("Zauber"))
                self.appendTalente(rules, ruleLineCounts, self.RuleCategories[-1], zauber)
                pass
            elif r[0] == "L":
                self.RuleCategories.append(self.formatCategory("Liturgien"))
                self.appendTalente(rules, ruleLineCounts, self.RuleCategories[-1], liturgien)
                pass
            elif r[0] == "A":
                self.RuleCategories.append(self.formatCategory("Anrufungen"))
                self.appendTalente(rules, ruleLineCounts, self.RuleCategories[-1], anrufungen)
                pass

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