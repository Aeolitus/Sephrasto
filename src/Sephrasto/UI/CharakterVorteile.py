# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterVorteile.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(701, 460)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonExpandToggle = QPushButton(self.verticalLayoutWidget)
        self.buttonExpandToggle.setObjectName(u"buttonExpandToggle")

        self.horizontalLayout.addWidget(self.buttonExpandToggle)

        self.nameFilterEdit = QLineEdit(self.verticalLayoutWidget)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")
        self.nameFilterEdit.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.nameFilterEdit)

        self.labelFilter = QLabel(self.verticalLayoutWidget)
        self.labelFilter.setObjectName(u"labelFilter")

        self.horizontalLayout.addWidget(self.labelFilter)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeWidget = QTreeWidget(self.verticalLayoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignLeading|Qt.AlignVCenter);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeWidget.setTabKeyNavigation(True)
        self.treeWidget.setProperty("showDropIndicator", False)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setAnimated(False)
        self.treeWidget.setAllColumnsShowFocus(True)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setMinimumSectionSize(80)
        self.treeWidget.header().setDefaultSectionSize(100)
        self.treeWidget.header().setHighlightSections(False)
        self.treeWidget.header().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.treeWidget)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.scrollArea = QScrollArea(self.splitter)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 268, 418))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelVorteil = QLabel(self.scrollAreaWidgetContents)
        self.labelVorteil.setObjectName(u"labelVorteil")
        font = QFont()
        font.setBold(True)
        self.labelVorteil.setFont(font)

        self.gridLayout_2.addWidget(self.labelVorteil, 0, 0, 1, 2)

        self.labelVoraussetzungen = QLabel(self.scrollAreaWidgetContents)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")
        self.labelVoraussetzungen.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.labelVoraussetzungen.setWordWrap(True)

        self.gridLayout_2.addWidget(self.labelVoraussetzungen, 2, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)

        self.plainText = QTextBrowser(self.scrollAreaWidgetContents)
        self.plainText.setObjectName(u"plainText")

        self.gridLayout_2.addWidget(self.plainText, 5, 0, 1, 2)

        self.vlQuerverweise = QVBoxLayout()
        self.vlQuerverweise.setSpacing(12)
        self.vlQuerverweise.setObjectName(u"vlQuerverweise")
        self.vlQuerverweise.setContentsMargins(-1, 10, -1, -1)

        self.gridLayout_2.addLayout(self.vlQuerverweise, 6, 0, 1, 2)

        self.labelTyp = QLabel(self.scrollAreaWidgetContents)
        self.labelTyp.setObjectName(u"labelTyp")
        self.labelTyp.setMinimumSize(QSize(0, 18))
        font1 = QFont()
        font1.setItalic(True)
        self.labelTyp.setFont(font1)
        self.labelTyp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelTyp, 1, 0, 1, 2)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.labelKosten = QLabel(self.scrollAreaWidgetContents)
        self.labelKosten.setObjectName(u"labelKosten")
        self.labelKosten.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelKosten, 3, 1, 1, 1)

        self.labelNachkauf = QLabel(self.scrollAreaWidgetContents)
        self.labelNachkauf.setObjectName(u"labelNachkauf")
        self.labelNachkauf.setMinimumSize(QSize(0, 18))
        self.labelNachkauf.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelNachkauf, 4, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 7, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.splitter.addWidget(self.scrollArea)

        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        QWidget.setTabOrder(self.buttonExpandToggle, self.nameFilterEdit)
        QWidget.setTabOrder(self.nameFilterEdit, self.treeWidget)
        QWidget.setTabOrder(self.treeWidget, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.plainText)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.buttonExpandToggle.setText(QCoreApplication.translate("Form", u"Expand Toggle", None))
        self.buttonExpandToggle.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
        self.nameFilterEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Suchen...", None))
        self.labelFilter.setText(QCoreApplication.translate("Form", u"Suchen", None))
        self.labelFilter.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Kosten", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Vorteil", None));
        self.labelVorteil.setText(QCoreApplication.translate("Form", u"Vorteil", None))
        self.labelVorteil.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.labelVoraussetzungen.setText(QCoreApplication.translate("Form", u"keine", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Voraussetzungen:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Kosten:", None))
        self.labelTyp.setText(QCoreApplication.translate("Form", u"Allgemeine Vorteile", None))
        self.labelTyp.setProperty("class", QCoreApplication.translate("Form", u"italic", None))
        self.label.setText(QCoreApplication.translate("Form", u"Nachkauf:", None))
        self.labelKosten.setText(QCoreApplication.translate("Form", u"20 EP", None))
        self.labelNachkauf.setText(QCoreApplication.translate("Form", u"H\u00e4ufig", None))
    # retranslateUi

