# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterFreieFertigkeitenPicker.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(461, 522)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QWidget(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLayout_2.sizePolicy().hasHeightForWidth())
        self.verticalLayout_2.setSizePolicy(sizePolicy)
        self.verticalLayout2 = QVBoxLayout(self.verticalLayout_2)
        self.verticalLayout2.setObjectName(u"verticalLayout2")
        self.labelUnofficial = QLabel(self.verticalLayout_2)
        self.labelUnofficial.setObjectName(u"labelUnofficial")
        self.labelUnofficial.setWordWrap(True)

        self.verticalLayout2.addWidget(self.labelUnofficial)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nameFilterEdit = QLineEdit(self.verticalLayout_2)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")
        self.nameFilterEdit.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.nameFilterEdit)

        self.labelFilter = QLabel(self.verticalLayout_2)
        self.labelFilter.setObjectName(u"labelFilter")

        self.horizontalLayout.addWidget(self.labelFilter)


        self.verticalLayout2.addLayout(self.horizontalLayout)

        self.treeFerts = QTreeWidget(self.verticalLayout_2)
        self.treeFerts.setObjectName(u"treeFerts")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.treeFerts.sizePolicy().hasHeightForWidth())
        self.treeFerts.setSizePolicy(sizePolicy1)
        self.treeFerts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeFerts.setProperty("showDropIndicator", False)
        self.treeFerts.setAlternatingRowColors(True)
        self.treeFerts.setSortingEnabled(False)
        self.treeFerts.setAllColumnsShowFocus(True)
        self.treeFerts.header().setVisible(True)
        self.treeFerts.header().setCascadingSectionResizes(False)
        self.treeFerts.header().setDefaultSectionSize(150)
        self.treeFerts.header().setStretchLastSection(True)

        self.verticalLayout2.addWidget(self.treeFerts)

        self.buttonBox = QDialogButtonBox(self.verticalLayout_2)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout2.addWidget(self.buttonBox)


        self.gridLayout.addWidget(self.verticalLayout_2, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nameFilterEdit, self.treeFerts)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Sephrasto - Freie Fertigkeit w\u00e4hlen...", None))
        self.labelUnofficial.setText(QCoreApplication.translate("Dialog", u"Inoffiziell: Bei den aufgef\u00fchrten Sprachen und Schriften handelt es sich um an WdS orientierte Vorschl\u00e4ge.", None))
        self.nameFilterEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Suchen...", None))
        self.labelFilter.setText(QCoreApplication.translate("Dialog", u"Suchen", None))
        self.labelFilter.setProperty("class", QCoreApplication.translate("Dialog", u"icon", None))
        ___qtreewidgetitem = self.treeFerts.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Freie Fertigkeit", None));
    # retranslateUi

