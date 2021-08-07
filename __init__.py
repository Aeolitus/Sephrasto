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

    def charakterGeladenHook(self, params):
        if not params["neu"]:
            return
        self.ed = WizardWrapper.WizardWrapper()
        self.ed.formMain = QtWidgets.QWidget()
        self.ed.ui = Wizard.Ui_formMain()
        self.ed.ui.setupUi(self.ed.formMain)
        self.ed.setupMainForm()
        self.ed.formMain.show()