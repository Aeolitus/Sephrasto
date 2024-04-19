# Skripte für Abgeleitete Werte, Vorteile und Waffeneigenschaften
Abgeleitete Werte, Vorteile und Waffeneigenschaften haben im Regelbasis-Editor ein Feld für benutzerdefinierte Skripte. Diese werden verwendet, um Auswirkungen auf die Charakterwerte umzusetzen. Skripte werden in Python geschrieben, wobei alles in eine Zeile geschrieben werden muss.

## API
Sephrasto bietet eine Reihe von Funktionen an, anhand derer die meisten Skripte mit ein paar wenigen Zeichen umzusetzen sind. Die 'get' Funktionen liefern den entsprechenden Wert zurück, die 'set' Funktionen setzen den Wert auf den übergebenen Ganzzahl-Parameter und die 'modify' Funktionen verändern den gewünschten Wert um den übergebenen Ganzzahl-Parameter. Ausnahmen sind in spitzen Klammern aufgeführt.  Bei komplexeren Vorhaben sollte ein 'one-lined python converter' genutzt werden.

Die folgenden Funktionen stehen neben Python-Builtins wie 'round' zur Verfügung:

### Beschreibung
- Hintergrund: ```getName, getSpezies, getStatus, getKurzbeschreibung, getHeimat, getFinanzen```
- Eigenheiten: ```getEigenheiten <Return: string[8]>```
- EP: ```getEPGesamt, getEPAusgegeben```

### Attribute
- ```getGE, getKK, getKO, getFF, getMU, getIN, getKL, getCH```
- ```getAttribut <Parameter: Attribut-Name>```

**Hinweis:** Sephrasto stellt die API für alle Attribute nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Attribute.

### Energien
- AsP: ```getAsPBasis, setAsPBasis, modifyAsPBasis, getAsPMod, setAsPMod, modifyAsPMod```
- KaP: ```getKaPBasis, setKaPBasis, modifyKaPBasis, getKaPMod, setKaPMod, modifyKaPMod```
- GuP: ```getGuPBasis, setGuPBasis, modifyGuPBasis, getGuPMod, setGuPMod, modifyGuPMod```

**Hinweis:** Sephrasto stellt die API für alle Energien nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Energien.

### Abgeleitete Werte
- SchiP: ```getSchiPBasis, getSchiP, setSchiP, modifySchiP```
- WS: ```getWSBasis, getWS (ohne RS!), setWS, modifyWS```
- MR: ```getMRBasis, getMR, setMR, modifyMR```
- GS: ```getGSBasis, getGS (ohne BE!), setGS, modifyGS```
- DH: ```getDHBasis, getDH (ohne BE!), setDH, modifyDH```
- SB: ```getSBBasis, getSB, setSB, modifySB```
- INI: ```getINIBasis, getINI, setINI, modifyINI```
- RS: ```getRSBasis, getRS, setRS, modifyRS```
- BE: ```getBEBasis, getBE, setBE, modifyBE```

**Hinweis:** Sephrasto stellt die API für alle Abgeleiteten Werte nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Abgeleitete Werte.

### Fertigkeiten und Talente
- Freie Fertigkeiten: ```getFreieFertigkeiten <Return: { definition { name, kategorie, voraussetzungen[] }, wert }>```
- Fertigkeiten: ```getFertigkeit/getÜbernatürlicheFertigkeit <Parameter: Fertigkeits-Name. Return: { definition { name, steigerungsfaktor, text, attribute [], kampffertigkeit, voraussetzungen [], kategorie, talenteGruppieren }, wert, gekaufteTalente[], talentMods {}, attributswerte, basiswert, basiswertMod, probenwert, probenwertTalent, maxWert, addToPdf  }>```
- Fertigkeiten Basis: ```modifyFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>```
Hinweis: Dies ist nützlich, um sich permanente Erleichterungen auf eine Fertigkeit nicht merken zu müssen. Diese Modifikation wird bei Voraussetzungen der Typen "Fertigkeit" und "Talent" nicht eingerechnet!
- Übernatürliche Fertigkeiten Basis: ```modifyÜbernatürlicheFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>```
- Talente Probenwert: ```modifyTalentProbenwert : <Parameter: Talent-Name, Modifikator>```
Beispiel: modifyTalentProbenwert('Überreden', 2)
Hinweis: Dies ist nützlich, um permanente Erleichterungen auf ein Talent direkt in der Talentliste aufzuführen. Ist das Talent noch nicht erworben, wird das ganze Talent mit der Modifizierung in Klammern gesetzt. Die Modifizierung wird ausschließlich im Charakterbogen eingerechnet!
- Talente zusätzliche Informationen: ```talentAddInfo : <Parameter: Talent-Name, Infotext>```
Beispiel: addTalentInfo('Überreden', "Rededuell +2")
Hinweis: Dies ist nützlich, um besondere Effekte wie beispielsweise von manchen Vorteilen direkt bei den Talenten im Charakterbogen aufzuführen.
- Talente hinzufügen: ```addTalent : <Parameter: Talent-Name, Kosten (optional), Benötigte übernatürliche Fertigkeit (optional)>```
Hinweis: Das Script fügt dem Talent den Vorteil zu dem es gehört als Voraussetzung hinzu. Sobald der Vorteil also abgewählt wird, verliert der Charakter auch das Talent. Mit dem Kosten-Parameter können die Standard-Talentkosten geändert werden (bei -1 werden sie nicht verändert). Optional kann außerdem eine übernatürliche Fertigkeit mit angegeben werden, die benötigt wird - falls der Charakter sie nicht besitzt, macht das Script nichts; diese wird dannauch als Voraussetzung hinzugefügt.
Beispiel ohne Bedingung und Kostenveränderung: addTalent("Spurlos Trittlos")
Beispiel mit Kosten auf 0 EP gesetzt und "Gaben des Butgeists" als Bedingung: addTalent("Spurlos Trittlos", 0, "Gaben des Blutgeists")

