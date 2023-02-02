# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankMain.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QListView,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.ApplicationModal)
        Form.resize(795, 535)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.labelParameter = QLabel(Form)
        self.labelParameter.setObjectName(u"labelParameter")
        font = QFont()
        font.setBold(True)
        self.labelParameter.setFont(font)

        self.verticalLayout.addWidget(self.labelParameter)

        self.nameFilterEdit = QLineEdit(Form)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")

        self.verticalLayout.addWidget(self.nameFilterEdit)

        self.checkFilterTyp = QCheckBox(Form)
        self.checkFilterTyp.setObjectName(u"checkFilterTyp")
        self.checkFilterTyp.setFont(font)
        self.checkFilterTyp.setChecked(True)
        self.checkFilterTyp.setTristate(True)

        self.verticalLayout.addWidget(self.checkFilterTyp)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.showVorteile = QCheckBox(Form)
        self.showVorteile.setObjectName(u"showVorteile")
        self.showVorteile.setChecked(True)
        self.showVorteile.setTristate(False)

        self.verticalLayout_3.addWidget(self.showVorteile)

        self.showFertigkeiten = QCheckBox(Form)
        self.showFertigkeiten.setObjectName(u"showFertigkeiten")
        self.showFertigkeiten.setChecked(True)

        self.verticalLayout_3.addWidget(self.showFertigkeiten)

        self.showFreieFertigkeiten = QCheckBox(Form)
        self.showFreieFertigkeiten.setObjectName(u"showFreieFertigkeiten")
        self.showFreieFertigkeiten.setChecked(True)

        self.verticalLayout_3.addWidget(self.showFreieFertigkeiten)

        self.showUebernatuerlicheFertigkeiten = QCheckBox(Form)
        self.showUebernatuerlicheFertigkeiten.setObjectName(u"showUebernatuerlicheFertigkeiten")
        self.showUebernatuerlicheFertigkeiten.setMinimumSize(QSize(200, 0))
        self.showUebernatuerlicheFertigkeiten.setChecked(True)

        self.verticalLayout_3.addWidget(self.showUebernatuerlicheFertigkeiten)

        self.showTalente = QCheckBox(Form)
        self.showTalente.setObjectName(u"showTalente")
        self.showTalente.setChecked(True)

        self.verticalLayout_3.addWidget(self.showTalente)

        self.showRuestungen = QCheckBox(Form)
        self.showRuestungen.setObjectName(u"showRuestungen")
        self.showRuestungen.setChecked(True)

        self.verticalLayout_3.addWidget(self.showRuestungen)

        self.showWaffen = QCheckBox(Form)
        self.showWaffen.setObjectName(u"showWaffen")
        self.showWaffen.setChecked(True)

        self.verticalLayout_3.addWidget(self.showWaffen)

        self.showWaffeneigenschaften = QCheckBox(Form)
        self.showWaffeneigenschaften.setObjectName(u"showWaffeneigenschaften")
        self.showWaffeneigenschaften.setChecked(True)

        self.verticalLayout_3.addWidget(self.showWaffeneigenschaften)

        self.showManoever = QCheckBox(Form)
        self.showManoever.setObjectName(u"showManoever")
        self.showManoever.setChecked(True)

        self.verticalLayout_3.addWidget(self.showManoever)

        self.showEinstellung = QCheckBox(Form)
        self.showEinstellung.setObjectName(u"showEinstellung")
        self.showEinstellung.setChecked(True)

        self.verticalLayout_3.addWidget(self.showEinstellung)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.labelParameter1 = QLabel(Form)
        self.labelParameter1.setObjectName(u"labelParameter1")
        self.labelParameter1.setFont(font)

        self.verticalLayout.addWidget(self.labelParameter1)

        self.showDeleted = QCheckBox(Form)
        self.showDeleted.setObjectName(u"showDeleted")
        self.showDeleted.setChecked(True)

        self.verticalLayout.addWidget(self.showDeleted)

        self.showUserAdded = QCheckBox(Form)
        self.showUserAdded.setObjectName(u"showUserAdded")
        self.showUserAdded.setChecked(False)

        self.verticalLayout.addWidget(self.showUserAdded)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonCloseDB = QPushButton(Form)
        self.buttonCloseDB.setObjectName(u"buttonCloseDB")
        self.buttonCloseDB.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.buttonCloseDB)

        self.buttonLoadDB = QPushButton(Form)
        self.buttonLoadDB.setObjectName(u"buttonLoadDB")
        self.buttonLoadDB.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.buttonLoadDB)

        self.buttonSaveDB = QPushButton(Form)
        self.buttonSaveDB.setObjectName(u"buttonSaveDB")
        self.buttonSaveDB.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.buttonSaveDB)

        self.buttonQuicksave = QPushButton(Form)
        self.buttonQuicksave.setObjectName(u"buttonQuicksave")
        self.buttonQuicksave.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.buttonQuicksave)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listDatenbank = QListView(Form)
        self.listDatenbank.setObjectName(u"listDatenbank")

        self.verticalLayout_2.addWidget(self.listDatenbank)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonHinzufuegen = QPushButton(Form)
        self.buttonHinzufuegen.setObjectName(u"buttonHinzufuegen")
        self.buttonHinzufuegen.setMinimumSize(QSize(28, 28))
        self.buttonHinzufuegen.setMaximumSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.buttonHinzufuegen)

        self.buttonEditieren = QPushButton(Form)
        self.buttonEditieren.setObjectName(u"buttonEditieren")
        self.buttonEditieren.setMinimumSize(QSize(28, 28))
        self.buttonEditieren.setMaximumSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.buttonEditieren)

        self.buttonDuplizieren = QPushButton(Form)
        self.buttonDuplizieren.setObjectName(u"buttonDuplizieren")
        self.buttonDuplizieren.setMinimumSize(QSize(28, 28))
        self.buttonDuplizieren.setMaximumSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.buttonDuplizieren)

        self.buttonLoeschen = QPushButton(Form)
        self.buttonLoeschen.setObjectName(u"buttonLoeschen")
        self.buttonLoeschen.setMinimumSize(QSize(28, 28))
        self.buttonLoeschen.setMaximumSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.buttonLoeschen)

        self.buttonWiederherstellen = QPushButton(Form)
        self.buttonWiederherstellen.setObjectName(u"buttonWiederherstellen")
        self.buttonWiederherstellen.setMinimumSize(QSize(28, 28))
        self.buttonWiederherstellen.setMaximumSize(QSize(28, 28))
        self.buttonWiederherstellen.setVisible(False)

        self.horizontalLayout.addWidget(self.buttonWiederherstellen)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(1, 1)

        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nameFilterEdit, self.checkFilterTyp)
        QWidget.setTabOrder(self.checkFilterTyp, self.showVorteile)
        QWidget.setTabOrder(self.showVorteile, self.showFertigkeiten)
        QWidget.setTabOrder(self.showFertigkeiten, self.showFreieFertigkeiten)
        QWidget.setTabOrder(self.showFreieFertigkeiten, self.showUebernatuerlicheFertigkeiten)
        QWidget.setTabOrder(self.showUebernatuerlicheFertigkeiten, self.showTalente)
        QWidget.setTabOrder(self.showTalente, self.showRuestungen)
        QWidget.setTabOrder(self.showRuestungen, self.showWaffen)
        QWidget.setTabOrder(self.showWaffen, self.showWaffeneigenschaften)
        QWidget.setTabOrder(self.showWaffeneigenschaften, self.showManoever)
        QWidget.setTabOrder(self.showManoever, self.showEinstellung)
        QWidget.setTabOrder(self.showEinstellung, self.showDeleted)
        QWidget.setTabOrder(self.showDeleted, self.showUserAdded)
        QWidget.setTabOrder(self.showUserAdded, self.buttonCloseDB)
        QWidget.setTabOrder(self.buttonCloseDB, self.buttonLoadDB)
        QWidget.setTabOrder(self.buttonLoadDB, self.buttonSaveDB)
        QWidget.setTabOrder(self.buttonSaveDB, self.buttonQuicksave)
        QWidget.setTabOrder(self.buttonQuicksave, self.listDatenbank)
        QWidget.setTabOrder(self.listDatenbank, self.buttonHinzufuegen)
        QWidget.setTabOrder(self.buttonHinzufuegen, self.buttonEditieren)
        QWidget.setTabOrder(self.buttonEditieren, self.buttonDuplizieren)
        QWidget.setTabOrder(self.buttonDuplizieren, self.buttonLoeschen)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Sephrasto - Datenbank-Editor", None))
        self.labelParameter.setText(QCoreApplication.translate("Form", u"Filter nach Name:", None))
        self.labelParameter.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.checkFilterTyp.setText(QCoreApplication.translate("Form", u"Filter nach Typ:", None))
        self.checkFilterTyp.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.showVorteile.setText(QCoreApplication.translate("Form", u"Vorteile", None))
        self.showFertigkeiten.setText(QCoreApplication.translate("Form", u"Profane Fertigkeiten", None))
        self.showFreieFertigkeiten.setText(QCoreApplication.translate("Form", u"Freie Fertigkeiten", None))
        self.showUebernatuerlicheFertigkeiten.setText(QCoreApplication.translate("Form", u"\u00dcbernat\u00fcrliche Fertigkeiten", None))
        self.showTalente.setText(QCoreApplication.translate("Form", u"Talente", None))
        self.showRuestungen.setText(QCoreApplication.translate("Form", u"R\u00fcstungen", None))
        self.showWaffen.setText(QCoreApplication.translate("Form", u"Waffen", None))
        self.showWaffeneigenschaften.setText(QCoreApplication.translate("Form", u"Waffeneigenschaften", None))
        self.showManoever.setText(QCoreApplication.translate("Form", u"Man\u00f6ver / Modifikation / Regel", None))
        self.showEinstellung.setText(QCoreApplication.translate("Form", u"Einstellung", None))
        self.labelParameter1.setText(QCoreApplication.translate("Form", u"Filter nach Status:", None))
        self.labelParameter1.setProperty("class", QCoreApplication.translate("Form", u"h4", None))
        self.showDeleted.setText(QCoreApplication.translate("Form", u"Gel\u00f6schte Standardelemente", None))
        self.showUserAdded.setText(QCoreApplication.translate("Form", u"Nur eigene \u00c4nderungen", None))
        self.buttonCloseDB.setText(QCoreApplication.translate("Form", u"Hausregeln schlie\u00dfen", None))
        self.buttonLoadDB.setText(QCoreApplication.translate("Form", u"Hausregeln laden", None))
        self.buttonSaveDB.setText(QCoreApplication.translate("Form", u"Speichern unter...", None))
        self.buttonQuicksave.setText(QCoreApplication.translate("Form", u"Speichern", None))
