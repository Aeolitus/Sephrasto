# Script-API:
'get' Funktionen liefern den entsprechenden Wert zurück, die 'set' Funktionen setzen den Wert auf den übergebenen Ganzzahl-Parameter und die 'modify' Funktionen verändern den gewünschten Wert um den übergebenen Ganzzahl-Parameter. Ausnahmen sind in spitzen Klammern aufgeführt. Skripte werden in Python geschrieben, wobei alles in eine Zeile geschrieben werden muss. Bei komplexeren Vorhaben sollte ein 'one-lined python converter' genutzt werden.

Die folgenden Funktionen stehen neben Python-Builtins wie 'round' zur Verfügung:

#### Hintergrund
    getName, getRasse, getStatus, getKurzbeschreibung, getHeimat, getFinanzen, getEigenheiten <Return: string[8]>, getEPTotal, getEPSpent

#### Attribute
    getGE, getKK, getKO, getFF, getMU, getIN, getKL, getCH,
    getAttribut <Parameter: Attribut-Name>

#### Abgeleitete Werte
    AsP: getAsPBasis, setAsPBasis, modifyAsPBasis, getAsPMod, setAsPMod, modifyAsPMod
    KaP: getKaPBasis, setKaPBasis, modifyKaPBasis, getKaPMod, setKaPMod, modifyKaPMod
    SchiP: getSchiPMax, setSchiPMax, modifySchiPMax
    WS: getWSBasis, getWS, setWS, modifyWS, getWSStern
    MR: getMRBasis, getMR, setMR, modifyMR
    GS: getGSBasis, getGS, setGS, modifyGS
    DH: getDH, setDH, modifyDH
    Schadensbonus: getSchadensbonusBasis, getSchadensbonus, setSchadensbonus, modifySchadensbonus
    INI: getINIBasis, getINI, setINI, modifyINI
    RS: getRSMod, setRSMod, modifyRSMod
    BE: getBEBasis, getBEMod, setBEMod, modifyBEMod

#### Fertigkeiten/Vorteile
    getFreieFertigkeiten <Return: string[]>,
    getVorteile <Return: { name, wert, steigerungsfaktor, text, kosten, typ, voraussetzungen[], nachkauf, text }[]>,
    getFertigkeit/getÜbernatürlicheFertigkeit <Parameter: Fertigkeits-Name. Return: { name, wert, steigerungsfaktor, text, gekaufteTalente[],
        kampffertigkeit, attribute[3], attributswerte[3], basiswert, probenwert, probenwertTalent, voraussetzungen[], maxWert }>
    modifyFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>
    modifyÜbernatürlicheFertigkeitBasiswert : <Parameter: Fertigkeits-Name, Modifikator>
    modifyTalent : <Parameter: Fertigkeits-Name, Talent-Name, Bedingung, Modifikator>
        Beispiel: modifyTalent('Beeinflussung', 'Überreden', 'Rededuell', 2)
    
#### Kampfstile
    getKampfstil <Parameter: Kampfstil-Name. Return: { AT, VT, TP, RW, BE }>
    setKampfstil/modifyKampfstil <Parameter: Kampfstil-Name, AT, VT, TP, RW, BE>
    setKampfstilBEIgnore <Parameter: Kampfstil-Name, Fertigkeit-Name, Talent-Name>

#### Ausrüstung
    getAusrüstung <Return: string[]>, getRüstung <Return: { name, text, be, rs[6] }[]>,
    getWaffen <Return: { name, text, W6, plus, eigenschaften[], haerte, fertigkeit, talent, kampfstile[], kampfstil, rw, wm, lz}[]>
    Hinweis: Nur Fernkampfwaffen haben das Feld 'lz'.

#### Sonstiges
    addWaffeneigenschaft <Parameter: TalentName, Eigenschaft>
        Beispiel: addWaffeneigenschaft('Waffenlos', 'Kopflastig')
    
#### Waffeneigenschaften (WE)
Diese Funktionen stehen nur innerhalb von Waffeneigenschaft-Scripts zur Verfügung.

    Parameter dieser WE als string erhalten: getEigenschaftParam <Parameter: Parameternummer>. Parameter müssen mit Semikolon getrennt werden.  
    Waffen mit dieser WE modifizieren: modifyWaffeAT, modifyWaffeVT, modifyWaffeTPW6, modifyWaffeTPPlus, modifyWaffeHaerte, modifyWaffeRW, setWaffeAT, setWaffeVT, setWaffeTPW6, setWaffeTPPlus, setWaffeHaerte, setWaffeRW
	Aktuelle Werte der Waffe erhalten: getWaffenWerte <Return: { AT, VT, RW, TPW6, TPPlus, Haerte, Kampfstil }>
       
## Beispiele

#### Vorteil Waffenloser Kampf
    addWaffeneigenschaft('Unbewaffnet', 'Kopflastig'); addWaffeneigenschaft('Unbewaffnet', 'Wendig')
    Fügt allen Waffen, die mit dem Talent Unbewaffnet geführt werden, die Eigenschaften Kopflastig und Wendig hinzu

#### Vorteil Gefäß der Sterne
    modifyAsPMod(getCH() + 4)
Erhöht die AsP um den Charismawert + 4

#### Vorteil Reiterkampf II
    modifyKampfstil('Reiterkampf', 1, 1, 1, 0); setKampfstilBEIgnore('Reiterkampf', 'Athletik', 'Reiten')">
Erhöht für den Kampfstil Reiterkampf die Werte für TP, AT und VT um eins. Außerdem wird mit dem Kampfstil Reiterkampf die Behinderung ignoriert, falls die Waffe mit dem Talent Reiten der Fertigkeit Athletik geführt wird.

#### Waffeneigenschaft Kopflastig
    modifyWaffeTPPlus(getSchadensbonus())
Erhöht die TP aller Waffen mit dieser Eigenschaft um den Schadensbonus.

#### Waffeneigenschaft Schwer
    if getKK() < int(getEigenschaftParam(1)): modifyWaffeAT(-2); modifyWaffeVT(-2)
Verringert AT und VT aller Waffen mit dieser Eigenschaft um 2, falls der Wert der Körperkraft unter dem Wert des ersten Parameters der Eigenschaft liegt (bei Schwer(4) ist dies 4).