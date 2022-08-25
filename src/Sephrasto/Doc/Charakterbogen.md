[Hilfe](Help.md) > Eigene Charakterbögen erstellen

# Eigene Charakterbögen erstellen
Du kannst Sephrasto weitere Charakterbögen hinzufügen. Kopiere deinen Bogen hierzu einfach in den Charakterbögen-Ordner, der in den Einstellungen von Sephrasto konfiguriert ist. Du musst Sephrasto allerdings noch ein paar Informationen zu deinem Bogen geben in Form einer Konfigurationsdatei. Diese ist eine Textdatei mit dem gleichen Namen wie die PDF-Datei, aber mit der Endung ".ini". Am einfachsten ist es, wenn du erstmal eine der bestehenden Konfigurationsdateien dorthin kopierst und entsprechend umbenennst. Diese findest du in deinem Sephrasto-Installationsordner im Unterordner Data/Charakterbögen. 
<br />
## Charakterbogen-Konfiguration
Alle Einstellungen sind Pflicht-Angaben, außer BildOffset (falls Bild: False).<br />
<br />
MaxVorteile: 24<br />
->Die Anzahl an Formularfeldern für Vorteile.<br />
<br />
MaxKampfVorteile: 16<br />
->Die Anzahl an Formularfeldern für Kampfvorteile.<br />
<br />
MaxÜbernatürlicheVorteile: 12<br />
->Die Anzahl an Formularfeldern für Übernatürliche Vorteile.<br />
<br />
MaxFreieFertigkeiten: 28<br />
->Die Anzahl an Formularfeldern für Freie Fertigkeiten.<br />
<br />
MaxFertigkeiten: 28<br />
->Die Anzahl an Formularfeldern für Fertigkeiten.<br />
<br />
MaxÜbernatürlicheFertigkeiten: 12<br />
->Die Anzahl an Formularfeldern für Übernatürliche Fertigkeiten.<br />
<br />
MaxÜbernatürlicheTalente: 30<br />
->Die Anzahl an Formularfeldern für übernatürliche Talente.<br />
<br />
SeitenProfan: 3<br />
->Die Anzahl an Seiten für profane Charaktere. Seiten die darüber hinausgehen werden bei profanen Charakteren abgeschnitten.<br />
<br />
BeschreibungDetails: True<br />
->Legt fest, ob der Beschreibung-Details Tab im Charaktereditor angezeigt werden soll.<br />
<br />
Bild: True<br />
->Legt fest, ob der Bogen ein Feld für ein Charakterbild hat (erfordert BeschreibungDetails).<br />
<br />
BildOffset:<br />
\- 115.55<br />
\- 89.55<br />
->Legt die Position des Bilds fest. Diese ist nicht wirklich zu errechnen, versuche es mit Trial & Error.<br />
<br />
## Formularfelder
Sephrasto befüllt die folgenden Formularfelder. In Eckigen Klammern befindet sich ggf. die Anzahl der Felder - "Eigen[1-8]" heißt beispielsweise, dass die Felder "Eigen1", "Eigen2" bis "Eigen8" befüllt werden. Ein "x" bedeutet hier, dass soviele Felder ausgegeben werden wie dein Charakterbogen unterstützt. Ein kleines "m" am Ende der Feldnamen ist mit einem "\*" gleichzusetzen, es handelt sich also um den durch BE modifizierten Wert. Falls der Feldname nicht eindeutig ist befindet sich in Klammern noch eine kurze Beschreibung; checkbox bedeutet hier, dass ein Checkbox-Formularfeld statt eines Textfelds erwartet wird. Alle Felder sind optional.

- Name
- Rasse
- Kultur
- Statu (Status)
- Finanzen
- Kurzb (Kurzbeschreibung)
- Schip (Schicksalspunkte)
- Schipm
- Eigen[1-8] (Eigenheit)
- KO
- MU
- GE
- KK
- IN
- KL
- CH
- FF
- KO[2-3] (PW, 3 ist identisch zu 2)
- MU[2-3] (PW)
- GE[2-3] (PW)
- KK[2-3] (PW)
- IN[2-3] (PW)
- KL[2-3] (PW)
- CH[2-3] (PW)
- FF[2-3] (PW)
- WundschwelleBasis
- Wundschwelle
- WS (identisch zu Wundschwelle)
- ModUnverwuestlich (checkbox)
- MagieresistenzBasis
- Magieresistenz
- ModWillensstark1 (checkbox)
- ModWillensstark2 (checkbox)
- ModUnbeugsam (checkbox)
- GeschwindigkeitBasis
- Geschwindigkeit
- ModFlink1 (checkbox)
- ModFlink2 (checkbox)
- SchadensbonusBasis
- Schadensbonus
- InitiativeBasis
- Initiative
- INIm
- ModKampfreflexe (checkbox)
- ModGefaess (Gefäß der Sterne, checkbox)
- AstralenergieBasis
- Astralenergie
- ModAstralenergie
- KarmaenergieBasis
- Karmaenergie
- ModKarmaenergie
- EN (Energie)
- DHm
- GSm
- WSm
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
- Hintergrund[0-8]