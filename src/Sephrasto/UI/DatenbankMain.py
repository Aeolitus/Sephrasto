# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankMain.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.NonModal)
        Form.resize(853, 663)
        self.actionSpeichern = QAction(Form)
        self.actionSpeichern.setObjectName(u"actionSpeichern")
        self.actionSpeichern_unter = QAction(Form)
        self.actionSpeichern_unter.setObjectName(u"actionSpeichern_unter")
        self.actionZur_cksetzen = QAction(Form)
        self.actionZur_cksetzen.setObjectName(u"actionZur_cksetzen")
        self.actionOeffnen = QAction(Form)
        self.actionOeffnen.setObjectName(u"actionOeffnen")
        self.actionBeenden = QAction(Form)
        self.actionBeenden.setObjectName(u"actionBeenden")
        self.actionDatenbank_Editor = QAction(Form)
        self.actionDatenbank_Editor.setObjectName(u"actionDatenbank_Editor")
        self.actionScript_API = QAction(Form)
        self.actionScript_API.setObjectName(u"actionScript_API")
        self.actionFehlerliste = QAction(Form)
        self.actionFehlerliste.setObjectName(u"actionFehlerliste")
        self.actionSchliessen = QAction(Form)
        self.actionSchliessen.setObjectName(u"actionSchliessen")
        self.actionZusaetzlichOeffnen = QAction(Form)
        self.actionZusaetzlichOeffnen.setObjectName(u"actionZusaetzlichOeffnen")
        self.actionCharakterAssistent = QAction(Form)
        self.actionCharakterAssistent.setObjectName(u"actionCharakterAssistent")
        self.actionDBMergen = QAction(Form)
        self.actionDBMergen.setObjectName(u"actionDBMergen")
        self.actionReload = QAction(Form)
        self.actionReload.setObjectName(u"actionReload")
        self.centralwidget = QWidget(Form)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.West)

        self.gridLayout.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelNumResults = QLabel(self.centralwidget)
        self.labelNumResults.setObjectName(u"labelNumResults")

        self.horizontalLayout.addWidget(self.labelNumResults)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonNeu = QPushButton(self.centralwidget)
        self.buttonNeu.setObjectName(u"buttonNeu")

        self.horizontalLayout.addWidget(self.buttonNeu)

        self.buttonEditieren = QPushButton(self.centralwidget)
        self.buttonEditieren.setObjectName(u"buttonEditieren")

        self.horizontalLayout.addWidget(self.buttonEditieren)

        self.buttonRAW = QPushButton(self.centralwidget)
        self.buttonRAW.setObjectName(u"buttonRAW")

        self.horizontalLayout.addWidget(self.buttonRAW)

        self.buttonDuplizieren = QPushButton(self.centralwidget)
        self.buttonDuplizieren.setObjectName(u"buttonDuplizieren")

        self.horizontalLayout.addWidget(self.buttonDuplizieren)

        self.buttonLoeschen = QPushButton(self.centralwidget)
        self.buttonLoeschen.setObjectName(u"buttonLoeschen")

        self.horizontalLayout.addWidget(self.buttonLoeschen)

        self.buttonWiederherstellen = QPushButton(self.centralwidget)
        self.buttonWiederherstellen.setObjectName(u"buttonWiederherstellen")

        self.horizontalLayout.addWidget(self.buttonWiederherstellen)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.buttonOpen = QPushButton(self.centralwidget)
        self.buttonOpen.setObjectName(u"buttonOpen")

        self.horizontalLayout_3.addWidget(self.buttonOpen)

        self.buttonQuicksave = QPushButton(self.centralwidget)
        self.buttonQuicksave.setObjectName(u"buttonQuicksave")

        self.horizontalLayout_3.addWidget(self.buttonQuicksave)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.nameFilterEdit = QLineEdit(self.centralwidget)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")
        self.nameFilterEdit.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.nameFilterEdit)

        self.labelFilterName = QLabel(self.centralwidget)
        self.labelFilterName.setObjectName(u"labelFilterName")

        self.horizontalLayout_3.addWidget(self.labelFilterName)

        self.checkFullText = QCheckBox(self.centralwidget)
        self.checkFullText.setObjectName(u"checkFullText")

        self.horizontalLayout_3.addWidget(self.checkFullText)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.checkDetails = QCheckBox(self.centralwidget)
        self.checkDetails.setObjectName(u"checkDetails")

        self.horizontalLayout_3.addWidget(self.checkDetails)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)

        Form.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Form)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 853, 26))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuAnalysieren = QMenu(self.menubar)
        self.menuAnalysieren.setObjectName(u"menuAnalysieren")
        self.menuHilfe = QMenu(self.menubar)
        self.menuHilfe.setObjectName(u"menuHilfe")
        self.menuExport = QMenu(self.menubar)
        self.menuExport.setObjectName(u"menuExport")
        Form.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.buttonOpen, self.buttonQuicksave)
        QWidget.setTabOrder(self.buttonQuicksave, self.nameFilterEdit)
        QWidget.setTabOrder(self.nameFilterEdit, self.checkFullText)
        QWidget.setTabOrder(self.checkFullText, self.checkDetails)
        QWidget.setTabOrder(self.checkDetails, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.buttonNeu)
        QWidget.setTabOrder(self.buttonNeu, self.buttonEditieren)
        QWidget.setTabOrder(self.buttonEditieren, self.buttonRAW)
        QWidget.setTabOrder(self.buttonRAW, self.buttonDuplizieren)
        QWidget.setTabOrder(self.buttonDuplizieren, self.buttonLoeschen)
        QWidget.setTabOrder(self.buttonLoeschen, self.buttonWiederherstellen)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuAnalysieren.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuHilfe.menuAction())
        self.menuDatei.addAction(self.actionOeffnen)
        self.menuDatei.addAction(self.actionZusaetzlichOeffnen)
        self.menuDatei.addAction(self.actionSpeichern)
        self.menuDatei.addAction(self.actionSpeichern_unter)
        self.menuDatei.addAction(self.actionSchliessen)
        self.menuDatei.addAction(self.actionReload)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionBeenden)
        self.menuAnalysieren.addAction(self.actionFehlerliste)
        self.menuHilfe.addAction(self.actionDatenbank_Editor)
        self.menuHilfe.addAction(self.actionScript_API)
        self.menuExport.addAction(self.actionDBMergen)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Sephrasto - Datenbank-Editor", None))
        self.actionSpeichern.setText(QCoreApplication.translate("Form", u"Speichern", None))
        self.actionSpeichern_unter.setText(QCoreApplication.translate("Form", u"Speichern unter...", None))
        self.actionZur_cksetzen.setText(QCoreApplication.translate("Form", u"Zur\u00fccksetzen", None))
        self.actionOeffnen.setText(QCoreApplication.translate("Form", u"\u00d6ffnen", None))
        self.actionBeenden.setText(QCoreApplication.translate("Form", u"Beenden", None))
        self.actionDatenbank_Editor.setText(QCoreApplication.translate("Form", u"Datenbank-Editor", None))
        self.actionScript_API.setText(QCoreApplication.translate("Form", u"Script API", None))
        self.actionFehlerliste.setText(QCoreApplication.translate("Form", u"Hausregeln", None))
        self.actionSchliessen.setText(QCoreApplication.translate("Form", u"Datei schlie\u00dfen und Originaldaten laden", None))
        self.actionZusaetzlichOeffnen.setText(QCoreApplication.translate("Form", u"Zus\u00e4tzlich \u00f6ffnen", None))
        self.actionCharakterAssistent.setText(QCoreApplication.translate("Form", u"Charakter Assistent Auswahlm\u00f6glichkeiten", None))
        self.actionDBMergen.setText(QCoreApplication.translate("Form", u"Datenbank mergen und exportieren", None))
        self.actionReload.setText(QCoreApplication.translate("Form", u"Datei neu laden", None))
        self.labelNumResults.setText(QCoreApplication.translate("Form", u"0 Ergebnisse", None))
