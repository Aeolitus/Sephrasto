# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterWaffen.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_formWaffen(object):
    def setupUi(self, formWaffen):
        if not formWaffen.objectName():
            formWaffen.setObjectName(u"formWaffen")
        formWaffen.resize(1198, 889)
        formWaffen.setMinimumSize(QSize(802, 0))
        self.verticalLayout = QVBoxLayout(formWaffen)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.Waffen = QGridLayout()
        self.Waffen.setObjectName(u"Waffen")
        self.Waffen.setVerticalSpacing(0)
        self.labelW8LeftFrame = QLabel(formWaffen)
        self.labelW8LeftFrame.setObjectName(u"labelW8LeftFrame")
        self.labelW8LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW8LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW8LeftFrame, 31, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.buttonW4Up = QPushButton(formWaffen)
        self.buttonW4Up.setObjectName(u"buttonW4Up")

        self.verticalLayout_5.addWidget(self.buttonW4Up)

        self.buttonW4Down = QPushButton(formWaffen)
        self.buttonW4Down.setObjectName(u"buttonW4Down")

        self.verticalLayout_5.addWidget(self.buttonW4Down)


        self.Waffen.addLayout(self.verticalLayout_5, 15, 11, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(8)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.spinW7w6 = QSpinBox(formWaffen)
        self.spinW7w6.setObjectName(u"spinW7w6")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinW7w6.sizePolicy().hasHeightForWidth())
        self.spinW7w6.setSizePolicy(sizePolicy)
        self.spinW7w6.setMinimumSize(QSize(25, 0))
        self.spinW7w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW7w6.setAlignment(Qt.AlignCenter)
        self.spinW7w6.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_12.addWidget(self.spinW7w6)

        self.labelW7seiten = QLabel(formWaffen)
        self.labelW7seiten.setObjectName(u"labelW7seiten")

        self.horizontalLayout_12.addWidget(self.labelW7seiten)

        self.spinW7plus = QSpinBox(formWaffen)
        self.spinW7plus.setObjectName(u"spinW7plus")
        sizePolicy.setHeightForWidth(self.spinW7plus.sizePolicy().hasHeightForWidth())
        self.spinW7plus.setSizePolicy(sizePolicy)
        self.spinW7plus.setMinimumSize(QSize(25, 0))
        self.spinW7plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW7plus.setAlignment(Qt.AlignCenter)
        self.spinW7plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW7plus.setMinimum(-99)

        self.horizontalLayout_12.addWidget(self.spinW7plus)


        self.Waffen.addLayout(self.horizontalLayout_12, 27, 2, 1, 1)

        self.labelW7RightFrame = QLabel(formWaffen)
        self.labelW7RightFrame.setObjectName(u"labelW7RightFrame")
        self.labelW7RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW7RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW7RightFrame, 27, 13, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

        self.editW3eig = QLineEdit(formWaffen)
        self.editW3eig.setObjectName(u"editW3eig")

        self.Waffen.addWidget(self.editW3eig, 11, 7, 1, 1)

        self.labelW3TopFrame = QLabel(formWaffen)
        self.labelW3TopFrame.setObjectName(u"labelW3TopFrame")
        self.labelW3TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW3TopFrame, 10, 0, 1, 14)

        self.spinW4lz = QSpinBox(formWaffen)
        self.spinW4lz.setObjectName(u"spinW4lz")
        self.spinW4lz.setMinimumSize(QSize(44, 0))
        self.spinW4lz.setAlignment(Qt.AlignCenter)
        self.spinW4lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW4lz.setMinimum(0)
        self.spinW4lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW4lz, 15, 5, 1, 1)

        self.labelContainerW8 = QWidget(formWaffen)
        self.labelContainerW8.setObjectName(u"labelContainerW8")
        self.horizontalLayout_18 = QHBoxLayout(self.labelContainerW8)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.labelW8Basis = QLabel(self.labelContainerW8)
        self.labelW8Basis.setObjectName(u"labelW8Basis")
        self.labelW8Basis.setMinimumSize(QSize(0, 30))
        self.labelW8Basis.setMargin(0)
        self.labelW8Basis.setIndent(14)

        self.horizontalLayout_18.addWidget(self.labelW8Basis)

        self.labelW8Werte = QLabel(self.labelContainerW8)
        self.labelW8Werte.setObjectName(u"labelW8Werte")
        self.labelW8Werte.setMinimumSize(QSize(0, 30))
        self.labelW8Werte.setIndent(14)

        self.horizontalLayout_18.addWidget(self.labelW8Werte)

        self.labelW8Mods = QLabel(self.labelContainerW8)
        self.labelW8Mods.setObjectName(u"labelW8Mods")
        self.labelW8Mods.setMinimumSize(QSize(0, 30))
        self.labelW8Mods.setIndent(14)

        self.horizontalLayout_18.addWidget(self.labelW8Mods)

        self.horizontalSpacer_9 = QSpacerItem(467, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_9)


        self.Waffen.addWidget(self.labelContainerW8, 32, 0, 1, 14)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spinW1w6 = QSpinBox(formWaffen)
        self.spinW1w6.setObjectName(u"spinW1w6")
        sizePolicy.setHeightForWidth(self.spinW1w6.sizePolicy().hasHeightForWidth())
        self.spinW1w6.setSizePolicy(sizePolicy)
        self.spinW1w6.setMinimumSize(QSize(25, 0))
        self.spinW1w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW1w6.setAlignment(Qt.AlignCenter)
        self.spinW1w6.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_3.addWidget(self.spinW1w6)

        self.labelW1seiten = QLabel(formWaffen)
        self.labelW1seiten.setObjectName(u"labelW1seiten")

        self.horizontalLayout_3.addWidget(self.labelW1seiten)

        self.spinW1plus = QSpinBox(formWaffen)
        self.spinW1plus.setObjectName(u"spinW1plus")
        sizePolicy.setHeightForWidth(self.spinW1plus.sizePolicy().hasHeightForWidth())
        self.spinW1plus.setSizePolicy(sizePolicy)
        self.spinW1plus.setMinimumSize(QSize(25, 0))
        self.spinW1plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW1plus.setAlignment(Qt.AlignCenter)
        self.spinW1plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW1plus.setMinimum(-99)

        self.horizontalLayout_3.addWidget(self.spinW1plus)


        self.Waffen.addLayout(self.horizontalLayout_3, 3, 2, 1, 1)

        self.spinW6wm = QSpinBox(formWaffen)
        self.spinW6wm.setObjectName(u"spinW6wm")
        self.spinW6wm.setMinimumSize(QSize(44, 0))
        self.spinW6wm.setAlignment(Qt.AlignCenter)
        self.spinW6wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW6wm.setMinimum(-99)
        self.spinW6wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW6wm, 23, 4, 1, 1)

        self.spinW1wm = QSpinBox(formWaffen)
        self.spinW1wm.setObjectName(u"spinW1wm")
        self.spinW1wm.setMinimumSize(QSize(44, 0))
        self.spinW1wm.setAlignment(Qt.AlignCenter)
        self.spinW1wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW1wm.setMinimum(-99)
        self.spinW1wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW1wm, 3, 4, 1, 1)

        self.labelContainerW2 = QWidget(formWaffen)
        self.labelContainerW2.setObjectName(u"labelContainerW2")
        self.horizontalLayout_5 = QHBoxLayout(self.labelContainerW2)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.labelW2Basis = QLabel(self.labelContainerW2)
        self.labelW2Basis.setObjectName(u"labelW2Basis")
        self.labelW2Basis.setMinimumSize(QSize(0, 30))
        self.labelW2Basis.setMargin(0)
        self.labelW2Basis.setIndent(14)

        self.horizontalLayout_5.addWidget(self.labelW2Basis)

        self.labelW2Werte = QLabel(self.labelContainerW2)
        self.labelW2Werte.setObjectName(u"labelW2Werte")
        self.labelW2Werte.setMinimumSize(QSize(0, 30))
        self.labelW2Werte.setIndent(14)

        self.horizontalLayout_5.addWidget(self.labelW2Werte)

        self.labelW2Mods = QLabel(self.labelContainerW2)
        self.labelW2Mods.setObjectName(u"labelW2Mods")
        self.labelW2Mods.setMinimumSize(QSize(0, 30))
        self.labelW2Mods.setIndent(14)

        self.horizontalLayout_5.addWidget(self.labelW2Mods)

        self.horizontalSpacer_3 = QSpacerItem(467, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.Waffen.addWidget(self.labelContainerW2, 8, 0, 1, 14)

        self.labelHaerte = QLabel(formWaffen)
        self.labelHaerte.setObjectName(u"labelHaerte")
        font = QFont()
        font.setBold(True)
        self.labelHaerte.setFont(font)
        self.labelHaerte.setAlignment(Qt.AlignCenter)

        self.Waffen.addWidget(self.labelHaerte, 0, 6, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(8)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.spinW8w6 = QSpinBox(formWaffen)
        self.spinW8w6.setObjectName(u"spinW8w6")
        sizePolicy.setHeightForWidth(self.spinW8w6.sizePolicy().hasHeightForWidth())
        self.spinW8w6.setSizePolicy(sizePolicy)
        self.spinW8w6.setMinimumSize(QSize(25, 0))
        self.spinW8w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW8w6.setAlignment(Qt.AlignCenter)
        self.spinW8w6.setReadOnly(False)
        self.spinW8w6.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW8w6.setValue(0)

        self.horizontalLayout_13.addWidget(self.spinW8w6)

        self.labelW8seiten = QLabel(formWaffen)
        self.labelW8seiten.setObjectName(u"labelW8seiten")

        self.horizontalLayout_13.addWidget(self.labelW8seiten)

        self.spinW8plus = QSpinBox(formWaffen)
        self.spinW8plus.setObjectName(u"spinW8plus")
        sizePolicy.setHeightForWidth(self.spinW8plus.sizePolicy().hasHeightForWidth())
        self.spinW8plus.setSizePolicy(sizePolicy)
        self.spinW8plus.setMinimumSize(QSize(25, 0))
        self.spinW8plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW8plus.setAlignment(Qt.AlignCenter)
        self.spinW8plus.setReadOnly(False)
        self.spinW8plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW8plus.setMinimum(-99)

        self.horizontalLayout_13.addWidget(self.spinW8plus)


        self.Waffen.addLayout(self.horizontalLayout_13, 31, 2, 1, 1)

        self.spinW4h = QSpinBox(formWaffen)
        self.spinW4h.setObjectName(u"spinW4h")
        self.spinW4h.setMinimumSize(QSize(44, 0))
        self.spinW4h.setAlignment(Qt.AlignCenter)
        self.spinW4h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW4h.setMinimum(0)
        self.spinW4h.setMaximum(99)
        self.spinW4h.setValue(6)

        self.Waffen.addWidget(self.spinW4h, 15, 6, 1, 1)

        self.spinW3lz = QSpinBox(formWaffen)
        self.spinW3lz.setObjectName(u"spinW3lz")
        self.spinW3lz.setMinimumSize(QSize(44, 0))
        self.spinW3lz.setAlignment(Qt.AlignCenter)
        self.spinW3lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW3lz.setMinimum(0)
        self.spinW3lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW3lz, 11, 5, 1, 1)

        self.spinW2h = QSpinBox(formWaffen)
        self.spinW2h.setObjectName(u"spinW2h")
        self.spinW2h.setMinimumSize(QSize(44, 0))
        self.spinW2h.setAlignment(Qt.AlignCenter)
        self.spinW2h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW2h.setMinimum(0)
        self.spinW2h.setMaximum(99)
        self.spinW2h.setValue(6)

        self.Waffen.addWidget(self.spinW2h, 7, 6, 1, 1)

        self.comboStil5 = QComboBox(formWaffen)
        self.comboStil5.setObjectName(u"comboStil5")
        self.comboStil5.setMinimumSize(QSize(160, 0))
        self.comboStil5.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil5, 19, 9, 1, 1)

        self.spinW2rw = QSpinBox(formWaffen)
        self.spinW2rw.setObjectName(u"spinW2rw")
        self.spinW2rw.setMinimumSize(QSize(44, 0))
        self.spinW2rw.setAlignment(Qt.AlignCenter)
        self.spinW2rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW2rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW2rw, 7, 3, 1, 1)

        self.labelContainerW7 = QWidget(formWaffen)
        self.labelContainerW7.setObjectName(u"labelContainerW7")
        self.horizontalLayout_17 = QHBoxLayout(self.labelContainerW7)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.labelW7Basis = QLabel(self.labelContainerW7)
        self.labelW7Basis.setObjectName(u"labelW7Basis")
        self.labelW7Basis.setMinimumSize(QSize(0, 30))
        self.labelW7Basis.setMargin(0)
        self.labelW7Basis.setIndent(14)

        self.horizontalLayout_17.addWidget(self.labelW7Basis)

        self.labelW7Werte = QLabel(self.labelContainerW7)
        self.labelW7Werte.setObjectName(u"labelW7Werte")
        self.labelW7Werte.setMinimumSize(QSize(0, 30))
        self.labelW7Werte.setIndent(14)

        self.horizontalLayout_17.addWidget(self.labelW7Werte)

        self.labelW7Mods = QLabel(self.labelContainerW7)
        self.labelW7Mods.setObjectName(u"labelW7Mods")
        self.labelW7Mods.setMinimumSize(QSize(0, 30))
        self.labelW7Mods.setIndent(14)

        self.horizontalLayout_17.addWidget(self.labelW7Mods)

        self.horizontalSpacer_8 = QSpacerItem(467, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_8)


        self.Waffen.addWidget(self.labelContainerW7, 28, 0, 1, 14)

        self.spinW7lz = QSpinBox(formWaffen)
        self.spinW7lz.setObjectName(u"spinW7lz")
        self.spinW7lz.setMinimumSize(QSize(44, 0))
        self.spinW7lz.setAlignment(Qt.AlignCenter)
        self.spinW7lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW7lz.setMinimum(0)
        self.spinW7lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW7lz, 27, 5, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.spinW3w6 = QSpinBox(formWaffen)
        self.spinW3w6.setObjectName(u"spinW3w6")
        sizePolicy.setHeightForWidth(self.spinW3w6.sizePolicy().hasHeightForWidth())
        self.spinW3w6.setSizePolicy(sizePolicy)
        self.spinW3w6.setMinimumSize(QSize(25, 0))
        self.spinW3w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW3w6.setAlignment(Qt.AlignCenter)
        self.spinW3w6.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_7.addWidget(self.spinW3w6)

        self.labelW3seiten = QLabel(formWaffen)
        self.labelW3seiten.setObjectName(u"labelW3seiten")

        self.horizontalLayout_7.addWidget(self.labelW3seiten)

        self.spinW3plus = QSpinBox(formWaffen)
        self.spinW3plus.setObjectName(u"spinW3plus")
        sizePolicy.setHeightForWidth(self.spinW3plus.sizePolicy().hasHeightForWidth())
        self.spinW3plus.setSizePolicy(sizePolicy)
        self.spinW3plus.setMinimumSize(QSize(25, 0))
        self.spinW3plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW3plus.setAlignment(Qt.AlignCenter)
        self.spinW3plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW3plus.setMinimum(-99)

        self.horizontalLayout_7.addWidget(self.spinW3plus)


        self.Waffen.addLayout(self.horizontalLayout_7, 11, 2, 1, 1)

        self.labelContainerW5 = QWidget(formWaffen)
        self.labelContainerW5.setObjectName(u"labelContainerW5")
        self.horizontalLayout_15 = QHBoxLayout(self.labelContainerW5)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.labelW5Basis = QLabel(self.labelContainerW5)
        self.labelW5Basis.setObjectName(u"labelW5Basis")
        self.labelW5Basis.setMinimumSize(QSize(0, 30))
        self.labelW5Basis.setMargin(0)
        self.labelW5Basis.setIndent(14)

        self.horizontalLayout_15.addWidget(self.labelW5Basis)

        self.labelW5Werte = QLabel(self.labelContainerW5)
        self.labelW5Werte.setObjectName(u"labelW5Werte")
        self.labelW5Werte.setMinimumSize(QSize(0, 30))
        self.labelW5Werte.setIndent(14)

        self.horizontalLayout_15.addWidget(self.labelW5Werte)

        self.labelW5Mods = QLabel(self.labelContainerW5)
        self.labelW5Mods.setObjectName(u"labelW5Mods")
        self.labelW5Mods.setMinimumSize(QSize(0, 30))
        self.labelW5Mods.setIndent(14)

        self.horizontalLayout_15.addWidget(self.labelW5Mods)

        self.horizontalSpacer_6 = QSpacerItem(467, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_6)


        self.Waffen.addWidget(self.labelContainerW5, 20, 0, 1, 14)

        self.labelContainerW6 = QWidget(formWaffen)
        self.labelContainerW6.setObjectName(u"labelContainerW6")
        self.horizontalLayout_16 = QHBoxLayout(self.labelContainerW6)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.labelW6Basis = QLabel(self.labelContainerW6)
        self.labelW6Basis.setObjectName(u"labelW6Basis")
        self.labelW6Basis.setMinimumSize(QSize(0, 30))
        self.labelW6Basis.setMargin(0)
        self.labelW6Basis.setIndent(14)

        self.horizontalLayout_16.addWidget(self.labelW6Basis)

        self.labelW6Werte = QLabel(self.labelContainerW6)
        self.labelW6Werte.setObjectName(u"labelW6Werte")
        self.labelW6Werte.setMinimumSize(QSize(0, 30))
        self.labelW6Werte.setIndent(14)

        self.horizontalLayout_16.addWidget(self.labelW6Werte)

        self.labelW6Mods = QLabel(self.labelContainerW6)
        self.labelW6Mods.setObjectName(u"labelW6Mods")
        self.labelW6Mods.setMinimumSize(QSize(0, 30))
        self.labelW6Mods.setIndent(14)

        self.horizontalLayout_16.addWidget(self.labelW6Mods)

        self.horizontalSpacer_7 = QSpacerItem(467, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_7)


        self.Waffen.addWidget(self.labelContainerW6, 24, 0, 1, 14)

        self.labelWName = QLabel(formWaffen)
        self.labelWName.setObjectName(u"labelWName")
        self.labelWName.setFont(font)

        self.Waffen.addWidget(self.labelWName, 0, 1, 1, 1)

        self.labelW2RightFrame = QLabel(formWaffen)
        self.labelW2RightFrame.setObjectName(u"labelW2RightFrame")
        self.labelW2RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW2RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW2RightFrame, 7, 13, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_5, 13, 1, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(8)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.spinW2w6 = QSpinBox(formWaffen)
        self.spinW2w6.setObjectName(u"spinW2w6")
        sizePolicy.setHeightForWidth(self.spinW2w6.sizePolicy().hasHeightForWidth())
        self.spinW2w6.setSizePolicy(sizePolicy)
        self.spinW2w6.setMinimumSize(QSize(25, 0))
        self.spinW2w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW2w6.setAlignment(Qt.AlignCenter)
        self.spinW2w6.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_11.addWidget(self.spinW2w6)

        self.labelW2seiten = QLabel(formWaffen)
        self.labelW2seiten.setObjectName(u"labelW2seiten")

        self.horizontalLayout_11.addWidget(self.labelW2seiten)

        self.spinW2plus = QSpinBox(formWaffen)
        self.spinW2plus.setObjectName(u"spinW2plus")
        sizePolicy.setHeightForWidth(self.spinW2plus.sizePolicy().hasHeightForWidth())
        self.spinW2plus.setSizePolicy(sizePolicy)
        self.spinW2plus.setMinimumSize(QSize(25, 0))
        self.spinW2plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW2plus.setAlignment(Qt.AlignCenter)
        self.spinW2plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW2plus.setMinimum(-99)

        self.horizontalLayout_11.addWidget(self.spinW2plus)


        self.Waffen.addLayout(self.horizontalLayout_11, 7, 2, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.buttonW7Up = QPushButton(formWaffen)
        self.buttonW7Up.setObjectName(u"buttonW7Up")

        self.verticalLayout_8.addWidget(self.buttonW7Up)

        self.buttonW7Down = QPushButton(formWaffen)
        self.buttonW7Down.setObjectName(u"buttonW7Down")

        self.verticalLayout_8.addWidget(self.buttonW7Down)


        self.Waffen.addLayout(self.verticalLayout_8, 27, 11, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_10, 1, 1, 1, 1)

        self.spinW1lz = QSpinBox(formWaffen)
        self.spinW1lz.setObjectName(u"spinW1lz")
        self.spinW1lz.setMinimumSize(QSize(44, 0))
        self.spinW1lz.setAlignment(Qt.AlignCenter)
        self.spinW1lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW1lz.setMinimum(0)
        self.spinW1lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW1lz, 3, 5, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_7, 21, 1, 1, 1)

        self.spinW4wm = QSpinBox(formWaffen)
        self.spinW4wm.setObjectName(u"spinW4wm")
        self.spinW4wm.setMinimumSize(QSize(44, 0))
        self.spinW4wm.setAlignment(Qt.AlignCenter)
        self.spinW4wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW4wm.setMinimum(-99)
        self.spinW4wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW4wm, 15, 4, 1, 1)

        self.addW6 = QPushButton(formWaffen)
        self.addW6.setObjectName(u"addW6")

        self.Waffen.addWidget(self.addW6, 23, 12, 1, 1)

        self.addW3 = QPushButton(formWaffen)
        self.addW3.setObjectName(u"addW3")

        self.Waffen.addWidget(self.addW3, 11, 12, 1, 1)

        self.spinW7h = QSpinBox(formWaffen)
        self.spinW7h.setObjectName(u"spinW7h")
        self.spinW7h.setMinimumSize(QSize(44, 0))
        self.spinW7h.setAlignment(Qt.AlignCenter)
        self.spinW7h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW7h.setMinimum(0)
        self.spinW7h.setMaximum(99)
        self.spinW7h.setValue(6)

        self.Waffen.addWidget(self.spinW7h, 27, 6, 1, 1)

        self.editW3name = QLineEdit(formWaffen)
        self.editW3name.setObjectName(u"editW3name")
        self.editW3name.setMaximumSize(QSize(200, 16777215))

        self.Waffen.addWidget(self.editW3name, 11, 1, 1, 1)

        self.addW1 = QPushButton(formWaffen)
        self.addW1.setObjectName(u"addW1")

        self.Waffen.addWidget(self.addW1, 3, 12, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.buttonW3Up = QPushButton(formWaffen)
        self.buttonW3Up.setObjectName(u"buttonW3Up")

        self.verticalLayout_4.addWidget(self.buttonW3Up)

        self.buttonW3Down = QPushButton(formWaffen)
        self.buttonW3Down.setObjectName(u"buttonW3Down")

        self.verticalLayout_4.addWidget(self.buttonW3Down)


        self.Waffen.addLayout(self.verticalLayout_4, 11, 11, 1, 1)

        self.spinW6rw = QSpinBox(formWaffen)
        self.spinW6rw.setObjectName(u"spinW6rw")
        self.spinW6rw.setMinimumSize(QSize(44, 0))
        self.spinW6rw.setAlignment(Qt.AlignCenter)
        self.spinW6rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW6rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW6rw, 23, 3, 1, 1)

        self.labelContainerW1 = QWidget(formWaffen)
        self.labelContainerW1.setObjectName(u"labelContainerW1")
        self.horizontalLayout_2 = QHBoxLayout(self.labelContainerW1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelW1Basis = QLabel(self.labelContainerW1)
        self.labelW1Basis.setObjectName(u"labelW1Basis")
        self.labelW1Basis.setMinimumSize(QSize(0, 30))
        self.labelW1Basis.setMargin(0)
        self.labelW1Basis.setIndent(14)

        self.horizontalLayout_2.addWidget(self.labelW1Basis)

        self.labelW1Werte = QLabel(self.labelContainerW1)
        self.labelW1Werte.setObjectName(u"labelW1Werte")
        self.labelW1Werte.setMinimumSize(QSize(0, 30))
        self.labelW1Werte.setIndent(14)

        self.horizontalLayout_2.addWidget(self.labelW1Werte)

        self.labelW1Mods = QLabel(self.labelContainerW1)
        self.labelW1Mods.setObjectName(u"labelW1Mods")
        self.labelW1Mods.setMinimumSize(QSize(0, 30))
        self.labelW1Mods.setIndent(14)

        self.horizontalLayout_2.addWidget(self.labelW1Mods)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.Waffen.addWidget(self.labelContainerW1, 4, 0, 1, 14)

        self.editW5name = QLineEdit(formWaffen)
        self.editW5name.setObjectName(u"editW5name")
        self.editW5name.setMaximumSize(QSize(200, 16777215))

        self.Waffen.addWidget(self.editW5name, 19, 1, 1, 1)

        self.editW1name = QLineEdit(formWaffen)
        self.editW1name.setObjectName(u"editW1name")
        self.editW1name.setMaximumSize(QSize(200, 16777215))

        self.Waffen.addWidget(self.editW1name, 3, 1, 1, 1)

        self.labelW7LeftFrame = QLabel(formWaffen)
        self.labelW7LeftFrame.setObjectName(u"labelW7LeftFrame")
        self.labelW7LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW7LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW7LeftFrame, 27, 0, 1, 1)

        self.comboStil1 = QComboBox(formWaffen)
        self.comboStil1.setObjectName(u"comboStil1")
        self.comboStil1.setMinimumSize(QSize(160, 0))
        self.comboStil1.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil1, 3, 9, 1, 1)

        self.editW4eig = QLineEdit(formWaffen)
        self.editW4eig.setObjectName(u"editW4eig")

        self.Waffen.addWidget(self.editW4eig, 15, 7, 1, 1)

        self.labelW5LeftFrame = QLabel(formWaffen)
        self.labelW5LeftFrame.setObjectName(u"labelW5LeftFrame")
        self.labelW5LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW5LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW5LeftFrame, 19, 0, 1, 1)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.buttonW8Up = QPushButton(formWaffen)
        self.buttonW8Up.setObjectName(u"buttonW8Up")

        self.verticalLayout_9.addWidget(self.buttonW8Up)

        self.verticalSpacer_11 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_9.addItem(self.verticalSpacer_11)


        self.Waffen.addLayout(self.verticalLayout_9, 31, 11, 1, 1)

        self.spinW5rw = QSpinBox(formWaffen)
        self.spinW5rw.setObjectName(u"spinW5rw")
        self.spinW5rw.setMinimumSize(QSize(44, 0))
        self.spinW5rw.setAlignment(Qt.AlignCenter)
        self.spinW5rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW5rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW5rw, 19, 3, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(8)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.spinW6w6 = QSpinBox(formWaffen)
        self.spinW6w6.setObjectName(u"spinW6w6")
        sizePolicy.setHeightForWidth(self.spinW6w6.sizePolicy().hasHeightForWidth())
        self.spinW6w6.setSizePolicy(sizePolicy)
        self.spinW6w6.setMinimumSize(QSize(25, 0))
        self.spinW6w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW6w6.setAlignment(Qt.AlignCenter)
        self.spinW6w6.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_10.addWidget(self.spinW6w6)

        self.labelW6seiten = QLabel(formWaffen)
        self.labelW6seiten.setObjectName(u"labelW6seiten")

        self.horizontalLayout_10.addWidget(self.labelW6seiten)

        self.spinW6plus = QSpinBox(formWaffen)
        self.spinW6plus.setObjectName(u"spinW6plus")
        sizePolicy.setHeightForWidth(self.spinW6plus.sizePolicy().hasHeightForWidth())
        self.spinW6plus.setSizePolicy(sizePolicy)
        self.spinW6plus.setMinimumSize(QSize(25, 0))
        self.spinW6plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW6plus.setAlignment(Qt.AlignCenter)
        self.spinW6plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW6plus.setMinimum(-99)

        self.horizontalLayout_10.addWidget(self.spinW6plus)


        self.Waffen.addLayout(self.horizontalLayout_10, 23, 2, 1, 1)

        self.spinW7wm = QSpinBox(formWaffen)
        self.spinW7wm.setObjectName(u"spinW7wm")
        self.spinW7wm.setMinimumSize(QSize(44, 0))
        self.spinW7wm.setAlignment(Qt.AlignCenter)
        self.spinW7wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW7wm.setMinimum(-99)
        self.spinW7wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW7wm, 27, 4, 1, 1)

        self.addW2 = QPushButton(formWaffen)
        self.addW2.setObjectName(u"addW2")

        self.Waffen.addWidget(self.addW2, 7, 12, 1, 1)

        self.comboStil2 = QComboBox(formWaffen)
        self.comboStil2.setObjectName(u"comboStil2")
        self.comboStil2.setMinimumSize(QSize(160, 0))
        self.comboStil2.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil2, 7, 9, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(8)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.spinW5w6 = QSpinBox(formWaffen)
        self.spinW5w6.setObjectName(u"spinW5w6")
        sizePolicy.setHeightForWidth(self.spinW5w6.sizePolicy().hasHeightForWidth())
        self.spinW5w6.setSizePolicy(sizePolicy)
        self.spinW5w6.setMinimumSize(QSize(25, 0))
        self.spinW5w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW5w6.setAlignment(Qt.AlignCenter)
        self.spinW5w6.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_9.addWidget(self.spinW5w6)

        self.labelW5seiten = QLabel(formWaffen)
        self.labelW5seiten.setObjectName(u"labelW5seiten")

        self.horizontalLayout_9.addWidget(self.labelW5seiten)

        self.spinW5plus = QSpinBox(formWaffen)
        self.spinW5plus.setObjectName(u"spinW5plus")
        sizePolicy.setHeightForWidth(self.spinW5plus.sizePolicy().hasHeightForWidth())
        self.spinW5plus.setSizePolicy(sizePolicy)
        self.spinW5plus.setMinimumSize(QSize(25, 0))
        self.spinW5plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW5plus.setAlignment(Qt.AlignCenter)
        self.spinW5plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW5plus.setMinimum(-99)

        self.horizontalLayout_9.addWidget(self.spinW5plus)


        self.Waffen.addLayout(self.horizontalLayout_9, 19, 2, 1, 1)

        self.spinW6lz = QSpinBox(formWaffen)
        self.spinW6lz.setObjectName(u"spinW6lz")
        self.spinW6lz.setMinimumSize(QSize(44, 0))
        self.spinW6lz.setAlignment(Qt.AlignCenter)
        self.spinW6lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW6lz.setMinimum(0)
        self.spinW6lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW6lz, 23, 5, 1, 1)

        self.labelW6TopFrame = QLabel(formWaffen)
        self.labelW6TopFrame.setObjectName(u"labelW6TopFrame")
        self.labelW6TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW6TopFrame, 22, 0, 1, 14)

        self.editW1eig = QLineEdit(formWaffen)
        self.editW1eig.setObjectName(u"editW1eig")

        self.Waffen.addWidget(self.editW1eig, 3, 7, 1, 1)

        self.editW5eig = QLineEdit(formWaffen)
        self.editW5eig.setObjectName(u"editW5eig")

        self.Waffen.addWidget(self.editW5eig, 19, 7, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_9, 29, 1, 1, 1)

        self.labelW2TopFrame = QLabel(formWaffen)
        self.labelW2TopFrame.setObjectName(u"labelW2TopFrame")
        self.labelW2TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW2TopFrame, 6, 0, 1, 14)

        self.editW7name = QLineEdit(formWaffen)
        self.editW7name.setObjectName(u"editW7name")
        self.editW7name.setMaximumSize(QSize(200, 16777215))

        self.Waffen.addWidget(self.editW7name, 27, 1, 1, 1)

        self.spinW4rw = QSpinBox(formWaffen)
        self.spinW4rw.setObjectName(u"spinW4rw")
        self.spinW4rw.setMinimumSize(QSize(44, 0))
        self.spinW4rw.setAlignment(Qt.AlignCenter)
        self.spinW4rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW4rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW4rw, 15, 3, 1, 1)

        self.editW6name = QLineEdit(formWaffen)
        self.editW6name.setObjectName(u"editW6name")
        self.editW6name.setMaximumSize(QSize(200, 16777215))

        self.Waffen.addWidget(self.editW6name, 23, 1, 1, 1)

        self.editW8eig = QLineEdit(formWaffen)
        self.editW8eig.setObjectName(u"editW8eig")
        self.editW8eig.setReadOnly(False)

        self.Waffen.addWidget(self.editW8eig, 31, 7, 1, 1)

        self.spinW5h = QSpinBox(formWaffen)
        self.spinW5h.setObjectName(u"spinW5h")
        self.spinW5h.setMinimumSize(QSize(44, 0))
        self.spinW5h.setAlignment(Qt.AlignCenter)
        self.spinW5h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW5h.setMinimum(0)
        self.spinW5h.setMaximum(99)
        self.spinW5h.setValue(6)

        self.Waffen.addWidget(self.spinW5h, 19, 6, 1, 1)

        self.spinW8wm = QSpinBox(formWaffen)
        self.spinW8wm.setObjectName(u"spinW8wm")
        self.spinW8wm.setMinimumSize(QSize(44, 0))
        self.spinW8wm.setAlignment(Qt.AlignCenter)
        self.spinW8wm.setReadOnly(False)
        self.spinW8wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW8wm.setMinimum(-99)
        self.spinW8wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW8wm, 31, 4, 1, 1)

        self.labelW7TopFrame = QLabel(formWaffen)
        self.labelW7TopFrame.setObjectName(u"labelW7TopFrame")
        self.labelW7TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW7TopFrame, 26, 0, 1, 14)

        self.labelW1TopFrame = QLabel(formWaffen)
        self.labelW1TopFrame.setObjectName(u"labelW1TopFrame")
        self.labelW1TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW1TopFrame, 2, 0, 1, 14)

        self.labelTP = QLabel(formWaffen)
        self.labelTP.setObjectName(u"labelTP")
        self.labelTP.setFont(font)
        self.labelTP.setAlignment(Qt.AlignCenter)

        self.Waffen.addWidget(self.labelTP, 0, 2, 1, 1)

        self.labelW2LeftFrame = QLabel(formWaffen)
        self.labelW2LeftFrame.setObjectName(u"labelW2LeftFrame")
        self.labelW2LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW2LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW2LeftFrame, 7, 0, 1, 1)

        self.labelW5TopFrame = QLabel(formWaffen)
        self.labelW5TopFrame.setObjectName(u"labelW5TopFrame")
        self.labelW5TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW5TopFrame, 18, 0, 1, 14)

        self.labelW4TopFrame = QLabel(formWaffen)
        self.labelW4TopFrame.setObjectName(u"labelW4TopFrame")
        self.labelW4TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW4TopFrame, 14, 0, 1, 14)

        self.labelW3RightFrame = QLabel(formWaffen)
        self.labelW3RightFrame.setObjectName(u"labelW3RightFrame")
        self.labelW3RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW3RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW3RightFrame, 11, 13, 1, 1)

        self.labelEigenschaften = QLabel(formWaffen)
        self.labelEigenschaften.setObjectName(u"labelEigenschaften")
        self.labelEigenschaften.setFont(font)

        self.Waffen.addWidget(self.labelEigenschaften, 0, 7, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.buttonW6Up = QPushButton(formWaffen)
        self.buttonW6Up.setObjectName(u"buttonW6Up")

        self.verticalLayout_7.addWidget(self.buttonW6Up)

        self.buttonW6Down = QPushButton(formWaffen)
        self.buttonW6Down.setObjectName(u"buttonW6Down")

        self.verticalLayout_7.addWidget(self.buttonW6Down)


        self.Waffen.addLayout(self.verticalLayout_7, 23, 11, 1, 1)

        self.addW4 = QPushButton(formWaffen)
        self.addW4.setObjectName(u"addW4")

        self.Waffen.addWidget(self.addW4, 15, 12, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(8)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.spinW4w6 = QSpinBox(formWaffen)
        self.spinW4w6.setObjectName(u"spinW4w6")
        sizePolicy.setHeightForWidth(self.spinW4w6.sizePolicy().hasHeightForWidth())
        self.spinW4w6.setSizePolicy(sizePolicy)
        self.spinW4w6.setMinimumSize(QSize(25, 0))
        self.spinW4w6.setMaximumSize(QSize(16777215, 16777215))
        self.spinW4w6.setAlignment(Qt.AlignCenter)
        self.spinW4w6.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout_8.addWidget(self.spinW4w6)

        self.labelW4seiten = QLabel(formWaffen)
        self.labelW4seiten.setObjectName(u"labelW4seiten")

        self.horizontalLayout_8.addWidget(self.labelW4seiten)

        self.spinW4plus = QSpinBox(formWaffen)
        self.spinW4plus.setObjectName(u"spinW4plus")
        sizePolicy.setHeightForWidth(self.spinW4plus.sizePolicy().hasHeightForWidth())
        self.spinW4plus.setSizePolicy(sizePolicy)
        self.spinW4plus.setMinimumSize(QSize(25, 0))
        self.spinW4plus.setMaximumSize(QSize(16777215, 16777215))
        self.spinW4plus.setAlignment(Qt.AlignCenter)
        self.spinW4plus.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinW4plus.setMinimum(-99)

        self.horizontalLayout_8.addWidget(self.spinW4plus)


        self.Waffen.addLayout(self.horizontalLayout_8, 15, 2, 1, 1)

        self.comboStil3 = QComboBox(formWaffen)
        self.comboStil3.setObjectName(u"comboStil3")
        self.comboStil3.setMinimumSize(QSize(160, 0))
        self.comboStil3.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil3, 11, 9, 1, 1)

        self.spinW8lz = QSpinBox(formWaffen)
        self.spinW8lz.setObjectName(u"spinW8lz")
        self.spinW8lz.setMinimumSize(QSize(44, 0))
        self.spinW8lz.setAlignment(Qt.AlignCenter)
        self.spinW8lz.setReadOnly(False)
        self.spinW8lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW8lz.setMinimum(0)
        self.spinW8lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW8lz, 31, 5, 1, 1)

        self.labelKampfstil = QLabel(formWaffen)
        self.labelKampfstil.setObjectName(u"labelKampfstil")
        self.labelKampfstil.setFont(font)

        self.Waffen.addWidget(self.labelKampfstil, 0, 9, 1, 1)

        self.labelW8RightFrame = QLabel(formWaffen)
        self.labelW8RightFrame.setObjectName(u"labelW8RightFrame")
        self.labelW8RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW8RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW8RightFrame, 31, 13, 1, 1)

        self.editW4name = QLineEdit(formWaffen)
        self.editW4name.setObjectName(u"editW4name")
        self.editW4name.setMaximumSize(QSize(200, 16777215))

        self.Waffen.addWidget(self.editW4name, 15, 1, 1, 1)

        self.labelLZ = QLabel(formWaffen)
        self.labelLZ.setObjectName(u"labelLZ")
        self.labelLZ.setMinimumSize(QSize(45, 0))
        self.labelLZ.setFont(font)
        self.labelLZ.setAlignment(Qt.AlignCenter)

        self.Waffen.addWidget(self.labelLZ, 0, 5, 1, 1)

        self.addW5 = QPushButton(formWaffen)
        self.addW5.setObjectName(u"addW5")

        self.Waffen.addWidget(self.addW5, 19, 12, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_3, 9, 1, 1, 1)

        self.spinW5lz = QSpinBox(formWaffen)
        self.spinW5lz.setObjectName(u"spinW5lz")
        self.spinW5lz.setMinimumSize(QSize(44, 0))
        self.spinW5lz.setAlignment(Qt.AlignCenter)
        self.spinW5lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW5lz.setMinimum(0)
        self.spinW5lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW5lz, 19, 5, 1, 1)

        self.labelW4RightFrame = QLabel(formWaffen)
        self.labelW4RightFrame.setObjectName(u"labelW4RightFrame")
        self.labelW4RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW4RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW4RightFrame, 15, 13, 1, 1)

        self.editW8name = QLineEdit(formWaffen)
        self.editW8name.setObjectName(u"editW8name")
        self.editW8name.setMaximumSize(QSize(200, 16777215))
        self.editW8name.setReadOnly(False)

        self.Waffen.addWidget(self.editW8name, 31, 1, 1, 1)

        self.labelW1LeftFrame = QLabel(formWaffen)
        self.labelW1LeftFrame.setObjectName(u"labelW1LeftFrame")
        self.labelW1LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW1LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW1LeftFrame, 3, 0, 1, 1)

        self.editW2name = QLineEdit(formWaffen)
        self.editW2name.setObjectName(u"editW2name")
        self.editW2name.setMaximumSize(QSize(200, 16777215))

        self.Waffen.addWidget(self.editW2name, 7, 1, 1, 1)

        self.spinW1h = QSpinBox(formWaffen)
        self.spinW1h.setObjectName(u"spinW1h")
        self.spinW1h.setMinimumSize(QSize(44, 0))
        self.spinW1h.setAlignment(Qt.AlignCenter)
        self.spinW1h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW1h.setMinimum(0)
        self.spinW1h.setMaximum(99)
        self.spinW1h.setValue(6)

        self.Waffen.addWidget(self.spinW1h, 3, 6, 1, 1)

        self.spinW5wm = QSpinBox(formWaffen)
        self.spinW5wm.setObjectName(u"spinW5wm")
        self.spinW5wm.setMinimumSize(QSize(44, 0))
        self.spinW5wm.setAlignment(Qt.AlignCenter)
        self.spinW5wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW5wm.setMinimum(-99)
        self.spinW5wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW5wm, 19, 4, 1, 1)

        self.labelW6LeftFrame = QLabel(formWaffen)
        self.labelW6LeftFrame.setObjectName(u"labelW6LeftFrame")
        self.labelW6LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW6LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW6LeftFrame, 23, 0, 1, 1)

        self.labelW3LeftFrame = QLabel(formWaffen)
        self.labelW3LeftFrame.setObjectName(u"labelW3LeftFrame")
        self.labelW3LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW3LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW3LeftFrame, 11, 0, 1, 1)

        self.addW8 = QPushButton(formWaffen)
        self.addW8.setObjectName(u"addW8")

        self.Waffen.addWidget(self.addW8, 31, 12, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.buttonW5Up = QPushButton(formWaffen)
        self.buttonW5Up.setObjectName(u"buttonW5Up")

        self.verticalLayout_6.addWidget(self.buttonW5Up)

        self.buttonW5Down = QPushButton(formWaffen)
        self.buttonW5Down.setObjectName(u"buttonW5Down")

        self.verticalLayout_6.addWidget(self.buttonW5Down)


        self.Waffen.addLayout(self.verticalLayout_6, 19, 11, 1, 1)

        self.comboStil4 = QComboBox(formWaffen)
        self.comboStil4.setObjectName(u"comboStil4")
        self.comboStil4.setMinimumSize(QSize(160, 0))
        self.comboStil4.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil4, 15, 9, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.buttonW1Down = QPushButton(formWaffen)
        self.buttonW1Down.setObjectName(u"buttonW1Down")

        self.verticalLayout_2.addWidget(self.buttonW1Down)


        self.Waffen.addLayout(self.verticalLayout_2, 3, 11, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_8, 25, 1, 1, 1)

        self.labelContainerW4 = QWidget(formWaffen)
        self.labelContainerW4.setObjectName(u"labelContainerW4")
        self.horizontalLayout_14 = QHBoxLayout(self.labelContainerW4)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.labelW4Basis = QLabel(self.labelContainerW4)
        self.labelW4Basis.setObjectName(u"labelW4Basis")
        self.labelW4Basis.setMinimumSize(QSize(0, 30))
        self.labelW4Basis.setMargin(0)
        self.labelW4Basis.setIndent(14)

        self.horizontalLayout_14.addWidget(self.labelW4Basis)

        self.labelW4Werte = QLabel(self.labelContainerW4)
        self.labelW4Werte.setObjectName(u"labelW4Werte")
        self.labelW4Werte.setMinimumSize(QSize(0, 30))
        self.labelW4Werte.setIndent(14)

        self.horizontalLayout_14.addWidget(self.labelW4Werte)

        self.labelW4Mods = QLabel(self.labelContainerW4)
        self.labelW4Mods.setObjectName(u"labelW4Mods")
        self.labelW4Mods.setMinimumSize(QSize(0, 30))
        self.labelW4Mods.setIndent(14)

        self.horizontalLayout_14.addWidget(self.labelW4Mods)

        self.horizontalSpacer_5 = QSpacerItem(467, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_5)


        self.Waffen.addWidget(self.labelContainerW4, 16, 0, 1, 14)

        self.addW7 = QPushButton(formWaffen)
        self.addW7.setObjectName(u"addW7")

        self.Waffen.addWidget(self.addW7, 27, 12, 1, 1)

        self.editW6eig = QLineEdit(formWaffen)
        self.editW6eig.setObjectName(u"editW6eig")

        self.Waffen.addWidget(self.editW6eig, 23, 7, 1, 1)

        self.labelW8TopFrame = QLabel(formWaffen)
        self.labelW8TopFrame.setObjectName(u"labelW8TopFrame")
        self.labelW8TopFrame.setMaximumSize(QSize(16777215, 8))

        self.Waffen.addWidget(self.labelW8TopFrame, 30, 0, 1, 14)

        self.spinW8rw = QSpinBox(formWaffen)
        self.spinW8rw.setObjectName(u"spinW8rw")
        self.spinW8rw.setMinimumSize(QSize(44, 0))
        self.spinW8rw.setAlignment(Qt.AlignCenter)
        self.spinW8rw.setReadOnly(False)
        self.spinW8rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW8rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW8rw, 31, 3, 1, 1)

        self.labelW4LeftFrame = QLabel(formWaffen)
        self.labelW4LeftFrame.setObjectName(u"labelW4LeftFrame")
        self.labelW4LeftFrame.setMinimumSize(QSize(5, 0))
        self.labelW4LeftFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW4LeftFrame, 15, 0, 1, 1)

        self.labelContainerW3 = QWidget(formWaffen)
        self.labelContainerW3.setObjectName(u"labelContainerW3")
        self.horizontalLayout_6 = QHBoxLayout(self.labelContainerW3)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.labelW3Basis = QLabel(self.labelContainerW3)
        self.labelW3Basis.setObjectName(u"labelW3Basis")
        self.labelW3Basis.setMinimumSize(QSize(0, 30))
        self.labelW3Basis.setMargin(0)
        self.labelW3Basis.setIndent(14)

        self.horizontalLayout_6.addWidget(self.labelW3Basis)

        self.labelW3Werte = QLabel(self.labelContainerW3)
        self.labelW3Werte.setObjectName(u"labelW3Werte")
        self.labelW3Werte.setMinimumSize(QSize(0, 30))
        self.labelW3Werte.setIndent(14)

        self.horizontalLayout_6.addWidget(self.labelW3Werte)

        self.labelW3Mods = QLabel(self.labelContainerW3)
        self.labelW3Mods.setObjectName(u"labelW3Mods")
        self.labelW3Mods.setMinimumSize(QSize(0, 30))
        self.labelW3Mods.setIndent(14)

        self.horizontalLayout_6.addWidget(self.labelW3Mods)

        self.horizontalSpacer_4 = QSpacerItem(424, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.Waffen.addWidget(self.labelContainerW3, 12, 0, 1, 14)

        self.labelW6RightFrame = QLabel(formWaffen)
        self.labelW6RightFrame.setObjectName(u"labelW6RightFrame")
        self.labelW6RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW6RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW6RightFrame, 23, 13, 1, 1)

        self.labelW1RightFrame = QLabel(formWaffen)
        self.labelW1RightFrame.setObjectName(u"labelW1RightFrame")
        self.labelW1RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW1RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW1RightFrame, 3, 13, 1, 1)

        self.comboStil6 = QComboBox(formWaffen)
        self.comboStil6.setObjectName(u"comboStil6")
        self.comboStil6.setMinimumSize(QSize(160, 0))
        self.comboStil6.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil6, 23, 9, 1, 1)

        self.spinW2wm = QSpinBox(formWaffen)
        self.spinW2wm.setObjectName(u"spinW2wm")
        self.spinW2wm.setMinimumSize(QSize(44, 0))
        self.spinW2wm.setAlignment(Qt.AlignCenter)
        self.spinW2wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW2wm.setMinimum(-99)
        self.spinW2wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW2wm, 7, 4, 1, 1)

        self.labelWM = QLabel(formWaffen)
        self.labelWM.setObjectName(u"labelWM")
        self.labelWM.setMinimumSize(QSize(45, 0))
        self.labelWM.setFont(font)
        self.labelWM.setAlignment(Qt.AlignCenter)

        self.Waffen.addWidget(self.labelWM, 0, 4, 1, 1)

        self.spinW3h = QSpinBox(formWaffen)
        self.spinW3h.setObjectName(u"spinW3h")
        self.spinW3h.setMinimumSize(QSize(44, 0))
        self.spinW3h.setAlignment(Qt.AlignCenter)
        self.spinW3h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW3h.setMinimum(0)
        self.spinW3h.setMaximum(99)
        self.spinW3h.setValue(6)

        self.Waffen.addWidget(self.spinW3h, 11, 6, 1, 1)

        self.editW7eig = QLineEdit(formWaffen)
        self.editW7eig.setObjectName(u"editW7eig")

        self.Waffen.addWidget(self.editW7eig, 27, 7, 1, 1)

        self.editW2eig = QLineEdit(formWaffen)
        self.editW2eig.setObjectName(u"editW2eig")

        self.Waffen.addWidget(self.editW2eig, 7, 7, 1, 1)

        self.spinW3rw = QSpinBox(formWaffen)
        self.spinW3rw.setObjectName(u"spinW3rw")
        self.spinW3rw.setMinimumSize(QSize(44, 0))
        self.spinW3rw.setAlignment(Qt.AlignCenter)
        self.spinW3rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW3rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW3rw, 11, 3, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.buttonW2Up = QPushButton(formWaffen)
        self.buttonW2Up.setObjectName(u"buttonW2Up")

        self.verticalLayout_3.addWidget(self.buttonW2Up)

        self.buttonW2Down = QPushButton(formWaffen)
        self.buttonW2Down.setObjectName(u"buttonW2Down")

        self.verticalLayout_3.addWidget(self.buttonW2Down)


        self.Waffen.addLayout(self.verticalLayout_3, 7, 11, 1, 1)

        self.spinW8h = QSpinBox(formWaffen)
        self.spinW8h.setObjectName(u"spinW8h")
        self.spinW8h.setMinimumSize(QSize(44, 0))
        self.spinW8h.setAlignment(Qt.AlignCenter)
        self.spinW8h.setReadOnly(False)
        self.spinW8h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW8h.setMinimum(0)
        self.spinW8h.setMaximum(99)
        self.spinW8h.setValue(6)

        self.Waffen.addWidget(self.spinW8h, 31, 6, 1, 1)

        self.spinW7rw = QSpinBox(formWaffen)
        self.spinW7rw.setObjectName(u"spinW7rw")
        self.spinW7rw.setMinimumSize(QSize(44, 0))
        self.spinW7rw.setAlignment(Qt.AlignCenter)
        self.spinW7rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW7rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW7rw, 27, 3, 1, 1)

        self.spinW1rw = QSpinBox(formWaffen)
        self.spinW1rw.setObjectName(u"spinW1rw")
        self.spinW1rw.setMinimumSize(QSize(44, 0))
        self.spinW1rw.setAlignment(Qt.AlignCenter)
        self.spinW1rw.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW1rw.setMaximum(999)

        self.Waffen.addWidget(self.spinW1rw, 3, 3, 1, 1)

        self.labelW5RightFrame = QLabel(formWaffen)
        self.labelW5RightFrame.setObjectName(u"labelW5RightFrame")
        self.labelW5RightFrame.setMinimumSize(QSize(5, 0))
        self.labelW5RightFrame.setMaximumSize(QSize(4, 16777215))

        self.Waffen.addWidget(self.labelW5RightFrame, 19, 13, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.Waffen.addItem(self.verticalSpacer_6, 17, 1, 1, 1)

        self.spinW6h = QSpinBox(formWaffen)
        self.spinW6h.setObjectName(u"spinW6h")
        self.spinW6h.setMinimumSize(QSize(44, 0))
        self.spinW6h.setAlignment(Qt.AlignCenter)
        self.spinW6h.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW6h.setMinimum(0)
        self.spinW6h.setMaximum(99)
        self.spinW6h.setValue(6)

        self.Waffen.addWidget(self.spinW6h, 23, 6, 1, 1)

        self.comboStil7 = QComboBox(formWaffen)
        self.comboStil7.setObjectName(u"comboStil7")
        self.comboStil7.setMinimumSize(QSize(160, 0))
        self.comboStil7.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil7, 27, 9, 1, 1)

        self.spinW2lz = QSpinBox(formWaffen)
        self.spinW2lz.setObjectName(u"spinW2lz")
        self.spinW2lz.setMinimumSize(QSize(44, 0))
        self.spinW2lz.setAlignment(Qt.AlignCenter)
        self.spinW2lz.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW2lz.setMinimum(0)
        self.spinW2lz.setMaximum(99)

        self.Waffen.addWidget(self.spinW2lz, 7, 5, 1, 1)

        self.spinW3wm = QSpinBox(formWaffen)
        self.spinW3wm.setObjectName(u"spinW3wm")
        self.spinW3wm.setMinimumSize(QSize(44, 0))
        self.spinW3wm.setAlignment(Qt.AlignCenter)
        self.spinW3wm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW3wm.setMinimum(-99)
        self.spinW3wm.setMaximum(99)

        self.Waffen.addWidget(self.spinW3wm, 11, 4, 1, 1)

        self.labelRW = QLabel(formWaffen)
        self.labelRW.setObjectName(u"labelRW")
        self.labelRW.setFont(font)
        self.labelRW.setAlignment(Qt.AlignCenter)

        self.Waffen.addWidget(self.labelRW, 0, 3, 1, 1)

        self.comboStil8 = QComboBox(formWaffen)
        self.comboStil8.setObjectName(u"comboStil8")
        self.comboStil8.setMinimumSize(QSize(160, 0))
        self.comboStil8.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Waffen.addWidget(self.comboStil8, 31, 9, 1, 1)

        self.label = QLabel(formWaffen)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.Waffen.addWidget(self.label, 0, 8, 1, 1)

        self.comboBEW1 = QComboBox(formWaffen)
        self.comboBEW1.addItem("")
        self.comboBEW1.addItem("")
        self.comboBEW1.addItem("")
        self.comboBEW1.addItem("")
        self.comboBEW1.setObjectName(u"comboBEW1")

        self.Waffen.addWidget(self.comboBEW1, 3, 8, 1, 1)

        self.comboBEW2 = QComboBox(formWaffen)
        self.comboBEW2.addItem("")
        self.comboBEW2.addItem("")
        self.comboBEW2.addItem("")
        self.comboBEW2.addItem("")
        self.comboBEW2.setObjectName(u"comboBEW2")

        self.Waffen.addWidget(self.comboBEW2, 7, 8, 1, 1)

        self.comboBEW3 = QComboBox(formWaffen)
        self.comboBEW3.addItem("")
        self.comboBEW3.addItem("")
        self.comboBEW3.addItem("")
        self.comboBEW3.addItem("")
        self.comboBEW3.setObjectName(u"comboBEW3")

        self.Waffen.addWidget(self.comboBEW3, 11, 8, 1, 1)

        self.comboBEW4 = QComboBox(formWaffen)
        self.comboBEW4.addItem("")
        self.comboBEW4.addItem("")
        self.comboBEW4.addItem("")
        self.comboBEW4.addItem("")
        self.comboBEW4.setObjectName(u"comboBEW4")

        self.Waffen.addWidget(self.comboBEW4, 15, 8, 1, 1)

        self.comboBEW5 = QComboBox(formWaffen)
        self.comboBEW5.addItem("")
        self.comboBEW5.addItem("")
        self.comboBEW5.addItem("")
        self.comboBEW5.addItem("")
        self.comboBEW5.setObjectName(u"comboBEW5")

        self.Waffen.addWidget(self.comboBEW5, 19, 8, 1, 1)

        self.comboBEW6 = QComboBox(formWaffen)
        self.comboBEW6.addItem("")
        self.comboBEW6.addItem("")
        self.comboBEW6.addItem("")
        self.comboBEW6.addItem("")
        self.comboBEW6.setObjectName(u"comboBEW6")

        self.Waffen.addWidget(self.comboBEW6, 23, 8, 1, 1)

        self.comboBEW7 = QComboBox(formWaffen)
        self.comboBEW7.addItem("")
        self.comboBEW7.addItem("")
        self.comboBEW7.addItem("")
        self.comboBEW7.addItem("")
        self.comboBEW7.setObjectName(u"comboBEW7")

        self.Waffen.addWidget(self.comboBEW7, 27, 8, 1, 1)

        self.comboBEW8 = QComboBox(formWaffen)
        self.comboBEW8.addItem("")
        self.comboBEW8.addItem("")
        self.comboBEW8.addItem("")
        self.comboBEW8.addItem("")
        self.comboBEW8.setObjectName(u"comboBEW8")

        self.Waffen.addWidget(self.comboBEW8, 31, 8, 1, 1)


        self.verticalLayout.addLayout(self.Waffen)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.editW1name, self.spinW1w6)
        QWidget.setTabOrder(self.spinW1w6, self.spinW1plus)
        QWidget.setTabOrder(self.spinW1plus, self.spinW1rw)
        QWidget.setTabOrder(self.spinW1rw, self.spinW1wm)
        QWidget.setTabOrder(self.spinW1wm, self.spinW1lz)
        QWidget.setTabOrder(self.spinW1lz, self.spinW1h)
        QWidget.setTabOrder(self.spinW1h, self.editW1eig)
        QWidget.setTabOrder(self.editW1eig, self.comboBEW1)
        QWidget.setTabOrder(self.comboBEW1, self.comboStil1)
        QWidget.setTabOrder(self.comboStil1, self.buttonW1Down)
        QWidget.setTabOrder(self.buttonW1Down, self.addW1)
        QWidget.setTabOrder(self.addW1, self.editW2name)
        QWidget.setTabOrder(self.editW2name, self.spinW2w6)
        QWidget.setTabOrder(self.spinW2w6, self.spinW2plus)
        QWidget.setTabOrder(self.spinW2plus, self.spinW2rw)
        QWidget.setTabOrder(self.spinW2rw, self.spinW2wm)
        QWidget.setTabOrder(self.spinW2wm, self.spinW2lz)
        QWidget.setTabOrder(self.spinW2lz, self.spinW2h)
        QWidget.setTabOrder(self.spinW2h, self.editW2eig)
        QWidget.setTabOrder(self.editW2eig, self.comboBEW2)
        QWidget.setTabOrder(self.comboBEW2, self.comboStil2)
        QWidget.setTabOrder(self.comboStil2, self.buttonW2Up)
        QWidget.setTabOrder(self.buttonW2Up, self.buttonW2Down)
        QWidget.setTabOrder(self.buttonW2Down, self.addW2)
        QWidget.setTabOrder(self.addW2, self.editW3name)
        QWidget.setTabOrder(self.editW3name, self.spinW3w6)
        QWidget.setTabOrder(self.spinW3w6, self.spinW3plus)
        QWidget.setTabOrder(self.spinW3plus, self.spinW3rw)
        QWidget.setTabOrder(self.spinW3rw, self.spinW3wm)
        QWidget.setTabOrder(self.spinW3wm, self.spinW3lz)
        QWidget.setTabOrder(self.spinW3lz, self.spinW3h)
        QWidget.setTabOrder(self.spinW3h, self.editW3eig)
        QWidget.setTabOrder(self.editW3eig, self.comboBEW3)
        QWidget.setTabOrder(self.comboBEW3, self.comboStil3)
        QWidget.setTabOrder(self.comboStil3, self.buttonW3Up)
        QWidget.setTabOrder(self.buttonW3Up, self.buttonW3Down)
        QWidget.setTabOrder(self.buttonW3Down, self.addW3)
        QWidget.setTabOrder(self.addW3, self.editW4name)
        QWidget.setTabOrder(self.editW4name, self.spinW4w6)
        QWidget.setTabOrder(self.spinW4w6, self.spinW4plus)
        QWidget.setTabOrder(self.spinW4plus, self.spinW4rw)
        QWidget.setTabOrder(self.spinW4rw, self.spinW4wm)
        QWidget.setTabOrder(self.spinW4wm, self.spinW4lz)
        QWidget.setTabOrder(self.spinW4lz, self.spinW4h)
        QWidget.setTabOrder(self.spinW4h, self.editW4eig)
        QWidget.setTabOrder(self.editW4eig, self.comboBEW4)
        QWidget.setTabOrder(self.comboBEW4, self.comboStil4)
        QWidget.setTabOrder(self.comboStil4, self.buttonW4Up)
        QWidget.setTabOrder(self.buttonW4Up, self.buttonW4Down)
        QWidget.setTabOrder(self.buttonW4Down, self.addW4)
        QWidget.setTabOrder(self.addW4, self.editW5name)
        QWidget.setTabOrder(self.editW5name, self.spinW5w6)
        QWidget.setTabOrder(self.spinW5w6, self.spinW5plus)
        QWidget.setTabOrder(self.spinW5plus, self.spinW5rw)
        QWidget.setTabOrder(self.spinW5rw, self.spinW5wm)
        QWidget.setTabOrder(self.spinW5wm, self.spinW5lz)
        QWidget.setTabOrder(self.spinW5lz, self.spinW5h)
        QWidget.setTabOrder(self.spinW5h, self.editW5eig)
        QWidget.setTabOrder(self.editW5eig, self.comboBEW5)
        QWidget.setTabOrder(self.comboBEW5, self.comboStil5)
        QWidget.setTabOrder(self.comboStil5, self.buttonW5Up)
        QWidget.setTabOrder(self.buttonW5Up, self.buttonW5Down)
        QWidget.setTabOrder(self.buttonW5Down, self.addW5)
        QWidget.setTabOrder(self.addW5, self.editW6name)
        QWidget.setTabOrder(self.editW6name, self.spinW6w6)
        QWidget.setTabOrder(self.spinW6w6, self.spinW6plus)
        QWidget.setTabOrder(self.spinW6plus, self.spinW6rw)
        QWidget.setTabOrder(self.spinW6rw, self.spinW6wm)
        QWidget.setTabOrder(self.spinW6wm, self.spinW6lz)
        QWidget.setTabOrder(self.spinW6lz, self.spinW6h)
        QWidget.setTabOrder(self.spinW6h, self.editW6eig)
        QWidget.setTabOrder(self.editW6eig, self.comboBEW6)
        QWidget.setTabOrder(self.comboBEW6, self.comboStil6)
        QWidget.setTabOrder(self.comboStil6, self.buttonW6Up)
        QWidget.setTabOrder(self.buttonW6Up, self.buttonW6Down)
        QWidget.setTabOrder(self.buttonW6Down, self.addW6)
        QWidget.setTabOrder(self.addW6, self.editW7name)
        QWidget.setTabOrder(self.editW7name, self.spinW7w6)
        QWidget.setTabOrder(self.spinW7w6, self.spinW7plus)
        QWidget.setTabOrder(self.spinW7plus, self.spinW7rw)
        QWidget.setTabOrder(self.spinW7rw, self.spinW7wm)
        QWidget.setTabOrder(self.spinW7wm, self.spinW7lz)
        QWidget.setTabOrder(self.spinW7lz, self.spinW7h)
        QWidget.setTabOrder(self.spinW7h, self.editW7eig)
        QWidget.setTabOrder(self.editW7eig, self.comboBEW7)
        QWidget.setTabOrder(self.comboBEW7, self.comboStil7)
        QWidget.setTabOrder(self.comboStil7, self.buttonW7Up)
        QWidget.setTabOrder(self.buttonW7Up, self.buttonW7Down)
        QWidget.setTabOrder(self.buttonW7Down, self.addW7)
        QWidget.setTabOrder(self.addW7, self.editW8name)
        QWidget.setTabOrder(self.editW8name, self.spinW8w6)
        QWidget.setTabOrder(self.spinW8w6, self.spinW8plus)
        QWidget.setTabOrder(self.spinW8plus, self.spinW8rw)
        QWidget.setTabOrder(self.spinW8rw, self.spinW8wm)
        QWidget.setTabOrder(self.spinW8wm, self.spinW8lz)
        QWidget.setTabOrder(self.spinW8lz, self.spinW8h)
        QWidget.setTabOrder(self.spinW8h, self.editW8eig)
        QWidget.setTabOrder(self.editW8eig, self.comboBEW8)
        QWidget.setTabOrder(self.comboBEW8, self.comboStil8)
        QWidget.setTabOrder(self.comboStil8, self.buttonW8Up)
        QWidget.setTabOrder(self.buttonW8Up, self.addW8)

        self.retranslateUi(formWaffen)

        self.comboStil1.setCurrentIndex(-1)
        self.comboBEW1.setCurrentIndex(1)
        self.comboBEW2.setCurrentIndex(1)
        self.comboBEW3.setCurrentIndex(1)
        self.comboBEW4.setCurrentIndex(1)
        self.comboBEW5.setCurrentIndex(1)
        self.comboBEW6.setCurrentIndex(1)
        self.comboBEW7.setCurrentIndex(1)
        self.comboBEW8.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(formWaffen)
    # setupUi

    def retranslateUi(self, formWaffen):
        formWaffen.setWindowTitle(QCoreApplication.translate("formWaffen", u"Form", None))
        self.labelW8LeftFrame.setText("")
