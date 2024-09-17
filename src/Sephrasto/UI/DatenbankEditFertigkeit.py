# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditFertigkeit.ui'
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
    QFormLayout, QHBoxLayout, QLabel, QLineEdit,
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 416, 527))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leName)

        self.labelSF = QLabel(self.scrollAreaWidgetContents)
        self.labelSF.setObjectName(u"labelSF")
        self.labelSF.setMinimumSize(QSize(110, 0))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelSF)

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


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.labelAttribute = QLabel(self.scrollAreaWidgetContents)
        self.labelAttribute.setObjectName(u"labelAttribute")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelAttribute)

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


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")
        self.labelKategorie.setMinimumSize(QSize(110, 0))

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelKategorie)

        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboKategorie)

        self.labelKampffertigkeit = QLabel(self.scrollAreaWidgetContents)
        self.labelKampffertigkeit.setObjectName(u"labelKampffertigkeit")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelKampffertigkeit)

        self.comboKampffertigkeit = QComboBox(self.scrollAreaWidgetContents)
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.setObjectName(u"comboKampffertigkeit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comboKampffertigkeit)

        self.labelGruppieren = QLabel(self.scrollAreaWidgetContents)
        self.labelGruppieren.setObjectName(u"labelGruppieren")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelGruppieren)

        self.checkGruppieren = QCheckBox(self.scrollAreaWidgetContents)
        self.checkGruppieren.setObjectName(u"checkGruppieren")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.checkGruppieren)

        self.labelVoraussetzungen = QLabel(self.scrollAreaWidgetContents)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelVoraussetzungen)

        self.teVoraussetzungen = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.teVoraussetzungen)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelBeschreibung)

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

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.tabWidget)

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
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelSF.setText(QCoreApplication.translate("dialog", u"Steigerungsfaktor", None))
        self.spinSF.setSuffix("")
        self.labelAttribute.setText(QCoreApplication.translate("dialog", u"Attribute", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u" - ", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u" - ", None))
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
#if QT_CONFIG(tooltip)
        self.comboKategorie.setToolTip(QCoreApplication.translate("dialog", u"Fertigkeiten werden nach diesem Typ gruppiert und dann alphabetisch sortiert.", None))
#endif // QT_CONFIG(tooltip)
        self.labelKampffertigkeit.setText(QCoreApplication.translate("dialog", u"Kampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(0, QCoreApplication.translate("dialog", u"Keine Kampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(1, QCoreApplication.translate("dialog", u"Nahkampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(2, QCoreApplication.translate("dialog", u"Sonstige Kampffertigkeit", None))

#if QT_CONFIG(tooltip)
        self.comboKampffertigkeit.setToolTip(QCoreApplication.translate("dialog", u"Nahkampf- und Sonstige Kampffertigkeiten stehen bei Waffen zur Auswahl. Nahkampffertigkeiten werden gegebenenfalls nach einem abweichenden Steigerungsfaktor berechnet.", None))
#endif // QT_CONFIG(tooltip)
        self.labelGruppieren.setText(QCoreApplication.translate("dialog", u"Talente", None))
#if QT_CONFIG(tooltip)
        self.checkGruppieren.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Talente werden grunds\u00e4tzlich nach Fertigkeitskategorie gruppiert. Mit dieser Option werden sie zus\u00e4tzlich noch nach dem Namen der Fertigkeit gruppiert. Bei Talenten mit mehreren Fertigkeiten werden bei der Gruppierung au\u00dferdem Fertigkeiten mit dieser Option priorisiert.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkGruppieren.setText(QCoreApplication.translate("dialog", u"Nach dieser Fertigkeit priorisiert gruppieren", None))
        self.labelVoraussetzungen.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe \"Datenbank Editor -> Einstellungsm\u00f6glichkeiten -> Voraussetzungen\" in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
    # retranslateUi

