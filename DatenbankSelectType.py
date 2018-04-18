# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatenbankSelectType.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(443, 167)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.buttonTalent = QtWidgets.QRadioButton(Dialog)
        self.buttonTalent.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonTalent.setChecked(True)
        self.buttonTalent.setObjectName("buttonTalent")
        self.gridLayout.addWidget(self.buttonTalent, 0, 0, 1, 1)
        self.buttonUebernatuerlich = QtWidgets.QRadioButton(Dialog)
        self.buttonUebernatuerlich.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonUebernatuerlich.setObjectName("buttonUebernatuerlich")
        self.gridLayout.addWidget(self.buttonUebernatuerlich, 1, 1, 1, 1)
        self.buttonFertigkeit = QtWidgets.QRadioButton(Dialog)
        self.buttonFertigkeit.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonFertigkeit.setObjectName("buttonFertigkeit")
        self.gridLayout.addWidget(self.buttonFertigkeit, 1, 0, 1, 1)
        self.buttonVorteil = QtWidgets.QRadioButton(Dialog)
        self.buttonVorteil.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonVorteil.setObjectName("buttonVorteil")
        self.gridLayout.addWidget(self.buttonVorteil, 0, 1, 1, 1)
        self.buttonWaffe = QtWidgets.QRadioButton(Dialog)
        self.buttonWaffe.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonWaffe.setObjectName("buttonWaffe")
        self.gridLayout.addWidget(self.buttonWaffe, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.buttonTalent, self.buttonVorteil)
        Dialog.setTabOrder(self.buttonVorteil, self.buttonFertigkeit)
        Dialog.setTabOrder(self.buttonFertigkeit, self.buttonUebernatuerlich)
        Dialog.setTabOrder(self.buttonUebernatuerlich, self.buttonWaffe)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sephrasto - Datenbankeintrag anlegen..."))
        self.label.setText(_translate("Dialog", "Was möchtest du anlegen?"))
        self.buttonTalent.setText(_translate("Dialog", "Talent"))
        self.buttonUebernatuerlich.setText(_translate("Dialog", "Übernatürliche Fertigkeit"))
        self.buttonFertigkeit.setText(_translate("Dialog", "Profane Fertigkeit"))
        self.buttonVorteil.setText(_translate("Dialog", "Vorteil"))
        self.buttonWaffe.setText(_translate("Dialog", "Waffe"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

