import lxml.etree as etree
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException, WaffeneigenschaftException
import os.path
from PySide6 import QtWidgets
from Wolke import Wolke
import logging
from EventBus import EventBus
import re
from Core.Fertigkeit import FertigkeitDefinition

# ACHTUNG: Existierenden Migrationscode nur ändern wenn du 100% weißt, was du tust!
# Migrationscode verändert die xml nodes von Charakter- oder Hausregeldateien, bevor sie eingelesen werden.
# Es kann dabei verlockend sein, auf den aktuellen Charakter oder die aktuelle Datenbank zuzugreifen, aber das ist sehr fehleranfällig!
# Deren Struktur ist in Zukunft eventuell nicht mehr rückwirkend mit einer alten Migration kompatibel.
# Die Versionsnummer aus der Datei wird verglichen mit der Versionsnummer aus dem code, dann wird (beginnend bei der Dateiversion) jede Migrationsfunktion ausgeführt, bis die Codeversion erreicht ist
# Bei Charaktermigrationen immer darauf achten, dass Datenbankelemente via Hausregeln editiert worden sein können (siehe Datenbank::isHausregel())
# Je nach Situation sollte eine Migration dann nicht ausgeführt werden.
# Die Charakter-Migrationsfunktionen können einen string zurückgeben, der erklärt was geändert wurde - dies wird dem Nutzer in einer Messagebox angezeigt.

