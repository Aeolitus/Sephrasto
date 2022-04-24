[Hilfe](Help.md) > Skripte für Vorteile und Waffeneigenschaften

# Skripte für Vorteile und Waffeneigenschaften
Vorteile und Waffeneigenschaften haben im Regelbasis-Editor ein Feld für benutzerdefinierte Skripte. Diese werden verwendet, um Auswirkungen auf die Charakterwerte umzusetzen. Skripte werden in Python geschrieben, wobei alles in eine Zeile geschrieben werden muss.
<br />
## API
Sephrasto bietet eine Reihe von Funktionen an, anhand derer die meisten Skripte mit ein paar wenigen Zeichen umzusetzen sind. Die 'get' Funktionen liefern den entsprechenden Wert zurück, die 'set' Funktionen setzen den Wert auf den übergebenen Ganzzahl-Parameter und die 'modify' Funktionen verändern den gewünschten Wert um den übergebenen Ganzzahl-Parameter. Ausnahmen sind in spitzen Klammern aufgeführt.  Bei komplexeren Vorhaben sollte ein 'one-lined python converter' genutzt werden.

Die folgenden Funktionen stehen neben Python-Builtins wie 'round' zur Verfügung:
<br />
### Beschreibung
- Hintergrund: ```getName, getRasse, getStatus, getKurzbeschreibung, getHeimat, getFinanzen```
- Eigenheiten: ```getEigenheiten <Return: string[8]>```
- EP: ```getEPTotal, getEPSpent```
<br />
### Attribute
- ```getGE, getKK, getKO, getFF, getMU, getIN, getKL, getCH```
- ```getAttribut <Parameter: Attribut-Name>```
<br />
### Abgeleitete Werte
- AsP: ```getAsPBasis, setAsPBasis, modifyAsPBasis, getAsPMod, setAsPMod, modifyAsPMod```
- KaP: ```getKaPBasis, setKaPBasis, modifyKaPBasis, getKaPMod, setKaPMod, modifyKaPMod```
- SchiP: ```getSchiPMax, setSchiPMax, modifySchiPMax```
- WS: ```getWSBasis, getWS (ohne RS!), setWS, modifyWS```
- MR: ```getMRBasis, getMR, setMR, modifyMR```
- GS: ```getGSBasis, getGS (ohne BE!), setGS, modifyGS```
- DH: ```getDHBasis, getDH (ohne BE!), setDH, modifyDH```
- Schadensbonus: ```getSchadensbonusBasis, getSchadensbonus, setSchadensbonus, modifySchadensbonus```
- INI: ```getINIBasis, getINI, setINI, modifyINI```
- RS: ```getRSMod, setRSMod, modifyRSMod```
- BE: ```getBEBasis, getBEMod, setBEMod, modifyBEMod```
<br />
### Fertigkeiten und Talente
- Freie Fertigkeiten: ```getFreieFertigkeiten <Return: string[]>```
- Fertigkeiten: ```getFertigkeit/getÜbernatürlicheFertigkeit <Parameter: Fertigkeits-Name. Return: { name, wert, steigerungsfaktor, text, gekaufteTalente[], kampffertigkeit, attribute[3], attributswerte[3], basiswert, probenwert, probenwertTalent, voraussetzungen[], maxWert }>```
- Fertigkeiten Basis: ```modifyFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>```
- Übern. Fertigkeiten Basis: ```modifyÜbernatürlicheFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>```
- Talente: ```modifyTalent : <Parameter: Fertigkeits-Name, Talent-Name, Bedingung, Modifikator>```<br />
Beispiel: modifyTalent('Beeinflussung', 'Überreden', 'Rededuell', 2)
<br />
### Vorteile
- Vorteile allgemein: ```getVorteile <Return: { name, wert, steigerungsfaktor, text, kosten, typ, voraussetzungen[], nachkauf, text }[]>```
- Kampfstile: ```getKampfstil <Parameter: Kampfstil-Name. Return: { AT, VT, TP, RW, BE }>, setKampfstil/modifyKampfstil <Parameter: Kampfstil-Name, AT, VT, TP, RW, BE>```
<br />
### Ausrüstung
- Inventar: ```getAusrüstung <Return: string[]>```
- Rüstung: ```getRüstung <Return: { name, text, be, rs[6] }[]>```
- Waffen: ```getWaffen <Return: { name, text, W6, plus, eigenschaften[], haerte, fertigkeit, talent, kampfstile[], kampfstil, rw, wm, lz}[]>```<br />
Hinweis: Nur Fernkampfwaffen haben das Feld 'lz'.
<br />
### Sonstiges
- ```addWaffeneigenschaft <Parameter: TalentName, Eigenschaft>```<br />
Beispiel: addWaffeneigenschaft('Unbewaffnet', 'Kopflastig')
- ```removeWaffeneigenschaft <Parameter: TalentName, Eigenschaft>```<br />
Beispiel: removeWaffeneigenschaft('Unbewaffnet', 'Zerbrechlich')
<br />
### Waffeneigenschaften (WE)
Waffeneigenschaft-Scripts haben keinen Zugriff auf: setSchadensbonus, modifySchadensbonus, setBEMod, modifyBEMod, modifyFertigkeitBasiswert, setKampfstil, modifyKampfstil, addWaffeneigenschaft, removeWaffeneigenschaft.
Die folgenden Funktionen stehen ausschließlich innerhalb von Waffeneigenschaft-Scripts zur Verfügung:
- Parameter dieser WE als string erhalten: ```getEigenschaftParam <Parameter: Parameternummer>```<br />
Parameter müssen mit Semikolon getrennt werden.  
- Waffen mit dieser WE modifizieren: ```modifyWaffeAT, modifyWaffeVT, modifyWaffeTPW6, modifyWaffeTPPlus, modifyWaffeHaerte, modifyWaffeRW, setWaffeAT, setWaffeVT, setWaffeTPW6, setWaffeTPPlus, setWaffeHaerte, setWaffeRW```
- Aktuelle Werte der Waffe erhalten: ```getWaffenWerte <Return: { AT, VT, RW, TPW6, TPPlus, Haerte, Kampfstil }>```
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
modifyKampfstil('Reiterkampf', 1, 1, 1, 0); setKampfstilBEIgnore('Reiterkampf', 'Athletik', 'Reiten')">
```
Erhöht für den Kampfstil Reiterkampf die Werte für TP, AT und VT um eins. Außerdem wird mit dem Kampfstil Reiterkampf die Behinderung ignoriert, falls die Waffe mit dem Talent Reiten der Fertigkeit Athletik geführt wird.
<br />

### Waffeneigenschaft Kopflastig
```
modifyWaffeTPPlus(getSchadensbonus())
```
Erhöht die TP aller Waffen mit dieser Eigenschaft um den Schadensbonus.
<br />

### Waffeneigenschaft Schwer
```
if getKK() < int(getEigenschaftParam(1)): modifyWaffeAT(-2); modifyWaffeVT(-2)
```
Verringert AT und VT aller Waffen mit dieser Eigenschaft um 2, falls der Wert der Körperkraft unter dem Wert des ersten Parameters der Eigenschaft liegt (bei Schwer(4) ist dies 4).