#if QT_CONFIG(tooltip)
        self.buttonW4Up.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach oben schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW4Up.setText(QCoreApplication.translate("formWaffen", u"Up", None))
        self.buttonW4Up.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
#if QT_CONFIG(tooltip)
        self.buttonW4Down.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach unten schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW4Down.setText(QCoreApplication.translate("formWaffen", u"Down", None))
        self.buttonW4Down.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
        self.labelW7seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
        self.labelW7RightFrame.setText("")
        self.labelW3TopFrame.setText("")
        self.labelW8Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW8Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW8Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.labelW1seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
        self.labelW2Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW2Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW2Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.labelHaerte.setText(QCoreApplication.translate("formWaffen", u"H\u00e4rte", None))
        self.labelHaerte.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
        self.labelW8seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
        self.labelW7Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW7Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW7Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.labelW3seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
        self.labelW5Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW5Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW5Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.labelW6Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW6Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW6Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.labelWName.setText(QCoreApplication.translate("formWaffen", u"Name", None))
        self.labelWName.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
        self.labelW2RightFrame.setText("")
        self.labelW2seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
#if QT_CONFIG(tooltip)
        self.buttonW7Up.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach oben schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW7Up.setText(QCoreApplication.translate("formWaffen", u"Up", None))
        self.buttonW7Up.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
