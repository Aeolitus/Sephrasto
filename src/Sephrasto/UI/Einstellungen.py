# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Einstellungen.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.setWindowModality(Qt.ApplicationModal)
        SettingsWindow.resize(589, 844)
        SettingsWindow.setMinimumSize(QSize(520, 0))
        self.gridLayout = QGridLayout(SettingsWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.buttonBox = QDialogButtonBox(SettingsWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.scrollArea = QScrollArea(SettingsWindow)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 605, 800))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setBold(False)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setItalic(False)
        self.label.setFont(font1)

        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 1)

        self.comboBogen = QComboBox(self.groupBox)
        self.comboBogen.setObjectName(u"comboBogen")
        self.comboBogen.setMinimumSize(QSize(240, 0))

        self.gridLayout_3.addWidget(self.comboBogen, 4, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.gridLayout_3.addWidget(self.label_6, 9, 0, 1, 1)

        self.comboRegelbasis = QComboBox(self.groupBox)
        self.comboRegelbasis.addItem("")
        self.comboRegelbasis.setObjectName(u"comboRegelbasis")
        self.comboRegelbasis.setMinimumSize(QSize(240, 0))

        self.gridLayout_3.addWidget(self.comboRegelbasis, 2, 2, 1, 1)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_3.addWidget(self.label_16, 8, 0, 1, 1)

        self.checkWizard = QCheckBox(self.groupBox)
        self.checkWizard.setObjectName(u"checkWizard")
        self.checkWizard.setChecked(True)

        self.gridLayout_3.addWidget(self.checkWizard, 1, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)

        self.comboFontSize = QComboBox(self.groupBox)
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.setObjectName(u"comboFontSize")
        self.comboFontSize.setMinimumSize(QSize(240, 0))

        self.gridLayout_3.addWidget(self.comboFontSize, 9, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 2, 1, 1, 1)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_3.addWidget(self.label_17, 1, 0, 1, 1)

        self.checkCheatsheet = QCheckBox(self.groupBox)
        self.checkCheatsheet.setObjectName(u"checkCheatsheet")
        self.checkCheatsheet.setChecked(True)

        self.gridLayout_3.addWidget(self.checkCheatsheet, 8, 2, 1, 1)

        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_3.addWidget(self.label_19, 10, 0, 1, 1)

        self.comboFormular = QComboBox(self.groupBox)
        self.comboFormular.addItem("")
        self.comboFormular.addItem("")
        self.comboFormular.addItem("")
        self.comboFormular.setObjectName(u"comboFormular")

        self.gridLayout_3.addWidget(self.comboFormular, 10, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(70, 0))

        self.gridLayout_5.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(70, 0))

        self.gridLayout_5.addWidget(self.label_3, 2, 0, 1, 1)

        self.buttonPlugins = QPushButton(self.groupBox_2)
        self.buttonPlugins.setObjectName(u"buttonPlugins")
        self.buttonPlugins.setMinimumSize(QSize(28, 28))
        self.buttonPlugins.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.buttonPlugins, 3, 2, 1, 1)

        self.resetPlugins = QPushButton(self.groupBox_2)
        self.resetPlugins.setObjectName(u"resetPlugins")
        self.resetPlugins.setMinimumSize(QSize(28, 28))
        self.resetPlugins.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.resetPlugins, 3, 3, 1, 1)

        self.resetChar = QPushButton(self.groupBox_2)
        self.resetChar.setObjectName(u"resetChar")
        self.resetChar.setMinimumSize(QSize(28, 28))
        self.resetChar.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.resetChar, 0, 3, 1, 1)

        self.editRegeln = QLineEdit(self.groupBox_2)
        self.editRegeln.setObjectName(u"editRegeln")

        self.gridLayout_5.addWidget(self.editRegeln, 2, 1, 1, 1)

        self.editChar = QLineEdit(self.groupBox_2)
        self.editChar.setObjectName(u"editChar")
        self.editChar.setReadOnly(False)
        self.editChar.setClearButtonEnabled(False)

        self.gridLayout_5.addWidget(self.editChar, 0, 1, 1, 1)

        self.resetRegeln = QPushButton(self.groupBox_2)
        self.resetRegeln.setObjectName(u"resetRegeln")
        self.resetRegeln.setMinimumSize(QSize(28, 28))
        self.resetRegeln.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.resetRegeln, 2, 3, 1, 1)

        self.buttonRegeln = QPushButton(self.groupBox_2)
        self.buttonRegeln.setObjectName(u"buttonRegeln")
        self.buttonRegeln.setMinimumSize(QSize(28, 28))
        self.buttonRegeln.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.buttonRegeln, 2, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(70, 0))

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)

        self.editPlugins = QLineEdit(self.groupBox_2)
        self.editPlugins.setObjectName(u"editPlugins")

        self.gridLayout_5.addWidget(self.editPlugins, 3, 1, 1, 1)

        self.buttonChar = QPushButton(self.groupBox_2)
        self.buttonChar.setObjectName(u"buttonChar")
        self.buttonChar.setMinimumSize(QSize(28, 28))
        self.buttonChar.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.buttonChar, 0, 2, 1, 1)

        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_5.addWidget(self.label_18, 4, 0, 1, 1)

        self.editCharakterboegen = QLineEdit(self.groupBox_2)
        self.editCharakterboegen.setObjectName(u"editCharakterboegen")

        self.gridLayout_5.addWidget(self.editCharakterboegen, 4, 1, 1, 1)

        self.buttonCharakterboegen = QPushButton(self.groupBox_2)
        self.buttonCharakterboegen.setObjectName(u"buttonCharakterboegen")
        self.buttonCharakterboegen.setMinimumSize(QSize(28, 28))
        self.buttonCharakterboegen.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.buttonCharakterboegen, 4, 2, 1, 1)

        self.resetCharakterboegen = QPushButton(self.groupBox_2)
        self.resetCharakterboegen.setObjectName(u"resetCharakterboegen")
        self.resetCharakterboegen.setMinimumSize(QSize(28, 28))
        self.resetCharakterboegen.setMaximumSize(QSize(28, 28))

        self.gridLayout_5.addWidget(self.resetCharakterboegen, 4, 3, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.gbPlugins = QGroupBox(self.scrollAreaWidgetContents)
        self.gbPlugins.setObjectName(u"gbPlugins")
        self.verticalLayout_10 = QVBoxLayout(self.gbPlugins)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")

        self.verticalLayout.addWidget(self.gbPlugins)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.comboFont = QComboBox(self.groupBox_4)
        self.comboFont.setObjectName(u"comboFont")
        self.comboFont.setMinimumSize(QSize(240, 0))

        self.gridLayout_2.addWidget(self.comboFont, 2, 2, 1, 1)

        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 8, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)

        self.comboFontHeading = QComboBox(self.groupBox_4)
        self.comboFontHeading.setObjectName(u"comboFontHeading")
        self.comboFontHeading.setMinimumSize(QSize(240, 0))

        self.gridLayout_2.addWidget(self.comboFontHeading, 5, 2, 1, 1)

        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 7, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 5, 0, 1, 1)

        self.checkDPI = QCheckBox(self.groupBox_4)
        self.checkDPI.setObjectName(u"checkDPI")

        self.gridLayout_2.addWidget(self.checkDPI, 8, 2, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboTheme = QComboBox(self.groupBox_4)
        self.comboTheme.setObjectName(u"comboTheme")
        self.comboTheme.setMinimumSize(QSize(240, 0))

        self.horizontalLayout_2.addWidget(self.comboTheme)

        self.resetFontOS = QPushButton(self.groupBox_4)
        self.resetFontOS.setObjectName(u"resetFontOS")
        self.resetFontOS.setMinimumSize(QSize(28, 28))
        self.resetFontOS.setMaximumSize(QSize(28, 28))

        self.horizontalLayout_2.addWidget(self.resetFontOS)

        self.resetFontDefault = QPushButton(self.groupBox_4)
        self.resetFontDefault.setObjectName(u"resetFontDefault")
        self.resetFontDefault.setMinimumSize(QSize(28, 28))
        self.resetFontDefault.setMaximumSize(QSize(28, 28))

        self.horizontalLayout_2.addWidget(self.resetFontDefault)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 5, 1, 1, 1)

        self.spinAppFontSize = QSpinBox(self.groupBox_4)
        self.spinAppFontSize.setObjectName(u"spinAppFontSize")
        self.spinAppFontSize.setMinimumSize(QSize(60, 0))
        self.spinAppFontSize.setMaximumSize(QSize(60, 16777215))
        self.spinAppFontSize.setLayoutDirection(Qt.LeftToRight)
        self.spinAppFontSize.setAlignment(Qt.AlignCenter)
        self.spinAppFontSize.setMinimum(6)
        self.spinAppFontSize.setMaximum(18)
        self.spinAppFontSize.setValue(8)

        self.gridLayout_2.addWidget(self.spinAppFontSize, 3, 2, 1, 1)

        self.spinAppFontHeadingSize = QSpinBox(self.groupBox_4)
        self.spinAppFontHeadingSize.setObjectName(u"spinAppFontHeadingSize")
        self.spinAppFontHeadingSize.setMinimumSize(QSize(60, 0))
        self.spinAppFontHeadingSize.setMaximumSize(QSize(60, 16777215))
        self.spinAppFontHeadingSize.setLayoutDirection(Qt.LeftToRight)
        self.spinAppFontHeadingSize.setAlignment(Qt.AlignCenter)
        self.spinAppFontHeadingSize.setMinimum(6)
        self.spinAppFontHeadingSize.setMaximum(18)
        self.spinAppFontHeadingSize.setValue(10)

        self.gridLayout_2.addWidget(self.spinAppFontHeadingSize, 7, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_4 = QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 3, 0, 1, 1)

        self.checkUpdate = QCheckBox(self.groupBox_5)
        self.checkUpdate.setObjectName(u"checkUpdate")
        self.checkUpdate.setChecked(True)

        self.gridLayout_4.addWidget(self.checkUpdate, 2, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 4, 0, 1, 1)

        self.checkPDFOpen = QCheckBox(self.groupBox_5)
        self.checkPDFOpen.setObjectName(u"checkPDFOpen")
        self.checkPDFOpen.setChecked(True)

        self.gridLayout_4.addWidget(self.checkPDFOpen, 3, 2, 1, 1)

        self.comboLogging = QComboBox(self.groupBox_5)
        self.comboLogging.addItem("")
        self.comboLogging.addItem("")
        self.comboLogging.addItem("")
        self.comboLogging.setObjectName(u"comboLogging")
        self.comboLogging.setMinimumSize(QSize(240, 0))

        self.gridLayout_4.addWidget(self.comboLogging, 4, 2, 1, 1)

        self.label_14 = QLabel(self.groupBox_5)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_4.addWidget(self.label_14, 2, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.scrollArea, self.comboRegelbasis)
        QWidget.setTabOrder(self.comboRegelbasis, self.comboBogen)
        QWidget.setTabOrder(self.comboBogen, self.comboFontSize)
        QWidget.setTabOrder(self.comboFontSize, self.editChar)
        QWidget.setTabOrder(self.editChar, self.buttonChar)
        QWidget.setTabOrder(self.buttonChar, self.resetChar)
        QWidget.setTabOrder(self.resetChar, self.editRegeln)
        QWidget.setTabOrder(self.editRegeln, self.buttonRegeln)
        QWidget.setTabOrder(self.buttonRegeln, self.resetRegeln)
        QWidget.setTabOrder(self.resetRegeln, self.editPlugins)
        QWidget.setTabOrder(self.editPlugins, self.buttonPlugins)
        QWidget.setTabOrder(self.buttonPlugins, self.resetPlugins)
        QWidget.setTabOrder(self.resetPlugins, self.comboFont)
        QWidget.setTabOrder(self.comboFont, self.comboFontHeading)
        QWidget.setTabOrder(self.comboFontHeading, self.comboLogging)

        self.retranslateUi(SettingsWindow)
        self.buttonBox.accepted.connect(SettingsWindow.accept)
        self.buttonBox.rejected.connect(SettingsWindow.reject)

        self.comboLogging.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"Sephrasto - Einstellungen", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsWindow", u"Standard-Einstellungen f\u00fcr neue Charaktere", None))
        self.label.setText(QCoreApplication.translate("SettingsWindow", u"Verwendeter Charakterbogen", None))
