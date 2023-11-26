from CharakterAssistent import ChoicePopupWrapper
from CharakterAssistent import VariantPopupWrapper
from CharakterAssistent import Choice
from Core.Energie import Energie
from Core.Ruestung import Ruestung, RuestungDefinition
from Core.Waffe import Waffe
from Core.Fertigkeit import Fertigkeit
from Core.FreieFertigkeit import FreieFertigkeit, FreieFertigkeitDefinition
import lxml.etree as etree
import logging
from Hilfsmethoden import Hilfsmethoden
from EventBus import EventBus
from CharakterAssistent.ChoiceXmlVerifier import ChoiceXmlVerifier
from Migrationen import Migrationen
import os
from VoraussetzungenListe import VoraussetzungenListe

class CharakterMerger:
    def __init__(self):
        pass
    
    def addFreieFertigkeit(char, db, name, wert, overrideEmpty):
        if name == "":
            return

        definition = None
        if name in db.freieFertigkeiten:
            definition = db.freieFertigkeiten[name]
        else:
            definition = FreieFertigkeitDefinition()
            definition.name = name
        fert = FreieFertigkeit(definition, char)            
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

    def readChoices(db, path):
        root = etree.parse(path).getroot()
        errors = []
        errors.extend(ChoiceXmlVerifier.validateXml(root))

        variantListCollections = []
        for varianten in root.findall('Varianten'):
            variantListCollection = Choice.ChoiceListCollection()
            if 'pflichtwahl' in varianten.attrib:
                variantListCollection.chooseOne = int(varianten.attrib['pflichtwahl']) != 0
            else:
                variantListCollection.chooseOne = False
            errors.extend(CharakterMerger.xmlNodeToChoices(db, variantListCollection, varianten.findall('Variante')))
            variantListCollections.append(variantListCollection)
        choiceListCollection = Choice.ChoiceListCollection()
        errors.extend(CharakterMerger.xmlNodeToChoices(db, choiceListCollection, root.findall('Auswahl')))

        return variantListCollections, choiceListCollection, errors

    def verifyChoices(db, path):
        _, _, errors = CharakterMerger.readChoices(db, path)
        if len(errors) > 0:
            errors.insert(0, f"<b>Fehler gefunden in {os.path.basename(path)}</b>")
            errors.append("<hr>")
        return errors

    def handleChoices(char, db, element, geschlecht, spezies, kultur, profession):
        if not spezies:
            if char.kurzbeschreibung:
                char.kurzbeschreibung += ", "
            if kultur:
                char.kurzbeschreibung += "Kultur: " + element.name
                char.kultur = element.name
            else:
                char.kurzbeschreibung += "Profession: " + element.name
                char.profession = element.name

        if not element.varPath:
            return

        description = []

        variantListCollections, choiceListCollection, _ = CharakterMerger.readChoices(db, element.varPath)

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
                popup = VariantPopupWrapper.VariantPopupWrapper(char, db, variantListCollection, element.name, char.epAusgegeben)
                choices = popup.choices
            for index in choices:
                variantsSelected.append(indexOffset + index)

                choiceList = variantListCollection.choiceLists[index]

                if choiceList.beschreibung == None:
                    description.append(choiceList.name)
                elif choiceList.beschreibung != "":
                    description.append(choiceList.beschreibung)

                for choice in choiceList.choices:
                    CharakterMerger.applyChoiceToChar(char, db, choice)
            indexOffset += len(variantListCollection.choiceLists)

        if len(description) > 0:
            description = ", ".join(description)
            if spezies:
                if anyChooseOne:
                    char.spezies = description
                else:
                    char.spezies = element.name + " (" + description + ")"
            elif kultur:
                char.kurzbeschreibung += " (" + description + ")"
                char.kultur = element.name + " (" + description + ")"
            elif profession:
                char.kurzbeschreibung += " (" + description + ")"
                char.profession = element.name + " (" + description + ")"

        for i in range(len(choiceListCollection.choiceLists)):
            choiceList = choiceListCollection.choiceLists[i]
            #Some choices are only enabled when a variant was (not) selected
            if not choiceList.meetsConditions(geschlecht, variantsSelected):
                continue

            #Let user choose via popup or auto-choose if there is only one entry (usually due to removal - see below)
            popup = ChoicePopupWrapper.ChoicePopupWrapper(char, db, choiceList, element.name, char.epAusgegeben)
            choice = popup.choice

            if not choice:
                continue
            choiceListCollection.filter(i, choice)
            CharakterMerger.applyChoiceToChar(char, db, choice)

    def xmlNodeToChoices(db, choiceListCollection, node):
        errors = []
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
                choiceList.geschlecht = child.attrib['geschlecht']

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

                if not choice.name in db.attribute:
                    errors.append("Konnte Attribut " + choice.name + " nicht finden")
                    logging.warn(errors[-1])
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

                if not choice.name in db.fertigkeiten:
                    errors.append("Konnte Fertigkeit " + choice.name + " nicht finden")
                    logging.warn(errors[-1])
                    continue
                choiceList.choices.append(choice)
                
            for fer in child.findall('Übernatürliche-Fertigkeit'):
                choice = Choice.Choice()
                choice.name = fer.attrib['name']
                choice.wert = int(fer.attrib['wert'])
                choice.typ = "Übernatürliche-Fertigkeit"

                if not choice.name in db.übernatürlicheFertigkeiten:
                    errors.append("Konnte Übernatürliche Fertigkeit " + choice.name + " nicht finden")
                    logging.warn(errors[-1])
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

                if not choice.name in db.vorteile:
                    errors.append("Konnte Vorteil " + choice.name + " nicht finden")
                    logging.warn(errors[-1])
                    continue
                choiceList.choices.append(choice)

            for tal in child.findall('Talent'):
                choice = Choice.Choice()
                choice.name = tal.attrib['name']
                choice.typ = "Talent"
                if "kommentar" in tal.attrib:
                    choice.kommentar = tal.attrib["kommentar"]
                if "wert" in tal.attrib:
                    choice.wert = int(tal.attrib["wert"])

                if not choice.name in db.talente:
                    errors.append("Konnte Talent " + choice.name + " nicht finden")
                    logging.warn(errors[-1])
                    continue
                choiceList.choices.append(choice)

            choiceListCollection.choiceLists.append(choiceList)
        return errors

    def applyChoiceToChar(char, db, choice):
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
            CharakterMerger.addFreieFertigkeit(char, db, choice.name, choice.wert, True)
        elif choice.typ == "Fertigkeit":
            if not choice.name in char.fertigkeiten:
                return
            char.fertigkeiten[choice.name].wert = max(char.fertigkeiten[choice.name].wert + choice.wert, 0)
            char.fertigkeiten[choice.name].aktualisieren()
        elif choice.typ == "Übernatürliche-Fertigkeit":
            if not choice.name in char.übernatürlicheFertigkeiten:
                return
            char.übernatürlicheFertigkeiten[choice.name].wert = max(char.übernatürlicheFertigkeiten[choice.name].wert + choice.wert, 0)
            char.übernatürlicheFertigkeiten[choice.name].aktualisieren()
        elif choice.typ == "Vorteil":
            if choice.wert == -1:
                char.removeVorteil(choice.name)
            else:
                exists = choice.name in char.vorteile
                vorteil = char.addVorteil(choice.name)
                if vorteil.kommentarErlauben and choice.kommentar in vorteil.kommentar:
                    return

                if vorteil.variableKosten:
                    if exists:
                        vorteil.kosten += choice.wert
                    else:
                        vorteil.kosten = choice.wert
                if vorteil.kommentarErlauben and choice.kommentar:
                    if vorteil.kommentar:
                        vorteil.kommentar += ", " + choice.kommentar
                    else:
                        vorteil.kommentar = choice.kommentar
        elif choice.typ == "Talent":
            found = False
            if choice.wert == -1:
                char.removeTalent(choice.name)
            else:      
                exists = choice.name in char.talente
                talent = char.addTalent(choice.name)
                if talent.kommentarErlauben and choice.kommentar in talent.kommentar:
                    return

                if talent.variableKosten:
                    if exists:
                        talent.kosten += choice.wert
                    else:
                        talent.kosten = choice.wert
                if talent.kommentarErlauben and choice.kommentar:
                    if talent.kommentar:
                        talent.kommentar += ", " + choice.kommentar
                    else:
                        talent.kommentar = choice.kommentar
        char.aktualisieren()

    def xmlLesen(char, db, path, spezies, kultur):
        root = etree.parse(path).getroot()
        Migrationen.charakterMigrieren(root)

        alg = root.find('Beschreibung')

        char.name = alg.find('Name').text or ''
        char.status = int(alg.find('Status').text)

        kurzbeschreibung = alg.find('Kurzbeschreibung').text or ''
        if kurzbeschreibung:
            if char.kurzbeschreibung:
                char.kurzbeschreibung += ", "
            char.kurzbeschreibung += kurzbeschreibung
        char.finanzen = int(alg.find('Finanzen').text)

        if spezies:
            char.spezies = alg.find('Spezies').text or ''

        tmp = alg.find('Heimat')
        skipTal = ""
        if not tmp is None:
            if kultur:
                char.heimat = tmp.text
            else:
                skipTal = "Gebräuche: " + tmp.text

        for eig in alg.findall('Eigenheiten/*'):
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

        for ene in root.findall('Energien/*'):
            if not ene.tag in db.energien:
                continue
            if ene.tag in char.energien:
                energie = char.energien[ene.tag].__deepcopy__()
            else:
                energie = Energie(db.energien[ene.tag], char)

            energie.wert += int(ene.attrib['wert'])
            char.energien.update({energie.name: energie})

        for vor in root.findall('Vorteile/Vorteil'):
            name = vor.attrib['name']
            if not name in db.vorteile:
                continue
            exists = name in char.vorteile
            vorteil = char.addVorteil(name)

            if vorteil.kommentarErlauben and 'kommentar' in vor.attrib and vor.attrib['kommentar'] in vorteil.kommentar:
                continue

            if vorteil.variableKosten and 'variableKosten' in vor.attrib:
                if exists:
                    vorteil.kosten += int(vor.attrib['variableKosten'])
                else:
                    vorteil.kosten = int(vor.attrib['variableKosten'])
            if vorteil.kommentarErlauben and 'kommentar' in vor.attrib and vor.attrib['kommentar']:
                if vorteil.kommentar:
                    vorteil.kommentar += ", " + vor.attrib['kommentar']
                else:
                    vorteil.kommentar = vor.attrib['kommentar']

        if "Minderpakt" in char.vorteile:
            minderpakt = char.vorteile["Minderpakt"]

            #remove potential existing minderpakte
            kommentare = minderpakt.kommentar.split(", ")
            if len(kommentare) > 1:
                for kommentar in kommentare[:-1]:
                    char.removeVorteil(kommentar)
            minderpakt.kommentar = kommentare[-1]

            #handle minderpakt as the regular character load would
            if not minderpakt.kommentar in db.vorteile:
                char.removeVorteil(minderpakt)
            else:
                minderpakt.voraussetzungen = VoraussetzungenListe().compile("Vorteil " + minderpakt.kommentar, db)
                vorteil = char.addVorteil(minderpakt.kommentar)
                vorteil.voraussetzungen = VoraussetzungenListe().compile("Vorteil Minderpakt", db)
                vorteil.kosten = 20

        for fer in root.findall('Fertigkeiten/Fertigkeit'):
            nam = fer.attrib['name']
            if not nam in db.fertigkeiten:
                continue

            if nam in char.fertigkeiten:
                fert = char.fertigkeiten[nam].__deepcopy__()
            else:
                fert = Fertigkeit(db.fertigkeiten[nam], char)

            fert.wert += int(fer.attrib['wert'])
            fert.aktualisieren()
            char.fertigkeiten.update({fert.name: fert})

        for fer in root.findall('Fertigkeiten/FreieFertigkeit'):
            CharakterMerger.addFreieFertigkeit(char, db, fer.attrib['name'], int(fer.attrib['wert']), False)

        objekte = root.find('Objekte');
        for rüs in objekte.findall('Rüstungen/Rüstung'):
            if len(char.rüstung) == 3:
                break
            name = rüs.attrib['name']
            if not name:
                continue

            exists = False
            for r in char.rüstung:
                if r.name == name:
                    exists = True
                    break
            if exists:
                continue

            if name in db.rüstungen:
                rüst = Ruestung(db.rüstungen[name])
            else:
                definition = RuestungDefinition()
                definition.name = name
                rüst = Ruestung(definition)
            rüst.be = int(rüs.attrib['be'])
            rüst.rs = Hilfsmethoden.RsStr2Array(rüs.attrib['rs'])
            char.rüstung.append(rüst)

        for waf in objekte.findall('Waffen/Waffe'):
            if len(char.waffen) == 8:
                break
            
            if not waf.attrib['name']:
                continue

            nam = waf.attrib['id']
            if not nam in db.waffen or nam in [w.name for w in char.waffen]:
                continue
            
            waff = Waffe(db.waffen[nam])

            if waff.fernkampf:
                waff.lz = int(waf.attrib['lz'])
            waff.wm = int(waf.get('wm') or 0)
            waff.anzeigename = waf.attrib['name']
            waff.rw = int(waf.attrib['rw'])
            waff.würfel = int(waf.attrib['würfel'])
            waff.würfelSeiten = int(waf.attrib['würfelSeiten'])
            waff.plus = int(waf.attrib['plus'])
            if waf.attrib['eigenschaften']:
                waff.eigenschaften = list(map(str.strip, waf.attrib['eigenschaften'].split(",")))
            waff.härte = int(waf.attrib['härte'])
            waff.kampfstil = waf.attrib['kampfstil']
            char.waffen.append(waff)

        for aus in objekte.findall('Ausrüstung/Ausrüstungsstück'):
            if len(char.ausrüstung) == 20:
                break
            if aus.text and not (aus.text in char.ausrüstung):
                char.ausrüstung.append(aus.text)

        for fer in root.findall('ÜbernatürlicheFertigkeiten/ÜbernatürlicheFertigkeit'):
            nam = fer.attrib['name']
            if not nam in db.übernatürlicheFertigkeiten:
                continue

            if nam in char.übernatürlicheFertigkeiten:
                fert = char.übernatürlicheFertigkeiten[nam].__deepcopy__()
            else:
                fert = Fertigkeit(db.übernatürlicheFertigkeiten[nam], char)

            fert.wert += int(fer.attrib['wert'])
            if 'exportieren' in fer.attrib:
                fert.addToPDF = fer.attrib['exportieren'] == "1"
            fert.aktualisieren()
            char.übernatürlicheFertigkeiten.update({fert.name: fert})

        for tal in root.findall('Talente/Talent'):
            nam = tal.attrib['name']
            if not nam in db.talente:
                continue
            if nam == skipTal:
                continue

            exists = nam in char.talente
            talent = char.addTalent(nam)

            if talent.kommentarErlauben and 'kommentar' in tal.attrib and tal.attrib['kommentar'] in talent.kommentar:
                continue

            if talent.variableKosten and 'variableKosten' in tal.attrib:
                if exists:
                    talent.kosten += + int(tal.attrib['variableKosten'])
                else:
                    talent.kosten = int(tal.attrib['variableKosten'])

            if talent.kommentarErlauben and 'kommentar' in tal.attrib and tal.attrib['kommentar']:
                if talent.kommentar:
                    talent.kommentar += ", " + tal.attrib['kommentar']
                else:
                    talent.kommentar = tal.attrib['kommentar']

        char.aktualisieren()