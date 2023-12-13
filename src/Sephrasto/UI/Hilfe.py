# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Hilfe.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLayout,
    QSizePolicy, QSpacerItem, QTextBrowser, QToolButton,
    QWidget)

class Ui_formHilfe(object):
    def setupUi(self, formHilfe):
        if not formHilfe.objectName():
            formHilfe.setObjectName(u"formHilfe")
        formHilfe.setWindowModality(Qt.NonModal)
        formHilfe.resize(872, 460)
        self.gridLayout_3 = QGridLayout(formHilfe)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.buttonBackward = QToolButton(formHilfe)
        self.buttonBackward.setObjectName(u"buttonBackward")

        self.horizontalLayout.addWidget(self.buttonBackward)

        self.buttonForward = QToolButton(formHilfe)
        self.buttonForward.setObjectName(u"buttonForward")

        self.horizontalLayout.addWidget(self.buttonForward)

        self.buttonHome = QToolButton(formHilfe)
        self.buttonHome.setObjectName(u"buttonHome")

        self.horizontalLayout.addWidget(self.buttonHome)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.teHelp = QTextBrowser(formHilfe)
        self.teHelp.setObjectName(u"teHelp")
        self.teHelp.setOpenExternalLinks(True)

        self.gridLayout_3.addWidget(self.teHelp, 1, 0, 1, 2)

        QWidget.setTabOrder(self.buttonBackward, self.buttonForward)
        QWidget.setTabOrder(self.buttonForward, self.buttonHome)
        QWidget.setTabOrder(self.buttonHome, self.teHelp)

        self.retranslateUi(formHilfe)

        QMetaObject.connectSlotsByName(formHilfe)
    # setupUi

    def retranslateUi(self, formHilfe):
        formHilfe.setWindowTitle(QCoreApplication.translate("formHilfe", u"Sephrasto - Hilfe", None))
        self.buttonBackward.setText(QCoreApplication.translate("formHilfe", u"...", None))
        self.buttonBackward.setProperty("class", QCoreApplication.translate("formHilfe", u"icon", None))
        self.buttonForward.setText(QCoreApplication.translate("formHilfe", u"...", None))
        self.buttonForward.setProperty("class", QCoreApplication.translate("formHilfe", u"icon", None))
        self.buttonHome.setText(QCoreApplication.translate("formHilfe", u"...", None))
        self.buttonHome.setProperty("class", QCoreApplication.translate("formHilfe", u"icon", None))
    # retranslateUi

