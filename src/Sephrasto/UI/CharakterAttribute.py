# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterAttribute.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_formAttribute(object):
    def setupUi(self, formAttribute):
        if not formAttribute.objectName():
            formAttribute.setObjectName(u"formAttribute")
        formAttribute.resize(936, 460)
        self.gridLayout_2 = QGridLayout(formAttribute)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelPlaceholderFullName = QLabel(formAttribute)
        self.labelPlaceholderFullName.setObjectName(u"labelPlaceholderFullName")

        self.gridLayout.addWidget(self.labelPlaceholderFullName, 0, 0, 1, 1)

        self.label_2 = QLabel(formAttribute)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 7, 1, 1)

        self.labelPlaceholderFullName_2 = QLabel(formAttribute)
        self.labelPlaceholderFullName_2.setObjectName(u"labelPlaceholderFullName_2")

        self.gridLayout.addWidget(self.labelPlaceholderFullName_2, 0, 6, 1, 1)

        self.labelPW = QLabel(formAttribute)
        self.labelPW.setObjectName(u"labelPW")
        self.labelPW.setMinimumSize(QSize(60, 0))
        font = QFont()
        font.setBold(True)
        self.labelPW.setFont(font)
        self.labelPW.setAlignment(Qt.AlignCenter)
        self.labelPW.setMargin(0)

        self.gridLayout.addWidget(self.labelPW, 0, 3, 1, 1)

        self.labelFormel = QLabel(formAttribute)
        self.labelFormel.setObjectName(u"labelFormel")
        self.labelFormel.setMinimumSize(QSize(60, 0))
        self.labelFormel.setFont(font)
        self.labelFormel.setMargin(0)

        self.gridLayout.addWidget(self.labelFormel, 0, 10, 1, 1)

        self.labelPlaceholderPlus = QLabel(formAttribute)
        self.labelPlaceholderPlus.setObjectName(u"labelPlaceholderPlus")

        self.gridLayout.addWidget(self.labelPlaceholderPlus, 0, 9, 1, 1)

        self.labelPlaceholderName = QLabel(formAttribute)
        self.labelPlaceholderName.setObjectName(u"labelPlaceholderName")

        self.gridLayout.addWidget(self.labelPlaceholderName, 0, 1, 1, 1)

        self.labelKosten = QLabel(formAttribute)
        self.labelKosten.setObjectName(u"labelKosten")
        self.labelKosten.setMinimumSize(QSize(60, 0))
        self.labelKosten.setFont(font)
        self.labelKosten.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKosten, 0, 4, 1, 1)

        self.labelWert2 = QLabel(formAttribute)
        self.labelWert2.setObjectName(u"labelWert2")
        self.labelWert2.setMinimumSize(QSize(60, 0))
        self.labelWert2.setFont(font)
        self.labelWert2.setAlignment(Qt.AlignCenter)
        self.labelWert2.setMargin(0)

        self.gridLayout.addWidget(self.labelWert2, 0, 8, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(70, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 5, 1, 1)

        self.labelWert = QLabel(formAttribute)
        self.labelWert.setObjectName(u"labelWert")
        self.labelWert.setMinimumSize(QSize(60, 0))
        self.labelWert.setFont(font)
        self.labelWert.setAlignment(Qt.AlignCenter)
        self.labelWert.setMargin(0)

        self.gridLayout.addWidget(self.labelWert, 0, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 4, 1, 1, 1)


        self.retranslateUi(formAttribute)

        QMetaObject.connectSlotsByName(formAttribute)
    # setupUi

    def retranslateUi(self, formAttribute):
        formAttribute.setWindowTitle(QCoreApplication.translate("formAttribute", u"Attribute", None))
        self.labelPlaceholderFullName.setText("")
        self.label_2.setText("")
        self.labelPlaceholderFullName_2.setText("")
#if QT_CONFIG(tooltip)
        self.labelPW.setToolTip(QCoreApplication.translate("formAttribute", u"Probenwert", None))
#endif // QT_CONFIG(tooltip)
        self.labelPW.setText(QCoreApplication.translate("formAttribute", u"PW", None))
        self.labelPW.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.labelFormel.setText(QCoreApplication.translate("formAttribute", u"Formel", None))
        self.labelFormel.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.labelPlaceholderPlus.setText("")
        self.labelPlaceholderName.setText("")
        self.labelKosten.setText(QCoreApplication.translate("formAttribute", u"Kosten", None))
        self.labelKosten.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.labelWert2.setText(QCoreApplication.translate("formAttribute", u"Wert", None))
        self.labelWert2.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.labelWert.setText(QCoreApplication.translate("formAttribute", u"Wert", None))
        self.labelWert.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
    # retranslateUi

