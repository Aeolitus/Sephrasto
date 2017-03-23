# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 21:33:46 2017

@author: Aeolitus
"""

import docx
import re
import Fertigkeiten
import Datenbank

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    #return '\n'.join(fullText)
    return doc
def updateUeber():
    ferts = {}
    txt = getText('ueber.docx')
    #results = re.search('', txt)
    count = 0
    while True:
        res = re.match("(?P<name>.*?)\s*?\(\s*?(?P<at1>[A-Z]{2})\s*?/\s*?(?P<at2>[A-Z]{2})\s*?/\s*?(?P<at3>[A-Z]{2})\s*?,\s*?(?P<sf>[0-9])\s*?\)\s*?", txt.paragraphs[count].text, re.UNICODE)
        if res is not None:
            fert = Fertigkeiten.Fertigkeit()
            dic = res.groupdict()
            fert.name = dic['name']
            fert.steigerungsfaktor = int(dic['sf'])
            fert.attribute = [dic['at1'], dic['at2'], dic['at3']]
            count += 1
            fert.text = txt.paragraphs[count].text
            ferts.update({dic['name']: fert})                         
        count +=1
        if count >= len(txt.paragraphs):
            break
    D = Datenbank.Datenbank()
    D.übernatürlicheFertigkeiten.update(ferts)
    D.xmlSchreiben()
    return ferts

def updateUeberTalents():
    Reps = {
            'Pra': "V:Praioskirchliche Tradition I:1",
            'Ron': "V:Rondrakirchliche Tradition I:1",
            'Brn': "V:Boronkirchliche Tradition I:1",
            'Phe': "V:Phexkirchliche Tradition I:1",
            'Eff': "V:Efferdkirchliche Tradition I:1",
            'Hes': "V:Hesindekirchliche Tradition I:1",
            'Ing': "V:Ingerimmkirchliche Tradition I:1",
            'Ang': "V:Angroschkirchliche Tradition I:1",
            'Per': "V:Perainekirchliche Tradition I:1",
            'Fir': "V:Firunkirchliche Tradition I:1",
            'Rah': "V:Rahjakirchliche Tradition I:1",
            'Tsa': "V:Tsakirchliche Tradition I:1",
            'Tra': "V:Traviakirchliche Tradition I:1",
            'Mag': "V:Gildenmagische Repräsentation I:1",
            'Hex': "V:Hexische Repräsentation I:1",
            'Geo': "V:Geodische Repräsentation I:1",
            'Dru': "V:Druidische Repräsentation I:1",
            'Srl': "V:Scharlatanische Repräsentation I:1",
            'Sch': "V:Schelmische Repräsentation I:1",
            'Ach': "V:Kristallomantische Repräsentation I:1",
            'Bor': "V:Borbaradianische Repräsentation I:1",
            'Alch': "V:Alchemistische Repräsentation I:1",
            'Elf': "V:Elfische Repräsentation I:1",
            }
    tals = {}
    txt = getText('ueber.docx')
    #results = re.search('', txt)
    count = len(txt.paragraphs)-1
    while True:
        flag = False
        #Is this erlernen?
        resEr = re.match(r"\s*?Erlernen:\s*?(?P<verb>.*?);\s*?(?P<EP>[0-9]{1,3})\s*?EP\s*?", txt.paragraphs[count].text, re.UNICODE)
        if resEr is not None:
            tal = Fertigkeiten.Talent()
            erDict = resEr.groupdict()
            tal.kosten = erDict['EP']
            # Get out different representations
            resVe = re.findall(u"(?:[\s0-9;,]*)([a-zA-ZäöüÄÖÜß]{3,4})(?:[\s0-9;,]*)",erDict['verb'], re.UNICODE)
            arr = []
            for el in resVe:
                arr.append([Reps[el]])
            tal.voraussetzungen.append(arr)
            #Move to fertigkeiten
            count -= 1
            resFe = re.findall(u"[a-zA-ZäöüÄÖÜß ]+",txt.paragraphs[count].text, re.UNICODE)
            if resFe[0] != "Fertigkeiten":
                flag = True
            else:
                for el in resFe[1:]:
                    tal.fertigkeiten.append(el.strip())
                    count -= 1
            #Get Text
            textpart = []
            iterate = txt.paragraphs[count].text
            while iterate != "":
                textpart.append(txt.paragraphs[count].text)
                count -= 1
                iterate = txt.paragraphs[count].text
            tal.name = textpart[-1].strip()
            textpart = textpart[:-1]
            textpart.reverse()
            tal.text = "\n".join(textpart)
            tals.update({tal.name: tal})
            if flag:
                print("Recheck " + tal.name)
            else:
                #print("Success with: " + tal.name)
                pass
        count -= 1
        if count <= 30:
            break
    D = Datenbank.Datenbank()
    D.datei = "datenbank2.xml"
    D.vorteile.clear()
    D.talente.clear()
    D.fertigkeiten.clear()
    D.übernatürlicheFertigkeiten.clear()
    tmp = []
    for tal in tals:
        tmp.append(tal)
    tmp.reverse()
    tmp2 = {}
    for el in tmp:
        tmp2.update({el: tals[el]})
    D.talente.update(tmp2)
    D.xmlSchreiben()
    return tmp2

if __name__ == "__main__":
    ret = updateUeberTalents()