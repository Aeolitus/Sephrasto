from Wolke import Wolke
from EventBus import EventBus
from Fertigkeiten import KampffertigkeitTyp

class Choice(object):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.wert = 0
        self.typ = "Fertigkeit"
        self.kommentar = ""

    def toString(self, addEP = True):
        valueStr = ""
        prefix = ""
        if self.typ == "Freie-Fertigkeit":
            fert = None
            for ff in Wolke.Char.freieFertigkeiten:
                if self.name == ff.name:
                    fert = ff
                    break
            if fert:
                werte = ["I", "II", "III"]
                valueStr += " (aktuell " + werte[ff.wert] + ")"
                wert = min(self.wert, 3 - ff.wert)
                if wert == 1:
                    valueStr = " +I"
                elif wert == 2:
                    valueStr = " +II"
            else:
                if self.wert == 1:
                    valueStr = " I"
                elif self.wert == 2:
                    valueStr = " II"
                elif self.wert == 3:
                    valueStr = " III"

        elif self.typ == "Fertigkeit":
            if self.wert >= 0:
                valueStr = " +" + str(self.wert)
            else:
                valueStr = " " + str(self.wert)

            if self.name in Wolke.Char.fertigkeiten:
                current = Wolke.Char.fertigkeiten[self.name].wert
                valueStr += " (aktuell FW " + str(current) + ")"
        elif self.typ == "Übernatürliche-Fertigkeit":
            if self.wert >= 0:
                valueStr = " +" + str(self.wert)
            else:
                valueStr = " " + str(self.wert)

            if self.name in Wolke.Char.übernatürlicheFertigkeiten:
                current = Wolke.Char.übernatürlicheFertigkeiten[self.name].wert
                valueStr += " (aktuell FW " + str(current) + ")"
        elif self.typ == "Attribut":
            if self.wert >= 0:
                valueStr = " +" + str(self.wert)
            else:
                valueStr = " " + str(self.wert)

            if self.name in Wolke.Char.attribute:
                current = Wolke.Char.attribute[self.name].wert
                valueStr += " (aktuell " + str(current) + ")"
        else:
            prefix = self.typ + " "

        if (self.typ == "Vorteil" or self.typ == "Talent") and self.wert == -1:
            valueStr += " entfernt"

        if self.kommentar:
            valueStr += " (" + self.kommentar + ")"

        if addEP and self.typ != "Eigenheit":
            if self.kommentar:
                valueStr = valueStr[:-1] + "; "
            else:
                valueStr += " ("
            valueStr += str(self.countEP()) + " EP)"

        return prefix + self.name + valueStr

    def __countEPNahkampf(self, includeChoice = False):
        ep = 0
        höchste = None
        höchsteWert = 0
        for fert in Wolke.Char.fertigkeiten.values():
            if fert.kampffertigkeit != KampffertigkeitTyp.Nahkampf:
                continue
            wert = fert.wert
            if includeChoice and fert.name == self.name:
                wert = min(fert.maxWert, fert.wert+self.wert)

            if höchste is None or wert > höchsteWert:
                höchste = fert
                höchsteWert = wert
            ep += sum(range(wert+1)) * fert.steigerungsfaktor
        ep += max(0, 2*sum(range(höchsteWert+1)))
        return ep

    def countEP(self):
        if self.typ == "Freie-Fertigkeit":
            if self.name in Wolke.Char.freieFertigkeiten:
                fert = Wolke.Char.freieFertigkeiten[self.name]
                level = min(self.wert, 3 - fert.wert)
                oldCost = EventBus.applyFilter("freiefertigkeit_kosten", Wolke.Char.freieFertigkeitKosten[fert.wert-1], { "Wolke.Charakter" : Wolke.Char, "name" : fert.name, "wert" : fert.wert })
                newCost = EventBus.applyFilter("freiefertigkeit_kosten", Wolke.Char.freieFertigkeitKosten[fert.wert+level-1], { "Wolke.Charakter" : Wolke.Char, "name" : fert.name, "wert" : fert.wert + level })
                return newCost - oldCost
            return EventBus.applyFilter("freiefertigkeit_kosten", Wolke.Char.freieFertigkeitKosten[self.wert-1], { "Wolke.Charakter" : Wolke.Char, "name" : self.name, "wert" : self.wert })

        elif self.typ == "Fertigkeit":
            if not self.name in Wolke.Char.fertigkeiten:
                return 0
            fert = Wolke.Char.fertigkeiten[self.name]
            if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf:
                return self.__countEPNahkampf(True) - self.__countEPNahkampf()
            oldVal = sum(range(fert.wert+1)) * fert.steigerungsfaktor
            wert = min(fert.maxWert, fert.wert+self.wert)
            newVal = sum(range(wert+1)) * fert.steigerungsfaktor
            return newVal - oldVal

        elif self.typ == "Übernatürliche-Fertigkeit":
            if not self.name in Wolke.Char.übernatürlicheFertigkeiten:
                return 0
            fert = Wolke.Char.übernatürlicheFertigkeiten[self.name]
            oldVal = sum(range(fert.wert+1)) * fert.steigerungsfaktor
            wert = min(fert.maxWert, fert.wert+self.wert)
            newVal = sum(range(wert+1)) * fert.steigerungsfaktor
            return newVal - oldVal

        elif self.typ == "Attribut":
            if not self.name in Wolke.Char.attribute:
                return 0
            attribut = Wolke.Char.attribute[self.name]
            oldCost = sum(range(attribut.wert+1)) * attribut.steigerungsfaktor
            oldCost = EventBus.applyFilter("attribut_kosten", oldCost, { "Wolke.Charakter" : Wolke.Char, "attribut" : self.name, "wert" : attribut.wert })
            newCost = sum(range(attribut.wert+self.wert+1)) * attribut.steigerungsfaktor
            newCost = EventBus.applyFilter("attribut_kosten", newCost, { "Wolke.Charakter" : Wolke.Char, "attribut" : self.name, "wert" : attribut.wert+self.wert })
            return newCost - oldCost

        elif self.typ == "Talent":
            if not self.name in Wolke.DB.talente:
                return 0
            talent = Wolke.DB.talente[self.name]
            if len(talent.fertigkeiten) == 0:
                return 0
            if talent.variableKosten:
                return self.wert

            if not talent.isSpezialTalent():
                for fert in Wolke.Char.fertigkeiten.values():
                    if self.name in fert.gekaufteTalente:
                        if self.wert == -1:
                            return -Wolke.Char.getDefaultTalentCost(self.name, fert.steigerungsfaktor)
                        else:
                            return 0
            else:
                if talent.variableKosten:
                    return self.wert
                for fert in Wolke.Char.übernatürlicheFertigkeiten.values():
                    if self.name in fert.gekaufteTalente:
                        if self.wert == -1:
                            return -Wolke.Char.getDefaultTalentCost(self.name, fert.steigerungsfaktor)
                        else:
                            return 0

            if self.wert == -1:
                return 0
            fert = None
            if talent.isSpezialTalent():
                fert = Wolke.DB.übernatürlicheFertigkeiten[talent.fertigkeiten[0]]
            else:
                fert = Wolke.DB.fertigkeiten[talent.fertigkeiten[0]]
            return Wolke.Char.getDefaultTalentCost(self.name, fert.steigerungsfaktor)

        elif self.typ == "Vorteil":
            if not self.name in Wolke.DB.vorteile:
                return 0
            vort = Wolke.DB.vorteile[self.name]
            if vort.variableKosten:
                return self.wert
            if self.name in Wolke.Char.vorteile:
                if self.wert == -1:
                    return -vort.kosten
                return 0
            if self.wert == -1:
                return 0
            return vort.kosten

        else:
            return 0

