# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:35:48 2017

@author: Lennart
"""
import Wolke
import CharakterUeber
from PyQt5 import QtWidgets
class UeberWrapper(object):
    def __init__(self):
        super().__init__()
        self.formUeber = QtWidgets.QWidget()
        self.uiUeber = CharakterUeber.Ui_Form()
        self.uiUeber.setupUi(self.formUeber)