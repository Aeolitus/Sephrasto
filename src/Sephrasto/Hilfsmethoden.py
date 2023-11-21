# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:35:08 2017

@author: Aeolitus
"""
import logging
import os
import re
from Wolke import Wolke
from Core.Vorteil import Vorteil, VorteilDefinition
import subprocess
import sys
import fnmatch

class VoraussetzungException(Exception):
    pass

class WaffeneigenschaftException(Exception):
    pass

class Hilfsmethoden:
    '''
    Aufrufen entweder:
        import Hilfsmethoden
        Hilfsmethoden.Hilfsmethoden.XYZ
        
        oder
        
        from Hilfsmethoden import Hilfsmethoden
        Hilfsmethoden.XYZ
    '''
    
    @staticmethod
    def GetWaffeneigenschaft(WaffeneigenschaftStr, Datenbank):
        weName = WaffeneigenschaftStr
        index = weName.find("(")
        if index != -1:
            weName = str.strip(weName[:index])
        
        if not weName in Datenbank.waffeneigenschaften:
            raise WaffeneigenschaftException("Unbekannte Waffeneigenschaft '" + weName + "'")

        if index != -1:
            endIndex = WaffeneigenschaftStr[index:].find(")")
            if endIndex == -1:
                raise WaffeneigenschaftException("Parameter der Waffeneigenschaft '" + weName + "' müssen mit ')' abgeschlossen werden. Mehrere Parameter werden mit Semikolon getrennt.")

        return Datenbank.waffeneigenschaften[weName]

    @staticmethod
    def VerifyWaffeneigenschaft(WaffeneigenschaftStr, Datenbank):
        we = Hilfsmethoden.GetWaffeneigenschaft(WaffeneigenschaftStr, Datenbank)

    @staticmethod
    def FertStr2Array(FertString, Datenbank = None):
        '''
        Fertigkeiten werden vom Nutzer Kommasepariert eingetragen. 
        Diese Hilfsmethode trennt den String und gibt ein Array aus einzelnen 
        Fertigkeiten zurück.
        '''
        retArr = []
        for itm in FertString.split(","):
            if len(itm) == 0:
                continue
            strpItm = itm.strip()
            if len(strpItm) > 0:
                if (Datenbank is None) or (strpItm in Datenbank.fertigkeiten ) or (strpItm in Datenbank.übernatürlicheFertigkeiten):
                    retArr.append(strpItm)
        return retArr
    
    @staticmethod
    def FertArray2Str(Arr, Datenbank = None):
        '''
        Verwandelt die Intern verwendeten Arrays von Fertigkeiten zurück in Strings.
        '''
        retStr = ""
        if len(Arr) > 0:
            retStr = Arr[0]
            for itm in Arr[1:]:
                retStr += ", "
                retStr += itm
        return retStr


    @staticmethod
    def containsWildcard(string):
        return "*" in string or "?" in string or "[" in string

    @staticmethod
    def VorStr2Array(VoraussetzungenString, Datenbank = None):
        '''
        Voraussetzungen werden vom User ebenfalls im Fließtext eingetragen.
        Das Format ist dabei im folgenden Illustriert:
            "Kein Vorteil Eisenaffine Aura, 
            Attribut MU 8 ODER Vorteil Geweiht I ODER Vorteil Emphatie,
            Waffeneigenschaft Rüstungsbrechend"
        Groß- und Kleinschreibung sind wichtig! Kein geht nicht für Attribute.
        Wenn die Datenbank übergeben wird, werden die Voraussetzungen auf Korrektheit geprüft und ggf. Exceptions geworfen
        '''
        delim = "~"

        retArr = []
        for itm in VoraussetzungenString.split(","):
            if len(itm) == 0:
                continue
            arrItm = ""
            strpItm = itm.strip()
            if " ODER " in strpItm:
                subArr = []
                for entr in strpItm.split(" ODER "):
                    subArr.append(Hilfsmethoden.VorStr2Array(entr, Datenbank))
                arrItm = subArr
            else:
                if strpItm.startswith("Vorteil "):
                    name = strpItm[8:]
                    if Datenbank is not None and not (name in Datenbank.vorteile):
                        if Hilfsmethoden.containsWildcard(name):
                            match = False
                            for vort in Datenbank.vorteile:
                                if fnmatch.fnmatchcase(vort, name):
                                    match = True
                                    break
                            if not match:
                                raise VoraussetzungException("Kann keinen Vorteil in der Datenbank finden, welcher der Wildcard-Suche '" + name + "' entspricht.")
                        else:
                            raise VoraussetzungException("Kann Vorteil '" + name + "' in der Datenbank nicht finden.")
                    arrItm = "V" + delim + name + delim + "1"
                elif strpItm.startswith("Kein Vorteil "):
                    name = strpItm[13:]
                    if Datenbank is not None and not (name in Datenbank.vorteile):
                        if Hilfsmethoden.containsWildcard(name):
                            match = False
                            for vort in Datenbank.vorteile:
                                if fnmatch.fnmatchcase(vort, name):
                                    match = True
                                    break
                            if not match:
                                raise VoraussetzungException("Kann keinen Vorteil in der Datenbank finden, welcher der Wildcard-Suche '" + name + "' entspricht.")
                        else:
                            raise VoraussetzungException("Kann Vorteil '" + name + "' in der Datenbank nicht finden.")
                    arrItm = "V" + delim + name + delim + "0"
                elif strpItm.startswith("Talent "):
                    if not strpItm[7] == "'":
                        raise VoraussetzungException("Der Name eines Talents muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    strpItm = strpItm[8:]
                    index = strpItm.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    name = strpItm[:index]
                    if Datenbank is not None and not (name in Datenbank.talente):
                        raise VoraussetzungException("Kann Talent '" + strpItm + "' in der Datenbank nicht finden.")
                    try:
                        wert = int(strpItm[index+2:]) if len(strpItm) -1 > index else -1
                        arrItm = "T" + delim + name + delim + str(wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Talent-PW '" + strpItm[index+2:] + "' ist keine gültige Zahl")
                elif strpItm.startswith("Waffeneigenschaft "):
                    name = strpItm[18:]
                    if Datenbank is not None and (not (name in Datenbank.waffeneigenschaften)) and name != "Nahkampfwaffe" and name != "Fernkampfwaffe":
                        raise VoraussetzungException("Kann keine Waffeneigenschaft '" + name + "' in der Datenbank finden.")
                    arrItm = "W" + delim + name + delim + "1"
                elif strpItm.startswith("Attribut "):
                    name = strpItm[9:11]
                    if Datenbank is not None and name not in Datenbank.attribute:
                        raise VoraussetzungException("Das angegebene Attribut '" + name + "' ist in der Datenbank nicht vorhanden.")
                    try:
                        wert = int(strpItm[12:])
                        arrItm = "A" + delim + name + delim + str(wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Attribut-Wert '" + strpItm[12:] + "' ist keine gültige Zahl.")
                elif strpItm.startswith("MeisterAttribut "):
                    name = strpItm[16:18]
                    if Datenbank is not None and name not in Datenbank.attribute:
                        raise VoraussetzungException("Das angegebene Attribut '" + name + "' ist ist in der Datenbank nicht vorhanden.")
                    try:
                        wert = int(strpItm[19:])
                        arrItm = "M" + delim + name + delim + str(wert)
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

                    if Datenbank is not None and name not in Datenbank.übernatürlicheFertigkeiten:
                        raise VoraussetzungException("Kann Übernatürliche Fertigkeit '" + name + "' in der Datenbank nicht finden.")
                    try:
                        wert = int(strpItm[index+2:]) if len(strpItm) -1 > index else -1
                        arrItm = "U" + delim + name + delim + str(wert)
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

                    if Datenbank is not None and name not in Datenbank.fertigkeiten:
                        raise VoraussetzungException("Kann Fertigkeit '" + name + "' in der Datenbank nicht finden.")

                    try:
                        wert = int(strpItm[index+2:]) if len(strpItm) -1 > index else -1
                        arrItm = "F" + delim + name + delim + str(wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Fertigkeitswert '" + strpItm[index+2:] + "' ist keine gültige Zahl")
                else:
                    raise VoraussetzungException("Unbekanntes Schlüsselwort '" + strpItm + "'. Unterstützt werden 'Vorteil', 'Kein Vorteil', 'Waffeneigenschaft', 'Attribut', 'MeisterAttribut', 'Übernatürliche-Fertigkeit' und 'Fertigkeit'.")
            retArr.append(arrItm)
        return retArr
    
    @staticmethod
    def VorArray2Str(VoraussetzungenArray):
        delim = "~"

        retArr = []
        retStr = ""
        for itm in VoraussetzungenArray:
            if type(itm) is list:
                orArr = []
                orStr = ""
                for part in itm:
                    orArr.append(Hilfsmethoden.VorArray2Str(part))    
                if len(orArr) > 0:
                    orStr = orArr[0]
                if len(orArr) > 1:
                    for ent in orArr[1:]:
                        orStr += " ODER " + ent
                if orStr != "":
                    retArr.append(orStr)
            else:
                arr = itm.split(delim)
                enStr = ""
                if arr[0] == "V":
                    if arr[2] == "1":
                        enStr += "Vorteil "
                    else:
                        enStr += "Kein Vorteil "
                    enStr += arr[1]
                elif arr[0] == "T":
                    enStr += "Talent "
                    enStr += "'" + arr[1] + "'"
                    if arr[2] != '-1':
                        enStr += " " + str(arr[2])
                elif arr[0] == "W":
                    enStr += "Waffeneigenschaft "
                    enStr += arr[1]
                elif arr[0] == "A":
                    enStr += "Attribut "
                    enStr += arr[1]
                    enStr += " "
                    enStr += str(arr[2])
                elif arr[0] == "M":
                    enStr += "MeisterAttribut "
                    enStr += arr[1]
                    enStr += " "
                    enStr += str(arr[2])
                elif arr[0] == "U":
                    enStr += "Übernatürliche-Fertigkeit "
                    enStr += "'" + arr[1] + "'"
                    if arr[2] != '-1':
                        enStr += " " + str(arr[2])
                elif arr[0] == "F":
                    enStr += "Fertigkeit "
                    enStr += "'" + arr[1] + "'"
                    if arr[2] != '-1':
                        enStr += " " + str(arr[2])
                if enStr != "":
                    retArr.append(enStr)
        if len(retArr) > 0:
            retStr = retArr[0]
        if len(retArr) > 1:
            for itm in retArr[1:]:
                if len(itm) > 0:
                    retStr += ", " + itm
        return retStr

    @staticmethod
    def VerifyVorArray(VoraussetzungenArray, Datenbank):
        Hilfsmethoden.VorStr2Array(Hilfsmethoden.VorArray2Str(VoraussetzungenArray), Datenbank)
    
    @staticmethod
    def VorArray2AnzeigeStr(VoraussetzungenArray, Datenbank):
        if len(VoraussetzungenArray) == 0:
            return "keine"
        # convert to non-nested array with entries separated by "," (= and)
        voraussetzungen = [v.strip() for v in Hilfsmethoden.VorArray2Str(VoraussetzungenArray).split(",")]
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
        for text, replace in Datenbank.einstellungen["Voraussetzungen: Anzeigetext ersetzen"].wert.items():
            voraussetzungen = voraussetzungen.replace(text, replace)
        return voraussetzungen

    @staticmethod
    def voraussetzungenPrüfen(dbElement, vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, talente):
        return Hilfsmethoden.__voraussetzungenPrüfen(dbElement, dbElement.voraussetzungen, vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, talente, False)

    @staticmethod
    def __voraussetzungenPrüfen(dbElement, voraussetzungen, vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, talente, Or):
        '''
        Prüft, ob ein Array von Voraussetzungen erfüllt ist.
        Format: ['L:Str:W', 'L:Str:W']
        Dabei ist L:
            V für Vorteil - prüft, ob ein Vorteil vorhanden ist. W = 1 bedeutet, der
                Vorteil muss vorhanden sein. W=0 bedeutet, der Vorteil darf nicht vorhanden sein.
            T für Talent - prüft, ob der Charakter ein Talent mit dem angegebenen Namen besitzt. W ist der Mindest-PW(T).
                Bei profanen Talenten wird auch der PW überprüft, falls das Talent nicht erworben wirde.
                W=-1 hat ein spezielle Bedeutung, hier wird lediglich überprüft, ob das Talent aktiviert ist.
            W für Waffeneigenschaft - prüft, ob der Charakter eine Waffe mit der angegebenen Eigenschaft besitzt. W ist immer 1.
            A für Attribut - prüft, ob das Attribut mit Key Str mindestens auf Wert W ist
            M für MeisterAttribut - wie Attribut, prüft außerdem ob zwei weitere Attribute auf insg. mindestens W * 1.6 sind
            U für Übernatürliche Fertigkeit - prüft, ob für die Übernatürliche Fertigkeit mit Key Str die Voraussetzungen erfüllt sind \
                und sie mindestens den PW(T) W hat. W=-1 hat ein spezielle Bedeutung, hier wird an Stelle des Fertigkeitswerts überprüft, ob mindestens ein Talent aktiviert ist.
            F für Fertigkeit - wie U für Übernatürliche Fertigkeit, aber betrifft profane Fertigkeiten.
        Einträge im Array können auch weitere Arrays and Voraussetzungen sein.
        Aus diesen Arrays muss nur ein Eintrag erfüllt sein.
        '''
        #Gehe über alle Elemente in der Liste
        retNor = True
        retOr = False
        for voraus in voraussetzungen:
            erfüllt = False
            if type(voraus) is list:
                erfüllt = Hilfsmethoden.__voraussetzungenPrüfen(dbElement, voraus, vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, talente, True)
            else: 
                #Split am Separator
                delim = "~"
                arr = re.split(delim, voraus, re.UNICODE)
                #Vorteile:
                if arr[0] == 'V':
                    if len(arr) > 2:
                        cond = int(arr[2]) == 1
                    else: 
                        cond = True
                    found = arr[1] in vorteile
                    if not found and Hilfsmethoden.containsWildcard(arr[1]):
                        for vort in vorteile:
                            #wildcard-suchen sollten das element ausschließen, dessen voraussetuzng gerade geprüft wird
                            if (isinstance(dbElement, VorteilDefinition) or isinstance(dbElement, Vorteil)) and dbElement.name == vort:
                                continue
                            if fnmatch.fnmatchcase(vort, arr[1]):
                                found = True
                                break
                    erfüllt = (found and cond) or (not found and not cond)
                #Talente:
                elif arr[0] == 'T':
                    if arr[1] in Wolke.DB.talente:
                        wert = int(arr[2])
                        if wert == -1:
                            if arr[1] in talente:
                                erfüllt = True
                        else:
                            talent = Wolke.DB.talente[arr[1]]
                            ferts = fertigkeiten
                            if talent.spezialTalent:
                                ferts = übernatürlicheFertigkeiten
                            for fertName in talent.fertigkeiten:
                                if not fertName in ferts:
                                    continue
                                fert = ferts[fertName]
                                pw = fert.probenwert
                                if arr[1] in talente:
                                    # do not use talent.probenwert here, it may not be up to date
                                    pw = fert.probenwertTalent
                                if pw >= wert:
                                    erfüllt = True
                                    break
                #Waffeneigenschaften:
                elif arr[0] == 'W':
                    for waffe in waffen:
                        if arr[1] == "Nahkampfwaffe" and waffe.nahkampf:
                            erfüllt = True
                            break
                        elif arr[1] == "Fernkampfwaffe" and waffe.fernkampf:
                            erfüllt = True
                            break
                        elif arr[1] in waffe.eigenschaften:
                            erfüllt = True
                            break
                #Attribute:
                elif arr[0] == 'A':
                    #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                    if attribute[arr[1]].wert >= int(arr[2]):
                        erfüllt = True
                #MeisterAttribute:
                elif arr[0] == 'M':
                    #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                    if attribute[arr[1]].wert >= int(arr[2]):
                        attrSorted = [a.wert for a in attribute.values() if a.name != arr[1]]
                        attr1 = max(attrSorted)
                        attrSorted.remove(attr1)
                        attr2 = max(attrSorted)
                        erfüllt = attr1 + attr2 >= int(arr[2]) * 1.6  
                #Übernatürliche Fertigkeiten:
                elif arr[0] == 'U':
                    if arr[1] in übernatürlicheFertigkeiten:
                        fertigkeit = übernatürlicheFertigkeiten[arr[1]]
                        wert = int(arr[2])
                        if wert == -1:
                            erfüllt = len(fertigkeit.gekaufteTalente) > 0
                        else:
                            erfüllt = fertigkeit.probenwertTalent >= wert
                #Fertigkeiten:
                elif arr[0] == 'F':
                    if arr[1] in fertigkeiten:
                        fertigkeit = fertigkeiten[arr[1]]
                        wert = int(arr[2])
                        if wert == -1:
                            erfüllt = len(fertigkeit.gekaufteTalente) > 0
                        else:
                            erfüllt = fertigkeit.probenwertTalent >= wert
            if not erfüllt:
                retNor = False
            else:
                retOr = True
        # Alle Voraussetzungen sind gecheckt und wir sind nirgendwo gefailt.
        if Or and (retNor or retOr):
            return retOr
        else:
            return retNor

    @staticmethod
    def isAttributVoraussetzung(attribut, voraussetzungen):
        for voraus in voraussetzungen:
            if type(voraus) is list:
                if Hilfsmethoden.isAttributVoraussetzung(attribut, voraus):
                    return True
            else: 
                if voraus[0] == 'A':
                    if voraus[2:4] == attribut:
                        return True
                elif voraus[0] == 'M':
                    return True
        return False

    @staticmethod
    def AttrArray2Str(AttrArray):
        if len(AttrArray) != 3:
            return ""
        return AttrArray[0] + "|" + AttrArray[1] + "|" + AttrArray[2]
    
    @staticmethod
    def AttrStr2Array(AttrStr):
        retArr = []
        if len(AttrStr) == 0:
            return []
        for el in AttrStr.split("|"):
            if len(el) == 0:
                continue
            retArr.append(el)
        return retArr
    
    @staticmethod
    def RsArray2Str(RsArr):
        return str(RsArr[0]) + "/" + str(RsArr[1]) + "/" + str(RsArr[2]) + "/"\
            + str(RsArr[3]) + "/" + str(RsArr[4]) + "/" + str(RsArr[5])
        
    @staticmethod
    def RsStr2Array(RsStr):
        return [int(a) for a in RsStr.split("/")]

    @staticmethod
    def ArrayEqual(lh, rh):
        if len(lh) != len(rh):
            return False
        else:
            for count in range(0,len(lh)):
                if lh[count] != rh[count]:
                    return False
        return True

    # os.startfile isn't implemented on linux and mac...
    @staticmethod
    def openFile(filepath):
        if sys.platform == "win32":
            os.startfile(filepath.replace('/', '\\'), "open")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filepath])
    
    @staticmethod
    def fixHtml(text, addCSS = True):
        # Replace newlines by <br> tags, unless they are preceded by a '>' or followed by a block-level element
        # Its a bit hacky but placing <br> tags after every line in the database editor would be too cumbersome.

        text = re.sub("\n\s*(?=</?(table|p|div|h\\d|ol|ul|li|tr|th|td))", "", text) #remove any spaces and newlines before a block-level element
        text = re.sub("(</(table|p|div|h\\d|ol|ul|li|tr|th|td)>)\n","\\1", text) #remove any newlines after a block-level element
        text = text.replace("\n", "<br>")
        text = text.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;") #replace 4 whitespaces by non-breaking spaces - the whitespaces would be removed otherwise
        text = text.replace("S. ", "S.&nbsp;") # make sure there is no linebreak in pagenumbers
        text = text.replace("$sephrasto_dir$", "file:///" + os.getcwd().replace('\\', '/'))
        text = text.replace("$regeln_dir$", "file:///" + Wolke.Settings['Pfad-Regeln'].replace('\\', '/'))
        text = text.replace("$plugins_dir$", "file:///" + Wolke.Settings['Pfad-Plugins'].replace('\\', '/'))

        if addCSS:
            css = """<style>
            h4 { margin: 0px; margin-top: 1em; }
            table {margin-top: 1em; margin-bottom: 1em; border-collapse: collapse;}
            th { border-bottom: 1px solid #4A000B; }
            td { padding: 0.1em; }
            ul { padding: 0; margin: 0; }
            ol { padding: 0; margin: 0; }
            </style>"""
            text = f"<head>{css}</head><body>{text}</body>"
        return text

    @staticmethod
    def emToPixels(em):
        return em * Wolke.Settings['FontSize']