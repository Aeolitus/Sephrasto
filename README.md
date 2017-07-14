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

Dieses Tool ist das Projekt, an dem ich Python / Qt gelernt habe. Deutliche Schwankungen im Coding-Stil und in der Codequalität sind demnach zu erwarten. Ich werde über die Zeit versuchen, das zu beheben; einige Spuren davon (wie das furchtbare denglisch) werden vermutlich bleiben. 
