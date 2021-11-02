import logging

import lxml.etree as etree
from PyQt5 import QtCore, QtWidgets

import CharakterNotiz
from Wolke import Wolke


class CharakterNotizWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = CharakterNotiz.Ui_formNotiz()
        self.ui.setupUi(self.form)

        self.ui.teNotiz.setPlainText(Wolke.Char.notiz)
        self.ui.teNotiz.textChanged.connect(self.valueChanged)

    def valueChanged(self):
        Wolke.Char.notiz = self.ui.teNotiz.toPlainText()
        self.modified.emit()