class ChoiceList(object):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.beschreibung = None
        self.varianten = None
        self.keineVarianten = None
        self.geschlecht = None
        self.choices = []

    def hasVarianten(self):
        return self.varianten and len(self.varianten) > 0

    def meetsConditions(self, geschlecht, variantsSelected):
        if self.geschlecht and self.geschlecht != geschlecht:
            return False

        if self.keineVarianten:
            for index in variantsSelected:
                if index in self.keineVarianten:
                    return False

        if self.varianten:
            for index in variantsSelected:
                if index in self.varianten:
                    return True
            return False
        return True

    def doVariantenIntersect(self, other):
        if not self.varianten or not other.varianten:
            return False

        for index in self.varianten:
            if index in other.varianten:
                return True
        return False

    def filter(self, choice):
        self.choices = [c for c in self.choices if not (c.name == choice.name and c.typ == choice.typ and c.kommentar == choice.kommentar)]

    def toString(self):
        return self.name + " (" + str(self.countEP()) + " EP)"

    def getDescription(self):
        if len(self.choices) > 0:
            return "        " + "\n        ".join([c.toString(False) for c in self.choices])
        else:
            return None

    def countEP(self):
        count = 0
        for choice in self.choices:
            count += choice.countEP()
        return count

class ChoiceListCollection(object):
    def __init__(self):
        super().__init__()
        self.chooseOne = True
        self.choiceLists = []

    def filter(self, startIndex, choice):
        #Remove choice further down the choices list
        choiceList = self.choiceLists[startIndex]
        if startIndex + 1 == len(self.choiceLists):
            return
        for i in range(startIndex + 1, len(self.choiceLists)):
            cl = self.choiceLists[i]
            if (not choiceList.hasVarianten() and not cl.hasVarianten()) or choiceList.doVariantenIntersect(cl):
                cl.filter(choice)