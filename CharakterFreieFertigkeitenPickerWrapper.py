from PyQt5 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import CharakterFreieFertigkeitenPicker
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

        self.Form = QtWidgets.QDialog()
        self.ui = CharakterFreieFertigkeitenPicker.Ui_Dialog()
        self.ui.setupUi(self.Form)
        
        self.Form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.populateTree()

        self.ui.treeFerts.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeFerts.itemDoubleClicked.connect(lambda item, column: self.ui.buttonBox.buttons()[0].click())
        self.ui.treeFerts.header().setSectionResizeMode(0,1)
        self.ui.treeFerts.setFocus()
        self.ui.nameFilterEdit.textChanged.connect(self.populateTree)
        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted and self.current != '':
            freieFertigkeit = Wolke.DB.freieFertigkeiten[self.current]
            self.fertigkeit = self.formatName(freieFertigkeit)
        else:
            self.fertigkeit = None

    def formatName(self, freieFertigkeit):
        return EventBus.applyFilter("format_freiefertigkeit_name", freieFertigkeit.kategorie + ": " + freieFertigkeit.name, { "fertigkeit" : freieFertigkeit } )

    def populateTree(self):
        currSet = self.current != ""
        self.ui.treeFerts.clear();
        kategorien = self.findKategorien()
        for kategorie in kategorien:
            ferts = []
            for fert in Wolke.DB.freieFertigkeiten:
                if Wolke.DB.freieFertigkeiten[fert].kategorie != kategorie:
                    continue
                if self.ui.nameFilterEdit.text() and (not self.ui.nameFilterEdit.text().lower() in fert.lower()) and (not self.ui.nameFilterEdit.text().lower() in kategorie.lower()):
                    continue
                if fert != self.current and self.formatName(Wolke.DB.freieFertigkeiten[fert]) in [fert.name for fert in Wolke.Char.freieFertigkeiten]:
                    continue
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.freieFertigkeiten[fert].voraussetzungen):
                    ferts.append(fert)
            ferts.sort()
            if len(ferts) == 0:
                continue

            parent = QtWidgets.QTreeWidgetItem(self.ui.treeFerts)
            parent.setText(0,kategorie)
            parent.setExpanded(True)
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
                self.ui.treeFerts.setCurrentItem(found[0], 0, QtCore.QItemSelectionModel.Select)
        elif self.ui.treeFerts.topLevelItemCount() > 0 and self.ui.treeFerts.topLevelItem(0).childCount() > 0:
            self.ui.treeFerts.setCurrentItem(self.ui.treeFerts.topLevelItem(0).child(0), 0, QtCore.QItemSelectionModel.Select)
        self.changeHandler()


    def findKategorien(self):
        kategorien = {}
        for tal in Wolke.DB.freieFertigkeiten:
            kategorien[Wolke.DB.freieFertigkeiten[tal].kategorie] = True
        return sorted(kategorien.keys())

    def changeHandler(self):
        kategorien = self.findKategorien()
        self.current = ""
        for el in self.ui.treeFerts.selectedItems():
            if el.text(0) in kategorien:
                continue
            self.current = el.data(0, QtCore.Qt.UserRole) # contains key of fert
            break