### Vorteile
- Vorteile allgemein: ```getVorteil <Parameter: Vorteils-Name. Return: { definition { name, text, info, bedingungen, kosten, variableKosten, kommentarErlauben, kategorie, voraussetzungen [], nachkauf,  cheatsheetAuflisten, cheatsheetBeschreibung, linkKategorie, linkElement, script, scriptPrio, querverweise [], querverweiseResolved {}, anzeigenameExt }[]>```
- Kampfstile: ```getKampfstil <Parameter: Kampfstil-Name. Return: { at, vt, plus, rw, be }>, setKampfstil/modifyKampfstil <Parameter: Kampfstil-Name, at, vt, plus, rw, be>```
Hinweis: Statt eines Kampfstil-Namens kann auch "Nahkampf" oder "Fernkampf" angegeben werden, um globale Modifikationen für alle Nah-/Fernkampfwaffen anzugeben. Diese werden dann zum tatsächlichen Kampfstil einer Waffe addiert.

### Ausrüstung
- Inventar: ```getAusrüstung <Return: string[]>```
- Rüstung: ```getRüstung <Return: { name, text, kategorie, system, rs[6], be }[]>```
- Waffen: ```getWaffen <Return: { name, würfel, würfelSeiten, plus, eigenschaften[], härte, fertigkeit, talent, beSlot, kampfstile[], kampfstil, rw, wm, lz, fernkampf, nahkampf, anzeigename}[]>```

### Sonstiges
- ```addWaffeneigenschaft <Parameter: WaffenName, Eigenschaft>```
Beispiel: addWaffeneigenschaft('Hand', 'Kopflastig')
- ```removeWaffeneigenschaft <Parameter: WaffenName, Eigenschaft>```
Beispiel: removeWaffeneigenschaft('Hand', 'Zerbrechlich')

## Besonderheiten

### Abgeleitete Werte
Das "Finalwert Script" von Abgeleiteten Werten hat vollen Zugriff auf die API. Das "Script" hat jedoch nur Zugriff auf die folgenden Funktionen: ```getAttribut, getRüstung```.

### Waffeneigenschaften (WE)
Waffeneigenschaft-Scripts haben keinen Zugriff auf: ```setSB, modifySB, setBE, modifyBE, setRS, modifyRS, modifyFertigkeitBasiswert, setKampfstil, modifyKampfstil, addWaffeneigenschaft, removeWaffeneigenschaft```.
Die folgenden zusätzlichen Funktionen stehen ausschließlich innerhalb von Waffeneigenschaft-Scripts zur Verfügung:
- Parameter dieser WE als string erhalten: ```getEigenschaftParam <Parameter: Parameternummer>```
Parameter müssen mit Semikolon getrennt werden.  
- Waffen mit dieser WE modifizieren: ```modifyWaffeAT, modifyWaffeVT, modifyWaffeTPWürfel, modifyWaffeTPPlus, modifyWaffeHäerte, modifyWaffeRW, setWaffeAT, setWaffeVT, setWaffeTPWürfel, setWaffeTPPlus, setWaffeHärte, setWaffeRW```
- Aktuelle Waffe erhalten: ```getWaffe <Return: { name, würfel, würfelSeiten, plus, eigenschaften[], härte, fertigkeit, talent, beSlot, kampfstile[], kampfstil, rw, wm, lz, fernkampf, nahkampf, anzeigename }>```
- Aktuelle Werte der Waffe erhalten: ```getWaffenWerte <Return: { at, vt, rw, würfel, plus, härte, kampfstil }>```

## Beispiele


### Vorteil Waffenloser Kampf
```
Beispiel: for waffe in ['Hand', 'Fuß']: addWaffeneigenschaft(waffe, 'Kopflastig');  addWaffeneigenschaft(waffe, 'Wendig')
```
Fügt den Waffen Hand und Fuß die Eigenschaften Kopflastig und Wendig hinzu.


### Vorteil Gefäß der Sterne
```
modifyAsPMod(getCH() + 4).
```
Erhöht die AsP um den Charismawert + 4.


### Vorteil Reiterkampf II
```
modifyKampfstil('Reiterkampf', 1, 1, 1, 0, -1)
```
Erhöht für den Kampfstil Reiterkampf die Werte für AT, VT und TP um +1 und senkt die BE um -1.


### Waffeneigenschaft Kopflastig
```
modifyWaffeTPPlus(getSB())
```
Erhöht die TP aller Waffen mit dieser Eigenschaft um den Schadensbonus.


### Waffeneigenschaft Schwer
```
if getKK() < int(getEigenschaftParam(1)): modifyWaffeAT(-2); modifyWaffeVT(-2)
```
Verringert AT und VT aller Waffen mit dieser Eigenschaft um 2, falls der Wert der Körperkraft unter dem Wert des ersten Parameters der Eigenschaft liegt (bei Schwer(4) ist dies 4).