#if QT_CONFIG(tooltip)
        self.comboBogen.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Hier erscheinen alle Charakterb\u00f6gen, die mit Sephrasto geliefert werden sowie alle aus deinem Charakterbogen-Pfad, siehe unten. Der gew\u00e4hlte Charakterbogen wird bei neuen Charakteren automatisch aktiv gesetzt. Dies kannst du nachtr\u00e4glich im Info-Tab des Charaktereditors \u00e4ndern.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("SettingsWindow", u"Regeln Schriftgr\u00f6\u00dfe", None))
        self.comboRegelbasis.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Keine", None))

#if QT_CONFIG(tooltip)
        self.comboRegelbasis.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Hier erscheinen alle Hausregeldatenbanken in deinem Regel-Pfad, siehe unten. Die gew\u00e4hlten Hausregeln werden bei neuen Charakteren automatisch aktiv gesetzt. Dies kannst du nachtr\u00e4glich im Info-Tab des Charaktereditors \u00e4ndern.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_16.setText(QCoreApplication.translate("SettingsWindow", u"Dem Charakterbogen Ilaris Regeln anh\u00e4ngen", None))
#if QT_CONFIG(tooltip)
        self.checkWizard.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Der Charakter Assistent erscheint beim Erstellen eines neuen Charakters und beschleunigt die Erstellung durch Schablonen f\u00fcr Spezies, Kultur und Profession.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkWizard.setText("")
        self.label_4.setText(QCoreApplication.translate("SettingsWindow", u"Hausregeln", None))
        self.comboFontSize.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Klein", None))
        self.comboFontSize.setItemText(1, QCoreApplication.translate("SettingsWindow", u"Mittel", None))
        self.comboFontSize.setItemText(2, QCoreApplication.translate("SettingsWindow", u"Gro\u00df", None))

        self.label_17.setText(QCoreApplication.translate("SettingsWindow", u"Charakter Assistent nutzen", None))
