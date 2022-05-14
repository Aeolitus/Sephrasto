# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:08:59 2017

@author: Lennart

This class exists to handle all the writing of the charactor to the pdf.
"""
from Wolke import Wolke
import PdfSerializer
import Definitionen
import Objekte
import Talentbox
import subprocess
import os
import math
import logging
import tempfile
from Charakter import KampfstilMod
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import sys
import traceback
from EventBus import EventBus
from CheatsheetGenerator import CheatsheetGenerator
from CharakterPrintUtility import CharakterPrintUtility
import yaml
from shutil import which
import platform
from PyQt5 import QtWidgets, QtCore, QtGui
import copy

class PdfExporter(object):
    def __init__(self):
        self.CharakterBogen = None
        self.ExtraPage = os.path.join("Data", "ExtraSpells.pdf")
        self.PrintRules = True
        self.RulesPage = os.path.join("Data", "Regeln.pdf")
        self.Energie = ""
        self.CheatsheetGenerator = CheatsheetGenerator()
        self.MergePerLineCount = 3

    def setCharakterbogen(self, charakterbogen):
        self.CharakterBogen = charakterbogen

    def pdfErstellen(self, filename, printRules, progressCallback):
        progressCallback(0)
        '''
        This entire subblock is responsible for filling all the fields of the
        Charakterbogen. It has been broken down into seven subroutines for
        testing purposes,
        '''
        fields = {}
        self.pdfErsterBlock(fields)
        self.pdfZweiterBlock(fields)
        extraVorteile = self.pdfDritterBlock(fields)
        self.pdfVierterBlock(fields)
        self.pdfFünfterBlock(fields)
        (extraUeber, extraTalente) = self.pdfSechsterBlock(fields)
        self.pdfSiebterBlock(fields)
        self.pdfAchterBlock(fields)

        # Plugins die felder filtern lassen
        fields = EventBus.applyFilter("pdf_export", fields)
        progressCallback(10)

        # PDF erstellen - Felder bleiben bearbeitbar
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
        allPages = [out_file]
        PdfSerializer.write_pdf(self.CharakterBogen.filePath, fields, out_file, False)
        progressCallback(20)

        # Extraseiten
        extraPageAdded = False
        if len(extraVorteile) > 0 or len(extraUeber) > 0 or len(extraTalente):
            if not os.path.isfile(self.ExtraPage):
                raise Exception() 
            extraPageAdded = True

        pageCount = 0
        while len(extraVorteile) > 0 or len(extraUeber) > 0 or len(extraTalente) > 0:
            pageCount += 1
            fieldsNew = {}
            self.createExtra(fieldsNew, extraVorteile, extraUeber, extraTalente)
            fieldsNew = EventBus.applyFilter("pdf_export_extrapage", fieldsNew)
            handle, out_file = tempfile.mkstemp()
            os.close(handle)
            allPages.append(out_file)
            PdfSerializer.write_pdf(self.ExtraPage, fieldsNew, out_file, False)
            progressCallback(20 + min(35, 20 + 3*pageCount))
        progressCallback(35)

        #Entferne Seite 3, falls keine übernatürlichen Fertigkeiten
        if not ('Uebervorteil1' in fields) and \
           not ('Ueberfer1NA' in fields) and \
           not ('Uebertal1NA' in fields) and not extraPageAdded:
            handle, out_file = tempfile.mkstemp()
            os.close(handle)
            PdfSerializer.shrink(allPages[0], 1, self.CharakterBogen.seitenProfan, out_file)
            os.remove(allPages[0])
            allPages[0] = out_file
        progressCallback(40)

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
                PdfSerializer.write_pdf(self.RulesPage, rulesFields, out_file, False)
                allPages.append(out_file)
                progressCallback(min(70, 40 + 3*pageCount))
        progressCallback(70)

        allPages = self.concatImage(allPages)
        allPages = EventBus.applyFilter("pdf_concat", allPages)
        progressCallback(75)

        PdfSerializer.concat(allPages, filename)
        progressCallback(90)

        for page in allPages:
            os.remove(page)
        progressCallback(95)

        EventBus.doAction("pdf_geschrieben", { "filename" : filename })
        progressCallback(100)

        #Open PDF with default application:
        if Wolke.Settings['PDF-Open']:
            if sys.platform == "win32":
                os.startfile(filename, "open")
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filename])

    def pdfErsterBlock(self, fields):
        logging.debug("PDF Block 1")
        fields['Name'] = Wolke.Char.name
        fields['Rasse'] = Wolke.Char.rasse
        fields['Kultur'] = Wolke.Char.heimat
        fields['Statu'] = Definitionen.Statusse[Wolke.Char.status]
        fields['Finanzen'] = Definitionen.Finanzen[Wolke.Char.finanzen]
        fields['Kurzb'] = Wolke.Char.kurzbeschreibung
        fields['Schip'] = Wolke.Char.schipsMax
        if Wolke.Char.finanzenAnzeigen:
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
        cellIndex = PdfExporter.getCellIndex(len(vorteileAllgemein), self.CharakterBogen.maxVorteile)
        for i in range(0, len(vorteileAllgemein)):
            field = 'Vorteil' + str(cellIndex[i]+1)
            if not field in fields:
                fields[field] = vorteileAllgemein[i]
            else:
                fields[field] += " | " + vorteileAllgemein[i]

        cellIndex = PdfExporter.getCellIndex(len(vorteileKampf), self.CharakterBogen.maxKampfVorteile)
        for i in range(0, len(vorteileKampf)):
            field = 'Kampfvorteil' + str(cellIndex[i]+1)
            if not field in fields:
                fields[field] = vorteileKampf[i]
            else:
                fields[field] += " | " + vorteileKampf[i]

        ueberLen = min(self.CharakterBogen.maxÜberVorteile * self.MergePerLineCount, len(vorteileUeber))
        cellIndex = PdfExporter.getCellIndex(ueberLen, self.CharakterBogen.maxÜberVorteile)
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
        (vorteileAllgemein, vorteileKampf, vorteileUeber) = CharakterPrintUtility.groupVorteile(Wolke.Char, vorteile, link = True)

        # Move vorteile to the next category if there is overflow
        maxVort = self.CharakterBogen.maxVorteile * self.MergePerLineCount
        if len(vorteileAllgemein) > maxVort:
            vorteileKampf.extend(vorteileAllgemein[maxVort:])
            del vorteileAllgemein[maxVort:]

        maxVort = self.CharakterBogen.maxKampfVorteile * self.MergePerLineCount
        if len(vorteileKampf) > maxVort:
            vorteileUeber.extend(vorteileKampf[maxVort:])
            del vorteileKampf[maxVort:]

        self.printVorteile(fields, vorteileAllgemein, vorteileKampf, vorteileUeber)
        # return uebervorteile - they need to go on extra page if any are left
        return vorteileUeber

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
                fields[base + "BA"] = str(fertigkeit.basiswert + fertigkeit.basiswertMod) + "*"

            fields[base + "FW"] = fertigkeit.wert
            fields[base + "TA"] = ", ".join([t.anzeigeName for t in CharakterPrintUtility.getTalente(Wolke.Char, fertigkeit)])
            fields[base + "PW"] = fertigkeit.probenwert + fertigkeit.basiswertMod
            fields[base + "PWT"] = fertigkeit.probenwertTalent + fertigkeit.basiswertMod
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

            self.printFertigkeiten(fields, None, copy.copy(standardFerts))
            self.printFertigkeiten(fields, "Indi", [f for f in fertigkeiten if not f in standardFerts])
        else:
            self.printFertigkeiten(fields, "Fertigkeit", fertigkeiten)

    def pdfFünfterBlock(self, fields):
        logging.debug("PDF Block 5")
        # Fill three rows of Rüstung
        for i in range(0, min(3, len(Wolke.Char.rüstung))):
            el = Wolke.Char.rüstung[i]
            if not el.name:
                base = 'Ruest' + str(i+1)
                fields[base + 'NA'] = ""
                fields[base + 'RS'] = ""
                fields[base + 'BE'] = ""
                fields[base + 'WS'] = ""
                base += 'RS'
                fields[base + 'Bein'] = ""
                fields[base + 'lArm'] = ""
                fields[base + 'rArm'] = ""
                fields[base + 'Bauch'] = ""
                fields[base + 'Brust'] = ""
                fields[base + 'Kopf'] = ""
            else:
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
                vtVerboten = Wolke.DB.einstellungen["Waffen: Talente VT verboten"].toTextList()
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
            fields[base + 'PW'] = fe.probenwertTalent + fe.basiswertMod

            if fe.basiswertMod == 0:
                fields[base + 'BA'] = fe.basiswert
            else:
                fields[base + 'BA'] = str(fe.basiswert + fe.basiswertMod) + "*"

        del überFertigkeiten[:min(self.CharakterBogen.maxÜberFertigkeiten, len(überFertigkeiten))]

    def printÜberTalente(self, fields, überTalente):
        wdAbbreviations = Wolke.DB.einstellungen["Charsheet: Talent-Abkürzungen Wirkungsdauer"].toTextDict('\n', False)
        koAbbreviations = Wolke.DB.einstellungen["Charsheet: Talent-Abkürzungen Kosten"].toTextDict('\n', False)

        for i in range(0, min(self.CharakterBogen.maxÜberTalente, len(überTalente))):
            base = 'Uebertal' + str(i+1)

            # need to fix both charsheets and extraspells to get rid of this hack...
            fieldSeite = 'Ubertal' + str(i+1) + 'SE'
            if i > 24:
                fieldSeite = "Ueberfer" + str(i+1) + 'FA'
            fields[base + 'NA'] = überTalente[i].anzeigeName
            fields[fieldSeite] = überTalente[i].se
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
        fertigkeitsTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen übernatürlich"].toTextList()
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

    def pdfAchterBlock(self, fields):
        if Wolke.Char.kultur:
            fields['Kultur'] = Wolke.Char.kultur

        fields['Profession'] = Wolke.Char.profession
        fields['Geschlecht'] = Wolke.Char.geschlecht
        fields['Geburtsdatum'] = Wolke.Char.geburtsdatum
        fields['Groesse'] = Wolke.Char.groesse
        fields['Gewicht'] = Wolke.Char.gewicht
        fields['Haarfarbe'] = Wolke.Char.haarfarbe
        fields['Augenfarbe'] = Wolke.Char.augenfarbe
        fields['Titel'] = Wolke.Char.titel

        fields['Aussehen1'] = Wolke.Char.aussehen1
        fields['Aussehen2'] = Wolke.Char.aussehen2
        fields['Aussehen3'] = Wolke.Char.aussehen3
        fields['Aussehen4'] = Wolke.Char.aussehen4
        fields['Aussehen5'] = Wolke.Char.aussehen5
        fields['Aussehen6'] = Wolke.Char.aussehen6
        
        fields['Hintergrund0'] = Wolke.Char.hintergrund0
        fields['Hintergrund1'] = Wolke.Char.hintergrund1
        fields['Hintergrund2'] = Wolke.Char.hintergrund2
        fields['Hintergrund3'] = Wolke.Char.hintergrund3
        fields['Hintergrund4'] = Wolke.Char.hintergrund4
        fields['Hintergrund5'] = Wolke.Char.hintergrund5
        fields['Hintergrund6'] = Wolke.Char.hintergrund6
        fields['Hintergrund7'] = Wolke.Char.hintergrund7
        fields['Hintergrund8'] = Wolke.Char.hintergrund8

    def createExtra(self, fields, überVorteile, überFertigkeiten, überTalente):
        self.printVorteile(fields, [], [], überVorteile)
        self.printÜberFertigkeiten(fields, überFertigkeiten)
        self.printÜberTalente(fields, überTalente)
        fields['EN'] = self.Energie

    def concatImage(self, pages):
        if not self.CharakterBogen.bild or not Wolke.Char.bild:
            return pages

        if platform.system() != 'Windows' and which("convert") is None:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Kann Charakterbild nicht einfügen")
            messagebox.setText("Das Einfügen des Charakterbilds benötigt das Programm 'convert' im Systempfad. Installationsdetails gibt es unter https://imagemagick.org. Der Charakterbogen wird nun ohne das Bild erstellt.")
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec_()
            return pages

        # The approach is to convert the image to pdf and stamp it over the char sheet with pdftk

        handle, image_file = tempfile.mkstemp()
        os.close(handle)
        characterImage = QtGui.QPixmap()
        characterImage.loadFromData(Wolke.Char.bild)
        characterImage.save(image_file, "JPG")

        handle, image_pdf = tempfile.mkstemp()
        os.close(handle)
        os.remove(image_pdf) # just using it to get a path
        image_pdf += ".pdf"

        handle, page1_pdf = tempfile.mkstemp()
        os.close(handle)

        handle, page1stamped_pdf = tempfile.mkstemp()
        os.close(handle)

        handle, pageRest_pdf = tempfile.mkstemp()
        os.close(handle)

        # pdftk stamps over every single page. We only want to stamp the first, so we need to split the char sheet first
        PdfSerializer.check_output_silent(['pdftk', pages[0], "cat", "1", "output", page1_pdf])
        PdfSerializer.check_output_silent(['pdftk', pages[0], "cat", "2-end", "output", pageRest_pdf])

        # Setting page size to a2 so stamping has to reduce size - this way we can use a higher image resolution.
        # The numbers after the page size are offsets from bottom and right to fit the image in the right spot
        # Density (dpi) has to be fixed, otherwise page offsets break
        # gravity + extent adds letterboxes to the image if needed, this keeps the image centered and allows to use fixed page offsets
        convertPath = "convert"
        if platform.system() == 'Windows':
            convertPath = "Bin\\ImageMagick\\convert"

        try:
            PdfSerializer.check_output_silent([convertPath, image_file, "-resize", "260x340", "-gravity", "Center", "-extent", "260x340", "-density", "96",
                                     "-page", f"a2+{self.CharakterBogen.bildOffset[0]}+{self.CharakterBogen.bildOffset[1]}", image_pdf])
            PdfSerializer.check_output_silent(['pdftk', page1_pdf, 'stamp', image_pdf, 'output', page1stamped_pdf, 'need_appearances'])

            os.remove(pages[0])
            os.remove(image_file)
            os.remove(image_pdf)
            os.remove(page1_pdf)
            pages[0] = page1stamped_pdf
            pages.insert(1, pageRest_pdf)
        except Exception as e:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Kann Charakterbild nicht einfügen")
            text = "Das Einfügen des Charakterbilds ist fehlgeschlagen: " + str(e) + "."
            if platform.system() == 'Linux':
                text += "\nUnter Linux gibt es ein bekanntes Problem mit ImageMagick, siehe https://github.com/Aeolitus/Sephrasto/blob/master/README.md für einen Workaround."
            text += "\nDer Charakterbogen wird nun ohne das Bild erstellt."
            messagebox.setText(text)
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec_()
            return pages


        return pages