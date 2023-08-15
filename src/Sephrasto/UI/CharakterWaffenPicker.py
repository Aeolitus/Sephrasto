# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterWaffenPicker.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
    QScrollArea, QSizePolicy, QSpacerItem, QSplitter,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

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
        self.filterLayout = QHBoxLayout()
        self.filterLayout.setObjectName(u"filterLayout")
        self.nameFilterEdit = QLineEdit(self.verticalLayout_2)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")
        self.nameFilterEdit.setClearButtonEnabled(True)

        self.filterLayout.addWidget(self.nameFilterEdit)

        self.labelFilter = QLabel(self.verticalLayout_2)
        self.labelFilter.setObjectName(u"labelFilter")

        self.filterLayout.addWidget(self.labelFilter)


        self.verticalLayout2.addLayout(self.filterLayout)

        self.treeWeapons = QTreeWidget(self.verticalLayout_2)
        self.treeWeapons.setObjectName(u"treeWeapons")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.treeWeapons.sizePolicy().hasHeightForWidth())
        self.treeWeapons.setSizePolicy(sizePolicy1)
        self.treeWeapons.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeWeapons.setProperty("showDropIndicator", False)
        self.treeWeapons.setAlternatingRowColors(True)
        self.treeWeapons.setSortingEnabled(False)
        self.treeWeapons.setAllColumnsShowFocus(True)
        self.treeWeapons.header().setVisible(True)
        self.treeWeapons.header().setCascadingSectionResizes(False)
        self.treeWeapons.header().setDefaultSectionSize(150)
        self.treeWeapons.header().setStretchLastSection(True)

        self.verticalLayout2.addWidget(self.treeWeapons)

        self.splitter.addWidget(self.verticalLayout_2)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setBold(False)
        self.scrollArea.setFont(font)
        self.scrollArea.setStyleSheet(u"padding: 1px")
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 407, 459))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelEigenschaften = QLabel(self.scrollAreaWidgetContents)
        self.labelEigenschaften.setObjectName(u"labelEigenschaften")
        self.labelEigenschaften.setWordWrap(True)

        self.gridLayout.addWidget(self.labelEigenschaften, 11, 0, 1, 2)

        self.labelFert = QLabel(self.scrollAreaWidgetContents)
        self.labelFert.setObjectName(u"labelFert")
        self.labelFert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.labelFert.setWordWrap(True)

        self.gridLayout.addWidget(self.labelFert, 2, 1, 1, 1)

        self.labelH = QLabel(self.scrollAreaWidgetContents)
        self.labelH.setObjectName(u"labelH")
        self.labelH.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelH, 10, 1, 1, 1)

        self.labelTalent = QLabel(self.scrollAreaWidgetContents)
        self.labelTalent.setObjectName(u"labelTalent")
        self.labelTalent.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.labelTalent.setWordWrap(True)

        self.gridLayout.addWidget(self.labelTalent, 3, 1, 1, 1)

        self.labelRW = QLabel(self.scrollAreaWidgetContents)
        self.labelRW.setObjectName(u"labelRW")
        self.labelRW.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelRW, 7, 1, 1, 1)

        self.labelKampfstile = QLabel(self.scrollAreaWidgetContents)
        self.labelKampfstile.setObjectName(u"labelKampfstile")
        self.labelKampfstile.setWordWrap(True)

        self.gridLayout.addWidget(self.labelKampfstile, 4, 0, 1, 2)

        self.labelTP = QLabel(self.scrollAreaWidgetContents)
        self.labelTP.setObjectName(u"labelTP")
        self.labelTP.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelTP, 6, 1, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        font1 = QFont()
        font1.setBold(True)
        self.labelName.setFont(font1)

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 5, 0, 1, 2)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 10, 0, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.labelWM = QLabel(self.scrollAreaWidgetContents)
        self.labelWM.setObjectName(u"labelWM")
        self.labelWM.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelWM, 8, 1, 1, 1)

        self.labelTyp = QLabel(self.scrollAreaWidgetContents)
        self.labelTyp.setObjectName(u"labelTyp")
        font2 = QFont()
        font2.setItalic(True)
        self.labelTyp.setFont(font2)
        self.labelTyp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelTyp, 1, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 12, 0, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.labelWM_Text = QLabel(self.scrollAreaWidgetContents)
        self.labelWM_Text.setObjectName(u"labelWM_Text")

        self.gridLayout.addWidget(self.labelWM_Text, 8, 0, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)

        self.labelLZ_Text = QLabel(self.scrollAreaWidgetContents)
        self.labelLZ_Text.setObjectName(u"labelLZ_Text")

        self.gridLayout.addWidget(self.labelLZ_Text, 9, 0, 1, 1)

        self.labelLZ = QLabel(self.scrollAreaWidgetContents)
        self.labelLZ.setObjectName(u"labelLZ")
        self.labelLZ.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelLZ, 9, 1, 1, 1)

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

        QWidget.setTabOrder(self.nameFilterEdit, self.treeWeapons)
        QWidget.setTabOrder(self.treeWeapons, self.scrollArea)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Sephrasto - Waffe w\u00e4hlen...", None))
        self.nameFilterEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Suchen...", None))
        self.labelFilter.setText(QCoreApplication.translate("Dialog", u"Suchen", None))
        self.labelFilter.setProperty("class", QCoreApplication.translate("Dialog", u"icon", None))
        ___qtreewidgetitem = self.treeWeapons.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Talent", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.labelEigenschaften.setText(QCoreApplication.translate("Dialog", u"Eigenschaften:", None))
        self.labelFert.setText(QCoreApplication.translate("Dialog", u"Hiebwaffen", None))
        self.labelH.setText(QCoreApplication.translate("Dialog", u"8", None))
        self.labelTalent.setText(QCoreApplication.translate("Dialog", u"Einhandhiebwaffen", None))
        self.labelRW.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.labelKampfstile.setText(QCoreApplication.translate("Dialog", u"Kampfstile:", None))
        self.labelTP.setText(QCoreApplication.translate("Dialog", u"2W6+2", None))
        self.labelName.setText(QCoreApplication.translate("Dialog", u"Brabakbengel", None))
        self.labelName.setProperty("class", QCoreApplication.translate("Dialog", u"h4", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Trefferpunkte:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"H\u00e4rte:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Talent:", None))
        self.labelWM.setText(QCoreApplication.translate("Dialog", u"-1", None))
        self.labelTyp.setText(QCoreApplication.translate("Dialog", u"Nahkampfwaffe", None))
        self.labelTyp.setProperty("class", QCoreApplication.translate("Dialog", u"italic", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Fertigkeit:", None))
        self.labelWM_Text.setText(QCoreApplication.translate("Dialog", u"Waffenmodifikator:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Reichweite:", None))
        self.labelLZ_Text.setText(QCoreApplication.translate("Dialog", u"Ladezeit:", None))
        self.labelLZ.setText(QCoreApplication.translate("Dialog", u"0", None))
    # retranslateUi

