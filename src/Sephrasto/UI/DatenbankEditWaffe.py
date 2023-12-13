# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditWaffe.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(440, 444)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_8 = QLabel(dialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 9, 0, 1, 1)

        self.label_6 = QLabel(dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 8, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboTyp = QComboBox(dialog)
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.setObjectName(u"comboTyp")

        self.horizontalLayout_2.addWidget(self.comboTyp)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.spinWM = QSpinBox(dialog)
        self.spinWM.setObjectName(u"spinWM")
        self.spinWM.setMinimumSize(QSize(50, 0))
        self.spinWM.setAlignment(Qt.AlignCenter)
        self.spinWM.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinWM.setMinimum(-99)
        self.spinWM.setMaximum(99)

        self.horizontalLayout_3.addWidget(self.spinWM)


        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.spinRW1 = QSpinBox(dialog)
        self.spinRW1.setObjectName(u"spinRW1")
        self.spinRW1.setMinimumSize(QSize(50, 0))
        self.spinRW1.setAlignment(Qt.AlignCenter)
        self.spinRW1.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinRW1.setMaximum(999)
        self.spinRW1.setValue(1)

        self.horizontalLayout_4.addWidget(self.spinRW1)


        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 1, 1, 1)

        self.layoutKampfstile = QGridLayout()
        self.layoutKampfstile.setObjectName(u"layoutKampfstile")

        self.gridLayout.addLayout(self.layoutKampfstile, 10, 1, 1, 1)

        self.label_5 = QLabel(dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 11, 0, 1, 1)

        self.label_3 = QLabel(dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.teEigenschaften = QPlainTextEdit(dialog)
        self.teEigenschaften.setObjectName(u"teEigenschaften")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teEigenschaften.sizePolicy().hasHeightForWidth())
        self.teEigenschaften.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.teEigenschaften, 11, 1, 1, 1)

        self.comboTalent = QComboBox(dialog)
        self.comboTalent.setObjectName(u"comboTalent")

        self.gridLayout.addWidget(self.comboTalent, 9, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.spinHaerte = QSpinBox(dialog)
        self.spinHaerte.setObjectName(u"spinHaerte")
        self.spinHaerte.setMinimumSize(QSize(50, 0))
        self.spinHaerte.setAlignment(Qt.AlignCenter)
        self.spinHaerte.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinHaerte.setMinimum(0)
        self.spinHaerte.setMaximum(99)
        self.spinHaerte.setValue(7)

        self.horizontalLayout_6.addWidget(self.spinHaerte)


        self.gridLayout.addLayout(self.horizontalLayout_6, 7, 1, 1, 1)

        self.label_2 = QLabel(dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.comboFert = QComboBox(dialog)
        self.comboFert.setObjectName(u"comboFert")

        self.gridLayout.addWidget(self.comboFert, 8, 1, 1, 1)

        self.labelWM = QLabel(dialog)
        self.labelWM.setObjectName(u"labelWM")

        self.gridLayout.addWidget(self.labelWM, 5, 0, 1, 1)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_9 = QLabel(dialog)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)

        self.leName = QLineEdit(dialog)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinWuerfel = QSpinBox(dialog)
        self.spinWuerfel.setObjectName(u"spinWuerfel")
        self.spinWuerfel.setMinimumSize(QSize(50, 0))
        self.spinWuerfel.setAlignment(Qt.AlignCenter)
        self.spinWuerfel.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinWuerfel.setMinimum(0)
        self.spinWuerfel.setMaximum(99)
        self.spinWuerfel.setValue(2)

        self.horizontalLayout.addWidget(self.spinWuerfel)

        self.comboWuerfelSeiten = QComboBox(dialog)
        self.comboWuerfelSeiten.addItem("")
        self.comboWuerfelSeiten.addItem("")
        self.comboWuerfelSeiten.setObjectName(u"comboWuerfelSeiten")

        self.horizontalLayout.addWidget(self.comboWuerfelSeiten)

        self.label_7 = QLabel(dialog)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.spinPlus = QSpinBox(dialog)
        self.spinPlus.setObjectName(u"spinPlus")
        self.spinPlus.setMinimumSize(QSize(50, 0))
        self.spinPlus.setAlignment(Qt.AlignCenter)
        self.spinPlus.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinPlus.setMinimum(-99)
        self.spinPlus.setValue(2)

        self.horizontalLayout.addWidget(self.spinPlus)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.label_4 = QLabel(dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.warning = QLabel(dialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 3)

        self.label_10 = QLabel(dialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 10, 0, 1, 1)

        self.labelLZ = QLabel(dialog)
        self.labelLZ.setObjectName(u"labelLZ")

        self.gridLayout.addWidget(self.labelLZ, 6, 0, 1, 1)

        self.layoutLZ = QHBoxLayout()
        self.layoutLZ.setObjectName(u"layoutLZ")
        self.spacerLZ = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layoutLZ.addItem(self.spacerLZ)

        self.spinLZ = QSpinBox(dialog)
        self.spinLZ.setObjectName(u"spinLZ")
        self.spinLZ.setMinimumSize(QSize(50, 0))
        self.spinLZ.setAlignment(Qt.AlignCenter)
        self.spinLZ.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.layoutLZ.addWidget(self.spinLZ)


        self.gridLayout.addLayout(self.layoutLZ, 6, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.spinWuerfel)
        QWidget.setTabOrder(self.spinWuerfel, self.comboWuerfelSeiten)
        QWidget.setTabOrder(self.comboWuerfelSeiten, self.spinPlus)
        QWidget.setTabOrder(self.spinPlus, self.spinRW1)
        QWidget.setTabOrder(self.spinRW1, self.spinWM)
        QWidget.setTabOrder(self.spinWM, self.spinLZ)
        QWidget.setTabOrder(self.spinLZ, self.spinHaerte)
        QWidget.setTabOrder(self.spinHaerte, self.comboFert)
        QWidget.setTabOrder(self.comboFert, self.comboTalent)
        QWidget.setTabOrder(self.comboTalent, self.teEigenschaften)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Waffe bearbeiten...", None))
        self.label_8.setText(QCoreApplication.translate("dialog", u"Talent", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"Fertigkeit", None))
        self.comboTyp.setItemText(0, QCoreApplication.translate("dialog", u"Nahkampfwaffe", None))
        self.comboTyp.setItemText(1, QCoreApplication.translate("dialog", u"Fernkampfwaffe", None))

        self.label_5.setText(QCoreApplication.translate("dialog", u"Eigenschaften", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Trefferpunkte", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Typ", None))
        self.labelWM.setText(QCoreApplication.translate("dialog", u"WM", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Waffenname", None))
        self.label_9.setText(QCoreApplication.translate("dialog", u"H\u00e4rte", None))
        self.spinWuerfel.setSuffix("")
        self.comboWuerfelSeiten.setItemText(0, QCoreApplication.translate("dialog", u"W6", None))
        self.comboWuerfelSeiten.setItemText(1, QCoreApplication.translate("dialog", u"W20", None))

        self.label_7.setText(QCoreApplication.translate("dialog", u"+", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Reichweite", None))
        self.warning.setText("")
        self.label_10.setText(QCoreApplication.translate("dialog", u"Kampfstil", None))
        self.labelLZ.setText(QCoreApplication.translate("dialog", u"LZ", None))
    # retranslateUi