#if QT_CONFIG(tooltip)
        self.checkCheatsheet.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Sephrasto kann automatisch alle Regeln, die f\u00fcr deinen Charakter relevant sind, zusammentragen und deiner PDF hinten anf\u00fcgen. Diese Einstellung gilt f\u00fcr neue Charaktere. Du kannst sie nachtr\u00e4glich im Info-Tab des Charaktereditors \u00e4ndern.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkCheatsheet.setText("")
        self.label_19.setText(QCoreApplication.translate("SettingsWindow", u"Formularfelder", None))
        self.comboFormular.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Charakterbogen & Regelanhang editierbar", None))
        self.comboFormular.setItemText(1, QCoreApplication.translate("SettingsWindow", u"Nur Charakterbogen editierbar", None))
        self.comboFormular.setItemText(2, QCoreApplication.translate("SettingsWindow", u"Nicht editierbar", None))

#if QT_CONFIG(tooltip)
        self.comboFormular.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Manche PDF-Reader k\u00f6nnen Formularfelder in PDF-Dokumenten nicht durchsuchen oder machen beispielsweise Probleme beim Regelanhang wegen der automatischen Schriftgr\u00f6\u00dfe. Die Formularfelder erh\u00f6hen die Dateigr\u00f6\u00dfe au\u00dferdem rund 10%. Mit dieser Option kannst du diese in reine Textfelder umwandeln. Sie sind dann allerdings nicht mehr editierbar. Diese Einstellung gilt f\u00fcr neue Charaktere. Du kannst sie nachtr\u00e4glich im Info-Tab des Charaktereditors \u00e4ndern.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsWindow", u"Speicherpfade", None))
        self.label_7.setText(QCoreApplication.translate("SettingsWindow", u"Plugins", None))
        self.label_3.setText(QCoreApplication.translate("SettingsWindow", u"Regeln", None))
