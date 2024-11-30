# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenbankErrorLog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.resize(889, 449)
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.listWidget = QListWidget(dialog)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonRefresh = QPushButton(dialog)
        self.buttonRefresh.setObjectName(u"buttonRefresh")
        self.buttonRefresh.setMinimumSize(QSize(28, 28))
        self.buttonRefresh.setMaximumSize(QSize(28, 28))
        font = QFont()
        font.setHintingPreference(QFont.PreferNoHinting)
        self.buttonRefresh.setFont(font)

        self.horizontalLayout.addWidget(self.buttonRefresh)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Sephrasto - Datenbankfehler", None))
#if QT_CONFIG(tooltip)
        self.buttonRefresh.setToolTip(QCoreApplication.translate("dialog", u"Aktualisieren", None))
#endif // QT_CONFIG(tooltip)
        self.buttonRefresh.setText(QCoreApplication.translate("dialog", u"Refresh", None))
        self.buttonRefresh.setProperty(u"class", QCoreApplication.translate("dialog", u"icon", None))
        self.label.setText(QCoreApplication.translate("dialog", u"Probleme beim Laden der Hausregeln entdeckt! Mit einem Doppelclick gelangst du direkt zum entsprechenden Element.", None))
    # retranslateUi

