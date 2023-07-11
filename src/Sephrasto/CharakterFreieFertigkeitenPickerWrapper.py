from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import UI.CharakterFreieFertigkeitenPicker
from EventBus import EventBus

class CharakterFreieFertigkeitenPickerWrapper(object):
    def __init__(self, fertigkeit=None):
        super().__init__()
        
        self.current = ""
        if fertigkeit is not None:
            if ": " in fertigkeit and (not fertigkeit in Wolke.DB.freieFertigkeiten):
                fertigkeit = fertigkeit.split(": ")[1]

            if fertigkeit in Wolke.DB.freieFertigkeiten:
                self.current = fertigkeit

        self.form = QtWidgets.QDialog()
        self.ui = UI.CharakterFreieFertigkeitenPicker.Ui_Dialog()
        self.ui.setupUi(self.form)
        
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Abbrechen")

        windowSize = Wolke.Settings["WindowSize-FreieFert"]
        self.form.resize(windowSize[0], windowSize[1])
        
        self.ui.treeFerts.setHeaderHidden(True)
        self.populateTree()

        self.ui.treeFerts.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeFerts.itemDoubleClicked.connect(lambda item, column: self.ui.buttonBox.buttons()[0].click())
        self.ui.treeFerts.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.ui.labelFilter.setText("\uf002")
        self.ui.nameFilterEdit.setFocus()
        self.ui.nameFilterEdit.textChanged.connect(self.populateTree)
        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()
        Wolke.Settings["WindowSize-FreieFert"] = [self.form.size().width(), self.form.size().height()]
        if self.ret == QtWidgets.QDialog.Accepted and self.current != '':
            freieFertigkeit = Wolke.DB.freieFertigkeiten[self.current]
            self.fertigkeit = self.formatName(freieFertigkeit)
        else:
            self.fertigkeit = None

    def formatName(self, freieFertigkeit):
        kategorie = freieFertigkeit.kategorie
        for abbreviation in Wolke.DB.einstellungen["FreieFertigkeiten: Typ-Abkürzungen"].wert:
            kategorie = kategorie.replace(abbreviation, Wolke.DB.einstellungen["FreieFertigkeiten: Typ-Abkürzungen"].wert[abbreviation])

        if kategorie.strip():
            return kategorie + ": " + freieFertigkeit.name
        else:
            return freieFertigkeit.name

    def populateTree(self):
        currSet = self.current != ""
        self.ui.treeFerts.clear();
        for kategorie in Wolke.DB.einstellungen["FreieFertigkeiten: Typen"].wert:
            ferts = []
            for fert in Wolke.DB.freieFertigkeiten:
                if Wolke.DB.freieFertigkeiten[fert].kategorie != kategorie:
                    continue
                if self.ui.nameFilterEdit.text() and (not self.ui.nameFilterEdit.text().lower() in fert.lower()) and (not self.ui.nameFilterEdit.text().lower() in kategorie.lower()):
                    continue
                if fert != self.current and self.formatName(Wolke.DB.freieFertigkeiten[fert]) in [fert.name for fert in Wolke.Char.freieFertigkeiten]:
                    continue
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.freieFertigkeiten[fert]):
                    ferts.append(fert)
            ferts.sort()
            if len(ferts) == 0:
                continue

            parent = QtWidgets.QTreeWidgetItem(self.ui.treeFerts)
            parent.setText(0,kategorie)
            parent.setExpanded(True)
            font = QtGui.QFont(Wolke.Settings["Font"], Wolke.FontHeadingSizeL3)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            parent.setFont(0, font)
            for el in ferts:
                if not currSet:
                    self.current = el
                    currSet = True
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, Wolke.DB.freieFertigkeiten[el].name)
                child.setData(0, QtCore.Qt.UserRole, el) # store key of talent in user data

        self.ui.treeFerts.sortItems(1,QtCore.Qt.AscendingOrder)

        if self.current in Wolke.DB.freieFertigkeiten:
            name = Wolke.DB.freieFertigkeiten[self.current].name
            found = self.ui.treeFerts.findItems(name, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            if len(found) > 0:
                self.ui.treeFerts.setCurrentItem(found[0], 0, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        elif self.ui.treeFerts.topLevelItemCount() > 0 and self.ui.treeFerts.topLevelItem(0).childCount() > 0:
            self.ui.treeFerts.setCurrentItem(self.ui.treeFerts.topLevelItem(0).child(0), 0, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        self.changeHandler()

    def changeHandler(self):
        self.current = ""
        for el in self.ui.treeFerts.selectedItems():
            if el.text(0) in Wolke.DB.einstellungen["FreieFertigkeiten: Typen"].wert:
                continue
            self.current = el.data(0, QtCore.Qt.UserRole) # contains key of fert
            break