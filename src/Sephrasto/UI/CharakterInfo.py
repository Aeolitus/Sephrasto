# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterInfo.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1058, 849)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.labelEinstellungen = QLabel(Form)
        self.labelEinstellungen.setObjectName(u"labelEinstellungen")
        font = QFont()
        font.setBold(True)
        self.labelEinstellungen.setFont(font)

        self.verticalLayout_4.addWidget(self.labelEinstellungen)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(20, 20, 20, 20)
        self.checkDetails = QCheckBox(self.groupBox_3)
        self.checkDetails.setObjectName(u"checkDetails")

        self.gridLayout_5.addWidget(self.checkDetails, 2, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 6, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 2, 0, 1, 1)

        self.checkReq = QCheckBox(self.groupBox_3)
        self.checkReq.setObjectName(u"checkReq")
        self.checkReq.setChecked(True)

        self.gridLayout_5.addWidget(self.checkReq, 0, 1, 1, 1)

        self.labelReload = QLabel(self.groupBox_3)
        self.labelReload.setObjectName(u"labelReload")
        self.labelReload.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.labelReload.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.labelReload.setWordWrap(True)

        self.gridLayout_5.addWidget(self.labelReload, 15, 0, 1, 2)

        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 1)

        self.comboHausregeln = QComboBox(self.groupBox_3)
        self.comboHausregeln.setObjectName(u"comboHausregeln")

        self.gridLayout_5.addWidget(self.comboHausregeln, 6, 1, 1, 1)

        self.checkFinanzen = QCheckBox(self.groupBox_3)
        self.checkFinanzen.setObjectName(u"checkFinanzen")
        self.checkFinanzen.setChecked(True)

        self.gridLayout_5.addWidget(self.checkFinanzen, 1, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_4.addItem(self.horizontalSpacer)

        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.verticalLayout_4.addWidget(self.label_16)

        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_6 = QGridLayout(self.groupBox_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(20, 20, 20, 20)
        self.checkFormular = QCheckBox(self.groupBox_4)
        self.checkFormular.setObjectName(u"checkFormular")
        self.checkFormular.setChecked(True)

        self.gridLayout_6.addWidget(self.checkFormular, 7, 1, 1, 1)

        self.cbFormular = QLabel(self.groupBox_4)
        self.cbFormular.setObjectName(u"cbFormular")

        self.gridLayout_6.addWidget(self.cbFormular, 7, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setWordWrap(True)

        self.gridLayout_6.addWidget(self.label_13, 8, 0, 1, 1)

        self.checkUeberPDF = QCheckBox(self.groupBox_4)
        self.checkUeberPDF.setObjectName(u"checkUeberPDF")
        self.checkUeberPDF.setChecked(False)

        self.gridLayout_6.addWidget(self.checkUeberPDF, 8, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_6.addWidget(self.label_14, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkRegeln = QCheckBox(self.groupBox_4)
        self.checkRegeln.setObjectName(u"checkRegeln")
        self.checkRegeln.setChecked(True)
        self.checkRegeln.setTristate(False)

        self.horizontalLayout.addWidget(self.checkRegeln)

        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.labelRegelnGroesse = QLabel(self.groupBox_4)
        self.labelRegelnGroesse.setObjectName(u"labelRegelnGroesse")

        self.horizontalLayout.addWidget(self.labelRegelnGroesse)

        self.spinRegelnGroesse = QSpinBox(self.groupBox_4)
        self.spinRegelnGroesse.setObjectName(u"spinRegelnGroesse")
        self.spinRegelnGroesse.setMinimumSize(QSize(60, 0))
        self.spinRegelnGroesse.setMaximumSize(QSize(60, 16777215))
        self.spinRegelnGroesse.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinRegelnGroesse.setMinimum(6)
        self.spinRegelnGroesse.setMaximum(12)
        self.spinRegelnGroesse.setValue(8)

        self.horizontalLayout.addWidget(self.spinRegelnGroesse)

        self.buttonRegeln = QPushButton(self.groupBox_4)
        self.buttonRegeln.setObjectName(u"buttonRegeln")

        self.horizontalLayout.addWidget(self.buttonRegeln)


        self.gridLayout_6.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.comboCharsheet = QComboBox(self.groupBox_4)
        self.comboCharsheet.setObjectName(u"comboCharsheet")

        self.gridLayout_6.addWidget(self.comboCharsheet, 0, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.labelEP = QLabel(Form)
        self.labelEP.setObjectName(u"labelEP")
        self.labelEP.setFont(font)

        self.verticalLayout_4.addWidget(self.labelEP)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.spinFertigkeitenSpent = QSpinBox(self.groupBox_2)
        self.spinFertigkeitenSpent.setObjectName(u"spinFertigkeitenSpent")
        self.spinFertigkeitenSpent.setFocusPolicy(Qt.NoFocus)
        self.spinFertigkeitenSpent.setAlignment(Qt.AlignCenter)
        self.spinFertigkeitenSpent.setReadOnly(True)
        self.spinFertigkeitenSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinFertigkeitenSpent.setMaximum(999999)

        self.gridLayout_2.addWidget(self.spinFertigkeitenSpent, 3, 1, 1, 1)

        self.spinUebernatuerlichPercent = QSpinBox(self.groupBox_2)
        self.spinUebernatuerlichPercent.setObjectName(u"spinUebernatuerlichPercent")
        self.spinUebernatuerlichPercent.setFocusPolicy(Qt.NoFocus)
        self.spinUebernatuerlichPercent.setAlignment(Qt.AlignCenter)
        self.spinUebernatuerlichPercent.setReadOnly(True)
        self.spinUebernatuerlichPercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinUebernatuerlichPercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinUebernatuerlichPercent, 6, 2, 1, 1)

        self.labelUeber3 = QLabel(self.groupBox_2)
        self.labelUeber3.setObjectName(u"labelUeber3")
        self.labelUeber3.setMinimumSize(QSize(230, 0))
        font1 = QFont()
        font1.setItalic(False)
        self.labelUeber3.setFont(font1)

        self.gridLayout_2.addWidget(self.labelUeber3, 8, 0, 1, 1)

        self.spinProfanPercent = QSpinBox(self.groupBox_2)
        self.spinProfanPercent.setObjectName(u"spinProfanPercent")
        self.spinProfanPercent.setFocusPolicy(Qt.NoFocus)
        self.spinProfanPercent.setAlignment(Qt.AlignCenter)
        self.spinProfanPercent.setReadOnly(True)
        self.spinProfanPercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinProfanPercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinProfanPercent, 2, 2, 1, 1)

        self.spinVorteileSpent = QSpinBox(self.groupBox_2)
        self.spinVorteileSpent.setObjectName(u"spinVorteileSpent")
        self.spinVorteileSpent.setFocusPolicy(Qt.NoFocus)
        self.spinVorteileSpent.setAlignment(Qt.AlignCenter)
        self.spinVorteileSpent.setReadOnly(True)
        self.spinVorteileSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinVorteileSpent.setMaximum(99999999)

        self.gridLayout_2.addWidget(self.spinVorteileSpent, 1, 1, 1, 1)

        self.spinAttributeSpent = QSpinBox(self.groupBox_2)
        self.spinAttributeSpent.setObjectName(u"spinAttributeSpent")
        self.spinAttributeSpent.setFocusPolicy(Qt.NoFocus)
        self.spinAttributeSpent.setAlignment(Qt.AlignCenter)
        self.spinAttributeSpent.setReadOnly(True)
        self.spinAttributeSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinAttributeSpent.setMaximum(99999999)

        self.gridLayout_2.addWidget(self.spinAttributeSpent, 0, 1, 1, 1)

        self.spinUeberTalenteSpent = QSpinBox(self.groupBox_2)
        self.spinUeberTalenteSpent.setObjectName(u"spinUeberTalenteSpent")
        self.spinUeberTalenteSpent.setFocusPolicy(Qt.NoFocus)
        self.spinUeberTalenteSpent.setAlignment(Qt.AlignCenter)
        self.spinUeberTalenteSpent.setReadOnly(True)
        self.spinUeberTalenteSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinUeberTalenteSpent.setMaximum(999999)

        self.gridLayout_2.addWidget(self.spinUeberTalenteSpent, 8, 1, 1, 1)

        self.spinFreieSpent = QSpinBox(self.groupBox_2)
        self.spinFreieSpent.setObjectName(u"spinFreieSpent")
        self.spinFreieSpent.setFocusPolicy(Qt.NoFocus)
        self.spinFreieSpent.setAlignment(Qt.AlignCenter)
        self.spinFreieSpent.setReadOnly(True)
        self.spinFreieSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinFreieSpent.setMaximum(999999)

        self.gridLayout_2.addWidget(self.spinFreieSpent, 5, 1, 1, 1)

        self.spinUeberFertigkeitenPercent = QSpinBox(self.groupBox_2)
        self.spinUeberFertigkeitenPercent.setObjectName(u"spinUeberFertigkeitenPercent")
        self.spinUeberFertigkeitenPercent.setFocusPolicy(Qt.NoFocus)
        self.spinUeberFertigkeitenPercent.setAlignment(Qt.AlignCenter)
        self.spinUeberFertigkeitenPercent.setReadOnly(True)
        self.spinUeberFertigkeitenPercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinUeberFertigkeitenPercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinUeberFertigkeitenPercent, 7, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(230, 0))
        self.label_2.setFont(font)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.spinAttributePercent = QSpinBox(self.groupBox_2)
        self.spinAttributePercent.setObjectName(u"spinAttributePercent")
        self.spinAttributePercent.setFocusPolicy(Qt.NoFocus)
        self.spinAttributePercent.setAlignment(Qt.AlignCenter)
        self.spinAttributePercent.setReadOnly(True)
        self.spinAttributePercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinAttributePercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinAttributePercent, 0, 2, 1, 1)

        self.spinUeberTalentePercent = QSpinBox(self.groupBox_2)
        self.spinUeberTalentePercent.setObjectName(u"spinUeberTalentePercent")
        self.spinUeberTalentePercent.setFocusPolicy(Qt.NoFocus)
        self.spinUeberTalentePercent.setAlignment(Qt.AlignCenter)
        self.spinUeberTalentePercent.setReadOnly(True)
        self.spinUeberTalentePercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinUeberTalentePercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinUeberTalentePercent, 8, 2, 1, 1)

        self.labelUeber1 = QLabel(self.groupBox_2)
        self.labelUeber1.setObjectName(u"labelUeber1")
        self.labelUeber1.setMinimumSize(QSize(230, 0))
        self.labelUeber1.setFont(font)

        self.gridLayout_2.addWidget(self.labelUeber1, 6, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(230, 0))
        self.label_4.setFont(font1)

        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)

        self.spinUebernatuerlichSpent = QSpinBox(self.groupBox_2)
        self.spinUebernatuerlichSpent.setObjectName(u"spinUebernatuerlichSpent")
        self.spinUebernatuerlichSpent.setFocusPolicy(Qt.NoFocus)
        self.spinUebernatuerlichSpent.setAlignment(Qt.AlignCenter)
        self.spinUebernatuerlichSpent.setReadOnly(True)
        self.spinUebernatuerlichSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinUebernatuerlichSpent.setMaximum(999999)

        self.gridLayout_2.addWidget(self.spinUebernatuerlichSpent, 6, 1, 1, 1)

        self.spinUeberFertigkeitenSpent = QSpinBox(self.groupBox_2)
        self.spinUeberFertigkeitenSpent.setObjectName(u"spinUeberFertigkeitenSpent")
        self.spinUeberFertigkeitenSpent.setFocusPolicy(Qt.NoFocus)
        self.spinUeberFertigkeitenSpent.setAlignment(Qt.AlignCenter)
        self.spinUeberFertigkeitenSpent.setReadOnly(True)
        self.spinUeberFertigkeitenSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinUeberFertigkeitenSpent.setMaximum(999999)

        self.gridLayout_2.addWidget(self.spinUeberFertigkeitenSpent, 7, 1, 1, 1)

        self.spinFreiePercent = QSpinBox(self.groupBox_2)
        self.spinFreiePercent.setObjectName(u"spinFreiePercent")
        self.spinFreiePercent.setFocusPolicy(Qt.NoFocus)
        self.spinFreiePercent.setAlignment(Qt.AlignCenter)
        self.spinFreiePercent.setReadOnly(True)
        self.spinFreiePercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinFreiePercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinFreiePercent, 5, 2, 1, 1)

        self.spinFertigkeitenPercent = QSpinBox(self.groupBox_2)
        self.spinFertigkeitenPercent.setObjectName(u"spinFertigkeitenPercent")
        self.spinFertigkeitenPercent.setFocusPolicy(Qt.NoFocus)
        self.spinFertigkeitenPercent.setAlignment(Qt.AlignCenter)
        self.spinFertigkeitenPercent.setReadOnly(True)
        self.spinFertigkeitenPercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinFertigkeitenPercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinFertigkeitenPercent, 3, 2, 1, 1)

        self.spinTalentePercent = QSpinBox(self.groupBox_2)
        self.spinTalentePercent.setObjectName(u"spinTalentePercent")
        self.spinTalentePercent.setFocusPolicy(Qt.NoFocus)
        self.spinTalentePercent.setAlignment(Qt.AlignCenter)
        self.spinTalentePercent.setReadOnly(True)
        self.spinTalentePercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinTalentePercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinTalentePercent, 4, 2, 1, 1)

        self.spinProfanSpent = QSpinBox(self.groupBox_2)
        self.spinProfanSpent.setObjectName(u"spinProfanSpent")
        self.spinProfanSpent.setFocusPolicy(Qt.NoFocus)
        self.spinProfanSpent.setAlignment(Qt.AlignCenter)
        self.spinProfanSpent.setReadOnly(True)
        self.spinProfanSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinProfanSpent.setMaximum(999999)

        self.gridLayout_2.addWidget(self.spinProfanSpent, 2, 1, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(230, 0))
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(230, 0))
        self.label_9.setFont(font1)

        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)

        self.labelUeber2 = QLabel(self.groupBox_2)
        self.labelUeber2.setObjectName(u"labelUeber2")
        self.labelUeber2.setMinimumSize(QSize(230, 0))
        self.labelUeber2.setFont(font1)

        self.gridLayout_2.addWidget(self.labelUeber2, 7, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(230, 0))
        self.label_8.setFont(font1)

        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(230, 0))
        self.label_3.setFont(font)

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.spinTalenteSpent = QSpinBox(self.groupBox_2)
        self.spinTalenteSpent.setObjectName(u"spinTalenteSpent")
        self.spinTalenteSpent.setFocusPolicy(Qt.NoFocus)
        self.spinTalenteSpent.setAlignment(Qt.AlignCenter)
        self.spinTalenteSpent.setReadOnly(True)
        self.spinTalenteSpent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinTalenteSpent.setMaximum(999999)

        self.gridLayout_2.addWidget(self.spinTalenteSpent, 4, 1, 1, 1)

        self.spinVorteilePercent = QSpinBox(self.groupBox_2)
        self.spinVorteilePercent.setObjectName(u"spinVorteilePercent")
        self.spinVorteilePercent.setFocusPolicy(Qt.NoFocus)
        self.spinVorteilePercent.setAlignment(Qt.AlignCenter)
        self.spinVorteilePercent.setReadOnly(True)
        self.spinVorteilePercent.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinVorteilePercent.setMaximum(100)

        self.gridLayout_2.addWidget(self.spinVorteilePercent, 1, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.labelNotiz = QLabel(Form)
        self.labelNotiz.setObjectName(u"labelNotiz")
        self.labelNotiz.setFont(font)

        self.verticalLayout_3.addWidget(self.labelNotiz)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(20, 20, 20, 20)
        self.teNotiz = QPlainTextEdit(self.groupBox)
        self.teNotiz.setObjectName(u"teNotiz")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teNotiz.sizePolicy().hasHeightForWidth())
        self.teNotiz.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.teNotiz, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        QWidget.setTabOrder(self.teNotiz, self.comboHausregeln)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelEinstellungen.setText(QCoreApplication.translate("Form", u"Charakter-Einstellungen", None))
        self.labelEinstellungen.setProperty("class", QCoreApplication.translate("Form", u"h2", None))
        self.groupBox_3.setTitle("")
