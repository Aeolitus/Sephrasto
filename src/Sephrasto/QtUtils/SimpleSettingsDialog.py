from PySide6 import QtWidgets, QtCore, QtGui
from Wolke import Wolke

# This dialog shall make it easier for plugins to provide their own settings
class SimpleSettingsDialog(QtWidgets.QDialog):
    def __init__(self, title, parent = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        rootLayout = QtWidgets.QVBoxLayout()

        self.settings = {}
        self.settingsLayout = QtWidgets.QFormLayout()
        rootLayout.addLayout(self.settingsLayout)
        
        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.addButton("OK", QtWidgets.QDialogButtonBox.YesRole).clicked.connect(lambda: self.accept())
        buttonBox.addButton("Abbrechen", QtWidgets.QDialogButtonBox.RejectRole).clicked.connect(lambda: self.reject())
        rootLayout.addWidget(buttonBox)

        self.setLayout(rootLayout)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    # The settingId will be used to initialize from and update to Wolke.Settings automatically
    # Supported widgets are QCheckBox, QComboBox, QSpinBox and QLineEdit
    # You may want to add not just a widget but a layout i.e. for also adding a file picker button
    # In this case you still need to provide the widget which contains the setting value
    def addSetting(self, settingId, settingText, settingWidget, layout = None):
        if layout:
            self.settingsLayout.addRow(settingText, layout)
        else:
            self.settingsLayout.addRow(settingText, settingWidget)
        self.settings[settingId] = settingWidget
        if isinstance(settingWidget, QtWidgets.QCheckBox):
            settingWidget.setChecked(Wolke.Settings[settingId])
        elif isinstance(settingWidget, QtWidgets.QComboBox):
            settingWidget.setCurrentText(Wolke.Settings[settingId])
        elif isinstance(settingWidget, QtWidgets.QSpinBox):
            settingWidget.setValue(Wolke.Settings[settingId])
        elif isinstance(settingWidget, QtWidgets.QLineEdit):
            settingWidget.setText(Wolke.Settings[settingId])

    def show(self):
        super().show()
        result = self.exec()
        if result == QtWidgets.QDialog.Accepted:
            for settingId, settingWidget in self.settings.items():
                if isinstance(settingWidget, QtWidgets.QCheckBox):
                    Wolke.Settings[settingId] = settingWidget.isChecked()
                elif isinstance(settingWidget, QtWidgets.QComboBox):
                    Wolke.Settings[settingId] = settingWidget.currentText()
                elif isinstance(settingWidget, QtWidgets.QSpinBox):
                    Wolke.Settings[settingId] = settingWidget.value()
                elif isinstance(settingWidget, QtWidgets.QLineEdit):
                    Wolke.Settings[settingId] = settingWidget.text()