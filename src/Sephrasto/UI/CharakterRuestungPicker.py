# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterRuestungPicker.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPlainTextEdit, QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(928, 522)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayout_2 = QWidget(self.splitter)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLayout_2.sizePolicy().hasHeightForWidth())
        self.verticalLayout_2.setSizePolicy(sizePolicy)
        self.verticalLayout2 = QVBoxLayout(self.verticalLayout_2)
        self.verticalLayout2.setObjectName(u"verticalLayout2")
        self.label = QLabel(self.verticalLayout_2)
        self.label.setObjectName(u"label")
        self.label.setInputMethodHints(Qt.ImhNone)
        self.label.setWordWrap(True)

        self.verticalLayout2.addWidget(self.label)

        self.filterLayout = QHBoxLayout()
        self.filterLayout.setObjectName(u"filterLayout")
        self.labelFilter = QLabel(self.verticalLayout_2)
        self.labelFilter.setObjectName(u"labelFilter")

        self.filterLayout.addWidget(self.labelFilter)

        self.nameFilterEdit = QLineEdit(self.verticalLayout_2)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")

        self.filterLayout.addWidget(self.nameFilterEdit)


        self.verticalLayout2.addLayout(self.filterLayout)

        self.treeArmors = QTreeWidget(self.verticalLayout_2)
        self.treeArmors.setObjectName(u"treeArmors")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.treeArmors.sizePolicy().hasHeightForWidth())
        self.treeArmors.setSizePolicy(sizePolicy1)
        self.treeArmors.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeArmors.setProperty("showDropIndicator", False)
        self.treeArmors.setAlternatingRowColors(True)
        self.treeArmors.setSortingEnabled(False)
        self.treeArmors.setAllColumnsShowFocus(True)
        self.treeArmors.header().setVisible(True)
        self.treeArmors.header().setCascadingSectionResizes(False)
        self.treeArmors.header().setDefaultSectionSize(150)
        self.treeArmors.header().setStretchLastSection(True)

        self.verticalLayout2.addWidget(self.treeArmors)

        self.splitter.addWidget(self.verticalLayout_2)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(220, 0))
        font = QFont()
        font.setBold(False)
        self.scrollArea.setFont(font)
        self.scrollArea.setStyleSheet(u"padding: 1px")
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 449, 459))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblKopf = QLabel(self.scrollAreaWidgetContents)
        self.lblKopf.setObjectName(u"lblKopf")
        self.lblKopf.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblKopf, 12, 1, 1, 1)

        self.lblBrustL = QLabel(self.scrollAreaWidgetContents)
        self.lblBrustL.setObjectName(u"lblBrustL")

        self.gridLayout.addWidget(self.lblBrustL, 11, 0, 1, 1)

        self.lblBeine = QLabel(self.scrollAreaWidgetContents)
        self.lblBeine.setObjectName(u"lblBeine")
        self.lblBeine.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblBeine, 7, 1, 1, 1)

        self.lblBauchL = QLabel(self.scrollAreaWidgetContents)
        self.lblBauchL.setObjectName(u"lblBauchL")

        self.gridLayout.addWidget(self.lblBauchL, 10, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 16, 1, 1, 1)

        self.lblSchild = QLabel(self.scrollAreaWidgetContents)
        self.lblSchild.setObjectName(u"lblSchild")
        self.lblSchild.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblSchild, 9, 1, 1, 1)

        self.lblName = QLabel(self.scrollAreaWidgetContents)
        self.lblName.setObjectName(u"lblName")
        font1 = QFont()
        font1.setBold(True)
        self.lblName.setFont(font1)

        self.gridLayout.addWidget(self.lblName, 0, 0, 1, 2)

        self.lblTyp = QLabel(self.scrollAreaWidgetContents)
        self.lblTyp.setObjectName(u"lblTyp")

        self.gridLayout.addWidget(self.lblTyp, 1, 0, 1, 2)

        self.lblBauch = QLabel(self.scrollAreaWidgetContents)
        self.lblBauch.setObjectName(u"lblBauch")
        self.lblBauch.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblBauch, 10, 1, 1, 1)

        self.lblKopfL = QLabel(self.scrollAreaWidgetContents)
        self.lblKopfL.setObjectName(u"lblKopfL")

        self.gridLayout.addWidget(self.lblKopfL, 12, 0, 1, 1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 5, 0, 1, 2)

        self.lblZRS = QLabel(self.scrollAreaWidgetContents)
        self.lblZRS.setObjectName(u"lblZRS")
        self.lblZRS.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblZRS, 14, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.lblBrust = QLabel(self.scrollAreaWidgetContents)
        self.lblBrust.setObjectName(u"lblBrust")
        self.lblBrust.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblBrust, 11, 1, 1, 1)

        self.lblSchildL = QLabel(self.scrollAreaWidgetContents)
        self.lblSchildL.setObjectName(u"lblSchildL")

        self.gridLayout.addWidget(self.lblSchildL, 9, 0, 1, 1)

        self.lblBeineL = QLabel(self.scrollAreaWidgetContents)
        self.lblBeineL.setObjectName(u"lblBeineL")
        self.lblBeineL.setFont(font)

        self.gridLayout.addWidget(self.lblBeineL, 7, 0, 1, 1)

        self.lblSchwert = QLabel(self.scrollAreaWidgetContents)
        self.lblSchwert.setObjectName(u"lblSchwert")
        self.lblSchwert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblSchwert, 8, 1, 1, 1)

        self.lblSchwertL = QLabel(self.scrollAreaWidgetContents)
        self.lblSchwertL.setObjectName(u"lblSchwertL")

        self.gridLayout.addWidget(self.lblSchwertL, 8, 0, 1, 1)

        self.lblRS = QLabel(self.scrollAreaWidgetContents)
        self.lblRS.setObjectName(u"lblRS")
        self.lblRS.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblRS, 3, 1, 1, 1)

        self.teBeschreibung = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teBeschreibung.setObjectName(u"teBeschreibung")
        self.teBeschreibung.setReadOnly(True)

        self.gridLayout.addWidget(self.teBeschreibung, 15, 0, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        self.splitter.addWidget(self.layoutWidget)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nameFilterEdit, self.treeArmors)
        QWidget.setTabOrder(self.treeArmors, self.scrollArea)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Sephrasto - R\u00fcstung w\u00e4hlen...", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Inoffiziell: Bei den hier aufgelisteten R\u00fcstungen handelt es sich um an WdS orientierte Vorschl\u00e4ge. Die Festlegung des RS einer R\u00fcstung obliegt am Ende dem Spielleiter.", None))
        self.labelFilter.setText(QCoreApplication.translate("Dialog", u"Suchen:", None))
        ___qtreewidgetitem = self.treeArmors.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.lblKopf.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblBrustL.setText(QCoreApplication.translate("Dialog", u"Brust", None))
        self.lblBeine.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblBauchL.setText(QCoreApplication.translate("Dialog", u"Bauch", None))
        self.lblSchild.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblName.setText(QCoreApplication.translate("Dialog", u"Kettenhemd", None))
        self.lblName.setProperty("class", QCoreApplication.translate("Dialog", u"h4", None))
        self.lblTyp.setText(QCoreApplication.translate("Dialog", u"Kettenr\u00fcstung", None))
        self.lblTyp.setProperty("class", QCoreApplication.translate("Dialog", u"italic", None))
        self.lblBauch.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblKopfL.setText(QCoreApplication.translate("Dialog", u"Kopf", None))
        self.lblZRS.setText(QCoreApplication.translate("Dialog", u"= 0", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"RS / BE", None))
        self.lblBrust.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblSchildL.setText(QCoreApplication.translate("Dialog", u"Schildarm", None))
        self.lblBeineL.setText(QCoreApplication.translate("Dialog", u"Beine", None))
        self.lblSchwert.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblSchwertL.setText(QCoreApplication.translate("Dialog", u"Schwertarm", None))
        self.lblRS.setText(QCoreApplication.translate("Dialog", u"0", None))
    # retranslateUi

