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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(628, 1086)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.spinKosten = QSpinBox(dialog)
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


        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)

        self.label_4 = QLabel(dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)

        self.groupBox = QGroupBox(dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
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

        self.listVerweise = QListWidget(self.groupBox)
        self.listVerweise.setObjectName(u"listVerweise")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listVerweise.sizePolicy().hasHeightForWidth())
        self.listVerweise.setSizePolicy(sizePolicy1)
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


        self.gridLayout.addWidget(self.groupBox, 12, 1, 1, 1)

        self.label_7 = QLabel(dialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.leScript = QLineEdit(dialog)
        self.leScript.setObjectName(u"leScript")

        self.horizontalLayout_4.addWidget(self.leScript)

        self.spinScriptPrio = QSpinBox(dialog)
        self.spinScriptPrio.setObjectName(u"spinScriptPrio")
        self.spinScriptPrio.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinScriptPrio.setMinimum(-10)
        self.spinScriptPrio.setMaximum(10)
        self.spinScriptPrio.setSingleStep(1)
        self.spinScriptPrio.setValue(0)

        self.horizontalLayout_4.addWidget(self.spinScriptPrio)


        self.gridLayout.addLayout(self.horizontalLayout_4, 10, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboLinkKategorie = QComboBox(dialog)
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.setObjectName(u"comboLinkKategorie")
        self.comboLinkKategorie.setMinimumSize(QSize(150, 0))
        self.comboLinkKategorie.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_5.addWidget(self.comboLinkKategorie)

        self.comboLinkElement = QComboBox(dialog)
        self.comboLinkElement.setObjectName(u"comboLinkElement")

        self.horizontalLayout_5.addWidget(self.comboLinkElement)


        self.gridLayout.addLayout(self.horizontalLayout_5, 11, 1, 1, 1)

        self.checkVariable = QCheckBox(dialog)
        self.checkVariable.setObjectName(u"checkVariable")

        self.gridLayout.addWidget(self.checkVariable, 5, 1, 1, 1)

        self.checkKommentar = QCheckBox(dialog)
        self.checkKommentar.setObjectName(u"checkKommentar")

        self.gridLayout.addWidget(self.checkKommentar, 6, 1, 1, 1)

        self.label_41 = QLabel(dialog)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_41, 10, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboNachkauf = QComboBox(dialog)
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.setObjectName(u"comboNachkauf")

        self.horizontalLayout.addWidget(self.comboNachkauf)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.comboTyp = QComboBox(dialog)
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 2, 1, 1, 1)

        self.label_12 = QLabel(dialog)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(dialog)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.gridLayout.addWidget(self.teVoraussetzungen, 8, 1, 1, 1)

        self.label_6 = QLabel(dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.leName = QLineEdit(dialog)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 1)

        self.label_5 = QLabel(dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)

        self.label_9 = QLabel(dialog)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setIndent(0)

        self.gridLayout.addWidget(self.label_9, 11, 0, 1, 1)

        self.label_11 = QLabel(dialog)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 12, 0, 1, 1)

        self.label_2 = QLabel(dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.label_10 = QLabel(dialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 7, 0, 1, 1)

        self.tabWidget = QTabWidget(dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.teBeschreibung = QPlainTextEdit(self.tab)
        self.teBeschreibung.setObjectName(u"teBeschreibung")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.teBeschreibung.sizePolicy().hasHeightForWidth())
        self.teBeschreibung.setSizePolicy(sizePolicy2)

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
        sizePolicy2.setHeightForWidth(self.teCheatsheet.sizePolicy().hasHeightForWidth())
        self.teCheatsheet.setSizePolicy(sizePolicy2)

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

        self.gridLayout.addWidget(self.tabWidget, 9, 1, 1, 1)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.warning = QLabel(dialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.checkCheatsheet = QCheckBox(dialog)
        self.checkCheatsheet.setObjectName(u"checkCheatsheet")
        self.checkCheatsheet.setChecked(True)

        self.gridLayout.addWidget(self.checkCheatsheet, 7, 1, 1, 1)

        self.label_3 = QLabel(dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.checkKommentar)
        QWidget.setTabOrder(self.checkKommentar, self.comboNachkauf)
        QWidget.setTabOrder(self.comboNachkauf, self.teVoraussetzungen)
        QWidget.setTabOrder(self.teVoraussetzungen, self.leScript)
        QWidget.setTabOrder(self.leScript, self.spinScriptPrio)
        QWidget.setTabOrder(self.spinScriptPrio, self.comboLinkElement)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Vorteil bearbeiten...", None))
        self.spinKosten.setSuffix(QCoreApplication.translate("dialog", u" EP", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
        self.groupBox.setTitle("")
        self.buttonVerweisUp.setText(QCoreApplication.translate("dialog", u"^", None))
        self.buttonVerweisUp.setProperty("class", QCoreApplication.translate("dialog", u"icon", None))
        self.buttonVerweisDown.setText(QCoreApplication.translate("dialog", u"v", None))
        self.buttonVerweisDown.setProperty("class", QCoreApplication.translate("dialog", u"icon", None))
        self.buttonVerweisDelete.setText(QCoreApplication.translate("dialog", u"DEL", None))
        self.buttonVerweisDelete.setProperty("class", QCoreApplication.translate("dialog", u"icon", None))
        self.comboVerweisTyp.setItemText(0, QCoreApplication.translate("dialog", u"Regel", None))
        self.comboVerweisTyp.setItemText(1, QCoreApplication.translate("dialog", u"Talent", None))
        self.comboVerweisTyp.setItemText(2, QCoreApplication.translate("dialog", u"Vorteil", None))
        self.comboVerweisTyp.setItemText(3, QCoreApplication.translate("dialog", u"Waffeneigenschaft", None))
        self.comboVerweisTyp.setItemText(4, QCoreApplication.translate("dialog", u"Abgeleiteter Wert", None))
        self.comboVerweisTyp.setItemText(5, QCoreApplication.translate("dialog", u"Statusse", None))
        self.comboVerweisTyp.setItemText(6, QCoreApplication.translate("dialog", u"Finanzen", None))

        self.buttonVerweisAdd.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonVerweisAdd.setProperty("class", QCoreApplication.translate("dialog", u"icon", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u"Kommentar", None))
#if QT_CONFIG(tooltip)
        self.leScript.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>In diesem Feld kannst du ein Python-Skript einf\u00fcgen, die beim Erwerb des Vorteils ausgef\u00fchrt werden. Siehe &quot;Skripte f\u00fcr Abgeleitete Werte, Vorteile und Waffeneigenschaften&quot; in der Sephrasto-Hilfe f\u00fcr verf\u00fcgbare Funktionen und Beispiele.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinScriptPrio.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Die Skript-Priorit\u00e4t legt die Reihenfolge der Auswertung fest. 0 ist Standard, negative Werte werden davor, positive Werte danach ausgewertet. Dies ist relevant, falls bspw. die INI verdoppelt werden soll nachdem Kampfreflexe eingerechnet wurde. In diesem Fall sollte die Skript-Priorit\u00e4t h\u00f6her als die von Kampfreflexe sein.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboLinkKategorie.setItemText(0, QCoreApplication.translate("dialog", u"Nicht verkn\u00fcpfen", None))
        self.comboLinkKategorie.setItemText(1, QCoreApplication.translate("dialog", u"Regel", None))
        self.comboLinkKategorie.setItemText(2, QCoreApplication.translate("dialog", u"\u00dcbernat. Talent", None))
        self.comboLinkKategorie.setItemText(3, QCoreApplication.translate("dialog", u"Vorteil", None))

        self.checkVariable.setText(QCoreApplication.translate("dialog", u"Kosten sind durch Nutzer \u00e4nderbar", None))
        self.checkKommentar.setText(QCoreApplication.translate("dialog", u"Feld f\u00fcr Nutzerkommentare hinzuf\u00fcgen", None))
        self.label_41.setText(QCoreApplication.translate("dialog", u"Script / Priorit\u00e4t", None))
        self.comboNachkauf.setItemText(0, QCoreApplication.translate("dialog", u"h\u00e4ufig", None))
        self.comboNachkauf.setItemText(1, QCoreApplication.translate("dialog", u"\u00fcblich", None))
        self.comboNachkauf.setItemText(2, QCoreApplication.translate("dialog", u"selten", None))
        self.comboNachkauf.setItemText(3, QCoreApplication.translate("dialog", u"extrem selten", None))
        self.comboNachkauf.setItemText(4, QCoreApplication.translate("dialog", u"nicht m\u00f6glich", None))

        self.label_12.setText(QCoreApplication.translate("dialog", u"Variable Kosten", None))
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe &quot;Datenbank Editor -&gt; Einstellungsm\u00f6glichkeiten -&gt; Voraussetzungen&quot; in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.label_9.setText(QCoreApplication.translate("dialog", u"Verkn\u00fcpfung", None))
        self.label_11.setText(QCoreApplication.translate("dialog", u"Querverweise", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Kosten", None))
        self.label_10.setText(QCoreApplication.translate("dialog", u"Regelanhang", None))
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
        self.label.setText(QCoreApplication.translate("dialog", u"Vorteilsname", None))
        self.warning.setText("")
        self.checkCheatsheet.setText(QCoreApplication.translate("dialog", u"Auflisten", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Nachkauf", None))
    # retranslateUi

