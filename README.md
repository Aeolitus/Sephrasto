# Sephrasto
Ein Charaktergenerator für das DSA-Hausregelsystem Ilaris, erstellt von Aeolitus. So vollständig wie möglich.

In der Gebrauchsanleitung.pdf finden sich Erklärungen und Warnhinweise.

Features:
* Automatisches Befüllen des Ilaris Charakterbogens (Benötigt pdftk : Gratis-Download @ https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/)
* Einfaches Einarbeiten von Hausregeln wie neuen Fertigkeiten, Vorteilen etc. durch frei editierbare Regelbasis
* Fast alle relevanten Regeln sind im Tool enthalten

Bei Fragen / Änderungswünschen / Feedback einfach Bescheid sagen - im dsaforum oder hier!

Dieses Tool verwendet 
* fdfgen (https://github.com/ccnmtl/fdfgen) zum Editieren des Charakterbogens 
* pdffields (https://github.com/evfredericksen/pdffields) für einfachere Bedienung von fdfgen ;)
* PyQt5 (https://www.riverbankcomputing.com/software/pyqt/download5) für die Grafische Oberfläche
* lxml (http://lxml.de/) als xml-parser

Um Sephrasto mit Python zu verwenden, ist Version 3.6 empfehlenswert, aber nicht dringend notwendig. Weiterhin müssen PyQt5 und lxml installiert werden. Starte einfach die Sephrasto.py und los gehts.

Anleitung für die Nutzung von Visual Studio als IDE:
* Installiere VS 2017 Community Edition mit dem Python Workload (kann auch nachträglich über den Installer installiert werden)
* Setze den Pfad der Python-Umgebung in der Umgebungsvariable PATH (in der Regel C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64)
* Starte Make/Sephrasto.sln
* Installiere die dependencies: Solution Explorer -> Python Environments -> Rechtsclick auf Python 3.x -> Install Python Package. Installiere die folgenden Pakete:
    * lxml
    * PyQt5
	* PyYAML
    * Um mit build.bat einen Build erstellen zu können: cx_freeze, pywin32
* Erstelle die IntelliSense Datenbank: Solution Explorer -> Rechtsclick auf Python Environments -> View all Python environments -> IntelliSense im Dropdown auswahlen und aktivieren/refreshen
* Stelle das Tab-Verhalten auf "Insert Spaces": Tools -> Options -> Text Editor -> Python -> Tabs
* Öffne das Exception Settings Fenster (Debug -> Windows -> Exception Settings) und selektiere alle Python Exceptions

Anleitung für die Nutzung auf der Kommandzeile (z.B. Linux, OS X):
* Installiere Python 3 für dein Betriebssystem
* Erstelle eine virtuelle Umgebung für Sephrasto und aktiviere es:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
* Installiere die Abhängigkeiten mit `python3 -m pip install -r requirements.txt`
* Baue die Applikation lokal mit `python3 setup.py py2app -A`
* Baue die Applikation zur Auslieferung mit `python3 setup.py py2app`

Anleitung für die UI:
* Modifiziere niemals Dateien, die am Anfang "Created by: PyQt5 UI code generator" stehen haben von Hand!
* Stattdessen wird die UI durch ".ui"-XML-Dateien im "Sephrasto/UI" Ordner definiert. Optionalerweise können diese mit dem Qt Creator visuell designed werden (enthalten im Qt-Installer unter https://www.qt.io/).
* Aus diesen Dateien wird dann der Python-Code mit Hilfe von "Sephrasto/UI/convert.bat" erzeugt.
* Erstelle in deinem "Python/Scripts" Ordner "pyuic5.bat" mit dem Inhalt "CALL pyuic5.exe %*"
* Bei Problemen mit convert.bat, stelle sicher, dass:
    * ... der Python Install-Ordner und der Unterordner "Scripts" in deiner PATH-Umgebungsvariable enthalten sind. Dies wird normalerweise vom Python installer automatisch gemacht. (Windows 10: System -> Advanced System Settings -> Environment Variables -> Path - in User oder System)
    * ... "Python/Scripts" die Datei "pyuic5.exe" enthält. Diese wird normalerweise durch das Installieren von PyQt5 dort angelegt.

Dieses Tool ist das Projekt, an dem ich Python / Qt gelernt habe. Deutliche Schwankungen im Coding-Stil und in der Codequalität sind demnach zu erwarten. Ich werde über die Zeit versuchen, das zu beheben; einige Spuren davon (wie das furchtbare denglisch) werden vermutlich bleiben. 