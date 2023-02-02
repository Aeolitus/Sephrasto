# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditVorteil.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_talentDialog(object):
    def setupUi(self, talentDialog):
        if not talentDialog.objectName():
            talentDialog.setObjectName(u"talentDialog")
        talentDialog.setWindowModality(Qt.ApplicationModal)
        talentDialog.resize(488, 772)
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
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboNachkauf = QComboBox(talentDialog)
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.addItem("")
        self.comboNachkauf.setObjectName(u"comboNachkauf")

        self.horizontalLayout.addWidget(self.comboNachkauf)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 1)

        self.voraussetzungenEdit = QPlainTextEdit(talentDialog)
        self.voraussetzungenEdit.setObjectName(u"voraussetzungenEdit")

        self.gridLayout.addWidget(self.voraussetzungenEdit, 6, 1, 1, 1)

        self.label_9 = QLabel(talentDialog)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setIndent(0)

        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)

        self.textEdit = QPlainTextEdit(talentDialog)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.textEdit, 7, 1, 1, 1)

        self.warning = QLabel(talentDialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.label_4 = QLabel(talentDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)

        self.label = QLabel(talentDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.line_2 = QFrame(talentDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 10, 0, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkVariable = QCheckBox(talentDialog)
        self.checkVariable.setObjectName(u"checkVariable")

        self.horizontalLayout_2.addWidget(self.checkVariable)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.kostenEdit = QSpinBox(talentDialog)
        self.kostenEdit.setObjectName(u"kostenEdit")
        self.kostenEdit.setAlignment(Qt.AlignCenter)
        self.kostenEdit.setMinimum(-10000)
        self.kostenEdit.setMaximum(10000)
        self.kostenEdit.setSingleStep(20)
        self.kostenEdit.setValue(40)

        self.horizontalLayout_2.addWidget(self.kostenEdit)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.nameEdit = QLineEdit(talentDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.checkCheatsheet = QCheckBox(talentDialog)
        self.checkCheatsheet.setObjectName(u"checkCheatsheet")
        self.checkCheatsheet.setChecked(True)

        self.gridLayout.addWidget(self.checkCheatsheet, 11, 1, 1, 1)

        self.teCheatsheet = QPlainTextEdit(talentDialog)
        self.teCheatsheet.setObjectName(u"teCheatsheet")
        sizePolicy.setHeightForWidth(self.teCheatsheet.sizePolicy().hasHeightForWidth())
        self.teCheatsheet.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.teCheatsheet, 12, 1, 1, 1)

        self.label_2 = QLabel(talentDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_10 = QLabel(talentDialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 11, 0, 1, 1)

        self.checkKommentar = QCheckBox(talentDialog)
        self.checkKommentar.setObjectName(u"checkKommentar")

        self.gridLayout.addWidget(self.checkKommentar, 3, 1, 1, 1)

        self.label_5 = QLabel(talentDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.scriptEdit = QLineEdit(talentDialog)
        self.scriptEdit.setObjectName(u"scriptEdit")

        self.horizontalLayout_4.addWidget(self.scriptEdit)

        self.scriptPrioEdit = QSpinBox(talentDialog)
        self.scriptPrioEdit.setObjectName(u"scriptPrioEdit")
        self.scriptPrioEdit.setMinimum(-10)
        self.scriptPrioEdit.setMaximum(10)
        self.scriptPrioEdit.setSingleStep(1)
        self.scriptPrioEdit.setValue(0)

        self.horizontalLayout_4.addWidget(self.scriptPrioEdit)


        self.gridLayout.addLayout(self.horizontalLayout_4, 8, 1, 1, 1)

        self.label_41 = QLabel(talentDialog)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_41, 6, 0, 1, 1)

        self.label_8 = QLabel(talentDialog)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setMinimumSize(QSize(0, 0))
        self.label_8.setMaximumSize(QSize(130, 16777215))
        self.label_8.setWordWrap(True)
        self.label_8.setIndent(0)

        self.gridLayout.addWidget(self.label_8, 12, 0, 1, 1)

        self.label_7 = QLabel(talentDialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboLinkKategorie = QComboBox(talentDialog)
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.addItem("")
        self.comboLinkKategorie.setObjectName(u"comboLinkKategorie")
        self.comboLinkKategorie.setMaximumSize(QSize(130, 16777215))

        self.horizontalLayout_5.addWidget(self.comboLinkKategorie)

        self.comboLinkElement = QComboBox(talentDialog)
        self.comboLinkElement.setObjectName(u"comboLinkElement")

        self.horizontalLayout_5.addWidget(self.comboLinkElement)


        self.gridLayout.addLayout(self.horizontalLayout_5, 9, 1, 1, 1)

        self.comboTyp = QComboBox(talentDialog)
        self.comboTyp.setObjectName(u"comboTyp")

        self.gridLayout.addWidget(self.comboTyp, 5, 1, 1, 1)

        self.label_6 = QLabel(talentDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.label_3 = QLabel(talentDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nameEdit, self.checkVariable)
        QWidget.setTabOrder(self.checkVariable, self.kostenEdit)
        QWidget.setTabOrder(self.kostenEdit, self.checkKommentar)
        QWidget.setTabOrder(self.checkKommentar, self.comboNachkauf)
        QWidget.setTabOrder(self.comboNachkauf, self.comboTyp)
        QWidget.setTabOrder(self.comboTyp, self.voraussetzungenEdit)
        QWidget.setTabOrder(self.voraussetzungenEdit, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.scriptEdit)
        QWidget.setTabOrder(self.scriptEdit, self.scriptPrioEdit)
        QWidget.setTabOrder(self.scriptPrioEdit, self.comboLinkKategorie)
        QWidget.setTabOrder(self.comboLinkKategorie, self.comboLinkElement)
        QWidget.setTabOrder(self.comboLinkElement, self.checkCheatsheet)
        QWidget.setTabOrder(self.checkCheatsheet, self.teCheatsheet)

        self.retranslateUi(talentDialog)
        self.buttonBox.accepted.connect(talentDialog.accept)
        self.buttonBox.rejected.connect(talentDialog.reject)

        QMetaObject.connectSlotsByName(talentDialog)
    # setupUi

    def retranslateUi(self, talentDialog):
        talentDialog.setWindowTitle(QCoreApplication.translate("talentDialog", u"Sephrasto - Vorteil bearbeiten...", None))
        self.comboNachkauf.setItemText(0, QCoreApplication.translate("talentDialog", u"h\u00e4ufig", None))
        self.comboNachkauf.setItemText(1, QCoreApplication.translate("talentDialog", u"\u00fcblich", None))
        self.comboNachkauf.setItemText(2, QCoreApplication.translate("talentDialog", u"selten", None))
        self.comboNachkauf.setItemText(3, QCoreApplication.translate("talentDialog", u"extrem selten", None))
        self.comboNachkauf.setItemText(4, QCoreApplication.translate("talentDialog", u"nicht m\u00f6glich", None))

        self.label_9.setText(QCoreApplication.translate("talentDialog", u"Verkn\u00fcpfung", None))
        self.warning.setText(QCoreApplication.translate("talentDialog", u"<html><head/><body><p>Dies ist ein Ilaris-Standardvorteil. Sobald du hier etwas ver\u00e4nderst, bekommst du eine pers\u00f6nliche Kopie und das Original wird in den Hausregeln gel\u00f6scht. Damit erh\u00e4ltst du f\u00fcr diesen Vorteil keine automatischen Updates mehr mit neuen Sephrasto-Versionen.</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("talentDialog", u"Script / Priorit\u00e4t", None))
        self.label.setText(QCoreApplication.translate("talentDialog", u"Vorteilsname", None))
        self.checkVariable.setText(QCoreApplication.translate("talentDialog", u"Kosten sind Variabel", None))
        self.kostenEdit.setSuffix(QCoreApplication.translate("talentDialog", u" EP", None))
        self.checkCheatsheet.setText(QCoreApplication.translate("talentDialog", u"Auflisten", None))
        self.label_2.setText(QCoreApplication.translate("talentDialog", u"Lernkosten", None))
        self.label_10.setText(QCoreApplication.translate("talentDialog", u"Regelanhang", None))
        self.checkKommentar.setText(QCoreApplication.translate("talentDialog", u"Nutzern erlauben einen Kommentar einzutragen", None))
        self.label_5.setText(QCoreApplication.translate("talentDialog", u"Beschreibung", None))
        self.label_41.setText(QCoreApplication.translate("talentDialog", u"Voraussetzungen", None))
        self.label_8.setText(QCoreApplication.translate("talentDialog", u"Alternative Beschreibung (optional)", None))
        self.label_7.setText(QCoreApplication.translate("talentDialog", u"Kommentar", None))
        self.comboLinkKategorie.setItemText(0, QCoreApplication.translate("talentDialog", u"Nicht verkn\u00fcpfen", None))
        self.comboLinkKategorie.setItemText(1, QCoreApplication.translate("talentDialog", u"Man\u00f6ver / Mod.", None))
        self.comboLinkKategorie.setItemText(2, QCoreApplication.translate("talentDialog", u"\u00dcbernat. Talent", None))
        self.comboLinkKategorie.setItemText(3, QCoreApplication.translate("talentDialog", u"Vorteil", None))

        self.label_6.setText(QCoreApplication.translate("talentDialog", u"Typ", None))
        self.label_3.setText(QCoreApplication.translate("talentDialog", u"Nachkauf", None))
    # retranslateUi

