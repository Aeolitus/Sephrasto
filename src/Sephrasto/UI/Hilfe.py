# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Hilfe.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_formHilfe(object):
    def setupUi(self, formHilfe):
        formHilfe.setObjectName("formHilfe")
        formHilfe.setWindowModality(QtCore.Qt.NonModal)
        formHilfe.resize(872, 460)
        self.gridLayout_3 = QtWidgets.QGridLayout(formHilfe)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonBackward = QtWidgets.QToolButton(formHilfe)
        self.buttonBackward.setObjectName("buttonBackward")
        self.horizontalLayout.addWidget(self.buttonBackward)
        self.buttonForward = QtWidgets.QToolButton(formHilfe)
        self.buttonForward.setObjectName("buttonForward")
        self.horizontalLayout.addWidget(self.buttonForward)
        self.buttonHome = QtWidgets.QToolButton(formHilfe)
        self.buttonHome.setObjectName("buttonHome")
        self.horizontalLayout.addWidget(self.buttonHome)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.teHelp = QtWidgets.QTextBrowser(formHilfe)
        self.teHelp.setOpenExternalLinks(True)
        self.teHelp.setObjectName("teHelp")
        self.gridLayout_3.addWidget(self.teHelp, 1, 0, 1, 2)

        self.retranslateUi(formHilfe)
        QtCore.QMetaObject.connectSlotsByName(formHilfe)

    def retranslateUi(self, formHilfe):
        _translate = QtCore.QCoreApplication.translate
        formHilfe.setWindowTitle(_translate("formHilfe", "Sephrasto - Hilfe"))
        self.buttonBackward.setText(_translate("formHilfe", "..."))
        self.buttonForward.setText(_translate("formHilfe", "..."))
        self.buttonHome.setText(_translate("formHilfe", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    formHilfe = QtWidgets.QWidget()
    ui = Ui_formHilfe()
    ui.setupUi(formHilfe)
    formHilfe.show()
    sys.exit(app.exec_())