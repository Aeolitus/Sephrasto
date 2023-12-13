# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRuestung.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QLineEdit, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextBrowser, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(441, 465)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(dialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 11, 1, 1, 1)

        self.spinBrust = QSpinBox(dialog)
        self.spinBrust.setObjectName(u"spinBrust")
        self.spinBrust.setMinimumSize(QSize(50, 0))
        self.spinBrust.setMaximumSize(QSize(16777215, 16777215))
        self.spinBrust.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBrust.setMaximum(8)

        self.gridLayout.addWidget(self.spinBrust, 10, 2, 1, 1)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.spinSchild = QSpinBox(dialog)
        self.spinSchild.setObjectName(u"spinSchild")
        self.spinSchild.setMinimumSize(QSize(50, 0))
        self.spinSchild.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchild.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchild.setMaximum(8)

        self.gridLayout.addWidget(self.spinSchild, 7, 2, 1, 1)

        self.label_10 = QLabel(dialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 12, 0, 1, 1)

        self.leName = QLineEdit(dialog)
        self.leName.setObjectName(u"leName")
        self.leName.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.leName, 2, 1, 1, 2)

        self.label_6 = QLabel(dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 10, 1, 1, 1)

        self.comboTyp = QComboBox(dialog)
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 3, 1, 1, 2)

        self.spinBeine = QSpinBox(dialog)
        self.spinBeine.setObjectName(u"spinBeine")
        self.spinBeine.setMinimumSize(QSize(50, 0))
        self.spinBeine.setMaximumSize(QSize(16777215, 16777215))
        self.spinBeine.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBeine.setMaximum(8)

        self.gridLayout.addWidget(self.spinBeine, 6, 2, 1, 1)

        self.label_4 = QLabel(dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 8, 1, 1, 1)

        self.spinKopf = QSpinBox(dialog)
        self.spinKopf.setObjectName(u"spinKopf")
        self.spinKopf.setMinimumSize(QSize(50, 0))
        self.spinKopf.setMaximumSize(QSize(16777215, 16777215))
        self.spinKopf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKopf.setMaximum(8)

        self.gridLayout.addWidget(self.spinKopf, 11, 2, 1, 1)

        self.label_5 = QLabel(dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 9, 1, 1, 1)

        self.spinBauch = QSpinBox(dialog)
        self.spinBauch.setObjectName(u"spinBauch")
        self.spinBauch.setMinimumSize(QSize(50, 0))
        self.spinBauch.setMaximumSize(QSize(16777215, 16777215))
        self.spinBauch.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBauch.setMaximum(8)

        self.gridLayout.addWidget(self.spinBauch, 9, 2, 1, 1)

        self.comboSystem = QComboBox(dialog)
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.addItem("")
        self.comboSystem.setObjectName(u"comboSystem")

        self.gridLayout.addWidget(self.comboSystem, 4, 1, 1, 2)

        self.label_2 = QLabel(dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 1, 1, 1)

        self.label_9 = QLabel(dialog)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)

        self.spinSchwert = QSpinBox(dialog)
        self.spinSchwert.setObjectName(u"spinSchwert")
        self.spinSchwert.setMinimumSize(QSize(50, 0))
        self.spinSchwert.setMaximumSize(QSize(16777215, 16777215))
        self.spinSchwert.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSchwert.setMaximum(8)

        self.gridLayout.addWidget(self.spinSchwert, 8, 2, 1, 1)

        self.labelRS = QLabel(dialog)
        self.labelRS.setObjectName(u"labelRS")

        self.gridLayout.addWidget(self.labelRS, 5, 2, 1, 1)

        self.label_11 = QLabel(dialog)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)

        self.warning = QLabel(dialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 3)

        self.label_8 = QLabel(dialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)

        self.label_3 = QLabel(dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 5, 1, 1, 1)

        self.tabWidget = QTabWidget(dialog)
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

        self.gridLayout.addWidget(self.tabWidget, 12, 1, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)

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
        self.label_7.setText(QCoreApplication.translate("dialog", u"Kopf", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.label_10.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"Brust", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Schwertarm", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Bauch", None))
        self.comboSystem.setItemText(0, QCoreApplication.translate("dialog", u"Beide R\u00fcstungssysteme", None))
        self.comboSystem.setItemText(1, QCoreApplication.translate("dialog", u"Einfaches R\u00fcstungssystem", None))
        self.comboSystem.setItemText(2, QCoreApplication.translate("dialog", u"Zonenr\u00fcstungssystem", None))

        self.label_2.setText(QCoreApplication.translate("dialog", u"Beine", None))
        self.label_9.setText(QCoreApplication.translate("dialog", u"Typ", None))
        self.labelRS.setText(QCoreApplication.translate("dialog", u"0", None))
        self.label_11.setText(QCoreApplication.translate("dialog", u"Verf\u00fcgbarkeit", None))
        self.warning.setText("")
        self.label_8.setText(QCoreApplication.translate("dialog", u"RS", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Schildarm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
    # retranslateUi

