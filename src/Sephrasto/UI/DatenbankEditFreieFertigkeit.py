# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditFreieFertigkeit.ui'
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

class Ui_ffDialog(object):
    def setupUi(self, ffDialog):
        if not ffDialog.objectName():
            ffDialog.setObjectName(u"ffDialog")
        ffDialog.setWindowModality(Qt.ApplicationModal)
        ffDialog.resize(440, 204)
        self.gridLayout_2 = QGridLayout(ffDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(ffDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(ffDialog)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")

        self.gridLayout.addWidget(self.teVoraussetzungen, 3, 1, 1, 1)

        self.warning = QLabel(ffDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.leName = QLineEdit(ffDialog)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 1)

        self.label = QLabel(ffDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(ffDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.comboTyp = QComboBox(ffDialog)
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 2, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ffDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.teVoraussetzungen)

        self.retranslateUi(ffDialog)
        self.buttonBox.accepted.connect(ffDialog.accept)
        self.buttonBox.rejected.connect(ffDialog.reject)

        QMetaObject.connectSlotsByName(ffDialog)
    # setupUi

    def retranslateUi(self, ffDialog):
        ffDialog.setWindowTitle(QCoreApplication.translate("ffDialog", u"Sephrasto - Freie Fertigkeit bearbeiten...", None))
        self.label_4.setText(QCoreApplication.translate("ffDialog", u"Voraussetzungen", None))
        self.warning.setText(QCoreApplication.translate("ffDialog", u"<html><head/><body><p>Dies ist eine Ilaris Standard-Freie-Fertigkeit. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr diese Freie Fertigkeit keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("ffDialog", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("ffDialog", u"Typ", None))
    # retranslateUi

