# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Wizard.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_formMain(object):
    def setupUi(self, formMain):
        if not formMain.objectName():
            formMain.setObjectName(u"formMain")
        formMain.setWindowModality(Qt.ApplicationModal)
        formMain.resize(623, 376)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(formMain.sizePolicy().hasHeightForWidth())
        formMain.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(formMain)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalSpacer_2 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.label_3 = QLabel(formMain)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.lblKultur = QLabel(formMain)
        self.lblKultur.setObjectName(u"lblKultur")
        self.lblKultur.setFont(font)

        self.gridLayout.addWidget(self.lblKultur, 7, 0, 1, 1)

        self.cbProfession = QComboBox(formMain)
        self.cbProfession.setObjectName(u"cbProfession")

        self.gridLayout.addWidget(self.cbProfession, 9, 1, 1, 1)

        self.label_4 = QLabel(formMain)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.lblProfession = QLabel(formMain)
        self.lblProfession.setObjectName(u"lblProfession")
        self.lblProfession.setFont(font)

        self.gridLayout.addWidget(self.lblProfession, 9, 0, 1, 1)

        self.lblProfessionKategorie = QLabel(formMain)
        self.lblProfessionKategorie.setObjectName(u"lblProfessionKategorie")
        self.lblProfessionKategorie.setFont(font)

        self.gridLayout.addWidget(self.lblProfessionKategorie, 8, 0, 1, 1)

        self.lblSpezies = QLabel(formMain)
        self.lblSpezies.setObjectName(u"lblSpezies")
        self.lblSpezies.setFont(font)

        self.gridLayout.addWidget(self.lblSpezies, 6, 0, 1, 1)

        self.cbRegeln = QComboBox(formMain)
        self.cbRegeln.setObjectName(u"cbRegeln")

        self.gridLayout.addWidget(self.cbRegeln, 3, 1, 1, 1)

        self.line = QFrame(formMain)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 17, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btnAccept = QPushButton(formMain)
        self.btnAccept.setObjectName(u"btnAccept")
        self.btnAccept.setEnabled(True)
        self.btnAccept.setMinimumSize(QSize(100, 0))
        self.btnAccept.setMaximumSize(QSize(16777214, 16777215))

        self.horizontalLayout_3.addWidget(self.btnAccept)


        self.gridLayout.addLayout(self.horizontalLayout_3, 16, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 12, 0, 1, 1)

        self.lblRegeln = QLabel(formMain)
        self.lblRegeln.setObjectName(u"lblRegeln")
        sizePolicy.setHeightForWidth(self.lblRegeln.sizePolicy().hasHeightForWidth())
        self.lblRegeln.setSizePolicy(sizePolicy)
        self.lblRegeln.setFont(font)

        self.gridLayout.addWidget(self.lblRegeln, 4, 0, 1, 1)

        self.label = QLabel(formMain)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(6)
        self.label.setFont(font1)
        self.label.setInputMethodHints(Qt.ImhNone)
        self.label.setTextFormat(Qt.RichText)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label, 18, 0, 1, 2)

        self.cbProfessionKategorie = QComboBox(formMain)
        self.cbProfessionKategorie.setObjectName(u"cbProfessionKategorie")

        self.gridLayout.addWidget(self.cbProfessionKategorie, 8, 1, 1, 1)

        self.lblGeschlecht = QLabel(formMain)
        self.lblGeschlecht.setObjectName(u"lblGeschlecht")
        self.lblGeschlecht.setFont(font)

        self.gridLayout.addWidget(self.lblGeschlecht, 5, 0, 1, 1)

        self.cbSpezies = QComboBox(formMain)
        self.cbSpezies.setObjectName(u"cbSpezies")
        self.cbSpezies.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.cbSpezies, 6, 1, 1, 1)

        self.cbBaukasten = QComboBox(formMain)
        self.cbBaukasten.setObjectName(u"cbBaukasten")
        self.cbBaukasten.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.cbBaukasten, 4, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnSkip = QRadioButton(formMain)
        self.btnSkip.setObjectName(u"btnSkip")
        self.btnSkip.setChecked(True)

        self.horizontalLayout.addWidget(self.btnSkip)

        self.btnMaennlich = QRadioButton(formMain)
        self.btnMaennlich.setObjectName(u"btnMaennlich")

        self.horizontalLayout.addWidget(self.btnMaennlich)

        self.btnWeiblich = QRadioButton(formMain)
        self.btnWeiblich.setObjectName(u"btnWeiblich")
        self.btnWeiblich.setChecked(False)

        self.horizontalLayout.addWidget(self.btnWeiblich)

        self.btnDivers = QRadioButton(formMain)
        self.btnDivers.setObjectName(u"btnDivers")

        self.horizontalLayout.addWidget(self.btnDivers)

        self.leDivers = QLineEdit(formMain)
        self.leDivers.setObjectName(u"leDivers")

        self.horizontalLayout.addWidget(self.leDivers)


        self.gridLayout.addLayout(self.horizontalLayout, 5, 1, 1, 1)

        self.cbKultur = QComboBox(formMain)
        self.cbKultur.setObjectName(u"cbKultur")

        self.gridLayout.addWidget(self.cbKultur, 7, 1, 1, 1)

        QWidget.setTabOrder(self.cbRegeln, self.cbBaukasten)
        QWidget.setTabOrder(self.cbBaukasten, self.btnMaennlich)
        QWidget.setTabOrder(self.btnMaennlich, self.btnDivers)
        QWidget.setTabOrder(self.btnDivers, self.leDivers)
        QWidget.setTabOrder(self.leDivers, self.cbSpezies)
        QWidget.setTabOrder(self.cbSpezies, self.cbKultur)
        QWidget.setTabOrder(self.cbKultur, self.cbProfessionKategorie)
        QWidget.setTabOrder(self.cbProfessionKategorie, self.cbProfession)
        QWidget.setTabOrder(self.cbProfession, self.btnAccept)

        self.retranslateUi(formMain)

        self.btnAccept.setDefault(True)


        QMetaObject.connectSlotsByName(formMain)
    # setupUi

    def retranslateUi(self, formMain):
        formMain.setWindowTitle(QCoreApplication.translate("formMain", u"Charakterassistent", None))
        self.label_3.setText(QCoreApplication.translate("formMain", u"Hausregeln", None))
        self.label_3.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.lblKultur.setText(QCoreApplication.translate("formMain", u"Kultur", None))
        self.lblKultur.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