#if QT_CONFIG(tooltip)
        self.buttonW7Down.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach unten schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW7Down.setText(QCoreApplication.translate("formWaffen", u"Down", None))
        self.buttonW7Down.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
        self.addW6.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW6.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
        self.addW3.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW3.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
        self.addW1.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW1.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
#if QT_CONFIG(tooltip)
        self.buttonW3Up.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach oben schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW3Up.setText(QCoreApplication.translate("formWaffen", u"Up", None))
        self.buttonW3Up.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
#if QT_CONFIG(tooltip)
        self.buttonW3Down.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach unten schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW3Down.setText(QCoreApplication.translate("formWaffen", u"Down", None))
        self.buttonW3Down.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
        self.labelW1Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW1Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW1Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.labelW7LeftFrame.setText("")
        self.labelW5LeftFrame.setText("")
#if QT_CONFIG(tooltip)
        self.buttonW8Up.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach oben schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW8Up.setText(QCoreApplication.translate("formWaffen", u"Up", None))
        self.buttonW8Up.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
        self.labelW6seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
        self.addW2.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW2.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
        self.labelW5seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
        self.labelW6TopFrame.setText("")
        self.labelW2TopFrame.setText("")
        self.editW8eig.setText("")
        self.labelW7TopFrame.setText("")
        self.labelW1TopFrame.setText("")
