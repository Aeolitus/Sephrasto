# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterAttribute.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QSpinBox,
    QWidget)

class Ui_formAttribute(object):
    def setupUi(self, formAttribute):
        if not formAttribute.objectName():
            formAttribute.setObjectName(u"formAttribute")
        formAttribute.resize(893, 460)
        self.gridLayout_2 = QGridLayout(formAttribute)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_20 = QLabel(formAttribute)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(25, 0))
        font = QFont()
        font.setItalic(True)
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 4, 2, 1, 1)

        self.pwCH = QSpinBox(formAttribute)
        self.pwCH.setObjectName(u"pwCH")
        self.pwCH.setFocusPolicy(Qt.NoFocus)
        self.pwCH.setWrapping(False)
        self.pwCH.setFrame(True)
        self.pwCH.setAlignment(Qt.AlignCenter)
        self.pwCH.setReadOnly(True)
        self.pwCH.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwCH.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwCH, 8, 4, 1, 1)

        self.abKaP = QSpinBox(formAttribute)
        self.abKaP.setObjectName(u"abKaP")
        self.abKaP.setFocusPolicy(Qt.NoFocus)
        self.abKaP.setAlignment(Qt.AlignCenter)
        self.abKaP.setReadOnly(True)
        self.abKaP.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.abKaP.setMaximum(999)

        self.gridLayout.addWidget(self.abKaP, 9, 9, 1, 1)

        self.spinFF = QSpinBox(formAttribute)
        self.spinFF.setObjectName(u"spinFF")
        self.spinFF.setAlignment(Qt.AlignCenter)
        self.spinFF.setReadOnly(False)
        self.spinFF.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinFF, 9, 3, 1, 1)

        self.label_33 = QLabel(formAttribute)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMinimumSize(QSize(20, 0))
        self.label_33.setMaximumSize(QSize(15, 16777215))
        self.label_33.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_33, 8, 10, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.spinKaP = QSpinBox(formAttribute)
        self.spinKaP.setObjectName(u"spinKaP")
        self.spinKaP.setMinimumSize(QSize(60, 0))
        self.spinKaP.setMaximumSize(QSize(37, 16777215))
        self.spinKaP.setAlignment(Qt.AlignCenter)
        self.spinKaP.setReadOnly(False)
        self.spinKaP.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.horizontalLayout_2.addWidget(self.spinKaP)

        self.label_32 = QLabel(formAttribute)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_2.addWidget(self.label_32)

        self.labelKostenKaP = QLabel(formAttribute)
        self.labelKostenKaP.setObjectName(u"labelKostenKaP")
        self.labelKostenKaP.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.labelKostenKaP)


        self.gridLayout.addLayout(self.horizontalLayout_2, 9, 11, 1, 1)

        self.pwFF = QSpinBox(formAttribute)
        self.pwFF.setObjectName(u"pwFF")
        self.pwFF.setFocusPolicy(Qt.NoFocus)
        self.pwFF.setWrapping(False)
        self.pwFF.setFrame(True)
        self.pwFF.setAlignment(Qt.AlignCenter)
        self.pwFF.setReadOnly(True)
        self.pwFF.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwFF.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwFF, 9, 4, 1, 1)

        self.pwGE = QSpinBox(formAttribute)
        self.pwGE.setObjectName(u"pwGE")
        self.pwGE.setFocusPolicy(Qt.NoFocus)
        self.pwGE.setWrapping(False)
        self.pwGE.setFrame(True)
        self.pwGE.setAlignment(Qt.AlignCenter)
        self.pwGE.setReadOnly(True)
        self.pwGE.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwGE.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwGE, 4, 4, 1, 1)

        self.pwKO = QSpinBox(formAttribute)
        self.pwKO.setObjectName(u"pwKO")
        self.pwKO.setFocusPolicy(Qt.NoFocus)
        self.pwKO.setWrapping(False)
        self.pwKO.setFrame(True)
        self.pwKO.setAlignment(Qt.AlignCenter)
        self.pwKO.setReadOnly(True)
        self.pwKO.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwKO.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwKO, 2, 4, 1, 1)

        self.label_11 = QLabel(formAttribute)
        self.label_11.setObjectName(u"label_11")
        font1 = QFont()
        font1.setBold(True)
        self.label_11.setFont(font1)

        self.gridLayout.addWidget(self.label_11, 4, 7, 1, 1)

        self.label_5 = QLabel(formAttribute)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.gridLayout.addWidget(self.label_5, 6, 1, 1, 1)

        self.label_21 = QLabel(formAttribute)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(25, 0))
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_21, 5, 2, 1, 1)

        self.spinCH = QSpinBox(formAttribute)
        self.spinCH.setObjectName(u"spinCH")
        self.spinCH.setAlignment(Qt.AlignCenter)
        self.spinCH.setReadOnly(False)
        self.spinCH.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinCH, 8, 3, 1, 1)

        self.label_19 = QLabel(formAttribute)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(25, 0))
        self.label_19.setFont(font)
        self.label_19.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_19, 3, 2, 1, 1)

        self.label_14 = QLabel(formAttribute)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)

        self.gridLayout.addWidget(self.label_14, 8, 7, 1, 1)

        self.label_9 = QLabel(formAttribute)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)

        self.gridLayout.addWidget(self.label_9, 2, 7, 1, 1)

        self.label_24 = QLabel(formAttribute)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(25, 0))
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_24, 8, 2, 1, 1)

        self.label_28 = QLabel(formAttribute)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(25, 0))
        self.label_28.setFont(font)
        self.label_28.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_28, 4, 8, 1, 1)

        self.pwMU = QSpinBox(formAttribute)
        self.pwMU.setObjectName(u"pwMU")
        self.pwMU.setFocusPolicy(Qt.NoFocus)
        self.pwMU.setWrapping(False)
        self.pwMU.setFrame(True)
        self.pwMU.setAlignment(Qt.AlignCenter)
        self.pwMU.setReadOnly(True)
        self.pwMU.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwMU.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwMU, 3, 4, 1, 1)

        self.label_8 = QLabel(formAttribute)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(100, 0))
        self.label_8.setFont(font1)

        self.gridLayout.addWidget(self.label_8, 9, 1, 1, 1)

        self.lblKapZugekauft = QLabel(formAttribute)
        self.lblKapZugekauft.setObjectName(u"lblKapZugekauft")
        self.lblKapZugekauft.setMinimumSize(QSize(100, 0))
        self.lblKapZugekauft.setFont(font1)

        self.gridLayout.addWidget(self.lblKapZugekauft, 9, 7, 1, 1)

        self.label_104 = QLabel(formAttribute)
        self.label_104.setObjectName(u"label_104")
        self.label_104.setMinimumSize(QSize(25, 0))

        self.gridLayout.addWidget(self.label_104, 6, 11, 1, 1)

        self.label = QLabel(formAttribute)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)

        self.label_100 = QLabel(formAttribute)
        self.label_100.setObjectName(u"label_100")
        self.label_100.setMinimumSize(QSize(25, 0))

        self.gridLayout.addWidget(self.label_100, 2, 11, 1, 1)

        self.label_34 = QLabel(formAttribute)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(20, 0))
        self.label_34.setMaximumSize(QSize(15, 16777215))
        self.label_34.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_34, 9, 10, 1, 1)

        self.spinKO = QSpinBox(formAttribute)
        self.spinKO.setObjectName(u"spinKO")
        self.spinKO.setAlignment(Qt.AlignCenter)
        self.spinKO.setReadOnly(False)
        self.spinKO.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinKO, 2, 3, 1, 1)

        self.labelWert = QLabel(formAttribute)
        self.labelWert.setObjectName(u"labelWert")
        self.labelWert.setMinimumSize(QSize(60, 0))
        self.labelWert.setFont(font1)
        self.labelWert.setAlignment(Qt.AlignCenter)
        self.labelWert.setMargin(0)

        self.gridLayout.addWidget(self.labelWert, 1, 3, 1, 1)

        self.label_102 = QLabel(formAttribute)
        self.label_102.setObjectName(u"label_102")
        self.label_102.setMinimumSize(QSize(25, 0))

        self.gridLayout.addWidget(self.label_102, 4, 11, 1, 1)

        self.label_7 = QLabel(formAttribute)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.gridLayout.addWidget(self.label_7, 8, 1, 1, 1)

        self.label_13 = QLabel(formAttribute)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)

        self.gridLayout.addWidget(self.label_13, 6, 7, 1, 1)

        self.label_101 = QLabel(formAttribute)
        self.label_101.setObjectName(u"label_101")
        self.label_101.setMinimumSize(QSize(25, 0))

        self.gridLayout.addWidget(self.label_101, 3, 11, 1, 1)

        self.pwIN = QSpinBox(formAttribute)
        self.pwIN.setObjectName(u"pwIN")
        self.pwIN.setFocusPolicy(Qt.NoFocus)
        self.pwIN.setWrapping(False)
        self.pwIN.setFrame(True)
        self.pwIN.setAlignment(Qt.AlignCenter)
        self.pwIN.setReadOnly(True)
        self.pwIN.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwIN.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwIN, 6, 4, 1, 1)

        self.abSB = QSpinBox(formAttribute)
        self.abSB.setObjectName(u"abSB")
        self.abSB.setFocusPolicy(Qt.NoFocus)
        self.abSB.setWrapping(False)
        self.abSB.setFrame(True)
        self.abSB.setAlignment(Qt.AlignCenter)
        self.abSB.setReadOnly(True)
        self.abSB.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.abSB.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.abSB, 5, 9, 1, 1)

        self.label_10 = QLabel(formAttribute)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.gridLayout.addWidget(self.label_10, 3, 7, 1, 1)

        self.spinMU = QSpinBox(formAttribute)
        self.spinMU.setObjectName(u"spinMU")
        self.spinMU.setAlignment(Qt.AlignCenter)
        self.spinMU.setReadOnly(False)
        self.spinMU.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinMU, 3, 3, 1, 1)

        self.abMR = QSpinBox(formAttribute)
        self.abMR.setObjectName(u"abMR")
        self.abMR.setFocusPolicy(Qt.NoFocus)
        self.abMR.setWrapping(False)
        self.abMR.setFrame(True)
        self.abMR.setAlignment(Qt.AlignCenter)
        self.abMR.setReadOnly(True)
        self.abMR.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.abMR.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.abMR, 3, 9, 1, 1)

        self.label_29 = QLabel(formAttribute)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(25, 0))
        self.label_29.setFont(font)
        self.label_29.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_29, 5, 8, 1, 1)

        self.label_103 = QLabel(formAttribute)
        self.label_103.setObjectName(u"label_103")
        self.label_103.setMinimumSize(QSize(25, 0))

        self.gridLayout.addWidget(self.label_103, 5, 11, 1, 1)

        self.label_31 = QLabel(formAttribute)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(25, 0))
        self.label_31.setFont(font)
        self.label_31.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_31, 8, 8, 1, 1)

        self.label_6 = QLabel(formAttribute)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.gridLayout.addWidget(self.label_6, 7, 1, 1, 1)

        self.label_30 = QLabel(formAttribute)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(25, 0))
        self.label_30.setFont(font)
        self.label_30.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_30, 6, 8, 1, 1)

        self.label_18 = QLabel(formAttribute)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(25, 0))
        self.label_18.setFont(font)
        self.label_18.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_18, 2, 2, 1, 1)

        self.spinGE = QSpinBox(formAttribute)
        self.spinGE.setObjectName(u"spinGE")
        self.spinGE.setAlignment(Qt.AlignCenter)
        self.spinGE.setReadOnly(False)
        self.spinGE.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinGE, 4, 3, 1, 1)

        self.abGS = QSpinBox(formAttribute)
        self.abGS.setObjectName(u"abGS")
        self.abGS.setFocusPolicy(Qt.NoFocus)
        self.abGS.setWrapping(False)
        self.abGS.setFrame(True)
        self.abGS.setAlignment(Qt.AlignCenter)
        self.abGS.setReadOnly(True)
        self.abGS.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.abGS.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.abGS, 4, 9, 1, 1)

        self.spinKL = QSpinBox(formAttribute)
        self.spinKL.setObjectName(u"spinKL")
        self.spinKL.setAlignment(Qt.AlignCenter)
        self.spinKL.setReadOnly(False)
        self.spinKL.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinKL, 7, 3, 1, 1)

        self.abIN = QSpinBox(formAttribute)
        self.abIN.setObjectName(u"abIN")
        self.abIN.setFocusPolicy(Qt.NoFocus)
        self.abIN.setWrapping(False)
        self.abIN.setFrame(True)
        self.abIN.setAlignment(Qt.AlignCenter)
        self.abIN.setReadOnly(True)
        self.abIN.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.abIN.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.abIN, 6, 9, 1, 1)

        self.pwKK = QSpinBox(formAttribute)
        self.pwKK.setObjectName(u"pwKK")
        self.pwKK.setFocusPolicy(Qt.NoFocus)
        self.pwKK.setWrapping(False)
        self.pwKK.setFrame(True)
        self.pwKK.setAlignment(Qt.AlignCenter)
        self.pwKK.setReadOnly(True)
        self.pwKK.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwKK.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwKK, 5, 4, 1, 1)

        self.label_4 = QLabel(formAttribute)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.gridLayout.addWidget(self.label_4, 5, 1, 1, 1)

        self.labelPW = QLabel(formAttribute)
        self.labelPW.setObjectName(u"labelPW")
        self.labelPW.setMinimumSize(QSize(60, 0))
        self.labelPW.setFont(font1)
        self.labelPW.setAlignment(Qt.AlignCenter)
        self.labelPW.setMargin(0)

        self.gridLayout.addWidget(self.labelPW, 1, 4, 1, 1)

        self.lblKap = QLabel(formAttribute)
        self.lblKap.setObjectName(u"lblKap")
        self.lblKap.setMinimumSize(QSize(26, 0))
        self.lblKap.setFont(font)
        self.lblKap.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lblKap, 9, 8, 1, 1)

        self.spinKK = QSpinBox(formAttribute)
        self.spinKK.setObjectName(u"spinKK")
        self.spinKK.setAlignment(Qt.AlignCenter)
        self.spinKK.setReadOnly(False)
        self.spinKK.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinKK, 5, 3, 1, 1)

        self.abWS = QSpinBox(formAttribute)
        self.abWS.setObjectName(u"abWS")
        self.abWS.setFocusPolicy(Qt.NoFocus)
        self.abWS.setWrapping(False)
        self.abWS.setFrame(True)
        self.abWS.setAlignment(Qt.AlignCenter)
        self.abWS.setReadOnly(True)
        self.abWS.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.abWS.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.abWS, 2, 9, 1, 1)

        self.label_27 = QLabel(formAttribute)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(25, 0))
        self.label_27.setFont(font)
        self.label_27.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_27, 3, 8, 1, 1)

        self.abAsP = QSpinBox(formAttribute)
        self.abAsP.setObjectName(u"abAsP")
        self.abAsP.setFocusPolicy(Qt.NoFocus)
        self.abAsP.setAlignment(Qt.AlignCenter)
        self.abAsP.setReadOnly(True)
        self.abAsP.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.abAsP.setMaximum(999)

        self.gridLayout.addWidget(self.abAsP, 8, 9, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinAsP = QSpinBox(formAttribute)
        self.spinAsP.setObjectName(u"spinAsP")
        self.spinAsP.setMinimumSize(QSize(60, 0))
        self.spinAsP.setMaximumSize(QSize(37, 16777215))
        self.spinAsP.setAlignment(Qt.AlignCenter)
        self.spinAsP.setReadOnly(False)
        self.spinAsP.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.horizontalLayout.addWidget(self.spinAsP)

        self.label_15 = QLabel(formAttribute)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout.addWidget(self.label_15)

        self.labelKostenAsP = QLabel(formAttribute)
        self.labelKostenAsP.setObjectName(u"labelKostenAsP")
        self.labelKostenAsP.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.labelKostenAsP)


        self.gridLayout.addLayout(self.horizontalLayout, 8, 11, 1, 1)

        self.labelFormel = QLabel(formAttribute)
        self.labelFormel.setObjectName(u"labelFormel")
        self.labelFormel.setMinimumSize(QSize(60, 0))
        self.labelFormel.setFont(font1)
        self.labelFormel.setMargin(0)

        self.gridLayout.addWidget(self.labelFormel, 1, 11, 1, 1)

        self.label_12 = QLabel(formAttribute)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)

        self.gridLayout.addWidget(self.label_12, 5, 7, 1, 1)

        self.label_25 = QLabel(formAttribute)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(25, 0))
        self.label_25.setFont(font)
        self.label_25.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_25, 9, 2, 1, 1)

        self.labelWert2 = QLabel(formAttribute)
        self.labelWert2.setObjectName(u"labelWert2")
        self.labelWert2.setMinimumSize(QSize(60, 0))
        self.labelWert2.setFont(font1)
        self.labelWert2.setAlignment(Qt.AlignCenter)
        self.labelWert2.setMargin(0)

        self.gridLayout.addWidget(self.labelWert2, 1, 9, 1, 1)

        self.label_2 = QLabel(formAttribute)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)

        self.label_23 = QLabel(formAttribute)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(25, 0))
        self.label_23.setFont(font)
        self.label_23.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_23, 7, 2, 1, 1)

        self.label_3 = QLabel(formAttribute)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout.addWidget(self.label_3, 4, 1, 1, 1)

        self.label_26 = QLabel(formAttribute)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(25, 0))
        self.label_26.setFont(font)
        self.label_26.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_26, 2, 8, 1, 1)

        self.label_22 = QLabel(formAttribute)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(25, 0))
        self.label_22.setFont(font)
        self.label_22.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_22, 6, 2, 1, 1)

        self.pwKL = QSpinBox(formAttribute)
        self.pwKL.setObjectName(u"pwKL")
        self.pwKL.setFocusPolicy(Qt.NoFocus)
        self.pwKL.setWrapping(False)
        self.pwKL.setFrame(True)
        self.pwKL.setAlignment(Qt.AlignCenter)
        self.pwKL.setReadOnly(True)
        self.pwKL.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.pwKL.setProperty("showGroupSeparator", False)

        self.gridLayout.addWidget(self.pwKL, 7, 4, 1, 1)

        self.spinIN = QSpinBox(formAttribute)
        self.spinIN.setObjectName(u"spinIN")
        self.spinIN.setAlignment(Qt.AlignCenter)
        self.spinIN.setReadOnly(False)
        self.spinIN.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.spinIN, 6, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(70, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 5, 6, 1, 1)

        self.labelKosten = QLabel(formAttribute)
        self.labelKosten.setObjectName(u"labelKosten")
        self.labelKosten.setMinimumSize(QSize(60, 0))
        self.labelKosten.setFont(font1)
        self.labelKosten.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKosten, 1, 5, 1, 1)

        self.labelKostenKO = QLabel(formAttribute)
        self.labelKostenKO.setObjectName(u"labelKostenKO")
        self.labelKostenKO.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenKO, 2, 5, 1, 1)

        self.labelKostenMU = QLabel(formAttribute)
        self.labelKostenMU.setObjectName(u"labelKostenMU")
        self.labelKostenMU.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenMU, 3, 5, 1, 1)

        self.labelKostenGE = QLabel(formAttribute)
        self.labelKostenGE.setObjectName(u"labelKostenGE")
        self.labelKostenGE.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenGE, 4, 5, 1, 1)

        self.labelKostenKK = QLabel(formAttribute)
        self.labelKostenKK.setObjectName(u"labelKostenKK")
        self.labelKostenKK.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenKK, 5, 5, 1, 1)

        self.labelKostenIN = QLabel(formAttribute)
        self.labelKostenIN.setObjectName(u"labelKostenIN")
        self.labelKostenIN.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenIN, 6, 5, 1, 1)

        self.labelKostenCH = QLabel(formAttribute)
        self.labelKostenCH.setObjectName(u"labelKostenCH")
        self.labelKostenCH.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenCH, 8, 5, 1, 1)

        self.labelKostenFF = QLabel(formAttribute)
        self.labelKostenFF.setObjectName(u"labelKostenFF")
        self.labelKostenFF.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenFF, 9, 5, 1, 1)

        self.labelKostenKL = QLabel(formAttribute)
        self.labelKostenKL.setObjectName(u"labelKostenKL")
        self.labelKostenKL.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKostenKL, 7, 5, 1, 1)

        self.label_16 = QLabel(formAttribute)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font1)

        self.gridLayout.addWidget(self.label_16, 7, 7, 1, 1)

        self.label_17 = QLabel(formAttribute)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_17, 7, 8, 1, 1)

        self.abDH = QSpinBox(formAttribute)
        self.abDH.setObjectName(u"abDH")
        self.abDH.setAlignment(Qt.AlignCenter)
        self.abDH.setReadOnly(True)
        self.abDH.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout.addWidget(self.abDH, 7, 9, 1, 1)

        self.label_35 = QLabel(formAttribute)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout.addWidget(self.label_35, 7, 11, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        QWidget.setTabOrder(self.spinKO, self.spinMU)
        QWidget.setTabOrder(self.spinMU, self.spinGE)
        QWidget.setTabOrder(self.spinGE, self.spinKK)
        QWidget.setTabOrder(self.spinKK, self.spinIN)
        QWidget.setTabOrder(self.spinIN, self.spinKL)
        QWidget.setTabOrder(self.spinKL, self.spinCH)
        QWidget.setTabOrder(self.spinCH, self.spinFF)
        QWidget.setTabOrder(self.spinFF, self.spinAsP)
        QWidget.setTabOrder(self.spinAsP, self.spinKaP)

        self.retranslateUi(formAttribute)

        QMetaObject.connectSlotsByName(formAttribute)
    # setupUi

    def retranslateUi(self, formAttribute):
        formAttribute.setWindowTitle(QCoreApplication.translate("formAttribute", u"Attribute", None))
        self.label_20.setText(QCoreApplication.translate("formAttribute", u"GE", None))
        self.label_33.setText(QCoreApplication.translate("formAttribute", u"+", None))
        self.label_32.setText(QCoreApplication.translate("formAttribute", u"zugekauft", None))
        self.labelKostenKaP.setText(QCoreApplication.translate("formAttribute", u"(0 EP)", None))
#if QT_CONFIG(tooltip)
        self.label_11.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Die Geschwindigkeit stellt die Schnelligkeit und Beweglichkeit deines Charakters dar. Sie bestimmt, wie weit er sich im Kampf bewegen kann und hilft auch bei Verfolgungsjagden zu Fu\u00df.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("formAttribute", u"Geschwindigkeit", None))
        self.label_11.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Intuition erm\u00f6glicht es deinem Charakter, Personen und Sachverhalte schnell richtig einzusch\u00e4tzen. Sie steht auch f\u00fcr Wahrnehmung und Einf\u00fchlungsverm\u00f6gen deines Charakters. Intuition beeinflusst eine breite Palette an Fertigkeiten und bestimmt deine Initiative im Kampf.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("formAttribute", u"Intuition", None))
        self.label_5.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_21.setText(QCoreApplication.translate("formAttribute", u"KK", None))
        self.label_19.setText(QCoreApplication.translate("formAttribute", u"MU", None))
