from Charakter import VariableKosten
from CharakterAssistent import ChoicePopupWrapper
from CharakterAssistent import VariantPopupWrapper
from CharakterAssistent import Choice
import Fertigkeiten
import Objekte
import Definitionen
from Wolke import Wolke
import lxml.etree as etree
import logging
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
from CharakterAssistent.XmlVerifier import XmlVerifier

class CharakterMerger(object):
    def __init__(self):
        pass

    def setVariableVorteilKosten(vorteil, var):
        char = Wolke.Char
        if vorteil in char.vorteileVariable:
            if vorteil in char.vorteile:
                char.vorteileVariable[vorteil].kosten += var.kosten
            else:
                char.vorteileVariable[vorteil].kosten = var.kosten

            if var.kommentar != "":
                if char.vorteileVariable[vorteil].kommentar != "":
                    char.vorteileVariable[vorteil].kommentar += ", " + var.kommentar
                else:
                    char.vorteileVariable[vorteil].kommentar = var.kommentar
        else:
            char.vorteileVariable[vorteil] = var

    def setVariableTalentKosten(talent, var):
        char = Wolke.Char
        #round down to nearest multiple in case of a db cost change
        defaultKosten = char.getDefaultTalentCost(talent, fert.steigerungsfaktor)
        var.kosten = max(var.kosten - (var.kosten%defaultKosten), defaultKosten)
        if talent in char.talenteVariable:
            char.talenteVariable[talent].kosten += var.kosten
            if var.kommentar != "":
                if char.talenteVariable[talent].kommentar != "":
                    char.talenteVariable[talent].kommentar += ", " + var.kommentar
                else:
                    char.talenteVariable[talent].kommentar = var.kommentar
        else:
            char.talenteVariable[talent] = var
     
    def addFreieFertigkeit(name, wert, overrideEmpty):
        if name == "":
            return

        char = Wolke.Char
        fert = Fertigkeiten.FreieFertigkeit()            
        fert.name = name
        fert.wert = wert

        found = False
        for ff in char.freieFertigkeiten:
            if fert.name == ff.name:
                ff.wert = min(ff.wert + fert.wert, 3)
                found = True
                break
        if not found:
            if len(char.freieFertigkeiten) == 28:
                return
            if overrideEmpty and fert.wert == 3 and len(char.freieFertigkeiten) > 0 and char.freieFertigkeiten[0].name == "":
                char.freieFertigkeiten[0] = fert
            else:
                char.freieFertigkeiten.append(fert)

    def readChoices(path):
        root = etree.parse(path).getroot()
        XmlVerifier.validateXml(root)

        variantListCollections = []
        for varianten in root.findall('Varianten'):
            variantListCollection = Choice.ChoiceListCollection()
            if 'pflichtwahl' in varianten.attrib:
                variantListCollection.chooseOne = int(varianten.attrib['pflichtwahl']) != 0
            else:
                variantListCollection.chooseOne = False
            CharakterMerger.xmlNodeToChoices(variantListCollection, varianten.findall('Variante'))
            variantListCollections.append(variantListCollection)
        choiceListCollection = Choice.ChoiceListCollection()
        CharakterMerger.xmlNodeToChoices(choiceListCollection, root.findall('Auswahl'))

        return variantListCollections, choiceListCollection

    def handleChoices(paths, title, geschlecht, spezies, kultur, profession):
        char = Wolke.Char

        if not spezies:
            char.kurzbeschreibung += ", "
            if kultur:
                char.kurzbeschreibung += "Kultur: " + title
                EventBus.doAction("cbext_update", { 'name' : "kultur", 'value' : title })
            else:
                char.kurzbeschreibung += "Profession: " + title
                EventBus.doAction("cbext_update", { 'name' : "profession", 'value' : title })

        if len(paths) != 2:
            return

        description = []

        variantListCollections, choiceListCollection = CharakterMerger.readChoices(paths[1])

        variantsSelected = []
        indexOffset = 0

        anyChooseOne = False
        for variantListCollection in variantListCollections:
            variantListCollection.choiceLists = [cl for cl in variantListCollection.choiceLists if cl.meetsConditions(geschlecht, variantsSelected)]

            if (len(variantListCollection.choiceLists) == 0):
                continue

            anyChooseOne = anyChooseOne or variantListCollection.chooseOne
            choices = []
            if (variantListCollection.chooseOne and len(variantListCollection.choiceLists) == 1):
                choices.append(0)
            else:
                popup = VariantPopupWrapper.VariantPopupWrapper(variantListCollection, title)
                choices = popup.choices
            for index in choices:
                variantsSelected.append(indexOffset + index)

                choiceList = variantListCollection.choiceLists[index]

                if choiceList.beschreibung == None:
                    description.append(choiceList.name)
                elif choiceList.beschreibung != "":
                    description.append(choiceList.beschreibung)

                for choice in choiceList.choices:
                    CharakterMerger.applyChoiceToChar(choice)
            indexOffset += len(variantListCollection.choiceLists)

        if len(description) > 0:
            description = ", ".join(description)
            if spezies:
                if anyChooseOne:
                    char.rasse = description
                else:
                    char.rasse = title + " (" + description + ")"
            elif kultur:
                char.kurzbeschreibung += " (" + description + ")"
                EventBus.doAction("cbext_update", { 'name' : "kultur", 'value' : title + " (" + description + ")" })
            elif profession:
                char.kurzbeschreibung += " (" + description + ")"
                EventBus.doAction("cbext_update", { 'name' : "profession", 'value' : title + " (" + description + ")" })

        for i in range(len(choiceListCollection.choiceLists)):
            choiceList = choiceListCollection.choiceLists[i]
            #Some choices are only enabled when a variant was (not) selected
            if not choiceList.meetsConditions(geschlecht, variantsSelected):
                continue

            #Let user choose via popup or auto-choose if there is only one entry (usually due to removal - see below)
            choice = None
            if len(choiceList.choices) > 1:
                popup = ChoicePopupWrapper.ChoicePopupWrapper(choiceList, title)
                choice = popup.choice
            elif len(choiceList.choices) == 1:
                choice = choiceList.choices[0]

            if not choice:
                continue
            choiceListCollection.filter(i, choice)
            CharakterMerger.applyChoiceToChar(choice)

    def xmlNodeToChoices(choiceListCollection, node):
        for child in node:
            choiceList = Choice.ChoiceList()

            if 'name' in child.attrib:
                choiceList.name = child.attrib['name']
            if 'varianten' in child.attrib:
                choiceList.varianten = [int(x) for x in child.attrib['varianten'].split(',')]
            if 'keine-varianten' in child.attrib:
                choiceList.keineVarianten = [int(x) for x in child.attrib['keine-varianten'].split(',')]
            if 'beschreibung' in child.attrib:
                choiceList.beschreibung = child.attrib['beschreibung']
            if 'geschlecht' in child.attrib:
                geschlecht = child.attrib['geschlecht']
                if geschlecht != "männlich" and geschlecht != "weiblich":
                    logging.warn("CharakterAssistent: Unbekanntes Geschlecht " + geschlecht)
                else:
                    choiceList.geschlecht = geschlecht

            for fer in child.findall('Eigenheit'):
                choice = Choice.Choice()
                choice.name = fer.attrib['name']
                choice.typ = "Eigenheit"
                choiceList.choices.append(choice)

            for fer in child.findall('Attribut'):
                choice = Choice.Choice()
                choice.name = fer.attrib['name']
                choice.wert = int(fer.attrib['wert'])
                choice.typ = "Attribut"

                if not choice.name in Definitionen.Attribute.keys():
                    logging.warn("CharakterAssistent: konnte Attribut " + choice.name + " nicht finden")
                    continue
                choiceList.choices.append(choice)

            for fer in child.findall('Freie-Fertigkeit'):
                choice = Choice.Choice()
                choice.name = fer.attrib['name']
                choice.wert = int(fer.attrib['wert'])
                choice.typ = "Freie-Fertigkeit"
                choiceList.choices.append(choice)

            for fer in child.findall('Fertigkeit'):
                choice = Choice.Choice()
                choice.name = fer.attrib['name']
                choice.wert = int(fer.attrib['wert'])
                choice.typ = "Fertigkeit"

                if not choice.name in Wolke.DB.fertigkeiten:
                    logging.warn("CharakterAssistent: konnte Fertigkeit " + choice.name + " nicht finden")
                    continue
                choiceList.choices.append(choice)
                
            for fer in child.findall('Übernatürliche-Fertigkeit'):
                choice = Choice.Choice()
                choice.name = fer.attrib['name']
                choice.wert = int(fer.attrib['wert'])
                choice.typ = "Übernatürliche-Fertigkeit"

                if not choice.name in Wolke.DB.übernatürlicheFertigkeiten:
                    logging.warn("CharakterAssistent: konnte Übernatürliche Fertigkeit " + choice.name + " nicht finden")
                    continue
                choiceList.choices.append(choice)

            for vor in child.findall('Vorteil'):
                choice = Choice.Choice()
                choice.name = vor.attrib['name']
                choice.typ = "Vorteil"
                if "kommentar" in vor.attrib:
                    choice.kommentar = vor.attrib["kommentar"]
                if "wert" in vor.attrib:
                    choice.wert = int(vor.attrib["wert"])

                if not choice.name in Wolke.DB.vorteile:
                    logging.warn("CharakterAssistent: konnte Vorteil " + choice.name + " nicht finden")
                    continue
                choiceList.choices.append(choice)

            for vor in child.findall('Talent'):
                choice = Choice.Choice()
                choice.name = vor.attrib['name']
                choice.typ = "Talent"

                if not choice.name in Wolke.DB.talente:
                    logging.warn("CharakterAssistent: konnte Talent " + choice.name + " nicht finden")
                    continue
                choiceList.choices.append(choice)

            choiceListCollection.choiceLists.append(choiceList)

    def applyChoiceToChar(choice):
        char = Wolke.Char

        if choice.typ == "Eigenheit":
            if len(char.eigenheiten) == 8:
                return
            if not choice.name in char.eigenheiten:
                char.eigenheiten.append(choice.name)
        elif choice.typ == "Attribut":
            if not choice.name in char.attribute:
                return
            char.attribute[choice.name].wert += int(choice.wert)
            char.attribute[choice.name].aktualisieren()
        elif choice.typ == "Freie-Fertigkeit":
            CharakterMerger.addFreieFertigkeit(choice.name, choice.wert, True)
        elif choice.typ == "Fertigkeit":
            char.fertigkeiten[choice.name].wert = max(char.fertigkeiten[choice.name].wert + choice.wert, 0)
            char.fertigkeiten[choice.name].aktualisieren(char.attribute)
        elif choice.typ == "Übernatürliche-Fertigkeit":
            char.übernatürlicheFertigkeiten[choice.name].wert = max(char.übernatürlicheFertigkeiten[choice.name].wert + choice.wert, 0)
            char.übernatürlicheFertigkeiten[choice.name].aktualisieren(char.attribute)
        elif choice.typ == "Vorteil":
            if Wolke.DB.vorteile[choice.name].variableKosten:
                var = VariableKosten()
                var.kosten = choice.wert
                var.kommentar = choice.kommentar
                CharakterMerger.setVariableVorteilKosten(choice.name, var)
            if choice.name in char.vorteile:
                return
            char.vorteile.append(choice.name)
            EventBus.doAction("vorteil_gekauft", { "name" : choice.name})
        elif choice.typ == "Talent":
            found = False
            for name, fert in char.fertigkeiten.items():
                if choice.name in fert.gekaufteTalente:
                    return
            for name, fert in char.übernatürlicheFertigkeiten.items():
                if choice.name in fert.gekaufteTalente:
                    return

            for fert in Wolke.DB.talente[choice.name].fertigkeiten:
                if fert in char.fertigkeiten:
                    char.fertigkeiten[fert].gekaufteTalente.append(choice.name)
                if fert in char.übernatürlicheFertigkeiten:
                    char.übernatürlicheFertigkeiten[fert].gekaufteTalente.append(choice.name)

    def xmlLesen(path, spezies, kultur):
        def parseVariableKosten(variable):
            var = list(map(str.strip, variable.split(",", 1)))
            if int(var[0]) != -1:
                vk = VariableKosten()
                vk.kosten = int(var[0])
                if len(var) > 1:
                    vk.kommentar = var[1]
                return vk
            return None

        char = Wolke.Char
        root = etree.parse(path).getroot()

        alg = root.find('AllgemeineInfos')

        char.name = alg.find('name').text or ''
        char.status = int(alg.find('status').text)

        kurzbeschreibung = alg.find('kurzbeschreibung').text or ''
        if kurzbeschreibung:
            if char.kurzbeschreibung:
                char.kurzbeschreibung += ", "
            char.kurzbeschreibung += kurzbeschreibung
        char.finanzen = int(alg.find('finanzen').text)

        if spezies:
            char.rasse = alg.find('rasse').text or ''

        tmp = alg.find('heimat')
        skipTal = ""
        if not tmp is None:
            if kultur:
                if "Gebräuche" in char.fertigkeiten:
                    gebräucheFert = char.fertigkeiten["Gebräuche"]
                    oldTal = "Gebräuche: " + char.heimat
                    if oldTal in gebräucheFert.gekaufteTalente:
                        gebräucheFert.gekaufteTalente.remove(oldTal)
                char.heimat = tmp.text
            else:
                skipTal = "Gebräuche: " + tmp.text

        for eig in alg.findall('eigenheiten/*'):
            if len(char.eigenheiten) == 8:
                break
            if eig.text and not (eig.text in char.eigenheiten):
                char.eigenheiten.append(eig.text)

        for atr in root.findall('Attribute/*'):
            if not spezies and not kultur:
                char.attribute[atr.tag].wert = max(char.attribute[atr.tag].wert, int(atr.text))
            else:
                char.attribute[atr.tag].wert += int(atr.text)
            char.attribute[atr.tag].aktualisieren()

        for ene in root.findall('Energien/AsP'):
            char.asp.wert += int(ene.attrib['wert'])
        for ene in root.findall('Energien/KaP'):
            char.kap.wert += int(ene.attrib['wert'])

        for vor in root.findall('Vorteile'):
            if "minderpakt" in vor.attrib:
                char.minderpakt = vor.get('minderpakt')
                EventBus.doAction("vorteil_gekauft", { "name" : char.minderpakt})
            else:
                char.minderpakt = None

        for vor in root.findall('Vorteile/*'):
            if not vor.text in Wolke.DB.vorteile:
                continue
            var = parseVariableKosten(vor.get('variable'))
            if var:
                CharakterMerger.setVariableVorteilKosten(vor.text, var)

            if vor.text in char.vorteile:
                continue
            char.vorteile.append(vor.text)
            EventBus.doAction("vorteil_gekauft", { "name" : vor.text})

        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            nam = fer.attrib['name']
            if not nam in Wolke.DB.fertigkeiten:
                continue

            if nam in char.fertigkeiten:
                fert = char.fertigkeiten[nam].__deepcopy__()
            else:
                fert = Wolke.DB.fertigkeiten[nam].__deepcopy__()

            fert.wert += int(fer.attrib['wert'])
            for tal in fer.findall('Talente/Talent'):
                nam = tal.attrib['name']
                if not nam in Wolke.DB.talente:
                    continue
                if nam in fert.gekaufteTalente:
                    continue
                if nam == skipTal:
                    continue
                fert.gekaufteTalente.append(nam)
                var = parseVariableKosten(tal.attrib['variable'])
                if var:
                    CharakterMerger.setVariableTalentKosten(nam, var)

            fert.aktualisieren(char.attribute)
            char.fertigkeiten.update({fert.name: fert})

        for fer in root.findall('Fertigkeiten/Freie-Fertigkeit'):
            CharakterMerger.addFreieFertigkeit(fer.attrib['name'], int(fer.attrib['wert']), False)

        objekte = root.find('Objekte');
        for rüs in objekte.findall('Rüstungen/Rüstung'):
            if len(char.rüstung) == 3:
                break

            exists = False
            for r in char.rüstung:
                if r.name == rüs.attrib['name']:
                    exists = True
                    break
            if exists:
                continue

            rüst = Objekte.Ruestung()
            rüst.name = rüs.attrib['name']
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = Hilfsmethoden.RsStr2Array(rüs.attrib['rs'])
            char.rüstung.append(rüst)

        for waf in objekte.findall('Waffen/Waffe'):
            if len(char.waffen) == 8:
                break

            exists = False
            for w in char.waffen:
                if w.name == waf.get('id'):
                    exists = True
                    break
            if exists:
                continue
            
            if waf.attrib['typ'] == 'Nah':
                waff = Objekte.Nahkampfwaffe()
            else:
                waff = Objekte.Fernkampfwaffe()
                waff.lz = int(waf.attrib['lz'])
            waff.wm = int(waf.get('wm') or 0)
            waff.anzeigename = waf.attrib['name']
            waff.name = waf.get('id') or waff.anzeigename
            waff.rw = int(waf.attrib['rw'])
            waff.W6 = int(waf.attrib['W6'])
            waff.plus = int(waf.attrib['plus'])
            if waf.attrib['eigenschaften']:
                waff.eigenschaften = list(map(str.strip, waf.attrib['eigenschaften'].split(",")))
            waff.haerte = int(waf.attrib['haerte'])
            waff.kampfstil = waf.attrib['kampfstil']
            if waff.name in Wolke.DB.waffen:
                dbWaffe = Wolke.DB.waffen[waff.name]
                waff.fertigkeit = dbWaffe.fertigkeit
                waff.talent = dbWaffe.talent
                waff.kampfstile = dbWaffe.kampfstile.copy()

            char.waffen.append(waff)

        for aus in objekte.findall('Ausrüstung/Ausrüstungsstück'):
            if len(char.ausrüstung) == 20:
                break
            if aus.text and not (aus.text in char.ausrüstung):
                char.ausrüstung.append(aus.text)

        for fer in root.findall('Übernatürliche-Fertigkeiten/Übernatürliche-Fertigkeit'):
            nam = fer.attrib['name']
            if not nam in Wolke.DB.übernatürlicheFertigkeiten:
                continue

            if nam in char.übernatürlicheFertigkeiten:
                fert = char.übernatürlicheFertigkeiten[nam].__deepcopy__()
            else:
                fert = Wolke.DB.übernatürlicheFertigkeiten[nam].__deepcopy__()

            fert.wert += int(fer.attrib['wert'])
            if 'addToPDF' in fer.attrib:
                fert.addToPDF = fer.attrib['addToPDF'] == "True"
            for tal in fer.findall('Talente/Talent'):
                nam = tal.attrib['name']
                if not nam in Wolke.DB.talente:
                    continue
                if nam in fert.gekaufteTalente:
                    continue
                fert.gekaufteTalente.append(nam)
                var = parseVariableKosten(tal.attrib['variable'])
                if var:
                    CharakterMerger.setVariableTalentKosten(nam, var)

            fert.aktualisieren(char.attribute)
            char.übernatürlicheFertigkeiten.update({fert.name: fert})