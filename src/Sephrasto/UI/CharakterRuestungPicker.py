# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterRuestungPicker.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
    QSpacerItem, QSplitter, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        Dialog.resize(928, 522)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.verticalLayout_2 = QWidget(self.splitter)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLayout_2.sizePolicy().hasHeightForWidth())
        self.verticalLayout_2.setSizePolicy(sizePolicy)
        self.verticalLayout2 = QVBoxLayout(self.verticalLayout_2)
        self.verticalLayout2.setObjectName(u"verticalLayout2")
        self.labelUnofficial = QLabel(self.verticalLayout_2)
        self.labelUnofficial.setObjectName(u"labelUnofficial")
        self.labelUnofficial.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.labelUnofficial.setWordWrap(True)

        self.verticalLayout2.addWidget(self.labelUnofficial)

        self.filterLayout = QHBoxLayout()
        self.filterLayout.setObjectName(u"filterLayout")
        self.buttonExpandToggle = QPushButton(self.verticalLayout_2)
        self.buttonExpandToggle.setObjectName(u"buttonExpandToggle")
        font = QFont()
        font.setHintingPreference(QFont.PreferNoHinting)
        self.buttonExpandToggle.setFont(font)

        self.filterLayout.addWidget(self.buttonExpandToggle)

        self.nameFilterEdit = QLineEdit(self.verticalLayout_2)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")
        self.nameFilterEdit.setClearButtonEnabled(True)

        self.filterLayout.addWidget(self.nameFilterEdit)

        self.labelFilter = QLabel(self.verticalLayout_2)
        self.labelFilter.setObjectName(u"labelFilter")
        self.labelFilter.setFont(font)

        self.filterLayout.addWidget(self.labelFilter)


        self.verticalLayout2.addLayout(self.filterLayout)

        self.treeArmors = QTreeWidget(self.verticalLayout_2)
        self.treeArmors.setObjectName(u"treeArmors")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.treeArmors.sizePolicy().hasHeightForWidth())
        self.treeArmors.setSizePolicy(sizePolicy1)
        self.treeArmors.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeArmors.setProperty(u"showDropIndicator", False)
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
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(220, 0))
        font1 = QFont()
        font1.setBold(False)
        self.scrollArea.setFont(font1)
        self.scrollArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 405, 460))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.lblName = QLabel(self.scrollAreaWidgetContents)
        self.lblName.setObjectName(u"lblName")
        font2 = QFont()
        font2.setBold(True)
        self.lblName.setFont(font2)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblName)

        self.lblTyp = QLabel(self.scrollAreaWidgetContents)
        self.lblTyp.setObjectName(u"lblTyp")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblTyp)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.lblRS = QLabel(self.scrollAreaWidgetContents)
        self.lblRS.setObjectName(u"lblRS")
        self.lblRS.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lblRS)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.line)

        self.lblBeineL = QLabel(self.scrollAreaWidgetContents)
        self.lblBeineL.setObjectName(u"lblBeineL")
        self.lblBeineL.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblBeineL)

        self.lblBeine = QLabel(self.scrollAreaWidgetContents)
        self.lblBeine.setObjectName(u"lblBeine")
        self.lblBeine.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lblBeine)

        self.lblSchwertL = QLabel(self.scrollAreaWidgetContents)
        self.lblSchwertL.setObjectName(u"lblSchwertL")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lblSchwertL)

        self.lblSchwert = QLabel(self.scrollAreaWidgetContents)
        self.lblSchwert.setObjectName(u"lblSchwert")
        self.lblSchwert.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lblSchwert)

        self.lblSchildL = QLabel(self.scrollAreaWidgetContents)
        self.lblSchildL.setObjectName(u"lblSchildL")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.lblSchildL)

        self.lblSchild = QLabel(self.scrollAreaWidgetContents)
        self.lblSchild.setObjectName(u"lblSchild")
        self.lblSchild.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lblSchild)

        self.lblBauchL = QLabel(self.scrollAreaWidgetContents)
        self.lblBauchL.setObjectName(u"lblBauchL")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.lblBauchL)

        self.lblBauch = QLabel(self.scrollAreaWidgetContents)
        self.lblBauch.setObjectName(u"lblBauch")
        self.lblBauch.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.lblBauch)

        self.lblBrustL = QLabel(self.scrollAreaWidgetContents)
        self.lblBrustL.setObjectName(u"lblBrustL")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.lblBrustL)

        self.lblBrust = QLabel(self.scrollAreaWidgetContents)
        self.lblBrust.setObjectName(u"lblBrust")
        self.lblBrust.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.lblBrust)

        self.lblKopfL = QLabel(self.scrollAreaWidgetContents)
        self.lblKopfL.setObjectName(u"lblKopfL")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.lblKopfL)

        self.lblKopf = QLabel(self.scrollAreaWidgetContents)
        self.lblKopf.setObjectName(u"lblKopf")
        self.lblKopf.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.lblKopf)

        self.lblZRS = QLabel(self.scrollAreaWidgetContents)
        self.lblZRS.setObjectName(u"lblZRS")
        self.lblZRS.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.lblZRS)

        self.teBeschreibung = QTextBrowser(self.scrollAreaWidgetContents)
        self.teBeschreibung.setObjectName(u"teBeschreibung")

        self.formLayout.setWidget(11, QFormLayout.SpanningRole, self.teBeschreibung)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(12, QFormLayout.FieldRole, self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
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
        self.labelUnofficial.setText(QCoreApplication.translate("Dialog", u"Inoffiziell: Bei den hier aufgelisteten R\u00fcstungen handelt es sich um an WdS orientierte Vorschl\u00e4ge. Die Festlegung des RS einer R\u00fcstung obliegt am Ende dem Spielleiter.", None))
        self.buttonExpandToggle.setText(QCoreApplication.translate("Dialog", u"Expand Toggle", None))
        self.buttonExpandToggle.setProperty(u"class", QCoreApplication.translate("Dialog", u"icon", None))
        self.nameFilterEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Suchen...", None))
        self.labelFilter.setText(QCoreApplication.translate("Dialog", u"Suchen", None))
        self.labelFilter.setProperty(u"class", QCoreApplication.translate("Dialog", u"icon", None))
        ___qtreewidgetitem = self.treeArmors.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.lblName.setText(QCoreApplication.translate("Dialog", u"Kettenhemd", None))
        self.lblName.setProperty(u"class", QCoreApplication.translate("Dialog", u"h4", None))
        self.lblTyp.setText(QCoreApplication.translate("Dialog", u"Kettenr\u00fcstung", None))
        self.lblTyp.setProperty(u"class", QCoreApplication.translate("Dialog", u"italic", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"RS / BE", None))
        self.lblRS.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblBeineL.setText(QCoreApplication.translate("Dialog", u"Beine", None))
        self.lblBeine.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblSchwertL.setText(QCoreApplication.translate("Dialog", u"Schwertarm", None))
        self.lblSchwert.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblSchildL.setText(QCoreApplication.translate("Dialog", u"Schildarm", None))
        self.lblSchild.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblBauchL.setText(QCoreApplication.translate("Dialog", u"Bauch", None))
        self.lblBauch.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblBrustL.setText(QCoreApplication.translate("Dialog", u"Brust", None))
        self.lblBrust.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblKopfL.setText(QCoreApplication.translate("Dialog", u"Kopf", None))
        self.lblKopf.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lblZRS.setText(QCoreApplication.translate("Dialog", u"= 0", None))
    # retranslateUi

