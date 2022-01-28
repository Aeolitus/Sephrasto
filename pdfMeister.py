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
from CharakterPrintUtility import CharakterPrintUtility

CharakterbogenInfo = namedtuple('CharakterbogenInfo', 'filePath maxVorteile maxKampfVorteile maxÜberVorteile maxFreie maxFertigkeiten maxÜberFertigkeiten maxÜberTalente seitenProfan kurzbogenHack')

class pdfMeister(object):

    CharakterBogen = CharakterbogenInfo(filePath="Charakterbogen.pdf",
                                        maxVorteile = 8,
                                        maxKampfVorteile = 16,
                                        maxÜberVorteile = 12,
                                        maxFreie = 12,
                                        maxFertigkeiten = 2,
                                        maxÜberFertigkeiten = 12,
                                        maxÜberTalente = 30,
                                        seitenProfan = 2,
                                        kurzbogenHack=True)

    CharakterBogenLang = CharakterbogenInfo(filePath="Charakterbogen_lang.pdf",
                                        maxVorteile = 24,
                                        maxKampfVorteile = 16,
                                        maxÜberVorteile = 12,
                                        maxFreie = 28,
                                        maxFertigkeiten = 28,
                                        maxÜberFertigkeiten = 12,
                                        maxÜberTalente = 30,
                                        seitenProfan = 3,
                                        kurzbogenHack=False)

    def __init__(self):
        # Name des Charakterbogens, der verwendet wird (im gleichen Ordner)
        self.CharakterBogen = pdfMeister.CharakterBogen
        self.ExtraPage = "ExtraSpells.pdf"
        self.PrintRules = True
        self.RulesPage = "Regeln.pdf"
        self.Energie = ""
        self.CheatsheetGenerator = CheatsheetGenerator()
        self.MergePerLineCount = 3

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
        Wolke.Fehlercode = -81
        fields = {}
        Wolke.Fehlercode = -82
        self.pdfErsterBlock(fields)
        Wolke.Fehlercode = -83
        self.pdfZweiterBlock(fields)
        Wolke.Fehlercode = -84
        extraVorteile = self.pdfDritterBlock(fields)
        Wolke.Fehlercode = -85
        self.pdfVierterBlock(fields)
        Wolke.Fehlercode = -86
        self.pdfFünfterBlock(fields)
        Wolke.Fehlercode = -87
        (extraUeber, extraTalente) = self.pdfSechsterBlock(fields)
        Wolke.Fehlercode = -88
        self.pdfSiebterBlock(fields)

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

        # Extraseiten
        Wolke.Fehlercode = -91
        extraPageAdded = False
        if len(extraVorteile) > 0 or len(extraUeber) > 0 or len(extraTalente):
            if not os.path.isfile(self.ExtraPage):
                raise Exception() 
            extraPageAdded = True

        pageCount = 0
        while len(extraVorteile) > 0 or len(extraUeber) > 0 or len(extraTalente) > 0:
            pageCount += 1
            Wolke.Fehlercode = -92
            fieldsNew = {}
            self.createExtra(fieldsNew, extraVorteile, extraUeber, extraTalente)
            Wolke.Fehlercode = -93

            handle, out_file = tempfile.mkstemp()
            os.close(handle)
            allPages.append(out_file)
            pdf.write_pdf(self.ExtraPage, fieldsNew, out_file, False)
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
            rules, ruleLineCounts = self.CheatsheetGenerator.prepareRules()
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
        for i in range(0, min(8, len(Wolke.Char.eigenheiten))):
            fields['Eigen' + str(i+1)] = Wolke.Char.eigenheiten[i]

    def pdfZweiterBlock(self, fields):
        logging.debug("PDF Block 2")
        for key in Definitionen.Attribute:
            fields[key] = Wolke.Char.attribute[key].wert
            fields[key + '2'] = Wolke.Char.attribute[key].probenwert
            fields[key + '3'] = Wolke.Char.attribute[key].probenwert
        fields['WundschwelleBasis'] = Wolke.Char.wsBasis
        fields['Wundschwelle'] = Wolke.Char.ws
        fields['WS'] = Wolke.Char.ws

        checked = 'Yes'
        if "Unverwüstlich" in Wolke.Char.vorteile:
            fields['ModUnverwuestlich'] = checked

        fields['MagieresistenzBasis'] = Wolke.Char.mrBasis
        fields['Magieresistenz'] = Wolke.Char.mr
        if "Willensstark I" in Wolke.Char.vorteile:
            fields['ModWillensstark1'] = checked
        if "Willensstark II" in Wolke.Char.vorteile:
            fields['ModWillensstark2'] = checked
        if "Unbeugsamkeit" in Wolke.Char.vorteile:
            fields['ModUnbeugsam'] = checked

        fields['GeschwindigkeitBasis'] = Wolke.Char.gsBasis
        fields['Geschwindigkeit'] = Wolke.Char.gs
        if "Flink I" in Wolke.Char.vorteile:
            fields['ModFlink1'] = checked
        if "Flink II" in Wolke.Char.vorteile:
            fields['ModFlink2'] = checked

        fields['SchadensbonusBasis'] = Wolke.Char.schadensbonusBasis
        fields['Schadensbonus'] = Wolke.Char.schadensbonus

        fields['InitiativeBasis'] = Wolke.Char.iniBasis
        fields['Initiative'] = Wolke.Char.ini
        fields['INIm'] = Wolke.Char.ini
        if "Kampfreflexe" in Wolke.Char.vorteile:
            fields['ModKampfreflexe'] = checked

        if "Gefäß der Sterne" in Wolke.Char.vorteile:
            fields['ModGefaess'] = checked

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

        fields['DHm'] = Wolke.Char.dhStern
        fields['GSm'] = Wolke.Char.gsStern
        fields['WSm'] = Wolke.Char.wsStern

    def groupVorteile(self, vorteile):
        # Collect a list of Vorteile, where different levels of the same are
        # combined into one entry and then split them into the three categories
        vorteileAllgemein = []
        vorteileKampf = []
        vorteileUeber = []

        vorteileMergeScript = Wolke.DB.einstellungen["CharsheetVorteileMergeScript"].toText()

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

        # Sort them, non-alphabetical sorting due to grouping might confuse
        vorteileAllgemein.sort(key = str.lower)
        vorteileKampf.sort(key = str.lower)
        vorteileUeber.sort(key = str.lower)

        # Move vorteile to the next category if there is overflow
        maxVort = self.CharakterBogen.maxVorteile * self.MergePerLineCount
        if len(vorteileAllgemein) > maxVort:
            vorteileKampf.extend(vorteileAllgemein[maxVort:])
            del vorteileAllgemein[maxVort:]

        maxVort = self.CharakterBogen.maxKampfVorteile * self.MergePerLineCount
        if len(vorteileKampf) > maxVort:
            vorteileUeber.extend(vorteileKampf[maxVort:])
            del vorteileKampf[maxVort:]

        return (vorteileAllgemein, vorteileKampf, vorteileUeber)
        
    @staticmethod
    def getCellIndex(numElements, maxCells):
        # This method maps elements to cell indices. It is used to keep alphabetical order in case of overflow
        perCell = numElements // maxCells
        extraCounter = numElements % maxCells
        cellCounter = 1
        cell = 0
        cellIndex = [0]*numElements
        for i in range(0, numElements):
            cellIndex[i] = cell
            pc = perCell
            if extraCounter > 0:
                pc += 1
            if cellCounter < pc:
                cellCounter += 1
            else:
                cellCounter = 1
                cell += 1
                extraCounter -= 1
        return cellIndex

    def printVorteile(self, fields, vorteileAllgemein, vorteileKampf, vorteileUeber):
        # Fill fields
        cellIndex = pdfMeister.getCellIndex(len(vorteileAllgemein), self.CharakterBogen.maxVorteile)
        for i in range(0, len(vorteileAllgemein)):
            field = 'Vorteil' + str(cellIndex[i]+1)
            if not field in fields:
                fields[field] = vorteileAllgemein[i]
            else:
                fields[field] += " | " + vorteileAllgemein[i]

        cellIndex = pdfMeister.getCellIndex(len(vorteileKampf), self.CharakterBogen.maxKampfVorteile)
        for i in range(0, len(vorteileKampf)):
            field = 'Kampfvorteil' + str(cellIndex[i]+1)
            if not field in fields:
                fields[field] = vorteileKampf[i]
            else:
                fields[field] += " | " + vorteileKampf[i]

        ueberLen = min(self.CharakterBogen.maxÜberVorteile * self.MergePerLineCount, len(vorteileUeber))
        cellIndex = pdfMeister.getCellIndex(ueberLen, self.CharakterBogen.maxÜberVorteile)
        for i in range(0, ueberLen):
            field = 'Uebervorteil' + str(cellIndex[i]+1)
            if not field in fields:
                fields[field] = vorteileUeber[i]
            else:
                fields[field] += " | " + vorteileUeber[i]

        del vorteileUeber[:ueberLen]

    def pdfDritterBlock(self, fields):
        logging.debug("PDF Block 3")
        vorteile = CharakterPrintUtility.getVorteile(Wolke.Char)
        grouped = self.groupVorteile(vorteile)
        self.printVorteile(fields, grouped[0], grouped[1], grouped[2])
        # return uebervorteile - they need to go on extra page if any are left
        return grouped[2]

    def printFertigkeiten(self, fields, baseStr, fertigkeitenNames):
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
            fields[base + "TA"] = CharakterPrintUtility.getTalente(Wolke.Char, fertigkeit)
            fields[base + "PW"] = fertigkeit.probenwert
            fields[base + "PWT"] = fertigkeit.probenwertTalent
            count += 1
        fertigkeitenNames.clear()

    def pdfVierterBlock(self, fields):
        logging.debug("PDF Block 4")
        # Freie Fertigkeiten
        freieFerts = CharakterPrintUtility.getFreieFertigkeiten(Wolke.Char)
        count = 1
        for fert in freieFerts:
            if ('Frei' + str(count)) in fields:
                fields['Frei' + str(count)] += ", " + fert
            else:
                fields['Frei' + str(count)] = fert
            count += 1
            if count > self.CharakterBogen.maxFreie:
                count = 1

        fertigkeiten = CharakterPrintUtility.getFertigkeiten(Wolke.Char)
        if self.CharakterBogen.kurzbogenHack:
            standardFerts = ["Handgemenge", "Hiebwaffen", "Klingenwaffen", "Stangenwaffen",
                 "Schusswaffen", "Wurfwaffen", "Athletik", "Heimlichkeit", 
                 "Selbstbeherrschung", "Wahrnehmung", "Autorität", 
                 "Beeinflussung", "Gebräuche", "Derekunde", "Magiekunde", 
                 "Mythenkunde", "Überleben", "Alchemie", "Handwerk", 
                 "Heilkunde", "Verschlagenheit"]

            self.printFertigkeiten(fields, None, standardFerts)
            self.printFertigkeiten(fields, "Indi", [f for f in fertigkeiten if not f in standardFerts])
        else:
            self.printFertigkeiten(fields, "Fertigkeit", fertigkeiten)

    def pdfFünfterBlock(self, fields):
        logging.debug("PDF Block 5")
        # Fill three rows of Rüstung
        for i in range(0, min(3, len(Wolke.Char.rüstung))):
            el = Wolke.Char.rüstung[i]
            base = 'Ruest' + str(i+1)
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

        # Fill eight rows of weapons
        for i in range(0, min(8, len(Wolke.Char.waffen))):
            el = Wolke.Char.waffen[i]
            waffenwerte = Wolke.Char.waffenwerte[i]

            base = 'Waffe' + str(i+1)
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
                vtVerboten = Wolke.DB.einstellungen["WaffenTalenteVTVerboten"].toTextList()
                if el.name in Wolke.DB.waffen:
                    waffe = Wolke.DB.waffen[el.name]
                    if waffe.talent in vtVerboten or waffe.name in vtVerboten:
                        fields[base + 'VTm'] = "-"

                fields[base + 'RW'] = str(waffenwerte.RW)

                fields[base + 'WM'] = str(el.wm)
                if type(el) == Objekte.Fernkampfwaffe:
                    fields[base + 'WM'] += " / " + str(el.lz)

                sg = ""
                if waffenwerte.TPPlus >= 0:
                    sg = "+"
                fields[base + 'TPm'] = "-" if keinSchaden else str(waffenwerte.TPW6) + "W6" + sg + str(waffenwerte.TPPlus)

        # Fill 20 Cells of Ausrüstung. Have to shift around because sephrasto ui and pdf form are transposed.
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

    def printÜberFertigkeiten(self, fields, überFertigkeiten):
        for i in range(0, min(self.CharakterBogen.maxÜberFertigkeiten, len(überFertigkeiten))):
            fe = Wolke.Char.übernatürlicheFertigkeiten[überFertigkeiten[i]]
            base = 'Ueberfer' + str(i + 1)
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

        del überFertigkeiten[:min(self.CharakterBogen.maxÜberFertigkeiten, len(überFertigkeiten))]

    def printÜberTalente(self, fields, überTalente):
        wdAbbreviations = Wolke.DB.einstellungen["CharsheetTalentAbkürzungenWirkungsdauer"].toTextDict('\n', False)
        koAbbreviations = Wolke.DB.einstellungen["CharsheetTalentAbkürzungenKosten"].toTextDict('\n', False)

        for i in range(0, min(self.CharakterBogen.maxÜberTalente, len(überTalente))):
            base = 'Uebertal' + str(i+1)
            base2 = 'Ubertal' + str(i+1)
            fields[base + 'NA'] = überTalente[i].anzeigeName
            fields[base2 + 'SE'] = überTalente[i].se
            fields[base + 'PW'] = überTalente[i].pw
            fields[base + 'VO'] = überTalente[i].vo
            fields[base + 'WD'] = überTalente[i].wd
            for a in wdAbbreviations:
                fields[base + 'WD'] = fields[base + 'WD'].replace(a, wdAbbreviations[a])
            fields[base + 'KO'] = überTalente[i].ko
            for a in koAbbreviations:
                fields[base + 'KO'] = fields[base + 'KO'].replace(a, koAbbreviations[a])
            fields[base + 'RE'] = überTalente[i].re

        del überTalente[:min(self.CharakterBogen.maxÜberTalente, len(überTalente))]

    def pdfSechsterBlock(self, fields):
        logging.debug("PDF Block 6")

        überFertigkeiten = CharakterPrintUtility.getÜberFertigkeiten(Wolke.Char)
        self.printÜberFertigkeiten(fields, überFertigkeiten)

        überTalenteTmp = CharakterPrintUtility.getÜberTalente(Wolke.Char)
        überTalente = []

        # Insert fertigkeit names into talente
        lastGroup = None
        fertigkeitsTypen = Wolke.DB.einstellungen["FertigkeitsTypenÜbernatürlich"].toTextList()
        for talent in überTalenteTmp:
            if lastGroup != talent.groupFert:
                if lastGroup is None or lastGroup.printclass != talent.groupFert.printclass or talent.groupFert.talenteGruppieren:
                    if lastGroup is not None:
                        tbEmpty = Talentbox.Talentbox()
                        tbEmpty.pw = ''
                        überTalente.append(tbEmpty)
                    
                    tb = Talentbox.Talentbox()
                    tb.pw = ''
                    tb.anzeigeName = talent.groupFert.name.upper()
                    if not talent.groupFert.talenteGruppieren and talent.groupFert.printclass < len(fertigkeitsTypen):
                        tb.anzeigeName = fertigkeitsTypen[talent.groupFert.printclass].upper()
                    überTalente.append(tb)
                lastGroup = talent.groupFert

            überTalente.append(talent)

        self.printÜberTalente(fields, überTalente)

        # return ueber fertigkeiten and talente - they need to go on extra page if any are left
        return (überFertigkeiten, überTalente) 


    def pdfSiebterBlock(self, fields):
        logging.debug("PDF Block 7")
        fields['ErfahGE'] = Wolke.Char.EPtotal
        fields['ErfahEI'] = Wolke.Char.EPspent
        fields['ErfahVE'] = Wolke.Char.EPtotal - Wolke.Char.EPspent

    def createExtra(self, fields, überVorteile, überFertigkeiten, überTalente):
        self.printVorteile(fields, [], [], überVorteile)
        self.printÜberFertigkeiten(fields, überFertigkeiten)
        self.printÜberTalente(fields, überTalente)
        fields['EN'] = self.Energie