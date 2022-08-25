# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterBeschreibung.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLayout, QLineEdit, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_formBeschreibung(object):
    def setupUi(self, formBeschreibung):
        if not formBeschreibung.objectName():
            formBeschreibung.setObjectName(u"formBeschreibung")
        formBeschreibung.resize(872, 460)
        self.gridLayout_3 = QGridLayout(formBeschreibung)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 3, 1, 1)

        self.label_4 = QLabel(formBeschreibung)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(120, 0))
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)

        self.gridLayout.addWidget(self.label_4, 6, 1, 1, 1)

        self.editKurzbeschreibung = QLineEdit(formBeschreibung)
        self.editKurzbeschreibung.setObjectName(u"editKurzbeschreibung")

        self.gridLayout.addWidget(self.editKurzbeschreibung, 6, 2, 1, 1)

        self.label_6 = QLabel(formBeschreibung)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.label_6, 7, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.label = QLabel(formBeschreibung)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)

        self.label_2 = QLabel(formBeschreibung)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)

        self.editName = QLineEdit(formBeschreibung)
        self.editName.setObjectName(u"editName")
        self.editName.setMinimumSize(QSize(600, 0))

        self.gridLayout.addWidget(self.editName, 1, 2, 1, 1)

        self.label_3 = QLabel(formBeschreibung)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)

        self.comboFinanzen = QComboBox(formBeschreibung)
        self.comboFinanzen.addItem("")
        self.comboFinanzen.addItem("")
        self.comboFinanzen.addItem("")
        self.comboFinanzen.addItem("")
        self.comboFinanzen.addItem("")
        self.comboFinanzen.setObjectName(u"comboFinanzen")
        self.comboFinanzen.setMaxVisibleItems(5)

        self.gridLayout.addWidget(self.comboFinanzen, 4, 2, 1, 1)

        self.comboStatus = QComboBox(formBeschreibung)
        self.comboStatus.addItem("")
        self.comboStatus.addItem("")
        self.comboStatus.addItem("")
        self.comboStatus.addItem("")
        self.comboStatus.addItem("")
        self.comboStatus.setObjectName(u"comboStatus")
        self.comboStatus.setMaxVisibleItems(5)
        self.comboStatus.setMinimumContentsLength(0)

        self.gridLayout.addWidget(self.comboStatus, 3, 2, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.editEig1 = QLineEdit(formBeschreibung)
        self.editEig1.setObjectName(u"editEig1")
        self.editEig1.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig1, 0, 0, 1, 1)

        self.editEig6 = QLineEdit(formBeschreibung)
        self.editEig6.setObjectName(u"editEig6")
        self.editEig6.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig6, 2, 1, 1, 1)

        self.editEig3 = QLineEdit(formBeschreibung)
        self.editEig3.setObjectName(u"editEig3")
        self.editEig3.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig3, 1, 0, 1, 1)

        self.editEig5 = QLineEdit(formBeschreibung)
        self.editEig5.setObjectName(u"editEig5")
        self.editEig5.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig5, 2, 0, 1, 1)

        self.editEig4 = QLineEdit(formBeschreibung)
        self.editEig4.setObjectName(u"editEig4")
        self.editEig4.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig4, 1, 1, 1, 1)

        self.editEig2 = QLineEdit(formBeschreibung)
        self.editEig2.setObjectName(u"editEig2")
        self.editEig2.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig2, 0, 1, 1, 1)

        self.editEig7 = QLineEdit(formBeschreibung)
        self.editEig7.setObjectName(u"editEig7")
        self.editEig7.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig7, 3, 0, 1, 1)

        self.editEig8 = QLineEdit(formBeschreibung)
        self.editEig8.setObjectName(u"editEig8")
        self.editEig8.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig8, 3, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 7, 2, 1, 1)

        self.editRasse = QLineEdit(formBeschreibung)
        self.editRasse.setObjectName(u"editRasse")

        self.gridLayout.addWidget(self.editRasse, 2, 2, 1, 1)

        self.labelFinanzen = QLabel(formBeschreibung)
        self.labelFinanzen.setObjectName(u"labelFinanzen")
        self.labelFinanzen.setFont(font)

        self.gridLayout.addWidget(self.labelFinanzen, 4, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 8, 1, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_7, 0, 1, 1, 1)

        self.label_7 = QLabel(formBeschreibung)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 5, 1, 1, 1)

        self.comboHeimat = QComboBox(formBeschreibung)
        self.comboHeimat.setObjectName(u"comboHeimat")

        self.gridLayout.addWidget(self.comboHeimat, 5, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.editName, self.editRasse)
        QWidget.setTabOrder(self.editRasse, self.comboStatus)
        QWidget.setTabOrder(self.comboStatus, self.comboFinanzen)
        QWidget.setTabOrder(self.comboFinanzen, self.comboHeimat)
        QWidget.setTabOrder(self.comboHeimat, self.editKurzbeschreibung)
        QWidget.setTabOrder(self.editKurzbeschreibung, self.editEig1)
        QWidget.setTabOrder(self.editEig1, self.editEig3)
        QWidget.setTabOrder(self.editEig3, self.editEig5)
        QWidget.setTabOrder(self.editEig5, self.editEig7)
        QWidget.setTabOrder(self.editEig7, self.editEig2)
        QWidget.setTabOrder(self.editEig2, self.editEig4)
        QWidget.setTabOrder(self.editEig4, self.editEig6)
        QWidget.setTabOrder(self.editEig6, self.editEig8)

        self.retranslateUi(formBeschreibung)

        self.comboFinanzen.setCurrentIndex(2)
        self.comboStatus.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(formBeschreibung)
    # setupUi

    def retranslateUi(self, formBeschreibung):
        formBeschreibung.setWindowTitle(QCoreApplication.translate("formBeschreibung", u"Beschreibung", None))
        self.label_4.setText(QCoreApplication.translate("formBeschreibung", u"Kurzbeschreibung", None))
        self.label_4.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_6.setText(QCoreApplication.translate("formBeschreibung", u"Eigenheiten", None))
        self.label_6.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label.setText(QCoreApplication.translate("formBeschreibung", u"Name", None))
        self.label.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_2.setText(QCoreApplication.translate("formBeschreibung", u"Spezies", None))
        self.label_2.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_3.setText(QCoreApplication.translate("formBeschreibung", u"Status", None))
        self.label_3.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.comboFinanzen.setItemText(0, QCoreApplication.translate("formBeschreibung", u"Sehr Reich", None))
        self.comboFinanzen.setItemText(1, QCoreApplication.translate("formBeschreibung", u"Reich", None))
        self.comboFinanzen.setItemText(2, QCoreApplication.translate("formBeschreibung", u"Normal", None))
        self.comboFinanzen.setItemText(3, QCoreApplication.translate("formBeschreibung", u"Arm", None))
        self.comboFinanzen.setItemText(4, QCoreApplication.translate("formBeschreibung", u"Sehr Arm", None))

        self.comboStatus.setItemText(0, QCoreApplication.translate("formBeschreibung", u"Elite", None))
        self.comboStatus.setItemText(1, QCoreApplication.translate("formBeschreibung", u"Oberschicht", None))
        self.comboStatus.setItemText(2, QCoreApplication.translate("formBeschreibung", u"Mittelschicht", None))
        self.comboStatus.setItemText(3, QCoreApplication.translate("formBeschreibung", u"Unterschicht", None))
        self.comboStatus.setItemText(4, QCoreApplication.translate("formBeschreibung", u"Abschaum", None))

        self.labelFinanzen.setText(QCoreApplication.translate("formBeschreibung", u"Finanzen", None))
        self.labelFinanzen.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_7.setText(QCoreApplication.translate("formBeschreibung", u"Heimatgebiet", None))
        self.label_7.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
    # retranslateUi

