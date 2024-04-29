# Skripte für Abgeleitete Werte, Vorteile und Waffeneigenschaften
Abgeleitete Werte, Vorteile und Waffeneigenschaften haben im Regelbasis-Editor ein Feld für benutzerdefinierte Skripte. Diese werden verwendet, um Auswirkungen auf die Charakterwerte umzusetzen. Skripte werden in Python geschrieben.

## API
Sephrasto bietet eine Reihe von Funktionen an, anhand derer die meisten Skripte mit ein paar wenigen Zeichen umzusetzen sind. Prinzipiell können in Scripten lokale Variablen, mathematische Operatoren wie ```+-/*```, ```while```- und ```for```-Loop, ```if```-Statements, ```list``` bzw. ```[]``` und ```dict``` bzw. ```{}``` verwendet werden.

### Arithmetik
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|roundDown|float|wert : float|Den Parameter "wert" abrunden. Rundet auf die nächste ganze Zahl in Richtung 0 ab.|
|roundUp|float|wert : float|Den Parameter "wert" aufrunden. Rundet auf die nächst-größere (positive Zahlen)/-kleinere (negative Zahlen) ganze Zahl auf.|
|round|float|wert : float|Den Parameter "wert" runden. Rundet kaufmännisch zur nächsten ganzen Zahl (ab .5 auf, darunter ab).|
|max|float|wert : float, minimum : float|Den Parameter "wert" auf "minimum" beschränken. Wenn der Wert niedriger als "minimum" ist, wird "minimum" zurückgegeben.|
|min|float|wert : float, maximum : float|Den Parameter "wert" auf "maximum" beschränken. Wenn der Wert größer als "maximum" ist, wird "maximum" zurückgegeben.|
|clamp|float|wert : float, minimum : float, maximum : float|Den Parameter "wert" auf "minimum" und "maximum" beschränken. Wenn der Wert niedriger als "minimum" ist, wird "minimum" zurückgegeben, wenn er größer als "maximum" ist, "maximum".|
|sum|int oder float|zahlen : float\[\] oder int\[\]|Summiert die Liste "zahlen" zu einem Wert.|

### Charakterbeschreibung

| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|getName|str|-|Name erhalten|
|getSpezies|str|-|Spezies erhalten|
|getStatus|str|-|Status erhalten|
|getStatusIndex|int|-|Status-Index der Statusse-Einstellung erhalten|
|getKurzbeschreibung|str|-|Kurzbeschreibung erhalten|
|getHeimat|str|-|Heimat erhalten|
|getFinanzen|str|-|Finanzen erhalten|
|getFinanzenIndex|int|-|Finanzen-Index der Finanzen-Einstellung erhalten|
|getEigenheit|str|index : int {0-7}|Eigenheit an Stelle "index" erhalten|
|getEPGesamt|int|-|Name|
|getEPAusgegeben|int|-|Name|


### Attribute
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|getAttribut|int|name : str|Wert des Attributs "name" erhalten|
|getAttributProbenwert|int|name : str|Probenwert des Attributs "name" erhalten|
|getGE|int|-|GE-Wert erhalten|
|getGEProbenwert|int|-|GE-Probenwert erhalten|
|getKO|int|-|KO-Wert erhalten|
|...||||

**Hinweis:** Sephrasto stellt die API für alle Attribute nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Attribute. In der Standarddatenbank sind dies GE, KO, KK, FF, MU, IN, KL und CH.

### Energien
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|getAsPBasis|int|-|AsP-Basiswert erhalten. Wird in der Regel von Vorteilen verwendet, welche den Grundvorrat der Energie bereitstellen. Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|setAsPBasis|-|wert : int|AsP-Basiswert auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyAsPBasis|-|mod : int|AsP-Basiswert um "mod" modifizieren.|
|getAsPMod|int|-|AsP-Modifikator erhalten. Wird in der Regel von Vorteilen verwendet, welche die Energie zusätzlich zum Grundvorrat erhöhen. Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|setAsPMod|-|wert : int|AsP-Modifikator auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyAsP|-|mod : int|AsP-Modifikator um "mod" modifizieren.|
|getAsP|int|-|Den reinen reinen AsP-Steigerungswert erhalten.|
|getAsPGebunden|int|-|Die Menge an gAsP erhalten.|
|getAsPFinal|int|-|Den AsP-Gesamtwert erhalten (Basis + Mod. + Steigerung). Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|getKaPBasis|int|-|KaP-Basiswert erhalten. Wird in der Regel von Vorteilen verwendet, welche den Grundvorrat der Energie bereitstellen. Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|...||||

