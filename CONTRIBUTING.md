# Für Entwickler

## Erstellen von Windows builds
Stelle sicher, dass alle Pakete aus der requirements.txt installiert sind. Aktuell nutzen wir außerdem Python 3.11 und cx_Freeze (immer aktuellste Version) zum Erstellen von Windows builds. Nun solltest du build.bat im Sephrasto root ausführen können.

## Einrichtung von Visual Studio als IDE
* Installiere VS Community Edition mit dem Python Workload (kann auch nachträglich über den Installer installiert werden)
* Installiere Python 3.11, aktiviere dabei die Option, dass Python zur Pfad-Umgebungsvariable hinzugefügt wird: https://www.python.org/downloads/windows/
* Erstelle ein virtual environment
    * Navigiere auf der Kommandozeile in den Sephrasto repository root
    * venv erstellen: ```python -m venv venv```
	* venv aktivieren: ```venv\Scripts\activate```
	* pip upgraden: ```python -m pip install --upgrade pip```
	* Von Sephrasto benötigte Pakete installieren: ```pip install -r requirements.txt```
* Öffne Sephrasto/src/Sephrasto.sln
* Erstelle die IntelliSense Datenbank: Solution Explorer -> Rechtsclick auf Python Environments -> View all Python environments -> IntelliSense im Dropdown auswahlen und aktivieren/refreshen
* Stelle das Tab-Verhalten auf "Insert Spaces": Tools -> Options -> Text Editor -> Python -> Tabs
* Öffne das Exception Settings Fenster (Debug -> Windows -> Exception Settings) und selektiere alle Python Exceptions, dann deaktiviere <All Python Exceptions not in this list>, BaseException und Exception - damit breaken die custom exceptions nicht, die Sephrasto intern nutzt.

## UI design mit Qt
* Modifiziere niemals Dateien im "src/Sephrasto/UI" Ordner von Hand!
* Stattdessen wird das UI durch ".ui"-XML-Dateien im "designer" Ordner definiert. Optionalerweise können diese mit dem Qt Designer visuell designed werden (siehe venv/Lib/site-packages/PySide6/designer.exe).
* Aus diesen Dateien wird dann der Python-Code mit Hilfe von "designer/convert.bat" erzeugt.
* Bei Problemen mit convert.bat, stelle sicher, dass:
    * ... du im Repository root ein Virutal Environment mit dem Namen venv angelegt (s.o.) und darin die requirements installiert hast (s. o.). Wenn dein environment wo anders liegt, musst du die convert.bat lokal entsprechend anpassen.
    * ... "venv/Scripts" die Datei "pyside6-uic.exe" enthält. Diese wird normalerweise durch das Installieren von PySide6 dort angelegt.

## Update der Dokumentation
Die Markdown-Dokumente in /docs werden für Sephrastos-In-App-Hilfe in HTML konvertiert. Dies muss also nach jeder Änderung der Dokumente durchgeführt werden.

Installation:
* Installiere mkdocs: ```pip install mkdocs```
* Installiere mkdocs-material: ```pip install mkdocs-material```

Update der HTML-Dateien:
* Navigiere auf der Kommandozeile in den Serphasto-Repo-Root.
* Führe aus: ```mkdocs build```

## Plugin Repositories
Sephrasto unterstützt Plugin repositories, um als User die Plugins bequem aus den Einstellungen heraus verwalten zu können. In den Standardeinstellungen ist https://github.com/brzGatsu/SephrastoPlugins voreingetragen und wir empfehlen dir dort für deine Plugins einen PR zu erstellen. Du kannst aber auch ein eigenes Repository anlegen. Aktuell ist Sephrasto hier auf Github beschränkt und du musst folgender Konvention folgen:
* Der Sephrasto Pluginmanager benötigt eine Github API URL zu deiner /releases page. Beispiel: https://api.github.com/repos/brzGatsu/SephrastoPlugins/releases
* Du musst den oder die Pluginordner zippen (.zip) und bei Github als Release hochladen (nur diese eine Datei). Der Release muss als Git-Tag die Sephrasto-Target-Version im folgenden Format enthalten: "v4.4.0.0". Die vierte Zahl kannst du für Plugin-Updates innerhalb derselben Sephrastoversion verwenden. Sephrasto-Versionen die älter als das Target sind wird das Plugin(-Update) nicht angezeigt.
* Es gibt im Einstellungsdialog keine Option für weitere Repos, aber du kannst es händisch in der Sephrasto.ini eintragen unter "Plugin-Repos".

## Abschlussbemerkung
Der Code ist teilweise von furchtbarem Denglisch durchzogen, da Sephrasto ein ausschließlich deutsches Regelwerk umsetzt. Die Begrifflichkeiten in zu übersetzen wäre aber wenig hilfreich für die Lesbarkeit.
