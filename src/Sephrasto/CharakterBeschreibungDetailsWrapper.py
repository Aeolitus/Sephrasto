from PySide6 import QtWidgets, QtCore, QtGui
import UI.CharakterBeschreibungDetails
import UI.CharakterBeschreibung
import CharakterBeschreibungWrapper
from Wolke import Wolke
import logging
import tempfile
from EventBus import EventBus

class CharakterBeschreibungDetailsWrapper(QtCore.QObject):
    modified = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterBeschreibungDetails.Ui_formBeschreibung()
        self.ui.setupUi(self.form)

        self.ui.chkKultur.stateChanged.connect(self.updateDetails)

        self.ui.leKultur.editingFinished.connect(self.updateDetails)
        self.ui.leProfession.editingFinished.connect(self.updateDetails)
        self.ui.leGeschlecht.editingFinished.connect(self.updateDetails)
        self.ui.leGeburtsdatum.editingFinished.connect(self.updateDetails)
        self.ui.leGroesse.editingFinished.connect(self.updateDetails)
        self.ui.leGewicht.editingFinished.connect(self.updateDetails)
        self.ui.leHaarfarbe.editingFinished.connect(self.updateDetails)
        self.ui.leAugenfarbe.editingFinished.connect(self.updateDetails)
        self.ui.leTitel.editingFinished.connect(self.updateDetails)

        self.ui.leAussehen1.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen2.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen3.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen4.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen5.editingFinished.connect(self.updateDetails)
        self.ui.leAussehen6.editingFinished.connect(self.updateDetails)

        self.ui.leHintergrund0.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund1.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund2.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund3.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund4.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund5.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund6.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund7.editingFinished.connect(self.updateDetails)
        self.ui.leHintergrund8.editingFinished.connect(self.updateDetails)

        self.currentlyLoading = False

    def load(self):
        self.currentlyLoading = True

        if Wolke.Char.kultur:
            self.ui.chkKultur.setChecked(False)
            self.ui.leKultur.setText(Wolke.Char.kultur)
        else:
            self.ui.leKultur.setText(Wolke.Char.heimat)

        self.ui.leKultur.setEnabled(not self.ui.chkKultur.isChecked())

        self.ui.leProfession.setText(Wolke.Char.profession)
        self.ui.leGeschlecht.setText(Wolke.Char.geschlecht)
        self.ui.leGeburtsdatum.setText(Wolke.Char.geburtsdatum)
        self.ui.leGroesse.setText(Wolke.Char.groesse)
        self.ui.leGewicht.setText(Wolke.Char.gewicht)
        self.ui.leHaarfarbe.setText(Wolke.Char.haarfarbe)
        self.ui.leAugenfarbe.setText(Wolke.Char.augenfarbe)
        self.ui.leTitel.setText(Wolke.Char.titel)

        self.ui.leAussehen1.setText(Wolke.Char.aussehen[0])
        self.ui.leAussehen2.setText(Wolke.Char.aussehen[1])
        self.ui.leAussehen3.setText(Wolke.Char.aussehen[2])
        self.ui.leAussehen4.setText(Wolke.Char.aussehen[3])
        self.ui.leAussehen5.setText(Wolke.Char.aussehen[4])
        self.ui.leAussehen6.setText(Wolke.Char.aussehen[5])

        self.ui.leHintergrund0.setText(Wolke.Char.hintergrund[0])
        self.ui.leHintergrund1.setText(Wolke.Char.hintergrund[1])
        self.ui.leHintergrund2.setText(Wolke.Char.hintergrund[2])
        self.ui.leHintergrund3.setText(Wolke.Char.hintergrund[3])
        self.ui.leHintergrund4.setText(Wolke.Char.hintergrund[4])
        self.ui.leHintergrund5.setText(Wolke.Char.hintergrund[5])
        self.ui.leHintergrund6.setText(Wolke.Char.hintergrund[6])
        self.ui.leHintergrund7.setText(Wolke.Char.hintergrund[7])
        self.ui.leHintergrund8.setText(Wolke.Char.hintergrund[8])

        self.currentlyLoading = False

    def updateDetails(self):
        if self.currentlyLoading:
            return

        changed = False

        self.ui.leKultur.setEnabled(not self.ui.chkKultur.isChecked())
        if not self.ui.chkKultur.isChecked():
            if Wolke.Char.kultur != self.ui.leKultur.text():
                Wolke.Char.kultur = self.ui.leKultur.text()
                changed = True
        else:
            if Wolke.Char.kultur:
                Wolke.Char.kultur = ""
                changed = True
            self.ui.leKultur.setText(Wolke.Char.heimat)

        if Wolke.Char.profession != self.ui.leProfession.text():
            Wolke.Char.profession = self.ui.leProfession.text()
            changed = True
        if Wolke.Char.geschlecht != self.ui.leGeschlecht.text():
            Wolke.Char.geschlecht = self.ui.leGeschlecht.text()
            changed = True
        if Wolke.Char.geburtsdatum != self.ui.leGeburtsdatum.text():
            Wolke.Char.geburtsdatum = self.ui.leGeburtsdatum.text()
            changed = True
        if Wolke.Char.groesse != self.ui.leGroesse.text():
            Wolke.Char.groesse = self.ui.leGroesse.text()
            changed = True
        if Wolke.Char.gewicht != self.ui.leGewicht.text():
            Wolke.Char.gewicht = self.ui.leGewicht.text()
            changed = True
        if Wolke.Char.haarfarbe != self.ui.leHaarfarbe.text():
            Wolke.Char.haarfarbe = self.ui.leHaarfarbe.text()
            changed = True
        if Wolke.Char.augenfarbe != self.ui.leAugenfarbe.text():
            Wolke.Char.augenfarbe = self.ui.leAugenfarbe.text()
            changed = True
        if Wolke.Char.titel != self.ui.leTitel.text():
            Wolke.Char.titel = self.ui.leTitel.text()
            changed = True

        if Wolke.Char.aussehen[0] != self.ui.leAussehen1.text():
            Wolke.Char.aussehen[0] = self.ui.leAussehen1.text()
            changed = True
        if Wolke.Char.aussehen[1] != self.ui.leAussehen2.text():
            Wolke.Char.aussehen[1] = self.ui.leAussehen2.text()
            changed = True
        if Wolke.Char.aussehen[2] != self.ui.leAussehen3.text():
            Wolke.Char.aussehen[2] = self.ui.leAussehen3.text()
            changed = True
        if Wolke.Char.aussehen[3] != self.ui.leAussehen4.text():
            Wolke.Char.aussehen[3] = self.ui.leAussehen4.text()
            changed = True
        if Wolke.Char.aussehen[4] != self.ui.leAussehen5.text():
            Wolke.Char.aussehen[4] = self.ui.leAussehen5.text()
            changed = True
        if Wolke.Char.aussehen[5] != self.ui.leAussehen6.text():
            Wolke.Char.aussehen[5] = self.ui.leAussehen6.text()
            changed = True

        if Wolke.Char.hintergrund[0] != self.ui.leHintergrund0.text():
            Wolke.Char.hintergrund[0] = self.ui.leHintergrund0.text()
            changed = True
        if Wolke.Char.hintergrund[1] != self.ui.leHintergrund1.text():
            Wolke.Char.hintergrund[1] = self.ui.leHintergrund1.text()
            changed = True
        if Wolke.Char.hintergrund[2] != self.ui.leHintergrund2.text():
            Wolke.Char.hintergrund[2] = self.ui.leHintergrund2.text()
            changed = True
        if Wolke.Char.hintergrund[3] != self.ui.leHintergrund3.text():
            Wolke.Char.hintergrund[3] = self.ui.leHintergrund3.text()
            changed = True
        if Wolke.Char.hintergrund[4] != self.ui.leHintergrund4.text():
            Wolke.Char.hintergrund[4] = self.ui.leHintergrund4.text()
            changed = True
        if Wolke.Char.hintergrund[5] != self.ui.leHintergrund5.text():
            Wolke.Char.hintergrund[5] = self.ui.leHintergrund5.text()
            changed = True
        if Wolke.Char.hintergrund[6] != self.ui.leHintergrund6.text():
            Wolke.Char.hintergrund[6] = self.ui.leHintergrund6.text()
            changed = True
        if Wolke.Char.hintergrund[7] != self.ui.leHintergrund7.text():
            Wolke.Char.hintergrund[7] = self.ui.leHintergrund7.text()
            changed = True
        if Wolke.Char.hintergrund[8] != self.ui.leHintergrund8.text():
            Wolke.Char.hintergrund[8] = self.ui.leHintergrund8.text()
            changed = True

        if changed:
            self.modified.emit()