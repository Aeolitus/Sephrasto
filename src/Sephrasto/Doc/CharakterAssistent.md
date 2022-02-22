[Hilfe](Help.md) > Charakter Assistent

# Charakter Assistent
Der Charakterassistent ist ein offizielles Plugin, mit eurer Sephrastoinstallation mitgeliefert wird. Wenn ihr einen neuen Charakter erstellt, erscheint ein Popup mit dem man auf Basis von Vorlagen nach dem bekannten Spezies/Kultur/Profession-Prinzip Charaktere mit wenigen Clicks erstellen kann. Aber auch bereits fertig erstellte Charaktere mit Namen, Eigenheiten usw. stehen als Archetypen zur Verfügung.
<br />
## Was ist aktuell enthalten?
- Ilaris S/K/P
	* Spezies - strikt nach Regelwerk + Halbelfen und Halborks
	* Kulturen - enthalten nur die Heimat + Muttersprache
	* Professionen: sehr kleine Basispakete, hauptsächlich interessant für Geweihte wegen den Segnungen; Professionspakete von WeZwanzigs Archetypen-Schmiede (leicht angepasst); Offizielle Ilaris Archetypen (aktualisiert); Archetypen von Baal Zephon (aktualisiert)
- Weitere Kits zum Download:
	* [Ilaris Advanced Kit](https://dsaforum.de/viewtopic.php?f=180&t=49412)
<br />
## Wie erstelle ich eigene Vorlagen?
Neue Spezies/Kulturen/Professionen anzulegen ist trivial - einfach mit Sephrasto erstellen und im entsprechenden Ordner abspeichern (siehe "Ordnerstruktur"). Der Assistent lebt von Communitybeiträgen - sendet mir gerne eure Kreationen, damit ich sie aufnehmen kann. Ich denke es wäre für viele insbesondere interessant, wenn jemand einen Ilaris Baukasten nach WdH anlegen würde.
<br />
### Ordnerstruktur
Damit ihr eigene Kreationen mit dem nächsten Sephrasto-Update nicht verliert, kann der Charakterassistent auch Vorlagen aus eurem persönlichen Plugins-Ordner auslesen. Erstellt in "%userprofile%/Dokumente/Sephrasto/Plugins" einen neuen Ordner "CharakterAssistent" und darin den Ordner "Data". Seht euch die genaue Ordnerstruktur am besten im Plugin-Ordner eurer Sephrastoinstallation an, aber hier nochmal der Vollständigkeit halber:<br />

- Alle Dateien müssen in den "Data"-Ordner.
- Jeder Ordner in "Data" ist ein eigener "Baukasten" und erhält einen entsprechenden Eintrag im ersten Dropdown. Die Benennung ist egal, bis auf einen Sonderfall (siehe unten).
- Jeder Baukasten benötigt je einen Ordner "Spezies", "Kultur" und "Profession". "Profession" benötigt als einziger weitere (beliebig benannte) Unterordner, die der "Professionskategorie" entsprechen.
- In die "Spezies"-, "Kultur"- und jeweiligen Professionskategorie-Ordner werden die entsprechenden Sephrasto-XMLs gespeichert.
<br />
## Wie werden S/K/P verschmolzen?
- Attribute: S und K werden addiert, bei P sind Attribute Mindestwerte. Wenn also bei S und K Charisma jeweils +2 beträgt und bei P +8, dann beträgt der Endwert +8.
- Vorteile + Talente: Werden von S/K/P appliziert. Doppelt vergebene Vorteile/Talente werden ignoriert, außer bei solchen mit variablen Kosten - hier werden die Kosten addiert und die Kommentare zusammengeführt.
- Fertigkeiten: Fertigkeitswerte werden von S/K/P addiert.
- Freie Fertigkeiten: Werden von S/K/P appliziert, sofern Sephrasto eine ausreichende Anzahl an Feldern bietet. Doppelt vergebene Freie Fertigkeiten werden addiert (max III).
- Eigenheiten, Ausrüstung, Inventar: Werden von S/K/P appliziert, sofern Sephrasto eine ausreichende Anzahl an Feldern bietet. Doppelt vergebene Einträge werden ignoriert, hier wird anhand des Namens verglichen.
- Das Spezies-Feld wird nur von der Spezies übernommen
- Das Heimat-Feld wird nur von der Kultur übernommen
- Name, Status und Finanzen werden nur vom letzten aus der Reihenfolge S/K/P übernommen
- Die Kurzbeschreibung enthält Geschlecht und die S/K/P Namen und wird mit in S/K/P eingetragenen Kurzbeschreibungen zusammengeführt
- Sonderfall: Wenn eine Spezies oder Profession das Gebräuche-Talent "Mittelreich" hinzufügen soll, dann muss die Heimat auf irgendetwas anderes gesetzt werden. Das macht nichts, da die Heimat eh nur von der Kultur übernommen wird.
<br />
## Kann ich Auswählmöglichkeiten wie in WdH realisieren?
Es ist möglich, dem Nutzer Auswahlmöglichkeiten (z.b. zwischen mehreren Talenten) via Popup anzubieten. Diese werden über eine zweite XML-Datei festgelegt, die aber leider von Hand geschrieben werden muss. Sehr viele Beispiele dafür gibt es im Ilaris Advanced Kit. Hier geht es zur Dokumentation: [Varianten und Auswahlmöglichkeiten](Varianten_Auswahlmöglichkeiten.md)
<br />
PS: Ich habe leider keine Zeit hier ein Tool für zu schreiben. Falls das jemand machen möchte - gerne! 
<br />
## Sollte ich sonst noch etwas beachten?
- Spezies und Kulturen brauchen ein Basis-Niveau an Attributen, damit in Sephrasto Fertigkeiten über 2 gesteigert werden können und für dan Fall, dass stimmte Attribute z.B. anhand der Spezies in Relation niedriger ausfallen sollen. In Ilaris ist ein Attributswert von 3 durchschnittlich, dementsprechend setze ich standardmäßig bei **Spezies alle Attribute auf 2 und bei Kulturen alle auf 1**. Dies bietet genügend Spielraum für Attributssenkungen bei bestimmten S/K und für Fertigkeitssteigerungen.
- Manchmal reichen die Attributswerte dennoch nicht aus für den gewünschten FW. Beträgt dieser mindestens 2 Punkte mehr als möglich ist, dann vergebe ich stattdessen ein passendes Talent in der Fertigkeit.
- Unbewaffnete "Waffen" sind abhängig von der Spezies und sollten dementsprechend dort eingetragen werden, nicht bei Professionen. Das spart Arbeit und man vergisst es nicht mehr.
- Wenn ein hoher FW (6+) gewünscht ist, sich aber nur auf ein bestimmtest Talent beziehen soll, dann sollte der gewünschte FW um 2 gesenkt und das entsprechende Talent gekauft werden. Beispiel: gewünscht ist Einhandklingenwaffen +6 und Zweihandklingenwaffen +4. Der FW sollte auf +4 gesetzt und das Talent Einhandklingenwaffen gekauft werden. Wenn es sich um ein verbilligtes Talent handelt ggf. schon ab FW 5+ so verfahren.
- Wenn eine Auswahl gewünscht ist und eine der Wahlmöglichkeiten bereits durch eine Fertigkeit abgedeckt ist, dann sollte die Auswahl einfach gestrichen werden
- Die erste (kostenlose) Freie Fertigkeit sollte nur in Kulturen ausgefüllt werden, da Kulturen die Muttersprache bestimmen. (Ilaris Advanced: auch die zweite Freie Fertigkeit, hier kommt die Kulturkunde rein)
- Damit doppelt vergebene Freie Fertigkeiten erkannt werden können, müssen sie konsistent benannt werden. Verwendet für maximale Kompabilität am besten unverändert die Einträge aus dem Freie Fertigkeiten-Auswahlfenster.

