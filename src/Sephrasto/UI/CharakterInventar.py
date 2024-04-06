# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterInventar.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QGridLayout,
    QGroupBox, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_formInventar(object):
    def setupUi(self, formInventar):
        if not formInventar.objectName():
            formInventar.setObjectName(u"formInventar")
        formInventar.resize(971, 586)
        formInventar.setMinimumSize(QSize(802, 0))
        self.verticalLayout = QVBoxLayout(formInventar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.gbRstungen = QGroupBox(formInventar)
        self.gbRstungen.setObjectName(u"gbRstungen")
        self.verticalLayout_3 = QVBoxLayout(self.gbRstungen)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.Ruestungen = QGridLayout()
        self.Ruestungen.setObjectName(u"Ruestungen")
        self.Ruestungen.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.spinR2brust = QSpinBox(self.gbRstungen)
        self.spinR2brust.setObjectName(u"spinR2brust")
        self.spinR2brust.setMinimumSize(QSize(44, 0))
        self.spinR2brust.setAlignment(Qt.AlignCenter)
        self.spinR2brust.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2brust.setMaximum(8)

        self.Ruestungen.addWidget(self.spinR2brust, 2, 7, 1, 1)

        self.spinR1bauch = QSpinBox(self.gbRstungen)
        self.spinR1bauch.setObjectName(u"spinR1bauch")
        self.spinR1bauch.setMinimumSize(QSize(44, 0))
        self.spinR1bauch.setAlignment(Qt.AlignCenter)
        self.spinR1bauch.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1bauch.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1bauch, 1, 6, 1, 1)

        self.removeR3 = QPushButton(self.gbRstungen)
        self.removeR3.setObjectName(u"removeR3")

        self.Ruestungen.addWidget(self.removeR3, 3, 10, 1, 1)

        self.spinR2kopf = QSpinBox(self.gbRstungen)
        self.spinR2kopf.setObjectName(u"spinR2kopf")
        self.spinR2kopf.setMinimumSize(QSize(44, 0))
        self.spinR2kopf.setAlignment(Qt.AlignCenter)
        self.spinR2kopf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2kopf.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR2kopf, 2, 8, 1, 1)

        self.spinR2RS = QSpinBox(self.gbRstungen)
        self.spinR2RS.setObjectName(u"spinR2RS")
        self.spinR2RS.setMinimumSize(QSize(44, 0))
        self.spinR2RS.setAlignment(Qt.AlignCenter)
        self.spinR2RS.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2RS.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR2RS, 2, 2, 1, 1)

        self.spinR2be = QSpinBox(self.gbRstungen)
        self.spinR2be.setObjectName(u"spinR2be")
        self.spinR2be.setMinimumSize(QSize(44, 0))
        self.spinR2be.setAlignment(Qt.AlignCenter)
        self.spinR2be.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2be.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR2be, 2, 1, 1, 1)

        self.spinR2rarm = QSpinBox(self.gbRstungen)
        self.spinR2rarm.setObjectName(u"spinR2rarm")
        self.spinR2rarm.setMinimumSize(QSize(44, 0))
        self.spinR2rarm.setAlignment(Qt.AlignCenter)
        self.spinR2rarm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2rarm.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR2rarm, 2, 5, 1, 1)

        self.editR3name = QLineEdit(self.gbRstungen)
        self.editR3name.setObjectName(u"editR3name")

        self.Ruestungen.addWidget(self.editR3name, 3, 0, 1, 1)

        self.spinR3bein = QSpinBox(self.gbRstungen)
        self.spinR3bein.setObjectName(u"spinR3bein")
        self.spinR3bein.setMinimumSize(QSize(44, 0))
        self.spinR3bein.setAlignment(Qt.AlignCenter)
        self.spinR3bein.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3bein.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3bein, 3, 3, 1, 1)

        self.spinR1be = QSpinBox(self.gbRstungen)
        self.spinR1be.setObjectName(u"spinR1be")
        self.spinR1be.setMinimumSize(QSize(44, 0))
        self.spinR1be.setAlignment(Qt.AlignCenter)
        self.spinR1be.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1be.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1be, 1, 1, 1, 1)

        self.spinR1rarm = QSpinBox(self.gbRstungen)
        self.spinR1rarm.setObjectName(u"spinR1rarm")
        self.spinR1rarm.setMinimumSize(QSize(44, 0))
        self.spinR1rarm.setAlignment(Qt.AlignCenter)
        self.spinR1rarm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1rarm.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1rarm, 1, 5, 1, 1)

        self.labelRS = QLabel(self.gbRstungen)
        self.labelRS.setObjectName(u"labelRS")
        font = QFont()
        font.setBold(True)
        self.labelRS.setFont(font)
        self.labelRS.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelRS, 0, 2, 1, 1)

        self.labelRName = QLabel(self.gbRstungen)
        self.labelRName.setObjectName(u"labelRName")
        self.labelRName.setFont(font)

        self.Ruestungen.addWidget(self.labelRName, 0, 0, 1, 1)

        self.addR3 = QPushButton(self.gbRstungen)
        self.addR3.setObjectName(u"addR3")

        self.Ruestungen.addWidget(self.addR3, 3, 11, 1, 1)

        self.spinR1brust = QSpinBox(self.gbRstungen)
        self.spinR1brust.setObjectName(u"spinR1brust")
        self.spinR1brust.setMinimumSize(QSize(44, 0))
        self.spinR1brust.setAlignment(Qt.AlignCenter)
        self.spinR1brust.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1brust.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1brust, 1, 7, 1, 1)

        self.spinR3rarm = QSpinBox(self.gbRstungen)
        self.spinR3rarm.setObjectName(u"spinR3rarm")
        self.spinR3rarm.setMinimumSize(QSize(44, 0))
        self.spinR3rarm.setAlignment(Qt.AlignCenter)
        self.spinR3rarm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3rarm.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3rarm, 3, 5, 1, 1)

        self.labelBrust = QLabel(self.gbRstungen)
        self.labelBrust.setObjectName(u"labelBrust")
        self.labelBrust.setMinimumSize(QSize(35, 0))
        self.labelBrust.setFont(font)
        self.labelBrust.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelBrust, 0, 7, 1, 1)

        self.labelBE = QLabel(self.gbRstungen)
        self.labelBE.setObjectName(u"labelBE")
        self.labelBE.setMinimumSize(QSize(35, 0))
        self.labelBE.setFont(font)
        self.labelBE.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelBE, 0, 1, 1, 1)

        self.labelBauch = QLabel(self.gbRstungen)
        self.labelBauch.setObjectName(u"labelBauch")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelBauch.sizePolicy().hasHeightForWidth())
        self.labelBauch.setSizePolicy(sizePolicy)
        self.labelBauch.setMinimumSize(QSize(35, 0))
        self.labelBauch.setFont(font)
        self.labelBauch.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelBauch, 0, 6, 1, 1)

        self.spinR1RS = QSpinBox(self.gbRstungen)
        self.spinR1RS.setObjectName(u"spinR1RS")
        self.spinR1RS.setMinimumSize(QSize(44, 0))
        self.spinR1RS.setAlignment(Qt.AlignCenter)
        self.spinR1RS.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1RS.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1RS, 1, 2, 1, 1)

        self.spinR3larm = QSpinBox(self.gbRstungen)
        self.spinR3larm.setObjectName(u"spinR3larm")
        self.spinR3larm.setMinimumSize(QSize(44, 0))
        self.spinR3larm.setAlignment(Qt.AlignCenter)
        self.spinR3larm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3larm.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3larm, 3, 4, 1, 1)

        self.labelRarm = QLabel(self.gbRstungen)
        self.labelRarm.setObjectName(u"labelRarm")
        sizePolicy.setHeightForWidth(self.labelRarm.sizePolicy().hasHeightForWidth())
        self.labelRarm.setSizePolicy(sizePolicy)
        self.labelRarm.setMinimumSize(QSize(35, 0))
        self.labelRarm.setFont(font)
        self.labelRarm.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelRarm, 0, 5, 1, 1)

        self.labelBein = QLabel(self.gbRstungen)
        self.labelBein.setObjectName(u"labelBein")
        self.labelBein.setMinimumSize(QSize(35, 0))
        self.labelBein.setFont(font)
        self.labelBein.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelBein, 0, 3, 1, 1)

        self.spinR2punkte = QSpinBox(self.gbRstungen)
        self.spinR2punkte.setObjectName(u"spinR2punkte")
        self.spinR2punkte.setEnabled(True)
        self.spinR2punkte.setMinimumSize(QSize(44, 0))
        self.spinR2punkte.setFrame(False)
        self.spinR2punkte.setAlignment(Qt.AlignCenter)
        self.spinR2punkte.setReadOnly(True)
        self.spinR2punkte.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinR2punkte.setMaximum(999)

        self.Ruestungen.addWidget(self.spinR2punkte, 2, 9, 1, 1)

        self.spinR1punkte = QSpinBox(self.gbRstungen)
        self.spinR1punkte.setObjectName(u"spinR1punkte")
        self.spinR1punkte.setMinimumSize(QSize(44, 0))
        self.spinR1punkte.setFrame(False)
        self.spinR1punkte.setAlignment(Qt.AlignCenter)
        self.spinR1punkte.setReadOnly(True)
        self.spinR1punkte.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinR1punkte.setMaximum(999)

        self.Ruestungen.addWidget(self.spinR1punkte, 1, 9, 1, 1)

        self.spinR3kopf = QSpinBox(self.gbRstungen)
        self.spinR3kopf.setObjectName(u"spinR3kopf")
        self.spinR3kopf.setMinimumSize(QSize(44, 0))
        self.spinR3kopf.setAlignment(Qt.AlignCenter)
        self.spinR3kopf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3kopf.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3kopf, 3, 8, 1, 1)

        self.labelLarm = QLabel(self.gbRstungen)
        self.labelLarm.setObjectName(u"labelLarm")
        self.labelLarm.setMinimumSize(QSize(35, 0))
        self.labelLarm.setFont(font)
        self.labelLarm.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelLarm, 0, 4, 1, 1)

        self.spinR2bein = QSpinBox(self.gbRstungen)
        self.spinR2bein.setObjectName(u"spinR2bein")
        self.spinR2bein.setMinimumSize(QSize(44, 0))
        self.spinR2bein.setAlignment(Qt.AlignCenter)
        self.spinR2bein.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2bein.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR2bein, 2, 3, 1, 1)

        self.spinR3RS = QSpinBox(self.gbRstungen)
        self.spinR3RS.setObjectName(u"spinR3RS")
        self.spinR3RS.setMinimumSize(QSize(44, 0))
        self.spinR3RS.setAlignment(Qt.AlignCenter)
        self.spinR3RS.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3RS.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3RS, 3, 2, 1, 1)

        self.spinR1larm = QSpinBox(self.gbRstungen)
        self.spinR1larm.setObjectName(u"spinR1larm")
        self.spinR1larm.setMinimumSize(QSize(44, 0))
        self.spinR1larm.setAlignment(Qt.AlignCenter)
        self.spinR1larm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1larm.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1larm, 1, 4, 1, 1)

        self.editR1name = QLineEdit(self.gbRstungen)
        self.editR1name.setObjectName(u"editR1name")

        self.Ruestungen.addWidget(self.editR1name, 1, 0, 1, 1)

        self.labelKopf = QLabel(self.gbRstungen)
        self.labelKopf.setObjectName(u"labelKopf")
        self.labelKopf.setMinimumSize(QSize(35, 0))
        self.labelKopf.setFont(font)
        self.labelKopf.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelKopf, 0, 8, 1, 1)

        self.spinR3punkte = QSpinBox(self.gbRstungen)
        self.spinR3punkte.setObjectName(u"spinR3punkte")
        self.spinR3punkte.setEnabled(True)
        self.spinR3punkte.setMinimumSize(QSize(44, 0))
        self.spinR3punkte.setFrame(False)
        self.spinR3punkte.setAlignment(Qt.AlignCenter)
        self.spinR3punkte.setReadOnly(True)
        self.spinR3punkte.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinR3punkte.setMaximum(999)

        self.Ruestungen.addWidget(self.spinR3punkte, 3, 9, 1, 1)

        self.spinR2bauch = QSpinBox(self.gbRstungen)
        self.spinR2bauch.setObjectName(u"spinR2bauch")
        self.spinR2bauch.setMinimumSize(QSize(44, 0))
        self.spinR2bauch.setAlignment(Qt.AlignCenter)
        self.spinR2bauch.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2bauch.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR2bauch, 2, 6, 1, 1)

        self.addR1 = QPushButton(self.gbRstungen)
        self.addR1.setObjectName(u"addR1")

        self.Ruestungen.addWidget(self.addR1, 1, 11, 1, 1)

        self.editR2name = QLineEdit(self.gbRstungen)
        self.editR2name.setObjectName(u"editR2name")

        self.Ruestungen.addWidget(self.editR2name, 2, 0, 1, 1)

        self.spinR2larm = QSpinBox(self.gbRstungen)
        self.spinR2larm.setObjectName(u"spinR2larm")
        self.spinR2larm.setMinimumSize(QSize(44, 0))
        self.spinR2larm.setAlignment(Qt.AlignCenter)
        self.spinR2larm.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR2larm.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR2larm, 2, 4, 1, 1)

        self.spinR1kopf = QSpinBox(self.gbRstungen)
        self.spinR1kopf.setObjectName(u"spinR1kopf")
        self.spinR1kopf.setMinimumSize(QSize(44, 0))
        self.spinR1kopf.setAlignment(Qt.AlignCenter)
        self.spinR1kopf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1kopf.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1kopf, 1, 8, 1, 1)

        self.removeR2 = QPushButton(self.gbRstungen)
        self.removeR2.setObjectName(u"removeR2")

        self.Ruestungen.addWidget(self.removeR2, 2, 10, 1, 1)

        self.addR2 = QPushButton(self.gbRstungen)
        self.addR2.setObjectName(u"addR2")

        self.Ruestungen.addWidget(self.addR2, 2, 11, 1, 1)

        self.removeR1 = QPushButton(self.gbRstungen)
        self.removeR1.setObjectName(u"removeR1")

        self.Ruestungen.addWidget(self.removeR1, 1, 10, 1, 1)

        self.labelPunkte = QLabel(self.gbRstungen)
        self.labelPunkte.setObjectName(u"labelPunkte")
        self.labelPunkte.setFont(font)
        self.labelPunkte.setAlignment(Qt.AlignCenter)

        self.Ruestungen.addWidget(self.labelPunkte, 0, 9, 1, 1)

        self.spinR3be = QSpinBox(self.gbRstungen)
        self.spinR3be.setObjectName(u"spinR3be")
        self.spinR3be.setMinimumSize(QSize(44, 0))
        self.spinR3be.setAlignment(Qt.AlignCenter)
        self.spinR3be.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3be.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3be, 3, 1, 1, 1)

        self.spinR3brust = QSpinBox(self.gbRstungen)
        self.spinR3brust.setObjectName(u"spinR3brust")
        self.spinR3brust.setMinimumSize(QSize(44, 0))
        self.spinR3brust.setAlignment(Qt.AlignCenter)
        self.spinR3brust.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3brust.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3brust, 3, 7, 1, 1)

        self.spinR1bein = QSpinBox(self.gbRstungen)
        self.spinR1bein.setObjectName(u"spinR1bein")
        self.spinR1bein.setMinimumSize(QSize(44, 0))
        self.spinR1bein.setAlignment(Qt.AlignCenter)
        self.spinR1bein.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR1bein.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR1bein, 1, 3, 1, 1)

        self.spinR3bauch = QSpinBox(self.gbRstungen)
        self.spinR3bauch.setObjectName(u"spinR3bauch")
        self.spinR3bauch.setMinimumSize(QSize(44, 0))
        self.spinR3bauch.setAlignment(Qt.AlignCenter)
        self.spinR3bauch.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinR3bauch.setMaximum(99)

        self.Ruestungen.addWidget(self.spinR3bauch, 3, 6, 1, 1)


        self.verticalLayout_3.addLayout(self.Ruestungen)

        self.checkZonen = QCheckBox(self.gbRstungen)
        self.checkZonen.setObjectName(u"checkZonen")
        self.checkZonen.setMinimumSize(QSize(0, 18))
        self.checkZonen.setLayoutDirection(Qt.RightToLeft)
        self.checkZonen.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkZonen)


        self.verticalLayout.addWidget(self.gbRstungen)

        self.gbInventar = QGroupBox(formInventar)
        self.gbInventar.setObjectName(u"gbInventar")
        self.gbInventar.setFlat(False)
        self.gridLayout_2 = QGridLayout(self.gbInventar)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(20, 20, 20, 20)
        self.lineEdit_11 = QLineEdit(self.gbInventar)
        self.lineEdit_11.setObjectName(u"lineEdit_11")

        self.gridLayout_2.addWidget(self.lineEdit_11, 5, 0, 1, 1)

        self.lineEdit_19 = QLineEdit(self.gbInventar)
        self.lineEdit_19.setObjectName(u"lineEdit_19")

        self.gridLayout_2.addWidget(self.lineEdit_19, 9, 0, 1, 1)

        self.lineEdit_3 = QLineEdit(self.gbInventar)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout_2.addWidget(self.lineEdit_3, 1, 0, 1, 1)

        self.lineEdit_17 = QLineEdit(self.gbInventar)
        self.lineEdit_17.setObjectName(u"lineEdit_17")

        self.gridLayout_2.addWidget(self.lineEdit_17, 8, 0, 1, 1)

        self.lineEdit_18 = QLineEdit(self.gbInventar)
        self.lineEdit_18.setObjectName(u"lineEdit_18")

        self.gridLayout_2.addWidget(self.lineEdit_18, 8, 1, 1, 1)

        self.lineEdit_7 = QLineEdit(self.gbInventar)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.gridLayout_2.addWidget(self.lineEdit_7, 3, 0, 1, 1)

        self.lineEdit_12 = QLineEdit(self.gbInventar)
        self.lineEdit_12.setObjectName(u"lineEdit_12")

        self.gridLayout_2.addWidget(self.lineEdit_12, 5, 1, 1, 1)

        self.lineEdit_15 = QLineEdit(self.gbInventar)
        self.lineEdit_15.setObjectName(u"lineEdit_15")

        self.gridLayout_2.addWidget(self.lineEdit_15, 7, 0, 1, 1)

        self.lineEdit_4 = QLineEdit(self.gbInventar)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout_2.addWidget(self.lineEdit_4, 1, 1, 1, 1)

        self.lineEdit_14 = QLineEdit(self.gbInventar)
        self.lineEdit_14.setObjectName(u"lineEdit_14")

        self.gridLayout_2.addWidget(self.lineEdit_14, 6, 1, 1, 1)

        self.lineEdit_10 = QLineEdit(self.gbInventar)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.gridLayout_2.addWidget(self.lineEdit_10, 4, 1, 1, 1)

        self.lineEdit_8 = QLineEdit(self.gbInventar)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.gridLayout_2.addWidget(self.lineEdit_8, 3, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(self.gbInventar)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(320, 0))

        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.lineEdit_20 = QLineEdit(self.gbInventar)
        self.lineEdit_20.setObjectName(u"lineEdit_20")

        self.gridLayout_2.addWidget(self.lineEdit_20, 9, 1, 1, 1)

        self.lineEdit_5 = QLineEdit(self.gbInventar)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.gridLayout_2.addWidget(self.lineEdit_5, 2, 0, 1, 1)

        self.lineEdit_16 = QLineEdit(self.gbInventar)
        self.lineEdit_16.setObjectName(u"lineEdit_16")

        self.gridLayout_2.addWidget(self.lineEdit_16, 7, 1, 1, 1)

        self.lineEdit_6 = QLineEdit(self.gbInventar)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.gridLayout_2.addWidget(self.lineEdit_6, 2, 1, 1, 1)

        self.lineEdit_9 = QLineEdit(self.gbInventar)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.gridLayout_2.addWidget(self.lineEdit_9, 4, 0, 1, 1)

        self.lineEdit_13 = QLineEdit(self.gbInventar)
        self.lineEdit_13.setObjectName(u"lineEdit_13")

        self.gridLayout_2.addWidget(self.lineEdit_13, 6, 0, 1, 1)

        self.lineEdit_1 = QLineEdit(self.gbInventar)
        self.lineEdit_1.setObjectName(u"lineEdit_1")
        self.lineEdit_1.setMinimumSize(QSize(320, 0))
        self.lineEdit_1.setCursor(QCursor(Qt.IBeamCursor))

        self.gridLayout_2.addWidget(self.lineEdit_1, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.gbInventar)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.editR1name, self.spinR1be)
        QWidget.setTabOrder(self.spinR1be, self.spinR1RS)
        QWidget.setTabOrder(self.spinR1RS, self.spinR1bein)
        QWidget.setTabOrder(self.spinR1bein, self.spinR1larm)
        QWidget.setTabOrder(self.spinR1larm, self.spinR1rarm)
        QWidget.setTabOrder(self.spinR1rarm, self.spinR1bauch)
        QWidget.setTabOrder(self.spinR1bauch, self.spinR1brust)
        QWidget.setTabOrder(self.spinR1brust, self.spinR1kopf)
        QWidget.setTabOrder(self.spinR1kopf, self.spinR1punkte)
        QWidget.setTabOrder(self.spinR1punkte, self.addR1)
        QWidget.setTabOrder(self.addR1, self.editR2name)
        QWidget.setTabOrder(self.editR2name, self.spinR2be)
        QWidget.setTabOrder(self.spinR2be, self.spinR2RS)
        QWidget.setTabOrder(self.spinR2RS, self.spinR2bein)
        QWidget.setTabOrder(self.spinR2bein, self.spinR2larm)
        QWidget.setTabOrder(self.spinR2larm, self.spinR2rarm)
        QWidget.setTabOrder(self.spinR2rarm, self.spinR2bauch)
        QWidget.setTabOrder(self.spinR2bauch, self.spinR2brust)
        QWidget.setTabOrder(self.spinR2brust, self.spinR2kopf)
        QWidget.setTabOrder(self.spinR2kopf, self.spinR2punkte)
        QWidget.setTabOrder(self.spinR2punkte, self.addR2)
        QWidget.setTabOrder(self.addR2, self.editR3name)
        QWidget.setTabOrder(self.editR3name, self.spinR3be)
        QWidget.setTabOrder(self.spinR3be, self.spinR3RS)
        QWidget.setTabOrder(self.spinR3RS, self.spinR3bein)
        QWidget.setTabOrder(self.spinR3bein, self.spinR3larm)
        QWidget.setTabOrder(self.spinR3larm, self.spinR3rarm)
        QWidget.setTabOrder(self.spinR3rarm, self.spinR3bauch)
        QWidget.setTabOrder(self.spinR3bauch, self.spinR3brust)
        QWidget.setTabOrder(self.spinR3brust, self.spinR3kopf)
        QWidget.setTabOrder(self.spinR3kopf, self.spinR3punkte)
        QWidget.setTabOrder(self.spinR3punkte, self.addR3)
        QWidget.setTabOrder(self.addR3, self.checkZonen)
        QWidget.setTabOrder(self.checkZonen, self.lineEdit_1)
        QWidget.setTabOrder(self.lineEdit_1, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.lineEdit_7)
        QWidget.setTabOrder(self.lineEdit_7, self.lineEdit_9)
        QWidget.setTabOrder(self.lineEdit_9, self.lineEdit_11)
        QWidget.setTabOrder(self.lineEdit_11, self.lineEdit_13)
        QWidget.setTabOrder(self.lineEdit_13, self.lineEdit_15)
        QWidget.setTabOrder(self.lineEdit_15, self.lineEdit_17)
        QWidget.setTabOrder(self.lineEdit_17, self.lineEdit_19)
        QWidget.setTabOrder(self.lineEdit_19, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.lineEdit_6)
        QWidget.setTabOrder(self.lineEdit_6, self.lineEdit_8)
        QWidget.setTabOrder(self.lineEdit_8, self.lineEdit_10)
        QWidget.setTabOrder(self.lineEdit_10, self.lineEdit_12)
        QWidget.setTabOrder(self.lineEdit_12, self.lineEdit_14)
        QWidget.setTabOrder(self.lineEdit_14, self.lineEdit_16)
        QWidget.setTabOrder(self.lineEdit_16, self.lineEdit_18)
        QWidget.setTabOrder(self.lineEdit_18, self.lineEdit_20)

        self.retranslateUi(formInventar)

        QMetaObject.connectSlotsByName(formInventar)
    # setupUi

    def retranslateUi(self, formInventar):
        formInventar.setWindowTitle(QCoreApplication.translate("formInventar", u"Form", None))
        self.gbRstungen.setTitle(QCoreApplication.translate("formInventar", u"R\u00fcstungen", None))
        self.gbRstungen.setProperty("class", QCoreApplication.translate("formInventar", u"h3", None))
        self.removeR3.setText(QCoreApplication.translate("formInventar", u"-", None))
        self.removeR3.setProperty("class", QCoreApplication.translate("formInventar", u"iconSmall", None))