#if QT_CONFIG(tooltip)
        self.label_14.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Magiebegabte Charaktere k\u00f6nnen Astralenergie in sich aufnehmen und speichern. Die Vorteile Zauberer I/II/III/IV verleihen deinem Charakter 8/16/24/32 Astralpunkte (AsP). Du kannst diesen Vorrat an maximalen AsP durch den Zukauf nach Steigerungsfaktor 1 weiter erh\u00f6hen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_14.setText(QCoreApplication.translate("formAttribute", u"Astralenergie", None))
        self.label_14.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Die Wundschwelle bestimmt, wie gut dein Charakter Schaden widerstehen kann. Schaden bis zu deiner Wundschwelle ist zwar schmerzhaft, aber noch nicht wirklich gef\u00e4hrlich. Erst Schadensmengen \u00fcber deiner Wundschwelle k\u00f6nnen deinen Charakter beeintr\u00e4chtigen oder sogar t\u00f6ten.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("formAttribute", u"Wundschwelle", None))
        self.label_9.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_24.setText(QCoreApplication.translate("formAttribute", u"CH", None))
        self.label_28.setText(QCoreApplication.translate("formAttribute", u"GS", None))
        self.label_28.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
#if QT_CONFIG(tooltip)
        self.label_8.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Fingerfertigkeit ist die manuelle Geschicklichkeit deines Charakters. Er verf\u00fcgt \u00fcber eine gute Hand-Augen-Koordination und kann feine Bewegungen schnell und fehlerfrei ausf\u00fchren. Handwerker, Fernk\u00e4mpfer und Hersteller von Artefakten sollten deswegen nicht auf eine hohe Fingerfertigkeit verzichten.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("formAttribute", u"Fingerfertigkeit", None))
        self.label_8.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.lblKapZugekauft.setText(QCoreApplication.translate("formAttribute", u"Karmaenergie", None))
        self.lblKapZugekauft.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_104.setText(QCoreApplication.translate("formAttribute", u"(IN)", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Konstitution beschreibt die Widerstandsf\u00e4higkeit deines Charakters gegen \u00e4u\u00dfere Einfl\u00fcsse wie Strapazen, Gifte, Krankheiten und Verwundungen. Die Konstitution beeinflusst nur wenige Fertigkeiten, bestimmt aber deine Wundschwelle, den wohl wichtigsten Basiswert.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("formAttribute", u"Konstitution", None))
        self.label.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_100.setText(QCoreApplication.translate("formAttribute", u"(4 + 1 je 4 KO)", None))
        self.label_34.setText(QCoreApplication.translate("formAttribute", u"+", None))
        self.labelWert.setText(QCoreApplication.translate("formAttribute", u"Wert", None))
        self.labelWert.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.label_102.setText(QCoreApplication.translate("formAttribute", u"(4 + 1 je 4 GE)", None))
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Charisma ist die nat\u00fcrliche Ausstrahlung deines Charakters auf seine Umgebung. Es steht f\u00fcr F\u00fchrungsqualit\u00e4ten, Selbstbewusstsein, \u00dcberzeugungskraft und ein gewinnendes Wesen. Alle gesellschaftlichen Fertigkeiten h\u00e4ngen von deinem Charisma ab und auch Elementaristen ben\u00f6tigen ein hohes Charisma.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("formAttribute", u"Charisma", None))
        self.label_7.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
