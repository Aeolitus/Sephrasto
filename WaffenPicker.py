# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import CharakterWaffen
from PyQt5 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import Objekte
import Definitionen

class WaffenPicker(object):
    def __init__(self,waffe=None):
        super().__init__()
        self.waffe = waffe
        self.Form = QtWidgets.QDialog()
        self.ui = CharakterWaffen.Ui_Dialog()
        self.ui.setupUi(self.Form)
        
        for kind in Definitionen.Kampftalente:
            parent = QtWidgets.QTreeWidgetItem(self.ui.treeWeapons)
            parent.setText(0,kind)
            parent.setExpanded(True)
            
        
        self.Form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Form.show()
        self.ret = self.Form.exec_()
        if self.ret == QtWidgets.QDialog.Accepted:
            pass
        else:
            self.waffe = None
    
