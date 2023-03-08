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
from PySide6 import QtWidgets, QtCore, QtGui
import copy

class PdfExporter(object):
    def __init__(self):
        self.CharakterBogen = None
        self.Energie = ""
        self.CheatsheetGenerator = CheatsheetGenerator()

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
        flatten = Wolke.Char.formularEditierbarkeit == 2
        allPages = [PdfSerializer.write_pdf(self.CharakterBogen.filePath, fields, None, flatten)]
        progressCallback(20)

        # Extraseiten
        extraPageAdded = False
        if self.CharakterBogen.extraÜberSeiten:
            extraPage = None
            if len(extraVorteile) > 0 or len(extraUeber) > 0 or len(extraTalente):
                extraPageAdded = True
                extraPage = PdfSerializer.shrink(self.CharakterBogen.filePath, self.CharakterBogen.überSeite, self.CharakterBogen.überSeite)

            pageCount = 0
            while len(extraVorteile) > 0 or len(extraUeber) > 0 or len(extraTalente) > 0:
                pageCount += 1
                fieldsNew = {}
                self.createExtra(fieldsNew, extraVorteile, extraUeber, extraTalente)
                fieldsNew = EventBus.applyFilter("pdf_export_extrapage", fieldsNew)
                allPages.append(PdfSerializer.write_pdf(extraPage, fieldsNew, None, flatten))
                
                progressCallback(min(35, 20 + 3*pageCount))

            if extraPage:
                os.remove(extraPage)
        progressCallback(35)

        #Entferne die Seite für Übernatürliches, falls keine übernatürlichen Fertigkeiten vorhanden sind
        if self.CharakterBogen.überSeite > 0 and \
           not ('Uebervorteil1' in fields) and \
           not ('Ueberfer1NA' in fields) and \
           not ('Uebertal1NA' in fields) and not extraPageAdded:
            shrinked = PdfSerializer.shrink(allPages[0], 1, self.CharakterBogen.überSeite-1)
            os.remove(allPages[0])
            allPages[0] = shrinked
        progressCallback(40)

        if printRules:
            rules = self.CheatsheetGenerator.generateRules()
            progressCallback(45)
            if len(rules) != 0:
                html = ""
                with open(self.CharakterBogen.regelanhangPfad, 'r', encoding="utf-8") as infile:
                    html = infile.read()
                    rules = self.CheatsheetGenerator.generateRules()
                    html = html.replace("{rules_content}", rules)
                    html = html.replace("{rules_font_size}", str(Wolke.Char.regelnGroesse))
                    html = html.replace("{sephrasto_dir}", "file:///" + os.getcwd().replace('\\', '/')) #should be done after content because it may use this macro
                rulesFile = PdfSerializer.convertHtmlToPdf(html, self.CharakterBogen.regelanhangPfad, self.CharakterBogen.getRegelanhangPageLayout())
                progressCallback(50)
                PdfSerializer.addText(rulesFile,
                                      "%Page/%EndPage",
                                      self.CharakterBogen.regelanhangSeitenzahlPosition,
                                      str(self.CharakterBogen.regelanhangSeitenzahlAbstand),
                                      "black", "Times-Roman", "12", rulesFile)
                progressCallback(60)
                # Add the background image separately with a pdftk "background" call - this way it will be shared by all pages to decrease file size
                if self.CharakterBogen.regelanhangHintergrundPfad:
                    allPages.append(PdfSerializer.addBackground(rulesFile, self.CharakterBogen.regelanhangHintergrundPfad))
                    os.remove(rulesFile)
                else:
                    allPages.append(rulesFile)

        progressCallback(70)

        allPages = self.stampImage(allPages)
        allPages = EventBus.applyFilter("pdf_concat", allPages)
        progressCallback(75)

        PdfSerializer.concat(allPages, filename)
        progressCallback(90)

        for page in allPages:
            os.remove(page)
        progressCallback(95)

        PdfSerializer.squeeze(filename, filename)

        EventBus.doAction("pdf_geschrieben", { "filepath" : filename, "filename" : filename }) # filename is deprecated, remove in future
        progressCallback(100)

        #Open PDF with default application:
        if Wolke.Settings['PDF-Open']:
            Hilfsmethoden.openFile(filename)

    def pdfErsterBlock(self, fields):
        logging.debug("PDF Block 1")
        fields['Name'] = Wolke.Char.name
        fields['Rasse'] = Wolke.Char.spezies
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

        fields['DH'] = Wolke.Char.dh

        if "Gefäß der Sterne" in Wolke.Char.vorteile:
            fields['ModGefaess'] = checked

        isZauberer = Wolke.Char.aspBasis + Wolke.Char.aspMod > 0
        isGeweiht = Wolke.Char.kapBasis + Wolke.Char.kapMod > 0
        if isZauberer:
            fields['AstralenergieBasis'] = Wolke.Char.aspBasis
            fields['Astralenergie'] = Wolke.Char.asp.wert + Wolke.Char.aspBasis + Wolke.Char.aspMod
            fields['ModAstralenergie'] = Wolke.Char.asp.wert
        else:
            fields['AstralenergieBasis'] = "-"
            fields['Astralenergie'] = "-"
            fields['ModAstralenergie'] = "-"

        if isGeweiht:
            fields['KarmaenergieBasis'] = Wolke.Char.kapBasis
            fields['Karmaenergie'] = Wolke.Char.kap.wert + Wolke.Char.kapBasis + Wolke.Char.kapMod
            fields['ModKarmaenergie'] = Wolke.Char.kap.wert
        else:
            fields['KarmaenergieBasis'] = "-"
            fields['Karmaenergie'] = "-"
            fields['ModKarmaenergie'] = "-"

        self.Energie = ""
        if isZauberer:
            self.Energie = str(Wolke.Char.asp.wert + Wolke.Char.aspBasis + Wolke.Char.aspMod)
            if isGeweiht:
                self.Energie += " / "
        if isGeweiht:
            self.Energie += str(Wolke.Char.kap.wert + Wolke.Char.kapBasis + Wolke.Char.kapMod)
        if not self.Energie:
            self.Energie = "-"

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

        if self.CharakterBogen.maxÜberVorteile > 0:
            ueberLen = min(self.CharakterBogen.maxÜberVorteile * self.CharakterBogen.maxÜberVorteileProFeld, len(vorteileUeber))
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
        if self.CharakterBogen.überVorteileZuKampf:
            vorteileKampf.extend(vorteileUeber)
            vorteileUeber = []


        # Move vorteile to the next category if there is overflow
        maxVort = self.CharakterBogen.maxVorteile * self.CharakterBogen.maxVorteileProFeld
        if len(vorteileAllgemein) > maxVort:
            vorteileKampf.extend(vorteileAllgemein[maxVort:])
            del vorteileAllgemein[maxVort:]

        maxVort = self.CharakterBogen.maxKampfVorteile * self.CharakterBogen.maxKampfVorteileProFeld
        if len(vorteileKampf) > maxVort:
            vorteileUeber.extend(vorteileKampf[maxVort:])
            del vorteileKampf[maxVort:]

        self.printVorteile(fields, vorteileAllgemein, vorteileKampf, vorteileUeber)
        # return uebervorteile - they need to go on extra page if any are left
        return vorteileUeber

    def printFertigkeiten(self, fields, fertigkeitenNames):
        count = 1
        höchsteKampffertigkeit = Wolke.Char.getHöchsteKampffertigkeit()
        for el in fertigkeitenNames:
            if el not in Wolke.Char.fertigkeiten:
                continue
            fertigkeit = Wolke.Char.fertigkeiten[el]

            base = "Fertigkeit" + str(count)
            fields[base + "NA"] = fertigkeit.name           
            if fertigkeit == höchsteKampffertigkeit:
                fields[base + "FA"] = 4
            else:
                fields[base + "FA"] = fertigkeit.steigerungsfaktor
            fields[base + "AT"] = \
                fertigkeit.attribute[0] + '/' + \
                fertigkeit.attribute[1] + '/' + \
                fertigkeit.attribute[2]

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

    def countMaxFertigkeiten(self):
        if self.CharakterBogen.überFertigkeitenZuProfan and len(Wolke.Char.übernatürlicheFertigkeiten) > 0:
            return self.CharakterBogen.maxFertigkeiten - min(len([fert for fert in Wolke.Char.übernatürlicheFertigkeiten.values() if fert.addToPDF]), self.CharakterBogen.maxÜberFertigkeiten)
        else:
            return self.CharakterBogen.maxFertigkeiten

    def pdfVierterBlock(self, fields):
        logging.debug("PDF Block 4")
        # Freie Fertigkeiten
        freieFertsTmp = copy.copy(Wolke.Char.freieFertigkeiten)

        # Usually we want to keep the same order as in Sephrasto, however,
        # compact the entries if there are too many  for the character sheet
        if len(freieFertsTmp) > self.CharakterBogen.maxFreie:
            freieFertsTmp = [f for f in freieFertsTmp if f.name]

        while len(freieFertsTmp) > self.CharakterBogen.maxFreie * self.CharakterBogen.maxFreieProFeld:
            niedrigste = None
            for el in freieFertsTmp:
                if niedrigste == None or el.wert < niedrigste.wert:
                    niedrigste = el
            freieFertsTmp.remove(niedrigste)
            logging.warning("Der Charakter hat zu viele Freie Fertigkeiten für den Charakterbogen. Ignoriere Fertigkeit mit niedrigstem Wert: " + niedrigste.name)

        freieFerts = CharakterPrintUtility.getFreieFertigkeitenNames(freieFertsTmp)
        cellIndex = PdfExporter.getCellIndex(len(freieFerts), self.CharakterBogen.maxFreie)
        for i in range(0, len(freieFerts)):
            field = 'Frei' + str(cellIndex[i]+1)
            if not field in fields:
                fields[field] = freieFerts[i]
            else:
                fields[field] += " | " + freieFerts[i]

        fertigkeiten = CharakterPrintUtility.getFertigkeiten(Wolke.Char)

        while len(fertigkeiten) > self.countMaxFertigkeiten():
            niedrigste = None
            for el in fertigkeiten:
                fertigkeit = Wolke.Char.fertigkeiten[el]
                if niedrigste == None or fertigkeit.probenwertTalent < niedrigste.probenwertTalent:
                    niedrigste = fertigkeit
            fertigkeiten.remove(niedrigste.name)
            logging.warning("Der Charakter hat zu viele Fertigkeiten für den Charakterbogen. Ignoriere Fertigkeit mit niedrigstem PWT: " + niedrigste.name)
        self.printFertigkeiten(fields, fertigkeiten)

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

                keinSchaden = el.würfel == 0 and el.plus == 0
                fields[base + 'TP'] = "-" if keinSchaden else str(el.würfel) + "W" + str(el.würfelSeiten) + sg + str(el.plus)
                fields[base + 'HA'] = str(waffenwerte.härte)
                fields[base + 'EI'] = ", ".join(el.eigenschaften)

                fields[base + 'ATm'] = str(waffenwerte.at)

                fields[base + 'VTm'] = str(waffenwerte.vt)
                vtVerboten = Wolke.DB.einstellungen["Waffen: Talente VT verboten"].toTextList()
                if el.name in Wolke.DB.waffen:
                    waffe = Wolke.DB.waffen[el.name]
                    if waffe.talent in vtVerboten or waffe.name in vtVerboten:
                        fields[base + 'VTm'] = "-"

                fields[base + 'RW'] = str(waffenwerte.rw)

                fields[base + 'WM'] = str(el.wm)
                if type(el) == Objekte.Fernkampfwaffe:
                    fields[base + 'WM'] += " / " + str(el.lz)

                sg = ""
                if waffenwerte.plus >= 0:
                    sg = "+"
                fields[base + 'TPm'] = "-" if keinSchaden else str(waffenwerte.würfel) + "W" + str(el.würfelSeiten) + sg + str(waffenwerte.plus)

        # Fill 20 Cells of Ausrüstung
        count = 1
        for el in Wolke.Char.ausrüstung:
            fields['Ausruestung' + str(count)] = el
            if count >= 20:
                break
            count += 1

    def printÜberFertigkeiten(self, fields, überFertigkeiten, fieldBase = 'Ueberfer', fieldStartIndex = 0):
        for i in range(0, min(self.CharakterBogen.maxÜberFertigkeiten, len(überFertigkeiten))):
            fe = Wolke.Char.übernatürlicheFertigkeiten[überFertigkeiten[i]]
            base = fieldBase + str(i + 1 + fieldStartIndex)
            fields[base + 'NA'] = fe.name
            fields[base + 'FA'] = fe.steigerungsfaktor
            fields[base + 'AT'] = fe.attribute[0] + '/' + \
                fe.attribute[1] + '/' + fe.attribute[2]
            fields[base + 'FW'] = fe.wert
            fields[base + 'PW'] = fe.probenwertTalent + fe.basiswertMod
            fields[base + 'PWT'] = "-"

            if fe.basiswertMod == 0:
                fields[base + 'BA'] = fe.basiswert
            else:
                fields[base + 'BA'] = str(fe.basiswert + fe.basiswertMod) + "*"

            fields[base + "TA"] = ", ".join([t.anzeigeName for t in CharakterPrintUtility.getTalente(Wolke.Char, fe, True)])

        del überFertigkeiten[:min(self.CharakterBogen.maxÜberFertigkeiten, len(überFertigkeiten))]

    def printÜberTalente(self, fields, überTalente):
        wdAbbreviations = Wolke.DB.einstellungen["Charsheet: Talent-Abkürzungen Wirkungsdauer"].toTextDict('\n', False)
        koAbbreviations = Wolke.DB.einstellungen["Charsheet: Talent-Abkürzungen Kosten"].toTextDict('\n', False)

        for i in range(0, min(self.CharakterBogen.maxÜberTalente, len(überTalente))):
            base = 'Uebertal' + str(i+1)
            fields[base + 'NA'] = überTalente[i].anzeigeName
            fields[base + 'SE'] = überTalente[i].se
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
        if not self.CharakterBogen.extraÜberSeiten:
            while len(überFertigkeiten) > self.CharakterBogen.maxÜberFertigkeiten:
                niedrigste = None
                for el in überFertigkeiten:
                    fertigkeit = Wolke.Char.übernatürlicheFertigkeiten[el]
                    if niedrigste == None or fertigkeit.probenwertTalent < niedrigste.probenwertTalent:
                        niedrigste = fertigkeit
                überFertigkeiten.remove(niedrigste.name)
                logging.warning("Der Charakter hat zu viele übernatürliche Fertigkeiten für den Charakterbogen. Ignoriere Fertigkeit mit niedrigstem PWT: " + niedrigste.name)

        if self.CharakterBogen.überFertigkeitenZuProfan:
            self.printÜberFertigkeiten(fields, überFertigkeiten, "Fertigkeit", self.countMaxFertigkeiten())
            return ([], [])
        self.printÜberFertigkeiten(fields, überFertigkeiten)

        überTalenteTmp = CharakterPrintUtility.getÜberTalente(Wolke.Char)
        if not self.CharakterBogen.extraÜberSeiten:
            while len(überTalenteTmp) > self.CharakterBogen.maxÜberTalente:
                niedrigste = None
                for el in überTalenteTmp:
                    if niedrigste == None or int(el.pw) < int(niedrigste.pw):
                        niedrigste = el
                überTalenteTmp.remove(niedrigste)
                logging.warning("Der Charakter hat zu viele übernatürliche Talente für den Charakterbogen. Ignoriere Talent mit niedrigstem PWT: " + niedrigste.na)

        überTalente = []

        # Insert fertigkeit names into talente
        lastGroup = None
        fertigkeitsTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen übernatürlich"].toTextList()
        for talent in überTalenteTmp:
            if lastGroup != talent.groupFert:
                if lastGroup is None or lastGroup.typ != talent.groupFert.typ or talent.groupFert.talenteGruppieren:
                    if lastGroup is not None:
                        tbEmpty = Talentbox.Talentbox()
                        tbEmpty.pw = ''
                        überTalente.append(tbEmpty)
                    
                    tb = Talentbox.Talentbox()
                    tb.pw = ''
                    tb.anzeigeName = talent.groupFert.name.upper()
                    if not talent.groupFert.talenteGruppieren and talent.groupFert.typ < len(fertigkeitsTypen):
                        tb.anzeigeName = fertigkeitsTypen[talent.groupFert.typ].upper()
                    überTalente.append(tb)
                lastGroup = talent.groupFert

            überTalente.append(talent)

        self.printÜberTalente(fields, überTalente)

        # return ueber fertigkeiten and talente - they need to go on extra page if any are left
        return (überFertigkeiten, überTalente) 


    def pdfSiebterBlock(self, fields):
        logging.debug("PDF Block 7")
        fields['ErfahGE'] = Wolke.Char.epGesamt
        fields['ErfahEI'] = Wolke.Char.epAusgegeben
        fields['ErfahVE'] = Wolke.Char.epGesamt - Wolke.Char.epAusgegeben

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
        fields['Aussehen'] = ((Wolke.Char.aussehen1 + "\n") if Wolke.Char.aussehen1 else "") + \
            ((Wolke.Char.aussehen2 + "\n") if Wolke.Char.aussehen2 else "") + \
            ((Wolke.Char.aussehen3 + "\n") if Wolke.Char.aussehen3 else "") + \
            ((Wolke.Char.aussehen4 + "\n") if Wolke.Char.aussehen4 else "") + \
            ((Wolke.Char.aussehen5 + "\n") if Wolke.Char.aussehen5 else "") + \
            ((Wolke.Char.aussehen6 + "\n") if Wolke.Char.aussehen6 else "")
        fields['Aussehen'] = fields['Aussehen'].rstrip()
        fields['Hintergrund0'] = Wolke.Char.hintergrund0
        fields['Hintergrund1'] = Wolke.Char.hintergrund1
        fields['Hintergrund2'] = Wolke.Char.hintergrund2
        fields['Hintergrund3'] = Wolke.Char.hintergrund3
        fields['Hintergrund4'] = Wolke.Char.hintergrund4
        fields['Hintergrund5'] = Wolke.Char.hintergrund5
        fields['Hintergrund6'] = Wolke.Char.hintergrund6
        fields['Hintergrund7'] = Wolke.Char.hintergrund7
        fields['Hintergrund8'] = Wolke.Char.hintergrund8
        fields['Hintergrund'] = ((Wolke.Char.hintergrund0 + "\n") if Wolke.Char.hintergrund0 else "") + \
            ((Wolke.Char.hintergrund1 + "\n") if Wolke.Char.hintergrund1 else "") + \
            ((Wolke.Char.hintergrund2 + "\n") if Wolke.Char.hintergrund2 else "") + \
            ((Wolke.Char.hintergrund3 + "\n") if Wolke.Char.hintergrund3 else "") + \
            ((Wolke.Char.hintergrund4 + "\n") if Wolke.Char.hintergrund4 else "") + \
            ((Wolke.Char.hintergrund5 + "\n") if Wolke.Char.hintergrund5 else "") + \
            ((Wolke.Char.hintergrund6 + "\n") if Wolke.Char.hintergrund6 else "") + \
            ((Wolke.Char.hintergrund7 + "\n") if Wolke.Char.hintergrund7 else "") + \
            ((Wolke.Char.hintergrund8 + "\n") if Wolke.Char.hintergrund8 else "")
        fields['Hintergrund'] = fields['Hintergrund'].rstrip()

        fields['Notiz'] = Wolke.Char.notiz or ""

    def createExtra(self, fields, überVorteile, überFertigkeiten, überTalente):
        self.printVorteile(fields, [], [], überVorteile)
        self.printÜberFertigkeiten(fields, überFertigkeiten)
        self.printÜberTalente(fields, überTalente)
        fields['EN'] = self.Energie

    def stampImage(self, pages):
        if len(self.CharakterBogen.bild) == 0 or not Wolke.Char.bild:
            return pages

        empty = PdfSerializer.createEmptyPage(self.CharakterBogen.getPageLayout())
        stampPages = []
        for i in range(len(self.CharakterBogen.bild)):
            if not self.CharakterBogen.hasImage(i):
                stampPages.append(empty)
                continue
            imagePdf = PdfSerializer.convertJpgToPdf(Wolke.Char.bild, self.CharakterBogen.getImageSize(i, [260, 340]), self.CharakterBogen.getImageOffset(i), self.CharakterBogen.getPageLayout())
            stampPages.append(imagePdf)

        # pdftk repeats the last page of the stamp pdf if its page count is lower - make sure its empty
        stampPages.append(empty)
            
        # make a single pdf file out of the stamp pages
        stampPdf = PdfSerializer.concat(stampPages)
        for page in stampPages:
            if os.path.isfile(page):
                os.remove(page)

        # overlay each page of the stamp pdf over the corresponding page of the character sheet
        result = PdfSerializer.multistamp(pages[0], stampPdf)
        os.remove(pages[0])
        os.remove(stampPdf)
        pages[0] = result

        return pages