# Adapted from Violet Giraffes answer at
# https://stackoverflow.com/questions/5821802/qspinbox-inside-a-qscrollarea-how-to-prevent-spin-box-from-stealing-focus-when
from PyQt5 import QtWidgets, QtCore, QtGui


class MousewheelProtector(QtCore.QObject):

    def eventFilter(self, obje, even):
        if type(even) == QtGui.QWheelEvent:
            if type(obje) == QtWidgets.QSpinBox:
                if not obje.hasFocus():
                    even.ignore()
                    return True
        try:
            return obje.eventFilter(obje, even)
        except:
            return False
