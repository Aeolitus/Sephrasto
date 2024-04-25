from Wolke import Wolke
import re
import math
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from Core.Vorteil import VorteilLinkKategorie
from CharakterPrintUtility import CharakterPrintUtility
from EventBus import EventBus
import base64

class CheatsheetGenerator(object):
    def __init__(self):
        pass

    @staticmethod
    def categoryHeading(title, category):
        if title == category:
            return f"<h1>{title}</h1>"
        if title:
            return f"<h1>{title}</h1><h2>{category}</h2>"
        return f"<h2>{category}</h2>"

    @staticmethod
    def ruleHeading(text):
        return "<h3>" + text + "</h3>"

    def appendWaffeneigenschaften(self, rules, category, eigenschaften):
        if not eigenschaften or (len(eigenschaften) == 0):
            return
        rules.append(category)
        count = 0
        for weName in sorted(list(eigenschaften.keys()), key=Hilfsmethoden.unicodeCaseInsensitive):
            we = Wolke.DB.waffeneigenschaften[weName]
            if not we.text:
                continue
            count += 1
            waffen = eigenschaften[weName]
            rules.append("<article>" + CheatsheetGenerator.ruleHeading(we.name + " (" + ", ".join(waffen) + ")") + we.text + "</article>")

        if count == 0:
            rules.pop()
            return False
        return True

    def isElementActive(self, r, element):
        return f"{r}:{element.kategorie}" not in Wolke.Char.deaktivierteRegelKategorien and f"{r}:{element.name}" not in Wolke.Char.deaktivierteRegelKategorien

    def isLinkedToAny(self, vorteil):
        if vorteil.linkKategorie == VorteilLinkKategorie.Regel:
            return vorteil.linkElement in Wolke.DB.regeln and self.isElementActive("R", Wolke.DB.regeln[vorteil.linkElement])
        elif vorteil.linkKategorie == VorteilLinkKategorie.ÜberTalent:
            if vorteil.linkElement in Wolke.Char.talente and self.isElementActive("S", Wolke.Char.talente[vorteil.linkElement]):
                return True
        elif vorteil.linkKategorie == VorteilLinkKategorie.Vorteil:
            if vorteil.linkElement in Wolke.Char.vorteile and self.isElementActive("V", Wolke.Char.vorteile[vorteil.linkElement]):
                return True
            return self.isLinkedToAny(Wolke.DB.vorteile[vorteil.linkElement])

        return False

    def appendVorteile(self, rules, category, vorteile):
        if not vorteile or (len(vorteile) == 0):
            return
        rules.append(category)
        count = 0
        for vorteil in vorteile:
            if "V:" + vorteil.name in Wolke.Char.deaktivierteRegelKategorien:
                continue

            if not vorteil.cheatsheetAuflisten or self.isLinkedToAny(vorteil):
                continue

            text = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
            if not text:
                continue
            count += 1
            result = []

            result.append("<article>" + CheatsheetGenerator.ruleHeading(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil, descriptionWillFollow=True)))

            bedingungen = CharakterPrintUtility.getLinkedBedingungen(Wolke.Char, vorteil)
            if bedingungen:
                result.append(f"<i>Bedingungen:</i> {bedingungen}\n")

            if "\n" in text and not "<ul" in text and not "<ol" in text:
                text = "<ul><li>" + text.replace("\n", "</li><li>") + "</li></ul>"
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
        rules.append(category)
        count = 0
        for regelName in regelList:
            regel = Wolke.DB.regeln[regelName]
            if "R:" + regel.name in Wolke.Char.deaktivierteRegelKategorien:
                continue

            if not Wolke.Char.voraussetzungenPrüfen(regel):
                continue
            count += 1
            result = []
            result.append("<article>")
            name = regel.anzeigename
            if regel.probe:
                name += " (" + regel.probe + ")"
            result.append(CheatsheetGenerator.ruleHeading(name))
            result.append(regel.text)
           
            linkedText = []
            for vorteil in Wolke.Char.vorteile.values():
                if CharakterPrintUtility.isLinkedTo(Wolke.Char, vorteil, VorteilLinkKategorie.Regel, regelName):
                    beschreibung = CharakterPrintUtility.getLinkedDescription(Wolke.Char, vorteil)
                    if not beschreibung:
                        continue
                    linkedText.append("<li class='checkbox'>")
                    linkedText.append(CharakterPrintUtility.getLinkedName(Wolke.Char, vorteil))
                    linkedText.append(": ")
                    linkedText.append(beschreibung.replace("\n", " "))
                    linkedText.append("</li>")

            if regelName in Wolke.Char.regelInfos:
                for regelInfo in Wolke.Char.regelInfos[regelName]:
                    linkedText.append(f"<li class='checkbox'>{regelInfo}</li>")

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
        rules.append(category)
        count = 0
        for talentName in talente:   
            tal = Wolke.Char.talente[talentName]
            if "S:" + tal.name in Wolke.Char.deaktivierteRegelKategorien:
                continue
            if not tal.cheatsheetAuflisten or not tal.text:
                continue
            count += 1
            result = []
            result.append("<article>" + CheatsheetGenerator.ruleHeading(tal.anzeigename + " (PW " + str(tal.probenwert) + ")"))
            result.append(tal.text)

            linkedText = []
            for vorteil in Wolke.Char.vorteile.values():
                if CharakterPrintUtility.isLinkedTo(Wolke.Char, vorteil, VorteilLinkKategorie.ÜberTalent, tal.name):
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
        
        talenteByKategorie = CharakterPrintUtility.getÜberTalente(Wolke.Char)

        rules = [] 

        sortV = Wolke.Char.vorteile.values()
        sortV = sorted(sortV, key=lambda vor: Hilfsmethoden.unicodeCaseInsensitive(vor.name))
        vorteileGruppiert = []
        for i in range(len(Wolke.DB.einstellungen["Vorteile: Kategorien"].wert)):
            vorteileGruppiert.append([el for el in sortV if el.kategorie == i])

        sortR = list(Wolke.DB.regeln.keys())
        sortR = sorted(sortR, key=Hilfsmethoden.unicodeCaseInsensitive)
        regelnGruppiert = []
        numRegelKategorien = len(Wolke.DB.einstellungen["Regeln: Kategorien"].wert)
        for i in range(numRegelKategorien):
            regelnGruppiert.append([])
        for i in range(numRegelKategorien):
            scriptAPI = Hilfsmethoden.createScriptAPI()
            scriptAPI.update({ "char" : Wolke.Char, "kategorie" : i, "mergeTo" : i })
            exec(Wolke.DB.einstellungen["Regelanhang: Regel Mergescript"].wert, scriptAPI)
            mergeTo = scriptAPI["mergeTo"]
            if mergeTo >= numRegelKategorien:
                mergeTo = i
            empty = len(regelnGruppiert[mergeTo]) == 0
            regelnGruppiert[mergeTo].extend([el for el in sortR if (Wolke.DB.regeln[el].kategorie == i)])
            if not empty:
                regelnGruppiert[mergeTo] = sorted(regelnGruppiert[mergeTo], key=Hilfsmethoden.unicodeCaseInsensitive)

        lastTitle = ""
        title = ""
        for r in Wolke.DB.einstellungen["Regelanhang: Reihenfolge"].wert:
            if r[0] == "T" and len(r) > 2:
                if lastTitle and len(rules) > 0 and rules[-1] == lastTitle:
                    rules.pop()
                title = r[2:]
                lastTitle = title
            if r in Wolke.Char.deaktivierteRegelKategorien:
                continue
            if r[0] == "V" and len(r) > 2 and r[2:].isnumeric():
                kategorie = int(r[2:])
                if kategorie >= len(vorteileGruppiert):
                    continue
                kategorieName = Wolke.DB.einstellungen["Vorteile: Kategorien"].wert.keyAtIndex(kategorie)
                if self.appendVorteile(rules, CheatsheetGenerator.categoryHeading(title, kategorieName), vorteileGruppiert[kategorie]):
                    title = ""
            elif r[0] == "R" and len(r) > 2 and r[2:].isnumeric():
                kategorie = int(r[2:])
                if kategorie >= len(regelnGruppiert):
                    continue
                kategorieName = Wolke.DB.einstellungen["Regeln: Kategorien"].wert.keyAtIndex(kategorie)
                if self.appendRegeln(rules, CheatsheetGenerator.categoryHeading(title, kategorieName), regelnGruppiert[kategorie]):
                    title = ""
            elif r[0] == "W":
                if self.appendWaffeneigenschaften(rules, CheatsheetGenerator.categoryHeading(title, "Waffeneigenschaften"), waffeneigenschaften):
                    title = ""
            elif r[0] == "S" and len(r) > 2 and r[2:].isnumeric():
                kategorie = int(r[2:])
                if kategorie >= len(Wolke.DB.einstellungen["Talente: Kategorien"].wert):
                    continue
                kategorieName = Wolke.DB.einstellungen["Talente: Kategorien"].wert.keyAtIndex(kategorie)
                if self.appendTalente(rules, CheatsheetGenerator.categoryHeading(title, kategorieName), talenteByKategorie[kategorieName]):
                    title = ""
            
            EventBus.doAction("regelanhang_anfuegen", { "reihenfolge" : r, "appendCallback" : lambda text: rules.append(text) })

        if lastTitle and len(rules) > 0 and rules[-1] == lastTitle:
            rules.pop()

        Wolke.Char.voraussetzungenPruefen = voraussetzungenPruefen
        rules = Hilfsmethoden.fixHtml("".join(rules), False)
        return rules