#if QT_CONFIG(tooltip)
        self.buttonHinzufuegen.setToolTip(QCoreApplication.translate("Form", u"Hinzuf\u00fcgen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonHinzufuegen.setText(QCoreApplication.translate("Form", u"Hinzuf\u00fcgen", None))
        self.buttonHinzufuegen.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonEditieren.setToolTip(QCoreApplication.translate("Form", u"Editieren", None))
#endif // QT_CONFIG(tooltip)
        self.buttonEditieren.setText(QCoreApplication.translate("Form", u"Editieren", None))
        self.buttonEditieren.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonDuplizieren.setToolTip(QCoreApplication.translate("Form", u"Duplizieren", None))
#endif // QT_CONFIG(tooltip)
        self.buttonDuplizieren.setText(QCoreApplication.translate("Form", u"Duplizieren", None))
        self.buttonDuplizieren.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonLoeschen.setToolTip(QCoreApplication.translate("Form", u"L\u00f6schen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonLoeschen.setText(QCoreApplication.translate("Form", u"L\u00f6schen", None))
        self.buttonLoeschen.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonWiederherstellen.setToolTip(QCoreApplication.translate("Form", u"Wiederherstellen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonWiederherstellen.setText(QCoreApplication.translate("Form", u"Wiederherstellen", None))
    # retranslateUi