#if QT_CONFIG(tooltip)
        self.buttonPlugins.setToolTip(QCoreApplication.translate("SettingsWindow", u"Ordner suchen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonPlugins.setText(QCoreApplication.translate("SettingsWindow", u"Durchsuchen", None))
        self.buttonPlugins.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
#if QT_CONFIG(tooltip)
        self.resetPlugins.setToolTip(QCoreApplication.translate("SettingsWindow", u"Auf den Standardordner zur\u00fccksetzen", None))
#endif // QT_CONFIG(tooltip)
        self.resetPlugins.setText(QCoreApplication.translate("SettingsWindow", u"Zur\u00fccksetzen", None))
        self.resetPlugins.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
#if QT_CONFIG(tooltip)
        self.resetChar.setToolTip(QCoreApplication.translate("SettingsWindow", u"Auf den Standardordner zur\u00fccksetzen", None))
#endif // QT_CONFIG(tooltip)
        self.resetChar.setText(QCoreApplication.translate("SettingsWindow", u"Zur\u00fccksetzen", None))
        self.resetChar.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
#if QT_CONFIG(tooltip)
        self.resetRegeln.setToolTip(QCoreApplication.translate("SettingsWindow", u"Auf den Standardordner zur\u00fccksetzen", None))
#endif // QT_CONFIG(tooltip)
        self.resetRegeln.setText(QCoreApplication.translate("SettingsWindow", u"Zur\u00fccksetzen", None))
        self.resetRegeln.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
#if QT_CONFIG(tooltip)
        self.buttonRegeln.setToolTip(QCoreApplication.translate("SettingsWindow", u"Ordner suchen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonRegeln.setText(QCoreApplication.translate("SettingsWindow", u"Durchsuchen", None))
        self.buttonRegeln.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
        self.label_2.setText(QCoreApplication.translate("SettingsWindow", u"Charaktere", None))
#if QT_CONFIG(tooltip)
        self.buttonChar.setToolTip(QCoreApplication.translate("SettingsWindow", u"Ordner suchen", None))
#endif // QT_CONFIG(tooltip)
        self.buttonChar.setText(QCoreApplication.translate("SettingsWindow", u"Durchsuchen", None))
        self.buttonChar.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
        self.label_18.setText(QCoreApplication.translate("SettingsWindow", u"Charakterb\u00f6gen", None))
        self.buttonCharakterboegen.setText(QCoreApplication.translate("SettingsWindow", u"Durchsuchen", None))
        self.buttonCharakterboegen.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
        self.resetCharakterboegen.setText(QCoreApplication.translate("SettingsWindow", u"Zur\u00fccksetzen", None))
        self.resetCharakterboegen.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
        self.gbPlugins.setTitle(QCoreApplication.translate("SettingsWindow", u"Plugins", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("SettingsWindow", u"Darstellung", None))
        self.label_9.setText(QCoreApplication.translate("SettingsWindow", u"Schriftart", None))
        self.label_13.setText(QCoreApplication.translate("SettingsWindow", u"DPI-Skalierung", None))
        self.label_10.setText(QCoreApplication.translate("SettingsWindow", u"Schriftgr\u00f6\u00dfe", None))
        self.label_12.setText(QCoreApplication.translate("SettingsWindow", u"Schriftgr\u00f6\u00dfe \u00dcberschriften", None))
        self.label_8.setText(QCoreApplication.translate("SettingsWindow", u"Theme", None))
        self.label_11.setText(QCoreApplication.translate("SettingsWindow", u"Schriftart \u00dcberschriften", None))
#if QT_CONFIG(tooltip)
        self.checkDPI.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Viele Betriebssysteme bieten an, Programme, Schriften usw. gr\u00f6\u00dfer darzustellen. Sephrasto kann diese sogenannte DPI-Skalierung vom Betriebssystem \u00fcbernehmen. Dabei kann es aktuell allerdings noch zu Darstellungsfehlern wie niedrigaufgel\u00f6sten Bildern oder Icons kommen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkDPI.setText("")
#if QT_CONFIG(tooltip)
        self.resetFontOS.setToolTip(QCoreApplication.translate("SettingsWindow", u"Darstellungsoptionen auf Betriebssystemstandard zur\u00fccksetzen", None))
#endif // QT_CONFIG(tooltip)
        self.resetFontOS.setText(QCoreApplication.translate("SettingsWindow", u"OS", None))
        self.resetFontOS.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
#if QT_CONFIG(tooltip)
        self.resetFontDefault.setToolTip(QCoreApplication.translate("SettingsWindow", u"Darstellungsoptionen auf Sephrastostandard zur\u00fccksetzen", None))
#endif // QT_CONFIG(tooltip)
        self.resetFontDefault.setText(QCoreApplication.translate("SettingsWindow", u"Zur\u00fccksetzen", None))
        self.resetFontDefault.setProperty("class", QCoreApplication.translate("SettingsWindow", u"icon", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("SettingsWindow", u"Sonstiges", None))
        self.label_15.setText(QCoreApplication.translate("SettingsWindow", u"Charakterbogen nach dem Erstellen \u00f6ffnen", None))
#if QT_CONFIG(tooltip)
        self.checkUpdate.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Falls aktiviert sendet Sephrasto bei jedem Start eine Anfrage an dsaforum.de, um nachzusehen, ob es eine neuere Version gibt.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkUpdate.setText("")
        self.label_5.setText(QCoreApplication.translate("SettingsWindow", u"Logging-Level", None))
        self.checkPDFOpen.setText("")
        self.comboLogging.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Nur Fehler", None))
        self.comboLogging.setItemText(1, QCoreApplication.translate("SettingsWindow", u"Warnungen und Fehler", None))
        self.comboLogging.setItemText(2, QCoreApplication.translate("SettingsWindow", u"Debug-Informationen", None))

        self.label_14.setText(QCoreApplication.translate("SettingsWindow", u"Beim Start nach Updates suchen", None))
    # retranslateUi

