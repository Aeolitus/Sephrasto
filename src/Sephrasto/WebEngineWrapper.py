from PySide6 import QtWidgets, QtCore, QtGui
import logging
from PySide6.QtWidgets import QStyle
from PySide6.QtCore import QUrl
from Wolke import Wolke
from QtUtils.WebEngineViewPlus import WebEngineViewPlus
import os

class WebEngineWrapper(QtCore.QObject):
    def __init__(self, windowTitle, source = "", extraCss = "", sizeSettingKey = "", backgroundColor = QtCore.Qt.transparent):
        super().__init__()
        self.sizeSettingKey = sizeSettingKey

        self.form = QtWidgets.QDialog()
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.setTitle(windowTitle)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.form)
        self.webengineView = WebEngineViewPlus()
        self.verticalLayout.addWidget(self.webengineView)

        self.webengineView.page().setBackgroundColor(backgroundColor)

        theme = Wolke.Themes[Wolke.Settings["Theme"]]

        if extraCss:
            self.webengineView.insertStyleSheet("extraCss", extraCss)

        if source:
            self.load(source)

        self.form.setWindowModality(QtCore.Qt.NonModal)
        if self.sizeSettingKey:
            windowSize = Wolke.Settings[self.sizeSettingKey]
            self.form.resize(windowSize[0], windowSize[1])
            self.form.closeEvent = self.closeEvent
        else:
            self.form.resize(1280, 768)

    def closeEvent(self,event):
        Wolke.Settings[self.sizeSettingKey] = [self.form.size().width(), self.form.size().height()]

    def setTitle(self, text):
        self.form.setWindowTitle("Sephrasto - " + text)

    def setHtml(self, html):
        self.webengineView.setHtml(html)

    def load(self, url):
        # web engine requires regular forward slashes and fully qualified paths...
        if url.startswith("./") or url.startswith(".\\"):
            url = os.getcwd() + url[1:]
        url = url.replace('\\', '/')
        self.webengineView.load(url)