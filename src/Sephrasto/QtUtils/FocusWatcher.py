from PySide6 import QtWidgets, QtCore, QtGui

# This class notifies you, when a widget loses focus
# Usage: Call the "installEventFilter" function of the widget you want to watch and pass a FocusWatcher instance
class FocusWatcher(QtCore.QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obje, even):
        if type(even) == QtGui.QFocusEvent:
            if not obje.hasFocus():
                self.callback()
        return False