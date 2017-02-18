# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatenbankSelectType.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(443, 163)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 0, 401, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.buttonTalent = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.buttonTalent.setChecked(True)
        self.buttonTalent.setObjectName("buttonTalent")
        self.gridLayout.addWidget(self.buttonTalent, 0, 0, 1, 1)
        self.buttonUebernatuerlich = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.buttonUebernatuerlich.setObjectName("buttonUebernatuerlich")
        self.gridLayout.addWidget(self.buttonUebernatuerlich, 1, 1, 1, 1)
        self.buttonFertigkeit = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.buttonFertigkeit.setObjectName("buttonFertigkeit")
        self.gridLayout.addWidget(self.buttonFertigkeit, 1, 0, 1, 1)
        self.buttonVorteil = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.buttonVorteil.setObjectName("buttonVorteil")
        self.gridLayout.addWidget(self.buttonVorteil, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.buttonTalent, self.buttonVorteil)
        Dialog.setTabOrder(self.buttonVorteil, self.buttonFertigkeit)
        Dialog.setTabOrder(self.buttonFertigkeit, self.buttonUebernatuerlich)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Datenbankeintrag anlegen..."))
        self.label.setText(_translate("Dialog", "Was möchtest du anlegen?"))
        self.buttonTalent.setText(_translate("Dialog", "Talent"))
        self.buttonUebernatuerlich.setText(_translate("Dialog", "Übernatürliche Fertigkeit"))
        self.buttonFertigkeit.setText(_translate("Dialog", "Profane Fertigkeit"))
        self.buttonVorteil.setText(_translate("Dialog", "Vorteil"))

    def returnEntryType(self):
        if self.buttonTalent.isChecked():
            return "Talent"
        elif self.buttonVorteil.isChecked():
            return "Vorteil"
        elif self.buttonFertigkeit.isChecked():
            return "Fertigkeit"
        else:
            return "Übernatürliche Fertigkeit"
            

if __name__ == "__main__":
    import sys
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

