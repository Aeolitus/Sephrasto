# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditManoever.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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

class Ui_manDialog(object):
    def setupUi(self, manDialog):
        if not manDialog.objectName():
            manDialog.setObjectName(u"manDialog")
        manDialog.setWindowModality(Qt.ApplicationModal)
        manDialog.resize(440, 550)
        self.gridLayout_2 = QGridLayout(manDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.textEdit = QPlainTextEdit(manDialog)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.textEdit, 6, 1, 1, 1)

        self.label_3 = QLabel(manDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.voraussetzungenEdit = QPlainTextEdit(manDialog)
        self.voraussetzungenEdit.setObjectName(u"voraussetzungenEdit")

        self.gridLayout.addWidget(self.voraussetzungenEdit, 5, 1, 1, 1)

        self.label_4 = QLabel(manDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.label_5 = QLabel(manDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.nameEdit = QLineEdit(manDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.label = QLabel(manDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(manDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.probeEdit = QLineEdit(manDialog)
        self.probeEdit.setObjectName(u"probeEdit")

        self.gridLayout.addWidget(self.probeEdit, 2, 1, 1, 1)

        self.comboTyp = QComboBox(manDialog)
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

        self.gridLayout.addWidget(self.comboTyp, 4, 1, 1, 1)

        self.label_6 = QLabel(manDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.gegenEdit = QLineEdit(manDialog)
        self.gegenEdit.setObjectName(u"gegenEdit")

        self.gridLayout.addWidget(self.gegenEdit, 3, 1, 1, 1)

        self.warning = QLabel(manDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(manDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.nameEdit, self.probeEdit)
        QWidget.setTabOrder(self.probeEdit, self.gegenEdit)
        QWidget.setTabOrder(self.gegenEdit, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.voraussetzungenEdit)
        QWidget.setTabOrder(self.voraussetzungenEdit, self.textEdit)

        self.retranslateUi(manDialog)
        self.buttonBox.accepted.connect(manDialog.accept)
        self.buttonBox.rejected.connect(manDialog.reject)

        QMetaObject.connectSlotsByName(manDialog)
    # setupUi

    def retranslateUi(self, manDialog):
        manDialog.setWindowTitle(QCoreApplication.translate("manDialog", u"Sephrasto - Man\u00f6ver / Modifikation bearbeiten...", None))
        self.label_3.setText(QCoreApplication.translate("manDialog", u"Gegenprobe", None))
        self.label_4.setText(QCoreApplication.translate("manDialog", u"Voraussetzungen", None))
        self.label_5.setText(QCoreApplication.translate("manDialog", u"Beschreibung", None))
        self.label.setText(QCoreApplication.translate("manDialog", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("manDialog", u"Probe", None))
        self.comboTyp.setItemText(0, QCoreApplication.translate("manDialog", u"Nahkampfman\u00f6ver", None))
        self.comboTyp.setItemText(1, QCoreApplication.translate("manDialog", u"Fernkampfman\u00f6ver", None))
        self.comboTyp.setItemText(2, QCoreApplication.translate("manDialog", u"Magische Modifikation", None))
        self.comboTyp.setItemText(3, QCoreApplication.translate("manDialog", u"Karmale Modifikation", None))
        self.comboTyp.setItemText(4, QCoreApplication.translate("manDialog", u"Weitere Magieregeln", None))
        self.comboTyp.setItemText(5, QCoreApplication.translate("manDialog", u"Aktion", None))
        self.comboTyp.setItemText(6, QCoreApplication.translate("manDialog", u"D\u00e4monische Modifikation", None))
        self.comboTyp.setItemText(7, QCoreApplication.translate("manDialog", u"Weitere Karmaregeln", None))
        self.comboTyp.setItemText(8, QCoreApplication.translate("manDialog", u"Weitere Kampfregeln", None))
        self.comboTyp.setItemText(9, QCoreApplication.translate("manDialog", u"Profane Regeln", None))

        self.label_6.setText(QCoreApplication.translate("manDialog", u"Typ", None))
        self.warning.setText(QCoreApplication.translate("manDialog", u"<html><head/><body><p>Dies ist ein Ilaris-Standardman\u00f6ver / eine Ilaris-Standardmodifikation. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr dieses Man\u00f6ver / diese Modifikation keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
    # retranslateUi

