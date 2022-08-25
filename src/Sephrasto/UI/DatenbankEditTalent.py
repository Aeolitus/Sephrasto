# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditTalent.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_talentDialog(object):
    def setupUi(self, talentDialog):
        if not talentDialog.objectName():
            talentDialog.setObjectName(u"talentDialog")
        talentDialog.setWindowModality(Qt.ApplicationModal)
        talentDialog.resize(442, 595)
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
        self.label_6 = QLabel(talentDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttonRegulaer = QRadioButton(talentDialog)
        self.buttonRegulaer.setObjectName(u"buttonRegulaer")
        self.buttonRegulaer.setChecked(True)

        self.verticalLayout.addWidget(self.buttonRegulaer)

        self.buttonVerbilligt = QRadioButton(talentDialog)
        self.buttonVerbilligt.setObjectName(u"buttonVerbilligt")

        self.verticalLayout.addWidget(self.buttonVerbilligt)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonSpezial = QRadioButton(talentDialog)
        self.buttonSpezial.setObjectName(u"buttonSpezial")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSpezial.sizePolicy().hasHeightForWidth())
        self.buttonSpezial.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.buttonSpezial)

        self.spinKosten = QSpinBox(talentDialog)
        self.spinKosten.setObjectName(u"spinKosten")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinKosten.sizePolicy().hasHeightForWidth())
        self.spinKosten.setSizePolicy(sizePolicy1)
        self.spinKosten.setMinimumSize(QSize(60, 0))
        self.spinKosten.setAlignment(Qt.AlignCenter)
        self.spinKosten.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinKosten.setMinimum(0)
        self.spinKosten.setMaximum(200)
        self.spinKosten.setSingleStep(20)

        self.horizontalLayout.addWidget(self.spinKosten)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkVariable = QCheckBox(talentDialog)
        self.checkVariable.setObjectName(u"checkVariable")

        self.horizontalLayout_2.addWidget(self.checkVariable)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 3, 1, 1, 1)

        self.nameEdit = QLineEdit(talentDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.warning = QLabel(talentDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.label_2 = QLabel(talentDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.textEdit = QPlainTextEdit(talentDialog)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.textEdit, 8, 1, 1, 1)

        self.checkCheatsheet = QCheckBox(talentDialog)
        self.checkCheatsheet.setObjectName(u"checkCheatsheet")
        self.checkCheatsheet.setLayoutDirection(Qt.LeftToRight)
        self.checkCheatsheet.setChecked(True)

        self.gridLayout.addWidget(self.checkCheatsheet, 5, 1, 1, 1)

        self.voraussetzungenEdit = QPlainTextEdit(talentDialog)
        self.voraussetzungenEdit.setObjectName(u"voraussetzungenEdit")

        self.gridLayout.addWidget(self.voraussetzungenEdit, 7, 1, 1, 1)

        self.label = QLabel(talentDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_7 = QLabel(talentDialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.label_3 = QLabel(talentDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.label_4 = QLabel(talentDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)

        self.label_5 = QLabel(talentDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)

        self.fertigkeitenEdit = QLineEdit(talentDialog)
        self.fertigkeitenEdit.setObjectName(u"fertigkeitenEdit")

        self.gridLayout.addWidget(self.fertigkeitenEdit, 6, 1, 1, 1)

        self.checkKommentar = QCheckBox(talentDialog)
        self.checkKommentar.setObjectName(u"checkKommentar")

        self.gridLayout.addWidget(self.checkKommentar, 4, 1, 1, 1)

        self.label_8 = QLabel(talentDialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 9, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.comboSeite = QComboBox(talentDialog)
        self.comboSeite.setObjectName(u"comboSeite")

        self.horizontalLayout_3.addWidget(self.comboSeite)

        self.spinSeite = QSpinBox(talentDialog)
        self.spinSeite.setObjectName(u"spinSeite")
        self.spinSeite.setMaximum(999)

        self.horizontalLayout_3.addWidget(self.spinSeite)


        self.gridLayout.addLayout(self.horizontalLayout_3, 9, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nameEdit, self.buttonRegulaer)
        QWidget.setTabOrder(self.buttonRegulaer, self.buttonVerbilligt)
        QWidget.setTabOrder(self.buttonVerbilligt, self.buttonSpezial)
        QWidget.setTabOrder(self.buttonSpezial, self.spinKosten)
        QWidget.setTabOrder(self.spinKosten, self.checkVariable)
        QWidget.setTabOrder(self.checkVariable, self.checkKommentar)
        QWidget.setTabOrder(self.checkKommentar, self.checkCheatsheet)
        QWidget.setTabOrder(self.checkCheatsheet, self.fertigkeitenEdit)
        QWidget.setTabOrder(self.fertigkeitenEdit, self.voraussetzungenEdit)
        QWidget.setTabOrder(self.voraussetzungenEdit, self.textEdit)

        self.retranslateUi(talentDialog)
        self.buttonBox.accepted.connect(talentDialog.accept)
        self.buttonBox.rejected.connect(talentDialog.reject)

        QMetaObject.connectSlotsByName(talentDialog)
    # setupUi

    def retranslateUi(self, talentDialog):
        talentDialog.setWindowTitle(QCoreApplication.translate("talentDialog", u"Sephrasto - Talent bearbeiten...", None))
        self.label_6.setText(QCoreApplication.translate("talentDialog", u"Kommentar", None))
        self.buttonRegulaer.setText(QCoreApplication.translate("talentDialog", u"Regul\u00e4res Talent (Kosten nach Fertigkeit)", None))
        self.buttonVerbilligt.setText(QCoreApplication.translate("talentDialog", u"Verbilligtes Talent (Kosten nach Fertigkeit)", None))
        self.buttonSpezial.setText(QCoreApplication.translate("talentDialog", u"Spezialtalent (Kosten frei w\u00e4hlbar)", None))
        self.spinKosten.setSuffix(QCoreApplication.translate("talentDialog", u" EP", None))
        self.checkVariable.setText(QCoreApplication.translate("talentDialog", u"Kosten sind variabel", None))
        self.warning.setText(QCoreApplication.translate("talentDialog", u"<html><head/><body><p>Dies ist ein Ilaris-Standardtalent. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr dieses Talent keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("talentDialog", u"Lernkosten", None))
        self.checkCheatsheet.setText(QCoreApplication.translate("talentDialog", u"Auflisten", None))
        self.label.setText(QCoreApplication.translate("talentDialog", u"Talentname", None))
        self.label_7.setText(QCoreApplication.translate("talentDialog", u"Regelanhang", None))
        self.label_3.setText(QCoreApplication.translate("talentDialog", u"Fertigkeiten", None))
        self.label_4.setText(QCoreApplication.translate("talentDialog", u"Voraussetzungen", None))
        self.label_5.setText(QCoreApplication.translate("talentDialog", u"Beschreibung", None))
        self.checkKommentar.setText(QCoreApplication.translate("talentDialog", u"Nutzern erlauben einen Kommentar einzutragen", None))
        self.label_8.setText(QCoreApplication.translate("talentDialog", u"Seitenreferenz", None))
    # retranslateUi

