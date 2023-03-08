# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRegel.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QPlainTextEdit, QSizePolicy, QWidget)

class Ui_regelDialog(object):
    def setupUi(self, regelDialog):
        if not regelDialog.objectName():
            regelDialog.setObjectName(u"regelDialog")
        regelDialog.setWindowModality(Qt.ApplicationModal)
        regelDialog.resize(440, 550)
        self.gridLayout_2 = QGridLayout(regelDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_5 = QLabel(regelDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.label_6 = QLabel(regelDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.probeEdit = QLineEdit(regelDialog)
        self.probeEdit.setObjectName(u"probeEdit")

        self.gridLayout.addWidget(self.probeEdit, 2, 1, 1, 1)

        self.nameEdit = QLineEdit(regelDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.warning = QLabel(regelDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.comboTyp = QComboBox(regelDialog)
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 3, 1, 1, 1)

        self.voraussetzungenEdit = QPlainTextEdit(regelDialog)
        self.voraussetzungenEdit.setObjectName(u"voraussetzungenEdit")

        self.gridLayout.addWidget(self.voraussetzungenEdit, 4, 1, 1, 1)

        self.label_4 = QLabel(regelDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_2 = QLabel(regelDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.textEdit = QPlainTextEdit(regelDialog)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.textEdit, 5, 1, 1, 1)

        self.label = QLabel(regelDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(regelDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.nameEdit, self.probeEdit)
        QWidget.setTabOrder(self.probeEdit, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.voraussetzungenEdit)
        QWidget.setTabOrder(self.voraussetzungenEdit, self.textEdit)

        self.retranslateUi(regelDialog)
        self.buttonBox.accepted.connect(regelDialog.accept)
        self.buttonBox.rejected.connect(regelDialog.reject)

        QMetaObject.connectSlotsByName(regelDialog)
    # setupUi

    def retranslateUi(self, regelDialog):
        regelDialog.setWindowTitle(QCoreApplication.translate("regelDialog", u"Sephrasto - Man\u00f6ver / Modifikation bearbeiten...", None))
        self.label_5.setText(QCoreApplication.translate("regelDialog", u"Beschreibung", None))
        self.label_6.setText(QCoreApplication.translate("regelDialog", u"Typ", None))
        self.warning.setText(QCoreApplication.translate("regelDialog", u"<html><head/><body><p>Dies ist ein Ilaris-Standardman\u00f6ver / eine Ilaris-Standardmodifikation. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr dieses Man\u00f6ver / diese Modifikation keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.comboTyp.setItemText(0, QCoreApplication.translate("regelDialog", u"Nahkampfman\u00f6ver", None))
        self.comboTyp.setItemText(1, QCoreApplication.translate("regelDialog", u"Fernkampfman\u00f6ver", None))
        self.comboTyp.setItemText(2, QCoreApplication.translate("regelDialog", u"Magische Modifikation", None))
        self.comboTyp.setItemText(3, QCoreApplication.translate("regelDialog", u"Karmale Modifikation", None))
        self.comboTyp.setItemText(4, QCoreApplication.translate("regelDialog", u"Weitere Magieregeln", None))
        self.comboTyp.setItemText(5, QCoreApplication.translate("regelDialog", u"Aktion", None))
        self.comboTyp.setItemText(6, QCoreApplication.translate("regelDialog", u"D\u00e4monische Modifikation", None))
        self.comboTyp.setItemText(7, QCoreApplication.translate("regelDialog", u"Weitere Karmaregeln", None))
        self.comboTyp.setItemText(8, QCoreApplication.translate("regelDialog", u"Weitere Kampfregeln", None))
        self.comboTyp.setItemText(9, QCoreApplication.translate("regelDialog", u"Profane Regeln", None))

        self.label_4.setText(QCoreApplication.translate("regelDialog", u"Voraussetzungen", None))
        self.label_2.setText(QCoreApplication.translate("regelDialog", u"Probe", None))
        self.label.setText(QCoreApplication.translate("regelDialog", u"Name", None))
    # retranslateUi

