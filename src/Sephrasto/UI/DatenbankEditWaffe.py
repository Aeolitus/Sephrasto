# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditWaffe.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QFormLayout,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPlainTextEdit, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(423, 430)
        self.verticalLayout = QVBoxLayout(dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 399, 406))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelName)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leName)

        self.labelTyp = QLabel(self.scrollAreaWidgetContents)
        self.labelTyp.setObjectName(u"labelTyp")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelTyp)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboTyp = QComboBox(self.scrollAreaWidgetContents)
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.setObjectName(u"comboTyp")

        self.horizontalLayout_2.addWidget(self.comboTyp)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.labelTP = QLabel(self.scrollAreaWidgetContents)
        self.labelTP.setObjectName(u"labelTP")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelTP)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinWuerfel = QSpinBox(self.scrollAreaWidgetContents)
        self.spinWuerfel.setObjectName(u"spinWuerfel")
        self.spinWuerfel.setMinimumSize(QSize(50, 0))
        self.spinWuerfel.setAlignment(Qt.AlignCenter)
        self.spinWuerfel.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinWuerfel.setMinimum(0)
        self.spinWuerfel.setMaximum(99)
        self.spinWuerfel.setValue(2)

        self.horizontalLayout.addWidget(self.spinWuerfel)

        self.comboWuerfelSeiten = QComboBox(self.scrollAreaWidgetContents)
        self.comboWuerfelSeiten.addItem("")
        self.comboWuerfelSeiten.addItem("")
        self.comboWuerfelSeiten.setObjectName(u"comboWuerfelSeiten")

        self.horizontalLayout.addWidget(self.comboWuerfelSeiten)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.spinPlus = QSpinBox(self.scrollAreaWidgetContents)
        self.spinPlus.setObjectName(u"spinPlus")
        self.spinPlus.setMinimumSize(QSize(50, 0))
        self.spinPlus.setAlignment(Qt.AlignCenter)
        self.spinPlus.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinPlus.setMinimum(-99)
        self.spinPlus.setValue(2)

        self.horizontalLayout.addWidget(self.spinPlus)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.labelRW = QLabel(self.scrollAreaWidgetContents)
        self.labelRW.setObjectName(u"labelRW")
        self.labelRW.setMinimumSize(QSize(110, 0))

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelRW)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.spinRW = QSpinBox(self.scrollAreaWidgetContents)
        self.spinRW.setObjectName(u"spinRW")
        self.spinRW.setMinimumSize(QSize(50, 0))
        self.spinRW.setAlignment(Qt.AlignCenter)
        self.spinRW.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinRW.setMaximum(999)
        self.spinRW.setValue(1)

        self.horizontalLayout_4.addWidget(self.spinRW)


        self.formLayout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)

        self.labelWM = QLabel(self.scrollAreaWidgetContents)
        self.labelWM.setObjectName(u"labelWM")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelWM)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.spinWM = QSpinBox(self.scrollAreaWidgetContents)
        self.spinWM.setObjectName(u"spinWM")
        self.spinWM.setMinimumSize(QSize(50, 0))
        self.spinWM.setAlignment(Qt.AlignCenter)
        self.spinWM.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinWM.setMinimum(-99)
        self.spinWM.setMaximum(99)

        self.horizontalLayout_3.addWidget(self.spinWM)


        self.formLayout.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)

        self.labelLZ = QLabel(self.scrollAreaWidgetContents)
        self.labelLZ.setObjectName(u"labelLZ")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelLZ)

        self.layoutLZ = QHBoxLayout()
        self.layoutLZ.setObjectName(u"layoutLZ")
        self.spacerLZ = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutLZ.addItem(self.spacerLZ)

        self.spinLZ = QSpinBox(self.scrollAreaWidgetContents)
        self.spinLZ.setObjectName(u"spinLZ")
        self.spinLZ.setMinimumSize(QSize(50, 0))
        self.spinLZ.setAlignment(Qt.AlignCenter)
        self.spinLZ.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.layoutLZ.addWidget(self.spinLZ)


        self.formLayout.setLayout(5, QFormLayout.ItemRole.FieldRole, self.layoutLZ)

        self.labelHaerte = QLabel(self.scrollAreaWidgetContents)
        self.labelHaerte.setObjectName(u"labelHaerte")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.labelHaerte)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.spinHaerte = QSpinBox(self.scrollAreaWidgetContents)
        self.spinHaerte.setObjectName(u"spinHaerte")
        self.spinHaerte.setMinimumSize(QSize(50, 0))
        self.spinHaerte.setAlignment(Qt.AlignCenter)
        self.spinHaerte.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinHaerte.setMinimum(0)
        self.spinHaerte.setMaximum(99)
        self.spinHaerte.setValue(7)

        self.horizontalLayout_6.addWidget(self.spinHaerte)


        self.formLayout.setLayout(6, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)

        self.labelFertigkeit = QLabel(self.scrollAreaWidgetContents)
        self.labelFertigkeit.setObjectName(u"labelFertigkeit")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.labelFertigkeit)

        self.comboFertigkeit = QComboBox(self.scrollAreaWidgetContents)
        self.comboFertigkeit.setObjectName(u"comboFertigkeit")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.comboFertigkeit)

        self.labelTalent = QLabel(self.scrollAreaWidgetContents)
        self.labelTalent.setObjectName(u"labelTalent")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.labelTalent)

        self.comboTalent = QComboBox(self.scrollAreaWidgetContents)
        self.comboTalent.setObjectName(u"comboTalent")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.comboTalent)

        self.labelKampfstil = QLabel(self.scrollAreaWidgetContents)
        self.labelKampfstil.setObjectName(u"labelKampfstil")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.labelKampfstil)

        self.layoutKampfstile = QGridLayout()
        self.layoutKampfstile.setObjectName(u"layoutKampfstile")

        self.formLayout.setLayout(9, QFormLayout.ItemRole.FieldRole, self.layoutKampfstile)

        self.labelEigenschaften = QLabel(self.scrollAreaWidgetContents)
        self.labelEigenschaften.setObjectName(u"labelEigenschaften")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.labelEigenschaften)

        self.teEigenschaften = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teEigenschaften.setObjectName(u"teEigenschaften")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teEigenschaften.sizePolicy().hasHeightForWidth())
        self.teEigenschaften.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.teEigenschaften)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

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
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelTyp.setText(QCoreApplication.translate("dialog", u"Typ", None))
        self.comboTyp.setItemText(0, QCoreApplication.translate("dialog", u"Nahkampfwaffe", None))
        self.comboTyp.setItemText(1, QCoreApplication.translate("dialog", u"Fernkampfwaffe", None))

        self.labelTP.setText(QCoreApplication.translate("dialog", u"Trefferpunkte", None))
        self.spinWuerfel.setSuffix("")
        self.comboWuerfelSeiten.setItemText(0, QCoreApplication.translate("dialog", u"W6", None))
        self.comboWuerfelSeiten.setItemText(1, QCoreApplication.translate("dialog", u"W20", None))

        self.label_7.setText(QCoreApplication.translate("dialog", u"+", None))
        self.labelRW.setText(QCoreApplication.translate("dialog", u"Reichweite", None))
        self.labelWM.setText(QCoreApplication.translate("dialog", u"WM", None))
        self.labelLZ.setText(QCoreApplication.translate("dialog", u"LZ", None))
        self.labelHaerte.setText(QCoreApplication.translate("dialog", u"H\u00e4rte", None))
        self.labelFertigkeit.setText(QCoreApplication.translate("dialog", u"Fertigkeit", None))
        self.labelTalent.setText(QCoreApplication.translate("dialog", u"Talent", None))
        self.labelKampfstil.setText(QCoreApplication.translate("dialog", u"Kampfstil", None))
        self.labelEigenschaften.setText(QCoreApplication.translate("dialog", u"Eigenschaften", None))
    # retranslateUi

