from Wolke import Wolke
import re
import math
from difflib import SequenceMatcher
from fractions import Fraction
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import Objekte

class CheatsheetGenerator(object):

    def __init__(self):
        self.RuleCategories = []
        self.RuleCategories.append(self.formatCategory('ALLGEMEINE VORTEILE'))
        self.RuleCategories.append(self.formatCategory('PROFANE VORTEILE'))
        self.RuleCategories.append(self.formatCategory('PROFANE REGELN'))
        self.RuleCategories.append(self.formatCategory('KAMPFVORTEILE'))
        self.RuleCategories.append(self.formatCategory('AKTIONEN'))
        self.RuleCategories.append(self.formatCategory('WAFFENEIGENSCHAFTEN'))
        self.RuleCategories.append(self.formatCategory('WEITERE KAMPFREGELN'))
        self.RuleCategories.append(self.formatCategory('NAHKAMPFMANÖVER'))
        self.RuleCategories.append(self.formatCategory('FERNKAMPFMANÖVER'))
        self.RuleCategories.append(self.formatCategory('MAGISCHE VORTEILE'))
        self.RuleCategories.append(self.formatCategory('SPONTANE MODIFIKATIONEN (ZAUBER)'))
        self.RuleCategories.append(self.formatCategory('WEITERE MAGIEREGELN'))
        self.RuleCategories.append(self.formatCategory('ZAUBER'))
        self.RuleCategories.append(self.formatCategory('KARMALE VORTEILE'))
        self.RuleCategories.append(self.formatCategory('SPONTANE MODIFIKATIONEN (LITURGIEN)'))
        self.RuleCategories.append(self.formatCategory('WEITERE KARMAREGELN'))
        self.RuleCategories.append(self.formatCategory('LITURGIEN'))
        self.RuleCategories.append(self.formatCategory('DÄMONISCHE VORTEILE'))
        self.RuleCategories.append(self.formatCategory('SPONTANE MODIFIKATIONEN (ANRUFUNGEN)'))
        self.RuleCategories.append(self.formatCategory('WEITERE ANRUFUNGSREGELN'))
        self.RuleCategories.append(self.formatCategory('ANRUFUNGEN'))

        self.RulesLineCount = 100
        self.RulesCharCount = 80
        fontSize = Wolke.Settings["Cheatsheet-Fontsize"]
        if fontSize == 1:
            self.RulesLineCount = 80
            self.RulesCharCount = 55
        elif fontSize == 2:
            self.RulesLineCount = 60
            self.RulesCharCount = 45

    def formatCategory(self, category):
        return "===== " + category + " ====="

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

    textToFraction = {
        'ein Achtel' : "1/8",
        'ein Viertel' : "1/4",
        "die Hälfte" : "1/2",
        'drei Viertel' : "3/4",
    }

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
        if vorteil.linkKategorie == 1:
            return True
        elif vorteil.linkKategorie == 2:
            for fer in Wolke.Char.übernatürlicheFertigkeiten:
                if vorteil.linkElement in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                    return True
        elif vorteil.linkKategorie == 3:
            if vorteil.linkElement in Wolke.Char.vorteile:
                return True
            return self.isCheatsheetLinkedToAny(Wolke.DB.vorteile[vorteil.linkElement])

        return False
    
    def isCheatsheetLinkedTo(self, vorteil, kategorie, element):
        if kategorie == 1 and vorteil.linkKategorie == 1:
            return vorteil.linkElement == element
        elif kategorie == 2 and vorteil.linkKategorie == 2:
            if vorteil.linkElement == element:
                for fer in Wolke.Char.übernatürlicheFertigkeiten:
                    if vorteil.linkElement in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                        return True
        elif vorteil.linkKategorie == 3:
            if kategorie == 3 and vorteil.linkElement == element and (vorteil.linkElement in Wolke.Char.vorteile):
                return True
            if vorteil.linkElement in Wolke.Char.vorteile:
                return False
            return Wolke.DB.vorteile[vorteil.linkElement].isCheatsheetLinkedTo(vorteil, kategorie, element)            

        return False

    def getLinkedName(self, vorteil, forceKommentar = False):
        name = vorteil.getFullName(Wolke.Char, forceKommentar)

        for vor2 in Wolke.Char.vorteile:
            vorteil2 = Wolke.DB.vorteile[vor2]
            if self.isCheatsheetLinkedTo(vorteil2, 3, vorteil.name):
                name2 = self.getLinkedName(vorteil2, forceKommentar)

                #allgemeine vorteile, kampfstile and traditionen only keep the last name (except vorteil is variable with a comment)
                if (not (vorteil.name in Wolke.Char.vorteileVariable) or not Wolke.Char.vorteileVariable[vorteil.name].kommentar)\
                   and (vorteil2.typ == 0 or vorteil2.typ == 3 or vorteil2.typ == 5 or vorteil2.typ == 7 or vorteil2.typ == 8):
                    name = name2
                else:
                    fullset = [" I", " II", " III", " IV", " V", " VI", " VII"]
                    basename = ""
                    for el in fullset:
                        if name.endswith(el):
                            basename = name[:-len(el)]
                            break
                    if basename and name2.startswith(basename):
                        name += "," + name2[len(basename):]
                    else:
                        name += ", " + name2

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
            if self.isCheatsheetLinkedTo(vorteil2, 3, vorteil.name):
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
                if self.isCheatsheetLinkedTo(vorteil, 1, man):
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

    def appendTalente(self, strList, lineCounts, category, talente, talentboxList):
        if not talente or (len(talente) == 0):
            return
        strList.append(category + "\n\n")
        lineCounts.append(self.getLineCount(strList[-1]))
        count = 0
        for tal in talente:
            result = []
            talent = Wolke.DB.talente[tal]
            if not talent.cheatsheetAuflisten or not talent.text:
                continue
            count += 1
            name = talent.getFullName(Wolke.Char)
            result.append(name)
            for i in range(len(talentboxList)):
                if talentboxList[i].na == name:
                    result.append(" (PW " + str(talentboxList[i].pw) + ")")
                    break
            result.append("\n")
            text = talent.text
            
            #Remove everything from Fertigkeiten on
            index = text.find('\nFertigkeiten')
            if index != -1:
                text = text[:index]

            #Remove everything from Erlernen on (some talents don't have a Fertigkeiten list)
            index = text.find('\nErlernen')
            if index != -1:
                text = text[:index]

            result.append(text)

            for vor in Wolke.Char.vorteile:
                vorteil = Wolke.DB.vorteile[vor]
                if self.isCheatsheetLinkedTo(vorteil, 2, talent.name):
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

    def prepareRules(self, talentboxList):
        sortV = Wolke.Char.vorteile.copy()
        sortV = sorted(sortV, key=str.lower)

        allgemein = [el for el in sortV if Wolke.DB.vorteile[el].typ == 0]
        
        profan = [el for el in sortV if Wolke.DB.vorteile[el].typ == 1]

        kampf = [el for el in sortV if (Wolke.DB.vorteile[el].typ == 2)]
        kampfstile = [el for el in sortV if (Wolke.DB.vorteile[el].typ == 3)]
        kampf.extend(kampfstile)

        magisch = [el for el in sortV if Wolke.DB.vorteile[el].typ == 4]
        magischTraditionen = [el for el in sortV if Wolke.DB.vorteile[el].typ == 5]
        magisch.extend(magischTraditionen)

        karmal = [el for el in sortV if Wolke.DB.vorteile[el].typ == 6]
        karmalTraditionen = [el for el in sortV if Wolke.DB.vorteile[el].typ == 7]
        karmal.extend(karmalTraditionen)

        dämonisch = [el for el in sortV if Wolke.DB.vorteile[el].typ == 8]

        sortM = list(Wolke.DB.manöver.keys())
        sortM = sorted(sortM, key=str.lower)

        aktionen = [el for el in sortM if (Wolke.DB.manöver[el].typ == 5)]

        manövernah = [el for el in sortM if (Wolke.DB.manöver[el].typ == 0)]

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

        manöverfern = []
        for waffe in Wolke.Char.waffen:
            if type(waffe) is Objekte.Fernkampfwaffe:
                manöverfern = [el for el in sortM if (Wolke.DB.manöver[el].typ == 1)]
                break
        
        weiteresprofan = [el for el in sortM if (Wolke.DB.manöver[el].typ == 9)]
        weitereskampf = [el for el in sortM if (Wolke.DB.manöver[el].typ == 8)]
            
        spomodsmagie = [el for el in sortM if (Wolke.DB.manöver[el].typ == 2)]
        weiteresmagie = [el for el in sortM if (Wolke.DB.manöver[el].typ == 4)]
        
        spomodskarma = [el for el in sortM if (Wolke.DB.manöver[el].typ == 3)]
        weitereskarma = [el for el in sortM if (Wolke.DB.manöver[el].typ == 7)]

        spomodsdämonisch = [el for el in sortM if (Wolke.DB.manöver[el].typ == 6)]
        weiteresdämonisch = []
        
        
        isZauberer = ("Zauberer I" in Wolke.Char.vorteile) or ("Tradition der Borbaradianer I" in Wolke.Char.vorteile)
        isGeweiht = "Geweiht I" in Wolke.Char.vorteile
        isPaktierer = "Paktierer I" in Wolke.Char.vorteile

        if len(weiteresmagie) > 0 and not isZauberer:
            # There a quite a few of shared rules, move them to the appropriate list if char isnt a magic user
            if isGeweiht:
                weitereskarma.extend(weiteresmagie)
                weitereskarma = sorted(weitereskarma)
                weiteresmagie.clear()
            elif isPaktierer:
                weiteresdämonisch = weiteresmagie
                weiteresmagie.clear()

        zauber = set()
        liturgien = set()
        anrufungen = set()
        for fer in Wolke.Char.übernatürlicheFertigkeiten:
            for tal in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                res = re.findall('Kosten:(.*?)\n', Wolke.DB.talente[tal].text, re.UNICODE)
                if len(res) >= 1 and " KaP" in res[0]:
                    liturgien.add(tal)
                elif len(res) >= 1 and " GuP" in res[0]:
                    anrufungen.add(tal)
                else:
                    if isZauberer:
                        zauber.add(tal)
                    elif isGeweiht:
                        liturgien.add(tal)
                    elif isPaktierer:
                        anrufungen.add(tal)
                    else:
                        zauber.add(tal)

        zauber = sorted(zauber, key=str.lower)
        liturgien = sorted(liturgien, key=str.lower)
        anrufungen = sorted(anrufungen, key=str.lower)

        rules = []
        ruleLineCounts = []

        self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[0], allgemein)
        self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[1], profan)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[2], weiteresprofan)

        self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[3], kampf)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[4], aktionen)
        self.appendWaffeneigenschaften(rules, ruleLineCounts, self.RuleCategories[5], waffeneigenschaften)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[6], weitereskampf)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[7], manövernah)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[8], manöverfern)

        self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[9], magisch)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[10], spomodsmagie)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[11], weiteresmagie)
        self.appendTalente(rules, ruleLineCounts, self.RuleCategories[12], zauber, talentboxList)

        self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[13], karmal)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[14], spomodskarma)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[15], weitereskarma)
        self.appendTalente(rules, ruleLineCounts, self.RuleCategories[16], liturgien, talentboxList)

        self.appendVorteile(rules, ruleLineCounts, self.RuleCategories[17], dämonisch)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[18], spomodsdämonisch)
        self.appendManöver(rules, ruleLineCounts, self.RuleCategories[19], weiteresdämonisch)
        self.appendTalente(rules, ruleLineCounts, self.RuleCategories[20], anrufungen, talentboxList)

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