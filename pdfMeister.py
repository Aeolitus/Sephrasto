# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:08:59 2017

@author: Lennart

This class exists to handle all the writing of the charactor to the pdf.
"""
from Wolke import Wolke
import pdf
import Definitionen
import Objekte
import re
import Talentbox
from subprocess import check_output
import os
import math
from collections import namedtuple
import logging
import tempfile
from Charakter import KampfstilMod
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import sys
import traceback

CharakterbogenInfo = namedtuple('CharakterbogenInfo', 'filePath maxVorteile maxFreie maxFertigkeiten seitenProfan kurzbogenHack')

class pdfMeister(object):

    def __init__(self):
        # Name des Charakterbogens, der verwendet wird (im gleichen Ordner)
        self.CharakterBogen = None
        self.ExtraPage = "ExtraSpells.pdf"
        self.UseExtraPage = False
        self.ExtraVorts = []
        self.ExtraUeber = []
        self.ExtraTalents = []
        self.PrintRules = True
        self.RulesPage = "Regeln.pdf"
        self.Rules = []
        self.RuleWeights = []
        self.RuleCategories = ['ALLGEMEINE VORTEILE', 'PROFANE VORTEILE', 'KAMPFVORTEILE', 'AKTIONEN', 'WAFFENEIGENSCHAFTEN', 'NAHKAMPFMANÖVER', 'FERNKAMPFMANÖVER', 'ÜBERNATÜRLICHE VORTEILE', 'SPONTANE MODIFIKATIONEN (ZAUBER)', 'SPONTANE MODIFIKATIONEN (LITURGIEN)', 'ÜBERNATÜRLICHE TALENTE', 'SONSTIGES']
        self.Talents = []
        self.Energie = 0
    
    def setCharakterbogenKurz(self):
        self.CharakterBogen = CharakterbogenInfo(filePath="Charakterbogen.pdf", maxVorteile = 8, maxFreie = 12, maxFertigkeiten = 2, seitenProfan = 2, kurzbogenHack=True)

    def setCharakterbogenLang(self):
        self.CharakterBogen = CharakterbogenInfo(filePath="Charakterbogen_lang.pdf", maxVorteile = 24, maxFreie = 28, maxFertigkeiten = 28, seitenProfan = 3, kurzbogenHack=False)

    def pdfErstellen(self, filename, printRules):
        '''
        This entire subblock is responsible for filling all the fields of the
        Charakterbogen. It has been broken down into seven subroutines for
        testing purposes,
        '''
        Wolke.Fehlercode = -80
        Wolke.Char.aktualisieren()
        self.ExtraVorts = []
        self.ExtraTalents = []
        self.ExtraUeber = []
        self.Talents = []
        self.UseExtraPage = False
        Wolke.Fehlercode = -81
        fields = pdf.get_fields(self.CharakterBogen.filePath)
        if self.CharakterBogen.filePath == "Charakterbogen_lang.pdf" and os.path.isfile(filename):
            oldFields = pdf.get_fields(filename)
            keep = ["Kultur", "Profession", "Geschlecht", "Geburtsdatum", "Groesse", "Gewicht", "Haarfarbe", "Augenfarbe",
                    "Aussehen1", "Aussehen2", "Aussehen3", "Aussehen4", "Aussehen5", "Aussehen6", "Titel", "Hintergrund0",
                    "Hintergrund1", "Hintergrund2", "Hintergrund3", "Hintergrund4", "Hintergrund5", "Hintergrund6", "Hintergrund7",
                    "Hintergrund8", "Notiz1", "Notiz2", "Notiz3", "Notiz4", "Notiz5"]
            for key in keep:
                if key in oldFields:
                    fields[key] = oldFields[key]

        Wolke.Fehlercode = -82
        fields = self.pdfErsterBlock(fields)
        Wolke.Fehlercode = -83
        fields = self.pdfZweiterBlock(fields)
        Wolke.Fehlercode = -84
        fields = self.pdfDritterBlock(fields)
        Wolke.Fehlercode = -85
        fields = self.pdfVierterBlock(fields)
        Wolke.Fehlercode = -86
        fields = self.pdfFünfterBlock(fields)
        Wolke.Fehlercode = -87
        fields = self.pdfSechsterBlock(fields)
        Wolke.Fehlercode = -88
        fields = self.pdfSiebterBlock(fields)

        Wolke.Fehlercode = -99
        if not self.pdfExecutePlugin(fields):
            Wolke.Fehlercode = 0
            return

        # PDF erstellen - Felder bleiben bearbeitbar
        Wolke.Fehlercode = -89
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
        allPages = [out_file]
        pdf.write_pdf(self.CharakterBogen.filePath, fields, out_file, False)
        Wolke.Fehlercode = -90
        extraPageAdded = False
        if self.UseExtraPage:
            while len(self.ExtraVorts) > 0 or \
                     len(self.ExtraTalents) > 0 or \
                        len(self.ExtraUeber) > 0:
                fieldsNew = None
                extraPageAdded = True
                Wolke.Fehlercode = -91
                fieldsNew = pdf.get_fields(self.ExtraPage)
                Wolke.Fehlercode = -92
                fieldsNew = self.createExtra(self.ExtraVorts,self.ExtraUeber,self.ExtraTalents,fieldsNew)
                Wolke.Fehlercode = -93

                handle, out_file = tempfile.mkstemp()
                os.close(handle)
                allPages.append(out_file)
                pdf.write_pdf(self.ExtraPage, fieldsNew, out_file, False)
                del self.ExtraVorts[0:12]
                del self.ExtraUeber[0:12]
                del self.ExtraTalents[0:30]
        
        #Entferne Seite 3, falls keine übernatürlichen Fertigkeiten
        if fields['Uebervorteil1'] == '' and \
           fields['Ueberfer1NA'] == '' and \
           fields['Uebertal1NA'] == '' and not extraPageAdded:
            Wolke.Fehlercode = -96
            handle, out_file = tempfile.mkstemp()
            os.close(handle)
            pdf.shrink(allPages[0], 1, self.CharakterBogen.seitenProfan, out_file)
            os.remove(allPages[0])
            allPages[0] = out_file
        
        Wolke.Fehlercode = -97
        if printRules:
            rulesFields = pdf.get_fields(self.RulesPage)
            self.prepareRules()
            startIndex = 0
            pageCount = 0

            fontSize = Wolke.Settings["Cheatsheet-Fontsize"]
            lineCount = 0
            if fontSize == 0:
                lineCount = 80
            elif fontSize == 1:
                lineCount = 60
            elif fontSize == 2:
                lineCount = 40

            while startIndex != -1:
                pageCount += 1
                rulesFields["Seite"] = pageCount
                startIndex = self.writeRules(rulesFields, startIndex, lineCount)
                handle, out_file = tempfile.mkstemp()
                os.close(handle)
                pdf.write_pdf(self.RulesPage, rulesFields, out_file, False)
                allPages.append(out_file)

        Wolke.Fehlercode = -94
        pdf.concat(allPages, filename)

        Wolke.Fehlercode = -95
        for page in allPages:
            os.remove(page)

        Wolke.Fehlercode = -98
        #Open PDF with default application:
        if Wolke.Settings['PDF-Open']:
            os.startfile(filename, 'open')
            
        Wolke.Fehlercode = 0

    def pdfErsterBlock(self, fields):
        logging.debug("PDF Block 1")
        fields['Name'] = Wolke.Char.name
        fields['Rasse'] = Wolke.Char.rasse
        fields['Kultur'] = Wolke.Char.heimat
        fields['Statu'] = Definitionen.Statusse[Wolke.Char.status]
        fields['Finanzen'] = Definitionen.Finanzen[Wolke.Char.finanzen]
        fields['Kurzb'] = Wolke.Char.kurzbeschreibung
        fields['Schip'] = Wolke.Char.schipsMax
        fields['Schipm'] = Wolke.Char.schips
        # Erste Acht Eigenheiten
        count = 0
        eigFields = [1, 2, 3, 4, 5, 6, 7, 8]
        for el in Wolke.Char.eigenheiten:
            fields['Eigen' + str(eigFields[count])] = el
            if count == 8:
                break
            count += 1
        return fields

    def pdfZweiterBlock(self, fields):
        logging.debug("PDF Block 2")
        for key in Definitionen.Attribute:
            fields[key] = Wolke.Char.attribute[key].wert
            fields[key + '2'] = Wolke.Char.attribute[key].probenwert
            fields[key + '3'] = Wolke.Char.attribute[key].probenwert
        fields['WundschwelleBasis'] = Wolke.Char.wsBasis
        fields['Wundschwelle'] = Wolke.Char.ws
        fields['WS'] = Wolke.Char.ws
        if "Unverwüstlich" in Wolke.Char.vorteile:
            fields['ModUnverwuestlich'] = 'Yes'

        fields['MagieresistenzBasis'] = Wolke.Char.mrBasis
        fields['Magieresistenz'] = Wolke.Char.mr
        if "Willensstark I" in Wolke.Char.vorteile:
            fields['ModWillensstark1'] = 'Yes'
        if "Willensstark II" in Wolke.Char.vorteile:
            fields['ModWillensstark2'] = 'Yes'
        if "Unbeugsamkeit" in Wolke.Char.vorteile:
            fields['ModUnbeugsam'] = 'Yes'

        fields['GeschwindigkeitBasis'] = Wolke.Char.gsBasis
        fields['Geschwindigkeit'] = Wolke.Char.gs
        if "Flink I" in Wolke.Char.vorteile:
            fields['ModFlink1'] = 'Yes'
        if "Flink II" in Wolke.Char.vorteile:
            fields['ModFlink2'] = 'Yes'

        fields['SchadensbonusBasis'] = Wolke.Char.schadensbonusBasis
        fields['Schadensbonus'] = Wolke.Char.schadensbonus

        fields['InitiativeBasis'] = Wolke.Char.iniBasis
        fields['Initiative'] = Wolke.Char.ini
        fields['INIm'] = Wolke.Char.ini
        if "Kampfreflexe" in Wolke.Char.vorteile:
            fields['ModKampfreflexe'] = 'Yes'

        if "Gefäß der Sterne" in Wolke.Char.vorteile:
            fields['ModGefaess'] = 'Yes'

        isZauberer = Wolke.Char.aspBasis + Wolke.Char.aspMod > 0
        isGeweiht = Wolke.Char.kapBasis + Wolke.Char.kapMod > 0
        if isZauberer:
            fields['AstralenergieBasis'] = Wolke.Char.aspBasis
            fields['Astralenergie'] = Wolke.Char.asp.wert + Wolke.Char.aspBasis + Wolke.Char.aspMod
            fields['ModAstralenergie'] = Wolke.Char.asp.wert

        if isGeweiht:
            fields['KarmaenergieBasis'] = Wolke.Char.kapBasis
            fields['Karmaenergie'] = Wolke.Char.kap.wert + Wolke.Char.kapBasis + Wolke.Char.kapMod
            fields['ModKarmaenergie'] = Wolke.Char.kap.wert

        if isZauberer and not isGeweiht:
            self.Energie = Wolke.Char.asp.wert + Wolke.Char.aspBasis + Wolke.Char.aspMod
            fields['EN'] = self.Energie
            #fields['gEN'] = "0"
        elif not isZauberer and isGeweiht:
            self.Energie = Wolke.Char.kap.wert + Wolke.Char.kapBasis + Wolke.Char.kapMod
            fields['EN'] = self.Energie
            #fields['gEN'] = "0"
        # Wenn sowohl AsP als auch KaP vorhanden sind, muss der Spieler ran..

        trueBE = max(Wolke.Char.be, 0)
        fields['DHm'] = max(Wolke.Char.dh - 2*trueBE, 1)
        fields['GSm'] = max(Wolke.Char.gs-trueBE, 1)
        fields['WSm'] = Wolke.Char.wsStern

        return fields

    def pdfDritterBlock(self, fields):
        logging.debug("PDF Block 3")
        sortV = Wolke.Char.vorteile.copy()
        typeDict = {}
        assembled = []
        removed = []
        # Collect a list of Vorteils, where different levels of the same are
        # combined into one entry and the type of Vorteil is preserved
        for vort in sortV:
            if vort in removed:
                continue
            if vort == "Minderpakt" and Wolke.Char.minderpakt is not None:
                removed.append(vort)
                mindername = "Minderpakt (" + Wolke.Char.minderpakt + ")"
                assembled.append(mindername)
                typeDict[mindername] = 0
                continue
            flag = False
            if not vort in Wolke.Char.vorteileVariable:
                if vort.endswith(" I"):
                    basename = vort[:-2]
                    flag = True
                elif vort.endswith(" II") or vort.endswith(" IV"):
                    basename = vort[:-3]
                    flag = True
                elif vort.endswith(" III"):
                    basename = vort[:-4]
                    flag = True

            if flag:
                fullset = [" I", " II", " III", " IV"]
                fullenum = ""
                for el in fullset:
                    if basename+el in sortV:
                        removed.append(basename+el)
                        fullenum += "," + el[1:]
                vname = basename + " " + fullenum[1:]
                typeDict[vname] = Wolke.DB.vorteile[vort].typ
                assembled.append(vname)
                if "Zauberer" in vname or "Geweiht" in vname:
                    typeDict[vname] = 4
            else:
                typeDict[vort] = Wolke.DB.vorteile[vort].typ
        for el in removed:
            if el in sortV:
                sortV.remove(el)
        for el in assembled:
            sortV.append(el)
        removed = []
        added = []

        # Add the cost for Vorteils with variable costs
        for el in sortV:
            # This is only going to be general Vorteile anyways,
            # so type doesnt matter
            if el in Wolke.Char.vorteileVariable:
                removed.append(el)
                vk = Wolke.Char.vorteileVariable[el]
                nname = el + " (" + vk.kommentar + "; " + str(vk.kosten) + " EP)"
                added.append(nname)
                typeDict[nname] = typeDict[el]
        for el in removed:
            sortV.remove(el)
        for el in added:
            sortV.append(el)

        # Sort and split the Vorteile into the three categories
        sortV = sorted(sortV, key=str.lower)
        tmpVorts = [el for el in sortV if typeDict[el] < 2]
        tmpKampf = [el for el in sortV if (typeDict[el] < 4 and
                                           typeDict[el] >= 2)]
        tmpUeber = [el for el in sortV if typeDict[el] >= 4]
        tmpOverflow = []
        tmpUeberflow = []
        
        # Fill up categories that are not full with the overflow
        if len(tmpVorts) > self.CharakterBogen.maxVorteile:
            tmpOverflow.extend(tmpVorts[self.CharakterBogen.maxVorteile:])
            tmpVorts = tmpVorts[:self.CharakterBogen.maxVorteile]
        if len(tmpKampf) > 16:
            tmpOverflow.extend(tmpKampf[16:])
            tmpKampf = tmpKampf[:16]
        if len(tmpUeber) > 12:
            tmpUeberflow.extend(tmpUeber[12:])
            tmpUeber = tmpUeber[:12]
        counter = 0
        for i in range(len(tmpVorts), self.CharakterBogen.maxVorteile):
            if len(tmpOverflow) > counter:
                tmpVorts.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(tmpKampf), 16):
            if len(tmpOverflow) > counter:
                tmpKampf.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(tmpUeber), 12):
            if len(tmpOverflow) > counter:
                tmpUeber.append(tmpOverflow[counter])
                counter += 1
        tmptmp = tmpOverflow[counter:]
        for el in tmptmp:
            tmpUeberflow.append(el)
        # Fill fields
        for i in range(1, self.CharakterBogen.maxVorteile+1):
            if i <= len(tmpVorts):
                fields['Vorteil' + str(i)] = tmpVorts[i-1]
        for i in range(1, 17):
            if i <= len(tmpKampf):
                fields['Kampfvorteil' + str(i)] = tmpKampf[i-1]
        for i in range(1, 13):
            if i <= len(tmpUeber):
                fields['Uebervorteil' + str(i)] = tmpUeber[i-1]
        if len(tmpUeberflow) > 0:
            self.UseExtraPage = True
            for el in tmpUeberflow:
                if len(el) > 0:
                    self.ExtraVorts.append(el)
            
        return fields

    def pdfVierterBlock(self, fields):
        logging.debug("PDF Block 4")
        # Freie Fertigkeiten
        count = 1

        for el in Wolke.Char.freieFertigkeiten:
            if el.wert < 1 or el.wert > 3 or not el.name:
                continue
            resp = el.name + " "
            for i in range(el.wert):
                resp += "I"

            if fields['Frei' + str(count)]:
                fields['Frei' + str(count)] += ", " + resp
            else:
                fields['Frei' + str(count)] = resp
            count += 1
            if count > self.CharakterBogen.maxFreie:
                count = 1

        if self.CharakterBogen.kurzbogenHack:
            self.writeFertigkeiten(fields, None, Definitionen.StandardFerts)

            nonstandardFerts = []
            for el in Wolke.Char.fertigkeiten:
                if not el in Definitionen.StandardFerts:
                    nonstandardFerts.append(el)
            nonstandardFerts.sort(key = lambda x: Wolke.DB.fertigkeiten[x].printclass)
            self.writeFertigkeiten(fields, "Indi", nonstandardFerts)
        else:
            sortedFerts = sorted(Wolke.Char.fertigkeiten, key = lambda x: (Wolke.DB.fertigkeiten[x].printclass, x))
            self.writeFertigkeiten(fields, "Fertigkeit", sortedFerts)
        return fields

    def writeFertigkeiten(self, fields, baseStr, fertigkeitenNames):
        count = 1
        for el in fertigkeitenNames:
            if el not in Wolke.Char.fertigkeiten:
                continue
            fertigkeit = Wolke.Char.fertigkeiten[el]

            if baseStr:
                base = baseStr + str(count)
                fields[base + "NA"] = fertigkeit.name           
                fields[base + "FA"] = fertigkeit.steigerungsfaktor
                fields[base + "AT"] = \
                    fertigkeit.attribute[0] + '/' + \
                    fertigkeit.attribute[1] + '/' + \
                    fertigkeit.attribute[2]
            else:
                base = el[0:5]
                # Fix Umlaute
                if el == "Gebräuche":
                    base = "Gebra"
                elif el == "Überleben":
                    base = "Ueber"

            if fertigkeit.basiswertMod == 0:
                fields[base + "BA"] = fertigkeit.basiswert
            else:
                fields[base + "BA"] = str(fertigkeit.basiswert) + "*"

            fields[base + "FW"] = fertigkeit.wert
            talStr = ""

            talente = sorted(fertigkeit.gekaufteTalente)
            for el2 in talente:
                talStr += ", "
                talStr += el2.replace(fertigkeit.name + ": ", "")

                if el2 in fertigkeit.talentMods:
                    for condition,mod in fertigkeit.talentMods[el2].items():
                        talStr += " " + (condition + " " if condition else "") + ("+" if mod >= 0 else "") + str(mod)

                if el2 in Wolke.Char.talenteVariable:
                    vk = Wolke.Char.talenteVariable[el2]
                    talStr += " (" + vk.kommentar + ")"

            #Append any talent mods of talents the character doesn't own in parentheses
            for talentName, talentMods in fertigkeit.talentMods.items():
                if not talentName in talente:
                    talStr += ", (" + talentName
                    for condition,mod in talentMods.items():
                        talStr += " " + (condition + " " if condition else "") + ("+" if mod >= 0 else "") + str(mod)
                    talStr += ")"

            talStr = talStr[2:]

            fields[base + "TA"] = talStr
            fields[base + "PW"] = fertigkeit.probenwert
            fields[base + "PWT"] = fertigkeit.probenwertTalent
            count += 1

    def pdfFünfterBlock(self, fields):
        logging.debug("PDF Block 5")
        # Fill three rows of Rüstung
        count = 1
        for el in Wolke.Char.rüstung:
            base = 'Ruest' + str(count)
            fields[base + 'NA'] = el.name
            fields[base + 'RS'] = int(sum(el.rs)/6+0.5+0.0001)+Wolke.Char.rsmod
            fields[base + 'BE'] = max(el.be - Wolke.Char.rüstungsgewöhnung, 0)
            fields[base + 'WS'] = int(sum(el.rs) / 6 + Wolke.Char.ws +
                                      0.5 + Wolke.Char.rsmod + 0.0001)
            base += 'RS'
            fields[base + 'Bein'] = el.rs[0]+Wolke.Char.rsmod+Wolke.Char.ws
            fields[base + 'lArm'] = el.rs[1]+Wolke.Char.rsmod+Wolke.Char.ws
            fields[base + 'rArm'] = el.rs[2]+Wolke.Char.rsmod+Wolke.Char.ws
            fields[base + 'Bauch'] = el.rs[3]+Wolke.Char.rsmod+Wolke.Char.ws
            fields[base + 'Brust'] = el.rs[4]+Wolke.Char.rsmod+Wolke.Char.ws
            fields[base + 'Kopf'] = el.rs[5]+Wolke.Char.rsmod+Wolke.Char.ws
            count += 1
            if count > 3:
                break

        # Fill eight rows of weapons
        count = 1
        for el in Wolke.Char.waffen:
            waffenwerte = Wolke.Char.waffenwerte[count-1]

            base = 'Waffe' + str(count)
            fields[base + 'NA'] = el.anzeigename
            sg = ""
            if el.plus >= 0:
                sg = "+"

            keinSchaden = el.W6 == 0 and el.plus == 0
            
            fields[base + 'TP'] = "-" if keinSchaden else str(el.W6) + "W6" + sg + str(el.plus)
            fields[base + 'HA'] = str(waffenwerte.Haerte)
            fields[base + 'EI'] = ", ".join(el.eigenschaften)

            fields[base + 'ATm'] = str(waffenwerte.AT)

            if type(el) == Objekte.Fernkampfwaffe or (el.name in Wolke.DB.waffen and Wolke.DB.waffen[el.name].talent == 'Lanzenreiten'):
                fields[base + 'VTm'] = "-"
            else:
                fields[base + 'VTm'] = str(waffenwerte.VT)

            fields[base + 'RW'] = str(waffenwerte.RW)

            wm = str(el.wm)
            if type(el) == Objekte.Fernkampfwaffe:
                wm = wm + " / " + str(el.lz)

            fields[base + 'WM'] = wm

            sg = ""
            if waffenwerte.TPPlus >= 0:
                sg = "+"
            fields[base + 'TPm'] = "-" if keinSchaden else str(waffenwerte.TPW6) + "W6" + sg + str(waffenwerte.TPPlus)

            if count >= 8:
                break
            count += 1

        # Fill 20 Cells of Ausrüstung
        count = 1
        for el in Wolke.Char.ausrüstung:
            fields['Ausruestung' + str(count)] = el
            if count >= 20:
                break
            count += 1
        return fields

    def pdfSechsterBlock(self, fields):
        logging.debug("PDF Block 6")

        #addedTals = {}  # Name: (PWT, base)

        # Get number of talents
        countFerts = 0
        talsList = []
        for f in Wolke.Char.übernatürlicheFertigkeiten:
            if Wolke.Char.übernatürlicheFertigkeiten[f].wert > 0 or\
                    len(Wolke.Char.übernatürlicheFertigkeiten[f].
                        gekaufteTalente) > 0:
                talsList.extend(Wolke.Char.übernatürlicheFertigkeiten[f].
                                gekaufteTalente)
                countFerts += 1
        talsList = set(talsList)

        fertsList = []
        for f in Wolke.Char.übernatürlicheFertigkeiten:
            if Wolke.Char.übernatürlicheFertigkeiten[f].wert <= 0 and\
                    len(Wolke.Char.übernatürlicheFertigkeiten[f].
                        gekaufteTalente) == 0:
                continue
            fertsList.append(f)
        fertsList.sort(key = lambda x: (Wolke.DB.übernatürlicheFertigkeiten[x].printclass, x))

        countF = 1
        countT = 1
        for f in fertsList:
            fe = Wolke.Char.übernatürlicheFertigkeiten[f]

            if countF < 13:
                # Fill Fertigkeitsslots
                base = 'Ueberfer' + str(countF)
                fields[base + 'NA'] = fe.name
                fields[base + 'FA'] = fe.steigerungsfaktor
                fields[base + 'AT'] = fe.attribute[0] + '/' + \
                    fe.attribute[1] + '/' + fe.attribute[2]
                fields[base + 'FW'] = fe.wert
                fields[base + 'PW'] = fe.probenwertTalent

                if fe.basiswertMod == 0:
                    fields[base + 'BA'] = fe.basiswert
                else:
                    fields[base + 'BA'] = str(fe.basiswert) + "*"
            else:
                self.UseExtraPage = True
                self.ExtraUeber.append(fe)
            countF += 1
            
            # Fill Talente
            tals = sorted(fe.gekaufteTalente, key=lambda s: s.lower())
            for t in tals:
                #base = 'Uebertal' + str(countT)
                tt = Talentbox.Talentbox()
                mod = ""
                if t in Wolke.Char.talenteVariable:
                    vk = Wolke.Char.talenteVariable[t]
                    mod += " (" + vk.kommentar + ")"

                #if t+mod in self.Talents:
                #    if fe.probenwertTalent > self.Talents[t+mod].pw:
                #        self.Talents[t+mod].pw = fe.probenwertTalent
                        #fields[self.addedTals[t+mod][1] + 'PW'] = \
                              #fe.probenwertTalent
                        #self.addedTals[t+mod] = (fe.probenwertTalent,
                        #                    self.addedTals[t+mod][1])
                #else:
                #self.addedTals[t+mod] = (fe.probenwertTalent, base)
                if t in Wolke.DB.talente and len(Wolke.DB.talente[t].fertigkeiten) == 1:
                    tt.na = t.replace(f + ": ", "") + mod
                else:
                    tt.na = t + mod
                #fields[base + 'NA'] = t + mod
                tt.pw = fe.probenwertTalent
                #fields[base + 'PW'] = fe.probenwertTalent
                # Get Spellinfo from text
                if t in Wolke.DB.talente:
                    txt = Wolke.DB.talente[t].text
                    res = re.findall('Vorbereitungszeit:(.*?)\n',
                                     txt,
                                     re.UNICODE)
                    if len(res) == 1:
                        tt.vo = res[0].strip()
                        #fields[base + 'VO'] = res[0].strip()
                    res = re.findall('Reichweite:(.*?)\n',
                                     txt,
                                     re.UNICODE)
                    if len(res) == 1:
                        tt.re = res[0].strip()
                        #fields[base + 'RE'] = res[0].strip()
                    res = re.findall('Wirkungsdauer:(.*?)\n',
                                     txt,
                                     re.UNICODE)
                    if len(res) == 1:
                        tt.wd = res[0].strip()
                        #fields[base + 'WD'] = res[0].strip()
                    res = re.findall('Kosten:(.*?)\n',
                                     txt,
                                     re.UNICODE)
                    if len(res) == 1:
                        tt.ko = res[0].strip()
                        #fields[base + 'KO'] = res[0].strip()

                    tt.pc = Wolke.DB.talente[t].printclass

                idx = -1
                for i in range(len(self.Talents)):
                    if self.Talents[i].na == tt.na:
                        idx = i
                        break
                if idx >= 0:
                    if self.Talents[idx].pw < tt.pw:
                        self.Talents.pop(idx)
                        self.Talents.append(tt)
                else:
                    self.Talents.append(tt)
                # if tt.na in self.Talents:
                #     if tt.pw > self.Talents[tt.na].pw:
                #         self.Talents.pop(tt.na,None)
                #         self.Talents[tt.na] = tt
                # else:
                #     self.Talents[tt.na] = tt

        # Sort by printclass. Old sorting stays for same printclass, so this should not mess stuff up.
        self.Talents.sort(key = lambda x: (x.pc, x.na))
        i = 0
        while i < len(self.Talents):
            if i < 30:
                base = 'Uebertal' + str(i+1)
                fields[base + 'NA'] = self.Talents[i].na
                fields[base + 'PW'] = self.Talents[i].pw
                fields[base + 'VO'] = self.Talents[i].vo
                fields[base + 'WD'] = self.Talents[i].wd
                fields[base + 'KO'] = self.Talents[i].ko
                fields[base + 'RE'] = self.Talents[i].re
            else:
                if self.Talents[i] not in self.ExtraTalents:
                    self.UseExtraPage = True
                    self.ExtraTalents.append(self.Talents[i])
            i += 1

        return fields

    def pdfSiebterBlock(self, fields):
        logging.debug("PDF Block 7")
        fields['ErfahGE'] = Wolke.Char.EPtotal
        fields['ErfahEI'] = Wolke.Char.EPspent
        fields['ErfahVE'] = Wolke.Char.EPtotal - Wolke.Char.EPspent
        return fields

    def pdfExecutePlugin(self, fields):
        if Wolke.Settings['Pfad-Export-Plugin'] and os.path.isfile(Wolke.Settings['Pfad-Export-Plugin']):
            api = {}
            for k, v in Wolke.Char.charakterScriptAPI.items():
                if k.startswith('get'):
                    api[k] = v
            api['data'] = fields
            api['sephrastoExport'] = True

            try:
                exec(open(Wolke.Settings['Pfad-Export-Plugin'], mode="r", encoding="utf-8").read(), api)
            except Exception as err:
                error_class = err.__class__.__name__
                detail = err.args[0]
                cl, exc, tb = sys.exc_info()
                line_number = traceback.extract_tb(tb)[-1][1]
                raise Exception("%s at line %d: %s" % (error_class, line_number, detail))

            return api['sephrastoExport']
        return True

    def createExtra(self, vorts, ferts, tals, fields):
        for i in range(1, 13):
            if i <= len(vorts):
                fields['Uebervorteil' + str(i) + "S2"] = vorts[i-1]
        for i in range(1, 13):
            if i <= len(ferts):
                fe = ferts[i-1]
                base = 'Ueberfer' + str(i)
                fields[base + 'NA' + '2'] = fe.name
                fields[base + 'FA' + '2'] = fe.steigerungsfaktor
                fields[base + 'AT' + '2'] = fe.attribute[0] + '/' + \
                    fe.attribute[1] + '/' + fe.attribute[2]
                fields[base + 'FW' + '2'] = fe.wert
                fields[base + 'PW' + '2'] = fe.probenwertTalent

                if fe.basiswertMod == 0:
                    fields[base + 'BA' + '2'] = fe.basiswert
                else:
                    fields[base + 'BA' + '2'] = str(fe.basiswert) + "*"
        for i in range(1, 31):
            if i <= len(tals):
                tt = tals[i-1]
                base = 'Uebertal' + str(i)
                fields[base + 'NA' + '2'] = tt.na
                fields[base + 'PW' + '2'] = tt.pw
                fields[base + 'VO' + '2'] = tt.vo
                fields[base + 'WD' + '2'] = tt.wd
                fields[base + 'KO' + '2'] = tt.ko
                fields[base + 'RE' + '2'] = tt.re
        fields['EN2'] = self.Energie
        return fields

    #The idea to divide by 100 is that one line is on average 100 characters.
    #This weighs lines with 140 characters same as much as those with 200 characters because they take up same as much vertical space.
    #Since every entry also creates a new paragraph (two \n), add one to the weight
    def getWeight(str):
        return max(int(math.ceil(len(str)/100)), 1) + 1

    def formatRuleCategory(category, firstLine = False):
        if firstLine:
            return category + '\n\n'
        else:
            return '\n' + category + '\n\n'

    def appendWaffeneigenschaften(strList, weights, category, eigenschaften):
        strList.append(pdfMeister.formatRuleCategory(category))
        weights.append(pdfMeister.getWeight(strList[-1]))
        for weName in eigenschaften:
            str = ['-']
            we = Wolke.DB.waffeneigenschaften[weName]
            if not we.text:
                continue
            str.append(we.name)
            str.append(": ")
            #Replace all line endings by space
            str.append(we.text.replace('\n', ' '))
            str.append('\n\n')
            strList.append("".join(str))
            weights.append(pdfMeister.getWeight(strList[-1]))

    def appendVorteile(strList, weights, category, vorteile):
        strList.append(pdfMeister.formatRuleCategory(category))
        weights.append(pdfMeister.getWeight(strList[-1]))
        for vor in vorteile:
            if vor in Wolke.DB.manöver:
                continue

            str = ['-']
            vorteil = Wolke.DB.vorteile[vor]
            if not vorteil.text:
                continue
            str.append(vorteil.name)
            str.append(": ")
            #Replace all line endings by space
            str.append(vorteil.text.replace('\n', ' '))
            str.append('\n\n')
            strList.append("".join(str))
            weights.append(pdfMeister.getWeight(strList[-1]))
    
    def appendManöver(strList, weights, category, manöverList):
        strList.append(pdfMeister.formatRuleCategory(category))
        weights.append(pdfMeister.getWeight(strList[-1]))
        count = 0
        for man in manöverList:
            manöver = Wolke.DB.manöver[man]
            if not Wolke.Char.voraussetzungenPrüfen(manöver.voraussetzungen):
                continue
            count += 1
            str = ['-']
            if manöver.name.endswith(" (M)") or manöver.name.endswith(" (L)"):
                str.append(manöver.name[:-4])
            else:
                str.append(manöver.name)
            if manöver.probe:
                str.append(" (")
                str.append(manöver.probe)
                str.append(")")
            str.append(": ")
            if manöver.gegenprobe:
                str.append("Gegenprobe: ")
                str.append(manöver.gegenprobe)
                str.append(". ")

            #Replace line endings without a full stop, colon or another line ending before by just a full stop
            text = re.sub('(?<![\.\n\:])\n', '. ', manöver.text)
            #Replace all the remaining line endings by space
            str.append(text.replace('\n', ' '))

            str.append('\n\n')
            strList.append("".join(str))
            weights.append(pdfMeister.getWeight(strList[-1]))
        if count == 0:
            strList.pop()
            weights.pop()

    def appendTalente(strList, weights, category, talente):
        strList.append(pdfMeister.formatRuleCategory(category))
        weights.append(pdfMeister.getWeight(strList[-1]))
        for tal in talente:
            str = ['-']
            talent = Wolke.DB.talente[tal]
            if not talent.text:
                continue
            str.append(talent.name)
            str.append(': ')

            text = talent.text
            
            #The page for uebernatuerliches already has most of the text information from vorbereitungszeit on, so remove it
            #Except for Ziel...
            match = re.search('^Ziel: (.*)', talent.text, re.MULTILINE)
            ziel = ""
            if match:
                ziel = match.group()
  
            index = text.find('Vorbereitungszeit')
            if index != -1:
                text = text[:index]
            #Some talents only specify Fertigkeiten in their text...
            index = text.find('Fertigkeiten')
            if index != -1:
                text = text[:index]

            text = text + ziel
            #Replace line endings without a full stop, colon or another line ending before by just a full stop
            text = re.sub('(?<![\.\n\:])\n', '. ', text)
            #Replace all the remaining line endings by space
            str.append(text.replace('\n', ' '))
            str.append('\n\n')
            strList.append("".join(str))
            weights.append(pdfMeister.getWeight(strList[-1]))

    def prepareRules(self):
        sortV = Wolke.Char.vorteile.copy()
        sortV = sorted(sortV, key=str.lower)

        allgemein = [el for el in sortV if Wolke.DB.vorteile[el].typ == 0]

        #Allgemein Vorteile with different levels contain the lower levels in the description, so remove them
        remove = set()
        for vort in allgemein:
            if vort.endswith(" II"):
                remove.add(vort[:-1])    
            elif vort.endswith(" III"):
                remove.add(vort[:-1])
            elif vort.endswith(" IV"):
                remove.add(vort[:-1] + "II")

        for vort in remove:
            if vort in allgemein:
                allgemein.remove(vort)
        
        profan = [el for el in sortV if Wolke.DB.vorteile[el].typ == 1]

        kampf = [el for el in sortV if (Wolke.DB.vorteile[el].typ < 4 and
                                           Wolke.DB.vorteile[el].typ >= 2)]

        ueber = [el for el in sortV if Wolke.DB.vorteile[el].typ >= 4]

        sortM = list(Wolke.DB.manöver.keys())
        sortM = sorted(sortM, key=str.lower)

        aktionen = [el for el in sortM if (Wolke.DB.manöver[el].typ == 5)]

        manövernah = [el for el in sortM if (Wolke.DB.manöver[el].typ == 0)]

        waffeneigenschaften = []
        for waffe in Wolke.Char.waffen:
            for el in waffe.eigenschaften:
                try:
                    we = Hilfsmethoden.GetWaffeneigenschaft(el, Wolke.DB)
                    if not we.name in waffeneigenschaften:
                        waffeneigenschaften.append(we.name)
                except WaffeneigenschaftException:
                    pass
        waffeneigenschaften = sorted(waffeneigenschaften, key=str.lower)

        manöverfern = []
        for waffe in Wolke.Char.waffen:
            if type(waffe) is Objekte.Fernkampfwaffe:
                manöverfern = [el for el in sortM if (Wolke.DB.manöver[el].typ == 1)]
                break
        manövermagisch = []
        if "Zauberer I" in Wolke.Char.vorteile or "Borbaradianische Repräsentation I" in Wolke.Char.vorteile:
            manövermagisch = [el for el in sortM if (Wolke.DB.manöver[el].typ == 2)]
        manöverkarmal = []
        if "Geweiht I" in Wolke.Char.vorteile:
            manöverkarmal = [el for el in sortM if (Wolke.DB.manöver[el].typ == 3)]
        manöversonstiges = [el for el in sortM if (Wolke.DB.manöver[el].typ == 4)]
            
        ueberTalente = set()
        for fer in Wolke.Char.übernatürlicheFertigkeiten:
            for tal in Wolke.Char.übernatürlicheFertigkeiten[fer].gekaufteTalente:
                ueberTalente.add(tal)
        ueberTalente = sorted(ueberTalente, key=str.lower)
        self.Rules = []
        self.RuleWeights = []

        if allgemein:
            pdfMeister.appendVorteile(self.Rules, self.RuleWeights, self.RuleCategories[0], allgemein)
        if profan:
            pdfMeister.appendVorteile(self.Rules, self.RuleWeights, self.RuleCategories[1], profan)
        if kampf:
            pdfMeister.appendVorteile(self.Rules, self.RuleWeights, self.RuleCategories[2], kampf)
        if aktionen:
            pdfMeister.appendManöver(self.Rules, self.RuleWeights, self.RuleCategories[3], aktionen)
        if waffeneigenschaften:
            pdfMeister.appendWaffeneigenschaften(self.Rules, self.RuleWeights, self.RuleCategories[4], waffeneigenschaften)
        if manövernah:
            pdfMeister.appendManöver(self.Rules, self.RuleWeights, self.RuleCategories[5], manövernah)
        if manöverfern:
            pdfMeister.appendManöver(self.Rules, self.RuleWeights, self.RuleCategories[6], manöverfern)
        if ueber:
            pdfMeister.appendVorteile(self.Rules, self.RuleWeights, self.RuleCategories[7], ueber)
        if manövermagisch:
            pdfMeister.appendManöver(self.Rules, self.RuleWeights, self.RuleCategories[8], manövermagisch)
        if manöverkarmal:
            pdfMeister.appendManöver(self.Rules, self.RuleWeights, self.RuleCategories[9], manöverkarmal)
        if ueberTalente:
            pdfMeister.appendTalente(self.Rules, self.RuleWeights, self.RuleCategories[10], ueberTalente)
        if manöversonstiges:
            pdfMeister.appendManöver(self.Rules, self.RuleWeights, self.RuleCategories[11], manöversonstiges)

    def writeRules(self, fields, start, roughLineCount):
        weights = 0
        endIndex = start
        while weights < roughLineCount and endIndex < len(self.RuleWeights):
            weights = weights + self.RuleWeights[endIndex]
            endIndex = endIndex + 1

        if endIndex <= start:
            return -1

        #Make sure to remove the leading new line from a category if its at the start of the page
        #Also make sure a category is never the last line on the page
        for category in self.RuleCategories:
            formatted = pdfMeister.formatRuleCategory(category)
            if self.Rules[start] == formatted:
                self.Rules[start] = pdfMeister.formatRuleCategory(category, firstLine=True)
            if self.Rules[endIndex-1] == formatted:
                endIndex = endIndex - 1

        #Remove the two trailing new lines from the last entry
        self.Rules[endIndex-1] = self.Rules[endIndex-1][:-2]

        fields['Regeln'] = ''.join(self.Rules[start:endIndex])

        if len(self.Rules) == endIndex:
            #append newlines to make the auto-fontsize about same as large as the other pages (kinda hack-ish...)
            #give it a tendency to be bigger than average by subtracting 10% of the line count
            lastPageMissingNewlines = roughLineCount - weights - int(0.1*roughLineCount)
            if lastPageMissingNewlines > 0:
                fields['Regeln'] += lastPageMissingNewlines*'\n'
            #return -1 to signal that we are done
            return -1
        return endIndex