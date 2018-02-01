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
from shutil import copyfile

class pdfMeister(object):

    def __init__(self):
        # Name des Charakterbogens, der verwendet wird (im gleichen Ordner)
        self.CharakterBogen = "Charakterbogen.pdf"
        self.ExtraPage = "ExtraSpells.pdf"
        self.UseExtraPage = False
        self.ExtraVorts = []
        self.ExtraUeber = []
        self.ExtraTalents = []
        self.Talents = {}
        self.Energie = 0
    
    def pdfErstellen(self, filename):
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
        self.Talents = {}
        self.UseExtraPage = False
        Wolke.Fehlercode = -81
        fields = pdf.get_fields(self.CharakterBogen)
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
        # PDF erstellen - Felder bleiben bearbeitbar
        Wolke.Fehlercode = -89
        pdf.write_pdf(self.CharakterBogen, fields, filename, False)
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
                pdf.write_pdf(self.ExtraPage, fieldsNew, 'temp_ex_page_feel_free_to_remove.pdf', False)
                Wolke.Fehlercode = -94
                call = 'pdftk ' + filename + ' temp_ex_page_feel_free_to_remove.pdf cat output \
temp_full_cb_feel_free_to_remove.pdf'                
                check_output(call)
                Wolke.Fehlercode = -95
                os.remove(filename)
                os.remove('temp_ex_page_feel_free_to_remove.pdf')
                os.rename('temp_full_cb_feel_free_to_remove.pdf', filename)
                del self.ExtraVorts[0:12]
                del self.ExtraUeber[0:12]
                del self.ExtraTalents[0:30]
        
        if fields['Uebervorteil1'] == '' and \
           fields['Ueberfer1NA'] == '' and \
           fields['Uebertal1NA'] == '' and not extraPageAdded:
            Wolke.Fehlercode = -96
            copyfile(filename, 'temp_copy_feel_free_to_remove.pdf')
            call = 'pdftk temp_copy_feel_free_to_remove.pdf cat 1-2 output ' + filename
            check_output(call)
            os.remove('temp_copy_feel_free_to_remove.pdf')
        Wolke.Fehlercode = 0

    def pdfErsterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 1")
        fields['Name'] = Wolke.Char.name
        fields['Rasse'] = Wolke.Char.rasse
        fields['Statu'] = Definitionen.Statusse[Wolke.Char.status]
        fields['Kurzb'] = Wolke.Char.kurzbeschreibung
        glMod = 0
        if "Glück I" in Wolke.Char.vorteile:
            glMod += 1
        if "Glück II" in Wolke.Char.vorteile:
            glMod += 1
        fields['Schip'] = 4 + glMod
        fields['Schipm'] = Wolke.Char.schips + glMod
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
        if Wolke.Debug:
            print("PDF Block 2")
        for key in Definitionen.Attribute:
            fields[key] = Wolke.Char.attribute[key].wert
            fields[key + '2'] = Wolke.Char.attribute[key].probenwert
            fields[key + '3'] = Wolke.Char.attribute[key].probenwert
        fields['Wundschwelle'] = Wolke.Char.ws
        fields['WS'] = Wolke.Char.ws
        fields['Magieresistenz'] = Wolke.Char.mr
        fields['Geschwindigkeit'] = Wolke.Char.gs
        fields['Schadensbonus'] = Wolke.Char.schadensbonus
        fields['Initiative'] = Wolke.Char.ini
        fields['INIm'] = Wolke.Char.ini
        aspMod = 0
        if "Zauberer I" in Wolke.Char.vorteile:
            aspMod += 8
        if "Zauberer II" in Wolke.Char.vorteile:
            aspMod += 8
        if "Zauberer III" in Wolke.Char.vorteile:
            aspMod += 8
        if "Zauberer IV" in Wolke.Char.vorteile:
            aspMod += 8
        if "Gefäß der Sterne" in Wolke.Char.vorteile:
            aspMod += Wolke.Char.attribute['CH'].wert+4
        if aspMod > 0:
            fields['Astralenergie'] = Wolke.Char.asp.wert + aspMod
        kapMod = 0
        if "Geweiht I" in Wolke.Char.vorteile:
            kapMod += 8
        if "Geweiht II" in Wolke.Char.vorteile:
            kapMod += 8
        if "Geweiht III" in Wolke.Char.vorteile:
            kapMod += 8
        if "Geweiht IV" in Wolke.Char.vorteile:
            kapMod += 8
        if kapMod > 0:
            fields['Karmaenergie'] = Wolke.Char.kap.wert + kapMod
        if aspMod > 0 and kapMod == 0:
            self.Energie = Wolke.Char.asp.wert + aspMod
            fields['EN'] = self.Energie
            #fields['gEN'] = "0"
        elif aspMod == 0 and kapMod > 0:
            self.Energie = Wolke.Char.kap.wert + kapMod
            fields['EN'] = self.Energie
            #fields['gEN'] = "0"
        # Wenn sowohl AsP als auch KaP vorhanden sind, muss der Spieler ran..
        trueBE = max(Wolke.Char.be, 0)
        fields['DHm'] = max(Wolke.Char.dh - 2*trueBE, 1)
        fields['GSm'] = max(Wolke.Char.gs-trueBE, 1)
        wsmod = Wolke.Char.rsmod + Wolke.Char.ws
        if len(Wolke.Char.rüstung) > 0:
            wsmod += int(sum(Wolke.Char.rüstung[0].rs)/6+0.5+0.0001)
        fields['WSm'] = wsmod

        return fields

    def pdfDritterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 3")
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
                nname = el + " (" + str(Wolke.Char.vorteileVariable[el]) + \
                    " EP)"
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
        if len(tmpVorts) > 8:
            tmpOverflow.extend(tmpVorts[8:])
            tmpVorts = tmpVorts[:8]
        if len(tmpKampf) > 16:
            tmpOverflow.extend(tmpKampf[16:])
            tmpKampf = tmpKampf[:16]
        if len(tmpUeber) > 12:
            tmpUeberflow.extend(tmpUeber[12:])
            tmpUeber = tmpUeber[:12]
        counter = 0
        for i in range(len(tmpVorts), 8):
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
        for i in range(1, 9):
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
        if Wolke.Debug:
            print("PDF Block 4")
        # Freie Fertigkeiten
        count = 1
        for el in Wolke.Char.freieFertigkeiten:
            if el.wert < 1 or el.wert > 3:
                continue
            resp = el.name + " "
            for i in range(el.wert):
                resp += "I"
            fields['Frei' + str(count)] = resp
            count += 1
            if count > 12:
                break

        # Standardfertigkeiten
        for el in Definitionen.StandardFerts:
            if el not in Wolke.Char.fertigkeiten:
                continue
            base = el[0:5]
            # Fix Umlaute
            if el == "Gebräuche":
                base = "Gebra"
            elif el == "Überleben":
                base = "Ueber"
            fields[base + "BA"] = Wolke.Char.fertigkeiten[el].basiswert
            fields[base + "FW"] = Wolke.Char.fertigkeiten[el].wert
            talStr = ""
            for el2 in Wolke.Char.fertigkeiten[el].gekaufteTalente:
                talStr += ", "
                if el2.startswith("Gebräuche: "):
                    talStr += el2[11:]
                elif el2.startswith("Mythen: "):
                    talStr += el2[8:]
                elif el2.startswith("Überleben: "):
                    talStr += el2[11:]
                else:
                    talStr += el2
                if el2 in Wolke.Char.talenteVariable:
                    talStr += " (" + str(Wolke.Char.talenteVariable[el2]) + \
                                 " EP)"
            talStr = talStr[2:]
            fields[base + "TA"] = talStr
            fields[base + "PW"] = Wolke.Char.fertigkeiten[el].probenwert
            fields[base + "PWT"] = Wolke.Char.fertigkeiten[el].probenwertTalent

        # Nonstandard Ferts
        count = 1
        for el in Wolke.Char.fertigkeiten:
            if el in Definitionen.StandardFerts:
                continue
            if count > 2:
                continue
            fields['Indi' + str(count) + 'NA'] = \
                Wolke.Char.fertigkeiten[el].name
            fields['Indi' + str(count) + 'FA'] = \
                Wolke.Char.fertigkeiten[el].steigerungsfaktor
            fields['Indi' + str(count) + 'AT'] = \
                Wolke.Char.fertigkeiten[el].attribute[0] + '/' + \
                Wolke.Char.fertigkeiten[el].attribute[1] + '/' + \
                Wolke.Char.fertigkeiten[el].attribute[2]
            fields['Indi' + str(count) + 'BA'] = \
                Wolke.Char.fertigkeiten[el].basiswert
            fields['Indi' + str(count) + 'FW'] = \
                Wolke.Char.fertigkeiten[el].wert
            fields['Indi' + str(count) + 'PW'] = \
                Wolke.Char.fertigkeiten[el].probenwert
            fields['Indi' + str(count) + 'PWT'] = \
                Wolke.Char.fertigkeiten[el].probenwertTalent
            talStr = ""
            for el2 in Wolke.Char.fertigkeiten[el].gekaufteTalente:
                talStr += ", "
                talStr += el2
                if el2 in Wolke.Char.talenteVariable:
                    talStr += " (" + str(Wolke.Char.talenteVariable[el2]) + \
                                 " EP)"
            talStr = talStr[2:]
            fields['Indi' + str(count) + 'TA'] = talStr
            count += 1
        return fields

    def pdfFünfterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 5")
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
            fields[base + 'Bein'] = el.rs[0]+Wolke.Char.rsmod
            fields[base + 'lArm'] = el.rs[1]+Wolke.Char.rsmod
            fields[base + 'rArm'] = el.rs[2]+Wolke.Char.rsmod
            fields[base + 'Bauch'] = el.rs[3]+Wolke.Char.rsmod
            fields[base + 'Brust'] = el.rs[4]+Wolke.Char.rsmod
            fields[base + 'Kopf'] = el.rs[5]+Wolke.Char.rsmod
            count += 1
            if count > 3:
                break

        # Fill eight rows of weapons
        count = 1
        for el in Wolke.Char.waffen:
            base = 'Waffe' + str(count)
            fields[base + 'NA'] = el.name
            sg = ""
            if el.plus >= 0:
                sg = "+"
            fields[base + 'TP'] = str(el.W6) + "W6" + sg + str(el.plus)
            fields[base + 'HA'] = str(el.haerte)
            fields[base + 'EI'] = el.eigenschaften
            fields[base + 'RW'] = str(el.rw)
            if type(el) == Objekte.Fernkampfwaffe:
                fields[base + 'WM'] = str(el.lz)
            else:
                fields[base + 'WM'] = str(el.wm)

            # Calculate modifiers for AT, PA, TP from Kampfstil
            if el.name in Wolke.DB.waffen:
                fertig = Wolke.DB.waffen[el.name].fertigkeit
                tale = Wolke.DB.waffen[el.name].talent
            else:
                fertig = ""
                tale = ""
            if fertig in Wolke.Char.fertigkeiten:
                if tale in Wolke.Char.fertigkeiten[fertig].gekaufteTalente:
                    bwert = Wolke.Char.fertigkeiten[fertig].probenwertTalent
                else:
                    bwert = Wolke.Char.fertigkeiten[fertig].probenwert
                at = bwert
                vt = bwert
                sp = 0
                flagReiter2 = False
                # 0 is no Kampfstil, no Effect
                # 1 is Beidhändig
                if el.kampfstil == 1:
                    levelC = 0
                    for vor in Wolke.Char.vorteile:
                        if Definitionen.Kampfstile[1] in vor:
                            levelC += 1
                    at += min(levelC, 3)
                # 2 is Parierwaffenkampf which does nothing
                # 3 is Reiterkampf
                elif el.kampfstil == 3:
                    levelC = 0
                    for vor in Wolke.Char.vorteile:
                        if Definitionen.Kampfstile[3] in vor:
                            levelC += 1
                    if levelC >= 2:
                        flagReiter2 = True
                    at += min(levelC, 3)
                    vt += min(levelC, 3)
                    sp += min(levelC, 3)
                # 4 is Schildkampf
                elif el.kampfstil == 4:
                    levelC = 0
                    for vor in Wolke.Char.vorteile:
                        if Definitionen.Kampfstile[4] in vor:
                            levelC += 1
                    vt += min(levelC, 3)
                # 5 is Kraftvoller Kampf
                elif el.kampfstil == 5:
                    levelC = 0
                    for vor in Wolke.Char.vorteile:
                        if Definitionen.Kampfstile[5] in vor:
                            levelC += 1
                    sp += min(levelC, 3)
                # 6 is Schneller Kampf
                elif el.kampfstil == 6:
                    levelC = 0
                    for vor in Wolke.Char.vorteile:
                        if Definitionen.Kampfstile[6] in vor:
                            levelC += 1
                    at += min(levelC, 3)

                if type(el) == Objekte.Nahkampfwaffe:
                    if "Kopflastig" in el.eigenschaften or\
                        (el.name == "Unbewaffnet" and "Waffenloser Kampf" in
                         Wolke.Char.vorteile):
                        sp += Wolke.Char.schadensbonus*2
                    else:
                        sp += Wolke.Char.schadensbonus
                    at += el.wm
                    vt += el.wm

                res = re.findall('Schwer \(([0-9]{1,2})\)',
                                 el.eigenschaften,
                                 re.UNICODE)
                if len(res) > 0:
                    minkk = int(res[0])
                    if Wolke.Char.attribute['KK'].wert < minkk:
                        at -= 2
                        vt -= 2

                if not (flagReiter2 and tale == "Reiten" and \
                        fertig == "Athletik"):
                    at -= Wolke.Char.be
                    vt -= Wolke.Char.be

                fields[base + 'ATm'] = at
                fields[base + 'VTm'] = vt
                sg = ""
                if el.plus+sp >= 0:
                    sg = "+"
                fields[base + 'TPm'] = str(el.W6) + "W6" + sg + str(el.plus+sp)

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
        if Wolke.Debug:
            print("PDF Block 6")

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
        flagPutEmpty = False
        if len(talsList)+countFerts-1 < 31:
            flagPutEmpty = True

        countF = 1
        countT = 1
        for f in Wolke.Char.übernatürlicheFertigkeiten:
            if Wolke.Char.übernatürlicheFertigkeiten[f].wert <= 0 and\
                    len(Wolke.Char.übernatürlicheFertigkeiten[f].
                        gekaufteTalente) == 0:
                continue
            fe = Wolke.Char.übernatürlicheFertigkeiten[f]

            if countF < 13:
                # Fill Fertigkeitsslots
                base = 'Ueberfer' + str(countF)
                fields[base + 'NA'] = fe.name
                fields[base + 'FA'] = fe.steigerungsfaktor
                fields[base + 'AT'] = fe.attribute[0] + '/' + \
                    fe.attribute[1] + '/' + fe.attribute[2]
                fields[base + 'BA'] = fe.basiswert
                fields[base + 'FW'] = fe.wert
                fields[base + 'PW'] = fe.probenwertTalent
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
                    mod += " (" + str(Wolke.Char.talenteVariable[t]) + \
                              " EP)"

                #if t+mod in self.Talents:
                #    if fe.probenwertTalent > self.Talents[t+mod].pw:
                #        self.Talents[t+mod].pw = fe.probenwertTalent
                        #fields[self.addedTals[t+mod][1] + 'PW'] = \
                              #fe.probenwertTalent
                        #self.addedTals[t+mod] = (fe.probenwertTalent,
                        #                    self.addedTals[t+mod][1])
                #else:
                #self.addedTals[t+mod] = (fe.probenwertTalent, base)
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
                if tt.na in self.Talents:
                    if tt.pw > self.Talents[tt.na].pw:
                        self.Talents[tt.na] = tt
                else:
                    self.Talents[tt.na] = tt
        for tt in self.Talents:
            if countT < 31:
                base = 'Uebertal' + str(countT)
                fields[base + 'NA'] = self.Talents[tt].na
                fields[base + 'PW'] = self.Talents[tt].pw
                fields[base + 'VO'] = self.Talents[tt].vo
                fields[base + 'WD'] = self.Talents[tt].wd
                fields[base + 'KO'] = self.Talents[tt].ko
                fields[base + 'RE'] = self.Talents[tt].re
            else:
                if self.Talents[tt] not in self.ExtraTalents:
                    self.UseExtraPage = True
                    self.ExtraTalents.append(self.Talents[tt])
            countT += 1
        if flagPutEmpty:
            countT += 1

        return fields

    def pdfSiebterBlock(self, fields):
        if Wolke.Debug:
            print("PDF Block 7")
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
                fields[base + 'BA' + '2'] = fe.basiswert
                fields[base + 'FW' + '2'] = fe.wert
                fields[base + 'PW' + '2'] = fe.probenwertTalent
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