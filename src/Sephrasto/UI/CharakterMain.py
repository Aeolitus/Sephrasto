# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterMain.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_formMain(object):
    def setupUi(self, formMain):
        if not formMain.objectName():
            formMain.setObjectName(u"formMain")
        formMain.setWindowModality(Qt.ApplicationModal)
        formMain.resize(1129, 903)
        self.gridLayout = QGridLayout(formMain)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = QScrollArea(formMain)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1107, 844))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabs = QTabWidget(self.scrollAreaWidgetContents)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setDocumentMode(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabs.addTab(self.tab_2, "")

        self.horizontalLayout.addWidget(self.tabs)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(formMain)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.spinEP = QSpinBox(formMain)
        self.spinEP.setObjectName(u"spinEP")
        self.spinEP.setAlignment(Qt.AlignCenter)
        self.spinEP.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinEP.setMaximum(100000)

        self.horizontalLayout_2.addWidget(self.spinEP)

        self.label_3 = QLabel(formMain)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.spinSpent = QSpinBox(formMain)
        self.spinSpent.setObjectName(u"spinSpent")
        self.spinSpent.setFocusPolicy(Qt.NoFocus)
        self.spinSpent.setAlignment(Qt.AlignCenter)
        self.spinSpent.setReadOnly(True)
        self.spinSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinSpent.setMinimum(-100000)
        self.spinSpent.setMaximum(100000)

        self.horizontalLayout_2.addWidget(self.spinSpent)

        self.label_2 = QLabel(formMain)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.spinRemaining = QSpinBox(formMain)
        self.spinRemaining.setObjectName(u"spinRemaining")
        self.spinRemaining.setFocusPolicy(Qt.NoFocus)
        self.spinRemaining.setAutoFillBackground(False)
        self.spinRemaining.setAlignment(Qt.AlignCenter)
        self.spinRemaining.setReadOnly(True)
        self.spinRemaining.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinRemaining.setMinimum(-100000)
        self.spinRemaining.setMaximum(100000)

        self.horizontalLayout_2.addWidget(self.spinRemaining)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.buttonQuicksave = QPushButton(formMain)
        self.buttonQuicksave.setObjectName(u"buttonQuicksave")
        self.buttonQuicksave.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_2.addWidget(self.buttonQuicksave)

        self.buttonSave = QPushButton(formMain)
        self.buttonSave.setObjectName(u"buttonSave")
        self.buttonSave.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_2.addWidget(self.buttonSave)

        self.buttonSavePDF = QPushButton(formMain)
        self.buttonSavePDF.setObjectName(u"buttonSavePDF")
        self.buttonSavePDF.setMinimumSize(QSize(100, 0))
        self.buttonSavePDF.setMaximumSize(QSize(16777214, 16777215))

        self.horizontalLayout_2.addWidget(self.buttonSavePDF)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.tabs, self.spinEP)
        QWidget.setTabOrder(self.spinEP, self.spinSpent)
        QWidget.setTabOrder(self.spinSpent, self.spinRemaining)

        self.retranslateUi(formMain)

        self.tabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(formMain)
    # setupUi

    def retranslateUi(self, formMain):
        formMain.setWindowTitle(QCoreApplication.translate("formMain", u"Sephrasto - Charakter erstellen", None))
        self.tabs.setProperty("class", QCoreApplication.translate("formMain", u"h1", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), QCoreApplication.translate("formMain", u"Tab 1", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), QCoreApplication.translate("formMain", u"Tab 2", None))
        self.label.setText(QCoreApplication.translate("formMain", u"    Total:    ", None))
        self.label.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.spinEP.setSuffix(QCoreApplication.translate("formMain", u" EP", None))
        self.label_3.setText(QCoreApplication.translate("formMain", u"    Ausgegeben:    ", None))
        self.label_3.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.spinSpent.setSuffix(QCoreApplication.translate("formMain", u" EP", None))
        self.label_2.setText(QCoreApplication.translate("formMain", u"    Verbleibend:    ", None))
        self.label_2.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.spinRemaining.setSuffix(QCoreApplication.translate("formMain", u" EP", None))
        self.buttonQuicksave.setText(QCoreApplication.translate("formMain", u"Speichern", None))
        self.buttonSave.setText(QCoreApplication.translate("formMain", u"Speichern unter...", None))
        self.buttonSavePDF.setText(QCoreApplication.translate("formMain", u"PDF erstellen", None))
    # retranslateUi

