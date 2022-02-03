from Wolke import Wolke
from Fertigkeiten import VorteilLinkKategorie
import Talentbox
import re
from difflib import SequenceMatcher
from fractions import Fraction

class CharakterPrintUtility:

    @staticmethod
    def getVorteile(char):
        return sorted(char.vorteile, key = lambda v: (Wolke.DB.vorteile[v].typ, Wolke.DB.vorteile[v].name))

    @staticmethod
    def groupVorteile(char, vorteile, link = True):
        # Collect a list of Vorteile, where different levels of the same are
        # combined into one entry and then split them into the three categories
        if link:
            vorteile = [v for v in vorteile if not CharakterPrintUtility.isLinkedToVorteil(char, Wolke.DB.vorteile[v])]

        vorteileAllgemein = []
        vorteileKampf = []
        vorteileUeber = []

        vorteileMergeScript = Wolke.DB.einstellungen["Charsheet: Vorteile Mergescript"].toText()
        for vort in vorteile:
            vorteil = Wolke.DB.vorteile[vort]
            if link:
                name = CharakterPrintUtility.getLinkedName(char, vorteil, forceKommentar=True)
            else:
                name = vorteil.getFullName(char)
            scriptVariables = { "char" : char, "name" : vort, "typ" : vorteil.typ, "mergeTo" : 0 }
            exec(vorteileMergeScript, scriptVariables)
            if scriptVariables["mergeTo"] == 0:
                vorteileAllgemein.append(name)
            elif scriptVariables["mergeTo"] == 1:
                vorteileKampf.append(name)
            else:
                vorteileUeber.append(name)

        # sort again, otherwise they are sorted by vorteil type which is confusing if they go into the same table
        vorteileAllgemein.sort(key = str.lower)
        vorteileKampf.sort(key = str.lower)
        vorteileUeber.sort(key = str.lower)

        return (vorteileAllgemein, vorteileKampf, vorteileUeber)

    @staticmethod
    def getFreieFertigkeiten(char):
        ferts = []
        for el in char.freieFertigkeiten:
            if el.wert < 1 or el.wert > 3 or not el.name:
                continue
            name = el.name + " "
            for i in range(el.wert):
                name += "I"
            ferts.append(name)
        return ferts

    @staticmethod
    def getFertigkeiten(char):
        return sorted(char.fertigkeiten, key = lambda x: (Wolke.DB.fertigkeiten[x].printclass, x))

    @staticmethod
    def getTalente(char, fertigkeit):
        talentBoxes = []
        talente = fertigkeit.gekaufteTalente.copy()
        talente.extend([t for t in fertigkeit.talentMods if not t in talente])
        talente = sorted(talente)

        for el in talente:
            talent = Wolke.DB.talente[el]
            tt = Talentbox.Talentbox()
            tt.na = el
            tt.pw = fertigkeit.probenwertTalent
            tt.groupFert = fertigkeit
            tt.text = talent.text

            tt.anzeigeName = talent.getFullName(char) if el in fertigkeit.gekaufteTalente else el
            tt.anzeigeName = tt.anzeigeName.replace(fertigkeit.name + ": ", "")
            if el in fertigkeit.talentMods:
                for condition,mod in sorted(fertigkeit.talentMods[el].items()):
                    tt.anzeigeName += " " + (condition + " " if condition else "") + ("+" if mod >= 0 else "") + str(mod)        
            if not el in fertigkeit.gekaufteTalente:
                tt.anzeigeName = "(" + tt.anzeigeName + ")"

            talentBoxes.append(tt)

        return talentBoxes

    @staticmethod
    def getÜberFertigkeiten(char):
        ferts = [f for f in char.übernatürlicheFertigkeiten if char.übernatürlicheFertigkeiten[f].addToPDF]
        ferts = sorted(ferts, key = lambda f: (Wolke.DB.übernatürlicheFertigkeiten[f].printclass, f))
        return ferts

    @staticmethod
    def getÜberTalente(char):
        talente = set()
        for fert in char.übernatürlicheFertigkeiten:
            for talent in char.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                talente.add(talent)
        talentBoxes = []
        referenzBücher = Wolke.DB.einstellungen["Referenzbücher"].toTextList()
        for t in talente:
            # Fill Talente
            talent = Wolke.DB.talente[t]
            tt = Talentbox.Talentbox()

            tt.na = talent.name
            tt.anzeigeName = talent.getFullName(char)
            tt.cheatsheetAuflisten = talent.cheatsheetAuflisten
            tt.text = talent.text

            if len(talent.fertigkeiten) == 1:
                tt.na = tt.na.replace(talent.fertigkeiten[0] + ": ", "")
            for el in talent.fertigkeiten:
                if not el in char.übernatürlicheFertigkeiten:
                    continue
                fert = char.übernatürlicheFertigkeiten[el]
                tt.pw = max(tt.pw, fert.probenwertTalent)

                if tt.groupFert is None:
                    tt.groupFert = fert
                elif not tt.groupFert.talenteGruppieren and fert.talenteGruppieren:
                    tt.groupFert = fert
                elif tt.groupFert.talenteGruppieren and fert.talenteGruppieren:
                    if tt.groupFert.probenwertTalent < fert.probenwertTalent:
                        tt.groupFert = fert

            res = re.findall('Vorbereitungszeit:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.vo = res[0].strip()
            res = re.findall('Reichweite:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.re = res[0].strip()
            res = re.findall('Wirkungsdauer:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.wd = res[0].strip()
            res = re.findall('Kosten:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.ko = res[0].strip()

            if talent.referenzSeite > 0:
                if talent.referenzBuch >= len(referenzBücher) or referenzBücher[talent.referenzBuch] == "Ilaris":
                    tt.se = "S. " + str(talent.referenzSeite)
                else:
                    tt.se = referenzBücher[talent.referenzBuch] + " S. " + str(talent.referenzSeite)

            talentBoxes.append(tt)

        def sortTalents(tt):
            if tt.groupFert is None:
                return (0, "", tt.na)
            elif tt.groupFert.talenteGruppieren:
               return (tt.groupFert.printclass, tt.groupFert.name, tt.na)
            else:
               return (tt.groupFert.printclass, "", tt.na)

        talentBoxes.sort(key = lambda tt: sortTalents(tt))
        return talentBoxes

    @staticmethod
    def groupUeberTalente(talentboxList):
        liturgieTypen = [int(t) for t in Wolke.DB.einstellungen["Fertigkeiten: Liturgie-Typen"].toTextList()]
        anrufungTypen = [int(t) for t in Wolke.DB.einstellungen["Fertigkeiten: Anrufungs-Typen"].toTextList()]
        zauber = []
        liturgien = []
        anrufungen = []
        for tal in talentboxList:
            if tal.groupFert is not None and tal.groupFert.printclass in liturgieTypen:
                liturgien.append(tal)
            elif tal.groupFert is not None and tal.groupFert.printclass in anrufungTypen:
                anrufungen.append(tal)
            else:
                zauber.append(tal)
        return (zauber, liturgien, anrufungen)

    textToFraction = {
        "ein Achtel" : "1/8",
        "ein Viertel" : "1/4",
        "die Hälfte" : "1/2",
        "drei Viertel" : "3/4",
    }

    @staticmethod
    def __prepareDescription(description):
        #convert text to fractions
        for k,v in CharakterPrintUtility.textToFraction.items():
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

    @staticmethod
    def __finalizeDescription(strList):
        result = ""
        for text in strList:
            if text == "\n":
                result = result.strip() + "\n"
            else:
                result += text

        #convert fractions back to text
        for k,v in CharakterPrintUtility.textToFraction.items():
            result = result.replace(v, k)

        return result.strip()

    @staticmethod
    def __mergeDescriptions(str1, str2):
        #match numbers or fractions, + is ignored, nums with prefix S. are skipped
        reNumbers = re.compile(r'-?\d+/\d+|-?\d+', re.UNICODE)

        lines1 = CharakterPrintUtility.__prepareDescription(str1)
        lines2 = CharakterPrintUtility.__prepareDescription(str2)

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
        return CharakterPrintUtility.__finalizeDescription(lines1)

    @staticmethod
    def isLinkedToVorteil(char, vorteil):
        if vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if vorteil.linkElement in char.vorteile:
                return True
            return CharakterPrintUtility.isLinkedToVorteil(char, Wolke.DB.vorteile[vorteil.linkElement])          

        return False

    @staticmethod
    def isLinkedTo(char, vorteil, kategorie, element):
        if kategorie == VorteilLinkKategorie.ManöverMod and vorteil.linkKategorie == VorteilLinkKategorie.ManöverMod:
            return vorteil.linkElement == element
        elif kategorie == VorteilLinkKategorie.ÜberTalent and vorteil.linkKategorie == VorteilLinkKategorie.ÜberTalent:
            if vorteil.linkElement == element:
                for fer in char.übernatürlicheFertigkeiten:
                    if vorteil.linkElement in char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                        return True
        elif vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if kategorie == VorteilLinkKategorie.Vorteil and vorteil.linkElement == element and (vorteil.linkElement in char.vorteile):
                return True
            if vorteil.linkElement in char.vorteile:
                return False
            return CharakterPrintUtility.isLinkedTo(char, Wolke.DB.vorteile[vorteil.linkElement], kategorie, element)            

        return False

    @staticmethod
    def getLinkedName(char, vorteil, forceKommentar = False):
        name = vorteil.getFullName(char, forceKommentar)
        vorteilsnamenErsetzen = [int(typ) for typ in Wolke.DB.einstellungen["Regelanhang: Vorteilsnamen ersetzen"].toTextList()]

        for vor2 in char.vorteile:
            vorteil2 = Wolke.DB.vorteile[vor2]
            if CharakterPrintUtility.isLinkedTo(char, vorteil2, VorteilLinkKategorie.Vorteil, vorteil.name):
                name2 = CharakterPrintUtility.getLinkedName(char, vorteil2, forceKommentar)

                #allgemeine vorteile, kampfstile and traditionen only keep the last name (except vorteil is variable with a comment)
                if (not (vorteil.name in char.vorteileVariable) or not char.vorteileVariable[vorteil.name].kommentar)\
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
            abbreviations = Wolke.DB.einstellungen["Charsheet: Verknüpfungs-Abkürzungen"].toTextDict('\n', False)
            nameStart = name[:name.index(",")]
            nameAbbreviate = name[name.index(","):]
            for k,v in abbreviations.items():
                nameAbbreviate = nameAbbreviate.replace(k, v)
            name = nameStart + nameAbbreviate
        return name

    @staticmethod
    def getLinkedDescription(char, vorteil):
        beschreibung = vorteil.cheatsheetBeschreibung.replace("\n\n", "\n")
        if beschreibung:
            if vorteil.name in char.vorteileVariable:
                if "$kommentar$" in beschreibung:
                    beschreibung = beschreibung.replace("$kommentar$", char.vorteileVariable[vorteil.name].kommentar)
        else:
            beschreibung = vorteil.text.replace("\n\n", "\n")

        for vor2 in char.vorteile:
            vorteil2 = Wolke.DB.vorteile[vor2]
            if CharakterPrintUtility.isLinkedTo(char, vorteil2, VorteilLinkKategorie.Vorteil, vorteil.name):
                beschreibung2 = CharakterPrintUtility.getLinkedDescription(char, vorteil2)

                if vorteil2.typ == 0:
                    #allgemeine vorteile replace the description of what they link to (except vorteil is variable with a comment)
                    if not (vorteil.name in char.vorteileVariable) or not char.vorteileVariable[vorteil.name].kommentar:
                        beschreibung = beschreibung2
                    else:
                        beschreibung += "\n" + beschreibung2
                else:
                    beschreibung = CharakterPrintUtility.__mergeDescriptions(beschreibung, beschreibung2)

        return beschreibung