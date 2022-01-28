from Wolke import Wolke
from Fertigkeiten import VorteilLinkKategorie
import Talentbox
import re

class CharakterPrintUtility:
    @staticmethod
    def isLinkedToVorteil(vorteil):
        if vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if vorteil.linkElement in Wolke.Char.vorteile:
                return True
            return CharakterPrintUtility.isLinkedToVorteil(Wolke.DB.vorteile[vorteil.linkElement])          

        return False

    @staticmethod
    def getVorteile(char):
        vorteile = [v for v in char.vorteile if not CharakterPrintUtility.isLinkedToVorteil(Wolke.DB.vorteile[v])]
        vorteile = sorted(vorteile, key = lambda v: (Wolke.DB.vorteile[v].typ, v))
        return vorteile

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
        talStr = ""
        talente = sorted(fertigkeit.gekaufteTalente)
        for el in talente:
            talStr += ", "
            talent = Wolke.DB.talente[el]
            talStr += talent.getFullName(char).replace(fertigkeit.name + ": ", "")

            if el in fertigkeit.talentMods:
                for condition,mod in sorted(fertigkeit.talentMods[el].items()):
                    talStr += " " + (condition + " " if condition else "") + ("+" if mod >= 0 else "") + str(mod)

        #Append any talent mods of talents the character doesn't own in parentheses
        for talentName, talentMods in sorted(fertigkeit.talentMods.items()):
            if not talentName in talente:
                talStr += ", (" + talentName
                for condition,mod in sorted(talentMods.items()):
                    talStr += " " + (condition + " " if condition else "") + ("+" if mod >= 0 else "") + str(mod)
                talStr += ")"

        talStr = talStr[2:]
        return talStr

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