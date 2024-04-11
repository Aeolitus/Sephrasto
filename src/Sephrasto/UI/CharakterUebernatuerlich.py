# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterUebernatuerlich.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QListView, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QSplitter, QTableWidget,
    QTableWidgetItem, QTextBrowser, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(872, 571)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tableWidget = QTableWidget(self.splitter)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setShowGrid(True)
        self.splitter.addWidget(self.tableWidget)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(80)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.scrollArea = QScrollArea(self.splitter)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 429, 529))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 3, 3, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 2, 2, 3, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 18))

        self.horizontalLayout_2.addWidget(self.label)

        self.labelAttribute = QLabel(self.scrollAreaWidgetContents)
        self.labelAttribute.setObjectName(u"labelAttribute")
        self.labelAttribute.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.labelAttribute)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")
        font = QFont()
        font.setItalic(True)
        self.labelKategorie.setFont(font)

        self.gridLayout_2.addWidget(self.labelKategorie, 1, 0, 1, 5)

        self.spinBasis = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBasis.setObjectName(u"spinBasis")
        self.spinBasis.setMinimumSize(QSize(60, 0))
        self.spinBasis.setMaximumSize(QSize(60, 16777215))
        self.spinBasis.setAlignment(Qt.AlignCenter)
        self.spinBasis.setReadOnly(True)
        self.spinBasis.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_2.addWidget(self.spinBasis, 4, 1, 1, 1)

        self.plainText = QTextBrowser(self.scrollAreaWidgetContents)
        self.plainText.setObjectName(u"plainText")
        self.plainText.setFrameShape(QFrame.StyledPanel)
        self.plainText.setFrameShadow(QFrame.Sunken)
        self.plainText.setLineWidth(1)

        self.gridLayout_2.addWidget(self.plainText, 7, 0, 1, 5)

        self.spinPW = QSpinBox(self.scrollAreaWidgetContents)
        self.spinPW.setObjectName(u"spinPW")
        self.spinPW.setMinimumSize(QSize(60, 0))
        self.spinPW.setMaximumSize(QSize(60, 16777215))
        self.spinPW.setAlignment(Qt.AlignCenter)
        self.spinPW.setReadOnly(True)
        self.spinPW.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_2.addWidget(self.spinPW, 3, 4, 1, 1)

        self.listTalente = QListView(self.scrollAreaWidgetContents)
        self.listTalente.setObjectName(u"listTalente")
        sizePolicy.setHeightForWidth(self.listTalente.sizePolicy().hasHeightForWidth())
        self.listTalente.setSizePolicy(sizePolicy)
        self.listTalente.setMaximumSize(QSize(16777215, 80))

        self.gridLayout_2.addWidget(self.listTalente, 6, 0, 1, 5)

        self.buttonAdd = QPushButton(self.scrollAreaWidgetContents)
        self.buttonAdd.setObjectName(u"buttonAdd")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.buttonAdd.sizePolicy().hasHeightForWidth())
        self.buttonAdd.setSizePolicy(sizePolicy1)
        self.buttonAdd.setLayoutDirection(Qt.RightToLeft)

        self.gridLayout_2.addWidget(self.buttonAdd, 5, 4, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 8, 0, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 5, 0, 1, 2)

        self.labelFertigkeit = QLabel(self.scrollAreaWidgetContents)
        self.labelFertigkeit.setObjectName(u"labelFertigkeit")
        self.labelFertigkeit.setMinimumSize(QSize(0, 20))
        font1 = QFont()
        font1.setBold(True)
        self.labelFertigkeit.setFont(font1)

        self.gridLayout_2.addWidget(self.labelFertigkeit, 0, 0, 1, 5)

        self.spinFW = QSpinBox(self.scrollAreaWidgetContents)
        self.spinFW.setObjectName(u"spinFW")
        self.spinFW.setMinimumSize(QSize(60, 0))
        self.spinFW.setMaximumSize(QSize(60, 16777215))
        self.spinFW.setAlignment(Qt.AlignCenter)
        self.spinFW.setReadOnly(False)
        self.spinFW.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout_2.addWidget(self.spinFW, 2, 4, 1, 1)

        self.spinSF = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSF.setObjectName(u"spinSF")
        self.spinSF.setMinimumSize(QSize(60, 0))
        self.spinSF.setMaximumSize(QSize(60, 16777215))
        self.spinSF.setAlignment(Qt.AlignCenter)
        self.spinSF.setReadOnly(True)
        self.spinSF.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_2.addWidget(self.spinSF, 3, 1, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 2, 3, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.splitter.addWidget(self.scrollArea)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        QWidget.setTabOrder(self.tableWidget, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.spinFW)
        QWidget.setTabOrder(self.spinFW, self.spinSF)
        QWidget.setTabOrder(self.spinSF, self.spinPW)
        QWidget.setTabOrder(self.spinPW, self.spinBasis)
        QWidget.setTabOrder(self.spinBasis, self.buttonAdd)
        QWidget.setTabOrder(self.buttonAdd, self.listTalente)
        QWidget.setTabOrder(self.listTalente, self.plainText)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Fertigkeitsname", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"FW", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Talente", None));
        self.label_6.setText(QCoreApplication.translate("Form", u"Basis:", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"PW:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"SF:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Attribute:", None))
        self.labelAttribute.setText(QCoreApplication.translate("Form", u"MU/IN/CH", None))
        self.labelKategorie.setText(QCoreApplication.translate("Form", u"Allgemeine Zauber", None))
        self.labelKategorie.setProperty("class", QCoreApplication.translate("Form", u"italic", None))
        self.buttonAdd.setText(QCoreApplication.translate("Form", u"+", None))
        self.buttonAdd.setProperty("class", QCoreApplication.translate("Form", u"iconSmall", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Erworbene Talente:", None))
        self.labelFertigkeit.setText(QCoreApplication.translate("Form", u"Fertigkeit", None))
        self.labelFertigkeit.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"FW:", None))
    # retranslateUi

