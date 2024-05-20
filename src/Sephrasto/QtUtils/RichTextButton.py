from PySide6 import QtCore, QtWidgets, QtGui

# Based on https://stackoverflow.com/questions/2990060/qt-qpushbutton-text-formatting
class RichTextPushButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.__rtLabel = QtWidgets.QLabel(self)
        if text is not None:
            self.__rtLabel.setText(text)
        self.__rtLayout = QtWidgets.QHBoxLayout()
        self.__rtLayout.setContentsMargins(0, 0, 0, 0)
        self.__rtLayout.setSpacing(0)
        self.setLayout(self.__rtLayout)
        self.__rtLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.__rtLabel.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.__rtLabel.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.__rtLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.__rtLabel.setTextFormat(QtCore.Qt.RichText)
        self.__rtLayout.addWidget(self.__rtLabel)

    def setText(self, text):
        self.__rtLabel.setText("&nbsp;&nbsp;" + text + "&nbsp;&nbsp;") # quickndirty
        self.updateGeometry()

    def text(self):
        return self.__rtLabel.text()[12:-12] if self.__rtLabel.text() else ""

    def sizeHint(self):
        s = super().sizeHint()
        w = self.__rtLabel.sizeHint()
        s.setWidth(max(s.width(), w.width()))
        s.setHeight(max(s.height(),w.height()))
        return s

class RichTextToolButton(QtWidgets.QToolButton):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.__rtLabel = QtWidgets.QLabel(self)
        if text is not None:
            self.__rtLabel.setText(text)
        self.__rtLayout = QtWidgets.QHBoxLayout()
        self.__rtLayout.setContentsMargins(0, 0, 0, 0)
        self.__rtLayout.setSpacing(0)
        self.setLayout(self.__rtLayout)
        self.__rtLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.__rtLabel.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.__rtLabel.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.__rtLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.__rtLabel.setTextFormat(QtCore.Qt.RichText)
        self.__rtLayout.addWidget(self.__rtLabel)

    def setText(self, text):
        self.__rtLabel.setText("&nbsp;&nbsp;" + text + "&nbsp;&nbsp;&nbsp;&nbsp;") # quickndirty, add more at the end for arrow button margin
        self.updateGeometry()

    def text(self):
        return self.__rtLabel.text()[12:-24] if self.__rtLabel.text() else ""

    def sizeHint(self):
        s = super().sizeHint()
        w = self.__rtLabel.sizeHint()
        s.setWidth(max(s.width(), w.width()))
        s.setHeight(max(s.height(), w.height()))
        return s