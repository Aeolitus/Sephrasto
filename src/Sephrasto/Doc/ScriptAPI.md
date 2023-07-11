[Hilfe](Help.md) > Skripte für Abgeleitete Werte, Vorteile und Waffeneigenschaften

# Skripte für Abgeleitete Werte, Vorteile und Waffeneigenschaften
Abgeleitete Werte, Vorteile und Waffeneigenschaften haben im Regelbasis-Editor ein Feld für benutzerdefinierte Skripte. Diese werden verwendet, um Auswirkungen auf die Charakterwerte umzusetzen. Skripte werden in Python geschrieben, wobei alles in eine Zeile geschrieben werden muss.
<br />
## API
Sephrasto bietet eine Reihe von Funktionen an, anhand derer die meisten Skripte mit ein paar wenigen Zeichen umzusetzen sind. Die 'get' Funktionen liefern den entsprechenden Wert zurück, die 'set' Funktionen setzen den Wert auf den übergebenen Ganzzahl-Parameter und die 'modify' Funktionen verändern den gewünschten Wert um den übergebenen Ganzzahl-Parameter. Ausnahmen sind in spitzen Klammern aufgeführt.  Bei komplexeren Vorhaben sollte ein 'one-lined python converter' genutzt werden.

Die folgenden Funktionen stehen neben Python-Builtins wie 'round' zur Verfügung:
<br />
### Beschreibung
- Hintergrund: ```getName, getSpezies, getStatus, getKurzbeschreibung, getHeimat, getFinanzen```
- Eigenheiten: ```getEigenheiten <Return: string[8]>```
- EP: ```getEPGesamt, getEPAusgegeben```
<br />
### Attribute
- ```getGE, getKK, getKO, getFF, getMU, getIN, getKL, getCH```
- ```getAttribut <Parameter: Attribut-Name>```<br />
<br />
**Hinweis:** Sephrasto stellt die API für alle Attribute nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Attribute.
<br />
### Energien
- AsP: ```getAsPBasis, setAsPBasis, modifyAsPBasis, getAsPMod, setAsPMod, modifyAsPMod```
- KaP: ```getKaPBasis, setKaPBasis, modifyKaPBasis, getKaPMod, setKaPMod, modifyKaPMod```
- GuP: ```getGuPBasis, setGuPBasis, modifyGuPBasis, getGuPMod, setGuPMod, modifyGuPMod```<br />
<br />
**Hinweis:** Sephrasto stellt die API für alle Energien nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Energien.
<br />
### Abgeleitete Werte
- SchiP: ```getSchiPBasis, getSchiP, setSchiP, modifySchiP```
- WS: ```getWSBasis, getWS (ohne RS!), setWS, modifyWS```
- MR: ```getMRBasis, getMR, setMR, modifyMR```
- GS: ```getGSBasis, getGS (ohne BE!), setGS, modifyGS```
- DH: ```getDHBasis, getDH (ohne BE!), setDH, modifyDH```
- SB: ```getSBBasis, getSB, setSB, modifySB```
- INI: ```getINIBasis, getINI, setINI, modifyINI```
- RS: ```getRSBasis, getRS, setRS, modifyRS```
- BE: ```getBEBasis, getBE, setBE, modifyBE```<br />
<br />
**Hinweis:** Sephrasto stellt die API für alle Abgeleiteten Werte nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Abgeleitete Werte.
<br />
### Fertigkeiten und Talente
- Freie Fertigkeiten: ```getFreieFertigkeiten <Return: { name, kategorie, voraussetzungen[], wert }>```
- Fertigkeiten: ```getFertigkeit/getÜbernatürlicheFertigkeit <Parameter: Fertigkeits-Name. Return: { name, steigerungsfaktor, text, attribute [], kampffertigkeit, voraussetzungen [], typ, talenteGruppieren, wert, gekaufteTalente[], talentMods {}, attributswerte, basiswert, basiswertMod, probenwert, probenwertTalent, maxWert, addToPdf  }>```
- Fertigkeiten Basis: ```modifyFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>```
Hinweis: Dies ist nützlich, um sich permanente Erleichterungen auf eine Fertigkeit nicht merken zu müssen. Die Modifizierung wird ausschließlich im Charakterbogen eingerechnet!
- Übern. Fertigkeiten Basis: ```modifyÜbernatürlicheFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>```
- Talente: ```modifyTalent : <Parameter: Fertigkeits-Name, Talent-Name, Bedingung, Modifikator>```<br />
Beispiel mit Bedingung: modifyTalent('Beeinflussung', 'Überreden', 'Rededuell', 2)
Beispiel ohne Bedingung: modifyTalent('Beeinflussung', 'Überreden', '', 2)
Hinweis: Dies ist nützlich, um permanente Erleichterungen auf ein Talent (ggf. unter einer bestimmten Bedingung) direkt in der Talentliste aufzuführen. Ist das Talent noch nicht erworben, wird das ganze Talent mit der Modifizierung in Klammern gesetzt. Die Modifizierung wird ausschließlich im Charakterbogen eingerechnet!
<br />
### Vorteile
- Vorteile allgemein: ```getVorteile <Return: { name, kosten, variableKosten, kommentarErlauben, typ, voraussetzungen [], nachkauf, text, cheatsheetAuflisten, cheatsheetBeschreibung, linkKategorie, linkElement, script, scriptPrio, querverweise [], querverweiseResolved {}, kommentar }[]>```
- Kampfstile: ```getKampfstil <Parameter: Kampfstil-Name. Return: { at, vt, plus, rw, be }>, setKampfstil/modifyKampfstil <Parameter: Kampfstil-Name, at, vt, plus, rw, be>```
<br />
### Ausrüstung
- Inventar: ```getAusrüstung <Return: string[]>```
- Rüstung: ```getRüstung <Return: { name, text, typ, system, rs[6], be }[]>```
- Waffen: ```getWaffen <Return: { name, würfel, würfelSeiten, plus, eigenschaften[], härte, fertigkeit, talent, kampfstile[], kampfstil, rw, wm, lz, fernkampf, nahkampf, anzeigename}[]>```
<br />
### Sonstiges
- ```addWaffeneigenschaft <Parameter: TalentName, Eigenschaft>```<br />
Beispiel: addWaffeneigenschaft('Unbewaffnet', 'Kopflastig')
- ```removeWaffeneigenschaft <Parameter: TalentName, Eigenschaft>```<br />
Beispiel: removeWaffeneigenschaft('Unbewaffnet', 'Zerbrechlich')
<br />
## Besonderheiten

