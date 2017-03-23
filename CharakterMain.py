# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CharakterMain.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_formMain(object):
    def setupUi(self, formMain):
        formMain.setObjectName("formMain")
        formMain.setWindowModality(QtCore.Qt.ApplicationModal)
        formMain.resize(713, 491)
        self.gridLayout = QtWidgets.QGridLayout(formMain)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabs = QtWidgets.QTabWidget(formMain)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabs)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(formMain)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.spinEP = QtWidgets.QSpinBox(formMain)
        self.spinEP.setAlignment(QtCore.Qt.AlignCenter)
        self.spinEP.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinEP.setMaximum(100000)
        self.spinEP.setObjectName("spinEP")
        self.horizontalLayout_2.addWidget(self.spinEP)
        self.label_2 = QtWidgets.QLabel(formMain)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinRemaining = QtWidgets.QSpinBox(formMain)
        self.spinRemaining.setAutoFillBackground(False)
        self.spinRemaining.setAlignment(QtCore.Qt.AlignCenter)
        self.spinRemaining.setReadOnly(True)
        self.spinRemaining.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinRemaining.setMinimum(-100000)
        self.spinRemaining.setMaximum(100000)
        self.spinRemaining.setObjectName("spinRemaining")
        self.horizontalLayout_2.addWidget(self.spinRemaining)
        self.checkReq = QtWidgets.QCheckBox(formMain)
        self.checkReq.setChecked(True)
        self.checkReq.setObjectName("checkReq")
        self.horizontalLayout_2.addWidget(self.checkReq)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonSave = QtWidgets.QPushButton(formMain)
        self.buttonSave.setMinimumSize(QtCore.QSize(75, 0))
        self.buttonSave.setObjectName("buttonSave")
        self.horizontalLayout_2.addWidget(self.buttonSave)
        self.buttonSavePDF = QtWidgets.QPushButton(formMain)
        self.buttonSavePDF.setMinimumSize(QtCore.QSize(100, 0))
        self.buttonSavePDF.setMaximumSize(QtCore.QSize(16777214, 16777215))
        self.buttonSavePDF.setObjectName("buttonSavePDF")
        self.horizontalLayout_2.addWidget(self.buttonSavePDF)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(formMain)
        QtCore.QMetaObject.connectSlotsByName(formMain)

    def retranslateUi(self, formMain):
        _translate = QtCore.QCoreApplication.translate
        formMain.setWindowTitle(_translate("formMain", "Sephrasto - Charakter erstellen"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("formMain", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("formMain", "Tab 2"))
        self.label.setText(_translate("formMain", " Erfahrung: "))
        self.spinEP.setSuffix(_translate("formMain", " EP"))
        self.label_2.setText(_translate("formMain", " Verfügbar: "))
        self.spinRemaining.setSuffix(_translate("formMain", " EP"))
        self.checkReq.setText(_translate("formMain", "Voraussetzungen"))
        self.buttonSave.setText(_translate("formMain", "Speichern"))
        self.buttonSavePDF.setText(_translate("formMain", "PDF erstellen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    formMain = QtWidgets.QWidget()
    ui = Ui_formMain()
    ui.setupUi(formMain)
    formMain.show()
    sys.exit(app.exec_())

