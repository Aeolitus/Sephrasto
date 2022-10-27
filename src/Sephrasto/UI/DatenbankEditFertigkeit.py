# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditFertigkeit.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

class Ui_talentDialog(object):
    def setupUi(self, talentDialog):
        if not talentDialog.objectName():
            talentDialog.setObjectName(u"talentDialog")
        talentDialog.setWindowModality(Qt.ApplicationModal)
        talentDialog.resize(440, 517)
        self.gridLayout_2 = QGridLayout(talentDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(talentDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelVoraussetzungen = QLabel(talentDialog)
        self.labelVoraussetzungen.setObjectName(u"labelVoraussetzungen")

        self.gridLayout.addWidget(self.labelVoraussetzungen, 7, 0, 1, 1)

        self.label = QLabel(talentDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_3 = QLabel(talentDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.labelGruppieren = QLabel(talentDialog)
        self.labelGruppieren.setObjectName(u"labelGruppieren")

        self.gridLayout.addWidget(self.labelGruppieren, 6, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboAttribut1 = QComboBox(talentDialog)
        self.comboAttribut1.addItem("")
        self.comboAttribut1.addItem("")
        self.comboAttribut1.addItem("")
        self.comboAttribut1.addItem("")
        self.comboAttribut1.addItem("")
        self.comboAttribut1.addItem("")
        self.comboAttribut1.addItem("")
        self.comboAttribut1.addItem("")
        self.comboAttribut1.setObjectName(u"comboAttribut1")
        self.comboAttribut1.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut1)

        self.label_6 = QLabel(talentDialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_6)

        self.comboAttribut2 = QComboBox(talentDialog)
        self.comboAttribut2.addItem("")
        self.comboAttribut2.addItem("")
        self.comboAttribut2.addItem("")
        self.comboAttribut2.addItem("")
        self.comboAttribut2.addItem("")
        self.comboAttribut2.addItem("")
        self.comboAttribut2.addItem("")
        self.comboAttribut2.addItem("")
        self.comboAttribut2.setObjectName(u"comboAttribut2")
        self.comboAttribut2.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut2)

        self.label_7 = QLabel(talentDialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.comboAttribut3 = QComboBox(talentDialog)
        self.comboAttribut3.addItem("")
        self.comboAttribut3.addItem("")
        self.comboAttribut3.addItem("")
        self.comboAttribut3.addItem("")
        self.comboAttribut3.addItem("")
        self.comboAttribut3.addItem("")
        self.comboAttribut3.addItem("")
        self.comboAttribut3.addItem("")
        self.comboAttribut3.setObjectName(u"comboAttribut3")
        self.comboAttribut3.setMinimumSize(QSize(45, 0))

        self.horizontalLayout.addWidget(self.comboAttribut3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.nameEdit = QLineEdit(talentDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.label_5 = QLabel(talentDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)

        self.label_12 = QLabel(talentDialog)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)

        self.warning = QLabel(talentDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.textEdit = QPlainTextEdit(talentDialog)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.textEdit, 8, 1, 1, 1)

        self.labelKampffertigkeit = QLabel(talentDialog)
        self.labelKampffertigkeit.setObjectName(u"labelKampffertigkeit")

        self.gridLayout.addWidget(self.labelKampffertigkeit, 5, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.steigerungsfaktorEdit = QSpinBox(talentDialog)
        self.steigerungsfaktorEdit.setObjectName(u"steigerungsfaktorEdit")
        self.steigerungsfaktorEdit.setMinimum(1)
        self.steigerungsfaktorEdit.setMaximum(4)
        self.steigerungsfaktorEdit.setSingleStep(1)
        self.steigerungsfaktorEdit.setValue(2)

        self.horizontalLayout_2.addWidget(self.steigerungsfaktorEdit)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.voraussetzungenEdit = QPlainTextEdit(talentDialog)
        self.voraussetzungenEdit.setObjectName(u"voraussetzungenEdit")

        self.gridLayout.addWidget(self.voraussetzungenEdit, 7, 1, 1, 1)

        self.checkGruppieren = QCheckBox(talentDialog)
        self.checkGruppieren.setObjectName(u"checkGruppieren")

        self.gridLayout.addWidget(self.checkGruppieren, 6, 1, 1, 1)

        self.comboKampffertigkeit = QComboBox(talentDialog)
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.addItem("")
        self.comboKampffertigkeit.setObjectName(u"comboKampffertigkeit")

        self.gridLayout.addWidget(self.comboKampffertigkeit, 5, 1, 1, 1)

        self.label_2 = QLabel(talentDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.comboTyp = QComboBox(talentDialog)
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 4, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nameEdit, self.steigerungsfaktorEdit)
        QWidget.setTabOrder(self.steigerungsfaktorEdit, self.comboAttribut1)
        QWidget.setTabOrder(self.comboAttribut1, self.comboAttribut2)
        QWidget.setTabOrder(self.comboAttribut2, self.comboAttribut3)
        QWidget.setTabOrder(self.comboAttribut3, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.comboKampffertigkeit)
        QWidget.setTabOrder(self.comboKampffertigkeit, self.checkGruppieren)
        QWidget.setTabOrder(self.checkGruppieren, self.voraussetzungenEdit)
        QWidget.setTabOrder(self.voraussetzungenEdit, self.textEdit)

        self.retranslateUi(talentDialog)
        self.buttonBox.accepted.connect(talentDialog.accept)
        self.buttonBox.rejected.connect(talentDialog.reject)

        QMetaObject.connectSlotsByName(talentDialog)
    # setupUi

    def retranslateUi(self, talentDialog):
        talentDialog.setWindowTitle(QCoreApplication.translate("talentDialog", u"Sephrasto - Fertigkeit bearbeiten...", None))
        self.labelVoraussetzungen.setText(QCoreApplication.translate("talentDialog", u"Voraussetzungen", None))
        self.label.setText(QCoreApplication.translate("talentDialog", u"Fertigkeitsname", None))
        self.label_3.setText(QCoreApplication.translate("talentDialog", u"Attribute", None))
        self.labelGruppieren.setText(QCoreApplication.translate("talentDialog", u"Talente", None))
        self.comboAttribut1.setItemText(0, QCoreApplication.translate("talentDialog", u"KO", None))
        self.comboAttribut1.setItemText(1, QCoreApplication.translate("talentDialog", u"MU", None))
        self.comboAttribut1.setItemText(2, QCoreApplication.translate("talentDialog", u"GE", None))
        self.comboAttribut1.setItemText(3, QCoreApplication.translate("talentDialog", u"KK", None))
        self.comboAttribut1.setItemText(4, QCoreApplication.translate("talentDialog", u"IN", None))
        self.comboAttribut1.setItemText(5, QCoreApplication.translate("talentDialog", u"KL", None))
        self.comboAttribut1.setItemText(6, QCoreApplication.translate("talentDialog", u"CH", None))
        self.comboAttribut1.setItemText(7, QCoreApplication.translate("talentDialog", u"FF", None))

        self.label_6.setText(QCoreApplication.translate("talentDialog", u" - ", None))
        self.comboAttribut2.setItemText(0, QCoreApplication.translate("talentDialog", u"KO", None))
        self.comboAttribut2.setItemText(1, QCoreApplication.translate("talentDialog", u"MU", None))
        self.comboAttribut2.setItemText(2, QCoreApplication.translate("talentDialog", u"GE", None))
        self.comboAttribut2.setItemText(3, QCoreApplication.translate("talentDialog", u"KK", None))
        self.comboAttribut2.setItemText(4, QCoreApplication.translate("talentDialog", u"IN", None))
        self.comboAttribut2.setItemText(5, QCoreApplication.translate("talentDialog", u"KL", None))
        self.comboAttribut2.setItemText(6, QCoreApplication.translate("talentDialog", u"CH", None))
        self.comboAttribut2.setItemText(7, QCoreApplication.translate("talentDialog", u"FF", None))

        self.label_7.setText(QCoreApplication.translate("talentDialog", u" - ", None))
        self.comboAttribut3.setItemText(0, QCoreApplication.translate("talentDialog", u"KO", None))
        self.comboAttribut3.setItemText(1, QCoreApplication.translate("talentDialog", u"MU", None))
        self.comboAttribut3.setItemText(2, QCoreApplication.translate("talentDialog", u"GE", None))
        self.comboAttribut3.setItemText(3, QCoreApplication.translate("talentDialog", u"KK", None))
        self.comboAttribut3.setItemText(4, QCoreApplication.translate("talentDialog", u"IN", None))
        self.comboAttribut3.setItemText(5, QCoreApplication.translate("talentDialog", u"KL", None))
        self.comboAttribut3.setItemText(6, QCoreApplication.translate("talentDialog", u"CH", None))
        self.comboAttribut3.setItemText(7, QCoreApplication.translate("talentDialog", u"FF", None))

        self.label_5.setText(QCoreApplication.translate("talentDialog", u"Beschreibung", None))
        self.label_12.setText(QCoreApplication.translate("talentDialog", u"Typ", None))
        self.warning.setText(QCoreApplication.translate("talentDialog", u"<html><head/><body><p>Dies ist eine Ilaris-Standardfertigkeit. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr diese Fertigkeit keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.labelKampffertigkeit.setText(QCoreApplication.translate("talentDialog", u"Kampffertigkeit", None))
        self.steigerungsfaktorEdit.setSuffix("")
#if QT_CONFIG(tooltip)
        self.checkGruppieren.setToolTip(QCoreApplication.translate("talentDialog", u"<html><head/><body><p>Talente werden grunds\u00e4tzlich nach Fertigkeitstyp gruppiert. Mit dieser Option werden sie zus\u00e4tzlich noch nach dem Namen der Fertigkeit gruppiert. Bei Talenten mit mehreren Fertigkeiten werden bei der Gruppierung au\u00dferdem Fertigkeiten mit dieser Option priorisiert.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkGruppieren.setText(QCoreApplication.translate("talentDialog", u"Nach dieser Fertigkeit priorisiert gruppieren", None))
        self.comboKampffertigkeit.setItemText(0, QCoreApplication.translate("talentDialog", u"Keine Kampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(1, QCoreApplication.translate("talentDialog", u"Nahkampffertigkeit", None))
        self.comboKampffertigkeit.setItemText(2, QCoreApplication.translate("talentDialog", u"Sonstige Kampffertigkeit", None))

#if QT_CONFIG(tooltip)
        self.comboKampffertigkeit.setToolTip(QCoreApplication.translate("talentDialog", u"Nahkampf- und Sonstige Kampffertigkeiten stehen bei Waffen zur Auswahl. Nahkampffertigkeiten werden gegebenenfalls nach einem abweichenden Steigerungsfaktor berechnet.", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("talentDialog", u"Steigerungsfaktor", None))
#if QT_CONFIG(tooltip)
        self.comboTyp.setToolTip(QCoreApplication.translate("talentDialog", u"Fertigkeiten werden nach diesem Typ gruppiert und dann alphabetisch sortiert.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

