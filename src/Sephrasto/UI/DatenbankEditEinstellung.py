# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditEinstellung.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
    QPlainTextEdit, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(572, 415)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 552, 310))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")
        self.labelBeschreibung.setWordWrap(True)

        self.gridLayout.addWidget(self.labelBeschreibung, 4, 2, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 3, 2, 1, 1)

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


        self.gridLayout.addLayout(self.verticalLayout, 5, 2, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 5, 1, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)

        self.warning = QLabel(self.scrollAreaWidgetContents)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(True)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 1, 1, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Einstellung bearbeiten...", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.labelBeschreibung.setText("")
        self.labelName.setText("")
        self.checkText.setText("")
        self.label_4.setText(QCoreApplication.translate("dialog", u"Wert", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.warning.setText("")
    # retranslateUi

