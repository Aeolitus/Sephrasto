# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterFreieFert.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(872, 460)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(20, 20, 20, 20)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(20)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 18))
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.freieFertsGrid = QGridLayout(self.groupBox)
        self.freieFertsGrid.setObjectName(u"freieFertsGrid")
        self.freieFertsGrid.setContentsMargins(20, 20, 20, 20)

        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)

        self.labelRegeln = QLabel(Form)
        self.labelRegeln.setObjectName(u"labelRegeln")
        self.labelRegeln.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelRegeln, 3, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Der erste Eintrag ist die Muttersprache des Charakters.\n"
"Jeder Charakter beherrscht seine Muttersprache meisterlich, ohne daf\u00fcr zu bezahlen.", None))
        self.groupBox.setTitle("")
        self.labelRegeln.setText(QCoreApplication.translate("Form", u"Freie Fertigkeiten sind in drei Stufen geteilt: Unerfahren (I), erfahren (II) und meisterlich (III).", None))
    # retranslateUi

