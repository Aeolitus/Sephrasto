# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditEinstellung.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout,
    QLabel, QPlainTextEdit, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(572, 411)
        self.verticalLayout_2 = QVBoxLayout(dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 552, 391))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelLabelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelLabelBeschreibung.setObjectName(u"labelLabelBeschreibung")

        self.gridLayout.addWidget(self.labelLabelBeschreibung, 3, 1, 1, 1)

        self.labelName_2 = QLabel(self.scrollAreaWidgetContents)
        self.labelName_2.setObjectName(u"labelName_2")

        self.gridLayout.addWidget(self.labelName_2, 2, 1, 1, 1)

        self.labelWert = QLabel(self.scrollAreaWidgetContents)
        self.labelWert.setObjectName(u"labelWert")
        self.labelWert.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelWert, 4, 1, 1, 1)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")
        self.labelBeschreibung.setWordWrap(True)

        self.gridLayout.addWidget(self.labelBeschreibung, 3, 2, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 2, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkText = QCheckBox(self.scrollAreaWidgetContents)
        self.checkText.setObjectName(u"checkText")

        self.verticalLayout.addWidget(self.checkText)

        self.spinText = QSpinBox(self.scrollAreaWidgetContents)
        self.spinText.setObjectName(u"spinText")
        self.spinText.setMinimum(-99999)
        self.spinText.setMaximum(99999)

        self.verticalLayout.addWidget(self.spinText)

        self.dspinText = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.dspinText.setObjectName(u"dspinText")
        self.dspinText.setMinimum(-99999.000000000000000)
        self.dspinText.setMaximum(99999.000000000000000)

        self.verticalLayout.addWidget(self.dspinText)

        self.teText = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teText.setObjectName(u"teText")

        self.verticalLayout.addWidget(self.teText)

        self.horizontalSpacer = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 4, 2, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Einstellung bearbeiten...", None))
        self.labelLabelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.labelName_2.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelWert.setText(QCoreApplication.translate("dialog", u"Wert", None))
        self.labelBeschreibung.setText("")
        self.labelName.setText("")
        self.checkText.setText("")
    # retranslateUi

