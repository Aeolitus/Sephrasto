from PySide6 import QtWidgets, QtCore, QtGui
import UI.Hilfe
import logging
from PySide6.QtWidgets import QStyle
from PySide6.QtCore import QUrl
from Wolke import Wolke

class HilfeWrapper(QtCore.QObject):
    def __init__(self, source="Help.md", enableNavigation = True, searchPaths = ['./Doc/']):
        super().__init__()
        self.form = QtWidgets.QDialog()
        self.ui = UI.Hilfe.Ui_formHilfe()
        self.ui.setupUi(self.form)
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        if enableNavigation:
            self.ui.buttonBackward.setText('\uf0a8')
            self.ui.buttonBackward.clicked.connect(self.ui.teHelp.backward)
            self.ui.buttonForward.setText('\uf0a9')
            self.ui.buttonForward.clicked.connect(self.ui.teHelp.forward)
            self.ui.buttonHome.setText('\uf015')
            self.ui.buttonHome.clicked.connect(self.ui.teHelp.home)
        else:
            self.ui.buttonBackward.hide()
            self.ui.buttonForward.hide()
            self.ui.buttonHome.hide()
            self.ui.teHelp.setOpenLinks(False)

        self.ui.teHelp.document().setDefaultStyleSheet("table {margin-top: 1em; margin-bottom: 1em; border-collapse: collapse;} td { padding: 10px; }");
        self.ui.teHelp.sourceChanged.connect(self.stylesheetHack)
        self.ui.teHelp.backwardAvailable.connect(self.updateBackwardAvailable)
        self.ui.teHelp.forwardAvailable.connect(self.updateForwardAvailable)
        self.updateBackwardAvailable()
        self.updateForwardAvailable()

        if source is not None:
            self.ui.teHelp.setSearchPaths(searchPaths)
            self.ui.teHelp.setSource(QUrl(source))

        self.form.setWindowModality(QtCore.Qt.NonModal)
        windowSize = Wolke.Settings["WindowSize-Hilfe"]
        self.form.resize(windowSize[0], windowSize[1])
        self.form.closeEvent = self.closeEvent

    def closeEvent(self,event):
        Wolke.Settings["WindowSize-Hilfe"] = [self.form.size().width(), self.form.size().height()]

    def stylesheetHack(self, src):
        # there is no css support for markdown -.-
        # convert the markdown document to html and then set it as html
        html = self.ui.teHelp.toHtml()
        self.ui.teHelp.setHtml(html)

    def setTitle(self, text):
        self.form.setWindowTitle("Sephrasto - " + text)

    def setText(self, text):
        self.ui.teHelp.setMarkdown(text)

    def updateBackwardAvailable(self):
        self.ui.buttonBackward.setEnabled(self.ui.teHelp.isBackwardAvailable())
        
    def updateForwardAvailable(self):
        self.ui.buttonForward.setEnabled(self.ui.teHelp.isForwardAvailable())