#if QT_CONFIG(tooltip)
        self.buttonNeu.setToolTip(QCoreApplication.translate("Form", u"Neues Element hinzuf\u00fcgen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonNeu.setText(QCoreApplication.translate("Form", u"Neu", None))
        self.buttonNeu.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonEditieren.setToolTip(QCoreApplication.translate("Form", u"Element bearbeiten", None))
#endif // QT_CONFIG(tooltip)
        self.buttonEditieren.setText(QCoreApplication.translate("Form", u"Editieren", None))
        self.buttonEditieren.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonRAW.setToolTip(QCoreApplication.translate("Form", u"\u00c4nderungen mit dem Original-Element vergleichen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonRAW.setText(QCoreApplication.translate("Form", u"RAW ansehen", None))
        self.buttonRAW.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonDuplizieren.setToolTip(QCoreApplication.translate("Form", u"Element Duplizieren", None))
#endif // QT_CONFIG(tooltip)
        self.buttonDuplizieren.setText(QCoreApplication.translate("Form", u"Duplizieren", None))
        self.buttonDuplizieren.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonLoeschen.setToolTip(QCoreApplication.translate("Form", u"Element L\u00f6schen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonLoeschen.setText(QCoreApplication.translate("Form", u"L\u00f6schen", None))
        self.buttonLoeschen.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonWiederherstellen.setToolTip(QCoreApplication.translate("Form", u"Element Wiederherstellen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonWiederherstellen.setText(QCoreApplication.translate("Form", u"Wiederherstellen", None))
        self.buttonWiederherstellen.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonOpen.setToolTip(QCoreApplication.translate("Form", u"\u00d6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonOpen.setText(QCoreApplication.translate("Form", u"\u00d6ffnen", None))
        self.buttonOpen.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonQuicksave.setToolTip(QCoreApplication.translate("Form", u"Speichern", None))
#endif // QT_CONFIG(tooltip)
        self.buttonQuicksave.setText(QCoreApplication.translate("Form", u"Speichern", None))
        self.buttonQuicksave.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
        self.nameFilterEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Suchen...", None))
#if QT_CONFIG(tooltip)
        self.labelFilterName.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Die Suche unterst\u00fctzt Wildcards. Dies sind Platzhalter, die verwendet werden k\u00f6nnen, um \u00dcbereinstimmungen mit einer Vielzahl von Suchergebnissen zu erm\u00f6glichen. Es gibt die folgenden Wildcards:</p><table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\"><thead><tr><td><p><span style=\" font-weight:600;\">Platzhalter</span></p></td><td><p><span style=\" font-weight:600;\">Wirkung</span></p></td></tr></thead><tr><td><p>*</p></td><td><p>Steht f\u00fcr null oder mehr beliebige Zeichen.</p></td></tr><tr><td><p>?</p></td><td><p>Steht f\u00fcr ein beliebiges einzelnes Zeichen.</p></td></tr><tr><td><p>[seq]</p></td><td><p>Steht f\u00fcr ein Zeichen in der angegebenen Sequenz 'seq'.</p></td></tr><tr><td><p>[!seq]</p></td><td><p>Steht f\u00fcr ein Zeichen, das nicht in der angegebenen Sequenz 'seq' enthalten ist.</p></td></tr></table></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelFilterName.setText(QCoreApplication.translate("Form", u"Suchen", None))
        self.labelFilterName.setProperty("class", QCoreApplication.translate("Form", u"icon", None))
        self.checkFullText.setText(QCoreApplication.translate("Form", u"Volltext", None))
        self.checkDetails.setText(QCoreApplication.translate("Form", u"Erweiterte Details", None))
        self.menuDatei.setTitle(QCoreApplication.translate("Form", u"Datei", None))
        self.menuAnalysieren.setTitle(QCoreApplication.translate("Form", u"Analysieren", None))
        self.menuHilfe.setTitle(QCoreApplication.translate("Form", u"Hilfe", None))
        self.menuExport.setTitle(QCoreApplication.translate("Form", u"Export", None))
    # retranslateUi