#if QT_CONFIG(tooltip)
        self.labelTP.setToolTip(QCoreApplication.translate("formWaffen", u"Trefferpunkte", None))
#endif // QT_CONFIG(tooltip)
        self.labelTP.setText(QCoreApplication.translate("formWaffen", u"TP", None))
        self.labelTP.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
        self.labelW2LeftFrame.setText("")
        self.labelW5TopFrame.setText("")
        self.labelW4TopFrame.setText("")
        self.labelW3RightFrame.setText("")
        self.labelEigenschaften.setText(QCoreApplication.translate("formWaffen", u"Eigenschaften", None))
        self.labelEigenschaften.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
#if QT_CONFIG(tooltip)
        self.buttonW6Up.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach oben schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW6Up.setText(QCoreApplication.translate("formWaffen", u"Up", None))
        self.buttonW6Up.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
#if QT_CONFIG(tooltip)
        self.buttonW6Down.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach unten schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW6Down.setText(QCoreApplication.translate("formWaffen", u"Down", None))
        self.buttonW6Down.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
        self.addW4.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW4.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
        self.labelW4seiten.setText(QCoreApplication.translate("formWaffen", u"W6 +", None))
        self.labelKampfstil.setText(QCoreApplication.translate("formWaffen", u"Kampfstil", None))
        self.labelKampfstil.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
        self.labelW8RightFrame.setText("")
