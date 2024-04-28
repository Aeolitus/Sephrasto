# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditTalent.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(442, 587)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 422, 538))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboTyp = QComboBox(self.scrollAreaWidgetContents)
        self.comboTyp.setObjectName(u"comboTyp")

        self.horizontalLayout.addWidget(self.comboTyp)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.checkVerbilligt = QCheckBox(self.scrollAreaWidgetContents)
        self.checkVerbilligt.setObjectName(u"checkVerbilligt")
        self.checkVerbilligt.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout.addWidget(self.checkVerbilligt)

        self.spinKosten = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKosten.setObjectName(u"spinKosten")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinKosten.sizePolicy().hasHeightForWidth())
        self.spinKosten.setSizePolicy(sizePolicy)
        self.spinKosten.setMinimumSize(QSize(60, 0))
        self.spinKosten.setAlignment(Qt.AlignCenter)
        self.spinKosten.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKosten.setMinimum(0)
        self.spinKosten.setMaximum(9999)
        self.spinKosten.setSingleStep(20)

        self.horizontalLayout.addWidget(self.spinKosten)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 2, 1, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)

        self.checkVariable = QCheckBox(self.scrollAreaWidgetContents)
        self.checkVariable.setObjectName(u"checkVariable")

        self.gridLayout.addWidget(self.checkVariable, 3, 1, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.checkKommentar = QCheckBox(self.scrollAreaWidgetContents)
        self.checkKommentar.setObjectName(u"checkKommentar")

        self.gridLayout.addWidget(self.checkKommentar, 4, 1, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.checkCheatsheet = QCheckBox(self.scrollAreaWidgetContents)
        self.checkCheatsheet.setObjectName(u"checkCheatsheet")
        self.checkCheatsheet.setLayoutDirection(Qt.LeftToRight)
        self.checkCheatsheet.setChecked(True)

        self.gridLayout.addWidget(self.checkCheatsheet, 5, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.leFertigkeiten = QLineEdit(self.scrollAreaWidgetContents)
        self.leFertigkeiten.setObjectName(u"leFertigkeiten")

        self.gridLayout.addWidget(self.leFertigkeiten, 6, 1, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.gridLayout.addWidget(self.teVoraussetzungen, 7, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)

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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.teBeschreibung.sizePolicy().hasHeightForWidth())
        self.teBeschreibung.setSizePolicy(sizePolicy1)

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

        self.gridLayout.addWidget(self.tabWidget, 8, 1, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 9, 0, 1, 1)

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


        self.gridLayout.addLayout(self.horizontalLayout_3, 9, 1, 1, 1)

        self.warning = QLabel(self.scrollAreaWidgetContents)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(True)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.checkKommentar)
        QWidget.setTabOrder(self.checkKommentar, self.checkCheatsheet)
        QWidget.setTabOrder(self.checkCheatsheet, self.leFertigkeiten)
        QWidget.setTabOrder(self.leFertigkeiten, self.teVoraussetzungen)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Talent bearbeiten...", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Kategorie und Kosten", None))
#if QT_CONFIG(tooltip)
        self.comboTyp.setToolTip(QCoreApplication.translate("dialog", u"Spezialtalente k\u00f6nnen nur \u00fcbernat\u00fcrlichen Fertigkeiten zugewiesen werden und sie haben frei w\u00e4hlbare Kosten.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkVerbilligt.setToolTip(QCoreApplication.translate("dialog", u"Verbilligte Talente kosten nur die H\u00e4lfte", None))
#endif // QT_CONFIG(tooltip)
        self.checkVerbilligt.setText(QCoreApplication.translate("dialog", u"verbilligt", None))
        self.spinKosten.setSuffix(QCoreApplication.translate("dialog", u" EP", None))
        self.label_9.setText(QCoreApplication.translate("dialog", u"Variable Kosten", None))
        self.checkVariable.setText(QCoreApplication.translate("dialog", u"Kosten sind durch Nutzer \u00e4nderbar", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"Kommentar", None))
        self.checkKommentar.setText(QCoreApplication.translate("dialog", u"Feld f\u00fcr Nutzerkommentare hinzuf\u00fcgen", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u"Regelanhang", None))
        self.checkCheatsheet.setText(QCoreApplication.translate("dialog", u"Auflisten", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Fertigkeiten", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe \"Datenbank Editor -> Einstellungsm\u00f6glichkeiten -> Voraussetzungen\" in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
#if QT_CONFIG(tooltip)
        self.tab_3.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Zus\u00e4tzliche Informationen, die im Charaktereditor nach der Beschreibung eingef\u00fcgt werden sollen, beispielsweise eine Erkl\u00e4rung, wozu der Kommentar genutzt werden soll (optional).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("dialog", u"Zusatzinfo", None))
        self.comboVorschau.setItemText(0, QCoreApplication.translate("dialog", u"HTML", None))
        self.comboVorschau.setItemText(1, QCoreApplication.translate("dialog", u"Zusatzinfo", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.label_8.setText(QCoreApplication.translate("dialog", u"Seitenreferenz", None))
        self.warning.setText("")
    # retranslateUi

