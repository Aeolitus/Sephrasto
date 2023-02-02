# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditRuestung.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
    QSizePolicy, QSpacerItem, QSpinBox, QTextEdit,
    QWidget)

class Ui_talentDialog(object):
    def setupUi(self, talentDialog):
        if not talentDialog.objectName():
            talentDialog.setObjectName(u"talentDialog")
        talentDialog.setWindowModality(Qt.ApplicationModal)
        talentDialog.resize(441, 434)
        self.gridLayout_2 = QGridLayout(talentDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.sbKopf = QSpinBox(talentDialog)
        self.sbKopf.setObjectName(u"sbKopf")
        self.sbKopf.setMinimumSize(QSize(50, 0))
        self.sbKopf.setMaximumSize(QSize(16777215, 16777215))
        self.sbKopf.setMaximum(8)

        self.gridLayout.addWidget(self.sbKopf, 11, 2, 1, 1)

        self.sbBeine = QSpinBox(talentDialog)
        self.sbBeine.setObjectName(u"sbBeine")
        self.sbBeine.setMinimumSize(QSize(50, 0))
        self.sbBeine.setMaximumSize(QSize(16777215, 16777215))
        self.sbBeine.setMaximum(8)

        self.gridLayout.addWidget(self.sbBeine, 6, 2, 1, 1)

        self.warning = QLabel(talentDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 3)

        self.label_7 = QLabel(talentDialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 11, 1, 1, 1)

        self.sbBauch = QSpinBox(talentDialog)
        self.sbBauch.setObjectName(u"sbBauch")
        self.sbBauch.setMinimumSize(QSize(50, 0))
        self.sbBauch.setMaximumSize(QSize(16777215, 16777215))
        self.sbBauch.setMaximum(8)

        self.gridLayout.addWidget(self.sbBauch, 9, 2, 1, 1)

        self.label_3 = QLabel(talentDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 1, 1, 1)

        self.sbSchild = QSpinBox(talentDialog)
        self.sbSchild.setObjectName(u"sbSchild")
        self.sbSchild.setMinimumSize(QSize(50, 0))
        self.sbSchild.setMaximumSize(QSize(16777215, 16777215))
        self.sbSchild.setMaximum(8)

        self.gridLayout.addWidget(self.sbSchild, 7, 2, 1, 1)

        self.label = QLabel(talentDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.leName = QLineEdit(talentDialog)
        self.leName.setObjectName(u"leName")
        self.leName.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.leName, 2, 1, 1, 2)

        self.label_5 = QLabel(talentDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 9, 1, 1, 1)

        self.sbSchwert = QSpinBox(talentDialog)
        self.sbSchwert.setObjectName(u"sbSchwert")
        self.sbSchwert.setMinimumSize(QSize(50, 0))
        self.sbSchwert.setMaximumSize(QSize(16777215, 16777215))
        self.sbSchwert.setMaximum(8)

        self.gridLayout.addWidget(self.sbSchwert, 8, 2, 1, 1)

        self.sbBrust = QSpinBox(talentDialog)
        self.sbBrust.setObjectName(u"sbBrust")
        self.sbBrust.setMinimumSize(QSize(50, 0))
        self.sbBrust.setMaximumSize(QSize(16777215, 16777215))
        self.sbBrust.setMaximum(8)

        self.gridLayout.addWidget(self.sbBrust, 10, 2, 1, 1)

        self.label_8 = QLabel(talentDialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)

        self.label_2 = QLabel(talentDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 1, 1, 1)

        self.label_9 = QLabel(talentDialog)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)

        self.label_4 = QLabel(talentDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 8, 1, 1, 1)

        self.lblRS = QLabel(talentDialog)
        self.lblRS.setObjectName(u"lblRS")

        self.gridLayout.addWidget(self.lblRS, 5, 2, 1, 1)

        self.label_6 = QLabel(talentDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 10, 1, 1, 1)

        self.cbTyp = QComboBox(talentDialog)
        self.cbTyp.setObjectName(u"cbTyp")

        self.gridLayout.addWidget(self.cbTyp, 3, 1, 1, 2)

        self.label_10 = QLabel(talentDialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 12, 0, 1, 1)

        self.teBeschreibung = QTextEdit(talentDialog)
        self.teBeschreibung.setObjectName(u"teBeschreibung")

        self.gridLayout.addWidget(self.teBeschreibung, 12, 1, 1, 2)

        self.label_11 = QLabel(talentDialog)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)

        self.cbSystem = QComboBox(talentDialog)
        self.cbSystem.addItem("")
        self.cbSystem.addItem("")
        self.cbSystem.addItem("")
        self.cbSystem.setObjectName(u"cbSystem")

        self.gridLayout.addWidget(self.cbSystem, 4, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 5, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(talentDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.cbTyp)
        QWidget.setTabOrder(self.cbTyp, self.cbSystem)
        QWidget.setTabOrder(self.cbSystem, self.sbBeine)
        QWidget.setTabOrder(self.sbBeine, self.sbSchild)
        QWidget.setTabOrder(self.sbSchild, self.sbSchwert)
        QWidget.setTabOrder(self.sbSchwert, self.sbBauch)
        QWidget.setTabOrder(self.sbBauch, self.sbBrust)
        QWidget.setTabOrder(self.sbBrust, self.sbKopf)
        QWidget.setTabOrder(self.sbKopf, self.teBeschreibung)

        self.retranslateUi(talentDialog)
        self.buttonBox.accepted.connect(talentDialog.accept)
        self.buttonBox.rejected.connect(talentDialog.reject)

        QMetaObject.connectSlotsByName(talentDialog)
    # setupUi

    def retranslateUi(self, talentDialog):
        talentDialog.setWindowTitle(QCoreApplication.translate("talentDialog", u"Sephrasto - R\u00fcstung bearbeiten...", None))
        self.warning.setText(QCoreApplication.translate("talentDialog", u"<html><head/><body><p>Dies ist eine Ilaris-Standardr\u00fcstung. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr diese R\u00fcstung keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("talentDialog", u"Kopf", None))
        self.label_3.setText(QCoreApplication.translate("talentDialog", u"Schildarm", None))
        self.label.setText(QCoreApplication.translate("talentDialog", u"Name", None))
        self.label_5.setText(QCoreApplication.translate("talentDialog", u"Bauch", None))
        self.label_8.setText(QCoreApplication.translate("talentDialog", u"RS", None))
        self.label_2.setText(QCoreApplication.translate("talentDialog", u"Beine", None))
        self.label_9.setText(QCoreApplication.translate("talentDialog", u"Typ", None))
        self.label_4.setText(QCoreApplication.translate("talentDialog", u"Schwertarm", None))
        self.lblRS.setText(QCoreApplication.translate("talentDialog", u"0", None))
        self.label_6.setText(QCoreApplication.translate("talentDialog", u"Brust", None))
        self.label_10.setText(QCoreApplication.translate("talentDialog", u"Beschreibung", None))
        self.label_11.setText(QCoreApplication.translate("talentDialog", u"Verf\u00fcgbarkeit", None))
        self.cbSystem.setItemText(0, QCoreApplication.translate("talentDialog", u"Beide R\u00fcstungssysteme", None))
        self.cbSystem.setItemText(1, QCoreApplication.translate("talentDialog", u"Einfaches R\u00fcstungssystem", None))
        self.cbSystem.setItemText(2, QCoreApplication.translate("talentDialog", u"Zonenr\u00fcstungssystem", None))

    # retranslateUi