# Beispielmigration:
# if not 'Handgemenge' in Wolke.DB.fertigkeiten or not Wolke.DB.isChangedOrNew(Wolke.DB.fertigkeiten['Handgemenge']):
#     for fer in xmlRoot.findall('Fertigkeiten/Fertigkeit'):
#         if fer.attrib['name'] == 'Handgemenge':
#             fer.attrib['name'] = 'Raufen'
#             return "Handgemenge wurde in Raufen umbenannt"
# return None
class Migrationen():
    def __init__(self):
        pass

    datenbankCodeVersion = 7
    charakterCodeVersion = 5

    def hausregelnMigrieren(xmlRoot, hausregelnVersion):
        migrationen = [
            lambda xmlRoot: None, #nichts zu tun, initiale db version
            Migrationen.hausregeln0zu1,    
            Migrationen.hausregeln1zu2,
            Migrationen.hausregeln2zu3,
            Migrationen.hausregeln3zu4,
            Migrationen.hausregeln4zu5,
            Migrationen.hausregeln5zu6,
            Migrationen.hausregeln6zu7,
        ]

        if not migrationen[Migrationen.datenbankCodeVersion]:
            raise Exception("Migrations-Code vergessen.")

        updates = []
        while hausregelnVersion < Migrationen.datenbankCodeVersion:
            logging.warning("Migriere Hausregeln von Version " + str(hausregelnVersion ) + " zu " + str(hausregelnVersion + 1))
            hausregelnVersion +=1
            update = migrationen[hausregelnVersion](xmlRoot)
            if update:
                updates.append(update)
        return updates

    def charakterMigrieren(xmlRoot):
        # Die Versionsdaten müssen immer migriert werden.
        versionXml = xmlRoot.find('Version')
        if versionXml is None:
            versionXml = etree.SubElement(xmlRoot, 'Version')
            etree.SubElement(versionXml, 'CharakterVersion').text = "0"
            etree.SubElement(versionXml, 'Plugins').text = ""
            etree.SubElement(versionXml, 'Hausregeln').text = ""
        else:
            if versionXml.find('DatenbankVersion') is not None:
                versionXml.find('DatenbankVersion').tag = 'CharakterVersion'
            if versionXml.find('Plugins') is None:
                etree.SubElement(versionXml, 'Plugins').text = ""
            if versionXml.find('NutzerDatenbankName') is not None:
                versionXml.find('NutzerDatenbankName').tag = "Hausregeln"

        charakterVersion = int(versionXml.find('CharakterVersion').text)

        migrationen = [
            lambda xmlRoot: None, #nichts zu tun, initiale db version
            Migrationen.charakter0zu1, 
            Migrationen.charakter1zu2, 
            Migrationen.charakter2zu3,
            Migrationen.charakter3zu4,
            Migrationen.charakter4zu5,
        ]

        if not migrationen[Migrationen.charakterCodeVersion]:
            raise Exception("Migrations-Code vergessen.")

        updates = []
        while charakterVersion < Migrationen.charakterCodeVersion:
            logging.warning("Migriere Charakter von Version " + str(charakterVersion) + " zu " + str(charakterVersion + 1))
            charakterVersion +=1
            update = migrationen[charakterVersion](xmlRoot)
            if update:
                updates.append(update)

        return updates

    #--------------------------------
    # Hausregeln Migrationsfunktionen
    #--------------------------------

    def hausregeln0zu1(root):
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
        return None

    def hausregeln1zu2(root):
        # removed this migration, it accessed the database for a convenience conversion - bad idea
        return None

    def hausregeln2zu3(root):
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
        return None

    def hausregeln3zu4(root):
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
        return None

    def hausregeln4zu5(root):
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
        return None

    def hausregeln5zu6(root):
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
                    "Ziel:", "Reichweite:", "Wirkungsdauer:", "Kosten:", "Fertigkeiten:", "Erlernen:", "Anmerkung:", "Fertigkeit Eis:",
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

        return "- Das Feld Gegenprobe wurde bei Regeln entfernt und der vorige Inhalt am Anfang der Beschreibung eingefügt.\n"\
               "- Bei Talenten und Regeln wurden HTML-Tags in die Beschreibung eingefügt."

    def hausregeln6zu7(root):
        # Use actual type names in remove tags instead of display names
        for node in root.findall('Remove'):
            if node.attrib['typ'] == "Fertigkeit (profan)":
                node.attrib['typ'] = "FertigkeitDefinition"
            elif node.attrib['typ'] == "Fertigkeit (übernatürlich)":
                node.attrib['typ'] = "UeberFertigkeitDefinition"
            elif node.attrib['typ'] == "Freie Fertigkeit":
                node.attrib['typ'] = "FreieFertigkeitDefinition"
            elif node.attrib['typ'] == "Einstellung":
                node.attrib['typ'] = "DatenbankEinstellung"
            elif node.attrib['typ'] == "Rüstung":
                node.attrib['typ'] = "RuestungDefinition"
            elif node.attrib['typ'] == "Talent":
                node.attrib['typ'] = "TalentDefinition"
            elif node.attrib['typ'] == "Vorteil":
                node.attrib['typ'] = "VorteilDefinition"
            elif node.attrib['typ'] == "Waffe":
                node.attrib['typ'] = "WaffeDefinition"
        # Querverweise were added as a new feature. These are the vanilla db values for it at version 7.
        # Lets apply them to houserules for convenience
        querverweise = {
            "Achaz" : "Regel:Nahkampfmodifikatoren", "Angepasst (Schnee) I" : "Regel:Nahkampfmodifikatoren", "Angepasst (Dunkelheit) I" : "Regel:Nahkampfmodifikatoren|Regel:Fernkampfmodifikatoren",
            "Angepasst (Wasser) I" : "Regel:Nahkampfmodifikatoren", "Angepasst (Wald) I" : "Regel:Nahkampfmodifikatoren", "Angepasst I" : "Regel:Nahkampfmodifikatoren",
            "Angepasst II" : "Regel:Nahkampfmodifikatoren", "Angepasst (Dunkelheit) II" : "Regel:Nahkampfmodifikatoren|Regel:Fernkampfmodifikatoren",
            "Angepasst (Schnee) II" : "Regel:Nahkampfmodifikatoren", "Angepasst (Wald) II" : "Regel:Nahkampfmodifikatoren", "Angepasst (Wasser) II" : "Regel:Nahkampfmodifikatoren",
            "Einkommen I" : "Statusse", "Einkommen II" : "Statusse", "Einkommen III" : "Statusse", "Einkommen IV" : "Statusse", "Eisenaffine Aura" : "Regel:Bann des Eisens",
            "Gefahreninstinkt" : "Talent:Wachsamkeit", "Glück I" : "Regel:Schicksalspunkte", "Glück II" : "Regel:Schicksalspunkte", "Kreis der Verdammnis I" : "Talent:Seelenprüfung|Talent:Willenskraft",
            "Kreis der Verdammnis II" : "Talent:Seelenprüfung|Talent:Willenskraft", "Kreis der Verdammnis III" : "Talent:Seelenprüfung|Talent:Willenskraft",
            "Kreis der Verdammnis IV" : "Talent:Seelenprüfung|Talent:Willenskraft", "Kreis der Verdammnis V" : "Talent:Seelenprüfung|Talent:Willenskraft",
            "Kreis der Verdammnis VI" : "Talent:Seelenprüfung|Talent:Willenskraft", "Kreis der Verdammnis VII" : "Talent:Seelenprüfung|Talent:Willenskraft",
            "Magieabweisend" : "Regel:Mächtige Magie", "Magiegespür" : "Talent:Sinnenschärfe", "Prophezeien" : "Talent:Willenskraft", "Resistenz gegen Gifte" : "Regel:Gifte & Krankheiten mildern",
            "Resistenz gegen Krankheiten" : "Regel:Gifte & Krankheiten mildern", "Verbindungen" : "Regel:Informationen suchen", "Zwergennase" : "Talent:Wachsamkeit", "Eindrucksvoll I" : "Regel:Rededuell|Talent:Betören|Talent:Einschüchtern",
            "Eindrucksvoll II" : "Regel:Rededuell|Talent:Betören|Talent:Einschüchtern", "Soziale Anpassungsfähigkeit" : "Regel:Rededuell", "Starke Aura" : "Regel:Rededuell|Talent:Willenskraft",
            "Zerstörerisch II" : "Regel:Hammerschlag", "Muskelprotz" : "Regel:Einschüchtern & Furcht", "Flink I" : "Abgeleiteter Wert:GS", "Flink II" : "Abgeleiteter Wert:GS",
            "Katzenhaft" : "Regel:Nahkampfmodifikatoren|Abgeleiteter Wert:WS", "Körperbeherrschung" : "Regel:Nahkampf", "Scharfsinnig I" : "Regel:Informationen suchen", "Scharfsinnig II" : "Regel:Informationen suchen",
            "Vorausschauend I" : "Regel:Rededuell|Talent:Rhetorik|Talent:Überreden", "Vorausschauend II" : "Regel:Rededuell|Talent:Rhetorik|Talent:Überreden", "Bedächtig" : "Regel:Rededuell", "Empathie" : "Talent:Willenskraft",
            "Abgehärtet II" : "Abgeleiteter Wert:DH", "Schnelle Heilung" : "Regel:Regeneration", "Unverwüstlich" : "Abgeleiteter Wert:WS|Talent:Zähigkeit|Regel:Kampfunfähigkeit", "Willensstark I" : "Abgeleiteter Wert:MR",
            "Willensstark II" : "Abgeleiteter Wert:MR|Regel:Einschüchtern & Furcht", "Geisterpanzer" : "Abgeleiteter Wert:WS", "Unbeugsamkeit" : "Abgeleiteter Wert:MR|Regel:Aktion Konflikt (einfach)|Regel:Eigenschaft Konterprobe (M)",
            "Kommando: Haltet Stand!" : "Regel:Kommandos|Regel:Einschüchtern & Furcht", "Kommando: Formiert Euch!" : "Regel:Kommandos", "Kommando: Keine Gefangenen!" : "Regel:Kommandos",
            "Kommando: Kennt Keinen Schmerz!" : "Regel:Kommandos|Abgeleiteter Wert:WS", "Ruhige Hand" : "Regel:Zielen", "Reflexschuss" : "Regel:Fernkampfmodifikatoren",
            "Schnellziehen" : "Regel:Schnellschuss|Regel:Aktion Bereit machen (einfach)", "Meisterschuss" : "Regel:Meisterschuss", "Niederwerfen" : "Regel:Niederwerfen",
            "Waffenloser Kampf" : "Waffeneigenschaft:Kopflastig|Waffeneigenschaft:Wendig", "Hammerschlag" : "Regel:Hammerschlag", "Unaufhaltsam" : "Regel:Ausweichen",
            "Standfest" : "Regel:Nahkampfmodifikatoren", "Sturmangriff" : "Regel:Sturmangriff", "Todesstoß" : "Regel:Todesstoß", "Ausfall" : "Regel:Ausfall",
            "Offensiver Kampfstil" : "Regel:Aktion Volle Offensive (voll)", "Gegenhalten" : "Regel:Reaktion", "Kampfreflexe" : "Abgeleiteter Wert:INI",
            "Defensiver Kampfstil" : "Regel:Aktion Volle Defensive (voll)", "Aufmerksamkeit" : "Regel:Reaktion|Regel:Freie Reaktion", "Klingentanz" : "Regel:Klingentanz",
            "Durchatmen" : "Regel:Aktion Konzentration (voll)|Talent:Zähigkeit", "Rüstungsgewöhnung" : "Abgeleiteter Wert:BE", "Atemtechnik" : "Regel:Freie Aktion",
            "Verbesserte Rüstungsgewöhnung" : "Abgeleiteter Wert:BE", "Beidhändiger Kampf II" : "Regel:Nahkampfmodifikatoren|Regel:Reaktion|Regel:Freie Reaktion",
            "Beidhändiger Kampf III" : "Regel:Doppelangriff", "Kraftvoller Kampf II" : "Regel:Nahkampfmodifikatoren|Regel:Freie Aktion", "Kraftvoller Kampf III" : "Regel:Befreiungsschlag",
            "Schildkampf II" : "Regel:Nahkampfmodifikatoren|Regel:Freie Reaktion", "Schildkampf III" : "Regel:Schildwall", "Schneller Kampf II" : "Regel:Nahkampfmodifikatoren|Regel:Freie Aktion",
            "Schneller Kampf III" : "Regel:Unterlaufen", "Parierwaffenkampf II" : "Regel:Nahkampfmodifikatoren",
            "Parierwaffenkampf III" : "Regel:Riposte", "Reiterkampf I" : "Regel:Sturmangriff|Waffeneigenschaft:Reittier", "Reiterkampf II" : "Regel:Nahkampfmodifikatoren|Waffeneigenschaft:Reittier|Regel:Fernkampfmodifikatoren",
            "Reiterkampf III" : "Regel:Überrennen|Waffeneigenschaft:Reittier", "Bändiger der Elemente" : "Regel:Beschwörungen|Regel:Beschwörungen - Elementare|Regel:Beschwörungen - Golems",
            "Meister der Wünsche" : "Regel:Beschwörungen|Regel:Beschwörungen - Elementare|Regel:Beschwörungen - Golems",
            "Gebieter der Urgewalten" : "Regel:Beschwörungen|Regel:Beschwörungen - Bindung|Regel:Beschwörungen - Elementare|Regel:Beschwörungen - Golems",
            "Reaktivierung" : "Regel:Artefaktherstellung", "Matrixverständnis" : "Regel:Artefaktherstellung",
            "Semipermanenz" : "Regel:Artefaktherstellung", "Thaumaturg" : "Regel:Artefaktherstellung|Vorteil:Meister der Wünsche|Vorteil:Meister der Seelenlosen",
            "Astrale Regeneration" : "Regel:Regeneration", "Verbotene Pforten" : "Vorteil:Tradition der Borbaradianer I|Abgeleiteter Wert:WS",
            "Verbesserte astrale Regeneration" : "Regel:Regeneration", "Meisterliche astrale Regeneration" : "Regel:Regeneration",
            "Bändiger der Kreaturen" : "Regel:Beschwörungen|Regel:Beschwörungen - Zusätzliche Fähigkeiten|Regel:Beschwörungen - Dämonen|Regel:Beschwörungen - Untote|Regel:Beschwörungen - Chimären|Regel:Beschwörungen - Golems",
            "Meister der Seelenlosen" : "Regel:Beschwörungen|Regel:Beschwörungen - Bindung|Regel:Beschwörungen - Dämonen|Regel:Beschwörungen - Untote|Regel:Beschwörungen - Chimären|Regel:Beschwörungen - Golems",
            "Blutmagie" : "Abgeleiteter Wert:WS|Regel:Beschwörungen - Dämonen|Regel:Beschwörungen - Elementare",
            "Gebieter der Finsternis" : "Regel:Beschwörungen|Regel:Beschwörungen - Bindung|Regel:Beschwörungen - Dämonen|Regel:Beschwörungen - Untote|Regel:Beschwörungen - Chimären|Regel:Beschwörungen - Golems",
            "Unitatio" : "Regel:Zusammenarbeit", "Flexible Magie" : "Regel:Aktion Konzentration (voll)", "Mühelose Magie" : "Regel:Mächtige Magie", "Flinke Magie" : "Regel:Aktion Konflikt (einfach)|Regel:Freie Aktion",
            "Kraftlinienmagie" : "Regel:Regeneration", "Effizientes Zaubern" : "Regel:Kosten sparen (M)", "Vorbereitendes Zaubern" : "Regel:Aktion Konzentration (voll)|Regel:Aktion Konflikt (einfach)",
            "Tiergeist (Affe)" : "Talent:Attributo|Talent:Axxeleratus Blitzgeschwind|Talent:Motoricus Geisterhand|Talent:Wipfellauf",
            "Tiergeist (Bär)" : "Talent:Bärenruhe Winterschlaf|Talent:Eiseskälte Kämpferherz|Talent:Ruhe Körper, Ruhe Geist|Talent:Sanftmut|Talent:Standfest Katzengleich|Talent:Zaubernahrung Hungerbann",
            "Tiergeist (Elefant)" : "Talent:Memorans Gedächtniskraft|Talent:Psychostabilis|Talent:Seelentier erkennen|Talent:Xenographus Schriftenkunde",
            "Tiergeist (Eule)" : "Talent:Blick aufs Wesen|Talent:Exposami Lebenskraft|Talent:Hexenkrallen|Talent:Sensibar Empathicus|Talent:Silentium Schweigekreis",
            "Tiergeist (Falke)" : "Talent:Adlerauge Luchsenohr|Talent:Axxeleratus Blitzgeschwind|Talent:Falkenauge Meisterschuss|Talent:Pfeil der Luft|Talent:Aeropulvis sanfter Fall",
            "Tiergeist (Fischotter)" : "Talent:Eins mit der Natur|Talent:Katzenaugen|Talent:Foramen Foraminor|Talent:Wasseratem|Talent:Wellenlauf|Talent:Hilfreiche Tatze, rettende Schwinge",
            "Tiergeist (Fuchs)" : "Talent:Attributo|Talent:Harmlose Gestalt|Talent:Sensibar Empathicus|Talent:Seidenzunge Elfenwort",
            "Tiergeist (Mungo)" : "Talent:Attributo|Talent:Harmlose Gestalt|Talent:Sensibar Empathicus|Talent:Seidenzunge Elfenwort",
            "Tiergeist (Gebirgsbock)" : "Talent:Axxeleratus Blitzgeschwind|Talent:Eins mit der Natur|Talent:Firnlauf|Talent:Spinnenlauf|Talent:Standfest Katzengleich",
            "Tiergeist (Löwe)" : "Talent:Ängste lindern|Talent:Armatrutz|Talent:Katzenaugen|Talent:Kusch!|Talent:Standfest Katzengleich",
            "Tiergeist (Mammut)" : "Talent:Ängste lindern|Talent:Armatrutz|Talent:Kusch!|Talent:Psychostabilis|Talent:Zaubernahrung Hungerbann",
            "Tiergeist (Rabe)" : "Talent:Krähenruf|Talent:Sensibar Empathicus|Talent:Nekropathia Seelenreise|Talent:Memorans Gedächtniskraft",
            "Tiergeist (Schlange)" : "Talent:Atemnot|Talent:Psychostabilis|Talent:Serpentialis Schlangenleib|Talent:Vipernblick|Talent:Warmes Blut",
            "Tiergeist (Stier)" : "Talent:Attributo|Talent:Horriphobus Schreckgestalt|Talent:Sensattaco Meisterstreich|Talent:Standfest Katzengleich",
            "Tiergeist (Wildkatze)" : "Talent:Eins mit der Natur|Talent:Katzenaugen|Talent:Krötensprung|Talent:Spurlos Trittlos|Talent:Standfest Katzengleich|Talent:Wipfellauf",
            "Tiergeist (Panther)" : "Talent:Eins mit der Natur|Talent:Katzenaugen|Talent:Krötensprung|Talent:Spurlos Trittlos|Talent:Standfest Katzengleich|Talent:Wipfellauf",
            "Tiergeist (Wildschwein)" : "Talent:Abvenenum reine Speise|Talent:Eins mit der Natur|Talent:Kusch!|Talent:Standfest Katzengleich|Talent:Zaubernahrung Hungerbann",
            "Tiergeist (Wolf)" : "Talent:Adlerauge Luchsenohr|Talent:Axxeleratus Blitzgeschwind|Talent:Eins mit der Natur|Talent:Kusch!|Talent:Movimento Dauerlauf|Talent:Spurlos Trittlos",
            "Tiergeist (Khoramsbestie)" : "Talent:Adlerauge Luchsenohr|Talent:Axxeleratus Blitzgeschwind|Talent:Eins mit der Natur|Talent:Kusch!|Talent:Movimento Dauerlauf|Spurlos",
            "Tradition der Alchemisten III" : "Regel:Zeit lassen", "Tradition der Borbaradianer I" : "Regel:Verbotene Pforten|Vorteil:Minderpakt",
            "Tradition der Borbaradianer III" : "Regel:Erzwingen", "Tradition der Geoden III" : "Regel:Zeit lassen", "Tradition der Gildenmagier III" : "Regel:Zeit lassen", 
            "Tradition der Druiden III" : "Regel:Erzwingen", "Tradition der Elfen III" : "Regel:Zeit lassen",
            "Tradition der Hexen III" : "Regel:Erzwingen", "Tradition der Kristallomanten I" : "Regel:Vorbereitung verkürzen (M)",
            "Tradition der Kristallomanten III" : "Regel:Zeit lassen", "Tradition der Schelme III" : "Regel:Erzwingen",
            "Tradition der Scharlatane III" : "Regel:Zeit lassen", "Tradition der Anach-Nurim I" : "Regel:Verbotene Pforten|Vorteil:Blutmagie", "Tradition der Anach-Nurim II" : "Regel:Verbotene Pforten|Vorteil:Blutmagie",
            "Tradition der Anach-Nurim III" : "Regel:Erzwingen", "Tradition der Derwische III" : "Regel:Opferung (Derwische)",
            "Tradition der Durro-dun III" : "Regel:Opferung (Durro-dûn)", "Tradition der Schamanen III" : "Regel:Zeremonie (M)", "Tradition der Zauberbarden II" : "Regel:Eigenschaft Konzentration (M)",
            "Tradition der Zauberbarden III" : "Regel:Zeit lassen", "Tradition der Zaubertänzer III" : "Regel:Opferung (Zaubertänzer)",
            "Unterstützung der Gläubigen" : "Regel:Mirakel", "Gemeinsames Wunder" : "Regel:Zusammenarbeit",
            "Zuverlässiges Wunder" : "Regel:Mirakel", "Beeindruckendes Wunder" : "Regel:Mirakel|Regel:Mächtige Liturgie", "Göttliche Nähe" : "Regel:Regeneration",
            "Liturgische Disziplin" : "Regel:Kosten sparen (L)", "Liebling der Gottheit" : "Regel:Mächtige Liturgie", "Stärke des Glaubens" : "Abgeleiteter Wert:WS",
            "Tradition der Avesgeweihten II" : "Regel:Aktion Konzentration (voll)|Regel:Aktion Bewegung (einfach)", "Tradition der Avesgeweihten III" : "Regel:Opferung (Aves)",
            "Tradition der Borongeweihten III" : "Regel:Zeremonie (L)", "Tradition der Efferdgeweihten III" : "Regel:Opferung (Efferd)",
            "Tradition der Firungeweihten III" : "Regel:Opferung (Firun)", "Tradition der Hesindegeweihten III" : "Regel:Zeremonie (L)",
            "Tradition der Ifirngeweihten III" : "Regel:Zeremonie (L)", "Tradition der Ingerimmgeweihten III" : "Regel:Opferung (Ingerimm)",
            "Tradition der Angroschgeweihten III" : "Regel:Opferung (Angrosch)", "Tradition der Korgeweihten II" : "Vorteil:Kalte Wut",
            "Tradition der Korgeweihten III" : "Regel:Opferung (Kor)", "Tradition der Nandusgeweihten II" : "Regel:Liturgische Technik ignorieren",
            "Tradition der Nandusgeweihten III" : "Regel:Opferung (Nandus)", "Tradition der Perainegeweihten II" : "Regel:Mehrere Ziele (L)",
            "Tradition der Perainegeweihten III" : "Regel:Zeremonie (L)", "Tradition der Phexgeweihten III" : "Regel:Opferung (Phex)",
            "Tradition der Praiosgeweihten III" : "Regel:Zeremonie (L)", "Tradition der Rahjageweihten III" : "Regel:Opferung (Rahja)", "Tradition der Rondrageweihten II" : "Vorteil:Kalte Wut",
            "Tradition der Rondrageweihten III" : "Regel:Opferung (Rondra)", "Tradition der Swafnirgeweihten III" : "Regel:Opferung (Swafnir)",
            "Tradition der Traviageweihten II" : "Regel:Wirkungsdauer verlängern (L)", "Tradition der Traviageweihten III" : "Regel:Zeremonie (L)",
            "Tradition der Tsageweihten II" : "Regel:Vorbereitung verkürzen (L)", "Tradition der Tsageweihten III" : "Regel:Zeremonie (L)",
            "Tradition der Paktierer II" : "Regel:Mächtige Anrufung", "Tradition der Paktierer III" : "Regel:Opferung (Paktierer)"
        }

        # we want to replace dashes by minus if followed by a number, also some Tiergeister were renamed
        dashPattern = re.compile("–(\d)")
        for elementType in ["Vorteil", "Talent", "Fertigkeit", "ÜbernatürlicheFertigkeit", "Waffeneigenschaft", "Rüstung", "Regel"]:
            for node in root.findall(elementType):
                if "voraussetzungen" in node.attrib:
                    node.attrib["voraussetzungen"] = node.attrib["voraussetzungen"].replace("Vorteil Tiergeist (Wolf/Khoramsbestie)", "Vorteil Tiergeist (Wolf) ODER Vorteil Tiergeist (Khoramsbestie)")
                    node.attrib["voraussetzungen"] = node.attrib["voraussetzungen"].replace("Vorteil Tiergeist (Wildkatze/Panther)", "Vorteil Tiergeist (Wildkatze) ODER Vorteil Tiergeist (Panther)")
                    node.attrib["voraussetzungen"] = node.attrib["voraussetzungen"].replace("Vorteil Tiergeist (Fuchs/Mungo)", "Vorteil Tiergeist (Fuchs) ODER Vorteil Tiergeist (Mungo)")
                if node.text is None:
                    continue
                node.text = dashPattern.sub(lambda m: "-" + m.group(1), node.text)

        for node in root.findall("Vorteil"):
            if "csBeschreibung" in node.attrib:
                node.attrib["csBeschreibung"] = dashPattern.sub(lambda m: "-" + m.group(1), node.attrib["csBeschreibung"])
        
            name = node.attrib["name"]
            if name in ["Paktierer I", "Paktierer II", "Paktierer III", "Paktierer IV"] and "script" in node.attrib:
                node.attrib["script"] = node.attrib["script"].replace("modifyKaPBasis", "modifyGuPBasis")

            if name.startswith("Tiergeist ("):
                node.attrib["voraussetzungen"] = "Vorteil Tradition der Anach-Nurim I ODER Vorteil Tradition der Durro-dun I ODER Vorteil Tradition der Schamanen I, Vorteil Tradition der Schamanen I ODER Kein Vorteil Tiergeist (*)"

            if name.startswith("Tradition der ") and name.endswith("geweihten I"):
                split = node.attrib["voraussetzungen"].split(",")
                attribut = None
                for v in split:
                    if v.startswith("Attribut"):
                        attribut = v + ", "
                node.attrib["voraussetzungen"] = (attribut if attribut else "") + "Vorteil Geweiht I, Kein Vorteil Tradition der *geweihten I"

            if name == "Scharfsinnig I" and "linkElement" not in node.attrib:
                node.attrib["linkKategorie"] = "1"
                node.attrib["linkElement"] = "Informationen suchen"

            if name in querverweise:
                node.set("querverweise", querverweise[name])

        for elementType in ["Vorteil", "Waffeneigenschaft"]:
            for node in root.findall(elementType):
                if "script" in node.attrib:
                    node.attrib["script"] = node.attrib["script"].replace("RSMod", "RS")
                    node.attrib["script"] = node.attrib["script"].replace("SchiPMax", "SchiP")
                    node.attrib["script"] = node.attrib["script"].replace("getBEMod", "getBE").replace("modifyBEMod(", "modifyBE(-").replace("setBEMod(", "setBE(-")
                    node.attrib["script"] = node.attrib["script"].replace("Schadensbonus", "SB")

        # Some weapons were renamed from x (Infanteriewaffen) to x (Infanteriewaffen und Speere)
        for node in root.findall('Remove'):
            if node.attrib['typ'] == "WaffeDefinition" and node.attrib['name'] in ["Dschadra (Infanteriewaffen)", "Efferdbart (Infanteriewaffen)", "Holzspeer (Infanteriewaffen)", "Speer (Infanteriewaffen)"]:
                node.attrib['name'] = node.attrib['name'][:-1] + " und Speere)"

        # Talents were updated to have a type that specifies Zauber/Liturgie/Anrufung
        # Migration is a bit nasty, because the detection was very implicit through the Fertigkeiten before
        # First we need to establish the database state of übernatürlicheFertigkeiten at this point in time
        # Then the Liturgie/Anrufung Typen setting which will be deleted in the next db version
        übernatürlicheFertigkeiten = {
            "Antimagie" : 0, "Dämonisch" : 0, "Eigenschaften" : 0, "Einfluss" : 0, "Eis" : 0, "Erz" : 0, "Feuer" : 0, "Hellsicht" : 0,
            "Humus" : 0, "Illusion" : 0, "Kraft" : 0, "Luft" : 0, "Temporal" : 0, "Umwelt" : 0, "Verständigung" : 0, "Verwandlung" : 0,
            "Wasser" : 0, "Dolchzauber" : 1, "Elfenlieder" : 1, "Gaben des Blutgeists" : 1, "Gaben des Odun" : 1, "Geister der Stärkung" : 1,
            "Geister des Zorns" : 1, "Geister rufen" : 1, "Geister vertreiben" : 1, "Hexenflüche" : 1, "Keulenrituale" : 1, "Kristallmagie" : 1,
            "Kugelzauber" : 1, "Ringrituale" : 1, "Schalenzauber" : 1, "Stabzauber" : 1, "Trommelrituale" : 1, "Vertrautenmagie" : 1,
            "Zaubermelodien" : 1, "Zaubertänze" : 1, "Zwölfgöttlicher Ritus" : 2, "Schlaf" : 3, "Tod" : 3, "Vergessen" : 3, "Flüsse und Quellen" : 3,
            "Seefahrt" : 3, "Wind und Wogen" : 3, "Jagd" : 3, "Wildnis" : 3, "Winter" : 3, "Magie" : 3, "Wissen" : 3, "Heiliges Erz" : 3,
            "Heiliges Feuer" : 3, "Heiliges Handwerk" : 3, "Heilung" : 3, "Wachstum" : 3, "Abu al'Mada" : 3, "List" : 3, "Nächtlicher Schatten" : 3,
            "Licht" : 3, "Magiebann" : 3, "Ordnung" : 3, "Harmonie" : 3, "Rausch" : 3, "Ehre" : 3, "Heerführung" : 3, "Schutz der Gläubigen" : 3,
            "Heim und Herd" : 3, "Sichere Heimkehr" : 3, "Friede" : 3, "Neubeginn" : 3, "Fröhlicher Wanderer" : 3, "Stiller Wanderer" : 3,
            "Guter Kampf" : 3, "Gutes Gold" : 3, "Dämonische Hilfe (Cpt)" : 4
        }

        talenteGruppieren = ["Dolchzauber", "Elfenlieder", "Gaben des Blutgeists", "Gaben des Odun", "Geister der Stärkung",
                            "Geister des Zorns", "Geister rufen", "Geister vertreiben", "Hexenflüche", "Keulenrituale", "Kristallmagie",
                            "Kugelzauber", "Ringrituale", "Schalenzauber", "Stabzauber", "Trommelrituale", "Vertrautenmagie", "Zaubermelodien",
                            "Zaubertänze", "Zwölfgöttlicher Ritus"]

        for fer in root.findall('ÜbernatürlicheFertigkeit'):
            übernatürlicheFertigkeiten[fer.get('name')] = int(fer.get('typ'))
            if fer.get('talentegruppieren') == 1:
                if not fer.get('name') in talenteGruppieren:
                    talenteGruppieren.append(fer.get('name'))
            elif fer.get('name') in talenteGruppieren:
                talenteGruppieren.remove(fer.get('name'))

        liturgieTypen = [2, 3]
        anrufungTypen = [4]
        for ein in root.findall('Einstellung'):
            if ein.get('name') == "Fertigkeiten: Liturgie-Typen":
                liturgieTypen = [int(t.strip()) for t in ein.text.split(",")]
            elif ein.get('name') == "Fertigkeiten: Anrufungs-Typen":
                anrufungTypen = [int(t.strip()) for t in ein.text.split(",")]

        for node in root.findall('Talent'):
            if int(node.get("kosten")) == -1:
                continue

            ferts = []
            for fert in Hilfsmethoden.FertStr2Array(node.get('fertigkeiten'), None):
                if fert in übernatürlicheFertigkeiten:
                    ferts.append(fert)
            hauptfertigkeit = None
            for fert in ferts:
                if hauptfertigkeit is None:
                    hauptfertigkeit = fert
                elif not hauptfertigkeit in talenteGruppieren and fert in talenteGruppieren:
                    hauptfertigkeit = fert

            if hauptfertigkeit is not None:
                if übernatürlicheFertigkeiten[hauptfertigkeit] in liturgieTypen:
                    node.set('spezialTyp', "1")
                elif übernatürlicheFertigkeiten[hauptfertigkeit] in anrufungTypen:
                    node.set('spezialTyp', "2")
                else:
                    node.set('spezialTyp', "0")
            else:
                node.set('spezialTyp', "0")

        # Fill the new info field
        waffenmeisterschaft = "Für je einen Punkt kannst du die fixe Erschwernis eines Manöver um einen Punkt senken (bis maximal auf die Hälfte), für 4 Punkte die AT oder VT um einen Punkt erhöhen oder für bis zu 4 Punkte ein passendes, neues Manöver erfinden. "\
                              "Besondere Vorteile wie eine geringere Patzerchance, höhere Reichweite oder Schaden sind ebenfalls möglich. Solche Vorteile – wie der Waffenmeister ganz allgemein – und ihre Kosten sollten unbedingt mit der Gruppe und dem Spielleiter abgesprochen werden. Trage die Verbesserungen in das Kommentarfeld ein."
        tiergeist = "Die Verbindung mit einem Tiergeist wird in Sephrasto als kostenloser Vorteil abgebildet. Schamanen können mehrere Tiergeister wählen. "\
                    "Durro-dûn müssen sich für ein Tier entscheiden und können dann die Zauber des Tiergeists unter der Fertigkeit Gaben des Odun erlernen. Anach-nûrim können das Tier wechseln, indem sie einen neuen Blutgeist aufnehmen und dann alle Zauber des Tiergeists unter der Fertigkeit Gaben des Blutgeists aktivieren."
        meisterschaftM = "Für 1 Punkt kann ein Zauber um +2 erleichtert werden (maximal +4). Für 2 Punkte kannst du eine spontane Modifikation außer Mächtige Magie um +1 erleichtern (maximal +1). Spezielle Vorteile wie eine geringere Patzerchance oder länger nachbrennende Feuerzauber sind ebenfalls möglich. "\
                         "Solche Verbesserungen (und ihre Kosten) sollten mit dem Spielleiter und der Gruppe abgesprochen werden. Trage die Verbesserungen in das Kommentarfeld ein."
        meisterschaftL = "Mit einem Punkt kannst du eine Liturgie um +2 erleichtern (maximal +4) oder eine spontane Modifikation, außer Mächtige Liturgie, um +1 erleichtern (maximal +1). "\
                         "Weitere Vorteile wie ein Schutzsegen mit größerem Wirkungsbereich sind ebenfalls möglich, sollten (mitsamt ihren Kosten) aber mit dem Spielleiter und der Gruppe abgesprochen werden. Trage die Verbesserungen in das Kommentarfeld ein."
        infos = { "Angepasst I" : "Wähle am besten direkt den separaten Vorteil Angepasst (Dunkelheit, Schnee, Wasser oder Wald) I. Falls du eine andere Umgebung möchtest, dann wähle diesen Vorteil und trage diese in das Kommentarfeld ein.",
                 "Angepasst II" : "Trage die gewählte Umgebung in das Kommentarfeld ein. Entferne diese Umgebung aus dem Kommentar von Angepasst I, damit der Regelanhang korrekt ausgegeben wird.", "Besonderer Besitz" : "Trage den gewählten Besitz in das Kommentarfeld ein.",
                 "Privilegien" : "Wähle am besten direkt den separaten Vorteil Privilegien (Adel, Krieger oder Gildenmagier). Falls du andere Privilegien möchtest, dann wähle diesen Vorteil und trage diese in das Kommentarfeld ein.",
                 "Tierempathie" : "Trage die gewählte Gruppe von Tieren in das Kommentarfeld ein.", "Verbindungen" : "Trage die gewählten Verbindungen in das Kommentarfeld ein. Wenn du mehrere Verbindungen hast, dann erhöhe die EP-Kosten entsprechend.",
                 "Beidhändiger Kampf IV" : waffenmeisterschaft, "Kraftvoller Kampf IV" : waffenmeisterschaft, "Schildkampf IV" : waffenmeisterschaft, "Schneller Kampf IV" : waffenmeisterschaft, "Parierwaffenkampf IV" : waffenmeisterschaft, "Reiterkampf IV" : waffenmeisterschaft,
                 "Tiergeist (Affe)" : tiergeist, "Tiergeist (Bär)" : tiergeist, "Tiergeist (Elefant)" : tiergeist, "Tiergeist (Eule)" : tiergeist, "Tiergeist (Falke)" : tiergeist, "Tiergeist (Fischotter)" : tiergeist, "Tiergeist (Fuchs)" : tiergeist,
                 "Tiergeist (Mungo)" : tiergeist, "Tiergeist (Gebirgsbock)" : tiergeist, "Tiergeist (Löwe)" : tiergeist, "Tiergeist (Mammut)" : tiergeist, "Tiergeist (Rabe)" : tiergeist, "Tiergeist (Schlange)" : tiergeist, "Tiergeist (Stier)" : tiergeist, "Tiergeist (Wildkatze)" : tiergeist,
                 "Tiergeist (Panther)" : tiergeist, "Tiergeist (Wildschwein)" : tiergeist, "Tiergeist (Wolf)" : tiergeist, "Tiergeist (Khoramsbestie)" : tiergeist, "Tradition der Alchemisten IV" : meisterschaftM, "Tradition der Borbaradianer IV" : meisterschaftM, "Tradition der Geoden IV" : meisterschaftM,
                 "Tradition der Gildenmagier IV" : meisterschaftM, "Tradition der Druiden IV" : meisterschaftM, "Tradition der Elfen IV" : meisterschaftM, "Tradition der Hexen IV" : meisterschaftM, "Tradition der Kristallomanten IV" : meisterschaftM, "Tradition der Schelme IV" : meisterschaftM,
                 "Tradition der Scharlatane IV" : meisterschaftM, "Tradition der Anach-Nurim IV" : meisterschaftM, "Tradition der Derwische IV" : meisterschaftM,
                 "Tradition der Durro-dun I" : "Die Tiertabelle ist in Sephrasto über die kostenlosen Tiergeist-Vorteile abgebildet, wähle einen davon aus. Dies schaltet alle Zauber des Tiergeists über die Fertigkeit Gaben des Odun frei.",
                 "Tradition der Durro-dun IV" : meisterschaftM, "Tradition der Schamanen IV" : meisterschaftM, "Tradition der Zauberbarden IV" : meisterschaftM, "Tradition der Zaubertänzer IV" : meisterschaftM, "Tradition der Avesgeweihten IV" : meisterschaftL,
                 "Tradition der Borongeweihten IV" : meisterschaftL, "Tradition der Efferdgeweihten IV" : meisterschaftL, "Tradition der Firungeweihten IV" : meisterschaftL, "Tradition der Hesindegeweihten IV" : meisterschaftL, "Tradition der Ifirngeweihten IV" : meisterschaftL,
                 "Tradition der Ingerimmgeweihten IV" : meisterschaftL, "Tradition der Angroschgeweihten IV" : meisterschaftL, "Tradition der Korgeweihten IV" : meisterschaftL, "Tradition der Nandusgeweihten IV" : meisterschaftL, "Tradition der Perainegeweihten IV" : meisterschaftL,
                 "Tradition der Phexgeweihten IV" : meisterschaftL, "Tradition der Praiosgeweihten IV" : meisterschaftL, "Tradition der Rahjageweihten IV" : meisterschaftL, "Tradition der Rondrageweihten IV" : meisterschaftL, "Tradition der Swafnirgeweihten IV" : meisterschaftL,
                 "Tradition der Traviageweihten IV" : meisterschaftL, "Tradition der Tsageweihten IV" : meisterschaftL,
                 "Tradition der Paktierer IV" : "Mit einem Punkt kannst du eine Anrufung um +2 erleichtern (maximal +4) oder eine spontane Modifikation, außer Mächtige Anrufung, um +1 erleichtern (maximal +1). Weitere Vorteile wie ein Krakenruf mit größerem Wirkungsbereich sind ebenfalls möglich, sollten (mitsamt ihren Kosten) aber mit dem Spielleiter und der Gruppe abgesprochen werden. Trage die Verbesserungen in das Kommentarfeld ein.",
                 "Adlerschwinge Wolfsgestalt" : "Trage die gewählten Tiere in das Kommentarfeld ein. Wenn du mehrere Tiere wählst, dann erhöhe die EP-Kosten entsprechend.", "Blutgeist aufnehmen" : "Die Tiertabelle ist in Sephrasto über die kostenlosen Tiergeist-Vorteile abgebildet, wähle einen davon aus. Dies schaltet alle Zauber des Tiergeists kostenlos über die Fertigkeit Gaben des Blutgeists frei - setze bei allen einen Haken.",
                 "Schutzgeist (Tier)" : "Trage die gewählten Tiere in das Kommentarfeld ein. Wenn du mehrere Tiere wählst, dann erhöhe die EP-Kosten entsprechend. Die Tiertabelle ist in Sephrasto außerdem über die kostenlosen Tiergeist-Vorteile abgebildet; wenn du diese auswählst, erhältst du die Werte des Tiergeists im Regelanhang.",
                 "Fluch des (Tieres)" : "Trage die gewählten Tiere in das Kommentarfeld ein. Wenn du mehrere Tiere wählst, dann erhöhe die EP-Kosten entsprechend. Die Tiertabelle ist in Sephrasto außerdem über die kostenlosen Tiergeist-Vorteile abgebildet; wenn du diese auswählst, erhältst du die Werte des Tiergeists im Regelanhang.",
                 "Lockruf (Wesen)" : "Trage die gewählten Wesen in das Kommentarfeld ein. Wenn du mehrere Wesen wählst, dann erhöhe die EP-Kosten entsprechend.", "Tiergestalt" : "Trage das entsprechende Tier in das Kommentarfeld ein.", "Krakenhaut" : "Trage das entsprechende Tier in das Kommentarfeld ein."}

        for el in root.findall('Vorteil') + root.findall('Talent'):
            if el.get('name') in infos:
                el.set("info", infos[el.get('name')])
            if el.text is not None:
                text = el.text.split("\n")
                if text[-1].startswith("Sephrasto:"):
                    el.text = "\n".join(text[:-1]).strip()
                    el.set("info", text[-1][len("Sephrasto:"):].strip())

        # Fill the new bedingungen field
        for el in root.findall('Vorteil'):
            if el.text is None:
                continue
            if not el.text.startswith("Bedingungen:"):
                continue
            text = el.text.split("\n")
            if len(text) == 1:
                text.append("")
            el.text = "\n".join(text[1:]).strip()
            el.set("bedingungen",  text[0][len("Bedingungen:"):].strip())

        # With the talent change the "Regelanhang: Reihenfolge" setting also changed to index the talent type
        for node in root.findall('Einstellung'):
            if node.attrib['name'] == "Regelanhang: Reihenfolge":
                if node.text:
                    node.text = node.text.replace("Z", "S:0")
                    node.text = node.text.replace("L", "S:1")
                    node.text = node.text.replace("A", "S:2")

        return "- Bei Vorteilen können nun Querverweise angegeben werden - bei geänderten RAW Elementen wurden diese automatisch übernommen. Bei selbst erstellten Vorteilen wurde nichts geändert.\n"\
               "- Bei Vorteilen und Talenten können über das neue Infofeld nun Nutzungshinweise für den Charaktereditor angegeben werden. Diese wurden automatisch aus dem Text extrahiert und in das neue Feld eingefügt (in seltenen Fällen können sie zusätzlich noch wie zuvor im Text stehen).\n"\
               "- Bei Vorteilen können über das neue Bedingungen-Feld Bedingungen für die Nutzbarkeit festgelegt werden, z. B. bei Kampfstilen. Diese wurden automatisch aus dem Text extrahiert und in das neue Feld eingefügt.\n"\
               "- Die Vorteile Tiergeist (Wolf/Khoramsbestie), Tiergeist (Wildkatze/Panther) und Vorteil Tiergeist (Fuchs/Mungo) wurden in individuelle Vorteile aufgeteilt und entsprechende Vorteils-Voraussetzungen überall angepasst.\n"\
               "- Die Voraussetzungen von allen Tiergeistern und Geweihtentraditionen wurden vereinfacht durch die neuen Wildcards.\n"\
               "- Bei Spezialtalenten muss nun angegeben werden, ob es sich um Zauber, Liturgien etc. handelt. Dies wurde für alle Spezialtalente automatisch ermittelt."

    #--------------------------------
    # Charakter Migrationsfunktionen
    #--------------------------------

    def charakter0zu1( xmlRoot):
        Kampfstile = ["Kein Kampfstil", "Beidhändiger Kampf", "Parierwaffenkampf", "Reiterkampf", 
              "Schildkampf", "Kraftvoller Kampf", "Schneller Kampf"]

        for waf in xmlRoot.findall('Objekte/Waffen/Waffe'):
            kampfstilIndex = int(waf.attrib['kampfstil'])
            waf.attrib['kampfstil'] = Kampfstile[kampfstilIndex]

        return None

    def charakter1zu2(xmlRoot):
        VorteileAlt = ["Angepasst I (Wasser)", "Angepasst I (Wald)", "Angepasst I (Dunkelheit)", "Angepasst I (Schnee)", "Angepasst II (Wasser)", "Angepasst II (Wald)", "Angepasst II (Dunkelheit)", "Angepasst II (Schnee)", "Tieremphatie"]
        VorteileNeu = ["Angepasst (Wasser) I", "Angepasst (Wald) I", "Angepasst (Dunkelheit) I", "Angepasst (Schnee) I", "Angepasst (Wasser) II", "Angepasst (Wald) II", "Angepasst (Dunkelheit) II", "Angepasst (Schnee) II", "Tierempathie"]

        for vort in xmlRoot.findall('Vorteile/Vorteil'):
            if vort.text in VorteileAlt:
                vort.text = VorteileNeu[VorteileAlt.index(vort.text)]

        return None

    def charakter2zu3(xmlRoot):
        # Some Talente ended with a space, we need to correct that
        # Also we are splitting variable kosten and kommentar into two attributes instead of one with comma separation
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

        # We are updating many tags for better consistency
        # Also we make sure that the many fields that have been added over time are set,
        # so the character load doesnt have to check anymore if they exist
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
            etree.SubElement(objekte, 'Zonensystem').text = "True"

        for waf in objekte.findall('Waffen/Waffe'):
            waf.attrib["härte"] = waf.attrib["haerte"]
            waf.attrib.pop("haerte")
            waf.attrib["würfel"] = waf.attrib["W6"]
            waf.attrib.pop("W6")
            waf.attrib["würfelSeiten"] = "6" # new attribute added
            if not 'wm' in waf.attrib:
                waf.set('wm', "0")

        objekte.find('Zonensystem').text = "1" if objekte.find('Zonensystem').text == "True" else "0"

        if xmlRoot.find('Einstellungen') is None:
            einstellungen = etree.SubElement(xmlRoot, 'Einstellungen')
            etree.SubElement(einstellungen, 'VoraussetzungenPruefen').text = "1"
            etree.SubElement(einstellungen, 'Charakterbogen').text = "Standard Charakterbogen"
            etree.SubElement(einstellungen, 'FinanzenAnzeigen').text = "1"
            etree.SubElement(einstellungen, 'UeberPDFAnzeigen').text = "0"
            etree.SubElement(einstellungen, 'RegelnAnhaengen').text = "1"
            etree.SubElement(einstellungen, 'RegelnGroesse').text = "1"
            etree.SubElement(einstellungen, 'RegelnKategorien').text = "V0, V1, M9, V2, V3, M5, W, M8, M0, M1, V4, V5, M2, M4, Z, V6, V7, M3, M7, L, V8, M6, A, M10"
            etree.SubElement(einstellungen, 'FormularEditierbarkeit').text = "0"
            etree.SubElement(einstellungen, 'Hausregeln').text = ""

        einstellungen = xmlRoot.find('Einstellungen')
        if einstellungen.find('VoraussetzungenPruefen') is None:
            etree.SubElement(einstellungen, 'VoraussetzungenPrüfen').text = "1"
        else:
            einstellungen.find('VoraussetzungenPruefen').tag = 'VoraussetzungenPrüfen'
        einstellungen.find('UeberPDFAnzeigen').tag = 'ÜbernatürlichesPDFSpalteAnzeigen'
        einstellungen.find('RegelnAnhaengen').tag = 'RegelnAnhängen'
        einstellungen.find('RegelnGroesse').tag = 'RegelnGrösse'
        if einstellungen.find('FormularEditierbarkeit') is None:
            etree.SubElement(einstellungen, 'FormularEditierbarkeit').text = "0"
        if einstellungen.find('RegelnKategorien') is None:
            etree.SubElement(einstellungen, 'RegelnKategorien').text = "V0, V1, M9, V2, V3, M5, W, M8, M0, M1, V4, V5, M2, M4, Z, V6, V7, M3, M7, L, V8, M6, A, M10"

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

    def charakter3zu4(xmlRoot):
        einstellungen = xmlRoot.find('Einstellungen')

        # FormularEditierbarkeit has changed from multiple options to on/off
        editierbar = einstellungen.find('FormularEditierbarkeit').text != "2"
        einstellungen.find('FormularEditierbarkeit').text = "1" if editierbar else "0"

        # RegelnGrösse has changed from abstract sizes to real point sizes
        groesse = int(einstellungen.find('RegelnGrösse').text)
        if groesse == 0:
            einstellungen.find('RegelnGrösse').text = "8"
        elif groesse == 1:
            einstellungen.find('RegelnGrösse').text = "10"
        elif groesse == 2:
            einstellungen.find('RegelnGrösse').text = "12"

        # RegelnKategorien has changed a lot, so we reset it
        einstellungen.find('RegelnKategorien').text = "R:12,V:0,R:11,R:9,V:1,R:5,R:0,V:2,V:3,R:8,R:1,W,V:4,V:5,R:2,R:4,Z,V:6,V:7,R:3,R:7,L,V:8,R:6,A,R:10"

        return None
        
    def charakter4zu5(xmlRoot):
        #Talente are now stored individually, not as subelement of Fertigkeit anymore
        talente = []
        targetNode = etree.SubElement(xmlRoot, 'Talente')
        for tal in xmlRoot.findall('.//Talent'):
            if not tal.attrib['name'] in talente:
                talente.append(tal.attrib['name'])
                targetNode.append(tal)

        # Vorteil purchased with Minderpakt is now stored in Minderpakts kommentar
        minderpakt = ""
        for vor in xmlRoot.findall('Vorteile'):
            if "minderpakt" in vor.attrib:
                minderpakt = vor.get('minderpakt')

        for vor in xmlRoot.findall('Vorteile/Vorteil'):
            if vor.text == "Minderpakt":
                vor.set('kommentar', minderpakt)
            vor.set('name', vor.text)
            vor.text = ""
        
        # Make sure the id tag exists so we dont have to check it on character load anymore
        # Some weapons were renamed from x (Infanteriewaffen) to x (Infanteriewaffen und Speere)
        for waf in xmlRoot.findall(".//Waffe"):
            if not "id" in waf.attrib:
                waf.attrib["id"] = waf.attrib["name"]

            if waf.attrib["id"] in ["Dschadra (Infanteriewaffen)", "Efferdbart (Infanteriewaffen)", "Holzspeer (Infanteriewaffen)", "Speer (Infanteriewaffen)"]: 
                waf.attrib["id"] = waf.attrib["id"][:-1] + " und Speere)"
        
        
        einstellungen = xmlRoot.find('Einstellungen')
        # Add new settings
        charakterbogen = einstellungen.find('Charakterbogen').text
        etree.SubElement(einstellungen, 'DetailsAnzeigen').text = "0" if charakterbogen == "Standard Charakterbogen" else "1"
        etree.SubElement(einstellungen, 'DeaktivierteRegelKategorien').text = ""
        return None

