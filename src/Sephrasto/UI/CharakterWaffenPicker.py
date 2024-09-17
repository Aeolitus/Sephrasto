# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterWaffenPicker.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QDialogButtonBox, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(742, 522)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayout_2 = QWidget(self.splitter)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLayout_2.sizePolicy().hasHeightForWidth())
        self.verticalLayout_2.setSizePolicy(sizePolicy)
        self.verticalLayout2 = QVBoxLayout(self.verticalLayout_2)
        self.verticalLayout2.setObjectName(u"verticalLayout2")
        self.filterLayout = QHBoxLayout()
        self.filterLayout.setObjectName(u"filterLayout")
        self.buttonExpandToggle = QPushButton(self.verticalLayout_2)
        self.buttonExpandToggle.setObjectName(u"buttonExpandToggle")

        self.filterLayout.addWidget(self.buttonExpandToggle)

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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 326, 459))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        font1 = QFont()
        font1.setBold(True)
        self.labelName.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)

        self.labelTyp = QLabel(self.scrollAreaWidgetContents)
        self.labelTyp.setObjectName(u"labelTyp")
        font2 = QFont()
        font2.setItalic(True)
        self.labelTyp.setFont(font2)
        self.labelTyp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelTyp)

        self.labelFertigkeit = QLabel(self.scrollAreaWidgetContents)
        self.labelFertigkeit.setObjectName(u"labelFertigkeit")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelFertigkeit)

        self.labelFertigkeitWert = QLabel(self.scrollAreaWidgetContents)
        self.labelFertigkeitWert.setObjectName(u"labelFertigkeitWert")
        self.labelFertigkeitWert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.labelFertigkeitWert.setWordWrap(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.labelFertigkeitWert)

        self.labelTalent = QLabel(self.scrollAreaWidgetContents)
        self.labelTalent.setObjectName(u"labelTalent")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelTalent)

        self.labelTalentWert = QLabel(self.scrollAreaWidgetContents)
        self.labelTalentWert.setObjectName(u"labelTalentWert")
        self.labelTalentWert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.labelTalentWert.setWordWrap(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.labelTalentWert)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.line)

        self.labelTP = QLabel(self.scrollAreaWidgetContents)
        self.labelTP.setObjectName(u"labelTP")
        self.labelTP.setFont(font)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelTP)

        self.labelTPWert = QLabel(self.scrollAreaWidgetContents)
        self.labelTPWert.setObjectName(u"labelTPWert")
        self.labelTPWert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.labelTPWert)

        self.labelRW = QLabel(self.scrollAreaWidgetContents)
        self.labelRW.setObjectName(u"labelRW")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelRW)

        self.labelRWWert = QLabel(self.scrollAreaWidgetContents)
        self.labelRWWert.setObjectName(u"labelRWWert")
        self.labelRWWert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.labelRWWert)

        self.labelWM = QLabel(self.scrollAreaWidgetContents)
        self.labelWM.setObjectName(u"labelWM")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.labelWM)

        self.labelWMWert = QLabel(self.scrollAreaWidgetContents)
        self.labelWMWert.setObjectName(u"labelWMWert")
        self.labelWMWert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.labelWMWert)

        self.labelLZ = QLabel(self.scrollAreaWidgetContents)
        self.labelLZ.setObjectName(u"labelLZ")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.labelLZ)

        self.labelLZWert = QLabel(self.scrollAreaWidgetContents)
        self.labelLZWert.setObjectName(u"labelLZWert")
        self.labelLZWert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.labelLZWert)

        self.labelHaerte = QLabel(self.scrollAreaWidgetContents)
        self.labelHaerte.setObjectName(u"labelHaerte")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.labelHaerte)

        self.labelHaerteWert = QLabel(self.scrollAreaWidgetContents)
        self.labelHaerteWert.setObjectName(u"labelHaerteWert")
        self.labelHaerteWert.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.labelHaerteWert)

        self.labelEigenschaften = QLabel(self.scrollAreaWidgetContents)
        self.labelEigenschaften.setObjectName(u"labelEigenschaften")
        self.labelEigenschaften.setWordWrap(True)

        self.formLayout.setWidget(11, QFormLayout.SpanningRole, self.labelEigenschaften)

        self.labelKampfstile = QLabel(self.scrollAreaWidgetContents)
        self.labelKampfstile.setObjectName(u"labelKampfstile")
        self.labelKampfstile.setWordWrap(True)

        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.labelKampfstile)

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
        self.buttonExpandToggle.setText(QCoreApplication.translate("Dialog", u"Expand Toggle", None))
        self.buttonExpandToggle.setProperty("class", QCoreApplication.translate("Dialog", u"icon", None))
        self.nameFilterEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Suchen...", None))
        self.labelFilter.setText(QCoreApplication.translate("Dialog", u"Suchen", None))
        self.labelFilter.setProperty("class", QCoreApplication.translate("Dialog", u"icon", None))
        ___qtreewidgetitem = self.treeWeapons.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Talent", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.labelName.setText(QCoreApplication.translate("Dialog", u"Brabakbengel", None))
        self.labelName.setProperty("class", QCoreApplication.translate("Dialog", u"h4", None))
        self.labelTyp.setText(QCoreApplication.translate("Dialog", u"Nahkampfwaffe", None))
        self.labelTyp.setProperty("class", QCoreApplication.translate("Dialog", u"italic", None))
        self.labelFertigkeit.setText(QCoreApplication.translate("Dialog", u"Fertigkeit:", None))
        self.labelFertigkeitWert.setText(QCoreApplication.translate("Dialog", u"Hiebwaffen", None))
        self.labelTalent.setText(QCoreApplication.translate("Dialog", u"Talent:", None))
        self.labelTalentWert.setText(QCoreApplication.translate("Dialog", u"Einhandhiebwaffen", None))
        self.labelTP.setText(QCoreApplication.translate("Dialog", u"Trefferpunkte:", None))
        self.labelTPWert.setText(QCoreApplication.translate("Dialog", u"2W6+2", None))
        self.labelRW.setText(QCoreApplication.translate("Dialog", u"Reichweite:", None))
        self.labelRWWert.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.labelWM.setText(QCoreApplication.translate("Dialog", u"Waffenmodifikator:", None))
        self.labelWMWert.setText(QCoreApplication.translate("Dialog", u"-1", None))
        self.labelLZ.setText(QCoreApplication.translate("Dialog", u"Ladezeit:", None))
        self.labelLZWert.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.labelHaerte.setText(QCoreApplication.translate("Dialog", u"H\u00e4rte:", None))
        self.labelHaerteWert.setText(QCoreApplication.translate("Dialog", u"8", None))
        self.labelEigenschaften.setText(QCoreApplication.translate("Dialog", u"Eigenschaften:", None))
        self.labelKampfstile.setText(QCoreApplication.translate("Dialog", u"Kampfstile:", None))
    # retranslateUi

