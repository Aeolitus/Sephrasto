# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:35:08 2017

@author: Aeolitus
"""

class Hilfsmethoden:
    @staticmethod
    def FertStr2Array(FertString, Datenbank):
        '''
        Fertigkeiten werden vom Nutzer Kommasepariert eingetragen. 
        Diese Hilfsmethode trennt den String und gibt ein Array aus einzelnen 
        Fertigkeiten zurück sowie ihre Anzahl.
        '''
        retArr = []
        count = 0;
        for itm in FertString.split(","):
            strpItm = itm.strip()
            if len(strpItm) > 0:
                if (strpItm in Datenbank.fertigkeiten ) or (strpItm in Datenbank.übernatürlicheFertigkeiten):
                    retArr.append(strpItm)
                    count += 1
        return (retArr, count)
    @staticmethod
    def FertArray2Str(Arr):
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
            Attribut MU 8 ODER Vorteil Geweiht I ODER Vorteil Emphatie"
        Groß- und Kleinschreibung sind wichtig! Kein geht nicht für Attribute.
        '''
        retArr = []
        for itm in VoraussetzungenString.split(","):
            arrItm = ""
            strpItm = itm.strip()
            if " ODER " in strpItm:
                subArr = []
                for entr in strpItm.split(" ODER "):
                    subArr.append(Hilfsmethoden.VorStr2Array(entr, Datenbank))
                arrItm = subArr
            else:
                if strpItm.startswith("Vorteil "):
                    arrItm = "V:" + strpItm[8:] + ":1"
                elif strpItm.startswith("Kein Vorteil "):
                    arrItm = "V:" + strpItm[13:] + ":0"
                elif strpItm.startswith("Attribut "):
                    arrItm = "A:" + strpItm[9:11] + ":" + str(strpItm[12:])
            retArr.append(arrItm)
        return retArr