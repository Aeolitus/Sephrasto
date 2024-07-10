import fnmatch

class VoraussetzungException(Exception):
    pass

class Voraussetzung:
    def __init__(self, typ, name, wert = -1):
        self.typ = typ
        self.name = name
        self.wert = wert

class VoraussetzungenListe:
    def __init__(self):
        self.text = ""
        self.compiled = []
        
    def __eq__(self, other):
        if self.__class__ != other.__class__: return False
        return self.text == other.text

    def __iter__(self):
        for vor in self.compiled:
            yield vor

    # Adds requirements and returns the combined requirements as a new object
    # Don't worry about duplicate requirements, they will be filtered out
    def add(self, text, datenbank = None):
        ret = VoraussetzungenListe()
        if not text:
            ret.compile(self.text, datenbank)
            return ret
        combined = self.text
        if combined:
            combined += ","
        combined += text
        ret.compile(combined, datenbank)
        return ret

    def compile(self, text, datenbank = None):
        # first reset, because it may throw
        self.compiled = []
        self.text = ""

        if text:
            textLines = dict.fromkeys((map(str.strip, text.split(",")))) #get rid of duplicates and space
            textLines.pop("", None)
            textLines = list(textLines.keys())
            self.compiled = self.__compileResurive(textLines, datenbank)
            self.text = ",".join(textLines)
        return self

    def __compileResurive(self, textLines, datenbank = None):
        '''
        Voraussetzungen werden vom User ebenfalls im Fließtext eingetragen.
        Das Format ist dabei im folgenden Illustriert:
            "Kein Vorteil Eisenaffine Aura, 
            Attribut MU 8 ODER Vorteil Geweiht I ODER Vorteil Emphatie,
            Waffeneigenschaft Rüstungsbrechend"
        Groß- und Kleinschreibung sind wichtig! Kein geht nicht für Attribute.
        Wenn die Datenbank übergeben wird, werden die Voraussetzungen auf Korrektheit geprüft und ggf. Exceptions geworfen
        '''
        retArr = []
        for line in textLines:
            arrItm = ""
            if " ODER " in line:
                subArr = []
                orEntries = list(map(str.strip, line.split(" ODER ")))
                for orEntry in orEntries:
                    subArr.append(self.__compileResurive([orEntry], datenbank))
                arrItm = subArr
            else:
                if line.startswith("Vorteil "):
                    name = line[8:]
                    if datenbank is not None and not (name in datenbank.vorteile):
                        if self.containsWildcard(name):
                            match = False
                            for vort in datenbank.vorteile:
                                if fnmatch.fnmatchcase(vort, name):
                                    match = True
                                    break
                            if not match:
                                raise VoraussetzungException("Kann keinen Vorteil in der Datenbank finden, welcher der Wildcard-Suche '" + name + "' entspricht.")
                        else:
                            raise VoraussetzungException("Kann Vorteil '" + name + "' in der Datenbank nicht finden.")
                    arrItm = Voraussetzung("V", name, 1)
                elif line.startswith("Kein Vorteil "):
                    name = line[13:]
                    if datenbank is not None and not (name in datenbank.vorteile):
                        if self.containsWildcard(name):
                            match = False
                            for vort in datenbank.vorteile:
                                if fnmatch.fnmatchcase(vort, name):
                                    match = True
                                    break
                            if not match:
                                raise VoraussetzungException("Kann keinen Vorteil in der Datenbank finden, welcher der Wildcard-Suche '" + name + "' entspricht.")
                        else:
                            raise VoraussetzungException("Kann Vorteil '" + name + "' in der Datenbank nicht finden.")
                    arrItm = Voraussetzung("V", name, 0)
                elif line.startswith("Talent "):
                    if not line[7] == "'":
                        raise VoraussetzungException("Der Name eines Talents muss in Apostrophen gefasst werden. . (" + line + ")")
                    line = line[8:]
                    index = line.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + line + ")")
                    name = line[:index]
                    if datenbank is not None and not (name in datenbank.talente):
                        raise VoraussetzungException("Kann Talent '" + line + "' in der Datenbank nicht finden.")
                    try:
                        wert = int(line[index+2:]) if len(line) -1 > index else -1
                        arrItm = Voraussetzung("T", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Talent-PW '" + line[index+2:] + "' ist keine gültige Zahl")
                elif line.startswith("Waffeneigenschaft "):
                    name = line[18:]
                    if datenbank is not None and (not (name in datenbank.waffeneigenschaften)) and name != "Nahkampfwaffe" and name != "Fernkampfwaffe":
                        raise VoraussetzungException("Kann keine Waffeneigenschaft '" + name + "' in der Datenbank finden.")
                    arrItm = Voraussetzung("W", name, 1)
                elif line.startswith("Attribut "):
                    name = line[9:11]
                    if datenbank is not None and name not in datenbank.attribute:
                        raise VoraussetzungException("Das angegebene Attribut '" + name + "' ist in der Datenbank nicht vorhanden.")
                    try:
                        wert = int(line[12:])
                        arrItm = Voraussetzung("A", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Attribut-Wert '" + line[12:] + "' ist keine gültige Zahl.")
                elif line.startswith("MeisterAttribut "):
                    name = line[16:18]
                    if datenbank is not None and name not in datenbank.attribute:
                        raise VoraussetzungException("Das angegebene Attribut '" + name + "' ist ist in der Datenbank nicht vorhanden.")
                    try:
                        wert = int(line[19:])
                        arrItm = Voraussetzung("M", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Attribut-Wert '" + line[19:] + "' ist keine gültige Zahl.")
                elif line.startswith("Übernatürliche-Fertigkeit "):
                    if not line[26] == "'":
                        raise VoraussetzungException("Der Name einer Übernatürlichen Fertigkeit muss in Apostrophen gefasst werden. (" + line + ")")
                    line = line[27:]
                    index = line.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Übernatürlichen Fertigkeit muss in Apostrophen gefasst werden. (" + line + ")")
                    name = line[:index]

                    if datenbank is not None and name not in datenbank.übernatürlicheFertigkeiten:
                        raise VoraussetzungException("Kann Übernatürliche Fertigkeit '" + name + "' in der datenbank nicht finden.")
                    try:
                        wert = int(line[index+2:]) if len(line) -1 > index else -1
                        arrItm = Voraussetzung("U", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Fertigkeitswert '" + line[index+2:] + "' ist keine gültige Zahl")
                elif line.startswith("Fertigkeit "):
                    if not line[11] == "'":
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + line + ")")
                    line = line[12:]
                    index = line.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + line + ")")
                    name = line[:index]

                    if datenbank is not None and name not in datenbank.fertigkeiten:
                        raise VoraussetzungException("Kann Fertigkeit '" + name + "' in der Datenbank nicht finden.")

                    try:
                        wert = int(line[index+2:]) if len(line) -1 > index else -1
                        arrItm = Voraussetzung("F", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Fertigkeitswert '" + line[index+2:] + "' ist keine gültige Zahl")
                else:
                    raise VoraussetzungException("Unbekanntes Schlüsselwort '" + line + "'. Unterstützt werden 'Vorteil', 'Kein Vorteil', 'Waffeneigenschaft', 'Attribut', 'MeisterAttribut', 'Übernatürliche-Fertigkeit' und 'Fertigkeit'.")
            retArr.append(arrItm)
        return retArr

    def anzeigetext(self, datenbank):
        if not self.text:
            return "keine"
        # convert to non-nested array with entries separated by "," (= and)
        voraussetzungen = [v.strip() for v in self.text.split(",")]
        # convert MeisterAttribut text
        voraussetzungen = [v + " und 2 weitere Attribute auf insgesamt 16" if "MeisterAttribut" in v else v for v in voraussetzungen]
        # merge multiple "Tradition der " (=marker) entries
        for i in range(len(voraussetzungen)):
            # convert each voraussetzung to array, split by ODER entries
            split = voraussetzungen[i].replace(" ODER ", ",").split(",")
            lastMarker = None
            for j in range(len(split)):
                # remove every occurence of the marker after the first until there is a new marker
                split[j] = split[j].strip()
                for marker in ["Vorteil Tradition der "]:
                    if split[j].startswith(marker):
                        if lastMarker is None or lastMarker != marker:
                            lastMarker = marker
                        else:
                            split[j] = split[j].replace(marker, "")
                    else:
                        lastMarker = None
            voraussetzungen[i] = ", ".join(split)
            voraussetzungen[i] = voraussetzungen[i][::-1].replace(" ,"," REDO ", 1)[::-1] #replace last ", " by " ODER "
        # merge to single string and apply replacements
        voraussetzungen = "; ".join(voraussetzungen)
        for text, replace in datenbank.einstellungen["Voraussetzungen: Anzeigetext ersetzen"].wert.items():
            voraussetzungen = voraussetzungen.replace(text, replace)
        return voraussetzungen
    
    def isAttributVoraussetzung(self, attribut):
        return self.__isAttributVoraussetzungRecusrive(attribut, self.compiled)

    def __isAttributVoraussetzungRecusrive(self, attribut, voraussetzungen):
        for voraus in voraussetzungen:
            if type(voraus) is list:
                if self.__isAttributVoraussetzungRecusrive(attribut, voraus):
                    return True
            else: 
                if voraus.typ == 'A':
                    if voraus.name == attribut:
                        return True
                elif voraus.typ == 'M':
                    return True
        return False

    def containsWildcard(self, string):
        return "*" in string or "?" in string or "[" in string