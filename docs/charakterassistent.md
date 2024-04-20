# Charakter Assistent
Der Charakter Assistent betreut dich beim Erstellen eines neuen Charakters. Es erscheint dann ein Popup mit dem man auf Basis von Vorlagen nach dem bekannten Spezies/Kultur/Profession-Prinzip Charaktere mit wenigen Clicks erstellen kann.

## Was ist aktuell enthalten?
- Spezies: enthalten Spezies-Vorteile strikt nach Regelwerk, zusätzlich Halbelfen und Halborks
- Kulturen: enthalten die Heimat und Muttersprache
- Professionen: kleine Basispakete, hauptsächlich interessant für Geweihte wegen den Segnungen; angepasste Professionen aus WeZwanzigs Archetypen-Schmiede, den offiziellen Ilaris Archetypen und den Archetypen von Baal Zephon.

## Wie erstelle ich eigene Vorlagen?
Neue Spezies/Kulturen/Professionen anzulegen ist trivial - einfach mit Sephrasto erstellen und im entsprechenden Ordner abspeichern (siehe "Ordnerstruktur"). Der Assistent lebt von Communitybeiträgen - sendet gerne eure Kreationen ein, damit wir sie aufnehmen können.

### Ordnerstruktur
Damit ihr eigene Kreationen mit dem nächsten Sephrasto-Update nicht verliert, kann der Charakterassistent auch Vorlagen aus eurem persönlichen Plugins-Ordner auslesen. Erstellt dazu in "%userprofile%/Dokumente/Sephrasto/Plugins" einen neuen Ordner "CharakterAssistent". Seht euch die genaue Ordnerstruktur am besten im Data-Ordner der Sephrastoinstallation an, aber hier nochmal der Vollständigkeit halber:

- Alle Dateien müssen in den "CharakterAssistent"-Ordner.
- Jeder Ordner in "CharakterAssistent" ist ein eigener "Baukasten" und erhält einen entsprechenden Eintrag in der ersten Dropdownliste. Er kann beliebig benannt werden.
- Jeder Baukasten benötigt je einen Ordner "Spezies", "Kultur" und "Profession". "Profession" benötigt als einziger weitere (beliebig benannte) Unterordner, die der Dropdownliste "Professionskategorie" entsprechen.
- In die "Spezies"-, "Kultur"- und jeweiligen Professionskategorie-Ordner werden die entsprechenden Sephrasto-XMLs gespeichert.

## Wie werden S/K/P verschmolzen und was gibt es zu beachten?
- Das Spezies-Feld wird nur von der Spezies übernommen
- Das Heimat-Feld wird nur von der Kultur übernommen
- Name, Status und Finanzen werden nur vom letzten aus der Reihenfolge S/K/P übernommen
- Die Kurzbeschreibung enthält Geschlecht und die S/K/P Namen und wird mit in S/K/P eingetragenen Kurzbeschreibungen zusammengeführt
- Attribute: Attribute aus Spezies und Kultur werden addiert, bei Professionen sind Attribute Mindestwerte. Wenn also bei Spezies und Kultur Charisma jeweils +2 beträgt und bei der Profession +8, dann beträgt der Endwert +8.
- Vorteile und Talente: Alle Vorteile und Talente aus S/K/P werden hinzugefügt. Doppelt vergebene Vorteile/Talente werden ignoriert, außer bei solchen mit variablen Kosten - hier werden die Kosten addiert und die Kommentare zusammengeführt. Sonderfall: Wenn eine Spezies oder Profession das Gebräuche-Talent "Mittelreich" hinzufügen soll, dann muss die Heimat auf irgendetwas anderes gesetzt werden. Das macht nichts, da die Heimat eh nur von der Kultur übernommen wird.
- Fertigkeiten: Alle Fertigkeitswerte aus S/K/P werden addiert. Hierbei wird wie üblich das von den Attributen abhängige FW-Maximum beachtet.
- Freie Fertigkeiten: Alle Freien Fertigkeiten aus S/K/P werden hinzugefügt. Doppelt vergebene Freie Fertigkeiten werden addiert (max III), falls sie exakt gleich benannt sind - verwende für eine konsistente Benennung am besten unverändert die Einträge aus dem Freie Fertigkeiten-Auswahlfenster (falls verfügbar). Die erste (kostenlose) Freie Fertigkeit sollte nur in Kulturen ausgefüllt werden, da Kulturen die Muttersprache bestimmen.
- Eigenheiten und Ausrüstung: Alle werden aus S/K/P hinzugefügt. Doppelt vergebene Einträge werden ignoriert, falls sie exakt gleich benannt sind. In der Datenbank eingestellte Standardwaffen werden von Sephrasto automatisch eingetragen (normalerweise die Waffe Hand) und sollten ausgelassen werden.

