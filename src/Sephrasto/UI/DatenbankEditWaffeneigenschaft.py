# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditWaffeneigenschaft.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpinBox, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(440, 436)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 420, 387))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.teBeschreibung = QPlainTextEdit(self.tab)
        self.teBeschreibung.setObjectName(u"teBeschreibung")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teBeschreibung.sizePolicy().hasHeightForWidth())
        self.teBeschreibung.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.teBeschreibung)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tbBeschreibung = QTextBrowser(self.tab_2)
        self.tbBeschreibung.setObjectName(u"tbBeschreibung")

        self.verticalLayout_2.addWidget(self.tbBeschreibung)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 3, 2, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_3, 4, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.teScript = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teScript.setObjectName(u"teScript")

        self.horizontalLayout.addWidget(self.teScript)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.spinScriptPrio = QSpinBox(self.scrollAreaWidgetContents)
        self.spinScriptPrio.setObjectName(u"spinScriptPrio")
        self.spinScriptPrio.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinScriptPrio.setMinimum(-999)
        self.spinScriptPrio.setMaximum(999)
        self.spinScriptPrio.setSingleStep(1)
        self.spinScriptPrio.setValue(0)

        self.verticalLayout_3.addWidget(self.spinScriptPrio)

        self.buttonPickScript = QPushButton(self.scrollAreaWidgetContents)
        self.buttonPickScript.setObjectName(u"buttonPickScript")

        self.verticalLayout_3.addWidget(self.buttonPickScript)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 2, 2, 1, 1)

        self.warning = QLabel(self.scrollAreaWidgetContents)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(True)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 1, 1, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Waffeneigenschaft bearbeiten...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Script / Priorit\u00e4t", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
#if QT_CONFIG(tooltip)
        self.spinScriptPrio.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Die Skript-Priorit\u00e4t legt die Reihenfolge der Auswertung fest. 0 ist Standard, negative Werte werden davor, positive Werte danach ausgewertet. Dies ist relevant, falls bspw. die INI verdoppelt werden soll nachdem Kampfreflexe eingerechnet wurde. In diesem Fall sollte die Skript-Priorit\u00e4t h\u00f6her als die von Kampfreflexe sein.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonPickScript.setToolTip(QCoreApplication.translate("dialog", u"Scripteditor \u00f6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonPickScript.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonPickScript.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.warning.setText("")
    # retranslateUi