**Hinweis:** Sephrasto stellt die API für alle Energien nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Energien. In der Standarddatenbank sind dies AsP, KaP und GuP.

### Abgeleitete Werte
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|getWSBasis|int|-|WS-Basiswert erhalten. Wird durch das Script von WS berechnet.|
|getWSMod|int|-|WS-Modifikator erhalten. Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|setWSMod|-|wert : int|WS-Modifikator auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWS|-|mod : int|WS-Modifikator um "mod" modifizieren.|
|getWS|int|-|Den WS-Gesamtwert erhalten (Basis + Mod.). Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|getMRBasis|int|-|MR-Basiswert erhalten. Wird durch das Script von MR berechnet.|
|...||||

**Hinweis:** Sephrasto stellt die API für alle Abgeleiteten Werte nach obigem Muster automatisch bereit, also auch für in den Hausregeln neu hinzugefügte Abgeleitete Werte. In der Standarddatenbank sind dies WS, MR, GS, DH, SB, INI, RS, BE und SchiP. Der finale Wert (zum Beispiel mit der BE abgezogen) kann nicht abgefragt werden, seine Berechnung findet erst nach allen Scripts statt. 

### Fertigkeiten
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|**Freie Fertigkeiten**|
|freieFertigkeitenCount|int|-|Anzahl freier Fertigkeiten erhalten.|
|getFreieFertigkeit|str|index : int {0 - 27}|Freie Fertigkeit an Stelle "index" erhalten.|
|getFreieFertigkeitWert|int|index : int {0 - 27}|Wert von freier Fertigkeit an Stelle "index" erhalten.|
|**Profane Fertigkeiten**|
|hasFertigkeit|bool|name : str|Abfragen, ob Charakter Fertigkeit "name" besitzt.|
|getFertigkeitBasiswert|int|name : str|Basiswert der profanen Fertigkeit "name" erhalten.|
|getFertigkeitProbenwert|int|name : str|Probenwert der profanen Fertigkeit "name" erhalten.|
|getFertigkeitProbenwertTalent|int|name : str|Probenwert(Talent) der profanen Fertigkeit "name" erhalten.|
|modifyFertigkeitBasiswert|-|name : str, mod : int|Basiswert der profanen Fertigkeit "name" um "mod" modifizieren. Dies ist nützlich, um sich permanente Erleichterungen auf eine Fertigkeit nicht merken zu müssen. Diese Modifikation wird nur im Charakterbogen eingerechnet!|
|**Übernatürliche Fertigkeiten**|
|hasÜbernatürlicheFertigkeit|bool|name : str|Abfragen, ob Charakter übernatürliche Fertigkeit "name" besitzt.|
|getÜbernatürlicheFertigkeitBasiswert|int|name : str|Basiswert der übernatürlichen Fertigkeit "name" erhalten.|
|getÜbernatürlicheFertigkeitProbenwert|int|name : str|Probenwert der übernatürlichen Fertigkeit "name" erhalten. Dieser Wert wird bei übernatürlichen Fertigkeiten in der Regel nicht verwendet.|
|getÜbernatürlicheFertigkeitProbenwertTalent|int|name : str|Probenwert(Talent) der übernatürlichen Fertigkeit "name" erhalten.|
|modifyÜbernatürlicheFertigkeitBasiswert|-|name : str, mod : int|Basiswert der übernatürlichen Fertigkeit "name" um "mod" modifizieren. Dies ist nützlich, um sich permanente Erleichterungen auf eine Fertigkeit nicht merken zu müssen. Diese Modifikation wird nur im Charakterbogen eingerechnet!|

