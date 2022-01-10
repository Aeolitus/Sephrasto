from PyQt5 import QtWidgets, QtCore
import Hilfe
import logging
from PyQt5.QtWidgets import QStyle
from PyQt5.QtCore import QUrl

class HilfeWrapper(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QDialog()
        self.ui = Hilfe.Ui_formHilfe()
        self.ui.setupUi(self.form)
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.ui.buttonBackward.setIcon(self.form.style().standardIcon(QStyle.SP_ArrowBack))
        self.ui.buttonBackward.clicked.connect(self.ui.teHelp.backward)
        self.ui.buttonForward.setIcon(self.form.style().standardIcon(QStyle.SP_ArrowForward))
        self.ui.buttonForward.clicked.connect(self.ui.teHelp.forward)
        self.ui.buttonHome.setIcon(self.form.style().standardIcon(QStyle.SP_ArrowUp))
        self.ui.buttonHome.clicked.connect(self.ui.teHelp.home)

        self.ui.teHelp.backwardAvailable.connect(self.updateBackwardAvailable)
        self.ui.teHelp.forwardAvailable.connect(self.updateForwardAvailable)
        self.updateBackwardAvailable()
        self.updateForwardAvailable()

        self.ui.teHelp.setSearchPaths(['./Doc/'])
        self.ui.teHelp.setSource(QUrl('Help.md'))

        self.form.setWindowModality(QtCore.Qt.NonModal)
        self.form.show()

    def updateBackwardAvailable(self):
        self.ui.buttonBackward.setEnabled(self.ui.teHelp.isBackwardAvailable())
        
    def updateForwardAvailable(self):
        self.ui.buttonForward.setEnabled(self.ui.teHelp.isForwardAvailable())