# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRuestung.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGridLayout,
    QLabel, QLineEdit, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QTextBrowser,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(475, 593)
        self.verticalLayout_3 = QVBoxLayout(dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 455, 573))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelBeine = QLabel(self.scrollAreaWidgetContents)
        self.labelBeine.setObjectName(u"labelBeine")

        self.gridLayout.addWidget(self.labelBeine, 4, 1, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.gridLayout.addWidget(self.labelBeschreibung, 10, 0, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")
        self.leName.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.leName, 0, 1, 1, 2)

        self.labelRS = QLabel(self.scrollAreaWidgetContents)
        self.labelRS.setObjectName(u"labelRS")

        self.gridLayout.addWidget(self.labelRS, 3, 2, 1, 1)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")

        self.gridLayout.addWidget(self.labelKategorie, 1, 0, 1, 1)

        self.spinSchwert = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSchwert.setObjectName(u"spinSchwert")
        self.spinSchwert.setMinimumSize(QSize(50, 0))
        self.spinSchwert.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchwert.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchwert.setMaximum(8)

        self.gridLayout.addWidget(self.spinSchwert, 6, 2, 1, 1)

        self.labelBauch = QLabel(self.scrollAreaWidgetContents)
        self.labelBauch.setObjectName(u"labelBauch")

        self.gridLayout.addWidget(self.labelBauch, 7, 1, 1, 1)

        self.labelSystem = QLabel(self.scrollAreaWidgetContents)
        self.labelSystem.setObjectName(u"labelSystem")

        self.gridLayout.addWidget(self.labelSystem, 2, 0, 1, 1)

        self.spinBrust = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBrust.setObjectName(u"spinBrust")
        self.spinBrust.setMinimumSize(QSize(50, 0))
        self.spinBrust.setMaximumSize(QSize(16777215, 16777215))
        self.spinBrust.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBrust.setMaximum(8)

        self.gridLayout.addWidget(self.spinBrust, 8, 2, 1, 1)

        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.teBeschreibung = QTextEdit(self.tab)
        self.teBeschreibung.setObjectName(u"teBeschreibung")

        self.verticalLayout.addWidget(self.teBeschreibung)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tbBeschreibung = QTextBrowser(self.tab_2)
        self.tbBeschreibung.setObjectName(u"tbBeschreibung")

        self.verticalLayout_2.addWidget(self.tbBeschreibung)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 10, 1, 1, 2)

        self.spinBauch = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBauch.setObjectName(u"spinBauch")
        self.spinBauch.setMinimumSize(QSize(50, 0))
        self.spinBauch.setMaximumSize(QSize(16777215, 16777215))
        self.spinBauch.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBauch.setMaximum(8)

        self.gridLayout.addWidget(self.spinBauch, 7, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(243, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 1, 1, 1)

        self.spinBeine = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBeine.setObjectName(u"spinBeine")
        self.spinBeine.setMinimumSize(QSize(50, 0))
        self.spinBeine.setMaximumSize(QSize(16777215, 16777215))
        self.spinBeine.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBeine.setMaximum(8)

        self.gridLayout.addWidget(self.spinBeine, 4, 2, 1, 1)

        self.labelBrust = QLabel(self.scrollAreaWidgetContents)
        self.labelBrust.setObjectName(u"labelBrust")

        self.gridLayout.addWidget(self.labelBrust, 8, 1, 1, 1)

        self.spinSchild = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSchild.setObjectName(u"spinSchild")
        self.spinSchild.setMinimumSize(QSize(50, 0))
        self.spinSchild.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchild.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchild.setMaximum(8)

        self.gridLayout.addWidget(self.spinSchild, 5, 2, 1, 1)

        self.labelSchild = QLabel(self.scrollAreaWidgetContents)
        self.labelSchild.setObjectName(u"labelSchild")

        self.gridLayout.addWidget(self.labelSchild, 5, 1, 1, 1)

        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.gridLayout.addWidget(self.comboKategorie, 1, 1, 1, 2)

        self.labelSchwert = QLabel(self.scrollAreaWidgetContents)
        self.labelSchwert.setObjectName(u"labelSchwert")

        self.gridLayout.addWidget(self.labelSchwert, 6, 1, 1, 1)

        self.spinKopf = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKopf.setObjectName(u"spinKopf")
        self.spinKopf.setMinimumSize(QSize(50, 0))
        self.spinKopf.setMaximumSize(QSize(16777215, 16777215))
        self.spinKopf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKopf.setMaximum(8)

        self.gridLayout.addWidget(self.spinKopf, 9, 2, 1, 1)

        self.labelKopf = QLabel(self.scrollAreaWidgetContents)
        self.labelKopf.setObjectName(u"labelKopf")

        self.gridLayout.addWidget(self.labelKopf, 9, 1, 1, 1)

        self.comboSystem = QComboBox(self.scrollAreaWidgetContents)
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.setObjectName(u"comboSystem")

        self.gridLayout.addWidget(self.comboSystem, 2, 1, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.comboKategorie)
        QWidget.setTabOrder(self.comboKategorie, self.comboSystem)
        QWidget.setTabOrder(self.comboSystem, self.spinBeine)
        QWidget.setTabOrder(self.spinBeine, self.spinSchild)
        QWidget.setTabOrder(self.spinSchild, self.spinSchwert)
        QWidget.setTabOrder(self.spinSchwert, self.spinBauch)
        QWidget.setTabOrder(self.spinBauch, self.spinBrust)
        QWidget.setTabOrder(self.spinBrust, self.spinKopf)

        self.retranslateUi(dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - R\u00fcstung bearbeiten...", None))
        self.labelBeine.setText(QCoreApplication.translate("dialog", u"Beine", None))
        self.label_8.setText(QCoreApplication.translate("dialog", u"RS", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.labelRS.setText(QCoreApplication.translate("dialog", u"0", None))
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
        self.labelBauch.setText(QCoreApplication.translate("dialog", u"Bauch", None))
        self.labelSystem.setText(QCoreApplication.translate("dialog", u"Verf\u00fcgbarkeit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.labelBrust.setText(QCoreApplication.translate("dialog", u"Brust", None))
        self.labelSchild.setText(QCoreApplication.translate("dialog", u"Schildarm", None))
        self.labelSchwert.setText(QCoreApplication.translate("dialog", u"Schwertarm", None))
        self.labelKopf.setText(QCoreApplication.translate("dialog", u"Kopf", None))
        self.comboSystem.setItemText(0, QCoreApplication.translate("dialog", u"Beide R\u00fcstungssysteme", None))
        self.comboSystem.setItemText(1, QCoreApplication.translate("dialog", u"Einfaches R\u00fcstungssystem", None))
        self.comboSystem.setItemText(2, QCoreApplication.translate("dialog", u"Zonenr\u00fcstungssystem", None))

    # retranslateUi