#if QT_CONFIG(tooltip)
        self.label_13.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Die Initiative steht f\u00fcr Reaktionsgeschwindigkeit und \u00dcbersicht im Kampf. K\u00e4mpfer mit hoher Initiative k\u00f6nnen zu Beginn eines Kampfes schneller handeln und so den Erstschlag f\u00fchren. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("formAttribute", u"Initiative", None))
        self.label_13.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_101.setText(QCoreApplication.translate("formAttribute", u"(4 + 1 je 4 MU)", None))
#if QT_CONFIG(tooltip)
        self.label_10.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Die Magieresistenz ist die Widerstandsf\u00e4higkeit gegen Zauberei. Viele Zauber wirken nur auf deinen Charakter, wenn sie seine Magieresistenz in einer vergleichenden Probe \u00fcberwinden.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("formAttribute", u"Magieresistenz", None))
        self.label_10.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_29.setText(QCoreApplication.translate("formAttribute", u"SB", None))
        self.label_29.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
        self.label_103.setText(QCoreApplication.translate("formAttribute", u"(1 je 4 KK)", None))
        self.label_31.setText(QCoreApplication.translate("formAttribute", u"AsP", None))
        self.label_31.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Klugheit ist das logische Denkverm\u00f6gen deines Charakters und seine F\u00e4higkeit, komplizierte Zusammenh\u00e4nge zu erkennen und zu analysieren. Kluge Charaktere verf\u00fcgen auch \u00fcber ein gutes Allgemeinwissen. Eine hohe Klugheit ist bei vielen gesellschaftlichen und allen Wissensfertigkeiten unverzichtbar.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("formAttribute", u"Klugheit", None))
        self.label_6.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_30.setText(QCoreApplication.translate("formAttribute", u"INI", None))
        self.label_30.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
        self.label_18.setText(QCoreApplication.translate("formAttribute", u"KO", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>K\u00f6rperkraft ist ein Ma\u00df f\u00fcr die St\u00e4rke deines Charakters. Kr\u00e4ftige Charaktere k\u00f6nnen schwere Lasten heben und ihre Angriffe richten durch den h\u00f6heren Schadensbonus mehr Schaden an. Dadurch ist eine hohe K\u00f6rperkraft gerade f\u00fcr k\u00e4mpferische Charaktere hilfreich.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("formAttribute", u"K\u00f6rperkraft", None))
        self.label_4.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
#if QT_CONFIG(tooltip)
        self.labelPW.setToolTip(QCoreApplication.translate("formAttribute", u"Probenwert", None))
#endif // QT_CONFIG(tooltip)
        self.labelPW.setText(QCoreApplication.translate("formAttribute", u"PW", None))
        self.labelPW.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.lblKap.setText(QCoreApplication.translate("formAttribute", u"KaP", None))
        self.lblKap.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
        self.label_27.setText(QCoreApplication.translate("formAttribute", u"MR", None))
        self.label_27.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
        self.spinAsP.setPrefix("")
        self.label_15.setText(QCoreApplication.translate("formAttribute", u"zugekauft", None))
        self.labelKostenAsP.setText(QCoreApplication.translate("formAttribute", u"(0 EP)", None))
        self.labelFormel.setText(QCoreApplication.translate("formAttribute", u"Formel", None))
        self.labelFormel.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
#if QT_CONFIG(tooltip)
        self.label_12.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Hohe K\u00f6rperkraft erh\u00f6ht den Waffenschaden bei allen Angriffen mit Nahkampf- und Wurfwaffen. Kopflastige Waffen profitieren sogar doppelt vom Schadensbonus.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("formAttribute", u"Schadensbonus", None))
        self.label_12.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_25.setText(QCoreApplication.translate("formAttribute", u"FF", None))
        self.labelWert2.setText(QCoreApplication.translate("formAttribute", u"Wert", None))
        self.labelWert2.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Ein mutiger Charakter bewahrt in kritischen Situationen einen k\u00fchlen Kopf und schreckt nicht vor Gefahren zur\u00fcck, was gerade im Nahkampf unerl\u00e4sslich ist. Zus\u00e4tzlich st\u00e4rkt Mut den Widerstand gegen magische Beeinflussungen, indem er deine Magieresistenz erh\u00f6ht. Auch D\u00e4monologen ben\u00f6tigen einen hohen Mut.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("formAttribute", u"Mut", None))
        self.label_2.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_23.setText(QCoreApplication.translate("formAttribute", u"KL", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("formAttribute", u"<html><head/><body><p>Gewandtheit ist die Beweglichkeit und Gelenkigkeit deines Charakters. Gewandte Charaktere bewegen sich geschmeidig und k\u00f6nnen ihre Bewegungen gut absch\u00e4tzen. Das f\u00f6rdert deine k\u00f6rperlichen und k\u00e4mpferischen Fertigkeiten und erh\u00f6ht deine Geschwindigkeit.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("formAttribute", u"Gewandheit", None))
        self.label_3.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_26.setText(QCoreApplication.translate("formAttribute", u"WS", None))
        self.label_26.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
        self.label_22.setText(QCoreApplication.translate("formAttribute", u"IN", None))
        self.labelKosten.setText(QCoreApplication.translate("formAttribute", u"Kosten", None))
        self.labelKosten.setProperty("class", QCoreApplication.translate("formAttribute", u"h2", None))
        self.labelKostenKO.setText(QCoreApplication.translate("formAttribute", u"16 EP", None))
        self.labelKostenMU.setText("")
        self.labelKostenGE.setText("")
        self.labelKostenKK.setText("")
        self.labelKostenIN.setText("")
        self.labelKostenCH.setText("")
        self.labelKostenFF.setText("")
        self.labelKostenKL.setText("")
        self.label_16.setText(QCoreApplication.translate("formAttribute", u"Durchhalteverm\u00f6gen", None))
        self.label_16.setProperty("class", QCoreApplication.translate("formAttribute", u"h4", None))
        self.label_17.setText(QCoreApplication.translate("formAttribute", u"DH", None))
        self.label_17.setProperty("class", QCoreApplication.translate("formAttribute", u"italic", None))
        self.label_35.setText(QCoreApplication.translate("formAttribute", u"(KO)", None))
    # retranslateUi

