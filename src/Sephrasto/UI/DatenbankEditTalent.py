# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditTalent.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPlainTextEdit, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(442, 587)
        self.verticalLayout_5 = QVBoxLayout(dialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 422, 567))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelVoraussetzungen = QLabel(self.scrollAreaWidgetContents)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")
        self.labelVoraussetzungen.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelVoraussetzungen, 6, 0, 1, 1)

        self.checkVariable = QCheckBox(self.scrollAreaWidgetContents)
        self.checkVariable.setObjectName(u"checkVariable")

        self.gridLayout.addWidget(self.checkVariable, 2, 1, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.gridLayout.addWidget(self.teVoraussetzungen, 6, 1, 1, 1)

        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.teBeschreibung = QPlainTextEdit(self.tab)
        self.teBeschreibung.setObjectName(u"teBeschreibung")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teBeschreibung.sizePolicy().hasHeightForWidth())
        self.teBeschreibung.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.teBeschreibung)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.teInfo = QPlainTextEdit(self.tab_3)
        self.teInfo.setObjectName(u"teInfo")

        self.verticalLayout_4.addWidget(self.teInfo)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.comboVorschau = QComboBox(self.tab_2)
        self.comboVorschau.addItem("")
        self.comboVorschau.addItem("")
        self.comboVorschau.setObjectName(u"comboVorschau")

        self.verticalLayout_3.addWidget(self.comboVorschau)

        self.tbBeschreibung = QTextBrowser(self.tab_2)
        self.tbBeschreibung.setObjectName(u"tbBeschreibung")

        self.verticalLayout_3.addWidget(self.tbBeschreibung)

        self.tbInfo = QTextBrowser(self.tab_2)
        self.tbInfo.setObjectName(u"tbInfo")

        self.verticalLayout_3.addWidget(self.tbInfo)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 7, 1, 1, 1)

        self.labelVariable = QLabel(self.scrollAreaWidgetContents)
        self.labelVariable.setObjectName(u"labelVariable")

        self.gridLayout.addWidget(self.labelVariable, 2, 0, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 0, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.horizontalLayout.addWidget(self.comboKategorie)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.checkVerbilligt = QCheckBox(self.scrollAreaWidgetContents)
        self.checkVerbilligt.setObjectName(u"checkVerbilligt")
        self.checkVerbilligt.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout.addWidget(self.checkVerbilligt)

        self.spinKosten = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKosten.setObjectName(u"spinKosten")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinKosten.sizePolicy().hasHeightForWidth())
        self.spinKosten.setSizePolicy(sizePolicy1)
        self.spinKosten.setMinimumSize(QSize(60, 0))
        self.spinKosten.setAlignment(Qt.AlignCenter)
        self.spinKosten.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKosten.setMinimum(0)
        self.spinKosten.setMaximum(9999)
        self.spinKosten.setSingleStep(20)

        self.horizontalLayout.addWidget(self.spinKosten)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.comboSeite = QComboBox(self.scrollAreaWidgetContents)
        self.comboSeite.setObjectName(u"comboSeite")

        self.horizontalLayout_3.addWidget(self.comboSeite)

        self.spinSeite = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSeite.setObjectName(u"spinSeite")
        self.spinSeite.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSeite.setMaximum(999)

        self.horizontalLayout_3.addWidget(self.spinSeite)


        self.gridLayout.addLayout(self.horizontalLayout_3, 8, 1, 1, 1)

        self.labelCheatsheet = QLabel(self.scrollAreaWidgetContents)
        self.labelCheatsheet.setObjectName(u"labelCheatsheet")

        self.gridLayout.addWidget(self.labelCheatsheet, 4, 0, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")

        self.gridLayout.addWidget(self.labelKategorie, 1, 0, 1, 1)

        self.checkKommentar = QCheckBox(self.scrollAreaWidgetContents)
        self.checkKommentar.setObjectName(u"checkKommentar")

        self.gridLayout.addWidget(self.checkKommentar, 3, 1, 1, 1)

        self.labelFertigkeiten = QLabel(self.scrollAreaWidgetContents)
        self.labelFertigkeiten.setObjectName(u"labelFertigkeiten")

        self.gridLayout.addWidget(self.labelFertigkeiten, 5, 0, 1, 1)

        self.labelSeite = QLabel(self.scrollAreaWidgetContents)
        self.labelSeite.setObjectName(u"labelSeite")

        self.gridLayout.addWidget(self.labelSeite, 8, 0, 1, 1)

        self.leFertigkeiten = QLineEdit(self.scrollAreaWidgetContents)
        self.leFertigkeiten.setObjectName(u"leFertigkeiten")

        self.gridLayout.addWidget(self.leFertigkeiten, 5, 1, 1, 1)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.gridLayout.addWidget(self.labelBeschreibung, 7, 0, 1, 1)

        self.checkCheatsheet = QCheckBox(self.scrollAreaWidgetContents)
        self.checkCheatsheet.setObjectName(u"checkCheatsheet")
        self.checkCheatsheet.setLayoutDirection(Qt.LeftToRight)
        self.checkCheatsheet.setChecked(True)

        self.gridLayout.addWidget(self.checkCheatsheet, 4, 1, 1, 1)

        self.labelKommentar = QLabel(self.scrollAreaWidgetContents)
        self.labelKommentar.setObjectName(u"labelKommentar")

        self.gridLayout.addWidget(self.labelKommentar, 3, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.checkKommentar)
        QWidget.setTabOrder(self.checkKommentar, self.checkCheatsheet)
        QWidget.setTabOrder(self.checkCheatsheet, self.leFertigkeiten)
        QWidget.setTabOrder(self.leFertigkeiten, self.teVoraussetzungen)

        self.retranslateUi(dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Talent bearbeiten...", None))
        self.labelVoraussetzungen.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
        self.checkVariable.setText(QCoreApplication.translate("dialog", u"Kosten sind durch Nutzer \u00e4nderbar", None))
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe \"Datenbank Editor -> Einstellungsm\u00f6glichkeiten -> Voraussetzungen\" in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
#if QT_CONFIG(tooltip)
        self.tab_3.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Zus\u00e4tzliche Informationen, die im Charaktereditor nach der Beschreibung eingef\u00fcgt werden sollen, beispielsweise eine Erkl\u00e4rung, wozu der Kommentar genutzt werden soll (optional).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("dialog", u"Zusatzinfo", None))
        self.comboVorschau.setItemText(0, QCoreApplication.translate("dialog", u"HTML", None))
        self.comboVorschau.setItemText(1, QCoreApplication.translate("dialog", u"Zusatzinfo", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.labelVariable.setText(QCoreApplication.translate("dialog", u"Variable Kosten", None))
#if QT_CONFIG(tooltip)
        self.comboKategorie.setToolTip(QCoreApplication.translate("dialog", u"Spezialtalente k\u00f6nnen nur \u00fcbernat\u00fcrlichen Fertigkeiten zugewiesen werden und sie haben frei w\u00e4hlbare Kosten.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkVerbilligt.setToolTip(QCoreApplication.translate("dialog", u"Verbilligte Talente kosten nur die H\u00e4lfte", None))
#endif // QT_CONFIG(tooltip)
        self.checkVerbilligt.setText(QCoreApplication.translate("dialog", u"verbilligt", None))
        self.spinKosten.setSuffix(QCoreApplication.translate("dialog", u" EP", None))
        self.labelCheatsheet.setText(QCoreApplication.translate("dialog", u"Regelanhang", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie und Kosten", None))
        self.checkKommentar.setText(QCoreApplication.translate("dialog", u"Feld f\u00fcr Nutzerkommentare hinzuf\u00fcgen", None))
        self.labelFertigkeiten.setText(QCoreApplication.translate("dialog", u"Fertigkeiten", None))
        self.labelSeite.setText(QCoreApplication.translate("dialog", u"Seitenreferenz", None))
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.checkCheatsheet.setText(QCoreApplication.translate("dialog", u"Auflisten", None))
        self.labelKommentar.setText(QCoreApplication.translate("dialog", u"Kommentar", None))
    # retranslateUi

