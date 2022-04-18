# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:11:39 2017

@author: Lennart
"""
from Wolke import Wolke
import UI.CharakterBeschreibung
from PyQt5 import QtWidgets, QtCore
import logging
from Hilfsmethoden import Hilfsmethoden

class BeschrWrapper(QtCore.QObject):
    '''
    Wrapper class for the Beschreibung GUI. Contains methods for updating
    the GUI elements to the current values and for changing the current values
    to the values set by the user.
    '''
    modified = QtCore.pyqtSignal()

    def __init__(self):
        ''' Initialize and connect signals '''
        super().__init__()
        logging.debug("Initializing BeschrWrapper...")
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterBeschreibung.Ui_formBeschreibung()
        self.ui.setupUi(self.form)

        self.ui.editName.editingFinished.connect(self.update)
        self.ui.editRasse.editingFinished.connect(self.update)
        self.ui.editKurzbeschreibung.editingFinished.connect(self.update)
        for i in range(8):
            editEig = getattr(self.ui, "editEig" + str(i+1))
            editEig.editingFinished.connect(self.update)
        self.ui.comboFinanzen.activated.connect(self.update)
        self.ui.comboStatus.activated.connect(self.update)
        self.ui.comboHeimat.activated.connect(self.update)
        self.currentGebraeuche = Wolke.Char.heimat
        if "Gebräuche" in Wolke.Char.fertigkeiten:
            if "Gebräuche: " + self.currentGebraeuche not in \
                    Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente and "Gebräuche: " + self.currentGebraeuche in Wolke.DB.talente:
                Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente.append("Gebräuche: " + self.currentGebraeuche)

        self.ui.comboStatus.setToolTip("""Der Status wirkt sich auf die Lebenshaltungskosten aus. Der Vorteil Einkommen kann helfen, diese zu bestreiten.<br>
        <b>Elite</b>: mind. 256 Dukaten pro Monat<br>
        Beispiele: Angehörige des Hochadels, reiche Patrizierinnen, Kirchenfürsten, Spektabilitäten und Handelsherrinnen, Bergkönige<br>
        Anmerkung: adlige Angehörige der Elite sollten in der Generierung den Vorteil Privilegien (Adel) wählen.<br>
        <b>Oberschicht</b>: 64 Dukaten pro Monat<br>
        Beispiele: Niederadlige, angesehene Zauberinnen, Gelehrte, Geweihte und Offiziere, wohlhabende Großbürgerinnen, weise Mitglieder elfischer Sippen, zwergische Klanführer<br>
        <b>Mittelschicht</b>: 16 Dukaten pro Monat<br>
        Beispiele: angesehene Bürgerinnen und Handwerker, Großbäuerinnen, einfache Geweihte, Zauberer und Akademieabgängerinnen, verarmte Adlige, Häuptlinge aus „barbarischen“ Kulturen, viele Elfen und Zwerge<br>
        <b>Unterschicht</b>: 4 Dukaten pro Monat<br>
        Beispiele: arme Bürger, freie oder leibeigene Kleinbäuerinnen, Soldaten, Angehörige barbarischer Kulturen<br>
        <b>Abschaum</b>: 1 Dukaten pro Monat<br>
        Beispiele: Sklavinnen, arme Leibeigene, Vagabundinnen, Wanderarbeiter
        """)

        self.ui.comboFinanzen.setToolTip("""Die Finanzen spielen nur bei einem neuen Charakter eine Rolle und haben Auswirkungen auf das Startkapital und die Anzahl Schicksalspunkte zu Beginn.<br>
        <b>Sehr reich</b>: 256 Dukaten, 0 Schicksalspunkte<br>
        <b>Reich</b>: 128 Dukaten, 2 Schicksalspunkte<br>
        <b>Normal</b>: 32 Dukaten, 4 Schicksalspunkte<br>
        <b>Arm</b>: 16 Dukaten, 5 Schicksalspunkte<br>
        <b>Sehr arm</b>: 4 Dukaten, 6 Schicksalspunkte
        """)

        self.ui.comboHeimat.setToolTip("Jeder Charakter beherrscht seine Muttersprache und die Gebräuche seiner Heimat.\nDu erhältst gratis die Freie Fertigkeit zu deiner Muttersprache auf Stufe III und das passende Gebräuche-­Talent.")

        self.currentlyLoading = False

    def update(self):
        if self.currentlyLoading:
            return

        ''' Transfer current values to Char object '''
        changed = False

        if Wolke.Char.name != self.ui.editName.text():
            Wolke.Char.name = self.ui.editName.text()
            changed = True

        if Wolke.Char.rasse != self.ui.editRasse.text():
            Wolke.Char.rasse = self.ui.editRasse.text()
            changed = True

        if Wolke.Char.status != self.ui.comboStatus.currentIndex():
            Wolke.Char.status = self.ui.comboStatus.currentIndex()
            changed = True

        if Wolke.Char.finanzen != self.ui.comboFinanzen.currentIndex():
            Wolke.Char.finanzen = self.ui.comboFinanzen.currentIndex()
            changed = True

        if "Gebräuche" in Wolke.Char.fertigkeiten:
            if self.ui.comboHeimat.currentText() != self.currentGebraeuche:
                if "Gebräuche: " + self.currentGebraeuche in \
                        Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente:
                    Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente.remove(
                            "Gebräuche: " + self.currentGebraeuche)
                self.currentGebraeuche = self.ui.comboHeimat.currentText()
                if "Gebräuche: " + self.currentGebraeuche not in \
                        Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente:
                    Wolke.Char.fertigkeiten["Gebräuche"].gekaufteTalente.append(
                        "Gebräuche: " + self.currentGebraeuche)
                changed = True

        if Wolke.Char.heimat != self.ui.comboHeimat.currentText():
            Wolke.Char.heimat = self.ui.comboHeimat.currentText()
            changed = True

        if Wolke.Char.kurzbeschreibung != self.ui.editKurzbeschreibung.text():
            Wolke.Char.kurzbeschreibung = self.ui.editKurzbeschreibung.text()
            changed = True

        eigenheitenNeu = []
        for i in range(8):
            text = eval("self.ui.editEig" + str(i+1) + ".text()")
            eigenheitenNeu.append(text)

        #Preserve the position of actual elements but remove any trailing empty elements
        #This is needed for ArrayEqual later to work as intended
        for eig in reversed(eigenheitenNeu):
            if eig == "":
                eigenheitenNeu.pop()
            else:
                break

        if not Hilfsmethoden.ArrayEqual(eigenheitenNeu, Wolke.Char.eigenheiten):
            changed = True
            Wolke.Char.eigenheiten = eigenheitenNeu

        if changed:
            self.modified.emit()

    def load(self):
        self.currentlyLoading = True

        self.ui.labelFinanzen.setVisible(Wolke.Char.finanzenAnzeigen)
        self.ui.comboFinanzen.setVisible(Wolke.Char.finanzenAnzeigen)

        ''' Load values from Char object '''
        self.ui.editName.setText(Wolke.Char.name)
        self.ui.editRasse.setText(Wolke.Char.rasse)
        self.ui.comboStatus.setCurrentIndex(Wolke.Char.status)
        self.ui.comboFinanzen.setCurrentIndex(Wolke.Char.finanzen)
        self.ui.editKurzbeschreibung.setText(Wolke.Char.kurzbeschreibung)
        arr = ["", "", "", "", "", "", "", ""]
        count = 0
        for el in Wolke.Char.eigenheiten:
            arr[count] = el
            count += 1
        self.ui.editEig1.setText(arr[0])
        self.ui.editEig2.setText(arr[1])
        self.ui.editEig3.setText(arr[2])
        self.ui.editEig4.setText(arr[3])
        self.ui.editEig5.setText(arr[4])
        self.ui.editEig6.setText(arr[5])
        self.ui.editEig7.setText(arr[6])
        self.ui.editEig8.setText(arr[7])

        ''' Fill and set Heimat '''
        self.ui.comboHeimat.clear()
        heimaten = Wolke.DB.findHeimaten()
        if len(heimaten) == 0:
            self.ui.comboHeimat.setToolTip("Diese Liste wird anhand der Talente befüllt, die mit 'Gebräuche: ' im Namen starten.\nBitte diese Talente in der Regelbasis beibehalten, die Fertigkeit 'Gebräuche' kann jedoch gelöscht werden.")
        else:
            self.ui.comboHeimat.addItems(heimaten)
            self.ui.comboHeimat.setCurrentText(Wolke.Char.heimat)

        self.currentlyLoading = False