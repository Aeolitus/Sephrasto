# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditEinstellung.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QDoubleSpinBox, QGridLayout, QLabel,
    QPlainTextEdit, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_deDialog(object):
    def setupUi(self, deDialog):
        if not deDialog.objectName():
            deDialog.setObjectName(u"deDialog")
        deDialog.setWindowModality(Qt.ApplicationModal)
        deDialog.resize(440, 275)
        self.gridLayout_2 = QGridLayout(deDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(deDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(deDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label = QLabel(deDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkWert = QCheckBox(deDialog)
        self.checkWert.setObjectName(u"checkWert")

        self.verticalLayout.addWidget(self.checkWert)

        self.spinWert = QSpinBox(deDialog)
        self.spinWert.setObjectName(u"spinWert")

        self.verticalLayout.addWidget(self.spinWert)

        self.dspinWert = QDoubleSpinBox(deDialog)
        self.dspinWert.setObjectName(u"dspinWert")

        self.verticalLayout.addWidget(self.dspinWert)

        self.teWert = QPlainTextEdit(deDialog)
        self.teWert.setObjectName(u"teWert")

        self.verticalLayout.addWidget(self.teWert)


        self.gridLayout.addLayout(self.verticalLayout, 3, 1, 1, 1)

        self.warning = QLabel(deDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.label_2 = QLabel(deDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.labelBeschreibung = QLabel(deDialog)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")
        self.labelBeschreibung.setWordWrap(True)

        self.gridLayout.addWidget(self.labelBeschreibung, 2, 1, 1, 1)

        self.labelName = QLabel(deDialog)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.retranslateUi(deDialog)
        self.buttonBox.accepted.connect(deDialog.accept)
        self.buttonBox.rejected.connect(deDialog.reject)

        QMetaObject.connectSlotsByName(deDialog)
    # setupUi

    def retranslateUi(self, deDialog):
        deDialog.setWindowTitle(QCoreApplication.translate("deDialog", u"Sephrasto - Einstellung bearbeiten...", None))
        self.label_4.setText(QCoreApplication.translate("deDialog", u"Wert", None))
        self.label.setText(QCoreApplication.translate("deDialog", u"Name", None))
        self.checkWert.setText("")
        self.warning.setText(QCoreApplication.translate("deDialog", u"<html><head/><body><p>Dies ist eine Ilaris Standard-Einstellung. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr diese Einstellung keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("deDialog", u"Beschreibung", None))
        self.labelBeschreibung.setText("")
        self.labelName.setText("")
    # retranslateUi