### Talente
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|hasTalent|bool|name : str|Abfragen, ob Charakter Talent "name" besitzt.|
|modifyTalentProbenwert|-|name : str, mod : int|Probenwert des Talents "name" um "mod" modifizieren. Dies ist nützlich, um permanente Erleichterungen auf ein Talent direkt in der Talentliste aufzuführen. Ist das Talent noch nicht erworben, wird das ganze Talent mit der Modifizierung in Klammern gesetzt. Die Modifizierung wird ausschließlich im Charakterbogen eingerechnet!|
|talentAddInfo|-|name : str, info : str|Fügt dem Talent "name" im Charakterbogen den Informationstext "info" hinzu. Dies ist nützlich, um besondere Effekte wie beispielsweise von manchen Vorteilen direkt bei den Talenten im Charakterbogen aufzuführen.|
|addTalent|-|name : str, kosten : int, kommentar : str|Fügt dem Charakter das Talent "name" zu regulären Kosten hinzu. Wenn das Script in einem Vorteil verwendet wird, wird der Vorteil dem neuen Talent, als Voraussetzung hinzugefügt. Sobald der Vorteil also abgewählt wird, verliert der Charakter auch das Talent. Wenn der Charakter das Talent bereits besitzt, werden Kosten und Kommentar angepasst, falls gesetzt. Mit dem "kosten"-Parameter können die EP-Kosten geändert werden (optional); bei -1 werden sie nicht verändert. Mit dem "kommentar"-Parameter kann ein Kommentar hinzugefügt werden, falls das Talent dies unterstützt (optional).|
|removeTalent|-|name : str|Entfernt das Talent "name", falls der Charakter es besitzt.|
|addTalentVoraussetzung|-|name : str, voraussetzung : str|Fügt dem Talent "name" die Voraussetzung "voraussetzung" hinzu (siehe [Datenbankeditor-Dokumentation](datenbankeditor.md)).|

### Vorteile
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|hasVorteil|bool|name : str|Abfragen, ob Charakter Vorteil "name" besitzt.|
|addVorteil|-|name : str, kosten : int, kommentar : str|Fügt dem Charakter den Vorteil "name" zu regulären Kosten hinzu. Wenn das Script in einem Vorteil verwendet wird, wird der Vorteil dem neuen Vorteil als Voraussetzung hinzugefügt. Sobald der Vorteil (der den neuen Vorteil verleiht) also abgewählt wird, verliert der Charakter auch den neuen Vorteil. Wenn der Charakter den Vorteil bereits besitzt, werden Kosten und Kommentar angepasst, falls gesetzt. Mit dem "kosten"-Parameter können die EP-Kosten geändert werden; bei -1 werden sie nicht verändert. Mit dem "kommentar"-Parameter kann ein Kommentar hinzugefügt werden, falls der Vorteil dies unterstützt.|
|removeVorteil|-|name : str|Entfernt den angegebenen Vorteil, falls der Charakter ihn besitzt.|
|addVorteilVoraussetzung|-|name : str, voraussetzung : str|Fügt dem Vorteil "name" die Voraussetzung "voraussetzung" hinzu (siehe [Datenbankeditor-Dokumentation](datenbankeditor.md)).|

### Kampfstile
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|getKampfstilAT|int|name : str|AT-Modifikator des Kampfstils "name" erhalten.|
|getKampfstilVT|int|name : str|VT-Modifikator des Kampfstils "name" erhalten.|
|getKampfstilTPPlus|int|name : str|Schadensbonus-Modifikator des Kampfstils "name" erhalten.|
|getKampfstilRW|int|name : str|RW-Modifikator des Kampfstils "name" erhalten.|
|getKampfstilBE|int|name : str|BE-Modifikator des Kampfstils "name" erhalten.|
|setKampfstil|-|name : str, at : int, vt : int, plus : int, rw : int, be : int|Modifikatoren des Kampfstils "name" auf "at", "vt", "plus", "rw" und "be" setzen.|
|modifyKampfstil|-|name : str, at : int, vt : int, plus : int, rw : int, be : int|Modifikatoren des Kampfstils "name" um "at", "vt", "plus", "rw" und "be" modifizieren.|

