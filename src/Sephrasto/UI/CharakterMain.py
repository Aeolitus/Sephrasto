# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterMain.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QWidget)

class Ui_formMain(object):
    def setupUi(self, formMain):
        if not formMain.objectName():
            formMain.setObjectName(u"formMain")
        formMain.setWindowModality(Qt.WindowModality.ApplicationModal)
        formMain.resize(1129, 903)
        self.gridLayout = QGridLayout(formMain)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabs = QTabWidget(formMain)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setElideMode(Qt.TextElideMode.ElideRight)
        self.tabs.setDocumentMode(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabs.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabs, 0, 0, 1, 1)

        self.layoutBottomBar = QHBoxLayout()
        self.layoutBottomBar.setObjectName(u"layoutBottomBar")
        self.label = QLabel(formMain)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.layoutBottomBar.addWidget(self.label)

        self.spinEP = QSpinBox(formMain)
        self.spinEP.setObjectName(u"spinEP")
        self.spinEP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinEP.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.spinEP.setMaximum(100000)

        self.layoutBottomBar.addWidget(self.spinEP)

        self.label_3 = QLabel(formMain)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.layoutBottomBar.addWidget(self.label_3)

        self.spinSpent = QSpinBox(formMain)
        self.spinSpent.setObjectName(u"spinSpent")
        self.spinSpent.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.spinSpent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinSpent.setReadOnly(True)
        self.spinSpent.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinSpent.setMinimum(-100000)
        self.spinSpent.setMaximum(100000)

        self.layoutBottomBar.addWidget(self.spinSpent)

        self.label_2 = QLabel(formMain)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.layoutBottomBar.addWidget(self.label_2)

        self.spinRemaining = QSpinBox(formMain)
        self.spinRemaining.setObjectName(u"spinRemaining")
        self.spinRemaining.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.spinRemaining.setAutoFillBackground(False)
        self.spinRemaining.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinRemaining.setReadOnly(True)
        self.spinRemaining.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinRemaining.setMinimum(-100000)
        self.spinRemaining.setMaximum(100000)

        self.layoutBottomBar.addWidget(self.spinRemaining)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutBottomBar.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.layoutBottomBar, 1, 0, 1, 1)

        QWidget.setTabOrder(self.spinEP, self.spinSpent)
        QWidget.setTabOrder(self.spinSpent, self.spinRemaining)

        self.retranslateUi(formMain)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(formMain)
    # setupUi

    def retranslateUi(self, formMain):
        formMain.setWindowTitle(QCoreApplication.translate("formMain", u"Sephrasto - Charakter erstellen", None))
        self.tabs.setProperty(u"class", QCoreApplication.translate("formMain", u"tabNavigation", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), QCoreApplication.translate("formMain", u"Tab 1", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), QCoreApplication.translate("formMain", u"Tab 2", None))
        self.label.setText(QCoreApplication.translate("formMain", u"    Total:    ", None))
        self.label.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.spinEP.setSuffix(QCoreApplication.translate("formMain", u" EP", None))
        self.label_3.setText(QCoreApplication.translate("formMain", u"    Ausgegeben:    ", None))
        self.label_3.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.spinSpent.setSuffix(QCoreApplication.translate("formMain", u" EP", None))
        self.label_2.setText(QCoreApplication.translate("formMain", u"    Verbleibend:    ", None))
        self.label_2.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.spinRemaining.setSuffix(QCoreApplication.translate("formMain", u" EP", None))
    # retranslateUi

