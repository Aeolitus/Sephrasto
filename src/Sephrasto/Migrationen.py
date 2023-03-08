import Fertigkeiten
import lxml.etree as etree
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException, WaffeneigenschaftException
import os.path
import Objekte
from PySide6 import QtWidgets
from Wolke import Wolke
import logging
from DatenbankEinstellung import DatenbankEinstellung
from EventBus import EventBus
import re

# ACHTUNG: Niemals existierenden Migrationscode ändern oder löschen!
# Migrationscode verändert die xml nodes von Charakter- oder Hausregeldateien, bevor sie eingelesen werden.
# Die Versionsnummer aus der Datei wird verglichen mit der Versionsnummer aus dem code, dann wird (beginnend bei der Dateiversion) jede Migrationsfunktion ausgeführt, bis die Codeversion erreicht ist
# Beim Migrationscode immer darauf achten, dass Datenbankelemente via Hausregeln editiert worden sein können. In diesem Fall ist deren attribut "userAdded" == True.
# Je nach Situation sollte eine Migration dann nicht ausgeführt werden.
# Die Charakter-Migrationsfunktionen können einen string zurückgeben, der erklärt was geändert wurde - dies wird dem Nutzer in einer Messagebox angezeigt.

# Beispielmigration:
# if not 'Handgemenge' in Wolke.DB.fertigkeiten or not Wolke.DB.fertigkeiten['Handgemenge'].isUserAdded:
#     for fer in xmlRoot.findall('Fertigkeiten/Fertigkeit'):
#         if fer.attrib['name'] == 'Handgemenge':
#             fer.attrib['name'] = 'Raufen'
#             return "Handgemenge wurde in Raufen umbenannt"
# return None
class Migrationen():
    def __init__(self):
        pass

    datenbankCodeVersion = 6
    charakterCodeVersion = 4

    def hausregelnMigrieren(datenbank, xmlRoot, hausregelnVersion):
        migrationen = [
            lambda datenbank, xmlRoot: None, #nichts zu tun, initiale db version
            Migrationen.hausregeln0zu1,    
            Migrationen.hausregeln1zu2,
            Migrationen.hausregeln2zu3,
            Migrationen.hausregeln3zu4,
            Migrationen.hausregeln4zu5,
            Migrationen.hausregeln5zu6,
        ]

        if not migrationen[Migrationen.datenbankCodeVersion]:
            raise Exception("Migrations-Code vergessen.")

        dbChanged = hausregelnVersion < Migrationen.datenbankCodeVersion
        while hausregelnVersion < Migrationen.datenbankCodeVersion:
            logging.warning("Migriere Hausregeln von Version " + str(hausregelnVersion ) + " zu " + str(hausregelnVersion + 1))
            hausregelnVersion +=1
            migrationen[hausregelnVersion](datenbank, xmlRoot)

    def charakterMigrieren(charakter, xmlRoot, charakterVersion):
        migrationen = [
            lambda charakter, xmlRoot: None, #nichts zu tun, initiale db version
            Migrationen.charakter0zu1, 
            Migrationen.charakter1zu2, 
            Migrationen.charakter2zu3,
            Migrationen.charakter3zu4,
        ]

        if not migrationen[Migrationen.charakterCodeVersion]:
            raise Exception("Migrations-Code vergessen.")

        updates = []
        while charakterVersion < Migrationen.charakterCodeVersion:
            logging.warning("Migriere Charakter von Version " + str(charakterVersion) + " zu " + str(charakterVersion + 1))
            charakterVersion +=1
            update = migrationen[charakterVersion](charakter, xmlRoot)
            if update:
                updates.append(update)

        return updates

    #--------------------------------
    # Hausregeln Migrationsfunktionen
    #--------------------------------

    def hausregeln0zu1(datenbank, root):
        for wa in root.findall('Waffe'):
            kampfstile = []
            if int(wa.get('beid')) == 1:
                kampfstile.append("Beidhändiger Kampf")
            if int(wa.get('pari')) == 1:
                kampfstile.append("Parierwaffenkampf")
            if int(wa.get('reit')) == 1:
                kampfstile.append("Reiterkampf")
            if int(wa.get('schi')) == 1:
                kampfstile.append("Schildkampf")
            if int(wa.get('kraf')) == 1:
                kampfstile.append("Kraftvoller Kampf")
            if int(wa.get('schn')) == 1:
                kampfstile.append("Schneller Kampf")

            wa.attrib.pop('beid')
            wa.attrib.pop('pari')
            wa.attrib.pop('reit')
            wa.attrib.pop('schi')
            wa.attrib.pop('kraf')
            wa.attrib.pop('schn')
            wa.set('kampfstile', ", ".join(kampfstile))

    def hausregeln1zu2(datenbank, root):
        # Apply the added attributes to the user database to make their life easier
        for ta in root.findall('Talent'):
            name = ta.get('name')
            if name in datenbank.talente:
                ta.set('referenzbuch', '0')
                ta.set('referenzseite', str(datenbank.talente[name].referenzSeite))
        for fe in root.findall('Übernatürliche-Fertigkeit'):
            name = fe.get('name')
            if name in datenbank.übernatürlicheFertigkeiten and datenbank.übernatürlicheFertigkeiten[name].talenteGruppieren:
                fe.set('talentegruppieren', '1')

    def hausregeln2zu3(datenbank, root):
        def fixTalentVoraussetzungen(type):
            for node in root.findall(type):
                vor = node.get('voraussetzungen')
                if not vor:
                    continue
                node.set('voraussetzungen', re.sub(r"Talent \s*(.*?)\s*(,| ODER |$)", r"Talent '\1'\2", vor))

        fixTalentVoraussetzungen('Talent')
        fixTalentVoraussetzungen('Vorteil')
        fixTalentVoraussetzungen('Manöver')
        fixTalentVoraussetzungen('Waffeneigenschaft')
        fixTalentVoraussetzungen('FreieFertigkeit')
        fixTalentVoraussetzungen('Fertigkeit')
        fixTalentVoraussetzungen('Übernatürliche-Fertigkeit')

    def hausregeln3zu4(datenbank, root):
        stripped = ["Krähenruf ", "Ruhe Körper, Ruhe Geist ", "Auge des Limbus ", "Aerofugo Vakuum ", "Schutz des Dolches ", "Lied der Lieder ",
                    "Nemekaths Geisterblick ", "Phexens Augenzwinkern ", "Daradors Bann der Schatten ", "Licht des Herrn ", "Harmonischer Rausch ", "Bund der Schwerter "]

        for node in root.findall('Talent'):
            if node.get('name') in stripped:
                node.set('name', node.get('name').strip())
            if 'variable' in node.attrib:
                node.set('variableKosten', node.get('variable'))
                node.attrib.pop('variable')

        for node in root.findall('Vorteil'):
            if 'variable' in node.attrib:
                node.set('variableKosten', node.get('variable'))
                node.attrib.pop('variable')

        for node in root.findall('Remove'):
            if node.get('name') in stripped:
                node.set('name', node.get('name').strip())

        for node in root.findall('FreieFertigkeit'):
            node.set('name', node.text)
            node.text = ""

        for node in root.findall('Fertigkeit'):
            node.set('typ', node.get('printclass'))
            node.attrib.pop('printclass')

        for node in root.findall('Übernatürliche-Fertigkeit'):
            node.tag = 'ÜbernatürlicheFertigkeit'
            node.set('typ', node.get('printclass'))
            node.attrib.pop('printclass')

        for node in root.findall('Waffe'):
            node.set('härte', node.get('haerte'))
            node.attrib.pop('haerte')
            node.set('würfelSeiten', '6')
            node.set('würfel', node.get('W6'))
            node.attrib.pop('W6')
            if not 'wm' in node.attrib:
                node.set('wm', '0')

    def hausregeln4zu5(datenbank, root):
        remove = []
        for node in root.findall('FreieFertigkeit'):
            if not 'name' in node.attrib:
                if node.text is None:
                    remove.append(node)
                else:
                    node.set('name', node.text)
                    node.text = ""
        for r in remove:
            root.remove(node)

    def hausregeln5zu6(datenbank, root):
        for node in root.findall('Manöver'):
            if 'gegenprobe' in node.attrib and node.attrib['gegenprobe']:
                node.text = "<i>Gegenprobe:</i> " + node.attrib['gegenprobe'] + (("\n" + node.text) if node.text else "")
            node.tag = "Regel"

        for node in root.findall('Remove'):
            if node.attrib['typ'] == "Manöver / Modifikation":
                node.attrib['typ'] = "Regel"
            elif node.attrib['typ'] == "Fertigkeit":
                node.attrib['typ'] = "Fertigkeit (profan)"
            elif node.attrib['typ'] == "Übernatürliche Fertigkeit":
                node.attrib['typ'] = "Fertigkeit (übernatürlich)"

            if node.attrib['name'] == "Regelanhang: Manöver Mergescript":
                node.attrib['name'] = "Regelanhang: Regel Mergescript"
            elif node.attrib['name'] == "Manöver: Typen":
                node.attrib['name'] = "Regeln: Typen"

        for node in root.findall('Einstellung'):
            if node.attrib['name'] == "Regelanhang: Manöver Mergescript":
                node.attrib['name'] = "Regelanhang: Regel Mergescript"
            elif node.attrib['name'] == "Manöver: Typen":
                node.attrib['name'] = "Regeln: Typen"
            elif node.attrib['name'] == "Regelanhang: Reihenfolge":
                if node.text:
                    node.text = node.text.replace("M", "R:")
                    node.text = node.text.replace("V", "V:")

        for node in root.findall('Talent'):
            if not node.text:
                continue
            bold = ["Mächtige Magie:", "Mächtige Liturgie:", "Mächtige Anrufung:", "Probenschwierigkeit:", "Modifikationen:", "Vorbereitungszeit:",
                    "Ziel:", "Reichweite:", "Wirkungsdauer:", "Kosten:", "Fertigkeiten:", "Erlernen:", "Anmerkung:", "Sephrasto:", "Fertigkeit Eis:",
                    "Fertigkeit Erz:", "Fertigkeit Feuer:", "Fertigkeit Humus:", "Fertigkeit Luft:", "Fertigkeit Wasser:"]
            boldPattern = re.compile("(?<!<b>)(" + "|".join(bold) + ")(?!</b>)")
            italic = ["Konterprobe", "Aufrechterhalten", "Ballistischer", "Ballistische", "Erfrieren", "Niederschmettern", "Nachbrennen", "Fesseln", "Zurückstoßen", "Ertränken", "Konzentration", "Objektritual", "Objektrituale"]
            italicPattern = re.compile("(?<!<i>)(" + "|".join(italic) + ")(?!</i>)")
            illusionPattern = re.compile("(?<!<i>)Illusion \((Sicht|Gehör|Geruch|Geschmack|Tast)")
            node.text = boldPattern.sub(lambda m: "<b>" + m.group(0) + "</b>", node.text)
            node.text = italicPattern.sub(lambda m: "<i>" + m.group(0) + "</i>", node.text)
            node.text = illusionPattern.sub(lambda m: m.group(0).replace("Illusion", "<i>Illusion</i>"), node.text)

        for node in root.findall('Regel'):
            if not node.text:
                continue
            italic = ["Gegenprobe:", "Wirkung:", "Voraussetzung:", "Voraussetzungen:", "Besonderheit:", "Besonderheiten:", "Anmerkung:", "Anmerkungen:",
                "Hohe Qualität:", "Probenschwierigkeit:", "Modifikationen:", "Dauer:", "Werkzeuge:", "Verbrauchsmaterialien:", "Haltbarkeit:",
                "Talent:", "Talente:", "Unterstützung:"]
            italicPattern = re.compile("(?<!<i>)(" + "|".join(italic) + ")(?!</i>)")
            node.text = italicPattern.sub(lambda m: "<i>" + m.group(0) + "</i>", node.text)

    #--------------------------------
    # Charakter Migrationsfunktionen
    #--------------------------------

    def charakter0zu1(charakter, xmlRoot):
        Kampfstile = ["Kein Kampfstil", "Beidhändiger Kampf", "Parierwaffenkampf", "Reiterkampf", 
              "Schildkampf", "Kraftvoller Kampf", "Schneller Kampf"]

        for waf in xmlRoot.findall('Objekte/Waffen/Waffe'):
            kampfstilIndex = int(waf.attrib['kampfstil'])
            waf.attrib['kampfstil'] = Kampfstile[kampfstilIndex]

        return "Datenbank Schema-Änderung (der selektierte Kampfstil bei Waffen wurde von indexbasiert zu stringbasiert geändert)"

    def charakter1zu2(charakter, xmlRoot):
        VorteileAlt = ["Angepasst I (Wasser)", "Angepasst I (Wald)", "Angepasst I (Dunkelheit)", "Angepasst I (Schnee)", "Angepasst II (Wasser)", "Angepasst II (Wald)", "Angepasst II (Dunkelheit)", "Angepasst II (Schnee)", "Tieremphatie"]
        VorteileNeu = ["Angepasst (Wasser) I", "Angepasst (Wald) I", "Angepasst (Dunkelheit) I", "Angepasst (Schnee) I", "Angepasst (Wasser) II", "Angepasst (Wald) II", "Angepasst (Dunkelheit) II", "Angepasst (Schnee) II", "Tierempathie"]

        for vort in xmlRoot.findall('Vorteile/Vorteil'):
            if vort.text in VorteileAlt:
                vort.text = VorteileNeu[VorteileAlt.index(vort.text)]

        return "Angepasst I (<Umgebung>) wurde in Angepasst (<Umgebung>) I umbenannt"

    def charakter2zu3(charakter, xmlRoot):
        stripped = ["Krähenruf ", "Ruhe Körper, Ruhe Geist ", "Auge des Limbus ", "Aerofugo Vakuum ", "Schutz des Dolches ", "Lied der Lieder ", 
                    "Nemekaths Geisterblick ", "Phexens Augenzwinkern ", "Daradors Bann der Schatten ", "Licht des Herrn ", "Harmonischer Rausch ", "Bund der Schwerter "]

        for node in xmlRoot.findall('.//Talent'):
            if node.get('name') in stripped:
                node.set('name', node.get('name').strip())
            if 'variable' in node.attrib:
                var = list(map(str.strip, node.attrib['variable'].split(",", 1)))
                if int(var[0]) != -1:
                    node.set('variableKosten', var[0])
                if len(var) > 1:
                    node.set('kommentar', var[1])
                node.attrib.pop('variable')

        for node in xmlRoot.findall('.//Vorteil'):
            if 'variable' in node.attrib:
                var = list(map(str.strip, node.attrib['variable'].split(",", 1)))
                if int(var[0]) != -1:
                    node.set('variableKosten', var[0])
                if len(var) > 1:
                    node.set('kommentar', var[1])
                node.attrib.pop('variable')

        alg = xmlRoot.find('AllgemeineInfos')
        alg.tag = "Beschreibung"
        alg.find('name').tag = 'Name'
        alg.find('rasse').tag = 'Spezies'
        alg.find('status').tag = 'Status'
        alg.find('kurzbeschreibung').tag = 'Kurzbeschreibung'
        alg.find('schips').tag = 'SchiP'
        alg.find('finanzen').tag = 'Finanzen'
        if alg.find('heimat') is None:
            etree.SubElement(alg, 'Heimat')
        else:
            alg.find('heimat').tag = "Heimat"
        alg.find('eigenheiten').tag = 'Eigenheiten'

        for fer in xmlRoot.findall('Fertigkeiten/Freie-Fertigkeit'):
            fer.tag = 'FreieFertigkeit'

        epn = xmlRoot.find('Erfahrung')
        epn.find('EPtotal').tag = "Gesamt"
        epn.find('EPspent').tag = "Ausgegeben"

        xmlRoot.find('Übernatürliche-Fertigkeiten').tag = 'ÜbernatürlicheFertigkeiten'
        for fer in xmlRoot.findall('ÜbernatürlicheFertigkeiten/Übernatürliche-Fertigkeit'):
            fer.tag = 'ÜbernatürlicheFertigkeit'
            if "addToPDF" in fer.attrib:
                fer.attrib["exportieren"] = "1" if fer.attrib["addToPDF"] == "True" else "0"
            else:
                fer.attrib["exportieren"] = "1"

        objekte = xmlRoot.find('Objekte');
        if objekte.find('Zonensystem') is None:
            etree.SubElement(objekte, 'Zonensystem').text = str(charakter.zonenSystemNutzen)

        for waf in objekte.findall('Waffen/Waffe'):
            waf.attrib["härte"] = waf.attrib["haerte"]
            waf.attrib.pop("haerte")
            waf.attrib["würfel"] = waf.attrib["W6"]
            waf.attrib.pop("W6")
            waf.attrib["würfelSeiten"] = "6"
            if not 'wm' in waf.attrib:
                waf.set('wm', "0")

        objekte.find('Zonensystem').text = "1" if objekte.find('Zonensystem').text == "True" else "0"

        if xmlRoot.find('Einstellungen') is None:
            einstellungen = etree.SubElement(xmlRoot, 'Einstellungen')
            etree.SubElement(einstellungen, 'VoraussetzungenPruefen').text = "1" if charakter.voraussetzungenPruefen else "0"
            etree.SubElement(einstellungen, 'Charakterbogen').text = str(charakter.charakterbogen)
            etree.SubElement(einstellungen, 'FinanzenAnzeigen').text = "1" if charakter.finanzenAnzeigen else "0"
            etree.SubElement(einstellungen, 'UeberPDFAnzeigen').text = "1" if charakter.ueberPDFAnzeigen else "0"
            etree.SubElement(einstellungen, 'RegelnAnhaengen').text = "1" if charakter.regelnAnhaengen else "0"
            etree.SubElement(einstellungen, 'RegelnGroesse').text = str(charakter.regelnGroesse)
            etree.SubElement(einstellungen, 'RegelnKategorien').text = str(", ".join(charakter.regelnKategorien))
            etree.SubElement(einstellungen, 'FormularEditierbarkeit').text = str(charakter.formularEditierbarkeit)
            etree.SubElement(einstellungen, 'Hausregeln').text = str(charakter.hausregeln or "")

        einstellungen = xmlRoot.find('Einstellungen')
        if einstellungen.find('VoraussetzungenPruefen') is None:
            etree.SubElement(einstellungen, 'VoraussetzungenPrüfen').text = "1" if charakter.voraussetzungenPruefen else "0"
        else:
            einstellungen.find('VoraussetzungenPruefen').tag = 'VoraussetzungenPrüfen'
        einstellungen.find('UeberPDFAnzeigen').tag = 'ÜbernatürlichesPDFSpalteAnzeigen'
        einstellungen.find('RegelnAnhaengen').tag = 'RegelnAnhängen'
        einstellungen.find('RegelnGroesse').tag = 'RegelnGrösse'
        if einstellungen.find('FormularEditierbarkeit') is None:
            etree.SubElement(einstellungen, 'FormularEditierbarkeit').text = str(charakter.formularEditierbarkeit)
        if einstellungen.find('RegelnKategorien') is None:
                etree.SubElement(einstellungen, 'RegelnKategorien').text = str(", ".join(charakter.regelnKategorien))

        if xmlRoot.find('Notiz') is None:
            etree.SubElement(xmlRoot, 'Notiz')

        if xmlRoot.find('AllgemeineInfosExt') is None:
            sub = etree.SubElement(xmlRoot, 'AllgemeineInfosExt')
            etree.SubElement(sub, 'kultur')
            etree.SubElement(sub, 'profession')
            etree.SubElement(sub, 'geschlecht')
            etree.SubElement(sub, 'geburtsdatum')
            etree.SubElement(sub, 'groesse')
            etree.SubElement(sub, 'gewicht')
            etree.SubElement(sub, 'haarfarbe')
            etree.SubElement(sub, 'augenfarbe')
            etree.SubElement(sub, 'titel')
            etree.SubElement(sub, 'aussehen1')
            etree.SubElement(sub, 'aussehen2')
            etree.SubElement(sub, 'aussehen3')
            etree.SubElement(sub, 'aussehen4')
            etree.SubElement(sub, 'aussehen5')
            etree.SubElement(sub, 'aussehen6')
            etree.SubElement(sub, 'hintergrund0')
            etree.SubElement(sub, 'hintergrund1')
            etree.SubElement(sub, 'hintergrund2')
            etree.SubElement(sub, 'hintergrund3')
            etree.SubElement(sub, 'hintergrund4')
            etree.SubElement(sub, 'hintergrund5')
            etree.SubElement(sub, 'hintergrund6')
            etree.SubElement(sub, 'hintergrund7')
            etree.SubElement(sub, 'hintergrund8')

        alg = xmlRoot.find('AllgemeineInfosExt')
        alg.tag = 'BeschreibungDetails'
        if alg.find('kultur') is None:
            etree.SubElement(alg, 'Kultur')
        else:
            alg.find('kultur').tag = "Kultur"

        alg.find('profession').tag = "Profession"
        alg.find('geschlecht').tag = "Geschlecht"
        alg.find('geburtsdatum').tag = "Geburtsdatum"
        alg.find('groesse').tag = "Grösse"
        alg.find('gewicht').tag = "Gewicht"
        alg.find('haarfarbe').tag = "Haarfarbe"
        alg.find('augenfarbe').tag = "Augenfarbe"
        alg.find('titel').tag = "Titel"

        alg.find('aussehen1').tag = "Aussehen1"
        alg.find('aussehen2').tag = "Aussehen2"
        alg.find('aussehen3').tag = "Aussehen3"
        alg.find('aussehen4').tag = "Aussehen4"
        alg.find('aussehen5').tag = "Aussehen5"
        alg.find('aussehen6').tag = "Aussehen6"

        alg.find('hintergrund0').tag = "Hintergrund0"
        alg.find('hintergrund1').tag = "Hintergrund1"
        alg.find('hintergrund2').tag = "Hintergrund2"
        alg.find('hintergrund3').tag = "Hintergrund3"
        alg.find('hintergrund4').tag = "Hintergrund4"
        alg.find('hintergrund5').tag = "Hintergrund5"
        alg.find('hintergrund6').tag = "Hintergrund6"
        alg.find('hintergrund7').tag = "Hintergrund7"
        alg.find('hintergrund8').tag = "Hintergrund8"

        if alg.find('bild') is not None:
            alg.find('bild').tag = "Bild"

        return None

    def charakter3zu4(charakter, xmlRoot):
        einstellungen = xmlRoot.find('Einstellungen')
        editierbar = einstellungen.find('FormularEditierbarkeit').text != "2"
        einstellungen.find('FormularEditierbarkeit').text = "1" if editierbar else "0"
        groesse = int(einstellungen.find('RegelnGrösse').text)
        if groesse == 0:
            einstellungen.find('RegelnGrösse').text = "8"
        elif groesse == 1:
            einstellungen.find('RegelnGrösse').text = "10"
        elif groesse == 2:
            einstellungen.find('RegelnGrösse').text = "12"
        einstellungen.find('RegelnKategorien').text = str(",".join(charakter.regelnKategorien))