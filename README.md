# Sephrasto
Ein Charaktergenerator für das DSA-Hausregelsystem Ilaris, erstellt von Aeolitus. So vollständig wie möglich.

In der Gebrauchsanleitung.pdf finden sich Erklärungen und Warnhinweise.

## Features
* Automatisches Befüllen des Ilaris Charakterbogens (Benötigt pdftk : Gratis-Download für Windows @ https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/, unter Linux das Paket `pdftk` installieren)
* Einfaches Einarbeiten von Hausregeln wie neuen Fertigkeiten, Vorteilen etc. durch frei editierbare Regelbasis
* Fast alle relevanten Regeln sind im Tool enthalten

Bei Fragen / Änderungswünschen / Feedback einfach Bescheid sagen - im dsaforum oder hier!

## Dieses Tool verwendet 
* fdfgen (https://github.com/ccnmtl/fdfgen) zum Editieren des Charakterbogens 
* pdffields (https://github.com/evfredericksen/pdffields) für einfachere Bedienung von fdfgen ;)
* PyQt5 (https://www.riverbankcomputing.com/software/pyqt/download5) für die Grafische Oberfläche
* lxml (http://lxml.de/) als xml-parser (unter Linux: `libxml2-dev` und `libxmlsec1-dev` global installieren, wenn lxml via pip installiert werden soll)
* PyYAML (https://pyyaml.org/) als yaml-parser

Um Sephrasto mit Python zu verwenden, ist Version 3.6+ empfehlenswert, aber nicht dringend notwendig. Weiterhin müssen PyQt5 und lxml installiert werden. Starte einfach die Sephrasto.py und los gehts.

## Installation Linux (ubuntu/debian)
```
sudo apt install pdftk
git clone https://github.com/Aeolitus/Sephrasto.git
pip install -r Sephrasto/requirements.txt
python Sephrasto/Sephrasto.py
```

## Anleitung für die Nutzung von Visual Studio als IDE
* Installiere VS 2019 Community Edition mit dem Python Workload (kann auch nachträglich über den Installer installiert werden)
* Setze den Pfad der Python-Umgebung in der Umgebungsvariable PATH (in der Regel C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64)
* Starte Make/Sephrasto.sln
* Installiere die dependencies: Solution Explorer -> Python Environments -> Rechtsclick auf Python 3.x -> Install Python Package.
* Stelle zuerst sicher, dass deine pip Version aktuell ist, aktualisiere diese gegebenenfalls und starte Visual Studio neu
* Installiere nun die folgenden Pakete im gleichen Menu:
    * lxml
    * PyQt5
	* PyYAML
    * Um mit build.bat einen Build erstellen zu können: cx_freeze, pywin32
* Erstelle die IntelliSense Datenbank: Solution Explorer -> Rechtsclick auf Python Environments -> View all Python environments -> IntelliSense im Dropdown auswahlen und aktivieren/refreshen
* Stelle das Tab-Verhalten auf "Insert Spaces": Tools -> Options -> Text Editor -> Python -> Tabs
* Öffne das Exception Settings Fenster (Debug -> Windows -> Exception Settings) und selektiere alle Python Exceptions, dann deaktiviere <All Python Exceptions not in this list>, BaseException und Exception - damit breaken die custom exceptions nicht, die Sephrasto intern nutzt.

## Anleitung für die UI:
* Modifiziere niemals Dateien, die am Anfang "Created by: PyQt5 UI code generator" stehen haben von Hand!
* Stattdessen wird die UI durch ".ui"-XML-Dateien im "Sephrasto/UI" Ordner definiert. Optionalerweise können diese mit dem Qt Creator visuell designed werden (enthalten im Qt-Installer unter https://www.qt.io/).
* Aus diesen Dateien wird dann der Python-Code mit Hilfe von "Sephrasto/UI/convert.bat" erzeugt.
* Erstelle in deinem "Python/Scripts" Ordner "pyuic5.bat" mit dem Inhalt "CALL pyuic5.exe %*"
* Bei Problemen mit convert.bat, stelle sicher, dass:
    * ... der Python Install-Ordner und der Unterordner "Scripts" in deiner PATH-Umgebungsvariable enthalten sind. Dies wird normalerweise vom Python installer automatisch gemacht. (Windows 10: System -> Advanced System Settings -> Environment Variables -> Path - in User oder System)
    * ... "Python/Scripts" die Datei "pyuic5.exe" enthält. Diese wird normalerweise durch das Installieren von PyQt5 dort angelegt.

Dieses Tool ist das Projekt, an dem ich Python / Qt gelernt habe. Deutliche Schwankungen im Coding-Stil und in der Codequalität sind demnach zu erwarten. Ich werde über die Zeit versuchen, das zu beheben; einige Spuren davon (wie das furchtbare denglisch) werden vermutlich bleiben. 
