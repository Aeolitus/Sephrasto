# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(384, 527)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonRules = QPushButton(Form)
        self.buttonRules.setObjectName(u"buttonRules")

        self.horizontalLayout.addWidget(self.buttonRules)

        self.buttonHelp = QPushButton(Form)
        self.buttonHelp.setObjectName(u"buttonHelp")

        self.horizontalLayout.addWidget(self.buttonHelp)

        self.buttonSettings = QPushButton(Form)
        self.buttonSettings.setObjectName(u"buttonSettings")

        self.horizontalLayout.addWidget(self.buttonSettings)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.horizontalSpacer_2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 50))
        self.label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(True)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setMaximumSize(QSize(16777215, 30))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.recents = QWidget()
        self.recents.setObjectName(u"recents")
        self.recents.setGeometry(QRect(0, 0, 114, 215))
        self.verticalLayout = QVBoxLayout(self.recents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.scrollArea.setWidget(self.recents)

        self.horizontalLayout_2.addWidget(self.scrollArea)

        self.horizontalSpacer_5 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_5 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.labelVersion = QLabel(Form)
        self.labelVersion.setObjectName(u"labelVersion")
        font1 = QFont()
        font1.setPointSize(7)
        font1.setItalic(True)
        self.labelVersion.setFont(font1)
        self.labelVersion.setAlignment(Qt.AlignBottom|Qt.AlignRight|Qt.AlignTrailing)

        self.verticalLayout_2.addWidget(self.labelVersion)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Sephrasto", None))
#if QT_CONFIG(tooltip)
        self.buttonRules.setToolTip(QCoreApplication.translate("Form", u"Regelbasis bearbeiten", None))
#endif // QT_CONFIG(tooltip)
        self.buttonRules.setText(QCoreApplication.translate("Form", u"Regelbasis bearbeiten", None))
        self.buttonRules.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonHelp.setToolTip(QCoreApplication.translate("Form", u"Hilfe", None))
#endif // QT_CONFIG(tooltip)
        self.buttonHelp.setText(QCoreApplication.translate("Form", u"Hilfe", None))
        self.buttonHelp.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonSettings.setToolTip(QCoreApplication.translate("Form", u"Einstellungen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonSettings.setText(QCoreApplication.translate("Form", u"Einst", None))
        self.buttonSettings.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
        self.label.setText(QCoreApplication.translate("Form", u"Sephrasto", None))
        self.label.setProperty("class", QCoreApplication.translate("Form", u"title", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Der Charaktergenerator f\u00fcr Ilaris", None))
        self.label_2.setProperty("class", QCoreApplication.translate("Form", u"subtitle", None))
        self.scrollArea.setProperty("class", QCoreApplication.translate("Form", u"charListScrollArea", None))
        self.recents.setProperty("class", QCoreApplication.translate("Form", u"recentCharsScrollArea", None))
        self.labelVersion.setText(QCoreApplication.translate("Form", u"PLACEHOLDER", None))
        self.labelVersion.setProperty("class", QCoreApplication.translate("Form", u"smallTextBright", None))
    # retranslateUi