## tl;dr für eigene Professionen im Ilaris Baukasten?
- Lege dein EP-Budget fest. Die meisten Charaktere werden mit 2000 oder 2500 EP erstellt. Ziehe von diesem Budget 160 EP ab, damit genug EP für alle Spezies übrig bleiben (Orks kosten 160 EP).
- Erstelle einen neuen Charakter, speichere ihn ab als \<Name der Profession\>.xml in %userprofile%/Dokumente/Sephrasto/Plugins/CharakterAssistent/Ilaris/Profession/\<Professions-Kategoriename\>.
- Erstelle den Charakter wie gewöhnlich, mit folgenden Ausnahmen:
	* Lass alle Felder im Beschreibungs-Tab leer/wie sie sind, außer Finanzen. Trage Eigenheiten nur ein, wenn jeder Anhänger dieser Profession sie hat.
	* Je nach Geschmack kannst du auch einen vollwertigen Archetyp erstellen und Name und Eigenheiten vollständig ausfüllen. Füge den Charakternamen dann mit Bindestrich dem Dateinamen an.
	* Lass bei den Freien Fertigkeiten die erste (kostenlose) Fertigkeit frei, die Muttersprache wird von der Kultur befüllt. Nutze für Sprachen und Schriften unverändert die Eintragungen des Freie Fertigkeiten Auswahlfensters - Dopplungen durch die Muttersprache werden dann automatisch zusammengefasst.
	* Die Waffe Hand wird bereits automatisch durch die Spezies eingetragen.

## Ich möchte andere Baukästen konvertieren, z.B. WdH, wie stelle ich das an?
- Spezies und Kulturen brauchen ein Basis-Niveau an Attributen, damit in Sephrasto Fertigkeiten über 2 gesteigert werden können und für dan Fall, dass stimmte Attribute z.B. anhand der Spezies in Relation niedriger ausfallen sollen. In Ilaris ist ein Attributswert von 3 durchschnittlich, dementsprechend setze ich standardmäßig bei **Spezies alle Attribute auf 2 und bei Kulturen alle auf 1**. Dies bietet genügend Spielraum für Attributssenkungen bei bestimmten S/K und für Fertigkeitssteigerungen.
- Manchmal reichen die Attributswerte dennoch nicht aus für den gewünschten FW. Beträgt dieser mindestens 2 Punkte mehr als möglich ist, dann vergebe ich stattdessen ein passendes Talent in der Fertigkeit.
- Manchmal ist man mit hohen Werten nur für ein bestimmtes Talent konfrontiert. Falls der konvertierte FW in diesem Fall 6 oder höher sein soll, dann sollte er stattdessen um 2 gesenkt und das entsprechende Talent gekauft werden. Beispiel: In WdH ist Schwerter +6 angegeben, was du gerne in Klingenwaffen +6 konvertieren würdest. Schwerter bezieht sich in DSA 4 nur auf Einhandwaffen. Der FW sollte also lieber auf +4 gesetzt und das Talent Einhandklingenwaffen gekauft werden. Wenn es sich um ein verbilligtes Talent handelt ggf. schon ab FW 5+ so verfahren.
- Wenn eine Auswahl konvertiert werden soll und eine der Wahlmöglichkeiten bereits komplett von der Vorlage abgedeckt ist, dann sollte die gesamte Auswahl einfach gestrichen werden. Bei einer teilweisen Abdeckung von Fertigkeiten kann der FW der entsprechenden Auswahlmöglichkeit gesenkt werden.

## Kann ich Auswählmöglichkeiten einbauen?
Es ist möglich, dem Nutzer Auswahlmöglichkeiten via Popup anzubieten. Dies ist eine zweite XML-Datei, die gleich benannt ist, wie die jeweilige S/K/P, enthält aber zusätzlich "_var" am Ende, z.B. "Halbelf_var.xml". Diese Datei muss leider von Hand geschrieben werden. Du kannst die Dateien auf Korrektheit überprüfen, indem du im Datenbankeditor-Menu "Analysieren -> Charakter Assistent" auswählst.

**Beispiel 1:**
```xml
<Charakter>
  <Auswahl>
    <Attribut name="KK" wert="3"/>
    <Fertigkeit name="Schusswaffen" wert="2"/>
    <Übernatürliche-Fertigkeit name="Einfluss" wert="2"/>
    <Freie-Fertigkeit name="Sprache: Garethi" wert="2"/>
    <Talent name="Armbrüste"/>
    <Talent name="Adlerschwinge Wolfsgestalt" wert="40" kommentar="Wolf"/>
    <Vorteil name="Schildkampf I"/>
    <Vorteil name="Tierempathie" wert="20" kommentar="Pferde"/>
    <Eigenheit name="Streiter der Göttin"/> 
  </Auswahl>
  <Auswahl>
    <Fertigkeit name="Schusswaffen" wert="1"/>
    <Fertigkeit name="Athletik" wert="2"/>
  </Auswahl>
</Charakter>
```

