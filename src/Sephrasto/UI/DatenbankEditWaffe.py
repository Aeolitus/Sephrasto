# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditWaffe.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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

class Ui_talentDialog(object):
    def setupUi(self, talentDialog):
        if not talentDialog.objectName():
            talentDialog.setObjectName(u"talentDialog")
        talentDialog.setWindowModality(Qt.ApplicationModal)
        talentDialog.resize(440, 394)
        self.gridLayout_2 = QGridLayout(talentDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.spinHaerte = QSpinBox(talentDialog)
        self.spinHaerte.setObjectName(u"spinHaerte")
        self.spinHaerte.setMinimumSize(QSize(50, 0))
        self.spinHaerte.setAlignment(Qt.AlignCenter)
        self.spinHaerte.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinHaerte.setMinimum(0)
        self.spinHaerte.setMaximum(99)
        self.spinHaerte.setValue(7)

        self.horizontalLayout_6.addWidget(self.spinHaerte)


        self.gridLayout.addLayout(self.horizontalLayout_6, 6, 1, 1, 1)

        self.label_9 = QLabel(talentDialog)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)

        self.label_4 = QLabel(talentDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboTyp = QComboBox(talentDialog)
        self.comboTyp.addItem("")
        self.comboTyp.addItem("")
        self.comboTyp.setObjectName(u"comboTyp")

        self.horizontalLayout_2.addWidget(self.comboTyp)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.spinRW1 = QSpinBox(talentDialog)
        self.spinRW1.setObjectName(u"spinRW1")
        self.spinRW1.setMinimumSize(QSize(50, 0))
        self.spinRW1.setAlignment(Qt.AlignCenter)
        self.spinRW1.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinRW1.setMaximum(999)
        self.spinRW1.setValue(1)

        self.horizontalLayout_4.addWidget(self.spinRW1)


        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 1, 1, 1)

        self.nameEdit = QLineEdit(talentDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.label = QLabel(talentDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_5 = QLabel(talentDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 10, 0, 1, 1)

        self.labelWMLZ = QLabel(talentDialog)
        self.labelWMLZ.setObjectName(u"labelWMLZ")

        self.gridLayout.addWidget(self.labelWMLZ, 5, 0, 1, 1)

        self.label_2 = QLabel(talentDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_3 = QLabel(talentDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.spinWMLZ = QSpinBox(talentDialog)
        self.spinWMLZ.setObjectName(u"spinWMLZ")
        self.spinWMLZ.setMinimumSize(QSize(50, 0))
        self.spinWMLZ.setAlignment(Qt.AlignCenter)
        self.spinWMLZ.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinWMLZ.setMinimum(-99)
        self.spinWMLZ.setMaximum(99)

        self.horizontalLayout_5.addWidget(self.spinWMLZ)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 1, 1, 1)

        self.textEigenschaften = QPlainTextEdit(talentDialog)
        self.textEigenschaften.setObjectName(u"textEigenschaften")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEigenschaften.sizePolicy().hasHeightForWidth())
        self.textEigenschaften.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.textEigenschaften, 10, 1, 1, 1)

        self.label_6 = QLabel(talentDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinW6 = QSpinBox(talentDialog)
        self.spinW6.setObjectName(u"spinW6")
        self.spinW6.setAlignment(Qt.AlignCenter)
        self.spinW6.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinW6.setMinimum(0)
        self.spinW6.setMaximum(99)
        self.spinW6.setValue(2)

        self.horizontalLayout.addWidget(self.spinW6)

        self.label_7 = QLabel(talentDialog)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.spinPlus = QSpinBox(talentDialog)
        self.spinPlus.setObjectName(u"spinPlus")
        self.spinPlus.setMinimumSize(QSize(50, 0))
        self.spinPlus.setAlignment(Qt.AlignCenter)
        self.spinPlus.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinPlus.setMinimum(-99)
        self.spinPlus.setValue(2)

        self.horizontalLayout.addWidget(self.spinPlus)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.label_8 = QLabel(talentDialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.comboTalent = QComboBox(talentDialog)
        self.comboTalent.setObjectName(u"comboTalent")

        self.gridLayout.addWidget(self.comboTalent, 8, 1, 1, 1)

        self.label_10 = QLabel(talentDialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 9, 0, 1, 1)

        self.comboFert = QComboBox(talentDialog)
        self.comboFert.setObjectName(u"comboFert")

        self.gridLayout.addWidget(self.comboFert, 7, 1, 1, 1)

        self.layoutKampfstile = QGridLayout()
        self.layoutKampfstile.setObjectName(u"layoutKampfstile")

        self.gridLayout.addLayout(self.layoutKampfstile, 9, 1, 1, 1)

        self.warning = QLabel(talentDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 3)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(talentDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.nameEdit, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.spinW6)
        QWidget.setTabOrder(self.spinW6, self.spinPlus)
        QWidget.setTabOrder(self.spinPlus, self.spinRW1)
        QWidget.setTabOrder(self.spinRW1, self.spinWMLZ)
        QWidget.setTabOrder(self.spinWMLZ, self.spinHaerte)
        QWidget.setTabOrder(self.spinHaerte, self.comboFert)
        QWidget.setTabOrder(self.comboFert, self.comboTalent)
        QWidget.setTabOrder(self.comboTalent, self.textEigenschaften)

        self.retranslateUi(talentDialog)
        self.buttonBox.accepted.connect(talentDialog.accept)
        self.buttonBox.rejected.connect(talentDialog.reject)

        QMetaObject.connectSlotsByName(talentDialog)
    # setupUi

    def retranslateUi(self, talentDialog):
        talentDialog.setWindowTitle(QCoreApplication.translate("talentDialog", u"Sephrasto - Waffe bearbeiten...", None))
        self.label_9.setText(QCoreApplication.translate("talentDialog", u"H\u00e4rte", None))
        self.label_4.setText(QCoreApplication.translate("talentDialog", u"Reichweite", None))
        self.comboTyp.setItemText(0, QCoreApplication.translate("talentDialog", u"Nahkampfwaffe", None))
        self.comboTyp.setItemText(1, QCoreApplication.translate("talentDialog", u"Fernkampfwaffe", None))

        self.label.setText(QCoreApplication.translate("talentDialog", u"Waffenname", None))
        self.label_5.setText(QCoreApplication.translate("talentDialog", u"Eigenschaften", None))
        self.labelWMLZ.setText(QCoreApplication.translate("talentDialog", u"WM/LZ", None))
        self.label_2.setText(QCoreApplication.translate("talentDialog", u"Typ", None))
        self.label_3.setText(QCoreApplication.translate("talentDialog", u"Trefferpunkte", None))
        self.label_6.setText(QCoreApplication.translate("talentDialog", u"Fertigkeit", None))
        self.spinW6.setSuffix(QCoreApplication.translate("talentDialog", u" W6", None))
        self.label_7.setText(QCoreApplication.translate("talentDialog", u"+", None))
        self.label_8.setText(QCoreApplication.translate("talentDialog", u"Talent", None))
        self.label_10.setText(QCoreApplication.translate("talentDialog", u"Kampfstil", None))
        self.warning.setText(QCoreApplication.translate("talentDialog", u"<html><head/><body><p>Dies ist eine Ilaris-Standardwaffe. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr diese Waffe keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
    # retranslateUi

