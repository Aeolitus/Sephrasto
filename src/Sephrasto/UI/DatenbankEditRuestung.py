# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRuestung.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QLabel,
    QLineEdit, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(456, 590)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 436, 541))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.spinBauch = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBauch.setObjectName(u"spinBauch")
        self.spinBauch.setMinimumSize(QSize(50, 0))
        self.spinBauch.setMaximumSize(QSize(16777215, 16777215))
        self.spinBauch.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBauch.setMaximum(8)

        self.gridLayout.addWidget(self.spinBauch, 8, 2, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 8, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 5, 1, 1, 1)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)

        self.spinBrust = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBrust.setObjectName(u"spinBrust")
        self.spinBrust.setMinimumSize(QSize(50, 0))
        self.spinBrust.setMaximumSize(QSize(16777215, 16777215))
        self.spinBrust.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBrust.setMaximum(8)

        self.gridLayout.addWidget(self.spinBrust, 9, 2, 1, 1)

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

        self.gridLayout.addWidget(self.tabWidget, 11, 1, 1, 2)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 11, 0, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 10, 1, 1, 1)

        self.spinSchild = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSchild.setObjectName(u"spinSchild")
        self.spinSchild.setMinimumSize(QSize(50, 0))
        self.spinSchild.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchild.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchild.setMaximum(8)

        self.gridLayout.addWidget(self.spinSchild, 6, 2, 1, 1)

        self.spinBeine = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBeine.setObjectName(u"spinBeine")
        self.spinBeine.setMinimumSize(QSize(50, 0))
        self.spinBeine.setMaximumSize(QSize(16777215, 16777215))
        self.spinBeine.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBeine.setMaximum(8)

        self.gridLayout.addWidget(self.spinBeine, 5, 2, 1, 1)

        self.spinSchwert = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSchwert.setObjectName(u"spinSchwert")
        self.spinSchwert.setMinimumSize(QSize(50, 0))
        self.spinSchwert.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchwert.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchwert.setMaximum(8)

        self.gridLayout.addWidget(self.spinSchwert, 7, 2, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")
        self.leName.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 2)

        self.spinKopf = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKopf.setObjectName(u"spinKopf")
        self.spinKopf.setMinimumSize(QSize(50, 0))
        self.spinKopf.setMaximumSize(QSize(16777215, 16777215))
        self.spinKopf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKopf.setMaximum(8)

        self.gridLayout.addWidget(self.spinKopf, 10, 2, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 7, 1, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)

        self.labelRS = QLabel(self.scrollAreaWidgetContents)
        self.labelRS.setObjectName(u"labelRS")

        self.gridLayout.addWidget(self.labelRS, 4, 2, 1, 1)

        self.warning = QLabel(self.scrollAreaWidgetContents)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(True)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 3)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 9, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(243, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 1, 1, 1)

        self.comboTyp = QComboBox(self.scrollAreaWidgetContents)
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 2, 1, 1, 2)

        self.comboSystem = QComboBox(self.scrollAreaWidgetContents)
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.setObjectName(u"comboSystem")

        self.gridLayout.addWidget(self.comboSystem, 3, 1, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.comboSystem)
        QWidget.setTabOrder(self.comboSystem, self.spinBeine)
        QWidget.setTabOrder(self.spinBeine, self.spinSchild)
        QWidget.setTabOrder(self.spinSchild, self.spinSchwert)
        QWidget.setTabOrder(self.spinSchwert, self.spinBauch)
        QWidget.setTabOrder(self.spinBauch, self.spinBrust)
        QWidget.setTabOrder(self.spinBrust, self.spinKopf)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - R\u00fcstung bearbeiten...", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Schildarm", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Bauch", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Beine", None))
        self.label_11.setText(QCoreApplication.translate("dialog", u"Verf\u00fcgbarkeit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.label_10.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u"Kopf", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Schwertarm", None))
        self.label_8.setText(QCoreApplication.translate("dialog", u"RS", None))
        self.labelRS.setText(QCoreApplication.translate("dialog", u"0", None))
        self.warning.setText("")
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.label_9.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"Brust", None))
        self.comboSystem.setItemText(0, QCoreApplication.translate("dialog", u"Beide R\u00fcstungssysteme", None))
        self.comboSystem.setItemText(1, QCoreApplication.translate("dialog", u"Einfaches R\u00fcstungssystem", None))
        self.comboSystem.setItemText(2, QCoreApplication.translate("dialog", u"Zonenr\u00fcstungssystem", None))

    # retranslateUi

