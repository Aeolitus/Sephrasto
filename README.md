# Sephrasto
Ein Charaktergenerator für das DSA-Hausregelsystem Ilaris, erstellt von Aeolitus. So vollständig wie möglich.

In der Gebrauchsanleitung.pdf finden sich Erklärungen und Warnhinweise.

## Features
* Automatisches Befüllen des Ilaris Charakterbogens (Benötigt pdftk : Gratis-Download für Windows @ https://www.pdflabs.com/tools/pdftk-server/, Linux-Installation siehe unten)
* Einfaches Einarbeiten von Hausregeln wie neuen Fertigkeiten, Vorteilen etc. durch frei editierbare Regelbasis
* Fast alle relevanten Regeln sind im Tool enthalten

Bei Fragen / Änderungswünschen / Feedback einfach Bescheid sagen - im dsaforum oder hier!

## Dieses Tool verwendet

Um Sephrasto mit Python zu verwenden, ist Version 3.7+ empfehlenswert, aber nicht dringend notwendig. 

### Pakete
* PyQt5 (https://www.riverbankcomputing.com/software/pyqt/download5) für die Grafische Oberfläche
* lxml (http://lxml.de/) als xml-parser (unter Linux: `libxml2-dev` und `libxmlsec1-dev` global installieren, wenn lxml via pip installiert werden soll)
* PyYAML (https://pyyaml.org/) als yaml-parser
* requests (https://github.com/psf/requests) für den update checker

### Integriert
* fdfgen (https://github.com/ccnmtl/fdfgen) zum Editieren des Charakterbogens 
* pdffields (https://github.com/evfredericksen/pdffields) für einfachere Bedienung von fdfgen ;)

## Installation Linux (Ubuntu/Debian)
```
sudo apt install python3-pip
sudo apt install openjdk-11-jdk
sudo apt install pdftk
git clone https://github.com/Aeolitus/Sephrasto.git
pip install -r Sephrasto/requirements.txt
```
Alternativ zu pip stehen auch Poetry files zur Verfügung. OpenJDK wird für pdftk benötigt, ohne diese beiden Pakete können keine Charakterbogen-PDFs erzeugt werden. Statt das Sephrasto Repository mit git zu klonen, kannst du es natürlich auch manuell herunterladen und entpacken (unter "Code" den Punkt "Download zip" auswählen).

Gestartet wird Sephrasto dann folgendermaßen:
```
python Sephrasto/src/Sephrasto/Sephrasto.py
```

### Charakterbild ###
Das Charakterbild kann im Beschreibung-Details Tab hinzugefügt werden (nur mit langem Charakterbogen sichtbar). Sollte die PDF-Erstellung mit Charakterbild nicht gelingen und wird dir folgende Fehlermeldung angezeigt:
```
Das Einfügen des Charakterbilds ist fehlgeschlagen: Command [...] returned non-zero exit status 1.. Der Charakterbogen wird nun ohne das Bild erstellt.
```
Dann öffne `etc/ImageMagick-{Version}/policy.xml` und füge unten die Zeile
```
<policy domain="coder" rights="read | write" pattern="PDF" />`
```
hinzu. Deine Versionsnummer musst du selbst eintragen. Getestet wurde bisher nur mit ImageMagick-Version 6 und höher. Die Datei ist vermutlich bei dir schreibgeschützt. Du kannst sie beispielsweise mit `sudo nano etc/ImageMagick-{Version}/policy.xml` öffnen, bearbeiten und speichern. Bedenke, dass die Änderung der Policy nicht nur für Sephrasto, sondern auch für andere Programme gilt, die ImageMagick nun für PDF-Bearbeitung frei nutzen können. Stelle via ```gs --version``` sicher, dass deine Ghostscript-Installation mindestens die Version 9.24 hat, ansonsten stellt diese Änderung ein Sicherheitsrisiko dar ([siehe hier](https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion).

## Einrichtung von Visual Studio als IDE:
* Installiere VS 2019 Community Edition mit dem Python Workload (kann auch nachträglich über den Installer installiert werden)
* Setze den Pfad der Python-Umgebung in der Umgebungsvariable PATH (in der Regel C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64)
* Öffne Sephrasto.sln
* Installiere die dependencies: Solution Explorer -> Python Environments -> Rechtsclick auf Python 3.x -> Install Python Package.
* Stelle zuerst sicher, dass deine pip Version aktuell ist, aktualisiere diese gegebenenfalls und starte Visual Studio neu
* Installiere nun die oben genannten Pakete im gleichen Menu. Um mit build.bat einen Build erstellen zu können wird zusätzlich folgendes benötigt:
    * cx_freeze (https://github.com/marcelotduarte/cx_Freeze)
    * pywin32 (https://github.com/mhammond/pywin32)
* Erstelle die IntelliSense Datenbank: Solution Explorer -> Rechtsclick auf Python Environments -> View all Python environments -> IntelliSense im Dropdown auswahlen und aktivieren/refreshen
* Stelle das Tab-Verhalten auf "Insert Spaces": Tools -> Options -> Text Editor -> Python -> Tabs
* Öffne das Exception Settings Fenster (Debug -> Windows -> Exception Settings) und selektiere alle Python Exceptions, dann deaktiviere <All Python Exceptions not in this list>, BaseException und Exception - damit breaken die custom exceptions nicht, die Sephrasto intern nutzt.

## UI design mit Qt
* Modifiziere niemals Dateien, die am Anfang "Created by: PyQt5 UI code generator" stehen haben von Hand!
* Stattdessen wird das UI durch ".ui"-XML-Dateien im "Sephrasto/UI" Ordner definiert. Optionalerweise können diese mit dem Qt Creator visuell designed werden (enthalten im Qt-Installer unter https://www.qt.io/).
* Aus diesen Dateien wird dann der Python-Code mit Hilfe von "Sephrasto/UI/convert.bat" erzeugt.
* Erstelle in deinem "Python/Scripts" Ordner "pyuic5.bat" mit dem Inhalt "CALL pyuic5.exe %*"
* Bei Problemen mit convert.bat, stelle sicher, dass:
    * ... der Python Install-Ordner und der Unterordner "Scripts" in deiner PATH-Umgebungsvariable enthalten sind. Dies wird normalerweise vom Python installer automatisch gemacht. (Windows 10: System -> Advanced System Settings -> Environment Variables -> Path - in User oder System)
    * ... "Python/Scripts" die Datei "pyuic5.exe" enthält. Diese wird normalerweise durch das Installieren von PyQt5 dort angelegt.

## Abschlussbemerkung
Dieses Tool ist das Projekt, an dem ich Python / Qt gelernt habe. Deutliche Schwankungen im Coding-Stil und in der Codequalität sind demnach zu erwarten. Ich werde über die Zeit versuchen, das zu beheben; einige Spuren davon (wie das furchtbare denglisch) werden vermutlich bleiben. 
