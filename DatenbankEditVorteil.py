# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatenbankEditVorteil.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden

class Ui_vorteilDialog(object):
    def setupUi(self, vorteilDialog):
        vorteilDialog.setObjectName("talentDialog")
        vorteilDialog.resize(381, 304)
        self.buttonBox = QtWidgets.QDialogButtonBox(vorteilDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 271, 361, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(vorteilDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.nameEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.voraussetzungenEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.voraussetzungenEdit.setObjectName("voraussetzungenEdit")
        self.gridLayout.addWidget(self.voraussetzungenEdit, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.textEdit = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 4, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboNachkauf = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboNachkauf.setObjectName("comboNachkauf")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.horizontalLayout.addWidget(self.comboNachkauf)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.kostenEdit = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.kostenEdit.setMaximum(160)
        self.kostenEdit.setSingleStep(20)
        self.kostenEdit.setProperty("value", 40)
        self.kostenEdit.setObjectName("kostenEdit")
        self.horizontalLayout_2.addWidget(self.kostenEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.retranslateUi(vorteilDialog)
        self.buttonBox.accepted.connect(vorteilDialog.accept)
        self.buttonBox.rejected.connect(vorteilDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(vorteilDialog)
        vorteilDialog.setTabOrder(self.nameEdit, self.kostenEdit)
        vorteilDialog.setTabOrder(self.kostenEdit, self.comboNachkauf)
        vorteilDialog.setTabOrder(self.comboNachkauf, self.voraussetzungenEdit)
        vorteilDialog.setTabOrder(self.voraussetzungenEdit, self.textEdit)

    def retranslateUi(self, vorteilDialog):
        _translate = QtCore.QCoreApplication.translate
        vorteilDialog.setWindowTitle(_translate("vorteilDialog", "Vorteils-Editor"))
        self.label.setText(_translate("vorteilDialog", "Vorteilsname"))
        self.label_2.setText(_translate("vorteilDialog", "Lernkosten"))
        self.label_3.setText(_translate("vorteilDialog", "Nachkauf"))
        self.label_4.setText(_translate("vorteilDialog", "Voraussetzungen"))
        self.label_5.setText(_translate("vorteilDialog", "Text"))
        self.comboNachkauf.setItemText(0, _translate("vorteilDialog", "häufig"))
        self.comboNachkauf.setItemText(1, _translate("vorteilDialog", "üblich"))
        self.comboNachkauf.setItemText(2, _translate("vorteilDialog", "selten"))
        self.comboNachkauf.setItemText(3, _translate("vorteilDialog", "extrem selten"))
        self.comboNachkauf.setItemText(4, _translate("vorteilDialog", "nicht möglich"))
        self.kostenEdit.setSuffix(_translate("vorteilDialog", " EP"))
        
    def createVorteil(self):
        vort = Fertigkeiten.Vorteil()
        vort.name = self.nameEdit.text()
        vort.kosten = self.kostenEdit.value()
        vort.nachkauf = self.comboNachkauf.currentText()
        vort.voraussetzungen = Hilfsmethoden.VorStr2Array(self.voraussetzungenEdit.text(),None)
        vort.text = self.textEdit.toPlainText()
        return vort
        
if __name__ == "__main__":
    import sys
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    vorteilDialog = QtWidgets.QDialog()
    ui = Ui_vorteilDialog()
    ui.setupUi(vorteilDialog)
    vorteilDialog.show()
    sys.exit(app.exec_())