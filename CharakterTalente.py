# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CharakterTalente.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(225, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(225, 16777215))
        self.scrollArea.setStyleSheet("padding: 1px")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 221, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plainText = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainText.setFrameShape(QtWidgets.QFrame.Box)
        self.plainText.setReadOnly(True)
        self.plainText.setObjectName("plainText")
        self.gridLayout_2.addWidget(self.plainText, 4, 0, 1, 2)
        self.spinKosten = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.spinKosten.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinKosten.setReadOnly(True)
        self.spinKosten.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinKosten.setMinimum(0)
        self.spinKosten.setMaximum(8000)
        self.spinKosten.setSingleStep(20)
        self.spinKosten.setObjectName("spinKosten")
        self.gridLayout_2.addWidget(self.spinKosten, 2, 1, 1, 1)
        self.labelName = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelName.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelName.setFont(font)
        self.labelName.setObjectName("labelName")
        self.gridLayout_2.addWidget(self.labelName, 0, 0, 1, 2)
        self.labelInfo = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelInfo.setMinimumSize(QtCore.QSize(0, 18))
        font = QtGui.QFont()
        font.setItalic(True)
        self.labelInfo.setFont(font)
        self.labelInfo.setObjectName("labelInfo")
        self.gridLayout_2.addWidget(self.labelInfo, 3, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setMaximumSize(QtCore.QSize(225, 16777215))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.listTalente = QtWidgets.QListView(Dialog)
        self.listTalente.setObjectName("listTalente")
        self.gridLayout.addWidget(self.listTalente, 0, 0, 2, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sephrasto - Talente wählen..."))
        self.spinKosten.setSuffix(_translate("Dialog", " EP"))
        self.labelName.setText(_translate("Dialog", "Talentname"))
        self.labelInfo.setText(_translate("Dialog", "Spezialtalent"))
        self.label_2.setText(_translate("Dialog", "Kosten:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

