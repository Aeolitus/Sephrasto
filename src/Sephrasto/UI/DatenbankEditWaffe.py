# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditWaffe.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(454, 450)
        self.verticalLayout = QVBoxLayout(dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 434, 430))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelTP = QLabel(self.scrollAreaWidgetContents_2)
        self.labelTP.setObjectName(u"labelTP")

        self.gridLayout.addWidget(self.labelTP, 2, 0, 1, 1)

        self.comboFertigkeit = QComboBox(self.scrollAreaWidgetContents_2)
        self.comboFertigkeit.setObjectName(u"comboFertigkeit")

        self.gridLayout.addWidget(self.comboFertigkeit, 7, 1, 1, 1)

        self.layoutLZ = QHBoxLayout()
        self.layoutLZ.setObjectName(u"layoutLZ")
        self.spacerLZ = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutLZ.addItem(self.spacerLZ)

        self.spinLZ = QSpinBox(self.scrollAreaWidgetContents_2)
        self.spinLZ.setObjectName(u"spinLZ")
        self.spinLZ.setMinimumSize(QSize(50, 0))
        self.spinLZ.setAlignment(Qt.AlignCenter)
        self.spinLZ.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.layoutLZ.addWidget(self.spinLZ)


        self.gridLayout.addLayout(self.layoutLZ, 5, 1, 1, 1)

        self.labelFertigkeit = QLabel(self.scrollAreaWidgetContents_2)
        self.labelFertigkeit.setObjectName(u"labelFertigkeit")

        self.gridLayout.addWidget(self.labelFertigkeit, 7, 0, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents_2)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.teEigenschaften = QPlainTextEdit(self.scrollAreaWidgetContents_2)
        self.teEigenschaften.setObjectName(u"teEigenschaften")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teEigenschaften.sizePolicy().hasHeightForWidth())
        self.teEigenschaften.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.teEigenschaften, 10, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboTyp = QComboBox(self.scrollAreaWidgetContents_2)
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.setObjectName(u"comboTyp")

        self.horizontalLayout_2.addWidget(self.comboTyp)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.spinRW = QSpinBox(self.scrollAreaWidgetContents_2)
        self.spinRW.setObjectName(u"spinRW")
        self.spinRW.setMinimumSize(QSize(50, 0))
        self.spinRW.setAlignment(Qt.AlignCenter)
        self.spinRW.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinRW.setMaximum(999)
        self.spinRW.setValue(1)

        self.horizontalLayout_4.addWidget(self.spinRW)


        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 1, 1, 1)

        self.labelWM = QLabel(self.scrollAreaWidgetContents_2)
        self.labelWM.setObjectName(u"labelWM")

        self.gridLayout.addWidget(self.labelWM, 4, 0, 1, 1)

        self.labelLZ = QLabel(self.scrollAreaWidgetContents_2)
        self.labelLZ.setObjectName(u"labelLZ")

        self.gridLayout.addWidget(self.labelLZ, 5, 0, 1, 1)

        self.layoutKampfstile = QGridLayout()
        self.layoutKampfstile.setObjectName(u"layoutKampfstile")

        self.gridLayout.addLayout(self.layoutKampfstile, 9, 1, 1, 1)

        self.labelEigenschaften = QLabel(self.scrollAreaWidgetContents_2)
        self.labelEigenschaften.setObjectName(u"labelEigenschaften")

        self.gridLayout.addWidget(self.labelEigenschaften, 10, 0, 1, 1)

        self.labelKampfstil = QLabel(self.scrollAreaWidgetContents_2)
        self.labelKampfstil.setObjectName(u"labelKampfstil")

        self.gridLayout.addWidget(self.labelKampfstil, 9, 0, 1, 1)

        self.labelRW = QLabel(self.scrollAreaWidgetContents_2)
        self.labelRW.setObjectName(u"labelRW")
        self.labelRW.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.labelRW, 3, 0, 1, 1)

        self.labelTalent = QLabel(self.scrollAreaWidgetContents_2)
        self.labelTalent.setObjectName(u"labelTalent")

        self.gridLayout.addWidget(self.labelTalent, 8, 0, 1, 1)

        self.labelHaerte = QLabel(self.scrollAreaWidgetContents_2)
        self.labelHaerte.setObjectName(u"labelHaerte")

        self.gridLayout.addWidget(self.labelHaerte, 6, 0, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents_2)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 0, 1, 1, 1)

        self.labelTyp = QLabel(self.scrollAreaWidgetContents_2)
        self.labelTyp.setObjectName(u"labelTyp")

        self.gridLayout.addWidget(self.labelTyp, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.spinWM = QSpinBox(self.scrollAreaWidgetContents_2)
        self.spinWM.setObjectName(u"spinWM")
        self.spinWM.setMinimumSize(QSize(50, 0))
        self.spinWM.setAlignment(Qt.AlignCenter)
        self.spinWM.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinWM.setMinimum(-99)
        self.spinWM.setMaximum(99)

        self.horizontalLayout_3.addWidget(self.spinWM)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 1, 1, 1)

        self.comboTalent = QComboBox(self.scrollAreaWidgetContents_2)
        self.comboTalent.setObjectName(u"comboTalent")

        self.gridLayout.addWidget(self.comboTalent, 8, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinWuerfel = QSpinBox(self.scrollAreaWidgetContents_2)
        self.spinWuerfel.setObjectName(u"spinWuerfel")
        self.spinWuerfel.setMinimumSize(QSize(50, 0))
        self.spinWuerfel.setAlignment(Qt.AlignCenter)
        self.spinWuerfel.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinWuerfel.setMinimum(0)
        self.spinWuerfel.setMaximum(99)
        self.spinWuerfel.setValue(2)

        self.horizontalLayout.addWidget(self.spinWuerfel)

        self.comboWuerfelSeiten = QComboBox(self.scrollAreaWidgetContents_2)
        self.comboWuerfelSeiten.addItem("")
        self.comboWuerfelSeiten.addItem("")
        self.comboWuerfelSeiten.setObjectName(u"comboWuerfelSeiten")

        self.horizontalLayout.addWidget(self.comboWuerfelSeiten)

        self.label_7 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.spinPlus = QSpinBox(self.scrollAreaWidgetContents_2)
        self.spinPlus.setObjectName(u"spinPlus")
        self.spinPlus.setMinimumSize(QSize(50, 0))
        self.spinPlus.setAlignment(Qt.AlignCenter)
        self.spinPlus.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinPlus.setMinimum(-99)
        self.spinPlus.setValue(2)

        self.horizontalLayout.addWidget(self.spinPlus)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.spinHaerte = QSpinBox(self.scrollAreaWidgetContents_2)
        self.spinHaerte.setObjectName(u"spinHaerte")
        self.spinHaerte.setMinimumSize(QSize(50, 0))
        self.spinHaerte.setAlignment(Qt.AlignCenter)
        self.spinHaerte.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinHaerte.setMinimum(0)
        self.spinHaerte.setMaximum(99)
        self.spinHaerte.setValue(7)

        self.horizontalLayout_6.addWidget(self.spinHaerte)


        self.gridLayout.addLayout(self.horizontalLayout_6, 6, 1, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.spinWuerfel)
        QWidget.setTabOrder(self.spinWuerfel, self.comboWuerfelSeiten)
        QWidget.setTabOrder(self.comboWuerfelSeiten, self.spinPlus)
        QWidget.setTabOrder(self.spinPlus, self.spinRW)
        QWidget.setTabOrder(self.spinRW, self.spinWM)
        QWidget.setTabOrder(self.spinWM, self.spinLZ)
        QWidget.setTabOrder(self.spinLZ, self.spinHaerte)
        QWidget.setTabOrder(self.spinHaerte, self.comboFertigkeit)
        QWidget.setTabOrder(self.comboFertigkeit, self.comboTalent)
        QWidget.setTabOrder(self.comboTalent, self.teEigenschaften)

        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Waffe bearbeiten...", None))
        self.labelTP.setText(QCoreApplication.translate("dialog", u"Trefferpunkte", None))
        self.labelFertigkeit.setText(QCoreApplication.translate("dialog", u"Fertigkeit", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.comboTyp.setItemText(0, QCoreApplication.translate("dialog", u"Nahkampfwaffe", None))
        self.comboTyp.setItemText(1, QCoreApplication.translate("dialog", u"Fernkampfwaffe", None))

        self.labelWM.setText(QCoreApplication.translate("dialog", u"WM", None))
        self.labelLZ.setText(QCoreApplication.translate("dialog", u"LZ", None))
        self.labelEigenschaften.setText(QCoreApplication.translate("dialog", u"Eigenschaften", None))
        self.labelKampfstil.setText(QCoreApplication.translate("dialog", u"Kampfstil", None))
        self.labelRW.setText(QCoreApplication.translate("dialog", u"Reichweite", None))
        self.labelTalent.setText(QCoreApplication.translate("dialog", u"Talent", None))
        self.labelHaerte.setText(QCoreApplication.translate("dialog", u"H\u00e4rte", None))
        self.labelTyp.setText(QCoreApplication.translate("dialog", u"Typ", None))
        self.spinWuerfel.setSuffix("")
        self.comboWuerfelSeiten.setItemText(0, QCoreApplication.translate("dialog", u"W6", None))
        self.comboWuerfelSeiten.setItemText(1, QCoreApplication.translate("dialog", u"W20", None))

        self.label_7.setText(QCoreApplication.translate("dialog", u"+", None))
    # retranslateUi

