from PySide6 import QtWidgets, QtCore, QtGui

# This dialog can disable cancel functionality or keep the window open until the calling code acts upon it
class ProgressDialogExt(QtWidgets.QProgressDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cancelPlease = False
        self.cb = self.findChild(QtWidgets.QPushButton)
        self.cb.setText("Abbrechen")
        self.canceled.disconnect(self.cancel)
        self.canceled.connect(self.cancelPlease)
        self.setMinimumWidth(400)
        self.setMinimumHeight(100)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setValue(0)

    def closeEvent(self, event):
        if event.spontaneous():
            event.ignore()
            self.cancelPlease()
            
    def cancelPlease(self):
        if self.cb is not None:
            self.__cancelPlease = True
            self.cb.setEnabled(False)
            self.setLabelText("Abbrechen...")

    def shouldCancel(self):
        return self.__cancelPlease

    def disableCancel(self):
        self.cb = None
        self.setCancelButton(None)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint);