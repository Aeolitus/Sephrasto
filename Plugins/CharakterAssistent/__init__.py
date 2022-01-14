from PyQt5 import QtWidgets, QtCore, QtGui
from EventBus import EventBus
from Wolke import Wolke
import tempfile
import pdf
import os
import re
import math
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
import Objekte
from CharakterAssistent import Wizard
from CharakterAssistent import WizardWrapper

class Plugin:

    def __init__(self):
        EventBus.addAction("charaktereditor_geoeffnet", self.charakterGeladenHook)

    @staticmethod
    def getDescription():
        return "Wenn du einen neuen Charakter erstellst, erscheint ein Popup mit du auf Basis von Vorlagen mit wenigen Clicks ein solides Grundgerüst erhältst."

    def charakterGeladenHook(self, params):
        if not params["neu"]:
            return
        self.ed = WizardWrapper.WizardWrapper()

        self.ed.formMain = QtWidgets.QDialog()
        self.ed.formMain .setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)

        self.ed.ui = Wizard.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.setupMainForm()
        self.ed.formMain.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ed.formMain.show()
        self.ed.formMain.exec_()