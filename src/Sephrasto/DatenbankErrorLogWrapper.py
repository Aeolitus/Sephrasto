# -*- coding: utf-8 -*-
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
import UI.DatenbankErrorLog

class DatenbankErrorLogWrapper():
    def __init__(self, datenbank, editCallback):
        self.datenbank = datenbank
        self.editCallback = editCallback
        self.form = QtWidgets.QDialog()
        self.ui = UI.DatenbankErrorLog.Ui_dialog()
        self.ui.setupUi(self.form)

        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        self.load()
        self.ui.buttonRefresh.clicked.connect(self.refresh)
        self.ui.buttonRefresh.setText('\uf2f1')
        self.ui.listWidget.itemDoubleClicked.connect(self.onClicked)
        settingName = "WindowSize-DBErrorLog"
        if not settingName in Wolke.Settings:
            Wolke.Settings[settingName] = [768, 522]
        windowSize = Wolke.Settings[settingName]
        self.form.resize(windowSize[0], windowSize[1])
        self.form.setWindowModality(QtCore.Qt.NonModal)
        self.form.show()
        Wolke.Settings[settingName] = [self.form.size().width(), self.form.size().height()]

    def refresh(self):      
        self.load()
        if len(self.datenbank.loadingErrors) > 0:
            self.form.show()
            self.form.activateWindow()


    def load(self):
        self.datenbank.verify()
        self.ui.listWidget.clear()
        if len(self.datenbank.loadingErrors) == 0:
            self.ui.label.setText(f"<span style='{Wolke.FontAwesomeCSS} color: {Wolke.ValidColor};'>\uf164</span>&nbsp;&nbsp;Keine Probleme gefunden.")
        else:
            self.ui.label.setText(f"<span style='{Wolke.FontAwesomeCSS} color: {Wolke.WarningColor};'>\uf071</span>&nbsp;&nbsp;Probleme bei den Hausregeln entdeckt! Mit einem Doppelclick gelangst du direkt zum entsprechenden Element.")

        for log in self.datenbank.loadingErrors:
            item = QtWidgets.QListWidgetItem(log[1])
            item.setData(QtCore.Qt.UserRole, log)
            self.ui.listWidget.addItem(item)

    def onClicked(self, item):
        log = item.data(QtCore.Qt.UserRole)
        fixed = self.editCallback(log[0])
        if fixed:
            self.refresh()