### Abgeleitete Werte
Das "Finalwert Script" von Abgeleiteten Werten hat vollen Zugriff auf die API. Das "Script" hat jedoch nur Zugriff auf die folgenden Funktionen: ```getAttribut, getRüstung```.
<br />
### Waffeneigenschaften (WE)
Waffeneigenschaft-Scripts haben keinen Zugriff auf: ```setSB, modifySB, setBE, modifyBE, setRS, modifyRS, modifyFertigkeitBasiswert, setKampfstil, modifyKampfstil, addWaffeneigenschaft, removeWaffeneigenschaft```.<br />
Die folgenden zusätzlichen Funktionen stehen ausschließlich innerhalb von Waffeneigenschaft-Scripts zur Verfügung:
- Parameter dieser WE als string erhalten: ```getEigenschaftParam <Parameter: Parameternummer>```<br />
Parameter müssen mit Semikolon getrennt werden.  
- Waffen mit dieser WE modifizieren: ```modifyWaffeAT, modifyWaffeVT, modifyWaffeTPWürfel, modifyWaffeTPPlus, modifyWaffeHäerte, modifyWaffeRW, setWaffeAT, setWaffeVT, setWaffeTPWürfel, setWaffeTPPlus, setWaffeHärte, setWaffeRW```
- Aktuelle Werte der Waffe erhalten: ```getWaffenWerte <Return: { at, vt, rw, würfel, plus, härte, kampfstil }>```
<br />
## Beispiele
<br />

### Vorteil Waffenloser Kampf
```
addWaffeneigenschaft('Unbewaffnet', 'Kopflastig'); addWaffeneigenschaft('Unbewaffnet', 'Wendig')
```
Fügt allen Waffen, die mit dem Talent Unbewaffnet geführt werden, die Eigenschaften Kopflastig und Wendig hinzu.
<br />

### Vorteil Gefäß der Sterne
```
modifyAsPMod(getCH() + 4).
```
Erhöht die AsP um den Charismawert + 4.
<br />

### Vorteil Reiterkampf II
```
modifyKampfstil('Reiterkampf', 1, 1, 1, 0, -1)
```
Erhöht für den Kampfstil Reiterkampf die Werte für AT, VT und TP um +1 und senkt die BE um -1.
<br />

### Waffeneigenschaft Kopflastig
```
modifyWaffeTPPlus(getSB())
```
Erhöht die TP aller Waffen mit dieser Eigenschaft um den Schadensbonus.
<br />

### Waffeneigenschaft Schwer
```
if getKK() < int(getEigenschaftParam(1)): modifyWaffeAT(-2); modifyWaffeVT(-2)
```
Verringert AT und VT aller Waffen mit dieser Eigenschaft um 2, falls der Wert der Körperkraft unter dem Wert des ersten Parameters der Eigenschaft liegt (bei Schwer(4) ist dies 4).
