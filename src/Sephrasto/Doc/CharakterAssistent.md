[Hilfe](Help.md) > Charakter Assistent

# Charakter Assistent
Der Charakter Assistent betreut dich beim Erstellen eines neuen Charakters. Es erscheint dann ein Popup mit dem man auf Basis von Vorlagen nach dem bekannten Spezies/Kultur/Profession-Prinzip Charaktere mit wenigen Clicks erstellen kann.
<br />
## Was ist aktuell enthalten?
- Ilaris
	* Spezies - enthalten Spezies-Vorteile strikt nach Regelwerk, zusätzlich Halbelfen und Halborks
	* Kulturen - enthalten die Heimat und Muttersprache
	* Professionen: kleine Basispakete, hauptsächlich interessant für Geweihte wegen den Segnungen; angepasste Professionen aus WeZwanzigs Archetypen-Schmiede, den offiziellen Ilaris Archetypen und den Archetypen von Baal Zephon.
- Weitere Kits zum Download:
	* [Ilaris Advanced Kit](https://dsaforum.de/viewtopic.php?f=180&t=49412)
<br />
## Wie erstelle ich eigene Vorlagen?
Neue Spezies/Kulturen/Professionen anzulegen ist trivial - einfach mit Sephrasto erstellen und im entsprechenden Ordner abspeichern (siehe "Ordnerstruktur"). Der Assistent lebt von Communitybeiträgen - sendet gerne eure Kreationen ein, damit wir sie aufnehmen können.
<br />
### Ordnerstruktur
Damit ihr eigene Kreationen mit dem nächsten Sephrasto-Update nicht verliert, kann der Charakterassistent auch Vorlagen aus eurem persönlichen Plugins-Ordner auslesen. Erstellt dazu in "%userprofile%/Dokumente/Sephrasto/Plugins" einen neuen Ordner "CharakterAssistent". Seht euch die genaue Ordnerstruktur am besten im Data-Ordner der Sephrastoinstallation an, aber hier nochmal der Vollständigkeit halber:<br />

- Alle Dateien müssen in den "CharakterAssistent"-Ordner.
- Jeder Ordner in "CharakterAssistent" ist ein eigener "Baukasten" und erhält einen entsprechenden Eintrag in der ersten Dropdownliste. Er kann beliebig benannt werden.
- Jeder Baukasten benötigt je einen Ordner "Spezies", "Kultur" und "Profession". "Profession" benötigt als einziger weitere (beliebig benannte) Unterordner, die der Dropdownliste "Professionskategorie" entsprechen.
- In die "Spezies"-, "Kultur"- und jeweiligen Professionskategorie-Ordner werden die entsprechenden Sephrasto-XMLs gespeichert.
<br />
## Wie werden S/K/P verschmolzen und was gibt es zu beachten?
- Das Spezies-Feld wird nur von der Spezies übernommen
- Das Heimat-Feld wird nur von der Kultur übernommen
- Name, Status und Finanzen werden nur vom letzten aus der Reihenfolge S/K/P übernommen
- Die Kurzbeschreibung enthält Geschlecht und die S/K/P Namen und wird mit in S/K/P eingetragenen Kurzbeschreibungen zusammengeführt
- Attribute: Attribute aus Spezies und Kultur werden addiert, bei Professionen sind Attribute Mindestwerte. Wenn also bei Spezies und Kultur Charisma jeweils +2 beträgt und bei der Profession +8, dann beträgt der Endwert +8.
- Vorteile und Talente: Alle Vorteile und Talente aus S/K/P werden hinzugefügt. Doppelt vergebene Vorteile/Talente werden ignoriert, außer bei solchen mit variablen Kosten - hier werden die Kosten addiert und die Kommentare zusammengeführt. Sonderfall: Wenn eine Spezies oder Profession das Gebräuche-Talent "Mittelreich" hinzufügen soll, dann muss die Heimat auf irgendetwas anderes gesetzt werden. Das macht nichts, da die Heimat eh nur von der Kultur übernommen wird.
- Fertigkeiten: Alle Fertigkeitswerte aus S/K/P werden addiert. Hierbei wird wie üblich das von den Attributen abhängige FW-Maximum beachtet.
- Freie Fertigkeiten: Alle Freien Fertigkeiten aus S/K/P werden hinzugefügt. Doppelt vergebene Freie Fertigkeiten werden addiert (max III), falls sie exakt gleich benannt sind - verwende für eine konsistente Benennung am besten unverändert die Einträge aus dem Freie Fertigkeiten-Auswahlfenster (falls verfügbar). Die erste (kostenlose) Freie Fertigkeit sollte nur in Kulturen ausgefüllt werden, da Kulturen die Muttersprache bestimmen.
- Eigenheiten und Ausrüstung: Alle werden aus S/K/P hinzugefügt. Doppelt vergebene Einträge werden ignoriert, falls sie exakt gleich benannt sind. Unbewaffnete Waffen wie "Hand" und "Fuß" sind abhängig von der Spezies und sollten dementsprechend dort eingetragen werden.
<br />
## tl;dr für eigene Professionen im Ilaris Baukasten?
- Lege dein EP-Budget fest. Die meisten Charaktere werden mit 2000 oder 2500 EP erstellt. Ziehe von diesem Budget 160 EP ab, damit genug EP für alle Spezies übrig bleiben (Orks kosten 160 EP).
- Erstelle einen neuen Charakter, speichere ihn ab als <Name der Profession>.xml in %userprofile%/Dokumente/Sephrasto/Plugins/CharakterAssistent/Ilaris/Profession/<Professions-Kategoriename>.
- Erstelle den Charakter wie gewöhnlich, mit folgenden Ausnahmen:
	* Lass alle Felder im Beschreibungs-Tab leer/wie sie sind, außer Finanzen. Trage Eigenheiten nur ein, wenn jeder Anhänger dieser Profession sie hat.
	* Je nach Geschmack kannst du auch einen vollwertigen Archetyp erstellen und Name und Eigenheiten vollständig ausfüllen. Füge den Charakternamen dann mit Bindestrich dem Dateinamen an.
	* Lass bei den Freien Fertigkeiten die erste (kostenlose) Fertigkeit frei, die Muttersprache wird von der Kultur befüllt. Nutze für Sprachen und Schriften unverändert die Eintragungen des Freie Fertigkeiten Auswahlfensters - Dopplungen durch die Muttersprache werden dann automatisch zusammengefasst.
	* Die Waffe Hand wird bereits automatisch durch die Spezies eingetragen.
<br />
## Kann ich Auswählmöglichkeiten wie in WdH einbauen?
Es ist möglich, dem Nutzer Auswahlmöglichkeiten (z.b. zwischen mehreren Talenten) via Popup anzubieten. Diese werden über eine zweite XML-Datei festgelegt, die aber leider von Hand geschrieben werden muss. Sehr viele Beispiele dafür gibt es im Ilaris Advanced Kit. Hier geht es zur Dokumentation: [Varianten und Auswahlmöglichkeiten](Varianten_Auswahlmöglichkeiten.md)
<br />
Falls übrigens jemand hierfür ein Tool schreiben möchte, darf er sich gerne melden! 
<br />
## Ich möchte andere Baukästen konvertieren, z.B. WdH, wie stelle ich das an?
- Spezies und Kulturen brauchen ein Basis-Niveau an Attributen, damit in Sephrasto Fertigkeiten über 2 gesteigert werden können und für dan Fall, dass stimmte Attribute z.B. anhand der Spezies in Relation niedriger ausfallen sollen. In Ilaris ist ein Attributswert von 3 durchschnittlich, dementsprechend setze ich standardmäßig bei **Spezies alle Attribute auf 2 und bei Kulturen alle auf 1**. Dies bietet genügend Spielraum für Attributssenkungen bei bestimmten S/K und für Fertigkeitssteigerungen.
- Manchmal reichen die Attributswerte dennoch nicht aus für den gewünschten FW. Beträgt dieser mindestens 2 Punkte mehr als möglich ist, dann vergebe ich stattdessen ein passendes Talent in der Fertigkeit.
- Manchmal ist man mit hohen Werten nur für ein bestimmtes Talent konfrontiert. Falls der konvertierte FW in diesem Fall 6 oder höher sein soll, dann sollte er stattdessen um 2 gesenkt und das entsprechende Talent gekauft werden. Beispiel: In WdH ist Schwerter +6 angegeben, was du gerne in Klingenwaffen +6 konvertieren würdest. Schwerter bezieht sich in DSA 4 nur auf Einhandwaffen. Der FW sollte also lieber auf +4 gesetzt und das Talent Einhandklingenwaffen gekauft werden. Wenn es sich um ein verbilligtes Talent handelt ggf. schon ab FW 5+ so verfahren.
- Wenn eine Auswahl konvertiert werden soll und eine der Wahlmöglichkeiten bereits komplett von der Vorlage abgedeckt ist, dann sollte die gesamte Auswahl einfach gestrichen werden. Bei einer teilweisen Abdeckung von Fertigkeiten kann der FW der entsprechenden Auswahlmöglichkeit gesenkt werden.


