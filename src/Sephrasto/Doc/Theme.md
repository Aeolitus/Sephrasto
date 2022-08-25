[Hilfe](Help.md) > Ein eigenes Theme erstellen

# Ein eigenes Theme erstellen
Du kannst das Aussehen von Sephrasto ohne Programmierkenntnisse nach deinen Wünschen anpassen, indem du ein eigenes Theme kreierst. Dazu musst du eine Text-Datei namens "Mein Theme.ini" in deinem Sephrasto-Konfigurationsordner erstellen. Diesen findest du hier:
- Windows: "User/Dokumente/Sephrasto"
- macOS: "User/Library/Preferences/Sephrasto"
- Linux: "home/user/.config/Sephrasto".

Am einfachsten ist es, wenn du erstmal eines der bestehenden Themes dorthin kopierst und entsprechend umbenennst. Diese findest du in deinem Sephrasto-Installationsordner im Unterordner Data/Themes. Nun kannst du beispielsweise ein paar der dort festgelegten Farben anpassen. Danach kannst du das Theme in den Einstellungen von Sephrasto aktivieren.
<br />
## Theme-Konfiguration
Alle der folgenden Einstellungsmöglichkeiten sind optional, bis auf die Einstellung Style.<br />
<br />
Style: fusion<br />
-> Hier trägst du einen der Qt-Styles ein, siehe https://doc.qt.io/qt-6/qtquickcontrols2-styles.html. Es sind leider nicht alle verfügbar, aber Fusion ist sehr gut anpassbar.<br />
<br />
Standardpalette: true<br />
-> Sorgt dafür, dass als Ausgangsbasis statt einer leeren Palette die Standardfarbpalette verwendet wird.<br />
<br />
Palette:<br />
&nbsp;&nbsp;&nbsp;&nbsp;Window: "#ffffff"<br />
&nbsp;&nbsp;&nbsp;&nbsp;WindowText: "#000000"<br />
&nbsp;&nbsp;&nbsp;&nbsp;[...]<br />
-> Optional. Hier kannst du den einzelnen Elementen Farben zuweisen. Eine Liste der möglichen "color roles" findest du hier: https://doc.qt.io/qt-6/qpalette.html#ColorRole-enum<br />
<br />
Palette-Active: [...]<br />
-> Gleiche Funktion wie Palette, die Farben gelten aber, wenn das entsprechende Element Fokus hat.<br />
<br />
Palette-Disabled: [...]<br />
-> Gleiche Funktion wie Palette, die Farben gelten aber, wenn das entsprechende Element deaktiviert ist.<br />
<br />
HeadingColor: "#000000"<br />
-> Legt die Farbe von Überschriften fest.<br />
<br />
BorderColor: "rgba(0,0,0,0.2)"<br />
-> Legt die Farbe vom Rahmen der einzelnen Waffenzeilen fest.<br />
<br />
ReadonlyColor: "#ffffff"<br />
-> Legt die Hintergrundfarbe von nicht-editierbaren Textfeldern fest, wie sie beispielsweise rechts in den Vorteile- und Fertigkeiten-Tabs vorkommen.<br />
<br />
PanelColor: "#b3b3b3"<br />
-> Legt die Huntergrundfarbe von überlagerten Panels fest, wie sie beispielsweise vom Charakterassistent verwendet werden.<br />
<br />
CSS: |<br />
&nbsp;&nbsp;&nbsp;&nbsp;QPushButton { background-color: #d1bd94; }<br />
-> Hier kannst du via CSS die Qt UI Elemente nach Belieben weiter anpassen. Weitere Infos findest du hier: https://doc.qt.io/qt-6/stylesheet-syntax.html