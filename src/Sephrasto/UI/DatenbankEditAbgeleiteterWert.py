# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankEditAbgeleiteterWert.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
    QLabel, QLineEdit, QPlainTextEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(440, 484)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.leScript = QLineEdit(dialog)
        self.leScript.setObjectName(u"leScript")

        self.gridLayout.addWidget(self.leScript, 7, 1, 1, 1)

        self.label_3 = QLabel(dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(110, 0))

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.label_8 = QLabel(dialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spinSortOrder = QSpinBox(dialog)
        self.spinSortOrder.setObjectName(u"spinSortOrder")
        self.spinSortOrder.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinSortOrder.setMinimum(-999)
        self.spinSortOrder.setMaximum(999)

        self.horizontalLayout.addWidget(self.spinSortOrder)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 1)

        self.leName = QLineEdit(dialog)
        self.leName.setObjectName(u"leName")

        self.gridLayout.addWidget(self.leName, 1, 1, 1, 1)

        self.label_2 = QLabel(dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.warning = QLabel(dialog)
        self.warning.setObjectName(u"warning")
        self.warning.setVisible(False)
        self.warning.setStyleSheet(u"background-color: rgb(255, 255, 0); color: black;")
        self.warning.setWordWrap(True)

        self.gridLayout.addWidget(self.warning, 0, 0, 1, 2)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_5 = QLabel(dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.leFormel = QLineEdit(dialog)
        self.leFormel.setObjectName(u"leFormel")

        self.gridLayout.addWidget(self.leFormel, 6, 1, 1, 1)

        self.label_4 = QLabel(dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.leAnzeigeName = QLineEdit(dialog)
        self.leAnzeigeName.setObjectName(u"leAnzeigeName")

        self.gridLayout.addWidget(self.leAnzeigeName, 2, 1, 1, 1)

        self.label_7 = QLabel(dialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)

        self.leFinalscript = QLineEdit(dialog)
        self.leFinalscript.setObjectName(u"leFinalscript")

        self.gridLayout.addWidget(self.leFinalscript, 8, 1, 1, 1)

        self.tabWidget = QTabWidget(dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.teBeschreibung = QPlainTextEdit(self.tab)
        self.teBeschreibung.setObjectName(u"teBeschreibung")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
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

        self.gridLayout.addWidget(self.tabWidget, 5, 1, 1, 1)

        self.checkShow = QCheckBox(dialog)
        self.checkShow.setObjectName(u"checkShow")

        self.gridLayout.addWidget(self.checkShow, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

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
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Abgeleiteten Wert bearbeiten...", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"Sortierreihenfolge", None))
#if QT_CONFIG(tooltip)
        self.leScript.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>In diesem Feld kannst du ein Python-Skript einf\u00fcgen, das den Basiswert berechnet. Siehe &quot;Skripte f\u00fcr Abgeleitete Werte, Vorteile und Waffeneigenschaften&quot; in der Sephrasto-Hilfe f\u00fcr verf\u00fcgbare Funktionen und Beispiele.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("dialog", u"Script", None))
        self.label_8.setText(QCoreApplication.translate("dialog", u"Anzeigen", None))
#if QT_CONFIG(tooltip)
        self.spinSortOrder.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Die Reihenfolge, in der der Wert im Charaktereditor aufgef\u00fchrt werden soll.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("dialog", u"Voller Name", None))
        self.warning.setText("")
        self.label.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"Beschreibung", None))
#if QT_CONFIG(tooltip)
        self.leFormel.setToolTip(QCoreApplication.translate("dialog", u"Die Berechnungsformel, die im Charaktereditor neben dem Namen angezeigt werden soll.", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("dialog", u"Formel", None))
        self.label_7.setText(QCoreApplication.translate("dialog", u"Finalwert Script", None))
#if QT_CONFIG(tooltip)
        self.leFinalscript.setToolTip(QCoreApplication.translate("dialog", u"<html><head/><body><p>Manche abgeleitete Werte werden nach allen Berechnungen (erneut) modifiziert, beispielsweise indem die BE noch abgezogen wird. In diesem Feld kannst du ein Python-Skript einf\u00fcgen, das den finalen Wert berechnet. Siehe &quot;Skripte f\u00fcr Abgeleitete Werte, Vorteile und Waffeneigenschaften&quot; in der Sephrasto-Hilfe f\u00fcr verf\u00fcgbare Funktionen und Beispiele.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("dialog", u"HTML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("dialog", u"Vorschau", None))
        self.checkShow.setText(QCoreApplication.translate("dialog", u"Im Attribute-Tab des Charaktereditors zeigen", None))
    # retranslateUi