#if QT_CONFIG(tooltip)
        self.cbProfession.setToolTip(QCoreApplication.translate("formMain", u"<html><head/><body><p>Hier sind manchmal Namen mitangegeben - dies sind vollwertige Archetypen mit Eigenheiten.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("formMain", u"Neuer Charakter", None))
        self.label_4.setProperty(u"class", QCoreApplication.translate("formMain", u"h2", None))
        self.lblProfession.setText(QCoreApplication.translate("formMain", u"Profession", None))
        self.lblProfession.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.lblProfessionKategorie.setText(QCoreApplication.translate("formMain", u"Professionskategorie", None))
        self.lblProfessionKategorie.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.lblSpezies.setText(QCoreApplication.translate("formMain", u"Spezies", None))
        self.lblSpezies.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.btnAccept.setText(QCoreApplication.translate("formMain", u"\u00dcbernehmen", None))
        self.lblRegeln.setText(QCoreApplication.translate("formMain", u"Baukasten", None))
        self.lblRegeln.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.label.setText(QCoreApplication.translate("formMain", u"<html><head/><body><p>Der Charakterassistent lebt von Communitybeitr\u00e4gen. Wie du eigene Spezies/Kulturen/Professionen/Archetypen erstellen kannst, erf\u00e4hrst du in der Sephrasto-Hilfe.</p></body></html>", None))
        self.label.setProperty(u"class", QCoreApplication.translate("formMain", u"smallText", None))
        self.lblGeschlecht.setText(QCoreApplication.translate("formMain", u"Geschlecht", None))
        self.lblGeschlecht.setProperty(u"class", QCoreApplication.translate("formMain", u"h4", None))
        self.btnSkip.setText(QCoreApplication.translate("formMain", u"\u00dcberspringen", None))
        self.btnMaennlich.setText(QCoreApplication.translate("formMain", u"M\u00e4nnlich", None))
        self.btnWeiblich.setText(QCoreApplication.translate("formMain", u"Weiblich", None))
        self.btnDivers.setText("")
    # retranslateUi

