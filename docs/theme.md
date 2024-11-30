# Ein eigenes Theme erstellen
Du kannst das Aussehen von Sephrasto ohne Programmierkenntnisse nach deinen Wünschen anpassen, indem du ein eigenes Theme kreierst. Dazu musst du eine Text-Datei namens "Mein Theme.ini" in deinem Sephrasto-Konfigurationsordner erstellen. Diesen findest du hier:

- Windows: "User/Dokumente/Sephrasto"
- macOS: "User/Library/Preferences/Sephrasto"
- Linux: "home/user/.config/Sephrasto".

Am einfachsten ist es, wenn du erstmal eines der bestehenden Themes dorthin kopierst und entsprechend umbenennst. Diese findest du in deinem Sephrasto-Installationsordner im Unterordner Data/Themes. Nun kannst du beispielsweise ein paar der dort festgelegten Farben anpassen. Danach kannst du das Theme in den Einstellungen von Sephrasto aktivieren.

## Theme-Konfiguration
Alle der folgenden Einstellungsmöglichkeiten sind optional, bis auf die Einstellung Style.

```yml
Style: fusion
```
Hier trägst du einen der Qt-Styles ein, in der Regel stehen fusion, windows, windowsvista und macos zur Verfügung.

```yml
ForceColorScheme: Dark
```
Optional. Hier kannst du ein Farbschema forcieren, unabhängig vom im Betriebssystem konfigurierten Farbschema. Zur Auswahl stehen Light und Dark.

```yml
Palette:
  Window: "#ffffff"
  [...]
```
Optional. Hier kannst du den einzelnen Elementen Farben zuweisen. Eine Liste der möglichen "color roles" findest du hier: <a href="https://doc.qt.io/qt-6/qpalette.html#ColorRole-enum">https://doc.qt.io/qt-6/qpalette.html#ColorRole-enum</a>. Wichtig: wenn du WindowText festlegst, funktioniert die automatische Anpassung der Fensterleistenfarbe entsprechend der Windows-Einstellungen nicht mehr. Setze die Schriftfarbe stattdessen als zusätzliches CSS für QWidget und QToolTip (s.u.). 

```yml
Palette-Active: [...]
```
Optional. Gleiche Funktion wie Palette, die Farben gelten aber, wenn das entsprechende Element Fokus hat.

```yml
Palette-Disabled: [...]
```
Optional. Gleiche Funktion wie Palette, die Farben gelten aber, wenn das entsprechende Element deaktiviert ist.

```yml
HeadingColor: "#000000"
```
Optional. Legt die Farbe von Überschriften fest.

```yml
BorderColor: "rgba(0,0,0,0.2)"
```
Optional. Legt die Farbe vom Rahmen der einzelnen Waffenzeilen fest.

```yml
ReadonlyColor: "#ffffff"
```
Optional. Legt die Hintergrundfarbe von nicht-editierbaren Textfeldern fest, wie sie beispielsweise rechts in den Vorteile- und Fertigkeiten-Tabs vorkommen.

```yml
ValidColor: "green"
```
Optional. Legt die Farbe für folgende Hervorhebungen fest: validiert, positiv, hinzugefügt.

```yml
WarningColor: "yellow"
```
Optional. Legt die Farbe für folgende Hervorhebungen fest: Warnung.

```yml
ErrorColor: "red"
```
Optional. Legt die Farbe für folgende Hervorhebungen fest: Fehler, negativ, gelöscht.

```yml
ModifiedColor: "#0000ff"
```
Optional. Legt die Farbe für folgende Hervorhebungen fest: modifiziert.

```yml
CodeKeywordColor: "#569CD6"
```
Optional. Legt die Farbe für Keywords im Scripteditor fest.

```yml
CodeOperatorsBracesColor: "#B4B4B4"
```
Optional. Legt die Farbe für Operatoren und Klammern im Scripteditor fest.

```yml
CodeDeclarationColor: "#4EC9B0"
```
Optional. Legt die Farbe für Klassendeklarationen und Imports im Scripteditor fest.

```yml
CodeStringColor: "#D69D85"
```
Optional. Legt die Farbe für Strings im Scripteditor fest.

```yml
CodeCommentColor: "#57A64A"
```
Optional. Legt die Farbe für Kommentare im Scripteditor fest.

```yml
CodeNumberColor: "#B5CEA8"
```
Optional. Legt die Farbe für Zahlen im Scripteditor fest.

```yml
CodeBackgroundColor: "#1E1E1E"
```
Optional. Legt die Farbe für den Hintergrund des Scripteditors fest.

```yml
CSS: |
    QPushButton { background-color: #d1bd94; }
    QWidget, QToolTip { color: #221E1F; }
```
Optional. Hier kannst du via CSS die Qt UI Elemente nach Belieben weiter anpassen. Weitere Infos findest du hier: <a href="https://doc.qt.io/qt-6/stylesheet-syntax.html">https://doc.qt.io/qt-6/stylesheet-syntax.html</a>