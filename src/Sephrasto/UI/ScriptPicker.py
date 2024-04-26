# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ScriptPicker.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSplitter, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(928, 522)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayout_2 = QWidget(self.splitter)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLayout_2.sizePolicy().hasHeightForWidth())
        self.verticalLayout_2.setSizePolicy(sizePolicy)
        self.verticalLayout2 = QVBoxLayout(self.verticalLayout_2)
        self.verticalLayout2.setObjectName(u"verticalLayout2")
        self.filterLayout = QHBoxLayout()
        self.filterLayout.setObjectName(u"filterLayout")
        self.buttonExpandToggle = QPushButton(self.verticalLayout_2)
        self.buttonExpandToggle.setObjectName(u"buttonExpandToggle")

        self.filterLayout.addWidget(self.buttonExpandToggle)

        self.nameFilterEdit = QLineEdit(self.verticalLayout_2)
        self.nameFilterEdit.setObjectName(u"nameFilterEdit")
        self.nameFilterEdit.setClearButtonEnabled(True)

        self.filterLayout.addWidget(self.nameFilterEdit)

        self.labelFilter = QLabel(self.verticalLayout_2)
        self.labelFilter.setObjectName(u"labelFilter")

        self.filterLayout.addWidget(self.labelFilter)

        self.buttonHelp = QPushButton(self.verticalLayout_2)
        self.buttonHelp.setObjectName(u"buttonHelp")

        self.filterLayout.addWidget(self.buttonHelp)


        self.verticalLayout2.addLayout(self.filterLayout)

        self.treeScripts = QTreeWidget(self.verticalLayout_2)
        self.treeScripts.setObjectName(u"treeScripts")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.treeScripts.sizePolicy().hasHeightForWidth())
        self.treeScripts.setSizePolicy(sizePolicy1)
        self.treeScripts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeScripts.setProperty("showDropIndicator", False)
        self.treeScripts.setAlternatingRowColors(True)
        self.treeScripts.setSortingEnabled(False)
        self.treeScripts.setAllColumnsShowFocus(True)
        self.treeScripts.header().setVisible(True)
        self.treeScripts.header().setCascadingSectionResizes(False)
        self.treeScripts.header().setDefaultSectionSize(150)
        self.treeScripts.header().setStretchLastSection(True)

        self.verticalLayout2.addWidget(self.treeScripts)

        self.splitter.addWidget(self.verticalLayout_2)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(220, 0))
        font = QFont()
        font.setBold(False)
        self.scrollArea.setFont(font)
        self.scrollArea.setStyleSheet(u"padding: 1px")
        self.scrollArea.setFrameShape(QFrame.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 452, 180))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.layoutParameter = QFormLayout()
        self.layoutParameter.setObjectName(u"layoutParameter")
        self.layoutParameter.setVerticalSpacing(14)

        self.gridLayout.addLayout(self.layoutParameter, 3, 0, 1, 1)

        self.lblName = QLabel(self.scrollAreaWidgetContents)
        self.lblName.setObjectName(u"lblName")
        font1 = QFont()
        font1.setBold(True)
        self.lblName.setFont(font1)

        self.gridLayout.addWidget(self.lblName, 0, 0, 1, 2)

        self.teBeschreibung = QTextBrowser(self.scrollAreaWidgetContents)
        self.teBeschreibung.setObjectName(u"teBeschreibung")

        self.gridLayout.addWidget(self.teBeschreibung, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.insertButtonLayout = QHBoxLayout()
        self.insertButtonLayout.setObjectName(u"insertButtonLayout")

        self.verticalLayout.addLayout(self.insertButtonLayout)

        self.codeLayout = QHBoxLayout()
        self.codeLayout.setObjectName(u"codeLayout")

        self.verticalLayout.addLayout(self.codeLayout)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(2, 3)
        self.splitter.addWidget(self.layoutWidget)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)

        QWidget.setTabOrder(self.buttonExpandToggle, self.nameFilterEdit)
        QWidget.setTabOrder(self.nameFilterEdit, self.treeScripts)
        QWidget.setTabOrder(self.treeScripts, self.scrollArea)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Sephrasto - Script erstellen...", None))
        self.buttonExpandToggle.setText(QCoreApplication.translate("Dialog", u"Expand Toggle", None))
        self.buttonExpandToggle.setProperty("class", QCoreApplication.translate("Dialog", u"icon", None))
        self.nameFilterEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Suchen...", None))
        self.labelFilter.setText(QCoreApplication.translate("Dialog", u"Suchen", None))
        self.labelFilter.setProperty("class", QCoreApplication.translate("Dialog", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonHelp.setToolTip(QCoreApplication.translate("Dialog", u"Script API Dokumentation \u00f6ffnen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonHelp.setText(QCoreApplication.translate("Dialog", u"Help", None))
        self.buttonHelp.setProperty("class", QCoreApplication.translate("Dialog", u"icon", None))
        ___qtreewidgetitem = self.treeScripts.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.lblName.setText(QCoreApplication.translate("Dialog", u"Script", None))
        self.lblName.setProperty("class", QCoreApplication.translate("Dialog", u"h4", None))
    # retranslateUi