#if QT_CONFIG(tooltip)
        self.editR3name.setToolTip(QCoreApplication.translate("formInventar", u"Nur die erste R\u00fcstung wird zur Berechnung der WS* usw. verwendet.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.labelRS.setToolTip(QCoreApplication.translate("formInventar", u"R\u00fcstungsschutz", None))
#endif // QT_CONFIG(tooltip)
        self.labelRS.setText(QCoreApplication.translate("formInventar", u"RS", None))
        self.labelRS.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.labelRName.setText(QCoreApplication.translate("formInventar", u"Name", None))
        self.labelRName.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.addR3.setText(QCoreApplication.translate("formInventar", u"+", None))
        self.addR3.setProperty("class", QCoreApplication.translate("formInventar", u"iconSmall", None))
        self.labelBrust.setText(QCoreApplication.translate("formInventar", u"Brust", None))
        self.labelBrust.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
#if QT_CONFIG(tooltip)
        self.labelBE.setToolTip(QCoreApplication.translate("formInventar", u"Behinderung", None))
#endif // QT_CONFIG(tooltip)
        self.labelBE.setText(QCoreApplication.translate("formInventar", u"BE", None))
        self.labelBE.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.labelBauch.setText(QCoreApplication.translate("formInventar", u"Bauch", None))
        self.labelBauch.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.labelRarm.setText(QCoreApplication.translate("formInventar", u"R. Arm", None))
        self.labelRarm.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.labelBein.setText(QCoreApplication.translate("formInventar", u"Bein", None))
        self.labelBein.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.labelLarm.setText(QCoreApplication.translate("formInventar", u"L. Arm", None))
        self.labelLarm.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
#if QT_CONFIG(tooltip)
        self.editR1name.setToolTip(QCoreApplication.translate("formInventar", u"Nur die erste R\u00fcstung wird zur Berechnung der WS* usw. verwendet.", None))
#endif // QT_CONFIG(tooltip)
        self.labelKopf.setText(QCoreApplication.translate("formInventar", u"Kopf", None))
        self.labelKopf.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.addR1.setText(QCoreApplication.translate("formInventar", u"+", None))
        self.addR1.setProperty("class", QCoreApplication.translate("formInventar", u"iconSmall", None))
#if QT_CONFIG(tooltip)
        self.editR2name.setToolTip(QCoreApplication.translate("formInventar", u"Nur die erste R\u00fcstung wird zur Berechnung der WS* usw. verwendet.", None))
#endif // QT_CONFIG(tooltip)
        self.removeR2.setText(QCoreApplication.translate("formInventar", u"-", None))
        self.removeR2.setProperty("class", QCoreApplication.translate("formInventar", u"iconSmall", None))
        self.addR2.setText(QCoreApplication.translate("formInventar", u"+", None))
        self.addR2.setProperty("class", QCoreApplication.translate("formInventar", u"iconSmall", None))
        self.removeR1.setText(QCoreApplication.translate("formInventar", u"-", None))
        self.removeR1.setProperty("class", QCoreApplication.translate("formInventar", u"iconSmall", None))
        self.labelPunkte.setText(QCoreApplication.translate("formInventar", u"Punkte", None))
        self.labelPunkte.setProperty("class", QCoreApplication.translate("formInventar", u"h4", None))
        self.checkZonen.setText(QCoreApplication.translate("formInventar", u"Zonenr\u00fcstungssystem benutzen", None))
        self.gbInventar.setTitle(QCoreApplication.translate("formInventar", u"Inventar", None))
        self.gbInventar.setProperty("class", QCoreApplication.translate("formInventar", u"h3", None))
        self.lineEdit_1.setText("")
    # retranslateUi