#if QT_CONFIG(tooltip)
        self.checkDetails.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Wenn diese Option aktiviert ist, wird ein weiterer Tab &quot;Hintergrund&quot; angezeigt, in welchem du eine ausf\u00fchrliche Beschreibung des Charakters vornehmen kannst. Daf\u00fcr wird in Beschreibungs-Tab die Kurzbeschreibung nicht mehr angezeigt.</p><p>Allerdings hat beispielsweise der Standard-Charakterbogen keine Formularfelder f\u00fcr diese Daten - deshalb ist diese Option standardm\u00e4\u00dfig deaktiviert.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkDetails.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"Hausregeln", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Hintergrundangaben", None))
#if QT_CONFIG(tooltip)
        self.checkReq.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Falls abgew\u00e4hlt, werden s\u00e4mtliche Voraussetzungspr\u00fcfungen f\u00fcr Vorteile, \u00fcbernat\u00fcrliche Fertigkeiten usw. deaktiviert.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkReq.setText("")
        self.labelReload.setText(QCoreApplication.translate("Form", u"Der Charakter muss gespeichert und neu geladen werden, damit die neuen Hausregeln \u00fcbernommen werden k\u00f6nnen!", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Voraussetzungen \u00fcberpr\u00fcfen", None))
#if QT_CONFIG(tooltip)
        self.comboHausregeln.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Hier erscheinen alle Hausregeldatenbanken in deinem Regel-Pfad.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkFinanzen.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Die Finanzen spielen nur bei einem neuen Charakter eine Rolle und k\u00f6nnen nach dem ersten Abenteuer ausgeblendet werden. Auch die aktuellen Schicksalspunkte werden dann nicht mehr ausgegeben, da diese ab dem ersten Abenteuer h\u00e4ndisch verwaltet werden.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkFinanzen.setText("")
        self.label_12.setText(QCoreApplication.translate("Form", u"Vor dem ersten Abenteuer", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"Export-Einstellungen", None))
        self.label_16.setProperty("class", QCoreApplication.translate("Form", u"h2", None))
        self.groupBox_4.setTitle("")
#if QT_CONFIG(tooltip)
        self.checkFormular.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Manche PDF-Reader k\u00f6nnen Formularfelder in PDF-Dokumenten nicht durchsuchen oder machen beispielsweise Probleme wegen der automatischen Schriftgr\u00f6\u00dfe. Die Formularfelder erh\u00f6hen die Dateigr\u00f6\u00dfe au\u00dferdem rund 10%. Mit dieser Option kannst du diese in reine Textfelder umwandeln. Sie sind dann allerdings nicht mehr editierbar. Diese Einstellung gilt f\u00fcr neue Charaktere. Du kannst sie nachtr\u00e4glich im Info-Tab des Charaktereditors \u00e4ndern.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkFormular.setText("")
        self.cbFormular.setText(QCoreApplication.translate("Form", u"Formularfelder editierbar", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Export-Option bei \u00fcbernat\u00fcrlichen Fertigkeiten", None))
#if QT_CONFIG(tooltip)
        self.checkUeberPDF.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Sephrasto \u00fcbernimmt automatisch alle \u00fcbernat\u00fcrlichen Fertigkeiten in den Charakterbogen, deren FW mindestens 1 betr\u00e4gt und f\u00fcr welche du mindestens ein Talent aktiviert hast. Wenn du diese Option aktivierst, zeigt Sephrasto eine PDF-Spalte bei den \u00fcbernat\u00fcrlichen Fertigkeiten an. Mit dieser kannst du selbst entscheiden, welche Fertigkeiten in den Charakterbogen \u00fcbernommen werden sollen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkUeberPDF.setText("")
        self.label_6.setText(QCoreApplication.translate("Form", u"Charakterbogen", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Relevante Regeln anh\u00e4ngen", None))
#if QT_CONFIG(tooltip)
        self.checkRegeln.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Sephrasto kann automatisch alle Regeln, die f\u00fcr deinen Charakter relevant sind, zusammentragen und deiner PDF hinten anf\u00fcgen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkRegeln.setText("")
        self.labelRegelnGroesse.setText(QCoreApplication.translate("Form", u"Schriftgr\u00f6\u00dfe", None))
        self.labelRegelnGroesse.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.spinRegelnGroesse.setToolTip(QCoreApplication.translate("Form", u"Schriftgr\u00f6\u00dfe des Regelanhangs", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonRegeln.setToolTip(QCoreApplication.translate("Form", u"Kategorien ausw\u00e4hlen, die im Regelanhang erscheinen sollen.", None))
#endif // QT_CONFIG(tooltip)
        self.buttonRegeln.setText(QCoreApplication.translate("Form", u"Regeln", None))
        self.buttonRegeln.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.comboCharsheet.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Hier erscheinen alle Charakterb\u00f6gen, die mit Sephrasto geliefert werden sowie alle aus deinem Charakterbogen-Pfad.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelEP.setText(QCoreApplication.translate("Form", u"EP-Verteilung", None))
        self.labelEP.setProperty("class", QCoreApplication.translate("Form", u"h2", None))
        self.groupBox_2.setTitle("")
        self.spinFertigkeitenSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinUebernatuerlichPercent.setSuffix(QCoreApplication.translate("Form", u" %", None))
        self.labelUeber3.setText(QCoreApplication.translate("Form", u"    Talente", None))
        self.spinProfanPercent.setSuffix(QCoreApplication.translate("Form", u" %", None))
        self.spinVorteileSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinAttributeSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinUeberTalenteSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinFreieSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinUeberFertigkeitenPercent.setSuffix(QCoreApplication.translate("Form", u" %)", None))
        self.spinUeberFertigkeitenPercent.setPrefix(QCoreApplication.translate("Form", u"(", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Vorteile", None))
        self.label_2.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.spinAttributePercent.setSuffix(QCoreApplication.translate("Form", u" %", None))
        self.spinUeberTalentePercent.setSuffix(QCoreApplication.translate("Form", u" %)", None))
        self.spinUeberTalentePercent.setPrefix(QCoreApplication.translate("Form", u"(", None))
        self.labelUeber1.setText(QCoreApplication.translate("Form", u"\u00dcbernat\u00fcrliche Fertigkeiten und Talente", None))
        self.labelUeber1.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"    Freie Fertigkeiten", None))
        self.spinUebernatuerlichSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinUeberFertigkeitenSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinFreiePercent.setSuffix(QCoreApplication.translate("Form", u" %)", None))
        self.spinFreiePercent.setPrefix(QCoreApplication.translate("Form", u"(", None))
        self.spinFertigkeitenPercent.setSuffix(QCoreApplication.translate("Form", u" %)", None))
        self.spinFertigkeitenPercent.setPrefix(QCoreApplication.translate("Form", u"(", None))
        self.spinTalentePercent.setSuffix(QCoreApplication.translate("Form", u" %)", None))
        self.spinTalentePercent.setPrefix(QCoreApplication.translate("Form", u"(", None))
        self.spinProfanSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.label.setText(QCoreApplication.translate("Form", u"Attribute", None))
        self.label.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"    Talente", None))
        self.labelUeber2.setText(QCoreApplication.translate("Form", u"    Fertigkeiten", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"    Fertigkeiten", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Profane Fertigkeiten und Talente", None))
        self.label_3.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.spinTalenteSpent.setSuffix(QCoreApplication.translate("Form", u" EP", None))
        self.spinVorteilePercent.setSuffix(QCoreApplication.translate("Form", u" %", None))
        self.labelNotiz.setText(QCoreApplication.translate("Form", u"Notiz", None))
        self.labelNotiz.setProperty("class", QCoreApplication.translate("Form", u"h2", None))
        self.groupBox.setTitle("")
        self.teNotiz.setPlainText("")
    # retranslateUi