Es erscheint ein Popup, bei dem der Nutzer sich zwischen KK +3, Schusswaffen +2, etc. entscheiden muss. Die Attribute "wert" und "kommentar" werden nur bei Talenten und Vorteilen mit variablen Kosten benötigt.<br>
Danach erscheint ein weiteres Popup, bei dem er sich zwischen Schusswaffen +1 und Athletik +2 entscheiden muss. Hat er bei der ersten Auswahl bereits Schusswaffen gewählt, so wird diese Fertigkeit aus Folge-Auswahlen entfernt. Da in diesem Fall die zweite Auswhal nur noch Athletik +2 enthält, wird dies automatisch appliziert und es erscheint kein zweites Popup.

**Beispiel 2, Spezies Halbelf:**
```xml
<Charakter>
  <Varianten>
    <Variante name="Firnelfische Abstammung">
      <Vorteil name="Resistenz gegen Kälte"/>
      <Fertigkeit name="Überleben" wert="1"/>
    </Variante>
    <Variante name="Nivesische Abstammung">
      <Attribut name="IN" wert="1"/>
    </Variante>
    <Variante name="Thorwalsche Abstammung">
      <Attribut name="GE" wert="-1"/>
      <Attribut name="KK" wert="1"/>
    </Variante>
  </Varianten>

  <Auswahl keine-varianten="0,1">
    <Vorteil name="Gut Aussehend"/>
  </Auswahl>
   
  <Auswahl varianten="2">
    <Vorteil name="Selbstbeherrschung" wert="1"/>
    <Vorteil name="Athletik" wert="1"/>
  </Auswahl>
</Charakter>
```

Eine Variante kann nur in einem Varianten-Element existieren. Sie verhält sich gleich wie eine Auswahl, nur werden alle Child-Elemente appliziert. Es erscheint ein Popup, bei dem der Nutzer die drei Varianten Firnelfische, Nivesische und Thorwalsche Abstammung zur Auswahl erhält, hierbei kann er auch keine oder mehrere auswählen.<br>
Die erste Auswahl hat nur ein Element, zeigt also niemals ein Popup. Durch das Attribut "keine-varianten" wird Gut Aussehend allerdings nur appliziert, wenn nicht die Variante an Index 0 (Firnelfische Abstammung) oder 1 (Nivesische Abstammung) ausgewählt wurde. Es wird auch dann appliziert, wenn garkeine Variante ausgewählt wurde.<br>
Die zweite Auswahl ist nur aktiv, wenn die Variante an Index 2 (Thorwalsche Abstammung) gewählt wurde - nur dann erscheint ein Popup, bei dem der Nutzer sich zwischen Selbstbeherrschung und Athletik entscheiden muss. Innerhalb von "Variante" ist keine Auswahl möglich (Variante appliziert immer alle Elemente) - mit dieser Methode können auch Varianten Auswahlmöglichkeiten bieten.

**Beispiel 3, Spezies Orks:**
```xml
<Charakter>
  <Varianten pflichtwahl="1">
    <Variante name="Mann" beschreibung="" geschlecht="männlich">
      <Eigenheit name="Jähzorn"/>
    </Variante>
    <Variante name="Frau" beschreibung="" geschlecht="weiblich">
      <Attribut name="MU" wert="-2"/>
      <Attribut name="KO" wert="-1"/>
      <Attribut name="KK" wert="-1"/>
    </Variante>
  </Varianten>
</Charakter>
```

Durch das Attribut "pflichtwahl" muss eine der Varianten ausgewählt werden, eine Mehrfachauswahl ist nicht möglich.<br>
Das Attribut "geschlecht" kann mit den "männlich" oder "weiblich" bei Variante und Auswahl genutzt werden, um diese zu entfernen, wenn im Hauptfenster das entsprechende Geschlecht nicht ausgewählt wurde.<br>
Das Attribut "beschreibung" kann genutzt werden um im Spezies-/Kurzbeschreibungsfeld neben dem Namen eine zusätzliche Beschreibung einzufügen, die nicht um Popup angezeigt wird. Falls das Attribut wie hier mit einem leeren Inhalt eingefügt wird, dann wird die Variante überhaupt nicht in das entsprechende Feld eingetragen.<br>
Da es sich in diesem Beispiel um eine Pflichtwahl handelt, bei der immer nur eine Variante - Mann oder Frau - bestehen bleiben kann, wird die entsprechende Variante automatisch appliziert und kein Popup angezeigt.

**Beispiel 3, Profession Geode:**
```xml
<Charakter>
  <Auswahl>
    <Vorteil name="Magieabweisend" wert="-1"/>
  </Auswahl>
</Charakter>
```

Geoden sind üblicherweise Zwerge, sollten aber den Vorteil Magieabweisend dieser Spezies nicht haben. Bei Vorteilen und Talenten kann der Wert auf -1 gesetzt werden, wodurch diese entfernt werden, falls vorhanden.

