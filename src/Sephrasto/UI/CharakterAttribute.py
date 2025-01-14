# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterAttribute.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_formAttribute(object):
    def setupUi(self, formAttribute):
        if not formAttribute.objectName():
            formAttribute.setObjectName(u"formAttribute")
        formAttribute.resize(936, 460)
        self.gridLayout_2 = QGridLayout(formAttribute)
        self.gridLayout_2.setSpacing(20)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_18 = QLabel(formAttribute)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_2.addWidget(self.label_18)

        self.gbAbgeleiteteWerte = QGroupBox(formAttribute)
        self.gbAbgeleiteteWerte.setObjectName(u"gbAbgeleiteteWerte")
        self.gridLayout_4 = QGridLayout(self.gbAbgeleiteteWerte)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(10)
        self.gridLayout_4.setContentsMargins(20, 20, 20, 20)
        self.label_9 = QLabel(self.gbAbgeleiteteWerte)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_8 = QLabel(self.gbAbgeleiteteWerte)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 0, 1, 1, 1)

        self.label_4 = QLabel(self.gbAbgeleiteteWerte)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 0, 2, 1, 1)

        self.label_5 = QLabel(self.gbAbgeleiteteWerte)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 0, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.gbAbgeleiteteWerte)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_16 = QLabel(formAttribute)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout.addWidget(self.label_16)

        self.gbAttribute = QGroupBox(formAttribute)
        self.gbAttribute.setObjectName(u"gbAttribute")
        self.gridLayout_3 = QGridLayout(self.gbAttribute)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(10)
        self.gridLayout_3.setContentsMargins(20, 20, 20, 20)
        self.label = QLabel(self.gbAttribute)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 2, 1, 1)

        self.label_3 = QLabel(self.gbAttribute)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 4, 1, 1)

        self.label_6 = QLabel(self.gbAttribute)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 1, 1, 1)

        self.label_7 = QLabel(self.gbAttribute)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_2 = QLabel(self.gbAttribute)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_2, 0, 3, 1, 1)


        self.verticalLayout.addWidget(self.gbAttribute)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)


        self.gridLayout_2.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 5, 1, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.labelEnergien = QLabel(formAttribute)
        self.labelEnergien.setObjectName(u"labelEnergien")

        self.verticalLayout_3.addWidget(self.labelEnergien)

        self.gbEnergien = QGroupBox(formAttribute)
        self.gbEnergien.setObjectName(u"gbEnergien")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbEnergien.sizePolicy().hasHeightForWidth())
        self.gbEnergien.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.gbEnergien)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.label_10 = QLabel(self.gbEnergien)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_15 = QLabel(self.gbEnergien)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_15, 0, 5, 1, 1)

        self.label_12 = QLabel(self.gbEnergien)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_12, 0, 2, 1, 1)

        self.label_11 = QLabel(self.gbEnergien)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 0, 1, 1, 1)

        self.label_13 = QLabel(self.gbEnergien)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_13, 0, 3, 1, 1)

        self.label_14 = QLabel(self.gbEnergien)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 0, 4, 1, 1)

        self.label_17 = QLabel(self.gbEnergien)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 0, 6, 1, 1)


        self.verticalLayout_3.addWidget(self.gbEnergien)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 3, 1, 1, 2)


        self.retranslateUi(formAttribute)

        QMetaObject.connectSlotsByName(formAttribute)
    # setupUi

    def retranslateUi(self, formAttribute):
        formAttribute.setWindowTitle(QCoreApplication.translate("formAttribute", u"Attribute", None))
        self.label_18.setText(QCoreApplication.translate("formAttribute", u"Abgeleitete Werte", None))
        self.label_18.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.gbAbgeleiteteWerte.setTitle("")
        self.label_9.setText("")
        self.label_8.setText("")
        self.label_4.setText(QCoreApplication.translate("formAttribute", u"Wert", None))
        self.label_4.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_5.setText(QCoreApplication.translate("formAttribute", u"Formel", None))
        self.label_5.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_16.setText(QCoreApplication.translate("formAttribute", u"Attribute", None))
        self.label_16.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.gbAttribute.setTitle("")
        self.label.setText(QCoreApplication.translate("formAttribute", u"Wert", None))
        self.label.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_3.setText(QCoreApplication.translate("formAttribute", u"Kosten", None))
        self.label_3.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_6.setText("")
        self.label_7.setText("")
        self.label_2.setText(QCoreApplication.translate("formAttribute", u"PW", None))
        self.label_2.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.labelEnergien.setText(QCoreApplication.translate("formAttribute", u"Energien", None))
        self.labelEnergien.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.gbEnergien.setTitle("")
        self.label_10.setText("")
        self.label_15.setText(QCoreApplication.translate("formAttribute", u"Gebunden", None))
        self.label_15.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_12.setText(QCoreApplication.translate("formAttribute", u"Wert", None))
        self.label_12.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_11.setText("")
        self.label_13.setText(QCoreApplication.translate("formAttribute", u"Zukauf", None))
        self.label_13.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_14.setText(QCoreApplication.translate("formAttribute", u"Kosten", None))
        self.label_14.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_17.setText(QCoreApplication.translate("formAttribute", u"Gesamt", None))
        self.label_17.setProperty(u"class", QCoreApplication.translate("formAttribute", u"h2", None))
    # retranslateUi

