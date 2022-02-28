# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:35:08 2017

@author: Aeolitus
"""
import Definitionen
import logging
import unicodedata
import os
import re
from Wolke import Wolke
import Objekte

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
    def VorStr2Array(VoraussetzungenString, Datenbank):
        '''
        Voraussetzungen werden vom User ebenfalls im Fließtext eingetragen.
        Das Format ist dabei im folgenden Illustriert:
            "Kein Vorteil Eisenaffine Aura, 
            Attribut MU 8 ODER Vorteil Geweiht I ODER Vorteil Emphatie,
            Waffeneigenschaft Rüstungsbrechend"
        Groß- und Kleinschreibung sind wichtig! Kein geht nicht für Attribute.
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
                    if not (strpItm[8:] in Datenbank.vorteile):
                        raise VoraussetzungException("Kann Vorteil '" + strpItm + "' in der Datenbank nicht finden.")
                    arrItm = "V" + delim + strpItm[8:] + delim + "1"
                elif strpItm.startswith("Kein Vorteil "):
                    if not (strpItm[13:] in Datenbank.vorteile):
                        raise VoraussetzungException("Kann Vorteil '" + strpItm + "' in der Datenbank nicht finden.")
                    arrItm = "V" + delim + strpItm[13:] + delim + "0"
                elif strpItm.startswith("Talent "):
                    if not (strpItm[7:] in Datenbank.talente):
                        raise VoraussetzungException("Kann Talent '" + strpItm + "' in der Datenbank nicht finden.")
                    arrItm = "T" + delim + strpItm[7:] + delim + "1"
                elif strpItm.startswith("Waffeneigenschaft "):
                    if (not (strpItm[18:] in Datenbank.waffeneigenschaften)) and strpItm[18:] != "Nahkampfwaffe" and strpItm[18:] != "Fernkampfwaffe":
                        raise VoraussetzungException("Kann keine Waffeneigenschaft '" + strpItm + "' in der Datenbank finden.")
                    arrItm = "W" + delim + strpItm[18:] + delim + "1"
                elif strpItm.startswith("Attribut "):
                    attribut = strpItm[9:11]
                    if attribut in Definitionen.Attribute:
                        try:
                            wert = int(strpItm[12:])
                            arrItm = "A" + delim + attribut + delim + str(wert)
                        except ValueError:
                            raise VoraussetzungException("Der angegebene Attribut-Wert '" + strpItm[12:] + "' ist keine gültige Zahl.")
                    else:
                        raise VoraussetzungException("Das angegebene Attribut '" + attribut + "' ist ungültig. Unterstützt werden 'KO', 'MU', 'GE', 'KK', 'IN', 'KL', 'CH' und 'FF'")
                elif strpItm.startswith("MeisterAttribut "):
                    attribut = strpItm[16:18]
                    if attribut in Definitionen.Attribute:
                        try:
                            wert = int(strpItm[19:])
                            arrItm = "M" + delim + attribut + delim + str(wert)
                        except ValueError:
                            raise VoraussetzungException("Der angegebene Attribut-Wert '" + strpItm[19:] + "' ist keine gültige Zahl.")
                    else:
                        raise VoraussetzungException("Das angegebene Attribut '" + attribut + "' ist ungültig. Unterstützt werden 'KO', 'MU', 'GE', 'KK', 'IN', 'KL', 'CH' und 'FF'")
                elif strpItm.startswith("Übernatürliche-Fertigkeit "):
                    if not strpItm[26] == "'":
                        raise VoraussetzungException("Der Name einer Übernatürlichen Fertigkeit muss in Apostrophen gefasst werden. (" + strpItm + ")")
                    strpItm = strpItm[27:]
                    index = strpItm.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Übernatürlichen Fertigkeit muss in Apostrophen gefasst werden. (" + strpItm + ")")
                    fertigkeit = strpItm[:index]

                    if not (fertigkeit in Datenbank.übernatürlicheFertigkeiten):
                        raise VoraussetzungException("Kann Übernatürliche Fertigkeit '" + fertigkeit + "' in der Datenbank nicht finden.")
                    try:
                        wert = int(strpItm[index+2:])
                        arrItm = "U" + delim + fertigkeit + delim + str(wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Fertigkeitswert '" + strpItm[index+2:] + "' ist keine gültige Zahl")
                elif strpItm.startswith("Fertigkeit "):
                    if not strpItm[11] == "'":
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    strpItm = strpItm[12:]
                    index = strpItm.find("'")
                    if index == -1:
                        raise VoraussetzungException("Der Name einer Fertigkeit muss in Apostrophen gefasst werden. . (" + strpItm + ")")
                    fertigkeit = strpItm[:index]

                    if not (fertigkeit in Datenbank.fertigkeiten):
                        raise VoraussetzungException("Kann Fertigkeit '" + fertigkeit + "' in der Datenbank nicht finden.")

                    try:
                        wert = int(strpItm[index+2:])
                        arrItm = "F" + delim + fertigkeit + delim + str(wert)
                    except ValueError:
                        raise VoraussetzungException("Der angegebene Fertigkeitswert '" + strpItm[index+2:] + "' ist keine gültige Zahl")
                else:
                    raise VoraussetzungException("Unbekanntes Schlüsselwort '" + strpItm + "'. Unterstützt werden 'Vorteil', 'Kein Vorteil', 'Waffeneigenschaft', 'Attribut', 'MeisterAttribut', 'Übernatürliche-Fertigkeit' und 'Fertigkeit'.")
            retArr.append(arrItm)
        return retArr
    
    @staticmethod
    def VorArray2Str(VoraussetzungenArray, Datenbank = None):
        delim = "~"

        retArr = []
        retStr = ""
        for itm in VoraussetzungenArray:
            if type(itm) is list:
                orArr = []
                orStr = ""
                for part in itm:
                    orArr.append(Hilfsmethoden.VorArray2Str(part, Datenbank))    
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
                    enStr += arr[1]
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
                    enStr += "'" + arr[1] + "' "
                    enStr += str(arr[2])
                elif arr[0] == "F":
                    enStr += "Fertigkeit "
                    enStr += "'" + arr[1] + "' "
                    enStr += str(arr[2])
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
    def voraussetzungenPrüfen(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, voraussetzungen):
        return Hilfsmethoden.__voraussetzungenPrüfen(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, voraussetzungen, False)

    @staticmethod
    def __voraussetzungenPrüfen(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, voraussetzungen, Or):
        '''
        Prüft, ob ein Array von Voraussetzungen erfüllt ist.
        Format: ['L:Str:W', 'L:Str:W']
        Dabei ist L:
            V für Vorteil - prüft, ob ein Vorteil vorhanden ist. W = 1 bedeutet, der
                Vorteil muss vorhanden sein. W=0 bedeutet, der Vorteil darf nicht vorhanden sein.
            T für Talent - prüft, ob der Charakter ein Talent mit dem angegebenen Namen besitzt. W ist immer 1.
            W für Waffeneigenschaft - prüft, ob der Charakter eine Waffe mit der angegebenen Eigenschaft besitzt. W ist immer 1.
            A für Attribut - prüft, ob das Attribut mit Key Str mindestens auf Wert W ist
            M für MeisterAttribut - wie Attribut, prüft außerdem ob zwei weitere Attribute auf insg. mindestens 16 sind
            U für Übernatürliche Fertigkeit - prüft, ob für die Übernatürliche Fertigkeit mit Key Str die Voraussetzungen erfüllt sind \
                und sie mindestens auf Wert W ist. W=-1 hat ein spezielle Bedeutung, hier wird an Stelle des Fertigkeitswerts überprüft ob mindestens ein Talent aktiviert ist.
            F für Fertigkeit - prüft, ob für die Übernatürliche Fertigkeit mit Key Str die Voraussetzungen erfüllt sind und sie mindestens auf Wert W ist.
        Einträge im Array können auch weitere Arrays and Voraussetzungen sein.
        Aus diesen Arrays muss nur ein Eintrag erfüllt sein.
        Wenn Wolke.Reqs nicht gesetzt ist, gibt die Methode immer True zurück.
        '''
        if not Wolke.Reqs:
            return True

        #Gehe über alle Elemente in der Liste
        retNor = True
        retOr = False
        for voraus in voraussetzungen:
            erfüllt = False
            if type(voraus) is list:
                erfüllt = Hilfsmethoden.__voraussetzungenPrüfen(vorteile, waffen, attribute, übernatürlicheFertigkeiten, fertigkeiten, voraus,True)
            else: 
                #Split am Separator
                delim = "~"
                arr = re.split(delim, voraus, re.UNICODE)
                #Vorteile:
                if arr[0] == 'V':
                    if len(arr) > 2:
                        cond = int(arr[2])
                    else: 
                        cond = 1
                    found = 0
                    if arr[1] in vorteile:
                        found = 1
                    if found == 1 and cond == 1:
                        erfüllt = True
                    elif found == 0 and cond == 0:
                        erfüllt = True
                #Talente:
                elif arr[0] == 'T':
                    for fert in fertigkeiten.values():
                        if arr[1] in fert.gekaufteTalente:
                            erfüllt = True
                            break
                    if not erfüllt:
                        for fert in übernatürlicheFertigkeiten.values():
                            if arr[1] in fert.gekaufteTalente:
                                erfüllt = True
                                break
                #Waffeneigenschaften:
                elif arr[0] == 'W':
                    for waffe in waffen:
                        if arr[1] == "Nahkampfwaffe" and type(waffe) == Objekte.Nahkampfwaffe:
                            erfüllt = True
                            break
                        elif arr[1] == "Fernkampfwaffe" and type(waffe) == Objekte.Fernkampfwaffe:
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
                        attrSorted = [a.wert for a in attribute.values() if a.key != arr[1]]
                        attr1 = max(attrSorted)
                        attrSorted.remove(attr1)
                        attr2 = max(attrSorted)
                        erfüllt = attr1 + attr2 >= 16  
                #Übernatürliche Fertigkeiten:
                elif arr[0] == 'U':
                    if arr[1] in übernatürlicheFertigkeiten:
                        fertigkeit = übernatürlicheFertigkeiten[arr[1]]
                        wert = int(arr[2])
                        if wert == -1:
                            erfüllt = len(fertigkeit.gekaufteTalente) > 0
                        else:
                            erfüllt = fertigkeit.wert >= wert
                #Fertigkeiten:
                elif arr[0] == 'F':
                    if arr[1] in fertigkeiten:
                        fertigkeit = fertigkeiten[arr[1]]
                        erfüllt = fertigkeit.wert >= int(arr[2])
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
                delim = "~"
                arr = re.split(delim, voraus, re.UNICODE)
                if arr[0] == 'A' or arr[0] == 'M':
                    if arr[1] == attribut:
                        return True
        return False

    @staticmethod
    def AttrArray2Str(AttrArray, Datenbank = None):
        if len(AttrArray) != 3:
            return ""
        retStr = ""
        for el in AttrArray:
            if el not in Definitionen.Attribute:
                return ""
        retStr = AttrArray[0] + "|" + AttrArray[1] + "|" + AttrArray[2]
        return retStr
    
    @staticmethod
    def AttrStr2Array(AttrStr, Datenbank = None):
        retArr = []
        if len(AttrStr) == 0:
            return []
        for el in AttrStr.split("|"):
            if len(el) == 0:
                continue
            if el not in Definitionen.Attribute:
                return []
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

    #The os.listdir implementation is having encoding issues. On OSX the paths are non normalized utf-8, on Unix the paths might be multibyte.
    @staticmethod
    def listdir(path):
        return [unicodedata.normalize('NFC', f.decode("utf-8") if isinstance(f, bytes) else f) for f in os.listdir(path)]
    