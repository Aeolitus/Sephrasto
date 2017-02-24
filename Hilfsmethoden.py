# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:35:08 2017

@author: Aeolitus
"""
import Definitionen

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
    def VorStr2Array(VoraussetzungenString, Datenbank = None):
        '''
        Voraussetzungen werden vom User ebenfalls im Fließtext eingetragen.
        Das Format ist dabei im folgenden Illustriert:
            "Kein Vorteil Eisenaffine Aura, 
            Attribut MU 8 ODER Vorteil Geweiht I ODER Vorteil Emphatie"
        Groß- und Kleinschreibung sind wichtig! Kein geht nicht für Attribute.
        '''
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
                    if (Datenbank is None) or (strpItm[8:] in Datenbank.vorteile):
                        arrItm = "V:" + strpItm[8:] + ":1"
                elif strpItm.startswith("Kein Vorteil "):
                    if (Datenbank is None) or (strpItm[13:] in Datenbank.vorteile):
                        arrItm = "V:" + strpItm[13:] + ":0"
                elif strpItm.startswith("Attribut "):
                    if strpItm[9:11] in Definitionen.Attribute:
                        arrItm = "A:" + strpItm[9:11] + ":" + str(strpItm[12:])
            retArr.append(arrItm)
        return retArr
    
    @staticmethod
    def VorArray2Str(VoraussetzungenArray, Datenbank = None):
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
                arr = itm.split(":")
                enStr = ""
                if arr[0] == "V":
                    if arr[2] == "1":
                        enStr += "Vorteil "
                    else:
                        enStr += "Kein Vorteil "
                    enStr += arr[1]
                elif arr[0] == "A":
                    enStr += "Attribut "
                    enStr += arr[1]
                    enStr += " "
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