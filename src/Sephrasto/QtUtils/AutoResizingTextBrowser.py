from PySide6 import QtWidgets, QtCore, QtGui

class AutoResizingTextBrowser(QtWidgets.QTextBrowser):
    sizeChanged = QtCore.Signal(float, float)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def setText(self, text):
        super().setText(text)
        self.fitToContent()

    def fitToContent(self):
        margins = self.contentsMargins()
        width = self.size().width() - margins.left() - margins.right() - self.document().documentMargin()*2
        self.document().setPageSize(QtCore.QSizeF(width, -1))
        height = self.document().size().height() + margins.top() + margins.bottom()
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.sizeChanged.emit(width, height)

    def showEvent(self, ev):
        self.fitToContent()

    def resizeEvent(self, ev):
        self.fitToContent()

# Use this helper instead, if you want to auto-resize text edit widgets created through Qt Creator
class TextEditAutoResizer:
    def __init__(self, textEdit):
        self.textEdit = textEdit
        textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        textEdit.showEvent = self.fitToContent
        textEdit.resizeEvent = self.fitToContent
        textEdit.textChanged.connect(self.fitToContent)

    def fitToContent(self, ev = None):
        margins = self.textEdit.contentsMargins()
        width = self.textEdit.size().width() - margins.left() - margins.right() - self.textEdit.document().documentMargin()*2
        self.textEdit.document().setPageSize(QtCore.QSizeF(width, -1))
        height = self.textEdit.document().size().height() + margins.top() + margins.bottom()
        self.textEdit.setMaximumHeight(height)
        self.textEdit.setMinimumHeight(height)