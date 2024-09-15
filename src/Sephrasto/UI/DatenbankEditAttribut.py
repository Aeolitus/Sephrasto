# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditAttribut.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(511, 530)
        self.verticalLayout_3 = QVBoxLayout(dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 491, 510))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.gridLayout.addWidget(self.labelBeschreibung, 4, 0, 1, 1)

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

        self.gridLayout.addWidget(self.tabWidget, 4, 1, 1, 1)

        self.labelAnzeigeName = QLabel(self.scrollAreaWidgetContents)
        self.labelAnzeigeName.setObjectName(u"labelAnzeigeName")

        self.gridLayout.addWidget(self.labelAnzeigeName, 1, 0, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 0, 1, 1, 1)

        self.labelSF = QLabel(self.scrollAreaWidgetContents)
        self.labelSF.setObjectName(u"labelSF")

        self.gridLayout.addWidget(self.labelSF, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.spinSortOrder = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSortOrder.setObjectName(u"spinSortOrder")
        self.spinSortOrder.setMinimumSize(QSize(52, 0))
        self.spinSortOrder.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSortOrder.setMinimum(-999)
        self.spinSortOrder.setMaximum(999)

        self.horizontalLayout_2.addWidget(self.spinSortOrder)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)

        self.labelSortOrder = QLabel(self.scrollAreaWidgetContents)
        self.labelSortOrder.setObjectName(u"labelSortOrder")

        self.gridLayout.addWidget(self.labelSortOrder, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinSF = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSF.setObjectName(u"spinSF")
        self.spinSF.setMinimumSize(QSize(52, 0))
        self.spinSF.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSF.setMinimum(1)
        self.spinSF.setMaximum(999)
        self.spinSF.setValue(16)

        self.horizontalLayout.addWidget(self.spinSF)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.leAnzeigeName = QLineEdit(self.scrollAreaWidgetContents)
        self.leAnzeigeName.setObjectName(u"leAnzeigeName")

        self.gridLayout.addWidget(self.leAnzeigeName, 1, 1, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.leAnzeigeName)
        QWidget.setTabOrder(self.leAnzeigeName, self.spinSF)
        QWidget.setTabOrder(self.spinSF, self.spinSortOrder)
        QWidget.setTabOrder(self.spinSortOrder, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.teBeschreibung)
        QWidget.setTabOrder(self.teBeschreibung, self.tbBeschreibung)

        self.retranslateUi(dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Attribut bearbeiten...", None))
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.labelAnzeigeName.setText(QCoreApplication.translate("dialog", u"Voller Name", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelSF.setText(QCoreApplication.translate("dialog", u"Steigerungsfaktor", None))
#if QT_CONFIG(tooltip)
        self.spinSortOrder.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Die Reihenfolge, in der der Wert im Charaktereditor aufgef\u00fchrt werden soll.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelSortOrder.setText(QCoreApplication.translate("dialog", u"Sortierreihenfolge", None))
    # retranslateUi

