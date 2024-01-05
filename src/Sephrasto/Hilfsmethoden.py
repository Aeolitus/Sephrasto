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
import unicodedata
import locale

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
                #Vorteile:
                if voraus.typ == 'V':
                    cond = voraus.wert == 1
                    found = voraus.name in vorteile
                    if not found and Hilfsmethoden.containsWildcard(voraus.name):
                        ownerIsVorteil = isinstance(dbElement, VorteilDefinition) or isinstance(dbElement, Vorteil)
                        for vort in vorteile:
                            #wildcard-suchen sollten das element ausschließen, dessen voraussetzung gerade geprüft wird
                            if ownerIsVorteil and dbElement.name == vort:
                                continue
                            if fnmatch.fnmatchcase(vort, voraus.name):
                                found = True
                                break
                    erfüllt = (found and cond) or (not found and not cond)
                #Talente:
                elif voraus.typ == 'T':
                    if voraus.name in Wolke.DB.talente:
                        if voraus.wert == -1:
                            if voraus.name in talente:
                                erfüllt = True
                        else:
                            talent = Wolke.DB.talente[voraus.name]
                            ferts = fertigkeiten
                            if talent.spezialTalent:
                                ferts = übernatürlicheFertigkeiten
                            for fertName in talent.fertigkeiten:
                                if not fertName in ferts:
                                    continue
                                fert = ferts[fertName]
                                pw = fert.probenwert
                                if voraus.name in talente:
                                    # do not use talent.probenwert here, it may not be up to date
                                    pw = fert.probenwertTalent
                                if pw >= voraus.wert:
                                    erfüllt = True
                                    break
                #Waffeneigenschaften:
                elif voraus.typ == 'W':
                    for waffe in waffen:
                        if voraus.name == "Nahkampfwaffe" and waffe.nahkampf:
                            erfüllt = True
                            break
                        elif voraus.name == "Fernkampfwaffe" and waffe.fernkampf:
                            erfüllt = True
                            break
                        elif voraus.name in waffe.eigenschaften:
                            erfüllt = True
                            break
                #Attribute:
                elif voraus.typ == 'A':
                    #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                    if attribute[voraus.name].wert >= voraus.wert:
                        erfüllt = True
                #MeisterAttribute:
                elif voraus.typ == 'M':
                    #Wir greifen direkt auf den Eintrag zu und vergleichen. 
                    if attribute[voraus.name].wert >= voraus.wert:
                        attrSorted = [a.wert for a in attribute.values() if a.name != voraus.name]
                        attr1 = max(attrSorted)
                        attrSorted.remove(attr1)
                        attr2 = max(attrSorted)
                        erfüllt = attr1 + attr2 >= voraus.wert * 1.6  
                #Übernatürliche Fertigkeiten:
                elif voraus.typ == 'U':
                    if voraus.name in übernatürlicheFertigkeiten:
                        fertigkeit = übernatürlicheFertigkeiten[voraus.name]
                        if voraus.wert == -1:
                            erfüllt = len(fertigkeit.gekaufteTalente) > 0
                        else:
                            erfüllt = fertigkeit.probenwertTalent >= voraus.wert
                #Fertigkeiten:
                elif voraus.typ == 'F':
                    if voraus.name in fertigkeiten:
                        fertigkeit = fertigkeiten[voraus.name]
                        if voraus.wert == -1:
                            erfüllt = len(fertigkeit.gekaufteTalente) > 0
                        else:
                            erfüllt = fertigkeit.probenwertTalent >= voraus.wert
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
    def AttrArray2Str(AttrArray):
        return "|".join(AttrArray)
    
    @staticmethod
    def AttrStr2Array(AttrStr):
        retArr = []
        if len(AttrStr) == 0:
            return retArr
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

    # see https://docs.python.org/3.9/howto/unicode.html#comparing-strings
    # added strxfrm to use current locale, i. e. to properly sort german umlauts
    # using the unicode collation algorithm would be the perfect solution but strxfrm suffices for now
    def unicodeCaseInsensitive(s):
        def NFD(s):
            return unicodedata.normalize('NFD', s)
        return locale.strxfrm(NFD(NFD(s).casefold()))