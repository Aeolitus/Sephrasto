# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:08:59 2017

@author: Lennart

This class exists to handle all the writing of the charactor to the pdf.
"""
from Wolke import Wolke
import PdfSerializer
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
from Core.Talent import Talent, TalentDefinition
from Core.Fertigkeit import Fertigkeit
from QtUtils.ProgressDialogExt import ProgressDialogExt

class PdfExporter(object):
    def __init__(self):
        self.CharakterBogen = None
        self.Energie = ""
        self.CheatsheetGenerator = CheatsheetGenerator()

    def setCharakterbogen(self, charakterbogen):
        self.CharakterBogen = charakterbogen

    def pdfErstellen(self, filename, printRules):
        dlg = ProgressDialogExt(minimum = 0, maximum = 100)
        dlg.setWindowTitle("Exportiere Charakter")
        dlg.setLabelText("Befülle Formularfelder")    
        dlg.show()
        QtWidgets.QApplication.processEvents() #make sure the dialog immediatelly shows

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

        # Mappings des Charakterbogens applizieren
        for field in self.CharakterBogen.formularMappings:
            if field in fields:
                if isinstance(self.CharakterBogen.formularMappings[field], list):
                    mappings = self.CharakterBogen.formularMappings[field]
                else:
                    mappings = [self.CharakterBogen.formularMappings[field]]

                for mapping in mappings:
                    fields[mapping] = fields[field]

        if dlg.shouldCancel():
            return
        dlg.setValue(10)


        # PDF erstellen
        flatten = not Wolke.Char.formularEditierbar
        bookmarks = []
        i = 0
        for i in range(PdfSerializer.getNumPages(self.CharakterBogen.filePath)):
            text = "Charakterbogen"
            if i < len(self.CharakterBogen.seitenbeschreibungen):
                text = self.CharakterBogen.seitenbeschreibungen[i]
            bookmarks.append(PdfSerializer.PdfBookmark("S. " + str(i+1) + " - " + text, i+1))
        i += 1

        allPages = [PdfSerializer.write_pdf(self.CharakterBogen.filePath, fields, None, flatten)]

        if dlg.shouldCancel():
            for page in allPages: os.remove(page)
            return
        dlg.setLabelText("Füge zusätzliche Seiten für Übernatürliches an")
        dlg.setValue(20)

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
                bookmarks.append(PdfSerializer.PdfBookmark("S. " + str(i+1) + " - " + text, i+1))
                i += 1
                if dlg.shouldCancel():
                    for page in allPages: os.remove(page)
                    os.remove(extraPage)
                    return
                dlg.setValue(min(30, 20 + 2*pageCount))

            if extraPage:
                os.remove(extraPage)

        #Entferne die Seite für Übernatürliches, falls keine übernatürlichen Fertigkeiten vorhanden sind
        if self.CharakterBogen.überSeite > 0 and \
           not ('Uebervorteil1' in fields) and \
           not ('Ueberfer1NA' in fields) and \
           not ('Uebertal1NA' in fields) and not extraPageAdded:
            if dlg.shouldCancel():
                for page in allPages: os.remove(page)
                return
            dlg.setValue(30)
            dlg.setLabelText("Charakter ist profan, entferne Seite für Übernatürliches")
            shrinked = PdfSerializer.shrink(allPages[0], 1, self.CharakterBogen.überSeite-1)
            os.remove(allPages[0])
            allPages[0] = shrinked
            if len(bookmarks) > 0:
                bookmarks.pop()
                i -= 1

        if printRules:
            if dlg.shouldCancel():
                for page in allPages: os.remove(page)
                return
            dlg.setLabelText("Erstelle Regelanhang")
            dlg.setValue(35)
            rules = self.CheatsheetGenerator.generateRules()
            if len(rules) != 0:
                dlg.setValue(40)
                html = ""
                with open(self.CharakterBogen.regelanhangPfad, 'r', encoding="utf-8") as infile:
                    html = infile.read()
                    html = html.replace("{sephrasto_dir}", "file:///" + os.getcwd().replace('\\', '/'))
                    html = html.replace("{rules_content}", rules)
                    html = html.replace("{rules_font_size}", str(Wolke.Char.regelnGroesse))
                rulesFile = PdfSerializer.convertHtmlToPdf(html, self.CharakterBogen.regelanhangPfad, self.CharakterBogen.getRegelanhangPageLayout(), 100)

                for j in range(1, PdfSerializer.getNumPages(rulesFile)+1):
                    bookmarks.append(PdfSerializer.PdfBookmark("S. " + str(i+1) + " - Regelanhang " + str(j), i+1))
                    i += 1

                if dlg.shouldCancel():
                    for page in allPages: os.remove(page)
                    os.remove(rulesFile)
                    return
                dlg.setValue(50)
                PdfSerializer.addText(rulesFile,
                                      "%Page/%EndPage",
                                      self.CharakterBogen.regelanhangSeitenzahlPosition,
                                      str(self.CharakterBogen.regelanhangSeitenzahlAbstand),
                                      "black", "Times-Roman", "10", rulesFile)
                dlg.setValue(52)
                PdfSerializer.addText(rulesFile,
                                      f"{Wolke.Char.name} ({Wolke.Char.epGesamt} EP)",
                                      self.CharakterBogen.regelanhangSeitenzahlPosition,
                                      str(self.CharakterBogen.regelanhangSeitenzahlAbstand-10),
                                      "black", "Times-Roman", "6", rulesFile)

                if dlg.shouldCancel():
                    for page in allPages: os.remove(page)
                    os.remove(rulesFile)
                    return
                dlg.setValue(55)
                # Add the background image separately with a pdftk "background" call - this way it will be shared by all pages to decrease file size
                if self.CharakterBogen.regelanhangHintergrundPfad:
                    allPages.append(PdfSerializer.addBackground(rulesFile, self.CharakterBogen.regelanhangHintergrundPfad))
                    os.remove(rulesFile)
                else:
                    allPages.append(rulesFile)

        if dlg.shouldCancel():
            for page in allPages: os.remove(page)
            return
        dlg.setLabelText("Stemple Charakterbild")
        dlg.setValue(60)
        allPages = self.stampImage(allPages)

        if dlg.shouldCancel():
            for page in allPages: os.remove(page)
            return
        dlg.setLabelText("Führe Plugins aus")
        dlg.setValue(70)
        allPages = EventBus.applyFilter("pdf_concat", allPages)

        if dlg.shouldCancel():
            for page in allPages: os.remove(page)
            return
        dlg.setLabelText("Füge PDF-Dateien zusammen")
        dlg.setValue(75)
        tmp = PdfSerializer.concat(allPages)

        dlg.setLabelText("Lösche temporäre Dateien")
        dlg.setValue(85)
        for page in allPages:
            os.remove(page)

        if dlg.shouldCancel():
            os.remove(tmp)
            return

        dlg.setLabelText("Füge Lesezeichen hinzu")
        dlg.setValue(90)
        PdfSerializer.addBookmarks(tmp, bookmarks, filename)
        os.remove(tmp)

        if dlg.shouldCancel():
            os.remove(filename)
            return
        dlg.setLabelText("Optimiere Dateigröße")
        dlg.setValue(95)
        PdfSerializer.squeeze(filename, filename)

        EventBus.doAction("pdf_geschrieben", { "filepath" : filename })
        dlg.setValue(100)

        dlg.hide()
        dlg.deleteLater()

        #Open PDF with default application:
        if Wolke.Settings['PDF-Open']:
            Hilfsmethoden.openFile(filename)

    def pdfErsterBlock(self, fields):
        logging.debug("PDF Block 1")
        fields['Name'] = Wolke.Char.name
        fields['Spezies'] = Wolke.Char.spezies
        fields['Kultur'] = Wolke.Char.heimat
        statusse = Wolke.DB.einstellungen["Statusse"].wert
        if Wolke.Char.status < len(statusse):
            fields['Status'] = statusse[Wolke.Char.status]
        finanzen = Wolke.DB.einstellungen["Finanzen"].wert
        if Wolke.Char.finanzen < len(finanzen):
            fields['Finanzen'] = finanzen[Wolke.Char.finanzen]
        fields['Kurzb'] = Wolke.Char.kurzbeschreibung
        # Erste Acht Eigenheiten
        for i in range(0, min(8, len(Wolke.Char.eigenheiten))):
            fields['Eigen' + str(i+1)] = Wolke.Char.eigenheiten[i]

    def pdfZweiterBlock(self, fields):
        logging.debug("PDF Block 2")
        for key in Wolke.Char.attribute:
            fields[key] = Wolke.Char.attribute[key].wert
            fields[key + 'PW'] = Wolke.Char.attribute[key].probenwert

        for aw in Wolke.Char.abgeleiteteWerte.values():
            fields[aw.name + "Basis"] = aw.basiswert
            fields[aw.name] = aw.wert
            fields[aw.name + "m"] = aw.finalwert

        if not Wolke.Char.finanzenAnzeigen and 'SchiPm' in fields:
            del fields['SchiPm']

        checked = 'Yes'
        for vort in Wolke.Char.vorteile:
            field = "Vorteil" + vort.replace(" ", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
            fields[field] = checked

        self.Energie = ""
        for en in Wolke.Char.energien.values():
            fields[en.name + 'Basis'] = en.basiswert
            fields[en.name] = en.gesamtwert
            fields['Mod' + en.name] = en.wert
            self.Energie += str(en.gesamtwert) + " / "

        if self.Energie:
            self.Energie = self.Energie[:-3]
        else:
            self.Energie = "-"

        for en in Wolke.DB.energien.values():
            if en.name in Wolke.Char.energien:
                continue
            fields[en.name + 'Basis'] = "-"
            fields[en.name] = "-"
            fields['Mod' + en.name] = "-"

        fields['EN'] = self.Energie

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
        höchsteKampffertigkeit = Fertigkeit.getHöchsteKampffertigkeit(Wolke.Char.fertigkeiten)
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
            fields[base + "TA"] = ", ".join(CharakterPrintUtility.getTalente(Wolke.Char, fertigkeit))
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
        scriptAPI = {}
        for ab in Wolke.Char.abgeleiteteWerte:
            scriptAPI['get' + ab + 'Basis'] = lambda ab=ab: Wolke.Char.abgeleiteteWerte[ab].basiswert
            scriptAPI['get' + ab] = lambda ab=ab: Wolke.Char.abgeleiteteWerte[ab].wert
            scriptAPI['get' + ab + 'Mod'] = lambda ab=ab: Wolke.Char.abgeleiteteWerte[ab].mod

        for i in range(0, min(3, len(Wolke.Char.rüstung))):
            el = Wolke.Char.rüstung[i]
            if not el.name and el.getRSGesamtInt() == 0:
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
                ws = 0
                rsmod = 0
                bemod = 0
                scriptAPI["rs"] = el.getRSGesamtInt()
                scriptAPI["be"] = el.be
                fields[base + 'NA'] = el.name
                fields[base + 'RS'] = eval(Wolke.DB.einstellungen["Rüstungen: RS Script"].wert, scriptAPI)
                fields[base + 'BE'] = eval(Wolke.DB.einstellungen["Rüstungen: BE Script"].wert, scriptAPI)
                fields[base + 'WS'] = eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, scriptAPI)

                base += 'RS'
                scriptAPI["rs"] = el.rs[0]
                fields[base + 'Bein'] = eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, scriptAPI)
                scriptAPI["rs"] = el.rs[1]
                fields[base + 'lArm'] = eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, scriptAPI)
                scriptAPI["rs"] = el.rs[2]
                fields[base + 'rArm'] = eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, scriptAPI)
                scriptAPI["rs"] = el.rs[3]
                fields[base + 'Bauch'] = eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, scriptAPI)
                scriptAPI["rs"] = el.rs[4]
                fields[base + 'Brust'] = eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, scriptAPI)
                scriptAPI["rs"] = el.rs[5]
                fields[base + 'Kopf'] = eval(Wolke.DB.einstellungen["Rüstungen: WSStern Script"].wert, scriptAPI)

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
                fields[base + 'RW'] = str(waffenwerte.rw)
                
                atVerboten = Wolke.DB.einstellungen["Waffen: Talente AT verboten"].wert
                if el.talent in atVerboten or el.name in atVerboten:
                    fields[base + 'RW'] = "-"
                    fields[base + 'ATm'] = "-"

                vtVerboten = Wolke.DB.einstellungen["Waffen: Talente VT verboten"].wert
                if el.talent in vtVerboten or el.name in vtVerboten:
                    fields[base + 'VTm'] = "-"

                fields[base + 'WM'] = str(el.wm)
                if el.fernkampf:
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

            fields[base + "TA"] = ", ".join(CharakterPrintUtility.getTalente(Wolke.Char, fe, True))

        del überFertigkeiten[:min(self.CharakterBogen.maxÜberFertigkeiten, len(überFertigkeiten))]

    def printÜberTalente(self, fields, überTalente):
        wdAbbreviations = Wolke.DB.einstellungen["Charsheet: Talent-Abkürzungen Wirkungsdauer"].wert
        koAbbreviations = Wolke.DB.einstellungen["Charsheet: Talent-Abkürzungen Kosten"].wert

        for i in range(0, min(self.CharakterBogen.maxÜberTalente, len(überTalente))):
            base = 'Uebertal' + str(i+1)
            fields[base + 'NA'] = überTalente[i].anzeigenameExt
            fields[base + 'SE'] = überTalente[i].referenz
            pw = überTalente[i].probenwert
            if pw != -1:
                fields[base + 'PW'] = str(pw)
            fields[base + 'VO'] = überTalente[i].vorbereitungszeit
            fields[base + 'WD'] = überTalente[i].wirkungsdauer
            for a in wdAbbreviations:
                fields[base + 'WD'] = fields[base + 'WD'].replace(a, wdAbbreviations[a])
            fields[base + 'KO'] = überTalente[i].energieKosten
            for a in koAbbreviations:
                fields[base + 'KO'] = fields[base + 'KO'].replace(a, koAbbreviations[a])
            fields[base + 'RE'] = überTalente[i].reichweite

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

        talenteByTyp = CharakterPrintUtility.getÜberTalente(Wolke.Char)
        überTalenteTmp = []
        for arr in talenteByTyp:
            überTalenteTmp.extend(arr)
        if not self.CharakterBogen.extraÜberSeiten:
            while len(überTalenteTmp) > self.CharakterBogen.maxÜberTalente:
                niedrigste = None
                for el in überTalenteTmp:
                    if niedrigste == None or int(el.probenwert) < int(niedrigste.probenwert):
                        niedrigste = el
                überTalenteTmp.remove(niedrigste)
                logging.warning("Der Charakter hat zu viele übernatürliche Talente für den Charakterbogen. Ignoriere Talent mit niedrigstem PWT: " + niedrigste.na)

        überTalente = []

        # Insert fertigkeit names into talente
        lastGroup = None
        fertigkeitsTypen = Wolke.DB.einstellungen["Fertigkeiten: Typen übernatürlich"].wert
        for talent in überTalenteTmp:
            hauptFert = talent.hauptfertigkeit
            if lastGroup != hauptFert:
                if lastGroup is None or lastGroup.typ != hauptFert.typ or hauptFert.talenteGruppieren:
                    if lastGroup is not None:
                        emptyDef = TalentDefinition()
                        emptyDef.finalize(Wolke.DB)
                        talEmpty = Talent(emptyDef, Wolke.Char)
                        überTalente.append(talEmpty)
                    
                    talHeaderDef = TalentDefinition()
                    talHeaderDef.name = hauptFert.name.upper()
                    if not hauptFert.talenteGruppieren:
                        talHeaderDef.name = hauptFert.typname(Wolke.DB).upper()
                    talHeaderDef.finalize(Wolke.DB)
                    talHeader = Talent(talHeaderDef, Wolke.Char)
                    überTalente.append(talHeader)
                lastGroup = hauptFert

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

        aussehenMerged = ""
        for i in range(6):
            fields['Aussehen' + str(i+1)] = Wolke.Char.aussehen[i]
            if Wolke.Char.aussehen[i]:
                aussehenMerged += Wolke.Char.aussehen[i] + "\n"
        fields['Aussehen'] = aussehenMerged.rstrip()

        hintergrundMerged = ""
        for i in range(9):
            fields['Hintergrund' + str(i)] = Wolke.Char.hintergrund[i]
            if Wolke.Char.hintergrund[i]:
                hintergrundMerged += Wolke.Char.hintergrund[i] + "\n"
        fields['Hintergrund'] = hintergrundMerged.rstrip()

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
            imagePdf = PdfSerializer.convertJpgToPdf(Wolke.Char.bild, self.CharakterBogen.getImageSize(i, Wolke.CharImageSize), self.CharakterBogen.getImageOffset(i), self.CharakterBogen.getPageLayout())
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