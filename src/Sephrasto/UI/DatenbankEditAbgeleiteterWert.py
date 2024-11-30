# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditAbgeleiteterWert.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(526, 617)
        self.verticalLayout_3 = QVBoxLayout(dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 485, 617))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leName)

        self.labelAnzeigeName = QLabel(self.scrollAreaWidgetContents)
        self.labelAnzeigeName.setObjectName(u"labelAnzeigeName")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelAnzeigeName)

        self.leAnzeigeName = QLineEdit(self.scrollAreaWidgetContents)
        self.leAnzeigeName.setObjectName(u"leAnzeigeName")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.leAnzeigeName)

        self.labelShow = QLabel(self.scrollAreaWidgetContents)
        self.labelShow.setObjectName(u"labelShow")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelShow)

        self.checkShow = QCheckBox(self.scrollAreaWidgetContents)
        self.checkShow.setObjectName(u"checkShow")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.checkShow)

        self.labelSortOrder = QLabel(self.scrollAreaWidgetContents)
        self.labelSortOrder.setObjectName(u"labelSortOrder")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelSortOrder)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinSortOrder = QSpinBox(self.scrollAreaWidgetContents)
        self.spinSortOrder.setObjectName(u"spinSortOrder")
        self.spinSortOrder.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.spinSortOrder.setMinimum(-999)
        self.spinSortOrder.setMaximum(999)

        self.horizontalLayout.addWidget(self.spinSortOrder)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)

        self.labelBeschreibung = QLabel(self.scrollAreaWidgetContents)
        self.labelBeschreibung.setObjectName(u"labelBeschreibung")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelBeschreibung)

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

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.tabWidget)

        self.labelFormel = QLabel(self.scrollAreaWidgetContents)
        self.labelFormel.setObjectName(u"labelFormel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelFormel)

        self.leFormel = QLineEdit(self.scrollAreaWidgetContents)
        self.leFormel.setObjectName(u"leFormel")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.leFormel)

        self.labelScript = QLabel(self.scrollAreaWidgetContents)
        self.labelScript.setObjectName(u"labelScript")
        self.labelScript.setMinimumSize(QSize(110, 0))

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelScript)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.teScript = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teScript.setObjectName(u"teScript")

        self.horizontalLayout_3.addWidget(self.teScript)

        self.buttonPickScript = QPushButton(self.scrollAreaWidgetContents)
        self.buttonPickScript.setObjectName(u"buttonPickScript")
        font = QFont()
        font.setHintingPreference(QFont.PreferNoHinting)
        self.buttonPickScript.setFont(font)

        self.horizontalLayout_3.addWidget(self.buttonPickScript)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.labelFinalscript = QLabel(self.scrollAreaWidgetContents)
        self.labelFinalscript.setObjectName(u"labelFinalscript")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelFinalscript)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.teFinalscript = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teFinalscript.setObjectName(u"teFinalscript")

        self.horizontalLayout_2.addWidget(self.teFinalscript)

        self.buttonPickFinalscript = QPushButton(self.scrollAreaWidgetContents)
        self.buttonPickFinalscript.setObjectName(u"buttonPickFinalscript")
        self.buttonPickFinalscript.setFont(font)

        self.horizontalLayout_2.addWidget(self.buttonPickFinalscript)


        self.formLayout.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

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

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Abgeleiteten Wert bearbeiten...", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelAnzeigeName.setText(QCoreApplication.translate("dialog", u"Voller Name", None))
        self.labelShow.setText(QCoreApplication.translate("dialog", u"Anzeigen", None))
        self.checkShow.setText(QCoreApplication.translate("dialog", u"Im Attribute-Tab des Charaktereditors zeigen", None))
        self.labelSortOrder.setText(QCoreApplication.translate("dialog", u"Sortierreihenfolge", None))
#if QT_CONFIG(tooltip)
        self.spinSortOrder.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Die Reihenfolge, in der der Wert im Charaktereditor aufgef\u00fchrt werden soll.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelBeschreibung.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.labelFormel.setText(QCoreApplication.translate("dialog", u"Formel", None))
#if QT_CONFIG(tooltip)
        self.leFormel.setToolTip(QCoreApplication.translate("dialog", u"Die Berechnungsformel, die im Charaktereditor neben dem Namen angezeigt werden soll.", None))
#endif // QT_CONFIG(tooltip)
        self.labelScript.setText(QCoreApplication.translate("dialog", u"Script", None))
#if QT_CONFIG(tooltip)
        self.teScript.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>In diesem Feld kannst du ein Python-Skript einf\u00fcgen, das den Basiswert berechnet.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonPickScript.setToolTip(QCoreApplication.translate("dialog", u"Scripteditor \u00f6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonPickScript.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonPickScript.setProperty(u"class", QCoreApplication.translate("dialog", u"iconSmall", None))
        self.labelFinalscript.setText(QCoreApplication.translate("dialog", u"Finalwert Script", None))
#if QT_CONFIG(tooltip)
        self.teFinalscript.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Manche abgeleitete Werte werden nach allen Berechnungen (erneut) modifiziert, beispielsweise indem die BE noch abgezogen wird. In diesem Feld kannst du ein Python-Skript einf\u00fcgen, das den finalen Wert berechnet.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonPickFinalscript.setToolTip(QCoreApplication.translate("dialog", u"Scripteditor \u00f6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonPickFinalscript.setText(QCoreApplication.translate("dialog", u"+", None))
        self.buttonPickFinalscript.setProperty(u"class", QCoreApplication.translate("dialog", u"iconSmall", None))
    # retranslateUi

