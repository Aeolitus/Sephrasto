# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatenbankEditTalent.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import Fertigkeiten

class Ui_talentDialog(object):
    def setupUi(self, talentDialog):
        talentDialog.setObjectName("talentDialog")
        talentDialog.resize(381, 304)
        self.buttonBox = QtWidgets.QDialogButtonBox(talentDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 271, 361, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(talentDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.nameEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.fertigkeitenEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.fertigkeitenEdit.setObjectName("fertigkeitenEdit")
        self.gridLayout.addWidget(self.fertigkeitenEdit, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonRegulaer = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.buttonRegulaer.setChecked(True)
        self.buttonRegulaer.setObjectName("buttonRegulaer")
        self.verticalLayout.addWidget(self.buttonRegulaer)
        self.buttonVerbilligt = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.buttonVerbilligt.setObjectName("buttonVerbilligt")
        self.verticalLayout.addWidget(self.buttonVerbilligt)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonSpezial = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.buttonSpezial.setObjectName("buttonSpezial")
        self.horizontalLayout.addWidget(self.buttonSpezial)
        self.comboKosten = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboKosten.setObjectName("comboKosten")
        self.comboKosten.addItem("")
        self.comboKosten.addItem("")
        self.comboKosten.addItem("")
        self.comboKosten.addItem("")
        self.comboKosten.addItem("")
        self.comboKosten.addItem("")
        self.horizontalLayout.addWidget(self.comboKosten)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
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

        self.retranslateUi(talentDialog)
        self.buttonBox.accepted.connect(talentDialog.accept)
        self.buttonBox.rejected.connect(talentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(talentDialog)
        talentDialog.setTabOrder(self.nameEdit, self.buttonRegulaer)
        talentDialog.setTabOrder(self.buttonRegulaer, self.buttonVerbilligt)
        talentDialog.setTabOrder(self.buttonVerbilligt, self.buttonSpezial)
        talentDialog.setTabOrder(self.buttonSpezial, self.comboKosten)
        talentDialog.setTabOrder(self.comboKosten, self.fertigkeitenEdit)
        talentDialog.setTabOrder(self.fertigkeitenEdit, self.voraussetzungenEdit)
        talentDialog.setTabOrder(self.voraussetzungenEdit, self.textEdit)

    def retranslateUi(self, talentDialog):
        _translate = QtCore.QCoreApplication.translate
        talentDialog.setWindowTitle(_translate("talentDialog", "Talent-Editor"))
        self.label.setText(_translate("talentDialog", "Talentname"))
        self.label_2.setText(_translate("talentDialog", "Lernkosten"))
        self.buttonRegulaer.setText(_translate("talentDialog", "Reguläres Talent (Kosten nach Fertigkeit)"))
        self.buttonVerbilligt.setText(_translate("talentDialog", "Verbilligtes Talent (Kosten nach Fertigkeit)"))
        self.buttonSpezial.setText(_translate("talentDialog", "Spezialtalent (Kosten frei wählbar)"))
        self.comboKosten.setItemText(0, _translate("talentDialog", "0 EP"))
        self.comboKosten.setItemText(1, _translate("talentDialog", "20 EP"))
        self.comboKosten.setItemText(2, _translate("talentDialog", "40 EP"))
        self.comboKosten.setItemText(3, _translate("talentDialog", "60 EP"))
        self.comboKosten.setItemText(4, _translate("talentDialog", "80 EP"))
        self.comboKosten.setItemText(5, _translate("talentDialog", "100 EP"))
        self.label_3.setText(_translate("talentDialog", "Fertigkeiten"))
        self.label_4.setText(_translate("talentDialog", "Voraussetzungen"))
        self.label_5.setText(_translate("talentDialog", "Text"))

    def createTalent(self):
        tal = Fertigkeiten.Talent()
        tal.name = self.nameEdit.text()
        tal.fertigkeiten = eval(self.fertigkeitenEdit.text())
        tal.voraussetzungen = eval(self.voraussetzungenEdit.text())
        tal.text = self.textEdit.toPlainText()
        if self.buttonSpezial.isChecked():
            tal.kosten = int(self.comboKosten.currentText()[:2])
            if tal.kosten == 10:
                tal.kosten = 100
        elif self.buttonVerbilligt.isChecked():
            tal.verbilligt = 1;
        return tal

if __name__ == "__main__":
    import sys
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    talentDialog = QtWidgets.QDialog()
    ui = Ui_talentDialog()
    ui.setupUi(talentDialog)
    talentDialog.show()
    sys.exit(app.exec_())

