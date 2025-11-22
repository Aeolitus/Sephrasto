# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterFreieFert.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1101, 699)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1099, 697))
        self.horizontalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.groupBox.setFlat(False)
        self.freieFertsGrid = QGridLayout(self.groupBox)
        self.freieFertsGrid.setObjectName(u"freieFertsGrid")
        self.freieFertsGrid.setContentsMargins(20, 20, 20, 20)

        self.verticalLayout.addWidget(self.groupBox)

        self.labelInfo = QLabel(self.scrollAreaWidgetContents)
        self.labelInfo.setObjectName(u"labelInfo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfo.sizePolicy().hasHeightForWidth())
        self.labelInfo.setSizePolicy(sizePolicy)
        self.labelInfo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelInfo.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelInfo)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.scrollArea.setProperty(u"class", QCoreApplication.translate("Form", u"transparent", None))
        self.groupBox.setTitle("")
        self.labelInfo.setText(QCoreApplication.translate("Form", u"Freie Fertigkeiten sind in drei Stufen geteilt: Unerfahren (I), erfahren (II) und meisterlich (III). Sie entsprechen jeweils einem PW von 6/14/22 und kosten 4/8/16 EP.\n"
"\n"
"Der erste Eintrag ist die Muttersprache des Charakters.\n"
"Jeder Charakter beherrscht seine Muttersprache meisterlich, ohne daf\u00fcr zu bezahlen.", None))
    # retranslateUi

