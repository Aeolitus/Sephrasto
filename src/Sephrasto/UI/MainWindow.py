# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(286, 346)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonNew = QPushButton(Form)
        self.buttonNew.setObjectName(u"buttonNew")

        self.gridLayout.addWidget(self.buttonNew, 7, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 19, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_6, 5, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.buttonEdit = QPushButton(Form)
        self.buttonEdit.setObjectName(u"buttonEdit")

        self.gridLayout.addWidget(self.buttonEdit, 8, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonHelp = QPushButton(Form)
        self.buttonHelp.setObjectName(u"buttonHelp")
        self.buttonHelp.setMinimumSize(QSize(28, 28))
        self.buttonHelp.setMaximumSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.buttonHelp)

        self.buttonSettings = QPushButton(Form)
        self.buttonSettings.setObjectName(u"buttonSettings")
        self.buttonSettings.setMinimumSize(QSize(28, 28))
        self.buttonSettings.setMaximumSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.buttonSettings)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(True)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.vlPluginButtons = QVBoxLayout()
        self.vlPluginButtons.setObjectName(u"vlPluginButtons")

        self.gridLayout.addLayout(self.vlPluginButtons, 15, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_5, 13, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.labelVersion = QLabel(Form)
        self.labelVersion.setObjectName(u"labelVersion")
        font1 = QFont()
        font1.setPointSize(7)
        font1.setItalic(True)
        self.labelVersion.setFont(font1)
        self.labelVersion.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelVersion, 24, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 10, 0, 1, 1)

        self.buttonRules = QPushButton(Form)
        self.buttonRules.setObjectName(u"buttonRules")

        self.gridLayout.addWidget(self.buttonRules, 9, 0, 1, 1)

        QWidget.setTabOrder(self.buttonNew, self.buttonEdit)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Sephrasto", None))
        self.buttonNew.setText(QCoreApplication.translate("Form", u"Neuen Charakter erstellen", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Ein Charaktergenerator f\u00fcr Ilaris", None))
        self.buttonEdit.setText(QCoreApplication.translate("Form", u"Charakter laden", None))
        self.buttonHelp.setText(QCoreApplication.translate("Form", u"Hilfe", None))
        self.buttonHelp.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
        self.buttonSettings.setText(QCoreApplication.translate("Form", u"Einst", None))
        self.buttonSettings.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
        self.label.setText(QCoreApplication.translate("Form", u"Sephrasto", None))
        self.label.setProperty("class", QCoreApplication.translate("Form", u"title", None))
        self.labelVersion.setText(QCoreApplication.translate("Form", u"PLACEHOLDER", None))
        self.labelVersion.setProperty("class", QCoreApplication.translate("Form", u"smallText", None))
        self.buttonRules.setText(QCoreApplication.translate("Form", u"Regelbasis bearbeiten", None))
    # retranslateUi

