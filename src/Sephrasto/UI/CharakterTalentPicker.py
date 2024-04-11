# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterTalentPicker.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLineEdit, QListView, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QSplitter, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(758, 522)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.listTalente = QListView(self.splitter)
        self.listTalente.setObjectName(u"listTalente")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 378, 436))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelKommentar = QLabel(self.scrollAreaWidgetContents)
        self.labelKommentar.setObjectName(u"labelKommentar")

        self.gridLayout_2.addWidget(self.labelKommentar, 8, 0, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setBold(True)
        self.labelName.setFont(font)

        self.gridLayout_2.addWidget(self.labelName, 5, 0, 1, 2)

        self.spinKosten = QSpinBox(self.scrollAreaWidgetContents)
        self.spinKosten.setObjectName(u"spinKosten")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinKosten.sizePolicy().hasHeightForWidth())
        self.spinKosten.setSizePolicy(sizePolicy1)
        self.spinKosten.setMaximumSize(QSize(80, 16777215))
        self.spinKosten.setLayoutDirection(Qt.LeftToRight)
        self.spinKosten.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinKosten.setReadOnly(True)
        self.spinKosten.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinKosten.setMinimum(0)
        self.spinKosten.setMaximum(9999)
        self.spinKosten.setSingleStep(20)

        self.gridLayout_2.addWidget(self.spinKosten, 6, 2, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 6, 0, 1, 1)

        self.plainText = QTextBrowser(self.scrollAreaWidgetContents)
        self.plainText.setObjectName(u"plainText")
        self.plainText.setFrameShape(QFrame.StyledPanel)

        self.gridLayout_2.addWidget(self.plainText, 9, 0, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 6, 1, 1, 1)

        self.textKommentar = QLineEdit(self.scrollAreaWidgetContents)
        self.textKommentar.setObjectName(u"textKommentar")

        self.gridLayout_2.addWidget(self.textKommentar, 8, 1, 1, 2)

        self.labelInfo = QLabel(self.scrollAreaWidgetContents)
        self.labelInfo.setObjectName(u"labelInfo")
        self.labelInfo.setMinimumSize(QSize(0, 18))
        font1 = QFont()
        font1.setItalic(True)
        self.labelInfo.setFont(font1)
        self.labelInfo.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelInfo, 5, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 10, 0, 1, 1)

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

        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        self.labelTip = QLabel(Dialog)
        self.labelTip.setObjectName(u"labelTip")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelTip.sizePolicy().hasHeightForWidth())
        self.labelTip.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.labelTip, 0, 0, 1, 1)

        QWidget.setTabOrder(self.listTalente, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.textKommentar)
        QWidget.setTabOrder(self.textKommentar, self.plainText)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Sephrasto - Talente w\u00e4hlen...", None))
        self.labelKommentar.setText(QCoreApplication.translate("Dialog", u"Kommentar:", None))
        self.labelName.setText(QCoreApplication.translate("Dialog", u"Talentname", None))
        self.labelName.setProperty("class", QCoreApplication.translate("Dialog", u"h4", None))
        self.spinKosten.setSuffix(QCoreApplication.translate("Dialog", u" EP", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Kosten:", None))
        self.labelInfo.setText(QCoreApplication.translate("Dialog", u"Spezialtalent", None))
        self.labelInfo.setProperty("class", QCoreApplication.translate("Dialog", u"italic", None))
        self.labelTip.setText(QCoreApplication.translate("Dialog", u"Ein Talent lohnt sich ab...", None))
    # retranslateUi

