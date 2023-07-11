[Hilfe](Help.md) > Eigene Charakterbögen erstellen

# Eigene Charakterbögen erstellen
Du kannst Sephrasto weitere Charakterbögen hinzufügen. Kopiere deinen Bogen hierzu einfach in den Charakterbögen-Ordner, der in den Einstellungen von Sephrasto konfiguriert ist. Du musst Sephrasto allerdings noch ein paar Informationen zu deinem Bogen geben in Form einer Konfigurationsdatei. Diese ist eine Textdatei mit dem gleichen Namen wie die PDF-Datei, aber mit der Endung ".ini". Am einfachsten ist es, wenn du erstmal eine der bestehenden Konfigurationsdateien dorthin kopierst und entsprechend umbenennst. Diese findest du in deinem Sephrasto-Installationsordner im Unterordner Data/Charakterbögen. Alle Konfigurationsmöglichkeiten sind optional.
<br />
## Charakterbogen-Konfiguration
<br />
Info: "Bester Charakterbogen"<br />
-> Tooltip, der im Info-Tab angezeigt wird.<br />
<br />
Datei: "Charakterbogen.pdf"<br />
-> Falls der Charakterbogen nicht gleich heisst wie die Konfigurationsdatei, kannst du hiermit den Namen der PDF-Datei angeben. Sie sollte dennoch im gleichen Ordner oder einem Unterordner der Konfig liegen.<br />
<br />
Seitengrösse: A4<br />
-> Legt die Seitengröße fest. Die üblichsten Werte sind A4, A5 und Letter - alle weiteren mögliche Werte können hier gefunden werden: <a href="https://doc.qt.io/qt-6/qpagesize.html">QPageSize</a><br />
<br />
Seitenorientierung: Portrait<br />
-> Legt die Orientierung der Regelanhangseiten fest, mögliche Werte sind "Portrait" und "Landscape".<br />
<br />
Seitenbeschreibungen:<br />
- Deckblatt<br />
- Kampf<br />
-> Die Beschreibungen werden für die Benennung der PDF-Lesezeichen verwendet. Jeder Eintrag entspricht einer Seite.<br />
<br />
MaxVorteile: 24<br />
-> Die Anzahl an Formularfeldern für Vorteile.<br />
<br />
MaxVorteileProFeld: 3<br />
-> Wenn mehr Vorteile als MaxVorteile vorhanden sind, trägt Sephrasto bis zu MaxVorteileProFeld in jedes Feld ein.<br />
<br />
MaxKampfVorteile: 16<br />
-> Die Anzahl an Formularfeldern für Kampfvorteile.<br />
<br />
MaxKampfVorteileProFeld: 3<br />
-> Wenn mehr Kampfvorteile als MaxKampfVorteile vorhanden sind, trägt Sephrasto bis zu MaxKampfVorteileProFeld in jedes Feld ein.<br />
<br />
MaxÜbernatürlicheVorteile: 12<br />
-> Die Anzahl an Formularfeldern für Übernatürliche Vorteile.<br />
<br />
MaxÜberVorteileProFeld: 3<br />
-> Wenn mehr übernatürliche Vorteile als MaxÜbernatürlicheVorteile vorhanden sind, trägt Sephrasto bis zu MaxÜberVorteileProFeld in jedes Feld ein.<br />
<br />
MaxFreieFertigkeiten: 28<br />
-> Die Anzahl an Formularfeldern für Freie Fertigkeiten.<br />
<br />
MaxFreieProFeld: 3<br />
-> Wenn mehr Freie Fertigkeiten als MaxFreieFertigkeiten vorhanden sind, trägt Sephrasto bis zu MaxFreieProFeld in jedes Feld ein.<br />
<br />
MaxFertigkeiten: 28<br />
-> Die Anzahl an Formularfeldern für Fertigkeiten.<br />
<br />
MaxÜbernatürlicheFertigkeiten: 12<br />
-> Die Anzahl an Formularfeldern für Übernatürliche Fertigkeiten.<br />
<br />
MaxÜbernatürlicheTalente: 30<br />
-> Die Anzahl an Formularfeldern für übernatürliche Talente.<br />
<br />
ÜberSeite: 3<br />
-> Die Seitenzahl der Seite für übernatürliche Fertigkeiten und Vorteile, falls vorhanden. Seiten die darüber hinausgehen werden bei profanen Charakteren abgeschnitten - Sephrasto geht also davon aus, dass übernatürliches zum Schluss kommt.<br />
<br />
ÜberFertigkeitenZuProfan: False<br />
-> Hiermit werden übernatürliche Fertigkeiten bei den profanen Fertigkeiten eingetragen.<br />
<br />
ÜberVorteileZuKampf: False<br />
-> Hiermit werden übernatürliche Vorteile bei den Kampfvorteilen eingetragen.<br />
<br />
ExtraÜberSeiten: True<br />
-> Hiermit kann die Ausgabe von Extra-Seiten (z.B. bei zu vielen Zaubern) deaktiviert werden. Es wird hierfür immer die Seite [ÜberSeite] verwendet, also die Seite für Übernatürliches.<br />
<br />
Bild:<br />
- [1.0, 115.55, 89.55]<br />
- []<br />
- [1.5, 130.8, 74.0]<br />
-> Mit diesem Eintrag kannst du das Charakterbild auf einer oder mehreren Seiten an unterschiedlichen Stellen einfügen. Die Seitenzahl entspricht dem Listen-Index +1. Die einzelnen Elemente enthalten einen Array mit 3 Werten: Größenmultiplikator, X-Offset und Y-Offset (jeweils von der Ecke oben-links des Dokuments). Füge einen leeren Array ein, um eine Seite zu überspringen (im Beispiel wird ein Bild auf den Seiten 1 und 3 eingefügt). Es kann ein paar Export-Versuche benötigen, bis du gute Größen- und Offsetwerte für deinen Charakterbogen gefunden hast - nutze zum Testen idealerweise ein einfarbiges Bild mit einer Auflösung von 260 x 340. Nach Änderungen musst du Sephrasto neustarten.<br />
<br />
RegelanhangSeitengrösse: A4<br />
-> Legt die Seitengröße für den Regelanhang fest. Die üblichsten Werte sind A4, A5 und Letter - alle weiteren mögliche Werte können hier gefunden werden: <a href="https://doc.qt.io/qt-6/qpagesize.html">QPageSize</a><br />
<br />
RegelanhangSeitenorientierung: Portrait<br />
-> Legt die Orientierung der Regelanhangseiten fest, mögliche Werte sind "Portrait" und "Landscape".<br />
<br />
RegelanhangSeitenabstände: [70, 36, 70, 36]<br />
-> Legt den Abstand des Regelanhangtexts zum Seitenrand in der Einheit Points fest. Die Reihenfolge ist oben, rechts, unten, links.<br />
<br />
RegelanhangSeitenzahlPosition: bottom<br />
-> Legt fest, an welchem Seitenrand die Regelanhang-Seitenzahlen verankert werden sollen. Möglich sind: top, topleft, topright, left, bottomleft, bottom, bottomright, right, diagonal, reverse-diagonal, center.<br />
<br />
RegelanhangSeitenzahlAbstand: 40<br />
-> Legt den Abstand der Regelanhang-Seitenzahlen von der gewählten Verankerung in der Einheit Points fest.<br />
<br />
FormularMappings:<br />
&nbsp;&nbsp;&nbsp;&nbsp;Status: Statu<br />
&nbsp;&nbsp;&nbsp;&nbsp;WS: Wundschwelle <br />
-> Falls die Formularfelder im Charakterbogen nicht so benannt sind, wie Sephrasto das erwartet, können mit dieser Einstellung die Namen angepasst werden. Links vom Doppelpunkt steht der von Sephrasto erwartete Name, rechts der Name des Formularfelds im Charakterbogen.
<br />

