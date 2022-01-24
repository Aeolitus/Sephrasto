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
from EventBus import EventBus
from CheatsheetGenerator import CheatsheetGenerator

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
        self.Talents = []
        self.Energie = ""
        self.CheatsheetGenerator = CheatsheetGenerator()

    def setCharakterbogen(self, charakterBogenInfo):
        self.CharakterBogen = charakterBogenInfo

    def pdfErstellen(self, filename, printRules, progressCallback):
        progressCallback(0)
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
        fields = {}
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

        # Plugins die felder filtern lassen
        fields = EventBus.applyFilter("pdf_export", fields)
        progressCallback(10)

        # PDF erstellen - Felder bleiben bearbeitbar
        Wolke.Fehlercode = -89
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
        allPages = [out_file]
        pdf.write_pdf(self.CharakterBogen.filePath, fields, out_file, False)
        progressCallback(20)

        Wolke.Fehlercode = -90
        extraPageAdded = False
        if self.UseExtraPage:
            pageCount = 0
            while len(self.ExtraVorts) > 0 or \
                     len(self.ExtraTalents) > 0 or \
                        len(self.ExtraUeber) > 0:
                pageCount += 1
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
                progressCallback(20 + min(35, 20 + 3*pageCount))
        progressCallback(35)

        #Entferne Seite 3, falls keine übernatürlichen Fertigkeiten
        if not ('Uebervorteil1' in fields) and \
           not ('Ueberfer1NA' in fields) and \
           not ('Uebertal1NA' in fields) and not extraPageAdded:
            Wolke.Fehlercode = -96
            handle, out_file = tempfile.mkstemp()
            os.close(handle)
            pdf.shrink(allPages[0], 1, self.CharakterBogen.seitenProfan, out_file)
            os.remove(allPages[0])
            allPages[0] = out_file
        progressCallback(40)

        Wolke.Fehlercode = -97
        if printRules:
            rules, ruleLineCounts = self.CheatsheetGenerator.prepareRules(self.Talents)
            startIndex = 0
            pageCount = 0

            rulesFields = {}
            while startIndex != -1:
                pageCount += 1
                rulesFields["Seite"] = pageCount
                str, startIndex = self.CheatsheetGenerator.writeRules(rules, ruleLineCounts, startIndex)
                rulesFields["Regeln1"] = str
                rulesFields["Regeln2"] = ""
                if startIndex != -1:
                    str, startIndex = self.CheatsheetGenerator.writeRules(rules, ruleLineCounts, startIndex)
                    rulesFields["Regeln2"] = str

                handle, out_file = tempfile.mkstemp()
                os.close(handle)
                pdf.write_pdf(self.RulesPage, rulesFields, out_file, False)
                allPages.append(out_file)
                progressCallback(min(70, 40 + 3*pageCount))
        progressCallback(70)

        Wolke.Fehlercode = -94
        allPages = EventBus.applyFilter("pdf_concat", allPages)
        progressCallback(75)

        pdf.concat(allPages, filename)
        progressCallback(90)

        Wolke.Fehlercode = -95
        for page in allPages:
            os.remove(page)
        progressCallback(95)

        EventBus.doAction("pdf_geschrieben", { "filename" : filename })
        progressCallback(100)

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

        self.Energie = ""
        if isZauberer:
            self.Energie = str(Wolke.Char.asp.wert + Wolke.Char.aspBasis + Wolke.Char.aspMod)
            if isGeweiht:
                self.Energie += " / "
        if isGeweiht:
            self.Energie += str(Wolke.Char.kap.wert + Wolke.Char.kapBasis + Wolke.Char.kapMod)
        fields['EN'] = self.Energie

        trueBE = max(Wolke.Char.be, 0)
        fields['DHm'] = max(Wolke.Char.dh - 2*trueBE, 1)
        fields['GSm'] = max(Wolke.Char.gs-trueBE, 1)
        fields['WSm'] = Wolke.Char.wsStern

        return fields

    def isLinkedToVorteil(self, vorteil):
        if vorteil.linkKategorie == 3:
            if vorteil.linkElement in Wolke.Char.vorteile:
                return True
            return self.isLinkedToVorteil(Wolke.DB.vorteile[vorteil.linkElement])          

        return False

    def pdfDritterBlock(self, fields):
        logging.debug("PDF Block 3")
        vorteile = [v for v in Wolke.Char.vorteile if not self.isLinkedToVorteil(Wolke.DB.vorteile[v])]
        vorteileAllgemein = []
        vorteileKampf = []
        vorteileUeber = []
        typeDict = {}

        vorteileMergeScript = Wolke.DB.einstellungen["CharsheetVorteileMergeScript"].toText()

        # Collect a list of Vorteils, where different levels of the same are
        # combined into one entry and split them into the three categories
        for vort in vorteile:
            name = self.CheatsheetGenerator.getLinkedName(Wolke.DB.vorteile[vort], forceKommentar=True)
            scriptVariables = { "char" : Wolke.Char, "name" : vort, "typ" : Wolke.DB.vorteile[vort].typ, "mergeTo" : 0 }
            exec(vorteileMergeScript, scriptVariables)
            if scriptVariables["mergeTo"] == 0:
                vorteileAllgemein.append(name)
            elif scriptVariables["mergeTo"] == 1:
                vorteileKampf.append(name)
            else:
                vorteileUeber.append(name)
            typeDict[name] = Wolke.DB.vorteile[vort].typ

        vorteileAllgemein = sorted(vorteileAllgemein, key = lambda v: (typeDict[v], name))
        vorteileKampf = sorted(vorteileKampf, key = lambda v: (typeDict[v], name))
        vorteileUeber = sorted(vorteileUeber, key = lambda v: (typeDict[v], name))
        tmpOverflow = []
        tmpUeberflow = []
        
        # Fill up categories that are not full with the overflow
        # We merge up to 3 vorteile together before we overflow to additional pages
        mergePerLineCount = 3

        if len(vorteileAllgemein) > self.CharakterBogen.maxVorteile * mergePerLineCount:
            tmpOverflow.extend(vorteileAllgemein[self.CharakterBogen.maxVorteile * mergePerLineCount:])
            vorteileAllgemein = vorteileAllgemein[:self.CharakterBogen.maxVorteile * mergePerLineCount]

        maxKampfvorteile = 16
        if len(vorteileKampf) > maxKampfvorteile * mergePerLineCount:
            tmpOverflow.extend(vorteileKampf[maxKampfvorteile * mergePerLineCount:])
            vorteileKampf = vorteileKampf[:maxKampfvorteile * mergePerLineCount]

        maxUebervorteile = 12
        if len(vorteileUeber) > maxUebervorteile * mergePerLineCount:
            tmpUeberflow.extend(vorteileUeber[maxUebervorteile * mergePerLineCount:])
            vorteileUeber = vorteileUeber[:maxUebervorteile * mergePerLineCount]
        counter = 0
        for i in range(len(vorteileAllgemein), self.CharakterBogen.maxVorteile * mergePerLineCount):
            if len(tmpOverflow) > counter:
                vorteileAllgemein.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(vorteileKampf), maxKampfvorteile * mergePerLineCount):
            if len(tmpOverflow) > counter:
                vorteileKampf.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(vorteileUeber), maxUebervorteile * mergePerLineCount):
            if len(tmpOverflow) > counter:
                vorteileUeber.append(tmpOverflow[counter])
                counter += 1
        tmptmp = tmpOverflow[counter:]
        for el in tmptmp:
            tmpUeberflow.append(el)

        # Fill fields
        for i in range(0, min(self.CharakterBogen.maxVorteile * mergePerLineCount, len(vorteileAllgemein))):
            field = 'Vorteil' + str((i % self.CharakterBogen.maxVorteile)+1)
            if not field in fields:
                fields[field] = vorteileAllgemein[i]
            else:
                fields[field] += " | " + vorteileAllgemein[i]
        for i in range(0, min(maxKampfvorteile * mergePerLineCount, len(vorteileKampf))):
            field = 'Kampfvorteil' + str((i % maxKampfvorteile)+1)
            if not field in fields:
                fields[field] = vorteileKampf[i]
            else:
                fields[field] += " | " + vorteileKampf[i]
        for i in range(0, min(maxUebervorteile * mergePerLineCount, len(vorteileUeber))):
            field = 'Uebervorteil' + str((i % maxUebervorteile)+1)
            if not field in fields:
                fields[field] = vorteileUeber[i]
            else:
                fields[field] += " | " + vorteileUeber[i]

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

            if ('Frei' + str(count)) in fields:
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
                talent = Wolke.DB.talente[el2]
                talStr += talent.getFullName(Wolke.Char).replace(fertigkeit.name + ": ", "")

                if el2 in fertigkeit.talentMods:
                    for condition,mod in sorted(fertigkeit.talentMods[el2].items()):
                        talStr += " " + (condition + " " if condition else "") + ("+" if mod >= 0 else "") + str(mod)

            #Append any talent mods of talents the character doesn't own in parentheses
            for talentName, talentMods in sorted(fertigkeit.talentMods.items()):
                if not talentName in talente:
                    talStr += ", (" + talentName
                    for condition,mod in sorted(talentMods.items()):
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
            fields[base + 'RS'] = el.getRSGesamtInt() + Wolke.Char.rsmod
            fields[base + 'BE'] = max(el.be - Wolke.Char.rüstungsgewöhnung, 0)
            fields[base + 'WS'] = int(el.getRSGesamtInt() + Wolke.Char.rsmod + Wolke.Char.ws)
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

            if not el.name and not el.anzeigename:
                fields[base + 'TP'] = ""
                fields[base + 'HA'] = ""
                fields[base + 'EI'] = ""
                fields[base + 'ATm'] = ""
                fields[base + 'VTm'] = ""
                fields[base + 'RW'] = ""
                fields[base + 'WM'] = ""
                fields[base + 'TPm'] = ""
            else:
                sg = ""
                if el.plus >= 0:
                    sg = "+"

                keinSchaden = el.W6 == 0 and el.plus == 0
                fields[base + 'TP'] = "-" if keinSchaden else str(el.W6) + "W6" + sg + str(el.plus)
                fields[base + 'HA'] = str(waffenwerte.Haerte)
                fields[base + 'EI'] = ", ".join(el.eigenschaften)

                fields[base + 'ATm'] = str(waffenwerte.AT)

                fields[base + 'VTm'] = str(waffenwerte.VT)
                vtVerboten = Wolke.DB.einstellungen["TalenteVTVerboten"].toTextList()
                if el.name in Wolke.DB.waffen:
                    waffe = Wolke.DB.waffen[el.name]
                    if waffe.talent in vtVerboten or waffe.name in vtVerboten:
                        fields[base + 'VTm'] = "-"

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
        countl = 1
        countr = 11
        for el in Wolke.Char.ausrüstung:
            if count % 2 != 0:
                index = countl
                countl += 1
            else:
                index = countr
                countr += 1

            fields['Ausruestung' + str(index)] = el
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
            fertsList.append(f)
        fertsList.sort(key = lambda x: (Wolke.DB.übernatürlicheFertigkeiten[x].printclass, x))

        countF = 1
        countT = 1
        for f in fertsList:
            fe = Wolke.Char.übernatürlicheFertigkeiten[f]

            if fe.addToPDF:
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

        talente = set()
        for fert in fertsList:
            for talent in Wolke.Char.übernatürlicheFertigkeiten[fert].gekaufteTalente:
                talente.add(talent)

        for t in talente:
            # Fill Talente
            talent = Wolke.DB.talente[t]
            tt = Talentbox.Talentbox()

            tt.na = talent.getFullName(Wolke.Char)
            if len(talent.fertigkeiten) == 1:
                tt.na = tt.na.replace(talent.fertigkeiten[0] + ": ", "")
            for el in talent.fertigkeiten:
                if not el in Wolke.Char.übernatürlicheFertigkeiten:
                    continue
                fert = Wolke.Char.übernatürlicheFertigkeiten[el]
                tt.pw = max(tt.pw, fert.probenwertTalent)

                if tt.groupFert is None:
                    tt.groupFert = fert
                elif not tt.groupFert.talenteGruppieren and fert.talenteGruppieren:
                    tt.groupFert = fert
                elif tt.groupFert.talenteGruppieren and fert.talenteGruppieren:
                    if tt.groupFert.probenwertTalent < fert.probenwertTalent:
                        tt.groupFert = fert

            res = re.findall('Vorbereitungszeit:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.vo = res[0].strip()
            res = re.findall('Reichweite:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.re = res[0].strip()
            res = re.findall('Wirkungsdauer:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.wd = res[0].strip()
            res = re.findall('Kosten:(.*?)\n', talent.text, re.UNICODE)
            if len(res) == 1:
                tt.ko = res[0].strip()

            self.Talents.append(tt)

        def sortTalents(tt):
            if tt.groupFert is None:
                return (0, "", tt.na)
            elif tt.groupFert.talenteGruppieren:
               return (tt.groupFert.printclass, tt.groupFert.name, tt.na)
            else:
               return (tt.groupFert.printclass, "", tt.na)

        self.Talents.sort(key = lambda tt: sortTalents(tt))

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