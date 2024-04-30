from Wolke import Wolke
from Core.Vorteil import VorteilLinkKategorie
from Core.Talent import Talent
import re
from difflib import SequenceMatcher
from fractions import Fraction
from Hilfsmethoden import Hilfsmethoden, SortedCategoryToListDict

class CharakterPrintUtility:

    @staticmethod
    def getVorteile(char):
        return sorted(char.vorteile.values(), key = lambda v: (v.kategorie, Hilfsmethoden.unicodeCaseInsensitive(v.name)))

    @staticmethod
    def groupVorteile(char, vorteile, link = True):
        # Collect a list of Vorteile, where different levels of the same are
        # combined into one entry and then split them into the three categories
        if link:
            vorteile = [v for v in vorteile if not CharakterPrintUtility.isLinkedToVorteil(char, v)]

        vorteileAllgemein = []
        vorteileKampf = []
        vorteileUeber = []

        scriptAPI = Hilfsmethoden.createScriptAPI()
        for vorteil in vorteile:
            if link:
                name = CharakterPrintUtility.getLinkedName(char, vorteil)
            else:
                name = vorteil.anzeigenameExt
            
            scriptAPI.update({ "name" : vorteil.name, "kategorie" : vorteil.kategorie, "mergeTo" : 0 })
            Wolke.DB.einstellungen["Charsheet: Vorteile Mergescript"].executeScript(scriptAPI)
            if scriptAPI["mergeTo"] == 0:
                vorteileAllgemein.append(name)
            elif scriptAPI["mergeTo"] == 1:
                vorteileKampf.append(name)
            else:
                vorteileUeber.append(name)

        # sort again, otherwise they are sorted by vorteil category which is confusing if they go into the same table
        vorteileAllgemein.sort(key=Hilfsmethoden.unicodeCaseInsensitive)
        vorteileKampf.sort(key=Hilfsmethoden.unicodeCaseInsensitive)
        vorteileUeber.sort(key=Hilfsmethoden.unicodeCaseInsensitive)

        return (vorteileAllgemein, vorteileKampf, vorteileUeber)

    @staticmethod
    def getFreieFertigkeiten(char):
        return CharakterPrintUtility.getFreieFertigkeitenNames(char.freieFertigkeiten)

    @staticmethod
    def getFreieFertigkeitenNames(freieFertigkeiten):
        ferts = []
        for el in freieFertigkeiten:
            if el.wert < 1 or el.wert > 3:
                continue
            name = el.name
            if name:
                name = el.name + " "
                for i in range(el.wert):
                    name += "I"
            ferts.append(name)
        return ferts

    @staticmethod
    def getFertigkeiten(char):
        fertigkeitenByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Fertigkeiten: Kategorien profan"].wert)
        for fert in char.fertigkeiten.values():
            fertigkeitenByKategorie.append(fert.kategorie, fert.name)
        fertigkeitenByKategorie.sortValues()
        return fertigkeitenByKategorie

    @staticmethod
    def getTalente(char, fertigkeit, nurHöchsteFertigkeit = False):
        result = []
        talente = [Wolke.DB.talente[t] for t in fertigkeit.gekaufteTalente]

        # Profane Talente mit mods hinzufügen, falls nicht gekauft
        for t in char.talentMods:
            talent = Wolke.DB.talente[t]
            if talent.spezialTalent:
                continue
            if fertigkeit.name not in talent.fertigkeiten:
               continue
            if talent.name in fertigkeit.gekaufteTalente:
               continue
            talente.append(talent)

        talente = sorted(talente, key = lambda t : Hilfsmethoden.unicodeCaseInsensitive(t.anzeigename))

        for el in talente:
            if nurHöchsteFertigkeit:
                höchste = None
                ferts = char.übernatürlicheFertigkeiten if el.spezialTalent else char.fertigkeiten
                for fertName in el.fertigkeiten:   
                    if fertName not in ferts:
                        continue
                    fert = ferts[fertName]
                    if höchste == None or (fert.addToPDF and höchste.probenwertTalent < fert.probenwertTalent):
                        höchste = fert
                if höchste.name != fertigkeit.name:
                    continue

            name = char.talente[el.name].anzeigenameExt if el.name in char.talente else el.anzeigename
            if el.name in char.talentMods:
                modPrefix = ""
                mod = char.talentMods[el.name]
                if mod >= 0:
                    modPrefix = "+"
                name += " " + modPrefix + str(mod)
            if el.name in char.talentInfos:
                name += "; " + "; ".join(char.talentInfos[el.name])
            if el.name not in fertigkeit.gekaufteTalente:
                name = "(" + name + ")"
            result.append(name)

        return result

    @staticmethod
    def getÜberFertigkeiten(char):
        fertigkeitenByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Fertigkeiten: Kategorien übernatürlich"].wert)
        for fert in char.übernatürlicheFertigkeiten.values():
            if fert.addToPDF:
                fertigkeitenByKategorie.append(fert.kategorie, fert.name)
        fertigkeitenByKategorie.sortValues()
        return fertigkeitenByKategorie

    @staticmethod
    def getÜberTalente(char):
        talenteByKategorie = SortedCategoryToListDict(Wolke.DB.einstellungen["Talente: Kategorien"].wert)
        for t in char.talente.values():
            if not t.spezialTalent:
                continue
            talenteByKategorie.append(t.kategorie, t.name)
        talenteByKategorie.sortValues(lambda t: Talent.sorter(char.talente[t]))
        return talenteByKategorie

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
    def mergeDescriptions(str1, str2):
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
        if kategorie == VorteilLinkKategorie.Regel and vorteil.linkKategorie == VorteilLinkKategorie.Regel:
            return vorteil.linkElement == element
        elif kategorie == VorteilLinkKategorie.ÜberTalent and vorteil.linkKategorie == VorteilLinkKategorie.ÜberTalent:
            if vorteil.linkElement == element and vorteil.linkElement in char.talente:
                return True
        elif vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if kategorie == VorteilLinkKategorie.Vorteil and vorteil.linkElement == element and (vorteil.linkElement in char.vorteile):
                return True
            if vorteil.linkElement in char.vorteile:
                return False
            return CharakterPrintUtility.isLinkedTo(char, Wolke.DB.vorteile[vorteil.linkElement], kategorie, element)            

        return False

    @staticmethod
    def getLinkedName(char, vorteil, descriptionWillFollow = False):
        name = vorteil.anzeigenameExt
        if descriptionWillFollow and "$kommentar$" in vorteil.cheatsheetBeschreibung:
            name = vorteil.name
        vorteilsnamenErsetzen = Wolke.DB.einstellungen["Regelanhang: Vorteilsnamen ersetzen"].wert

        for vorteil2 in char.vorteile.values():
            if CharakterPrintUtility.isLinkedTo(char, vorteil2, VorteilLinkKategorie.Vorteil, vorteil.name):
                name2 = CharakterPrintUtility.getLinkedName(char, vorteil2, descriptionWillFollow)

                #allgemeine vorteile, kampfstile and traditionen only keep the last name (except vorteil is variable with a comment)
                if (not vorteil.variableKosten) and vorteil2.kategorie in vorteilsnamenErsetzen:
                    name = name2
                    if vorteil.kommentarErlauben and vorteil.kommentar:
                        if name.endswith(")"):
                            name = name[:-1]
                            name += f"; {vorteil.kommentar})" # todo: kommentar order is wrong
                        else:
                            name += f" ({vorteil.kommentar})"
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
            abbreviations = Wolke.DB.einstellungen["Charsheet: Verknüpfungs-Abkürzungen"].wert
            nameStart = name[:name.index(",")]
            nameAbbreviate = name[name.index(","):]
            for k,v in abbreviations.items():
                nameAbbreviate = nameAbbreviate.replace(k, v)
            name = nameStart + nameAbbreviate
        return name

    @staticmethod
    def getLinkedBedingungen(char, vorteil):
        bedingungen = vorteil.bedingungen
        beschreibungenErsetzen = Wolke.DB.einstellungen["Regelanhang: Vorteilsbeschreibungen ersetzen"].wert
        for vorteil2 in char.vorteile.values():
            if CharakterPrintUtility.isLinkedTo(char, vorteil2, VorteilLinkKategorie.Vorteil, vorteil.name):
                if vorteil2.kategorie in beschreibungenErsetzen:
                    continue
                bedingungen2 = CharakterPrintUtility.getLinkedBedingungen(char, vorteil2)
                if bedingungen2:
                    bedingungen += "\n" + bedingungen2

        return bedingungen.strip()

    @staticmethod
    def getLinkedDescription(char, vorteil):
        beschreibung = vorteil.cheatsheetBeschreibung.replace("\n\n", "\n")
        if beschreibung:
            if vorteil.kommentarErlauben and "$kommentar$" in beschreibung:
                beschreibung = beschreibung.replace("$kommentar$", vorteil.kommentar)
        else:
            beschreibung = vorteil.text.replace("\n\n", "\n")

        beschreibungenErsetzen = Wolke.DB.einstellungen["Regelanhang: Vorteilsbeschreibungen ersetzen"].wert
        for vorteil2 in char.vorteile.values():
            if CharakterPrintUtility.isLinkedTo(char, vorteil2, VorteilLinkKategorie.Vorteil, vorteil.name):
                beschreibung2 = CharakterPrintUtility.getLinkedDescription(char, vorteil2)

                if vorteil2.kategorie in beschreibungenErsetzen:
                    #allgemeine vorteile replace the description of what they link to (except vorteil is variable with a comment)
                    if not vorteil.variableKosten or not (vorteil.kommentarErlauben and vorteil.kommentar):
                        beschreibung = beschreibung2
                    else:
                        beschreibung += "\n" + beschreibung2
                else:
                    beschreibung = CharakterPrintUtility.mergeDescriptions(beschreibung, beschreibung2)

        return beschreibung