# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterBeschreibungDetails.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QWidget)

class Ui_formBeschreibung(object):
    def setupUi(self, formBeschreibung):
        if not formBeschreibung.objectName():
            formBeschreibung.setObjectName(u"formBeschreibung")
        formBeschreibung.resize(872, 535)
        self.gridLayout_3 = QGridLayout(formBeschreibung)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(20, 20, 20, 20)
        self.tabWidget = QTabWidget(formBeschreibung)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout = QGridLayout(self.tab_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(20)
        self.leAugenfarbe = QLineEdit(self.tab_2)
        self.leAugenfarbe.setObjectName(u"leAugenfarbe")

        self.gridLayout_2.addWidget(self.leAugenfarbe, 8, 2, 1, 1)

        self.label_10 = QLabel(self.tab_2)
        self.label_10.setObjectName(u"label_10")
        font = QFont()
        font.setBold(True)
        self.label_10.setFont(font)

        self.gridLayout_2.addWidget(self.label_10, 5, 4, 1, 2)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(68, 0))
        self.label_2.setFont(font)

        self.gridLayout_2.addWidget(self.label_2, 4, 4, 1, 1)

        self.leHintergrund6 = QLineEdit(self.tab_2)
        self.leHintergrund6.setObjectName(u"leHintergrund6")

        self.gridLayout_2.addWidget(self.leHintergrund6, 12, 4, 1, 2)

        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout_2.addWidget(self.label_7, 7, 1, 1, 1)

        self.leAussehen1 = QLineEdit(self.tab_2)
        self.leAussehen1.setObjectName(u"leAussehen1")

        self.gridLayout_2.addWidget(self.leAussehen1, 9, 2, 1, 1)

        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout_2.addWidget(self.label_5, 5, 1, 1, 1)

        self.leHintergrund5 = QLineEdit(self.tab_2)
        self.leHintergrund5.setObjectName(u"leHintergrund5")

        self.gridLayout_2.addWidget(self.leHintergrund5, 11, 4, 1, 2)

        self.leHintergrund1 = QLineEdit(self.tab_2)
        self.leHintergrund1.setObjectName(u"leHintergrund1")

        self.gridLayout_2.addWidget(self.leHintergrund1, 7, 4, 1, 2)

        self.label_9 = QLabel(self.tab_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout_2.addWidget(self.label_9, 9, 1, 1, 1)

        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout_2.addWidget(self.label_6, 6, 1, 1, 1)

        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout_2.addWidget(self.label_3, 3, 1, 1, 1)

        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 2, 1, 1, 1)

        self.leHintergrund3 = QLineEdit(self.tab_2)
        self.leHintergrund3.setObjectName(u"leHintergrund3")

        self.gridLayout_2.addWidget(self.leHintergrund3, 9, 4, 1, 2)

        self.leAussehen3 = QLineEdit(self.tab_2)
        self.leAussehen3.setObjectName(u"leAussehen3")

        self.gridLayout_2.addWidget(self.leAussehen3, 11, 1, 1, 2)

        self.leAussehen4 = QLineEdit(self.tab_2)
        self.leAussehen4.setObjectName(u"leAussehen4")

        self.gridLayout_2.addWidget(self.leAussehen4, 12, 1, 1, 2)

        self.label_11 = QLabel(self.tab_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout_2.addWidget(self.label_11, 1, 1, 1, 1)

        self.leGroesse = QLineEdit(self.tab_2)
        self.leGroesse.setObjectName(u"leGroesse")

        self.gridLayout_2.addWidget(self.leGroesse, 5, 2, 1, 1)

        self.leAussehen2 = QLineEdit(self.tab_2)
        self.leAussehen2.setObjectName(u"leAussehen2")

        self.gridLayout_2.addWidget(self.leAussehen2, 10, 1, 1, 2)

        self.chkKultur = QCheckBox(self.tab_2)
        self.chkKultur.setObjectName(u"chkKultur")
        self.chkKultur.setChecked(True)

        self.gridLayout_2.addWidget(self.chkKultur, 1, 5, 1, 1)

        self.leHintergrund7 = QLineEdit(self.tab_2)
        self.leHintergrund7.setObjectName(u"leHintergrund7")

        self.gridLayout_2.addWidget(self.leHintergrund7, 13, 4, 1, 2)

        self.leGeschlecht = QLineEdit(self.tab_2)
        self.leGeschlecht.setObjectName(u"leGeschlecht")

        self.gridLayout_2.addWidget(self.leGeschlecht, 3, 2, 1, 1)

        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.gridLayout_2.addWidget(self.label_4, 4, 1, 1, 1)

        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout_2.addWidget(self.label_8, 8, 1, 1, 1)

        self.leKultur = QLineEdit(self.tab_2)
        self.leKultur.setObjectName(u"leKultur")
        self.leKultur.setEnabled(False)

        self.gridLayout_2.addWidget(self.leKultur, 1, 2, 1, 3)

        self.leGeburtsdatum = QLineEdit(self.tab_2)
        self.leGeburtsdatum.setObjectName(u"leGeburtsdatum")

        self.gridLayout_2.addWidget(self.leGeburtsdatum, 4, 2, 1, 1)

        self.labelImage = QLabel(self.tab_2)
        self.labelImage.setObjectName(u"labelImage")
        self.labelImage.setMinimumSize(QSize(208, 272))
        self.labelImage.setMaximumSize(QSize(208, 272))
        self.labelImage.setAlignment(Qt.AlignCenter)
        self.labelImage.setWordWrap(True)

        self.gridLayout_2.addWidget(self.labelImage, 3, 3, 11, 1)

        self.leHaarfarbe = QLineEdit(self.tab_2)
        self.leHaarfarbe.setObjectName(u"leHaarfarbe")

        self.gridLayout_2.addWidget(self.leHaarfarbe, 7, 2, 1, 1)

        self.leHintergrund8 = QLineEdit(self.tab_2)
        self.leHintergrund8.setObjectName(u"leHintergrund8")

        self.gridLayout_2.addWidget(self.leHintergrund8, 14, 4, 1, 2)

        self.leHintergrund2 = QLineEdit(self.tab_2)
        self.leHintergrund2.setObjectName(u"leHintergrund2")

        self.gridLayout_2.addWidget(self.leHintergrund2, 8, 4, 1, 2)

        self.leProfession = QLineEdit(self.tab_2)
        self.leProfession.setObjectName(u"leProfession")

        self.gridLayout_2.addWidget(self.leProfession, 2, 2, 1, 4)

        self.leHintergrund4 = QLineEdit(self.tab_2)
        self.leHintergrund4.setObjectName(u"leHintergrund4")

        self.gridLayout_2.addWidget(self.leHintergrund4, 10, 4, 1, 2)

        self.leTitel = QLineEdit(self.tab_2)
        self.leTitel.setObjectName(u"leTitel")
        self.leTitel.setMinimumSize(QSize(0, 0))

        self.gridLayout_2.addWidget(self.leTitel, 4, 5, 1, 1)

        self.leAussehen6 = QLineEdit(self.tab_2)
        self.leAussehen6.setObjectName(u"leAussehen6")

        self.gridLayout_2.addWidget(self.leAussehen6, 14, 1, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonLoadImage = QPushButton(self.tab_2)
        self.buttonLoadImage.setObjectName(u"buttonLoadImage")

        self.horizontalLayout.addWidget(self.buttonLoadImage)

        self.buttonDeleteImage = QPushButton(self.tab_2)
        self.buttonDeleteImage.setObjectName(u"buttonDeleteImage")

        self.horizontalLayout.addWidget(self.buttonDeleteImage)


        self.gridLayout_2.addLayout(self.horizontalLayout, 14, 3, 1, 1)

        self.leGewicht = QLineEdit(self.tab_2)
        self.leGewicht.setObjectName(u"leGewicht")

        self.gridLayout_2.addWidget(self.leGewicht, 6, 2, 1, 1)

        self.leAussehen5 = QLineEdit(self.tab_2)
        self.leAussehen5.setObjectName(u"leAussehen5")

        self.gridLayout_2.addWidget(self.leAussehen5, 13, 1, 1, 2)

        self.leHintergrund0 = QLineEdit(self.tab_2)
        self.leHintergrund0.setObjectName(u"leHintergrund0")

        self.gridLayout_2.addWidget(self.leHintergrund0, 6, 4, 1, 2)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 2, 1)

        QWidget.setTabOrder(self.leKultur, self.chkKultur)
        QWidget.setTabOrder(self.chkKultur, self.leProfession)
        QWidget.setTabOrder(self.leProfession, self.leGeschlecht)
        QWidget.setTabOrder(self.leGeschlecht, self.leGeburtsdatum)
        QWidget.setTabOrder(self.leGeburtsdatum, self.leGroesse)
        QWidget.setTabOrder(self.leGroesse, self.leGewicht)
        QWidget.setTabOrder(self.leGewicht, self.leHaarfarbe)
        QWidget.setTabOrder(self.leHaarfarbe, self.leAugenfarbe)
        QWidget.setTabOrder(self.leAugenfarbe, self.leAussehen1)
        QWidget.setTabOrder(self.leAussehen1, self.leAussehen2)
        QWidget.setTabOrder(self.leAussehen2, self.leAussehen3)
        QWidget.setTabOrder(self.leAussehen3, self.leAussehen4)
        QWidget.setTabOrder(self.leAussehen4, self.leAussehen5)
        QWidget.setTabOrder(self.leAussehen5, self.leAussehen6)
        QWidget.setTabOrder(self.leAussehen6, self.leTitel)
        QWidget.setTabOrder(self.leTitel, self.leHintergrund0)
        QWidget.setTabOrder(self.leHintergrund0, self.leHintergrund1)
        QWidget.setTabOrder(self.leHintergrund1, self.leHintergrund2)
        QWidget.setTabOrder(self.leHintergrund2, self.leHintergrund3)
        QWidget.setTabOrder(self.leHintergrund3, self.leHintergrund4)
        QWidget.setTabOrder(self.leHintergrund4, self.leHintergrund5)
        QWidget.setTabOrder(self.leHintergrund5, self.leHintergrund6)
        QWidget.setTabOrder(self.leHintergrund6, self.leHintergrund7)
        QWidget.setTabOrder(self.leHintergrund7, self.leHintergrund8)
        QWidget.setTabOrder(self.leHintergrund8, self.buttonLoadImage)
        QWidget.setTabOrder(self.buttonLoadImage, self.buttonDeleteImage)
        QWidget.setTabOrder(self.buttonDeleteImage, self.tabWidget)

        self.retranslateUi(formBeschreibung)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(formBeschreibung)
    # setupUi

    def retranslateUi(self, formBeschreibung):
        formBeschreibung.setWindowTitle(QCoreApplication.translate("formBeschreibung", u"Beschreibung", None))
        self.tabWidget.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h2", None))
        self.label_10.setText(QCoreApplication.translate("formBeschreibung", u"Familie/Hintergrund/Herkunft", None))
        self.label_10.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_2.setText(QCoreApplication.translate("formBeschreibung", u"Titel", None))
        self.label_2.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_7.setText(QCoreApplication.translate("formBeschreibung", u"Haarfarbe", None))
        self.label_7.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_5.setText(QCoreApplication.translate("formBeschreibung", u"Gr\u00f6\u00dfe", None))
        self.label_5.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_9.setText(QCoreApplication.translate("formBeschreibung", u"Aussehen", None))
        self.label_9.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_6.setText(QCoreApplication.translate("formBeschreibung", u"Gewicht", None))
        self.label_6.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_3.setText(QCoreApplication.translate("formBeschreibung", u"Geschlecht", None))
        self.label_3.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label.setText(QCoreApplication.translate("formBeschreibung", u"Profession", None))
        self.label.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_11.setText(QCoreApplication.translate("formBeschreibung", u"Kultur", None))
        self.label_11.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.chkKultur.setText(QCoreApplication.translate("formBeschreibung", u"Automatisch bef\u00fcllen", None))
        self.label_4.setText(QCoreApplication.translate("formBeschreibung", u"Geburtsdatum", None))
        self.label_4.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.label_8.setText(QCoreApplication.translate("formBeschreibung", u"Augenfarbe", None))
        self.label_8.setProperty("class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.labelImage.setText(QCoreApplication.translate("formBeschreibung", u"Bild-Aufl\u00f6sung: 260x340 px\n"
"(wird automatisch angepasst)", None))
        self.buttonLoadImage.setText(QCoreApplication.translate("formBeschreibung", u"Bild laden", None))
        self.buttonDeleteImage.setText(QCoreApplication.translate("formBeschreibung", u"Bild L\u00f6schen", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("formBeschreibung", u"Details", None))
    # retranslateUi

