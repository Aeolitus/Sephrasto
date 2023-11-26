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

    def __iter__(self):
        for vor in self.compiled:
            yield vor

    def add(self, text, datenbank = None):
        ret = VoraussetzungenListe()
        if text:
            ret.compile(text, datenbank)
        if not self.text:
            return ret
        if ret.text:
            ret.text += ", "
        ret.text += self.text
        ret.compiled += self.compiled.copy()
        return ret

    def compile(self, text, datenbank = None):
        # first reset, because it may throw
        self.compiled = []
        self.text = ""
        if text:
            self.compiled = self.__compileResurive(text, datenbank)
            self.text = text
        return self

    def __compileResurive(self, text, datenbank = None):
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
        for itm in text.split(","):
            if len(itm) == 0:
                continue
            arrItm = ""
            strpItm = itm.strip()
            if " ODER " in strpItm:
                subArr = []
                for entr in strpItm.split(" ODER "):
                    subArr.append(self.__compileResurive(entr, datenbank))
                arrItm = subArr
            else:
                if strpItm.startswith("Vorteil "):
                    name = strpItm[8:]
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
                elif strpItm.startswith("Kein Vorteil "):
                    name = strpItm[13:]
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
                elif strpItm.startswith("Talent "):
                    if not strpItm[7] == "'":
                        raise VoraussetzungException("Der Name eines Talents muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    strpItm = strpItm[8:]
                    index = strpItm.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    name = strpItm[:index]
                    if datenbank is not None and not (name in datenbank.talente):
                        raise VoraussetzungException("Kann Talent '" + strpItm + "' in der Datenbank nicht finden.")
                    try:
                        wert = int(strpItm[index+2:]) if len(strpItm) -1 > index else -1
                        arrItm = Voraussetzung("T", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Talent-PW '" + strpItm[index+2:] + "' ist keine gültige Zahl")
                elif strpItm.startswith("Waffeneigenschaft "):
                    name = strpItm[18:]
                    if datenbank is not None and (not (name in datenbank.waffeneigenschaften)) and name != "Nahkampfwaffe" and name != "Fernkampfwaffe":
                        raise VoraussetzungException("Kann keine Waffeneigenschaft '" + name + "' in der Datenbank finden.")
                    arrItm = Voraussetzung("W", name, 1)
                elif strpItm.startswith("Attribut "):
                    name = strpItm[9:11]
                    if datenbank is not None and name not in datenbank.attribute:
                        raise VoraussetzungException("Das angegebene Attribut '" + name + "' ist in der Datenbank nicht vorhanden.")
                    try:
                        wert = int(strpItm[12:])
                        arrItm = Voraussetzung("A", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Attribut-Wert '" + strpItm[12:] + "' ist keine gültige Zahl.")
                elif strpItm.startswith("MeisterAttribut "):
                    name = strpItm[16:18]
                    if datenbank is not None and name not in datenbank.attribute:
                        raise VoraussetzungException("Das angegebene Attribut '" + name + "' ist ist in der Datenbank nicht vorhanden.")
                    try:
                        wert = int(strpItm[19:])
                        arrItm = Voraussetzung("M", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Attribut-Wert '" + strpItm[19:] + "' ist keine gültige Zahl.")
                elif strpItm.startswith("Übernatürliche-Fertigkeit "):
                    if not strpItm[26] == "'":
                        raise VoraussetzungException("Der Name einer Übernatürlichen Fertigkeit muss in Apostrophen gefasst werden. (" + strpItm + ")")
                    strpItm = strpItm[27:]
                    index = strpItm.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Übernatürlichen Fertigkeit muss in Apostrophen gefasst werden. (" + strpItm + ")")
                    name = strpItm[:index]

                    if datenbank is not None and name not in datenbank.übernatürlicheFertigkeiten:
                        raise VoraussetzungException("Kann Übernatürliche Fertigkeit '" + name + "' in der datenbank nicht finden.")
                    try:
                        wert = int(strpItm[index+2:]) if len(strpItm) -1 > index else -1
                        arrItm = Voraussetzung("U", name, wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Fertigkeitswert '" + strpItm[index+2:] + "' ist keine gültige Zahl")
                elif strpItm.startswith("Fertigkeit "):
                    if not strpItm[11] == "'":
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    strpItm = strpItm[12:]
                    index = strpItm.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    name = strpItm[:index]

                    if datenbank is not None and name not in datenbank.fertigkeiten:
                        raise VoraussetzungException("Kann Fertigkeit '" + name + "' in der Datenbank nicht finden.")

                    try:
                        wert = int(strpItm[index+2:]) if len(strpItm) -1 > index else -1
                        arrItm = Voraussetzung("F", name, str(wert))
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Fertigkeitswert '" + strpItm[index+2:] + "' ist keine gültige Zahl")
                else:
                    raise VoraussetzungException("Unbekanntes Schlüsselwort '" + strpItm + "'. Unterstützt werden 'Vorteil', 'Kein Vorteil', 'Waffeneigenschaft', 'Attribut', 'MeisterAttribut', 'Übernatürliche-Fertigkeit' und 'Fertigkeit'.")
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