#if QT_CONFIG(tooltip)
        self.labelLZ.setToolTip(QCoreApplication.translate("formWaffen", u"Ladezeit", None))
#endif // QT_CONFIG(tooltip)
        self.labelLZ.setText(QCoreApplication.translate("formWaffen", u"LZ", None))
        self.labelLZ.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
        self.addW5.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW5.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
        self.labelW4RightFrame.setText("")
        self.editW8name.setText("")
        self.labelW1LeftFrame.setText("")
        self.labelW6LeftFrame.setText("")
        self.labelW3LeftFrame.setText("")
        self.addW8.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW8.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
#if QT_CONFIG(tooltip)
        self.buttonW5Up.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach oben schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW5Up.setText(QCoreApplication.translate("formWaffen", u"Up", None))
        self.buttonW5Up.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
#if QT_CONFIG(tooltip)
        self.buttonW5Down.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach unten schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW5Down.setText(QCoreApplication.translate("formWaffen", u"Down", None))
        self.buttonW5Down.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
#if QT_CONFIG(tooltip)
        self.buttonW1Down.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach unten schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW1Down.setText(QCoreApplication.translate("formWaffen", u"Down", None))
        self.buttonW1Down.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
        self.labelW4Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW4Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW4Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.addW7.setText(QCoreApplication.translate("formWaffen", u"+", None))
        self.addW7.setProperty("class", QCoreApplication.translate("formWaffen", u"iconSmall", None))
        self.labelW8TopFrame.setText("")
        self.labelW4LeftFrame.setText("")
        self.labelW3Basis.setText(QCoreApplication.translate("formWaffen", u"Basiswaffe Hand", None))
        self.labelW3Werte.setText(QCoreApplication.translate("formWaffen", u"Werte AT* 10 VT* 10 TP 2W6+2", None))
        self.labelW3Mods.setText(QCoreApplication.translate("formWaffen", u"Verbesserungen AT +1", None))
        self.labelW6RightFrame.setText("")
        self.labelW1RightFrame.setText("")
