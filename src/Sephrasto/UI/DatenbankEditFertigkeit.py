# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditFertigkeit.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPlainTextEdit, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(440, 551)
        self.verticalLayout_3 = QVBoxLayout(dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 420, 531))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboAttribut1 = QComboBox(self.scrollAreaWidgetContents)
        self.comboAttribut1.setObjectName(u"comboAttribut1")
        self.comboAttribut1.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_6)

        self.comboAttribut2 = QComboBox(self.scrollAreaWidgetContents)
        self.comboAttribut2.setObjectName(u"comboAttribut2")
        self.comboAttribut2.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut2)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.comboAttribut3 = QComboBox(self.scrollAreaWidgetContents)
        self.comboAttribut3.setObjectName(u"comboAttribut3")
        self.comboAttribut3.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 2, 1, 1)

        self.labelVoraussetzungen = QLabel(self.scrollAreaWidgetContents)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")

        self.gridLayout.addWidget(self.labelVoraussetzungen, 7, 1, 1, 1)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.gridLayout.addWidget(self.labelBeschreibung, 8, 1, 1, 1)

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

        self.gridLayout.addWidget(self.tabWidget, 8, 2, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 1, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.spinSF = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSF.setObjectName(u"spinSF")
        self.spinSF.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSF.setMinimum(1)
        self.spinSF.setMaximum(999)
        self.spinSF.setSingleStep(1)
        self.spinSF.setValue(2)

        self.horizontalLayout_2.addWidget(self.spinSF)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 2, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 2, 1, 1)

        self.labelSF = QLabel(self.scrollAreaWidgetContents)
        self.labelSF.setObjectName(u"labelSF")
        self.labelSF.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelSF, 2, 1, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.gridLayout.addWidget(self.teVoraussetzungen, 7, 2, 1, 1)

        self.labelKampffertigkeit = QLabel(self.scrollAreaWidgetContents)
        self.labelKampffertigkeit.setObjectName(u"labelKampffertigkeit")

        self.gridLayout.addWidget(self.labelKampffertigkeit, 5, 1, 1, 1)

        self.labelAttribute = QLabel(self.scrollAreaWidgetContents)
        self.labelAttribute.setObjectName(u"labelAttribute")

        self.gridLayout.addWidget(self.labelAttribute, 3, 1, 1, 1)

        self.labelGruppieren = QLabel(self.scrollAreaWidgetContents)
        self.labelGruppieren.setObjectName(u"labelGruppieren")

        self.gridLayout.addWidget(self.labelGruppieren, 6, 1, 1, 1)

        self.checkGruppieren = QCheckBox(self.scrollAreaWidgetContents)
        self.checkGruppieren.setObjectName(u"checkGruppieren")

        self.gridLayout.addWidget(self.checkGruppieren, 6, 2, 1, 1)

        self.comboKampffertigkeit = QComboBox(self.scrollAreaWidgetContents)
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.setObjectName(u"comboKampffertigkeit")

        self.gridLayout.addWidget(self.comboKampffertigkeit, 5, 2, 1, 1)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")
        self.labelKategorie.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelKategorie, 4, 1, 1, 1)

        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.gridLayout.addWidget(self.comboKategorie, 4, 2, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.spinSF)
        QWidget.setTabOrder(self.spinSF, self.comboAttribut1)
        QWidget.setTabOrder(self.comboAttribut1, self.comboAttribut2)
        QWidget.setTabOrder(self.comboAttribut2, self.comboAttribut3)
        QWidget.setTabOrder(self.comboAttribut3, self.comboKategorie)
        QWidget.setTabOrder(self.comboKategorie, self.comboKampffertigkeit)
        QWidget.setTabOrder(self.comboKampffertigkeit, self.checkGruppieren)
        QWidget.setTabOrder(self.checkGruppieren, self.teVoraussetzungen)

        self.retranslateUi(dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Fertigkeit bearbeiten...", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u" - ", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u" - ", None))
        self.labelVoraussetzungen.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.spinSF.setSuffix("")
        self.labelSF.setText(QCoreApplication.translate("dialog", u"Steigerungsfaktor", None))
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe \"Datenbank Editor -> Einstellungsm\u00f6glichkeiten -> Voraussetzungen\" in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelKampffertigkeit.setText(QCoreApplication.translate("dialog", u"Kampffertigkeit", None))
        self.labelAttribute.setText(QCoreApplication.translate("dialog", u"Attribute", None))
        self.labelGruppieren.setText(QCoreApplication.translate("dialog", u"Talente", None))
#if QT_CONFIG(tooltip)
        self.checkGruppieren.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Talente werden grunds\u00e4tzlich nach Fertigkeitskategorie gruppiert. Mit dieser Option werden sie zus\u00e4tzlich noch nach dem Namen der Fertigkeit gruppiert. Bei Talenten mit mehreren Fertigkeiten werden bei der Gruppierung au\u00dferdem Fertigkeiten mit dieser Option priorisiert.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkGruppieren.setText(QCoreApplication.translate("dialog", u"Nach dieser Fertigkeit priorisiert gruppieren", None))
        self.comboKampffertigkeit.setItemText(0, QCoreApplication.translate("dialog", u"Keine Kampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(1, QCoreApplication.translate("dialog", u"Nahkampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(2, QCoreApplication.translate("dialog", u"Sonstige Kampffertigkeit", None))

#if QT_CONFIG(tooltip)
        self.comboKampffertigkeit.setToolTip(QCoreApplication.translate("dialog", u"Nahkampf- und Sonstige Kampffertigkeiten stehen bei Waffen zur Auswahl. Nahkampffertigkeiten werden gegebenenfalls nach einem abweichenden Steigerungsfaktor berechnet.", None))
#endif // QT_CONFIG(tooltip)
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
#if QT_CONFIG(tooltip)
        self.comboKategorie.setToolTip(QCoreApplication.translate("dialog", u"Fertigkeiten werden nach diesem Typ gruppiert und dann alphabetisch sortiert.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

