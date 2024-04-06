# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRegel.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QPlainTextEdit, QSizePolicy, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(440, 462)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.warning = QLabel(dialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.leProbe = QLineEdit(dialog)
        self.leProbe.setObjectName(u"leProbe")

        self.gridLayout.addWidget(self.leProbe, 2, 1, 1, 1)

        self.teVoraussetzungen = QPlainTextEdit(dialog)
        self.teVoraussetzungen.setObjectName(u"teVoraussetzungen")
        self.teVoraussetzungen.setMaximumSize(QSize(16777215, 250))

        self.gridLayout.addWidget(self.teVoraussetzungen, 4, 1, 1, 1)

        self.label_2 = QLabel(dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_4 = QLabel(dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

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

        self.gridLayout.addWidget(self.tabWidget, 5, 1, 1, 1)

        self.label_5 = QLabel(dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.comboTyp = QComboBox(dialog)
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 3, 1, 1, 1)

        self.leName = QLineEdit(dialog)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 1)

        self.label_6 = QLabel(dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.leProbe)
        QWidget.setTabOrder(self.leProbe, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.teVoraussetzungen)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Regel bearbeiten...", None))
        self.warning.setText("")
#if QT_CONFIG(tooltip)
        self.teVoraussetzungen.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Siehe \"Datenbank Editor -> Einstellungsm\u00f6glichkeiten -> Voraussetzungen\" in der Sephrasto-Hilfe f\u00fcr eine Anleitung.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("dialog", u"Probe", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Voraussetzungen", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.comboTyp.setItemText(0, QCoreApplication.translate("dialog", u"Nahkampfman\u00f6ver", None))
        self.comboTyp.setItemText(1, QCoreApplication.translate("dialog", u"Fernkampfman\u00f6ver", None))
        self.comboTyp.setItemText(2, QCoreApplication.translate("dialog", u"Magische Modifikation", None))
        self.comboTyp.setItemText(3, QCoreApplication.translate("dialog", u"Karmale Modifikation", None))
        self.comboTyp.setItemText(4, QCoreApplication.translate("dialog", u"Weitere Magieregeln", None))
        self.comboTyp.setItemText(5, QCoreApplication.translate("dialog", u"Aktion", None))
        self.comboTyp.setItemText(6, QCoreApplication.translate("dialog", u"D\u00e4monische Modifikation", None))
        self.comboTyp.setItemText(7, QCoreApplication.translate("dialog", u"Weitere Karmaregeln", None))
        self.comboTyp.setItemText(8, QCoreApplication.translate("dialog", u"Weitere Kampfregeln", None))
        self.comboTyp.setItemText(9, QCoreApplication.translate("dialog", u"Profane Regeln", None))

        self.label_6.setText(QCoreApplication.translate("dialog", u"Typ", None))
    # retranslateUi

