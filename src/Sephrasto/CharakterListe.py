from PySide6 import QtWidgets, QtCore, QtGui
import os
import Charakter
from functools import partial
from Hilfsmethoden import Hilfsmethoden
from Wolke import Wolke
import math
import base64

class CharWidget(QtWidgets.QAbstractButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(12, 6, 12, 6)
        self.iconLabel = QtWidgets.QLabel()
        self.iconLabel.setProperty("class", "charWidgetIcon")            
        self.iconLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.iconLabel)

        self.label = QtWidgets.QLabel()
        self.label.setProperty("class", "charWidgetLabel")
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setProperty("class", "charWidget")

        self.infoLabel = QtWidgets.QLabel(self)
        self.infoLabel.setProperty("class", "iconTiny")

    # Fore some reason this is needed to support style sheets in QWidget subclasses
    def paintEvent(self, pe):    
        o = QtWidgets.QStyleOption()
        o.initFrom(self)
        p = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, o, p, self)

    # Custom widgets dont support :pressed in css, so we do this ourselves via a property
    def mousePressEvent(self, event):
        self.setProperty("pressed", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setProperty("pressed", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().mouseReleaseEvent(event)

    # fishy but works for now: requires setFixedHeight to be called afterwards
    def setPixmap(self, pixmap):
        self.pixmap = pixmap

    def setIcon(self, icon):
        self.iconLabel.setText(icon)

    def setText(self, text):
        self.label.setText(text)

    def setToolTip(self, text):
        self.infoLabel.setText("\uf129")
        self.infoLabel.setToolTip(text)

    def setFixedHeight(self, height):
        super().setFixedHeight(height)
        margins = self.layout().contentsMargins()
        height = height - margins.top() - margins.bottom()
        width = height * (Wolke.CharImageSize[0]/Wolke.CharImageSize[1]) # aspect ratio of the char image
        self.iconLabel.setFixedSize(width, height)
        if hasattr(self, "pixmap"):
            self.iconLabel.setPixmap(self.pixmap.scaled(self.iconLabel.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        self.infoLabel.move(self.maximumWidth()-Hilfsmethoden.emToPixels(2), height-Hilfsmethoden.emToPixels(1.3))

class CharakterListe(QtWidgets.QWidget):
    createNew = QtCore.Signal()
    load = QtCore.Signal(str)

    def __init__(self, numCols, numRows, parent = None):
        super().__init__(parent)
        self.charWidgets = []
        self.layouts = []
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.numCols = numCols
        self.numRows = numRows

        wl = QtWidgets.QHBoxLayout()
        wl.setContentsMargins(0, 0, 0, 0)
        self.newCharWidget = CharWidget()
        self.newCharWidget.setText("<br><b>Neuer Charakter</b><br>")
        self.newCharWidget.setIcon("\u002b")
        self.newCharWidget.clicked.connect(self.emitCreateNew)
        wl.addWidget(self.newCharWidget)
        
        if numCols == 1:
            layout.addLayout(wl)
            wl = QtWidgets.QHBoxLayout()
            wl.setContentsMargins(0, 0, 0, 0)
        
        self.loadCharWidget = CharWidget()
        self.loadCharWidget.setText("<br><b>Charakter laden</b><br>")
        self.loadCharWidget.setIcon("\uf07c")
        self.loadCharWidget.clicked.connect(partial(self.emitLoad, path=""))
        wl.addWidget(self.loadCharWidget)
        
        layout.addLayout(wl)
        self.setLayout(layout)

        self.setProperty("class", "charListScrollArea")

    def emitCreateNew(self):
        self.createNew.emit()

    def emitLoad(self, path):
        self.load.emit(path)

    def update(self, chars):
        for w in self.charWidgets:
            w.setParent(None)
            w.deleteLater()
        self.charWidgets = []

        layout = self.layout()
        for i in reversed(range((2 if self.numCols == 1 else 1), layout.count())): 
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().setParent(None)
            else:
                layout.removeItem(layout.itemAt(i))

        wl = QtWidgets.QHBoxLayout()
        wl.setContentsMargins(0, 0, 0, 0)
        count = 0
        for char in chars:
            if not os.path.isfile(char["path"]):
                continue

            if count % self.numCols == 0 and (count / self.numCols) + 1 >= self.numRows:
                break

            charWidget = CharWidget()
            charWidget.setToolTip(char["path"])

            if "bild" in char:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(base64.b64decode(char["bild"]))
            else:
                pixmap = QtGui.QPixmap("Data/Images/default_avatar.png")
            charWidget.setPixmap(pixmap)

            text = "<b>" + char["name"] + "</b>"
            if char["hausregeln"] != "Keine":
                text += "<br>" + os.path.splitext(char["hausregeln"])[0]
            text += "<br>" + str(char["epGesamt"]) + " EP"
            charWidget.setText(text)
            charWidget.clicked.connect(partial(self.emitLoad, path=char["path"]))
            self.charWidgets.append(charWidget)
            wl.addWidget(charWidget)
            count += 1
            if count % self.numCols == 0:
                layout.addLayout(wl)
                wl = QtWidgets.QHBoxLayout()
                wl.setContentsMargins(0, 0, 0, 0)
        if count % self.numCols != 0:
            wl.addStretch()
            layout.addLayout(wl)

        allWidgets = self.charWidgets + [self.newCharWidget, self.loadCharWidget]
        maxHeight = 0
        for w in allWidgets:
            maxHeight = max(maxHeight, w.sizeHint().height())
        numRows = math.ceil((len(self.charWidgets)) / self.numCols) + (2 if self.numCols == 1 else 1)
        totalHeight = numRows * maxHeight
        totalHeight += (numRows) * layout.spacing()
        totalHeight += layout.contentsMargins().top() + layout.contentsMargins().bottom()
        maxWidth = Hilfsmethoden.emToPixels(40) if self.numCols == 1 else Hilfsmethoden.emToPixels(30)
        totalWidth = self.numCols * maxWidth
        horizontalSpacing = 7.0
        totalWidth += (self.numCols-1) * horizontalSpacing
        totalWidth += layout.contentsMargins().left() + layout.contentsMargins().right()
        for w in [self.newCharWidget, self.loadCharWidget]:
            multiplier = (1 if self.numCols == 1 else float(self.numCols)/2)
            extraSpacing = max((self.numCols-2), 0) * horizontalSpacing * 0.5
            w.setFixedWidth(maxWidth * multiplier + extraSpacing)
            w.setFixedHeight(maxHeight)
        for w in self.charWidgets:
            w.setFixedWidth(maxWidth)
            w.setFixedHeight(maxHeight)
        layout.addStretch()
        self.totalWidth = totalWidth
        self.totalHeight = totalHeight