### Ausrüstung
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|**Inventar**|
|inventarCount|int|-|Anzahl an Inventargegenständen erhalten.|
|getInventar|str|index : int {0-19}|Inventar an Stelle "index" erhalten.|
|**Rüstungen**|
|rüstungenCount|int|-|Anzahl an Rüstungen erhalten.|
|getRüstung|str|index : int {0-2}|Name der Rüstung an Stelle "index" erhalten.|
|getRüstungRS|int|index : int {0-2}|RS der Rüstung an Stelle "index" erhalten.|
|getRüstungRSZone|int|index : int {0-2}, zone {0-5}|ZRS der Rüstung an Stelle "index" erhalten. 0=Beine, 1=Arm links, 2=Arm rechts, 3=Bauch, 4=Brust, 5=Kopf|
|getRüstungRSFinal|int|index : int {0-2}, zone {(-1)-5}|RS + RS-Modifikator der Rüstung an Stelle "index" erhalten. Dies ist der Gesamt-RS Falls für "zone" -1 angegeben wird, ansonsten: 0=Beine, 1=Arm links, 2=Arm rechts, 3=Bauch, 4=Brust, 5=Kopf. Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|getRüstungBE|int|index : int {0-2}|BE der Rüstung an Stelle "index" erhalten.|
|getRüstungBEFinal|int|index : int {0-2}|BE + BE-Modifikator der Rüstung an Stelle "index" erhalten. Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|getRüstungWSFinal|int|index : int {0-2}|WS + Gesamt-RS + RS-Modifikator der Rüstung an Stelle "index" erhalten. Der Wert kann je nach Scriptpriorität vom endgültigen Wert abweichen.|
|**Waffen**|
|waffenCount|int|-|Anzahl an Waffen erhalten.|
|getWaffe|str|index : int {0-7}|Name der Waffe an Stelle "index" erhalten.|
|getWaffeATMod|int|index : int {0-7}|AT-Modifikator der Waffe an Stelle "index" erhalten.|
|setWaffeAT|-|index : int {0-7}, wert : int|AT der Waffe an Stelle "index" auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWaffeAT|-|index : int {0-7}, mod : int|AT der Waffe an Stelle "index" um "mod" modifizieren.|
|getWaffeVTMod|int|index : int {0-7}|VT-Modifikator der Waffe an Stelle "index" erhalten.|
|setWaffeVT|-|index : int {0-7}, wert : int|VT der Waffe an Stelle "index" auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWaffeVT|-|index : int {0-7}, mod : int|VT der Waffe an Stelle "index" um "mod" modifizieren.|
|getWaffeRW|int|index : int {0-7}|RW der Waffe an Stelle "index" erhalten.|
|getWaffeRWMod|int|index : int {0-7}|RW-Modifikator der Waffe an Stelle "index" erhalten.|
|setWaffeRW|-|index : int {0-7}, wert : int|RW der Waffe an Stelle "index" auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWaffeRW|-|index : int {0-7}, mod : int|RW der Waffe an Stelle "index" um "mod" modifizieren.|
|getWaffeWM|int|index : int {0-7}|WM der Waffe an Stelle "index" erhalten.|
|getWaffeLZ|int|index : int {0-7}|LZ der Waffe an Stelle "index" erhalten.|
|getWaffeLZMod|int|index : int {0-7}|LZ-Modifikator der Waffe an Stelle "index" erhalten.|
|setWaffeLZ|-|index : int {0-7}, wert : int|LZ der Waffe an Stelle "index" auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWaffeLZ|-|index : int {0-7}, mod : int|LZ der Waffe an Stelle "index" um "mod" modifizieren.|
|getWaffeTPWürfel|int|index : int {0-7}|Die Anzahl Schadenswürfel der Waffe an Stelle "index" erhalten.|
|setWaffeTPWürfel|-|index : int {0-7}, wert : int|Anzahl Schadenswürfel der Waffe an Stelle "index" auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWaffeTPWürfel|-|index : int {0-7}, mod : int|Anzahl Schadenswürfel der Waffe an Stelle "index" um "mod" modifizieren.|
|getWaffeTPWürfelMod|int|index : int {0-7}|Schadenswürfelanzahl-Modifikator der Waffe an Stelle "index" erhalten.|
|getWaffeTPWürfelSeiten|int|index : int {0-7}|Die Seitenzahl der Schadenswürfel der Waffe an Stelle "index" erhalten.|
|getWaffeTPPlus|int|index : int {0-7}|Schadensbonus der Waffe an Stelle "index" erhalten.|
|getWaffeTPPlusMod|int|index : int {0-7}|Schadensbonus-Modifikator der Waffe an Stelle "index" erhalten.|
|setWaffeTPPlus|-|index : int {0-7}, wert : int|Schadensbonus der Waffe an Stelle "index" auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWaffeTPPlus|-|index : int {0-7}, mod : int|Schadensbonus der Waffe an Stelle "index" um "mod" modifizieren.|
|getWaffeHärte|int|index : int {0-7}|Härte der Waffe an Stelle "index" erhalten.|
|getWaffeHärteMod|int|index : int {0-7}|Härte-Modifikator der Waffe an Stelle "index" erhalten.|
|setWaffeHärte|-|index : int {0-7}, wert : int|Härte der Waffe an Stelle "index" auf "wert" setzen. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert.|
|modifyWaffeHärte|-|index : int {0-7}, mod : int|Härte der Waffe an Stelle "index" um "mod" modifizieren.|
|getWaffeEigenschaften|str\[\]|index : int {0-7}|Liste der Eigenschaften der Waffe an Stelle "index" erhalten.|
|getWaffeFertigkeit|str|index : int {0-7}|Fertigkeit der Waffe an Stelle "index" erhalten.|
|getWaffeTalent|str|index : int {0-7}|Talent der Waffe an Stelle "index" erhalten.|
|getWaffeKampfstil|str|index : int {0-7}|Kampfstil der Waffe an Stelle "index" erhalten. Wenn keiner gesetzt ist, wird "Kein Kampfstil" zurückgegeben.|
|getWaffeBESlot|int|index : int {0-7}|BE Slot der Waffe an Stelle "index" erhalten. Dies ist die Rüstungsnummer (1-3), deren BE für die Berechnung der Waffenwerte verwendet werden soll. 0 bedeutet keine Rüstung.|
|isWaffeNahkampf|bool|index : int {0-7}|Abfragen, ob Waffe an Stelle "index" eine Nahkampfwaffe ist.|
|isWaffeFernkampf|bool|index : int {0-7}|Abfragen, ob Waffe an Stelle "index" eine Fernkampfwaffe ist.|
|addWaffeneigenschaft|-|name : str, eigenschaft : str|Allen Waffen mit der Basiswaffe "name" die Eigenschaft "eigenschaft" hinzufügen.|
|removeWaffeneigenschaft|-|name : str, eigenschaft : str|Bei allen Waffen mit der Basiswaffe "name" die Eigenschaft "eigenschaft" entfernen.|

