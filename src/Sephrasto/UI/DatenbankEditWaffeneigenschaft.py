# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditWaffeneigenschaft.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPlainTextEdit, QSizePolicy, QSpinBox, QWidget)

class Ui_waffeneigenschaftDialog(object):
    def setupUi(self, waffeneigenschaftDialog):
        if not waffeneigenschaftDialog.objectName():
            waffeneigenschaftDialog.setObjectName(u"waffeneigenschaftDialog")
        waffeneigenschaftDialog.setWindowModality(Qt.ApplicationModal)
        waffeneigenschaftDialog.resize(440, 334)
        self.gridLayout_2 = QGridLayout(waffeneigenschaftDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(waffeneigenschaftDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.nameEdit = QLineEdit(waffeneigenschaftDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.textEdit = QPlainTextEdit(waffeneigenschaftDialog)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.textEdit, 2, 1, 1, 1)

        self.label_5 = QLabel(waffeneigenschaftDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scriptEdit = QLineEdit(waffeneigenschaftDialog)
        self.scriptEdit.setObjectName(u"scriptEdit")

        self.horizontalLayout.addWidget(self.scriptEdit)

        self.scriptPrioEdit = QSpinBox(waffeneigenschaftDialog)
        self.scriptPrioEdit.setObjectName(u"scriptPrioEdit")
        self.scriptPrioEdit.setMinimum(-10)
        self.scriptPrioEdit.setMaximum(10)
        self.scriptPrioEdit.setSingleStep(1)
        self.scriptPrioEdit.setValue(0)

        self.horizontalLayout.addWidget(self.scriptPrioEdit)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.warning = QLabel(waffeneigenschaftDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.label = QLabel(waffeneigenschaftDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(waffeneigenschaftDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.nameEdit, self.textEdit)

        self.retranslateUi(waffeneigenschaftDialog)
        self.buttonBox.accepted.connect(waffeneigenschaftDialog.accept)
        self.buttonBox.rejected.connect(waffeneigenschaftDialog.reject)

        QMetaObject.connectSlotsByName(waffeneigenschaftDialog)
    # setupUi

    def retranslateUi(self, waffeneigenschaftDialog):
        waffeneigenschaftDialog.setWindowTitle(QCoreApplication.translate("waffeneigenschaftDialog", u"Sephrasto - Waffeneigenschaft bearbeiten...", None))
        self.label_3.setText(QCoreApplication.translate("waffeneigenschaftDialog", u"Script / Priorit\u00e4t", None))
        self.label_5.setText(QCoreApplication.translate("waffeneigenschaftDialog", u"Beschreibung", None))
        self.warning.setText(QCoreApplication.translate("waffeneigenschaftDialog", u"<html><head/><body><p>Dies ist eine Ilaris-Standardwaffeneigenschaft. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr diese Waffeneigenschaft keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("waffeneigenschaftDialog", u"Name", None))
    # retranslateUi

