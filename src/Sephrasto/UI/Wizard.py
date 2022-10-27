# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Wizard.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_formMain(object):
    def setupUi(self, formMain):
        if not formMain.objectName():
            formMain.setObjectName(u"formMain")
        formMain.setWindowModality(Qt.ApplicationModal)
        formMain.resize(506, 472)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(formMain.sizePolicy().hasHeightForWidth())
        formMain.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(formMain)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btnCancel = QPushButton(formMain)
        self.btnCancel.setObjectName(u"btnCancel")

        self.horizontalLayout_3.addWidget(self.btnCancel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btnAccept = QPushButton(formMain)
        self.btnAccept.setObjectName(u"btnAccept")
        self.btnAccept.setEnabled(True)
        self.btnAccept.setMinimumSize(QSize(100, 0))
        self.btnAccept.setMaximumSize(QSize(16777214, 16777215))

        self.horizontalLayout_3.addWidget(self.btnAccept)


        self.gridLayout.addLayout(self.horizontalLayout_3, 15, 0, 1, 2)

        self.cbRegeln = QComboBox(formMain)
        self.cbRegeln.setObjectName(u"cbRegeln")
        self.cbRegeln.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.cbRegeln, 3, 1, 1, 1)

        self.label = QLabel(formMain)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(6)
        self.label.setFont(font)
        self.label.setInputMethodHints(Qt.ImhNone)
        self.label.setTextFormat(Qt.RichText)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label, 17, 0, 1, 2)

        self.cbKultur = QComboBox(formMain)
        self.cbKultur.setObjectName(u"cbKultur")

        self.gridLayout.addWidget(self.cbKultur, 6, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(formMain)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)
        self.label_2.setMargin(0)

        self.verticalLayout_2.addWidget(self.label_2)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 2)

        self.lblGeschlecht = QLabel(formMain)
        self.lblGeschlecht.setObjectName(u"lblGeschlecht")
        font1 = QFont()
        font1.setBold(True)
        self.lblGeschlecht.setFont(font1)

        self.gridLayout.addWidget(self.lblGeschlecht, 4, 0, 1, 1)

        self.lblRegeln = QLabel(formMain)
        self.lblRegeln.setObjectName(u"lblRegeln")
        sizePolicy.setHeightForWidth(self.lblRegeln.sizePolicy().hasHeightForWidth())
        self.lblRegeln.setSizePolicy(sizePolicy)
        self.lblRegeln.setFont(font1)

        self.gridLayout.addWidget(self.lblRegeln, 3, 0, 1, 1)

        self.lblProfession = QLabel(formMain)
        self.lblProfession.setObjectName(u"lblProfession")
        self.lblProfession.setFont(font1)

        self.gridLayout.addWidget(self.lblProfession, 8, 0, 1, 1)

        self.lblProfessionKategorie = QLabel(formMain)
        self.lblProfessionKategorie.setObjectName(u"lblProfessionKategorie")
        self.lblProfessionKategorie.setFont(font1)

        self.gridLayout.addWidget(self.lblProfessionKategorie, 7, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnWeiblich = QRadioButton(formMain)
        self.btnWeiblich.setObjectName(u"btnWeiblich")
        self.btnWeiblich.setChecked(True)

        self.horizontalLayout.addWidget(self.btnWeiblich)

        self.btnMaennlich = QRadioButton(formMain)
        self.btnMaennlich.setObjectName(u"btnMaennlich")

        self.horizontalLayout.addWidget(self.btnMaennlich)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 1)

        self.lblSpezies = QLabel(formMain)
        self.lblSpezies.setObjectName(u"lblSpezies")
        self.lblSpezies.setFont(font1)

        self.gridLayout.addWidget(self.lblSpezies, 5, 0, 1, 1)

        self.cbSpezies = QComboBox(formMain)
        self.cbSpezies.setObjectName(u"cbSpezies")
        self.cbSpezies.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.cbSpezies, 5, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.line = QFrame(formMain)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 16, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 11, 0, 1, 1)

        self.lblKultur = QLabel(formMain)
        self.lblKultur.setObjectName(u"lblKultur")
        self.lblKultur.setFont(font1)

        self.gridLayout.addWidget(self.lblKultur, 6, 0, 1, 1)

        self.cbProfessionKategorie = QComboBox(formMain)
        self.cbProfessionKategorie.setObjectName(u"cbProfessionKategorie")

        self.gridLayout.addWidget(self.cbProfessionKategorie, 7, 1, 1, 1)

        self.cbProfession = QComboBox(formMain)
        self.cbProfession.setObjectName(u"cbProfession")

        self.gridLayout.addWidget(self.cbProfession, 8, 1, 1, 1)

        QWidget.setTabOrder(self.cbRegeln, self.btnWeiblich)
        QWidget.setTabOrder(self.btnWeiblich, self.btnMaennlich)
        QWidget.setTabOrder(self.btnMaennlich, self.cbSpezies)
        QWidget.setTabOrder(self.cbSpezies, self.cbKultur)
        QWidget.setTabOrder(self.cbKultur, self.cbProfessionKategorie)
        QWidget.setTabOrder(self.cbProfessionKategorie, self.cbProfession)
        QWidget.setTabOrder(self.cbProfession, self.btnCancel)
        QWidget.setTabOrder(self.btnCancel, self.btnAccept)

        self.retranslateUi(formMain)

        QMetaObject.connectSlotsByName(formMain)
    # setupUi

    def retranslateUi(self, formMain):
        formMain.setWindowTitle(QCoreApplication.translate("formMain", u"Charakterassistent", None))
        self.btnCancel.setText(QCoreApplication.translate("formMain", u"Ohne Assistent fortfahren", None))
        self.btnAccept.setText(QCoreApplication.translate("formMain", u"\u00dcbernehmen", None))
        self.label.setText(QCoreApplication.translate("formMain", u"<html><head/><body><p>Der Charakterassistent lebt von Communitybeitr\u00e4gen. Eigene Spezies/Kulturen/Professionen/Archetypen lassen sich spielend leicht erstellen. Finde hier heraus wie und teile deine Kreationen: <a href=\"https://dsaforum.de/viewtopic.php?f=180&amp;t=56703\"><span style=\" text-decoration: underline;\">Charakterassistent auf dsaforum.de</span></a></p></body></html>", None))
        self.label.setProperty("class", QCoreApplication.translate("formMain", u"smallText", None))
        self.label_2.setText(QCoreApplication.translate("formMain", u"Dieser Assistent betreut dich bei der Erstellung deines Charakters. Bei den Professionen sind manchmal Namen mitangegeben - dies sind vollwertige Archetypen mit Eigenheiten. Die angegebenen ben\u00f6tigten Erfahrungspunkte k\u00f6nnen niedriger oder h\u00f6her ausfallen.", None))
        self.label_2.setProperty("class", QCoreApplication.translate("formMain", u"panel", None))
        self.lblGeschlecht.setText(QCoreApplication.translate("formMain", u"Geschlecht", None))
        self.lblGeschlecht.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.lblRegeln.setText(QCoreApplication.translate("formMain", u"Baukasten", None))
        self.lblRegeln.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.lblProfession.setText(QCoreApplication.translate("formMain", u"Profession", None))
        self.lblProfession.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.lblProfessionKategorie.setText(QCoreApplication.translate("formMain", u"Professionskategorie", None))
        self.lblProfessionKategorie.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.btnWeiblich.setText(QCoreApplication.translate("formMain", u"Weiblich", None))
        self.btnMaennlich.setText(QCoreApplication.translate("formMain", u"M\u00e4nnlich", None))
        self.lblSpezies.setText(QCoreApplication.translate("formMain", u"Spezies", None))
        self.lblSpezies.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
        self.lblKultur.setText(QCoreApplication.translate("formMain", u"Kultur", None))
        self.lblKultur.setProperty("class", QCoreApplication.translate("formMain", u"h4", None))
    # retranslateUi

