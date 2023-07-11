# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditFertigkeit.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(440, 551)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelVoraussetzungen = QLabel(dialog)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")

        self.gridLayout.addWidget(self.labelVoraussetzungen, 7, 0, 1, 1)

        self.labelGruppieren = QLabel(dialog)
        self.labelGruppieren.setObjectName(u"labelGruppieren")

        self.gridLayout.addWidget(self.labelGruppieren, 6, 0, 1, 1)

        self.checkGruppieren = QCheckBox(dialog)
        self.checkGruppieren.setObjectName(u"checkGruppieren")

        self.gridLayout.addWidget(self.checkGruppieren, 6, 1, 1, 1)

        self.comboKampffertigkeit = QComboBox(dialog)
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.setObjectName(u"comboKampffertigkeit")

        self.gridLayout.addWidget(self.comboKampffertigkeit, 5, 1, 1, 1)

        self.comboTyp = QComboBox(dialog)
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 4, 1, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(dialog)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.gridLayout.addWidget(self.teVoraussetzungen, 7, 1, 1, 1)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.warning = QLabel(dialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.label_2 = QLabel(dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_5 = QLabel(dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)

        self.label_12 = QLabel(dialog)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.spinSF = QSpinBox(dialog)
        self.spinSF.setObjectName(u"spinSF")
        self.spinSF.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSF.setMinimum(1)
        self.spinSF.setMaximum(99)
        self.spinSF.setSingleStep(1)
        self.spinSF.setValue(2)

        self.horizontalLayout_2.addWidget(self.spinSF)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.labelKampffertigkeit = QLabel(dialog)
        self.labelKampffertigkeit.setObjectName(u"labelKampffertigkeit")

        self.gridLayout.addWidget(self.labelKampffertigkeit, 5, 0, 1, 1)

        self.leName = QLineEdit(dialog)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 1)

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
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
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

        self.gridLayout.addWidget(self.tabWidget, 8, 1, 1, 1)

        self.label_3 = QLabel(dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboAttribut1 = QComboBox(dialog)
        self.comboAttribut1.setObjectName(u"comboAttribut1")
        self.comboAttribut1.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut1)

        self.label_6 = QLabel(dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_6)

        self.comboAttribut2 = QComboBox(dialog)
        self.comboAttribut2.setObjectName(u"comboAttribut2")
        self.comboAttribut2.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut2)

        self.label_7 = QLabel(dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.comboAttribut3 = QComboBox(dialog)
        self.comboAttribut3.setObjectName(u"comboAttribut3")
        self.comboAttribut3.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.spinSF)
        QWidget.setTabOrder(self.spinSF, self.comboAttribut1)
        QWidget.setTabOrder(self.comboAttribut1, self.comboAttribut2)
        QWidget.setTabOrder(self.comboAttribut2, self.comboAttribut3)
        QWidget.setTabOrder(self.comboAttribut3, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.comboKampffertigkeit)
        QWidget.setTabOrder(self.comboKampffertigkeit, self.checkGruppieren)
        QWidget.setTabOrder(self.checkGruppieren, self.teVoraussetzungen)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Fertigkeit bearbeiten...", None))
        self.labelVoraussetzungen.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
        self.labelGruppieren.setText(QCoreApplication.translate("dialog", u"Talente", None))
#if QT_CONFIG(tooltip)
        self.checkGruppieren.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Talente werden grunds\u00e4tzlich nach Fertigkeitstyp gruppiert. Mit dieser Option werden sie zus\u00e4tzlich noch nach dem Namen der Fertigkeit gruppiert. Bei Talenten mit mehreren Fertigkeiten werden bei der Gruppierung au\u00dferdem Fertigkeiten mit dieser Option priorisiert.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkGruppieren.setText(QCoreApplication.translate("dialog", u"Nach dieser Fertigkeit priorisiert gruppieren", None))
        self.comboKampffertigkeit.setItemText(0, QCoreApplication.translate("dialog", u"Keine Kampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(1, QCoreApplication.translate("dialog", u"Nahkampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(2, QCoreApplication.translate("dialog", u"Sonstige Kampffertigkeit", None))

#if QT_CONFIG(tooltip)
        self.comboKampffertigkeit.setToolTip(QCoreApplication.translate("dialog", u"Nahkampf- und Sonstige Kampffertigkeiten stehen bei Waffen zur Auswahl. Nahkampffertigkeiten werden gegebenenfalls nach einem abweichenden Steigerungsfaktor berechnet.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboTyp.setToolTip(QCoreApplication.translate("dialog", u"Fertigkeiten werden nach diesem Typ gruppiert und dann alphabetisch sortiert.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe \"Datenbank Editor -> Einstellungsm\u00f6glichkeiten -> Voraussetzungen\" in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("dialog", u"Fertigkeitsname", None))
        self.warning.setText("")
        self.label_2.setText(QCoreApplication.translate("dialog", u"Steigerungsfaktor", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.label_12.setText(QCoreApplication.translate("dialog", u"Typ", None))
        self.spinSF.setSuffix("")
        self.labelKampffertigkeit.setText(QCoreApplication.translate("dialog", u"Kampffertigkeit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Attribute", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u" - ", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u" - ", None))
    # retranslateUi

