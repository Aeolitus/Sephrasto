# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRuestung.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 451, 569))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setMinimumSize(QSize(110, 0))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")
        self.leName.setMinimumSize(QSize(300, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leName)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelKategorie)

        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboKategorie)

        self.labelSystem = QLabel(self.scrollAreaWidgetContents)
        self.labelSystem.setObjectName(u"labelSystem")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelSystem)

        self.comboSystem = QComboBox(self.scrollAreaWidgetContents)
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.setObjectName(u"comboSystem")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboSystem)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.labelRS = QLabel(self.scrollAreaWidgetContents)
        self.labelRS.setObjectName(u"labelRS")

        self.horizontalLayout_7.addWidget(self.labelRS)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.labelBeine = QLabel(self.scrollAreaWidgetContents)
        self.labelBeine.setObjectName(u"labelBeine")
        self.labelBeine.setIndent(8)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelBeine)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.spinBeine = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBeine.setObjectName(u"spinBeine")
        self.spinBeine.setMinimumSize(QSize(50, 0))
        self.spinBeine.setMaximumSize(QSize(16777215, 16777215))
        self.spinBeine.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBeine.setMaximum(8)

        self.horizontalLayout_6.addWidget(self.spinBeine)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.labelSchild = QLabel(self.scrollAreaWidgetContents)
        self.labelSchild.setObjectName(u"labelSchild")
        self.labelSchild.setIndent(8)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelSchild)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.spinSchild = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSchild.setObjectName(u"spinSchild")
        self.spinSchild.setMinimumSize(QSize(50, 0))
        self.spinSchild.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchild.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchild.setMaximum(8)

        self.horizontalLayout_5.addWidget(self.spinSchild)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.labelSchwert = QLabel(self.scrollAreaWidgetContents)
        self.labelSchwert.setObjectName(u"labelSchwert")
        self.labelSchwert.setIndent(8)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelSchwert)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.spinSchwert = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSchwert.setObjectName(u"spinSchwert")
        self.spinSchwert.setMinimumSize(QSize(50, 0))
        self.spinSchwert.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchwert.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchwert.setMaximum(8)

        self.horizontalLayout_4.addWidget(self.spinSchwert)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.labelBauch = QLabel(self.scrollAreaWidgetContents)
        self.labelBauch.setObjectName(u"labelBauch")
        self.labelBauch.setIndent(8)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelBauch)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.spinBauch = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBauch.setObjectName(u"spinBauch")
        self.spinBauch.setMinimumSize(QSize(50, 0))
        self.spinBauch.setMaximumSize(QSize(16777215, 16777215))
        self.spinBauch.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBauch.setMaximum(8)

        self.horizontalLayout_3.addWidget(self.spinBauch)


        self.formLayout.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.labelBrust = QLabel(self.scrollAreaWidgetContents)
        self.labelBrust.setObjectName(u"labelBrust")
        self.labelBrust.setIndent(8)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.labelBrust)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.spinBrust = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBrust.setObjectName(u"spinBrust")
        self.spinBrust.setMinimumSize(QSize(50, 0))
        self.spinBrust.setMaximumSize(QSize(16777215, 16777215))
        self.spinBrust.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBrust.setMaximum(8)

        self.horizontalLayout_2.addWidget(self.spinBrust)


        self.formLayout.setLayout(8, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.labelKopf = QLabel(self.scrollAreaWidgetContents)
        self.labelKopf.setObjectName(u"labelKopf")
        self.labelKopf.setIndent(8)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.labelKopf)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_7)

        self.spinKopf = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKopf.setObjectName(u"spinKopf")
        self.spinKopf.setMinimumSize(QSize(50, 0))
        self.spinKopf.setMaximumSize(QSize(16777215, 16777215))
        self.spinKopf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKopf.setMaximum(8)

        self.horizontalLayout.addWidget(self.spinKopf)


        self.formLayout.setLayout(9, QFormLayout.FieldRole, self.horizontalLayout)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.labelBeschreibung)

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

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.tabWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.comboKategorie)
        QWidget.setTabOrder(self.comboKategorie, self.comboSystem)

        self.retranslateUi(dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - R\u00fcstung bearbeiten...", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
        self.labelSystem.setText(QCoreApplication.translate("dialog", u"Verf\u00fcgbarkeit", None))
        self.comboSystem.setItemText(0, QCoreApplication.translate("dialog", u"Beide R\u00fcstungssysteme", None))
        self.comboSystem.setItemText(1, QCoreApplication.translate("dialog", u"Einfaches R\u00fcstungssystem", None))
        self.comboSystem.setItemText(2, QCoreApplication.translate("dialog", u"Zonenr\u00fcstungssystem", None))

        self.label_8.setText(QCoreApplication.translate("dialog", u"RS", None))
        self.labelRS.setText(QCoreApplication.translate("dialog", u"0", None))
        self.labelBeine.setText(QCoreApplication.translate("dialog", u"Beine", None))
        self.labelSchild.setText(QCoreApplication.translate("dialog", u"Schildarm", None))
        self.labelSchwert.setText(QCoreApplication.translate("dialog", u"Schwertarm", None))
        self.labelBauch.setText(QCoreApplication.translate("dialog", u"Bauch", None))
        self.labelBrust.setText(QCoreApplication.translate("dialog", u"Brust", None))
        self.labelKopf.setText(QCoreApplication.translate("dialog", u"Kopf", None))
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
    # retranslateUi