### Regeln
| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|addRegelInfo|-|name : str, info : str|Fügt der Regel "name" im Charakterbogen den Informationstext "info" hinzu. Dies ist nützlich, um besondere Effekte wie beispielsweise von manchen Vorteilen direkt bei den Regeln im Regelanhang des Charakterbogens aufzuführen.|

## Besonderheiten

### Waffeneigenschaften (WE)
Bei Waffeneigenschaften gilt Vorsicht bei der Nutzung der folgenden Scripts, da sie Berechnungen durcheinander bringen können: ```setSB, modifySB, setBE, modifyBE, setRS, modifyRS, modifyFertigkeitBasiswert, setKampfstil, modifyKampfstil, addWaffeneigenschaft, removeWaffeneigenschaft```.

Waffeneigenschaft-Scripts haben außerdem Zugriff auf zusätzliche Scripts:

| Script | Rückgabetyp | Parameter | Zweck |
|---|:---:|:---:|---|
|getEigenschaftParam|str|index: int| Den Parameter einer Waffeneigenschaft an Stelle "index" erhalten. Dieser wird immer als string zurückgegeben, sollte im Falle einer Zahl also gecastet werden, siehe Beispiele.|
|getWaffeIndex|int|-| Den index der Waffe erhalten, welche die Waffeneigenschaft mit diesem Script enthält. Essenziell für viele Eigenschaften, siehe Beispiele.|

## Beispiele


### Vorteil Waffenloser Kampf
```python
for waffe in ['Hand', 'Fuß']:
    addWaffeneigenschaft(waffe, 'Kopflastig')
    addWaffeneigenschaft(waffe, 'Wendig')
```
Fügt den Waffen Hand und Fuß die Eigenschaften Kopflastig und Wendig hinzu.


### Vorteil Gefäß der Sterne
```python
modifyAsP(getCH() + 4)
```
Erhöht die AsP um den Charismawert + 4.


### Vorteil Reiterkampf II
```python
modifyKampfstil('Reiterkampf', 1, 1, 1, 0, -1)
```
Erhöht für den Kampfstil Reiterkampf die Werte für AT, VT und TP um +1 und senkt die BE um -1.


### Waffeneigenschaft Kopflastig
```python
modifyWaffeTPPlus(getWaffeIndex(), getSB())
```
Erhöht die TP aller Waffen mit dieser Eigenschaft um den Schadensbonus.


### Waffeneigenschaft Schwer
```python
if getKK() < int(getEigenschaftParam(0)):
    modifyWaffeAT(-2)
	modifyWaffeVT(-2)
```
Verringert AT und VT aller Waffen mit dieser Eigenschaft um 2, falls der Wert der Körperkraft unter dem Wert des ersten Parameters der Eigenschaft liegt (bei Schwer(4) ist dies 4).