## Formularfelder
Sephrasto befüllt die folgenden Formularfelder. In Eckigen Klammern befindet sich ggf. die Anzahl der Felder - "Eigen[1-8]" heißt beispielsweise, dass die Felder "Eigen1", "Eigen2" bis "Eigen8" befüllt werden. Ein "x" bedeutet hier, dass soviele Felder ausgegeben werden wie dein Charakterbogen unterstützt. Ein kleines "m" am Ende der Feldnamen ist mit einem "\*" gleichzusetzen, es handelt sich also um den durch BE modifizierten Wert. Falls der Feldname nicht eindeutig ist befindet sich in Klammern noch eine kurze Beschreibung; checkbox bedeutet hier, dass ein Checkbox-Formularfeld statt eines Textfelds erwartet wird. Alle Felder sind optional.

- Name
- Spezies
- Kultur
- Status
- Finanzen
- Kurzb (Kurzbeschreibung)
- Eigen[1-8] (Eigenheit)
- [Attribut-Name] (Attributswert, z. B. KO)
- [Attribut-Name]PW (Attributs-PW, z. B. KOPW)
- [Abgeleiteter Wert-Name]Basis (unmodifizierter Abgeleiteter Wert, z. B. GSBasis)
- [Abgeleiteter Wert-Name] (modifizierter Abgeleiteter Wert, z. B. GS)
- [Abgeleiteter Wert-Name]m (final modifizierter Abgeleiteter Wert, z. B. GSm)
- [Energie-Name]Basis (Basiswert der Energie - üblicherweise durch Vorteile wie Zauberer, z. B. AsPBasis)
- [Energie-Name] (Gesamtwert der Energie, z. B. AsP)
- Mod[Energie-Name] (zugekaufte Energie-Punkte, z. B. modAsP)
- EN (alle Energie-Gesamtwerte zusammengefasst)
- Vorteil[Vorteil-Name] (checkbox; Name enthält keine Leerzeichen und Sonderzeichen (ä, ö, ü, ß) werden ersetzt (ae, ou, ue, ss); z. B. VorteilGefaessderSterne)
- Vorteil[1-x]
- Kampfvorteil[1-x]
- Uebervorteil[1-x]
- Fertigkeit[1-x]NA (Name)
- Fertigkeit[1-x]FA (Steigerungsfaktor)
- Fertigkeit[1-x]AT (Attribute)
- Fertigkeit[1-x]BA (Basiswert)
- Fertigkeit[1-x]FW (Fertigkeitswert)
- Fertigkeit[1-x]TA (Talente)
- Fertigkeit[1-x]PW (Probenwert)
- Fertigkeit[1-x]PWT (Probenwert mit Talent)
- Frei[1-x] (Freie Fertigkeiten)
- Ruest[1-3]NA (Rüstungsname)
- Ruest[1-3]RS
- Ruest[1-3]BE
- Ruest[1-3]WS
- Ruest[1-3]RSBein
- Ruest[1-3]RSlArm
- Ruest[1-3]RSrArm
- Ruest[1-3]RSBauch
- Ruest[1-3]RSBrust
- Ruest[1-3]RSKopf
- Waffe[1-8]NA (Waffenname)
- Waffe[1-8]TP
- Waffe[1-8]HA (Härte)
- Waffe[1-8]EI (Eigenschaften)
- Waffe[1-8]ATm
- Waffe[1-8]VTm
- Waffe[1-8]RW
- Waffe[1-8]WM
- Waffe[1-8]TPm
- Ausruestung[1-20]
- Ueberfer[1-x]NA (Übernatürliche Fertigkeit Name)
- Ueberfer[1-x]FA (Steigerungsfaktor)
- Ueberfer[1-x]AT (Attribute)
- Ueberfer[1-x]FW (Fertigkeitswert)
- Ueberfer[1-x]PW (Probenwert)
- Ueberfer[1-x]BA (Basiswert)
- Uebertal[1-x]NA (Übernatürliches Talent Name)
- Uebertal[1-x]SE (Seite)
- Uebertal[1-x]PW (Probenwert)
- Uebertal[1-x]VO (Vorbereitung)
- Uebertal[1-x]WD (Wirkungsdauer)
- Uebertal[1-x]KO (Kosten)
- Uebertal[1-x]RE (Reichweite)
- Uebertal[1-x]TA (Talente)
- ErfahGE (EP gesamt)
- ErfahEI (EP ausgegeben)
- ErfahVE (EP übrig)
- Kultur
- Profession
- Geschlecht
- Geburtsdatum
- Groesse
- Gewicht
- Haarfarbe
- Augenfarbe
- Titel
- Aussehen[1-6]
- Aussehen (Aussehen[1-6] zusammengefasst)
- Hintergrund[0-8]
- Hintergrund (Hintergrund[0-8] zusammengefasst)
- Notiz (Notizen aus dem Info-Tab)
<br />

## Regelanhang anpassen
Alle Charakterbögen verwenden für den Regelanhang standardmäßig die Dateien Data/Charakterbögen/Regelanhang.html und Data/Charakterbögen/Hintergrund.pdf. Die HTML-Datei wird anhand der Regelanhang-Einstellungen (s. o.) zu einer PDF umgewandelt. Hierbei werden \{rules_content\} und \{rules_font_size\} durch den Regelanhang-Text bzw. die in Sephrasto eingestellte Schriftgröße ersetzt. In der HTML-Datei angegebene Pfade haben immer den Ordner der HTML-Datei als Ausgangsbasis. Der Hintergrund ist separat, um geringere Dateigrößen zu ermöglichen.<br />
Wenn dein Charakterbogen auch andere Dokumente verwenden soll, dann benenne sie \[Charakterbogen-Dateiname\]_Regelanhang.html und \[Charakterbogen-Dateiname\]_Hintergrund.pdf und lege sie ebenso in deinen in den Einstellungen festgelegten Charakterbögen-Ordner. Wenn du die Hintergrund-PDF weglässt, wird der Regelanhang entsprechend ohne Hintergrund ausgegeben.