#if QT_CONFIG(tooltip)
        self.labelWM.setToolTip(QCoreApplication.translate("formWaffen", u"Waffenmodifikator", None))
#endif // QT_CONFIG(tooltip)
        self.labelWM.setText(QCoreApplication.translate("formWaffen", u"WM", None))
        self.labelWM.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
#if QT_CONFIG(tooltip)
        self.buttonW2Up.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach oben schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW2Up.setText(QCoreApplication.translate("formWaffen", u"Up", None))
        self.buttonW2Up.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
#if QT_CONFIG(tooltip)
        self.buttonW2Down.setToolTip(QCoreApplication.translate("formWaffen", u"Waffe eine Zeile nach unten schieben", None))
#endif // QT_CONFIG(tooltip)
        self.buttonW2Down.setText(QCoreApplication.translate("formWaffen", u"Down", None))
        self.buttonW2Down.setProperty("class", QCoreApplication.translate("formWaffen", u"iconTopDownArrow", None))
        self.labelW5RightFrame.setText("")
#if QT_CONFIG(tooltip)
        self.labelRW.setToolTip(QCoreApplication.translate("formWaffen", u"Reichweite", None))
#endif // QT_CONFIG(tooltip)
        self.labelRW.setText(QCoreApplication.translate("formWaffen", u"RW", None))
        self.labelRW.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
        self.label.setText(QCoreApplication.translate("formWaffen", u"BE", None))
        self.label.setProperty("class", QCoreApplication.translate("formWaffen", u"h4", None))
        self.comboBEW1.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW1.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW1.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW1.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

        self.comboBEW2.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW2.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW2.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW2.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

        self.comboBEW3.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW3.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW3.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW3.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

        self.comboBEW4.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW4.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW4.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW4.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

        self.comboBEW5.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW5.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW5.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW5.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

        self.comboBEW6.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW6.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW6.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW6.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

        self.comboBEW7.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW7.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW7.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW7.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

        self.comboBEW8.setItemText(0, QCoreApplication.translate("formWaffen", u"Keine", None))
        self.comboBEW8.setItemText(1, QCoreApplication.translate("formWaffen", u"R\u00fcstung 1", None))
        self.comboBEW8.setItemText(2, QCoreApplication.translate("formWaffen", u"R\u00fcstung 2", None))
        self.comboBEW8.setItemText(3, QCoreApplication.translate("formWaffen", u"R\u00fcstung 3", None))

    # retranslateUi

