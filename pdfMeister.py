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
        if not ('Uebervorteil1' in fields) and \
           not ('Ueberfer1NA' in fields) and \
           not ('Uebertal1NA' in fields) and not extraPageAdded:
            Wolke.Fehlercode = -96
            handle, out_file = tempfile.mkstemp()
            os.close(handle)
            pdf.shrink(allPages[0], 1, self.CharakterBogen.seitenProfan, out_file)
            os.remove(allPages[0])
            allPages[0] = out_file
        
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

        Wolke.Fehlercode = -94
        pdf.concat(allPages, filename)

        Wolke.Fehlercode = -95
        for page in allPages:
            os.remove(page)

        EventBus.doAction("pdf_geschrieben", { "filename" : filename })

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
        sortV = Wolke.Char.vorteile.copy()
        sortV = [v for v in sortV if not self.isLinkedToVorteil(Wolke.DB.vorteile[v])]
        typeDict = {}
        added = []
        removed = []
        # Collect a list of Vorteils, where different levels of the same are
        # combined into one entry and the type of Vorteil is preserved
        for vort in sortV:
            if vort in removed:
                continue
            if vort == "Minderpakt" and Wolke.Char.minderpakt is not None:
                removed.append(vort)
                mindername = "Minderpakt (" + Wolke.Char.minderpakt + ")"
                added.append(mindername)
                typeDict[mindername] = 0
                continue

            name = self.CheatsheetGenerator.getLinkedName(Wolke.DB.vorteile[vort], forceKommentar=True)
            removed.append(vort)
            added.append(name)

            if "Zauberer" in name or "Geweiht" in name or "Paktierer" in name:
                typeDict[name] = 4
            else:
                typeDict[name] = Wolke.DB.vorteile[vort].typ
            
        for el in removed:
            if el in sortV:
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
        # We merge up to 3 vorteile of together before we overflow to additional pages
        mergePerLineCount = 3

        if len(tmpVorts) > self.CharakterBogen.maxVorteile * mergePerLineCount:
            tmpOverflow.extend(tmpVorts[self.CharakterBogen.maxVorteile * mergePerLineCount:])
            tmpVorts = tmpVorts[:self.CharakterBogen.maxVorteile * mergePerLineCount]

        maxKampfvorteile = 16
        if len(tmpKampf) > maxKampfvorteile * mergePerLineCount:
            tmpOverflow.extend(tmpKampf[maxKampfvorteile * mergePerLineCount:])
            tmpKampf = tmpKampf[:maxKampfvorteile * mergePerLineCount]

        maxUebervorteile = 12
        if len(tmpUeber) > maxUebervorteile * mergePerLineCount:
            tmpUeberflow.extend(tmpUeber[maxUebervorteile * mergePerLineCount:])
            tmpUeber = tmpUeber[:maxUebervorteile * mergePerLineCount]
        counter = 0
        for i in range(len(tmpVorts), self.CharakterBogen.maxVorteile * mergePerLineCount):
            if len(tmpOverflow) > counter:
                tmpVorts.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(tmpKampf), maxKampfvorteile * mergePerLineCount):
            if len(tmpOverflow) > counter:
                tmpKampf.append(tmpOverflow[counter])
                counter += 1
        for i in range(len(tmpUeber), maxUebervorteile * mergePerLineCount):
            if len(tmpOverflow) > counter:
                tmpUeber.append(tmpOverflow[counter])
                counter += 1
        tmptmp = tmpOverflow[counter:]
        for el in tmptmp:
            tmpUeberflow.append(el)
        # Fill fields

        for i in range(0, min(self.CharakterBogen.maxVorteile * mergePerLineCount, len(tmpVorts))):
            field = 'Vorteil' + str((i % self.CharakterBogen.maxVorteile)+1)
            if not field in fields:
                fields[field] = tmpVorts[i]
            else:
                fields[field] += " | " + tmpVorts[i]
        for i in range(0, min(maxKampfvorteile * mergePerLineCount, len(tmpKampf))):
            field = 'Kampfvorteil' + str((i % maxKampfvorteile)+1)
            if not field in fields:
                fields[field] = tmpKampf[i]
            else:
                fields[field] += " | " + tmpKampf[i]
        for i in range(0, min(maxUebervorteile * mergePerLineCount, len(tmpUeber))):
            field = 'Uebervorteil' + str((i % maxUebervorteile)+1)
            if not field in fields:
                fields[field] = tmpUeber[i]
            else:
                fields[field] += " | " + tmpUeber[i]

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
            sg = ""
            if el.plus >= 0:
                sg = "+"

            keinSchaden = el.W6 == 0 and el.plus == 0
            
            fields[base + 'TP'] = "-" if keinSchaden else str(el.W6) + "W6" + sg + str(el.plus)
            fields[base + 'HA'] = str(waffenwerte.Haerte)
            fields[base + 'EI'] = ", ".join(el.eigenschaften)

            fields[base + 'ATm'] = str(waffenwerte.AT)

            vtErlaubt = not (type(el) == Objekte.Fernkampfwaffe or (el.name in Wolke.DB.waffen and Wolke.DB.waffen[el.name].talent == 'Lanzenreiten'))
            vtErlaubt = EventBus.applyFilter("waffe_vt_erlaubt", vtErlaubt, { "waffe" : el })
            if vtErlaubt:
                fields[base + 'VTm'] = str(waffenwerte.VT)
            else:
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
            
            # Fill Talente
            tals = sorted(fe.gekaufteTalente, key=lambda s: s.lower())
            for t in tals:
                talent = Wolke.DB.talente[t]
                tt = Talentbox.Talentbox()

                tt.na = talent.getFullName(Wolke.Char)
                if len(talent.fertigkeiten) == 1:
                    tt.na = tt.na.replace(f + ": ", "")
                tt.pw = fe.probenwertTalent

                res = re.findall('Vorbereitungszeit:(.*?)\n',
                                    talent.text,
                                    re.UNICODE)
                if len(res) == 1:
                    tt.vo = res[0].strip()
                    #fields[base + 'VO'] = res[0].strip()
                res = re.findall('Reichweite:(.*?)\n',
                                    talent.text,
                                    re.UNICODE)
                if len(res) == 1:
                    tt.re = res[0].strip()
                    #fields[base + 'RE'] = res[0].strip()
                res = re.findall('Wirkungsdauer:(.*?)\n',
                                    talent.text,
                                    re.UNICODE)
                if len(res) == 1:
                    tt.wd = res[0].strip()
                    #fields[base + 'WD'] = res[0].strip()
                res = re.findall('Kosten:(.*?)\n',
                                    talent.text,
                                    re.UNICODE)
                if len(res) == 1:
                    tt.ko = res[0].strip()
                    #fields[base + 'KO'] = res[0].strip()

                tt.pc = talent.printclass

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