# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterBeschreibung.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_formBeschreibung(object):
    def setupUi(self, formBeschreibung):
        if not formBeschreibung.objectName():
            formBeschreibung.setObjectName(u"formBeschreibung")
        formBeschreibung.resize(872, 460)
        self.gridLayout_3 = QGridLayout(formBeschreibung)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.editName = QLineEdit(formBeschreibung)
        self.editName.setObjectName(u"editName")

        self.gridLayout.addWidget(self.editName, 1, 2, 1, 1)

        self.labelStatus = QLabel(formBeschreibung)
        self.labelStatus.setObjectName(u"labelStatus")
        font = QFont()
        font.setBold(True)
        self.labelStatus.setFont(font)

        self.gridLayout.addWidget(self.labelStatus, 3, 1, 1, 1)

        self.editKurzbeschreibung = QLineEdit(formBeschreibung)
        self.editKurzbeschreibung.setObjectName(u"editKurzbeschreibung")

        self.gridLayout.addWidget(self.editKurzbeschreibung, 6, 2, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_7, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(150, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 5, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 8, 1, 1, 1)

        self.labelFinanzen = QLabel(formBeschreibung)
        self.labelFinanzen.setObjectName(u"labelFinanzen")
        self.labelFinanzen.setFont(font)

        self.gridLayout.addWidget(self.labelFinanzen, 4, 1, 1, 1)

        self.comboStatus = QComboBox(formBeschreibung)
        self.comboStatus.setObjectName(u"comboStatus")
        self.comboStatus.setMaxVisibleItems(5)
        self.comboStatus.setMinimumContentsLength(0)

        self.gridLayout.addWidget(self.comboStatus, 3, 2, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.editEig2 = QLineEdit(formBeschreibung)
        self.editEig2.setObjectName(u"editEig2")
        self.editEig2.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig2, 0, 1, 1, 1)

        self.editEig3 = QLineEdit(formBeschreibung)
        self.editEig3.setObjectName(u"editEig3")
        self.editEig3.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig3, 1, 0, 1, 1)

        self.editEig8 = QLineEdit(formBeschreibung)
        self.editEig8.setObjectName(u"editEig8")
        self.editEig8.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig8, 3, 1, 1, 1)

        self.editEig6 = QLineEdit(formBeschreibung)
        self.editEig6.setObjectName(u"editEig6")
        self.editEig6.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig6, 2, 1, 1, 1)

        self.editEig7 = QLineEdit(formBeschreibung)
        self.editEig7.setObjectName(u"editEig7")
        self.editEig7.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig7, 3, 0, 1, 1)

        self.editEig1 = QLineEdit(formBeschreibung)
        self.editEig1.setObjectName(u"editEig1")
        self.editEig1.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig1, 0, 0, 1, 1)

        self.editEig5 = QLineEdit(formBeschreibung)
        self.editEig5.setObjectName(u"editEig5")
        self.editEig5.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig5, 2, 0, 1, 1)

        self.editEig4 = QLineEdit(formBeschreibung)
        self.editEig4.setObjectName(u"editEig4")
        self.editEig4.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.editEig4, 1, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 7, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(150, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.labelKurzbeschreibung = QLabel(formBeschreibung)
        self.labelKurzbeschreibung.setObjectName(u"labelKurzbeschreibung")
        self.labelKurzbeschreibung.setMinimumSize(QSize(120, 0))
        self.labelKurzbeschreibung.setFont(font)

        self.gridLayout.addWidget(self.labelKurzbeschreibung, 6, 1, 1, 1)

        self.labelEigenheiten = QLabel(formBeschreibung)
        self.labelEigenheiten.setObjectName(u"labelEigenheiten")
        self.labelEigenheiten.setFont(font)
        self.labelEigenheiten.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.gridLayout.addWidget(self.labelEigenheiten, 7, 1, 1, 1)

        self.labelName = QLabel(formBeschreibung)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setFont(font)

        self.gridLayout.addWidget(self.labelName, 1, 1, 1, 1)

        self.labelSpezies = QLabel(formBeschreibung)
        self.labelSpezies.setObjectName(u"labelSpezies")
        self.labelSpezies.setFont(font)

        self.gridLayout.addWidget(self.labelSpezies, 2, 1, 1, 1)

        self.comboFinanzen = QComboBox(formBeschreibung)
        self.comboFinanzen.setObjectName(u"comboFinanzen")
        self.comboFinanzen.setMaxVisibleItems(5)

        self.gridLayout.addWidget(self.comboFinanzen, 4, 2, 1, 1)

        self.comboHeimat = QComboBox(formBeschreibung)
        self.comboHeimat.setObjectName(u"comboHeimat")

        self.gridLayout.addWidget(self.comboHeimat, 5, 2, 1, 1)

        self.labelHeimat = QLabel(formBeschreibung)
        self.labelHeimat.setObjectName(u"labelHeimat")
        self.labelHeimat.setFont(font)

        self.gridLayout.addWidget(self.labelHeimat, 5, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalSpacer_4 = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.horizontalSpacer_4)

        self.labelImage = QLabel(formBeschreibung)
        self.labelImage.setObjectName(u"labelImage")
        self.labelImage.setMinimumSize(QSize(208, 272))
        self.labelImage.setMaximumSize(QSize(208, 272))
        self.labelImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelImage.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelImage)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonLoadImage = QPushButton(formBeschreibung)
        self.buttonLoadImage.setObjectName(u"buttonLoadImage")

        self.horizontalLayout.addWidget(self.buttonLoadImage)

        self.buttonDeleteImage = QPushButton(formBeschreibung)
        self.buttonDeleteImage.setObjectName(u"buttonDeleteImage")

        self.horizontalLayout.addWidget(self.buttonDeleteImage)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalSpacer_5 = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.horizontalSpacer_5)


        self.gridLayout.addLayout(self.verticalLayout, 0, 4, 9, 1)

        self.comboSpezies = QComboBox(formBeschreibung)
        self.comboSpezies.setObjectName(u"comboSpezies")

        self.gridLayout.addWidget(self.comboSpezies, 2, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.comboStatus, self.comboFinanzen)
        QWidget.setTabOrder(self.comboFinanzen, self.comboHeimat)
        QWidget.setTabOrder(self.comboHeimat, self.editKurzbeschreibung)
        QWidget.setTabOrder(self.editKurzbeschreibung, self.editEig1)
        QWidget.setTabOrder(self.editEig1, self.editEig3)
        QWidget.setTabOrder(self.editEig3, self.editEig5)
        QWidget.setTabOrder(self.editEig5, self.editEig7)
        QWidget.setTabOrder(self.editEig7, self.editEig2)
        QWidget.setTabOrder(self.editEig2, self.editEig4)
        QWidget.setTabOrder(self.editEig4, self.editEig6)
        QWidget.setTabOrder(self.editEig6, self.editEig8)

        self.retranslateUi(formBeschreibung)

        self.comboStatus.setCurrentIndex(-1)
        self.comboFinanzen.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(formBeschreibung)
    # setupUi

    def retranslateUi(self, formBeschreibung):
        formBeschreibung.setWindowTitle(QCoreApplication.translate("formBeschreibung", u"Beschreibung", None))
        self.labelStatus.setText(QCoreApplication.translate("formBeschreibung", u"Status", None))
        self.labelStatus.setProperty(u"class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.labelFinanzen.setText(QCoreApplication.translate("formBeschreibung", u"Finanzen", None))
        self.labelFinanzen.setProperty(u"class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.labelKurzbeschreibung.setText(QCoreApplication.translate("formBeschreibung", u"Kurzbeschreibung", None))
        self.labelKurzbeschreibung.setProperty(u"class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.labelEigenheiten.setText(QCoreApplication.translate("formBeschreibung", u"Eigenheiten", None))
        self.labelEigenheiten.setProperty(u"class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.labelName.setText(QCoreApplication.translate("formBeschreibung", u"Name", None))
        self.labelName.setProperty(u"class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.labelSpezies.setText(QCoreApplication.translate("formBeschreibung", u"Spezies", None))
        self.labelSpezies.setProperty(u"class", QCoreApplication.translate("formBeschreibung", u"h4", None))
        self.labelHeimat.setText(QCoreApplication.translate("formBeschreibung", u"Heimatgebiet", None))
        self.labelHeimat.setProperty(u"class", QCoreApplication.translate("formBeschreibung", u"h4", None))
#if QT_CONFIG(tooltip)
        self.labelImage.setToolTip(QCoreApplication.translate("formBeschreibung", u"<html><head/><body><p>Das Bild wird im Sephrasto-Hauptfenster f\u00fcr die Schnellade-Funktion verwendet und im Charakterbogen ausgegeben. Hinweis: Der Standard Charakterbogen hat keinen Platz f\u00fcr ein Bild. Wechsle im Info-Tab auf den \"Standardbogen mit Bild statt SchiP\" oder einen der anderen B\u00f6gen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelImage.setText(QCoreApplication.translate("formBeschreibung", u"Bild-Aufl\u00f6sung: 260x340 px\n"
"(wird automatisch angepasst)", None))
        self.buttonLoadImage.setText(QCoreApplication.translate("formBeschreibung", u"Bild laden", None))
        self.buttonDeleteImage.setText(QCoreApplication.translate("formBeschreibung", u"Bild l\u00f6schen", None))
    # retranslateUi

