import math
import os
import re
import tempfile

from CharakterAssistent import Wizard, WizardWrapper
from PyQt5 import QtCore, QtGui, QtWidgets

import Objekte
import pdf
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from Wolke import Wolke


class Plugin:
    def __init__(self):
        EventBus.addAction("charaktereditor_geoeffnet", self.charakterGeladenHook)

    def charakterGeladenHook(self, params):
        if not params["neu"]:
            return
        self.ed = WizardWrapper.WizardWrapper()
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = Wizard.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.setupMainForm()
        self.ed.formMain.show()
