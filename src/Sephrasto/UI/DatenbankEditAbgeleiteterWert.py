# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditAbgeleiteterWert.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(475, 603)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 455, 554))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 7, 1, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_3, 8, 1, 1, 1)

        self.leAnzeigeName = QLineEdit(self.scrollAreaWidgetContents)
        self.leAnzeigeName.setObjectName(u"leAnzeigeName")

        self.gridLayout.addWidget(self.leAnzeigeName, 3, 2, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 2, 2, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 9, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)

        self.leFormel = QLineEdit(self.scrollAreaWidgetContents)
        self.leFormel.setObjectName(u"leFormel")

        self.gridLayout.addWidget(self.leFormel, 7, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.teScript = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teScript.setObjectName(u"teScript")

        self.horizontalLayout_3.addWidget(self.teScript)

        self.buttonPickScript = QPushButton(self.scrollAreaWidgetContents)
        self.buttonPickScript.setObjectName(u"buttonPickScript")

        self.horizontalLayout_3.addWidget(self.buttonPickScript)


        self.gridLayout.addLayout(self.horizontalLayout_3, 8, 2, 1, 1)

        self.checkShow = QCheckBox(self.scrollAreaWidgetContents)
        self.checkShow.setObjectName(u"checkShow")

        self.gridLayout.addWidget(self.checkShow, 4, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinSortOrder = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSortOrder.setObjectName(u"spinSortOrder")
        self.spinSortOrder.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSortOrder.setMinimum(-999)
        self.spinSortOrder.setMaximum(999)

        self.horizontalLayout.addWidget(self.spinSortOrder)


        self.gridLayout.addLayout(self.horizontalLayout, 5, 2, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.teFinalscript = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teFinalscript.setObjectName(u"teFinalscript")

        self.horizontalLayout_2.addWidget(self.teFinalscript)

        self.buttonPickFinalscript = QPushButton(self.scrollAreaWidgetContents)
        self.buttonPickFinalscript.setObjectName(u"buttonPickFinalscript")

        self.horizontalLayout_2.addWidget(self.buttonPickFinalscript)


        self.gridLayout.addLayout(self.horizontalLayout_2, 9, 2, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 1, 1, 1)

        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.teBeschreibung = QPlainTextEdit(self.tab)
        self.teBeschreibung.setObjectName(u"teBeschreibung")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teBeschreibung.sizePolicy().hasHeightForWidth())
        self.teBeschreibung.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.teBeschreibung)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout = QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tbBeschreibung = QTextBrowser(self.tab_2)
        self.tbBeschreibung.setObjectName(u"tbBeschreibung")

        self.verticalLayout.addWidget(self.tbBeschreibung)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 6, 2, 1, 1)

        self.warning = QLabel(self.scrollAreaWidgetContents)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(True)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 1, 1, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.leName, self.leAnzeigeName)
        QWidget.setTabOrder(self.leAnzeigeName, self.checkShow)
        QWidget.setTabOrder(self.checkShow, self.spinSortOrder)
        QWidget.setTabOrder(self.spinSortOrder, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.teBeschreibung)
        QWidget.setTabOrder(self.teBeschreibung, self.leFormel)
        QWidget.setTabOrder(self.leFormel, self.teScript)
        QWidget.setTabOrder(self.teScript, self.buttonPickScript)
        QWidget.setTabOrder(self.buttonPickScript, self.teFinalscript)
        QWidget.setTabOrder(self.teFinalscript, self.buttonPickFinalscript)
        QWidget.setTabOrder(self.buttonPickFinalscript, self.tbBeschreibung)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Abgeleiteten Wert bearbeiten...", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Formel", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"Sortierreihenfolge", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Script", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u"Finalwert Script", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Voller Name", None))
#if QT_CONFIG(tooltip)
        self.leFormel.setToolTip(QCoreApplication.translate("dialog", u"Die Berechnungsformel, die im Charaktereditor neben dem Namen angezeigt werden soll.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.teScript.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>In diesem Feld kannst du ein Python-Skript einf\u00fcgen, das den Basiswert berechnet.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonPickScript.setToolTip(QCoreApplication.translate("dialog", u"Scripteditor \u00f6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonPickScript.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonPickScript.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.checkShow.setText(QCoreApplication.translate("dialog", u"Im Attribute-Tab des Charaktereditors zeigen", None))
#if QT_CONFIG(tooltip)
        self.spinSortOrder.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Die Reihenfolge, in der der Wert im Charaktereditor aufgef\u00fchrt werden soll.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.teFinalscript.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Manche abgeleitete Werte werden nach allen Berechnungen (erneut) modifiziert, beispielsweise indem die BE noch abgezogen wird. In diesem Feld kannst du ein Python-Skript einf\u00fcgen, das den finalen Wert berechnet.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonPickFinalscript.setToolTip(QCoreApplication.translate("dialog", u"Scripteditor \u00f6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonPickFinalscript.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonPickFinalscript.setProperty("class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.label_8.setText(QCoreApplication.translate("dialog", u"Anzeigen", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.warning.setText("")
    # retranslateUi

