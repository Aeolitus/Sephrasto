# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterMinderpakt.ui'
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
    QDialogButtonBox, QFrame, QGridLayout, QHeaderView,
    QLabel, QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(922, 558)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.treeWidget = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignLeading|Qt.AlignVCenter);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QSize(0, 0))
        self.treeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeWidget.setTabKeyNavigation(True)
        self.treeWidget.setProperty(u"showDropIndicator", False)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setAnimated(False)
        self.treeWidget.setAllColumnsShowFocus(True)
        self.treeWidget.setHeaderHidden(False)
        self.splitter.addWidget(self.treeWidget)
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setMinimumSectionSize(80)
        self.treeWidget.header().setDefaultSectionSize(100)
        self.treeWidget.header().setHighlightSections(False)
        self.treeWidget.header().setStretchLastSection(False)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 465, 497))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.labelTyp = QLabel(self.scrollAreaWidgetContents)
        self.labelTyp.setObjectName(u"labelTyp")
        self.labelTyp.setMinimumSize(QSize(0, 18))
        font = QFont()
        font.setItalic(True)
        self.labelTyp.setFont(font)
        self.labelTyp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelTyp, 1, 0, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.labelNachkauf = QLabel(self.scrollAreaWidgetContents)
        self.labelNachkauf.setObjectName(u"labelNachkauf")
        self.labelNachkauf.setMinimumSize(QSize(0, 18))
        self.labelNachkauf.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelNachkauf, 3, 1, 1, 1)

        self.labelVorteil = QLabel(self.scrollAreaWidgetContents)
        self.labelVorteil.setObjectName(u"labelVorteil")
        self.labelVorteil.setMinimumSize(QSize(0, 20))
        font1 = QFont()
        font1.setBold(True)
        self.labelVorteil.setFont(font1)

        self.gridLayout.addWidget(self.labelVorteil, 0, 0, 1, 2)

        self.plainText = QTextBrowser(self.scrollAreaWidgetContents)
        self.plainText.setObjectName(u"plainText")
        self.plainText.setFrameShape(QFrame.StyledPanel)
        self.plainText.setFrameShadow(QFrame.Sunken)
        self.plainText.setLineWidth(1)

        self.gridLayout.addWidget(self.plainText, 4, 0, 1, 2)

        self.labelKosten = QLabel(self.scrollAreaWidgetContents)
        self.labelKosten.setObjectName(u"labelKosten")
        self.labelKosten.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKosten, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 1)

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

        QWidget.setTabOrder(self.treeWidget, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.plainText)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Sephrasto - Minderpakt-Vorteil w\u00e4hlen", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Kosten", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Vorteil", None));
        self.label.setText(QCoreApplication.translate("Dialog", u"Nachkauf:", None))
        self.labelTyp.setText(QCoreApplication.translate("Dialog", u"Profan", None))
        self.labelTyp.setProperty(u"class", QCoreApplication.translate("Dialog", u"italic", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Kosten:", None))
        self.labelNachkauf.setText(QCoreApplication.translate("Dialog", u"H\u00e4ufig", None))
        self.labelVorteil.setText(QCoreApplication.translate("Dialog", u"Vorteil", None))
        self.labelVorteil.setProperty(u"class", QCoreApplication.translate("Dialog", u"h4", None))
        self.labelKosten.setText(QCoreApplication.translate("Dialog", u"20 EP", None))
    # retranslateUi

