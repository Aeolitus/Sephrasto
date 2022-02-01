from PyQt5 import QtWidgets, QtCore
import UI.CharakterNotiz
import lxml.etree as etree
import logging
from Wolke import Wolke

class CharakterNotizWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = UI.CharakterNotiz.Ui_formNotiz()
        self.ui.setupUi(self.form)

        self.ui.teNotiz.setPlainText(Wolke.Char.notiz)
        self.ui.teNotiz.textChanged.connect(self.valueChanged)

    def valueChanged(self):
        Wolke.Char.notiz = self.ui.teNotiz.toPlainText()
        self.modified.emit()