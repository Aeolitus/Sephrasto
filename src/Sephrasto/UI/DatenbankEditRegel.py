# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRegel.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QLineEdit, QPlainTextEdit, QScrollArea, QSizePolicy,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(440, 462)
        self.verticalLayout_3 = QVBoxLayout(dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 416, 438))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leName)

        self.labelProbe = QLabel(self.scrollAreaWidgetContents)
        self.labelProbe.setObjectName(u"labelProbe")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelProbe)

        self.leProbe = QLineEdit(self.scrollAreaWidgetContents)
        self.leProbe.setObjectName(u"leProbe")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.leProbe)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelKategorie)

        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.addItem("")
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboKategorie)

        self.labelVoraussetzungen = QLabel(self.scrollAreaWidgetContents)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")
        self.labelVoraussetzungen.setMinimumSize(QSize(110, 0))

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelVoraussetzungen)

        self.teVoraussetzungen = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.teVoraussetzungen)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelBeschreibung)

        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.teBeschreibung = QPlainTextEdit(self.tab)
        self.teBeschreibung.setObjectName(u"teBeschreibung")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teBeschreibung.sizePolicy().hasHeightForWidth())
        self.teBeschreibung.setSizePolicy(sizePolicy)

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

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.tabWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.leProbe)
        QWidget.setTabOrder(self.leProbe, self.comboKategorie)
        QWidget.setTabOrder(self.comboKategorie, self.teVoraussetzungen)

        self.retranslateUi(dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Regel bearbeiten...", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelProbe.setText(QCoreApplication.translate("dialog", u"Probe", None))
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
        self.comboKategorie.setItemText(0, QCoreApplication.translate("dialog", u"Nahkampfman\u00f6ver", None))
        self.comboKategorie.setItemText(1, QCoreApplication.translate("dialog", u"Fernkampfman\u00f6ver", None))
        self.comboKategorie.setItemText(2, QCoreApplication.translate("dialog", u"Magische Modifikation", None))
        self.comboKategorie.setItemText(3, QCoreApplication.translate("dialog", u"Karmale Modifikation", None))
        self.comboKategorie.setItemText(4, QCoreApplication.translate("dialog", u"Weitere Magieregeln", None))
        self.comboKategorie.setItemText(5, QCoreApplication.translate("dialog", u"Aktion", None))
        self.comboKategorie.setItemText(6, QCoreApplication.translate("dialog", u"D\u00e4monische Modifikation", None))
        self.comboKategorie.setItemText(7, QCoreApplication.translate("dialog", u"Weitere Karmaregeln", None))
        self.comboKategorie.setItemText(8, QCoreApplication.translate("dialog", u"Weitere Kampfregeln", None))
        self.comboKategorie.setItemText(9, QCoreApplication.translate("dialog", u"Profane Regeln", None))

        self.labelVoraussetzungen.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe \"Datenbank Editor -> Einstellungsm\u00f6glichkeiten -> Voraussetzungen\" in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
    # retranslateUi

