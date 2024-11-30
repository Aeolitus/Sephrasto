from PySide6 import QtWidgets, QtCore, QtGui
from Wolke import Wolke
from Hilfsmethoden import Hilfsmethoden
import base64

class HtmlToolbar(QtWidgets.QWidget):
    def __init__(self, textEdit, parent = None):
        super().__init__(parent)
        self.editor = textEdit
        layout = QtWidgets.QHBoxLayout()
        margin = Hilfsmethoden.emToPixels(0.5)
        layout.setContentsMargins(margin, margin, margin, margin)

        self.paragraphButton = QtWidgets.QPushButton(self)
        self.paragraphButton.setText("\u0050")
        self.paragraphButton.setShortcut("Ctrl+P")
        self.paragraphButton.setToolTip("Paragraph (" + self.paragraphButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.paragraphButton.clicked.connect(lambda: self.insertTag("<p>", "</p>"))

        self.boldButton = QtWidgets.QPushButton(self)
        self.boldButton.setText("\uf032")
        self.boldButton.setShortcut(QtGui.QKeySequence.Bold)
        self.boldButton.setToolTip("Fett (" + self.boldButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.boldButton.clicked.connect(lambda: self.insertTag("<b>", "</b>"))

        self.italicButton = QtWidgets.QPushButton(self)
        self.italicButton.setText("\uf033")
        self.italicButton.setShortcut(QtGui.QKeySequence.Italic)
        self.italicButton.setToolTip("Kursiv (" + self.italicButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.italicButton.clicked.connect(lambda: self.insertTag("<i>", "</i>"))

        self.underlineButton = QtWidgets.QPushButton(self)
        self.underlineButton.setText("\uf0cd")
        self.underlineButton.setShortcut(QtGui.QKeySequence.Underline)
        self.underlineButton.setToolTip("Unterstrichen (" + self.underlineButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.underlineButton.clicked.connect(lambda: self.insertTag("<u>", "</u>"))

        self.line1 = QtWidgets.QFrame()
        self.line1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.ulButton = QtWidgets.QPushButton(self)
        self.ulButton.setText("\uf0ca")
        self.ulButton.setShortcut(QtGui.QKeySequence("Ctrl+L"))
        self.ulButton.setToolTip("Liste (" + self.ulButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.ulButton.clicked.connect(lambda: self.insertTag("<ul>", "</ul>"))
        
        self.olButton = QtWidgets.QPushButton(self)
        self.olButton.setText("\uf0cb")
        self.olButton.setShortcut(QtGui.QKeySequence("Ctrl+O"))
        self.olButton.setToolTip("Geordnete Liste (" + self.olButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.olButton.clicked.connect(lambda: self.insertTag("<ol>", "</ol>"))

        self.liButton = QtWidgets.QPushButton(self)
        self.liButton.setText("\uf621")
        self.liButton.setShortcut(QtGui.QKeySequence("Ctrl+E"))
        self.liButton.setToolTip("Listeneintrag (" + self.liButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.liButton.clicked.connect(lambda: self.insertTag("<li>", "</li>"))

        self.line2 = QtWidgets.QFrame()
        self.line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.tableButton = QtWidgets.QPushButton(self)
        self.tableButton.setText("\uf00a")
        self.tableButton.setShortcut(QtGui.QKeySequence("Ctrl+T"))
        self.tableButton.setToolTip("Tabelle (" + self.tableButton.shortcut().toString(QtGui.QKeySequence.NativeText) + ")")
        self.tableButton.clicked.connect(self.tablePopup)

        self.line3 = QtWidgets.QFrame()
        self.line3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.imageButton = QtWidgets.QPushButton(self)
        self.imageButton.setText("\uf03e")
        self.imageButton.setToolTip("Bildlink einfügen")
        self.imageButton.clicked.connect(self.imagePopup)
                
        self.imageEmbedButton = QtWidgets.QPushButton(self)
        self.imageEmbedButton.setText("\uf1c5")
        self.imageEmbedButton.setToolTip("<html><head/><body>Bild einbetten.<br>"\
            "Das Bild wird auf max. 512x512 Pixel reduziert, wobei das Seitenverhältnis erhalten bleibt.<br>"\
            "Danach wird es in Textform eingefügt, was üblicherweise einen sehr langen &lt;img&gt;-Tag zur Folge hat.<br>"\
            "Dies hat allerdings den Vorteil, dass das Bild im Gegensatz zu einem Link nicht verloren gehen kann, da es direkt in der Datenbank gespeichert wird.</body></html>")
        self.imageEmbedButton.clicked.connect(self.imageEmbedPopup)

        self._widgets = [
            self.paragraphButton,
            self.boldButton,
            self.italicButton,
            self.underlineButton,
            self.line1,
            self.ulButton,
            self.olButton,
            self.liButton,
            self.line2,
            self.tableButton,
            self.line3,
            self.imageButton,
            self.imageEmbedButton
        ]

        for w in self._widgets:
            if isinstance(w, QtWidgets.QPushButton):
                w.setProperty("class", "icon")
                font = w.font()
                font.setHintingPreference(QtGui.QFont.PreferNoHinting)
                w.setFont(font)
            layout.addWidget(w)

        layout.addStretch()
        self.setLayout(layout)

    def insertTag(self, startTag, endTag):
        cursor = self.editor.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        cursor.setPosition(start)
        cursor.insertText(startTag)
        cursor.setPosition(end+len(startTag))
        cursor.insertText(endTag)
        cursor.setPosition(start+len(startTag))
        cursor.setPosition(end+len(startTag), QtGui.QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def tablePopup(self):
        messageBox = QtWidgets.QDialog()
        messageBox.setWindowTitle("Tabelle erstellen")

        layout = QtWidgets.QVBoxLayout()
        layout2 = QtWidgets.QHBoxLayout()
        labelCol = QtWidgets.QLabel("Spalten")
        spinCol = QtWidgets.QSpinBox()
        spinCol.setValue(2)
        spinCol.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        labelRow = QtWidgets.QLabel("Zeilen")
        spinRow = QtWidgets.QSpinBox()
        spinRow.setValue(2)
        spinRow.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        layout2.addWidget(labelCol)
        layout2.addWidget(spinCol)
        layout2.addWidget(labelRow)
        layout2.addWidget(spinRow)
        layout.addLayout(layout2)
        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.addButton("Einfügen", QtWidgets.QDialogButtonBox.YesRole)
        buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)       
        buttonBox.accepted.connect(lambda: messageBox.accept())
        buttonBox.rejected.connect(lambda: messageBox.reject())

        layout.addWidget(buttonBox)

        messageBox.setLayout(layout)
        result = messageBox.exec()
        if result == 0:
            return
        table = "<table>"
        first = True
        for row in range(spinRow.value()):
            table += "\n<tr>"
            for col in range(spinCol.value()):
                table += "\n<th></th>" if first else "\n<td></td>"
            table += "\n</tr>"
            first = False
        if table == "<table>":
            table += "</table>"
        else:
            table += "\n</table>"
        cursor = self.editor.textCursor()
        cursor.insertText(table)
        self.editor.setFocus()

    def imagePopup(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Bild laden...", "", "Bild Dateien (*.png *.jpg *.bmp)")
        if spath == "":
            return
        image = f"<img src='{spath}'>"
        cursor = self.editor.textCursor()
        cursor.insertText(image)
        self.editor.setFocus()

    def imageEmbedPopup(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Bild laden...", "", "Bild Dateien (*.png *.jpg *.bmp)")
        if spath == "":
            return

        pixmap = QtGui.QPixmap(spath)
        width = min(pixmap.width(), 512)
        height = min(pixmap.height(), 512)
        image = pixmap.scaled(QtCore.QSize(width, height), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.WriteOnly);
        image.save(buffer, "PNG")
        image = base64.b64encode(buffer.data().data()).decode('ascii')
        imageTag = f"<img src='data:image/jpg;base64, {image}'>"
        cursor = self.editor.textCursor()
        cursor.insertText(imageTag)
        self.editor.setFocus()