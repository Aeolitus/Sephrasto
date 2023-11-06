from EventBus import EventBus
from Core.Fertigkeit import KampffertigkeitTyp
from Core.FreieFertigkeit import FreieFertigkeitDefinition
import logging

class Choice(object):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.wert = 0
        self.typ = "Fertigkeit"
        self.kommentar = ""

    def getErrorString(self, char, db):
        # Some paths are logging instead of returning the error.
        # These cases may not always be true, i.e. if the choice is bundled with others inside a variant
        # So we're not displaying these errors because it might be more confusing if the displayed a wrong info
        # Usually the commented out parts mean anyways, that the creator of the template made an error
        if self.typ == "Freie-Fertigkeit":
            for ff in char.freieFertigkeiten:
                if self.name == ff.name:
                    if ff.wert == 3:
                        return "bereits Maximum"
                    break
        elif self.typ == "Fertigkeit":
            if self.name in char.fertigkeiten:
                if self.wert > 0 and char.fertigkeiten[self.name].wert == char.fertigkeiten[self.name].maxWert:
                    logging.warn(f"CharakterAssistent: {self.typ} {self.name} bereits Maximum")
                    return None
                if self.wert < 0 and char.fertigkeiten[self.name].wert == 0:
                    logging.warn(f"CharakterAssistent: {self.typ} {self.name} bereits Minimum")
                    return None
            else:
                logging.warn(f"CharakterAssistent: {self.typ} {self.name} nicht vorhanden")
                return None
        elif self.typ == "Übernatürliche-Fertigkeit":
            if self.name in char.übernatürlicheFertigkeiten:
                if self.wert > 0 and char.übernatürlicheFertigkeiten[self.name].wert == char.übernatürlicheFertigkeiten[self.name].maxWert:
                    logging.warn(f"CharakterAssistent: {self.typ} {self.name} bereits Maximum")
                    return None
                if self.wert < 0 and char.übernatürlicheFertigkeiten[self.name].wert == 0:
                    logging.warn(f"CharakterAssistent: {self.typ} {self.name} bereits Minimum")
                    return None
            else:
                logging.warn(f"CharakterAssistent: {self.typ} {self.name} nicht vorhanden")
                return None
        elif self.typ == "Attribut":
            if self.name in char.attribute and self.wert < 0 and char.attribute[self.name].wert == 0:
                return "bereits Minimum"
        elif self.typ == "Vorteil":
            if self.name in char.vorteile:
                vorteil = char.vorteile[self.name]
                if vorteil.kommentarErlauben and self.kommentar in vorteil.kommentar:
                    return "bereits erworben"

                if not vorteil.variableKosten:
                    return "bereits erworben"
            if not self.name in db.vorteile:
                logging.warn(f"CharakterAssistent: {self.typ} {self.name} unbekannt")
                return None          
            if not char.voraussetzungenPrüfen(db.vorteile[self.name]):
                logging.warn(f"CharakterAssistent: {self.typ} {self.name} Voraussetzungen nicht erfüllt")
                return None
        elif self.typ == "Talent":
            if self.name in char.talente:
                talent = char.talente[self.name]
                if talent.kommentarErlauben and self.kommentar in talent.kommentar:
                    return "bereits erworben"

                if not talent.variableKosten:
                    return "bereits erworben"

            if not self.name in db.talente:
                logging.warn(f"CharakterAssistent: {self.typ} {self.name} unbekannt")
                return None
            if not char.voraussetzungenPrüfen(db.talente[self.name]):
                logging.warn(f"CharakterAssistent: {self.typ} {self.name} Voraussetzungen nicht erfüllt")
                return None
        elif self.typ == "Eigenheit":
            if self.name in char.eigenheiten:
                return "bereits vorhanden"
        return None

    def toString(self, char, db, addEP = True):
        valueStr = ""
        prefix = ""
        if self.typ == "Freie-Fertigkeit":
            fert = None
            for ff in char.freieFertigkeiten:
                if self.name == ff.name:
                    fert = ff
                    break
            if fert:
                werte = ["-", "I", "II", "III"]
                wert = min(self.wert, 3 - ff.wert)
                if wert == 0:
                    valueStr += " +0"
                elif wert == 1:
                    valueStr += " +I"
                elif wert == 2:
                    valueStr += " +II"
                valueStr += " (aktuell " + werte[ff.wert] + ")"
            else:
                if self.wert == 1:
                    valueStr = " I"
                elif self.wert == 2:
                    valueStr = " II"
                elif self.wert == 3:
                    valueStr = " III"

        elif self.typ == "Fertigkeit":
            wert = self.wert
            if self.name in char.fertigkeiten:
                wert = max(min(char.fertigkeiten[self.name].maxWert - char.fertigkeiten[self.name].wert, self.wert), -char.fertigkeiten[self.name].wert)
            if self.wert >= 0:
                valueStr = " +" + str(wert)
            else:
                valueStr = " " + str(wert)

            if self.name in char.fertigkeiten:
                current = char.fertigkeiten[self.name].wert
                valueStr += " (aktuell FW " + str(current) + ")"
        elif self.typ == "Übernatürliche-Fertigkeit":
            wert = self.wert
            if self.name in char.übernatürlicheFertigkeiten:
                wert = max(min(char.übernatürlicheFertigkeiten[self.name].maxWert - char.übernatürlicheFertigkeiten[self.name].wert, self.wert), -char.übernatürlicheFertigkeiten[self.name].wert)
            if self.wert >= 0:
                valueStr = " +" + str(wert)
            else:
                valueStr = " " + str(wert)

            if self.name in char.übernatürlicheFertigkeiten:
                current = char.übernatürlicheFertigkeiten[self.name].wert
                valueStr += " (aktuell FW " + str(current) + ")"
        elif self.typ == "Attribut":
            if self.wert >= 0:
                valueStr = " +" + str(self.wert)
            else:
                valueStr = " " + str(self.wert)

            if self.name in char.attribute:
                current = char.attribute[self.name].wert
                valueStr += " (aktuell " + str(current) + ")"
        else:
            prefix = self.typ + " "

        if (self.typ == "Vorteil" or self.typ == "Talent") and self.wert == -1:
            valueStr += " entfernt"

        if self.kommentar:
            valueStr += " (" + self.kommentar + ")"

        errorString = self.getErrorString(char, db)
        if addEP and self.typ != "Eigenheit" and not errorString:
            if valueStr.endswith(")"):
                valueStr = valueStr[:-1] + "; "
            else:
                valueStr += " ("
            valueStr += str(self.countEP(char, db)) + " EP)"

        if errorString:
            if valueStr.endswith(")"):
                valueStr = valueStr[:-1] + "; "
            else:
                valueStr += " ("
            valueStr += errorString + ")"

        return prefix + self.name + valueStr

    def __countEPNahkampf(self, char, includeChoice = False):
        ep = 0
        höchste = None
        höchsteWert = 0
        for fert in char.fertigkeiten.values():
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

    def countEP(self, char, db):
        if self.typ == "Freie-Fertigkeit":
            for fert in char.freieFertigkeiten:
                if self.name == fert.name:
                    return fert.steigerungskosten(self.wert)
            return EventBus.applyFilter("freiefertigkeit_kosten", FreieFertigkeitDefinition.gesamtkosten[self.wert], { "name" : self.name, "wertVon" : 0, "wertAuf" : self.wert })

        elif self.typ == "Fertigkeit":
            if not self.name in char.fertigkeiten:
                return 0
            fert = char.fertigkeiten[self.name]
            if fert.kampffertigkeit == KampffertigkeitTyp.Nahkampf:
                return self.__countEPNahkampf(char, True) - self.__countEPNahkampf(char)
            oldVal = sum(range(fert.wert+1)) * fert.steigerungsfaktor
            wert = min(fert.maxWert, fert.wert+self.wert)
            newVal = sum(range(wert+1)) * fert.steigerungsfaktor
            return newVal - oldVal

        elif self.typ == "Übernatürliche-Fertigkeit":
            if not self.name in char.übernatürlicheFertigkeiten:
                return 0
            fert = char.übernatürlicheFertigkeiten[self.name]
            oldVal = sum(range(fert.wert+1)) * fert.steigerungsfaktor
            wert = min(fert.maxWert, fert.wert+self.wert)
            newVal = sum(range(wert+1)) * fert.steigerungsfaktor
            return newVal - oldVal

        elif self.typ == "Attribut":
            if not self.name in char.attribute:
                return 0
            attribut = char.attribute[self.name]
            return attribut.steigerungskosten(self.wert)

        elif self.typ == "Talent":
            if not self.name in db.talente:
                return 0
            talentDefinition = db.talente[self.name]
            if self.wert == -1:
                if self.name in char.talente:
                    return -char.talente[self.name].kosten
                return 0
            else:
                if talentDefinition.variableKosten:
                    return self.wert
                return talentDefinition.kosten
        elif self.typ == "Vorteil":
            if not self.name in db.vorteile:
                return 0
            vorteilDefinition = db.vorteile[self.name]
            if self.wert == -1:
                if self.name in char.vorteile:
                    return -char.vorteile[self.name].kosten
                return 0
            else:
                if vorteilDefinition.variableKosten:
                    return self.wert
                return vorteilDefinition.kosten

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

    def toString(self, char, db):
        return self.name + " (" + str(self.countEP(char, db)) + " EP)"

    def getDescription(self, char, db):
        if len(self.choices) > 0:
            return "        " + "\n        ".join([c.toString(char, db, False) for c in self.choices])
        else:
            return None

    def countEP(self, char, db):
        count = 0
        for choice in self.choices:
            count += choice.countEP(char, db)
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