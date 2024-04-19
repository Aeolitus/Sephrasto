# Ein eigenes Theme erstellen
Du kannst das Aussehen von Sephrasto ohne Programmierkenntnisse nach deinen Wünschen anpassen, indem du ein eigenes Theme kreierst. Dazu musst du eine Text-Datei namens "Mein Theme.ini" in deinem Sephrasto-Konfigurationsordner erstellen. Diesen findest du hier:
- Windows: "User/Dokumente/Sephrasto"
- macOS: "User/Library/Preferences/Sephrasto"
- Linux: "home/user/.config/Sephrasto".

Am einfachsten ist es, wenn du erstmal eines der bestehenden Themes dorthin kopierst und entsprechend umbenennst. Diese findest du in deinem Sephrasto-Installationsordner im Unterordner Data/Themes. Nun kannst du beispielsweise ein paar der dort festgelegten Farben anpassen. Danach kannst du das Theme in den Einstellungen von Sephrasto aktivieren.

## Theme-Konfiguration
Alle der folgenden Einstellungsmöglichkeiten sind optional, bis auf die Einstellung Style.

Style: fusion
-> Hier trägst du einen der Qt-Styles ein, siehe https://doc.qt.io/qt-6/qtquickcontrols2-styles.html. Es sind leider nicht alle verfügbar, aber Fusion ist sehr gut anpassbar.

Standardpalette: true
-> Sorgt dafür, dass als Ausgangsbasis statt einer leeren Palette die Standardfarbpalette verwendet wird.

Palette:
&nbsp;&nbsp;&nbsp;&nbsp;Window: "#ffffff"
&nbsp;&nbsp;&nbsp;&nbsp;WindowText: "#000000"
&nbsp;&nbsp;&nbsp;&nbsp;[...]
-> Optional. Hier kannst du den einzelnen Elementen Farben zuweisen. Eine Liste der möglichen "color roles" findest du hier: https://doc.qt.io/qt-6/qpalette.html#ColorRole-enum

Palette-Active: [...]
-> Gleiche Funktion wie Palette, die Farben gelten aber, wenn das entsprechende Element Fokus hat.

Palette-Disabled: [...]
-> Gleiche Funktion wie Palette, die Farben gelten aber, wenn das entsprechende Element deaktiviert ist.

HeadingColor: "#000000"
-> Legt die Farbe von Überschriften fest.

BorderColor: "rgba(0,0,0,0.2)"
-> Legt die Farbe vom Rahmen der einzelnen Waffenzeilen fest.

ReadonlyColor: "#ffffff"
-> Legt die Hintergrundfarbe von nicht-editierbaren Textfeldern fest, wie sie beispielsweise rechts in den Vorteile- und Fertigkeiten-Tabs vorkommen.

PanelColor: "#b3b3b3"
-> Legt die Huntergrundfarbe von überlagerten Panels fest, wie sie beispielsweise vom Charakterassistent verwendet werden.

CSS: |
&nbsp;&nbsp;&nbsp;&nbsp;QPushButton { background-color: #d1bd94; }
-> Hier kannst du via CSS die Qt UI Elemente nach Belieben weiter anpassen. Weitere Infos findest du hier: https://doc.qt.io/qt-6/stylesheet-syntax.html