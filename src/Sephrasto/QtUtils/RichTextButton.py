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
        self.__rtLabel.setText(text)
        self.updateGeometry()

    def text(self):
        return self.__rtLabel.text()

    def sizeHint(self):
        # reimplement QPushButton's sizeHint but use our label size

        self.ensurePolished()
        w = 0
        h = 0

        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)

        showButtonBoxIcons = False
        if isinstance(self.parentWidget(), QtWidgets.QDialogButtonBox):
            showButtonBoxIcons = self.style().styleHint(QtWidgets.QStyle.SH_DialogButtonBox_ButtonsHaveIcons)

        if not self.icon().isNull() or showButtonBoxIcons:
            ih = opt.iconSize.height()
            iw = opt.iconSize.width() + 4
            w += iw
            h = max(h, ih)

        textSize = self.__rtLabel.sizeHint()
        textSize.setWidth(textSize.width() + self.fontMetrics().horizontalAdvance(u' ') * 2)
        if not self.text() or not w:
            w += textSize.width()
        if not self.text() or not h:
            h = max(h, textSize.height())
        opt.rect.setSize(QtCore.QSize(w, h))

        if self.menu():
            w += self.style().pixelMetric(QtWidgets.QStyle.PM_MenuButtonIndicator, opt, self)

        return self.style().sizeFromContents(QtWidgets.QStyle.CT_PushButton, opt, QtCore.QSize(w, h), self)

class RichTextToolButton(QtWidgets.QToolButton):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
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
        self.__rtLabel.setText(text)
        self.updateGeometry()
    
    def text(self):
        return self.__rtLabel.text()

    def setPopupMode(self, mode):
        super().setPopupMode(mode)
        if mode == QtWidgets.QToolButton.InstantPopup:
            fm = self.fontMetrics()
            self.__rtLayout.setContentsMargins(0, 0, fm.horizontalAdvance(u' ') * 2, 0)
        elif mode == QtWidgets.QToolButton.MenuButtonPopup:
            opt = QtWidgets.QStyleOptionToolButton()
            self.initStyleOption(opt)
            self.__rtLayout.setContentsMargins(0, 0, self.style().pixelMetric(QtWidgets.QStyle.PM_MenuButtonIndicator, opt, self), 0)
        else:
            self.__rtLayout.setContentsMargins(0, 0, 0, 0)

    def sizeHint(self):
        # reimplement QToolButton's sizeHint but use our label size
        self.ensurePolished()

        opt = QtWidgets.QStyleOptionToolButton()
        self.initStyleOption(opt)
        w = 0
        h = 0

        if opt.toolButtonStyle != QtCore.Qt.ToolButtonTextOnly:
            icon = opt.iconSize
            w = icon.width()
            h = icon.height()

        if opt.toolButtonStyle != QtCore.Qt.ToolButtonIconOnly:
            textSize = self.__rtLabel.sizeHint()
            textSize.setWidth(textSize.width() + self.fontMetrics().horizontalAdvance(u' ') * 2)
            if opt.toolButtonStyle == QtCore.Qt.ToolButtonTextUnderIcon:
                h += 4 + textSize.height()
                if textSize.width() > w:
                    w = textSize.width();
            elif opt.toolButtonStyle == QtCore.Qt.ToolButtonTextBesideIcon:
                w += 4 + textSize.width()
                if textSize.height() > h:
                    h = textSize.height()
            else:
                w = textSize.width();
                h = textSize.height();

        opt.rect.setSize(QtCore.QSize(w, h))
        if self.popupMode() == QtWidgets.QToolButton.MenuButtonPopup:
            w += self.style().pixelMetric(QtWidgets.QStyle.PM_MenuButtonIndicator, opt, self)

        toolSize = self.style().sizeFromContents(QtWidgets.QStyle.CT_ToolButton, opt, QtCore.QSize(w, h), self)

        # Also calculate hypothetical size as push button to make sure they match
        opt2 = QtWidgets.QStyleOptionButton()
        opt2.direction = opt.direction
        if opt.features & QtWidgets.QStyleOptionToolButton.Menu:
            opt2.features |= QtWidgets.QStyleOptionButton.HasMenu
        opt2.fontMetrics = opt.fontMetrics
        opt2.icon = opt.icon
        opt2.iconSize = opt.iconSize
        opt2.palette = opt.palette
        opt2.rect = opt.rect
        opt2.state = opt.state
        opt2.styleObject = opt.styleObject
        opt2.text = opt.text
        pushSize = self.style().sizeFromContents(QtWidgets.QStyle.CT_PushButton, opt2, QtCore.QSize(w, h), self)
        
        return toolSize.expandedTo(pushSize)