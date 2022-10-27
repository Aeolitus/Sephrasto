# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterTalentPicker.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLineEdit, QListView, QPlainTextEdit, QScrollArea,
    QSizePolicy, QSpinBox, QSplitter, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(928, 522)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.listTalente = QListView(self.splitter)
        self.listTalente.setObjectName(u"listTalente")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listTalente.sizePolicy().hasHeightForWidth())
        self.listTalente.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.listTalente)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setStyleSheet(u"padding: 1px")
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 467, 459))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.spinKosten = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKosten.setObjectName(u"spinKosten")
        self.spinKosten.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinKosten.setReadOnly(True)
        self.spinKosten.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinKosten.setMinimum(0)
        self.spinKosten.setMaximum(8000)
        self.spinKosten.setSingleStep(20)

        self.gridLayout_2.addWidget(self.spinKosten, 1, 1, 1, 1)

        self.labelKommentar = QLabel(self.scrollAreaWidgetContents)
        self.labelKommentar.setObjectName(u"labelKommentar")

        self.gridLayout_2.addWidget(self.labelKommentar, 3, 0, 1, 1)

        self.textKommentar = QLineEdit(self.scrollAreaWidgetContents)
        self.textKommentar.setObjectName(u"textKommentar")

        self.gridLayout_2.addWidget(self.textKommentar, 3, 1, 1, 1)

        self.plainText = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainText.setObjectName(u"plainText")
        self.plainText.setFrameShape(QFrame.StyledPanel)
        self.plainText.setReadOnly(True)

        self.gridLayout_2.addWidget(self.plainText, 4, 0, 1, 2)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setBold(True)
        self.labelName.setFont(font)

        self.gridLayout_2.addWidget(self.labelName, 0, 0, 1, 2)

        self.labelInfo = QLabel(self.scrollAreaWidgetContents)
        self.labelInfo.setObjectName(u"labelInfo")
        self.labelInfo.setMinimumSize(QSize(0, 18))
        font1 = QFont()
        font1.setItalic(True)
        self.labelInfo.setFont(font1)

        self.gridLayout_2.addWidget(self.labelInfo, 2, 0, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMaximumSize(QSize(16777215, 16777215))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        QWidget.setTabOrder(self.listTalente, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.spinKosten)
        QWidget.setTabOrder(self.spinKosten, self.textKommentar)
        QWidget.setTabOrder(self.textKommentar, self.plainText)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Sephrasto - Talente w\u00e4hlen...", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Kosten:", None))
        self.spinKosten.setSuffix(QCoreApplication.translate("Dialog", u" EP", None))
        self.labelKommentar.setText(QCoreApplication.translate("Dialog", u"Kommentar:", None))
        self.labelName.setText(QCoreApplication.translate("Dialog", u"Talentname", None))
        self.labelName.setProperty("class", QCoreApplication.translate("Dialog", u"h4", None))
        self.labelInfo.setText(QCoreApplication.translate("Dialog", u"Spezialtalent", None))
        self.labelInfo.setProperty("class", QCoreApplication.translate("Dialog", u"italic", None))
    # retranslateUi

