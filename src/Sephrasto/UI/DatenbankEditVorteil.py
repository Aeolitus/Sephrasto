# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditVorteil.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPlainTextEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(661, 1200)
        self.verticalLayout_8 = QVBoxLayout(dialog)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 641, 1180))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 2, 1, 1)

        self.labelVoraussetzungen = QLabel(self.scrollAreaWidgetContents)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")
        self.labelVoraussetzungen.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelVoraussetzungen, 9, 1, 1, 1)

        self.checkKommentar = QCheckBox(self.scrollAreaWidgetContents)
        self.checkKommentar.setObjectName(u"checkKommentar")

        self.gridLayout.addWidget(self.checkKommentar, 6, 2, 1, 1)

        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.gridLayout.addWidget(self.comboKategorie, 2, 2, 1, 1)

        self.labelCheatsheet = QLabel(self.scrollAreaWidgetContents)
        self.labelCheatsheet.setObjectName(u"labelCheatsheet")

        self.gridLayout.addWidget(self.labelCheatsheet, 8, 1, 1, 1)

        self.labelKommentar = QLabel(self.scrollAreaWidgetContents)
        self.labelKommentar.setObjectName(u"labelKommentar")

        self.gridLayout.addWidget(self.labelKommentar, 6, 1, 1, 1)

        self.checkVariable = QCheckBox(self.scrollAreaWidgetContents)
        self.checkVariable.setObjectName(u"checkVariable")

        self.gridLayout.addWidget(self.checkVariable, 5, 2, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.teScript = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teScript.setObjectName(u"teScript")

        self.horizontalLayout_4.addWidget(self.teScript)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.spinScriptPrio = QSpinBox(self.scrollAreaWidgetContents)
        self.spinScriptPrio.setObjectName(u"spinScriptPrio")
        self.spinScriptPrio.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinScriptPrio.setMinimum(-999)
        self.spinScriptPrio.setMaximum(999)
        self.spinScriptPrio.setSingleStep(1)
        self.spinScriptPrio.setValue(0)

        self.verticalLayout_7.addWidget(self.spinScriptPrio)

        self.buttonPickScript = QPushButton(self.scrollAreaWidgetContents)
        self.buttonPickScript.setObjectName(u"buttonPickScript")

        self.verticalLayout_7.addWidget(self.buttonPickScript)


        self.horizontalLayout_4.addLayout(self.verticalLayout_7)


        self.gridLayout.addLayout(self.horizontalLayout_4, 11, 2, 1, 1)

        self.labelScript = QLabel(self.scrollAreaWidgetContents)
        self.labelScript.setObjectName(u"labelScript")
        self.labelScript.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelScript, 11, 1, 1, 1)

        self.labelKosten = QLabel(self.scrollAreaWidgetContents)
        self.labelKosten.setObjectName(u"labelKosten")

        self.gridLayout.addWidget(self.labelKosten, 4, 1, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 1, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboLinkKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.setObjectName(u"comboLinkKategorie")
        self.comboLinkKategorie.setMinimumSize(QSize(150, 0))
        self.comboLinkKategorie.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_5.addWidget(self.comboLinkKategorie)

        self.comboLinkElement = QComboBox(self.scrollAreaWidgetContents)
        self.comboLinkElement.setObjectName(u"comboLinkElement")

        self.horizontalLayout_5.addWidget(self.comboLinkElement)


        self.gridLayout.addLayout(self.horizontalLayout_5, 12, 2, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.spinKosten = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKosten.setObjectName(u"spinKosten")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinKosten.sizePolicy().hasHeightForWidth())
        self.spinKosten.setSizePolicy(sizePolicy)
        self.spinKosten.setAlignment(Qt.AlignCenter)
        self.spinKosten.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKosten.setMinimum(-9999)
        self.spinKosten.setMaximum(9999)
        self.spinKosten.setSingleStep(20)
        self.spinKosten.setValue(40)

        self.horizontalLayout_2.addWidget(self.spinKosten)


        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 2, 1, 1)

        self.labelNachkauf = QLabel(self.scrollAreaWidgetContents)
        self.labelNachkauf.setObjectName(u"labelNachkauf")

        self.gridLayout.addWidget(self.labelNachkauf, 3, 1, 1, 1)

        self.checkScript = QCheckBox(self.scrollAreaWidgetContents)
        self.checkScript.setObjectName(u"checkScript")

        self.gridLayout.addWidget(self.checkScript, 7, 2, 1, 1)

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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.teBeschreibung.sizePolicy().hasHeightForWidth())
        self.teBeschreibung.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.teBeschreibung)

        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_4 = QVBoxLayout(self.tab_4)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.teBedingungen = QPlainTextEdit(self.tab_4)
        self.teBedingungen.setObjectName(u"teBedingungen")

        self.verticalLayout_4.addWidget(self.teBedingungen)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.teCheatsheet = QPlainTextEdit(self.tab_2)
        self.teCheatsheet.setObjectName(u"teCheatsheet")
        sizePolicy1.setHeightForWidth(self.teCheatsheet.sizePolicy().hasHeightForWidth())
        self.teCheatsheet.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.teCheatsheet)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_5 = QVBoxLayout(self.tab_5)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.teInfo = QPlainTextEdit(self.tab_5)
        self.teInfo.setObjectName(u"teInfo")

        self.verticalLayout_5.addWidget(self.teInfo)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_3 = QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.comboVorschau = QComboBox(self.tab_3)
        self.comboVorschau.addItem("")
        self.comboVorschau.addItem("")
        self.comboVorschau.addItem("")
        self.comboVorschau.addItem("")
        self.comboVorschau.setObjectName(u"comboVorschau")

        self.verticalLayout_3.addWidget(self.comboVorschau)

        self.tbBeschreibung = QTextBrowser(self.tab_3)
        self.tbBeschreibung.setObjectName(u"tbBeschreibung")

        self.verticalLayout_3.addWidget(self.tbBeschreibung)

        self.tbBedingungen = QTextBrowser(self.tab_3)
        self.tbBedingungen.setObjectName(u"tbBedingungen")

        self.verticalLayout_3.addWidget(self.tbBedingungen)

        self.tbCheatsheet = QTextBrowser(self.tab_3)
        self.tbCheatsheet.setObjectName(u"tbCheatsheet")

        self.verticalLayout_3.addWidget(self.tbCheatsheet)

        self.tbInfo = QTextBrowser(self.tab_3)
        self.tbInfo.setObjectName(u"tbInfo")

        self.verticalLayout_3.addWidget(self.tbInfo)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget, 10, 2, 1, 1)

        self.labelLink = QLabel(self.scrollAreaWidgetContents)
        self.labelLink.setObjectName(u"labelLink")
        self.labelLink.setIndent(0)

        self.gridLayout.addWidget(self.labelLink, 12, 1, 1, 1)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.gridLayout.addWidget(self.labelBeschreibung, 10, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboNachkauf = QComboBox(self.scrollAreaWidgetContents)
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.setObjectName(u"comboNachkauf")

        self.horizontalLayout.addWidget(self.comboNachkauf)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 2, 1, 1)

        self.labelScriptfeld = QLabel(self.scrollAreaWidgetContents)
        self.labelScriptfeld.setObjectName(u"labelScriptfeld")

        self.gridLayout.addWidget(self.labelScriptfeld, 7, 1, 1, 1)

        self.labelVerweise = QLabel(self.scrollAreaWidgetContents)
        self.labelVerweise.setObjectName(u"labelVerweise")

        self.gridLayout.addWidget(self.labelVerweise, 13, 1, 1, 1)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.listVerweise = QListWidget(self.groupBox)
        self.listVerweise.setObjectName(u"listVerweise")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listVerweise.sizePolicy().hasHeightForWidth())
        self.listVerweise.setSizePolicy(sizePolicy2)
        self.listVerweise.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listVerweise.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout_3.addWidget(self.listVerweise, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.comboVerweisTyp = QComboBox(self.groupBox)
        self.comboVerweisTyp.addItem("")
        self.comboVerweisTyp.addItem("")
        self.comboVerweisTyp.addItem("")
        self.comboVerweisTyp.addItem("")
        self.comboVerweisTyp.addItem("")
        self.comboVerweisTyp.addItem("")
        self.comboVerweisTyp.addItem("")
        self.comboVerweisTyp.setObjectName(u"comboVerweisTyp")
        self.comboVerweisTyp.setMinimumSize(QSize(150, 0))
        self.comboVerweisTyp.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_3.addWidget(self.comboVerweisTyp)

        self.comboVerweis = QComboBox(self.groupBox)
        self.comboVerweis.setObjectName(u"comboVerweis")

        self.horizontalLayout_3.addWidget(self.comboVerweis)

        self.buttonVerweisAdd = QPushButton(self.groupBox)
        self.buttonVerweisAdd.setObjectName(u"buttonVerweisAdd")

        self.horizontalLayout_3.addWidget(self.buttonVerweisAdd)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.buttonVerweisUp = QPushButton(self.groupBox)
        self.buttonVerweisUp.setObjectName(u"buttonVerweisUp")

        self.verticalLayout_6.addWidget(self.buttonVerweisUp)

        self.buttonVerweisDown = QPushButton(self.groupBox)
        self.buttonVerweisDown.setObjectName(u"buttonVerweisDown")

        self.verticalLayout_6.addWidget(self.buttonVerweisDown)

        self.buttonVerweisDelete = QPushButton(self.groupBox)
        self.buttonVerweisDelete.setObjectName(u"buttonVerweisDelete")

        self.verticalLayout_6.addWidget(self.buttonVerweisDelete)


        self.gridLayout_3.addLayout(self.verticalLayout_6, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 13, 2, 1, 1)

        self.checkCheatsheet = QCheckBox(self.scrollAreaWidgetContents)
        self.checkCheatsheet.setObjectName(u"checkCheatsheet")
        self.checkCheatsheet.setChecked(True)

        self.gridLayout.addWidget(self.checkCheatsheet, 8, 2, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.gridLayout.addWidget(self.teVoraussetzungen, 9, 2, 1, 1)

        self.labelVariable = QLabel(self.scrollAreaWidgetContents)
        self.labelVariable.setObjectName(u"labelVariable")

        self.gridLayout.addWidget(self.labelVariable, 5, 1, 1, 1)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")

        self.gridLayout.addWidget(self.labelKategorie, 2, 1, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_8.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.comboKategorie)
        QWidget.setTabOrder(self.comboKategorie, self.comboNachkauf)
        QWidget.setTabOrder(self.comboNachkauf, self.spinKosten)
        QWidget.setTabOrder(self.spinKosten, self.checkVariable)
        QWidget.setTabOrder(self.checkVariable, self.checkKommentar)
        QWidget.setTabOrder(self.checkKommentar, self.checkScript)
        QWidget.setTabOrder(self.checkScript, self.checkCheatsheet)
        QWidget.setTabOrder(self.checkCheatsheet, self.teVoraussetzungen)
        QWidget.setTabOrder(self.teVoraussetzungen, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.teBeschreibung)
        QWidget.setTabOrder(self.teBeschreibung, self.teScript)
        QWidget.setTabOrder(self.teScript, self.spinScriptPrio)
        QWidget.setTabOrder(self.spinScriptPrio, self.buttonPickScript)
        QWidget.setTabOrder(self.buttonPickScript, self.comboLinkKategorie)
        QWidget.setTabOrder(self.comboLinkKategorie, self.comboLinkElement)
        QWidget.setTabOrder(self.comboLinkElement, self.listVerweise)
        QWidget.setTabOrder(self.listVerweise, self.comboVerweisTyp)
        QWidget.setTabOrder(self.comboVerweisTyp, self.comboVerweis)
        QWidget.setTabOrder(self.comboVerweis, self.buttonVerweisAdd)
        QWidget.setTabOrder(self.buttonVerweisAdd, self.buttonVerweisUp)
        QWidget.setTabOrder(self.buttonVerweisUp, self.buttonVerweisDown)
        QWidget.setTabOrder(self.buttonVerweisDown, self.buttonVerweisDelete)
        QWidget.setTabOrder(self.buttonVerweisDelete, self.teBedingungen)
        QWidget.setTabOrder(self.teBedingungen, self.tbCheatsheet)
        QWidget.setTabOrder(self.tbCheatsheet, self.tbBedingungen)
        QWidget.setTabOrder(self.tbBedingungen, self.teInfo)
        QWidget.setTabOrder(self.teInfo, self.teCheatsheet)
        QWidget.setTabOrder(self.teCheatsheet, self.comboVorschau)
        QWidget.setTabOrder(self.comboVorschau, self.tbInfo)
        QWidget.setTabOrder(self.tbInfo, self.tbBeschreibung)

        self.retranslateUi(dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Vorteil bearbeiten...", None))
        self.labelVoraussetzungen.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
        self.checkKommentar.setText(QCoreApplication.translate("dialog", u"Nutzer k\u00f6nnen Kommentare hinzuf\u00fcgen", None))
        self.labelCheatsheet.setText(QCoreApplication.translate("dialog", u"Regelanhang", None))
        self.labelKommentar.setText(QCoreApplication.translate("dialog", u"Kommentarfeld", None))
        self.checkVariable.setText(QCoreApplication.translate("dialog", u"Nutzer k\u00f6nnen die EP-Kosten \u00e4ndern", None))
#if QT_CONFIG(tooltip)
        self.spinScriptPrio.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Die Skript-Priorit\u00e4t legt die Reihenfolge der Auswertung fest. 0 ist Standard, negative Werte werden davor, positive Werte danach ausgewertet. Dies ist relevant, falls bspw. die INI verdoppelt werden soll nachdem Kampfreflexe eingerechnet wurde. In diesem Fall sollte die Skript-Priorit\u00e4t h\u00f6her als die von Kampfreflexe sein.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonPickScript.setToolTip(QCoreApplication.translate("dialog", u"Scripteditor \u00f6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonPickScript.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonPickScript.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.labelScript.setText(QCoreApplication.translate("dialog", u"Script / Priorit\u00e4t", None))
        self.labelKosten.setText(QCoreApplication.translate("dialog", u"Kosten", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.comboLinkKategorie.setItemText(0, QCoreApplication.translate("dialog", u"Nicht verkn\u00fcpfen", None))
        self.comboLinkKategorie.setItemText(1, QCoreApplication.translate("dialog", u"Regel", None))
        self.comboLinkKategorie.setItemText(2, QCoreApplication.translate("dialog", u"\u00dcbernat. Talent", None))
        self.comboLinkKategorie.setItemText(3, QCoreApplication.translate("dialog", u"Vorteil", None))

        self.spinKosten.setSuffix(QCoreApplication.translate("dialog", u" EP", None))
        self.labelNachkauf.setText(QCoreApplication.translate("dialog", u"Nachkauf", None))
        self.checkScript.setText(QCoreApplication.translate("dialog", u"Nutzer k\u00f6nnen Scripts hinzuf\u00fcgen", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
#if QT_CONFIG(tooltip)
        self.tab_4.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Manche Vorteile wie Kampfstile und Traditionen haben im Spiel Bedingungen, damit sie genutzt werden k\u00f6nnen. Diese kannst du hier eintragen (optional).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("dialog", u"Bedingungen", None))
#if QT_CONFIG(tooltip)
        self.tab_2.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Eine alternative Beschreibung f\u00fcr den Regelanhang. Falls das Textfeld leer ist, wird im Regelanhang die regul\u00e4re Beschreibung verwendet. Du hast hier die M\u00f6glichkeit das Makro $kommentar$ zu verwenden - Sephrasto wird dann dann Nutzerkommentar an entsprechender Stelle einf\u00fcgen</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Regelanhang", None))
#if QT_CONFIG(tooltip)
        self.tab_5.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Zus\u00e4tzliche Informationen, die im Charaktereditor nach der Beschreibung eingef\u00fcgt werden sollen, beispielsweise eine Erkl\u00e4rung, wozu der Kommentar genutzt werden soll (optional).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("dialog", u"Zusatzinfo", None))
        self.comboVorschau.setItemText(0, QCoreApplication.translate("dialog", u"HTML", None))
        self.comboVorschau.setItemText(1, QCoreApplication.translate("dialog", u"Bedingungen", None))
        self.comboVorschau.setItemText(2, QCoreApplication.translate("dialog", u"Regelanhang", None))
        self.comboVorschau.setItemText(3, QCoreApplication.translate("dialog", u"Zusatzinfo", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.labelLink.setText(QCoreApplication.translate("dialog", u"Verkn\u00fcpfung", None))
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.comboNachkauf.setItemText(0, QCoreApplication.translate("dialog", u"h\u00e4ufig", None))
        self.comboNachkauf.setItemText(1, QCoreApplication.translate("dialog", u"\u00fcblich", None))
        self.comboNachkauf.setItemText(2, QCoreApplication.translate("dialog", u"selten", None))
        self.comboNachkauf.setItemText(3, QCoreApplication.translate("dialog", u"extrem selten", None))
        self.comboNachkauf.setItemText(4, QCoreApplication.translate("dialog", u"nicht m\u00f6glich", None))

        self.labelScriptfeld.setText(QCoreApplication.translate("dialog", u"Scriptfeld", None))
        self.labelVerweise.setText(QCoreApplication.translate("dialog", u"Querverweise", None))
        self.groupBox.setTitle("")
        self.comboVerweisTyp.setItemText(0, QCoreApplication.translate("dialog", u"Regel", None))
        self.comboVerweisTyp.setItemText(1, QCoreApplication.translate("dialog", u"Talent", None))
        self.comboVerweisTyp.setItemText(2, QCoreApplication.translate("dialog", u"Vorteil", None))
        self.comboVerweisTyp.setItemText(3, QCoreApplication.translate("dialog", u"Waffeneigenschaft", None))
        self.comboVerweisTyp.setItemText(4, QCoreApplication.translate("dialog", u"Abgeleiteter Wert", None))
        self.comboVerweisTyp.setItemText(5, QCoreApplication.translate("dialog", u"Statusse", None))
        self.comboVerweisTyp.setItemText(6, QCoreApplication.translate("dialog", u"Finanzen", None))

        self.buttonVerweisAdd.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonVerweisAdd.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.buttonVerweisUp.setText(QCoreApplication.translate("dialog", u"^", None))
        self.buttonVerweisUp.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.buttonVerweisDown.setText(QCoreApplication.translate("dialog", u"v", None))
        self.buttonVerweisDown.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.buttonVerweisDelete.setText(QCoreApplication.translate("dialog", u"DEL", None))
        self.buttonVerweisDelete.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.checkCheatsheet.setText(QCoreApplication.translate("dialog", u"Auflisten", None))
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe &quot;Datenbank Editor -&gt; Einstellungsm\u00f6glichkeiten -&gt; Voraussetzungen&quot; in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelVariable.setText(QCoreApplication.translate("dialog", u"Variable Kosten", None))
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
    # retranslateUi

