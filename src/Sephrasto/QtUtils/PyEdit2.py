# Based on https://github.com/Axel-Erfurt/PyEdit2. Upgraded it to PySide6, merged some files together.
# Also added some features (i.e. backtab) and fixed some bugs.

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QCompleter
from PySide6.QtGui import QPainter, QTextCursor
from PySide6.QtCore import Qt, QRect, QStringListModel
from sys import argv
from QtUtils.PyEdit2Syntax import *

tab = chr(9)

wordlist = ["False",
"True",
"None",
"and",
"as",
"assert",
"async",
"await",
"break",
"class",
"continue",
"def",
"del",
"elif",
"else:",
"except",
"finally",
"for",
"from",
"global",
"if",
"import",
"in",
"is",
"lambda",
"nonlocal",
"not",
"or",
"pass",
"raise",
"return",
"try",
"while",
"with",
"yield",
"self",
"Exception",
"append()",
"extend()",
"insert()",
"remove()",
"pop()",
"clear()",
"index()",
"count()",
"sort()",
"reverse()",
"copy()",
"getattr()",
"setattr()",
"len()",
"list()",
"set()",
"int()",
"str()",
"float()",
"pow()",
"round()",
"floor()",
"ceil()",
"min()",
"max()",
"startswith()",
"endswith()",
"find()",
"join()",
"strip()",
"lstrip()",
"rstrip()",
"split()",
"lower()",
"upper()",
"keys()",
"values()",
"items()",
"difference()",
"intersection()",
"union()"]

class TextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.installEventFilter(self)

        self.highlighter = Highlighter(self.document())

        self._completer = None
        completer = QCompleter()
        completer.setModel(QStringListModel(wordlist, completer))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setWrapAround(False)
        completer.setCompletionRole(Qt.EditRole)
        self.setCompleter(completer)
        self.setError(False)
        self.setProperty("class", ["monospace", "codeEditor"])

    def setPlainText(self, text):
        self.highlighter.rebuildDynamicRules(text)
        super().setPlainText(text)

    def setError(self, hasError):
        self.setProperty("error", hasError)
        self.style().unpolish(self)
        self.style().polish(self)

    def setCompleter(self, c):
        if self._completer is not None:
            self._completer.activated.disconnect()

        self._completer = c
        c.setWidget(self)
        c.setCompletionMode(QCompleter.PopupCompletion)
        c.activated.connect(self.insertCompletion)

    def completer(self):
        return self._completer

    def insertCompletion(self, completion):
        if self._completer.widget() is not self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())

        tc.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, len(self._completer.completionPrefix()))
        tc.select(QTextCursor.WordUnderCursor)
        tc.removeSelectedText()
        tc.insertText(completion)
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)

        return tc.selectedText()

    def focusInEvent(self, e):
        if self._completer is not None:
            self._completer.setWidget(self)

        super().focusInEvent(e)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Backtab:
            cursor = self.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)
            selectedText = cursor.selectedText()
            if selectedText.startswith('    '):
                text = selectedText.replace('    ', '', 1)
                cursor.insertText(text)
            return
        if e.key() == Qt.Key_Tab:
            self.textCursor().insertText("    ")
            return
        if e.key() == Qt.Key_Escape and self._completer is not None and self._completer.popup().isVisible():
            self._completer.popup().hide()
            return
        if self._completer is not None and self._completer.popup().isVisible():
            # The following keys are forwarded by the completer to the widget.
            if e.key() in (Qt.Key_Enter, Qt.Key_Return):
                e.ignore()
                # Let the completer do default behavior.
                return

        isShortcut = ((e.modifiers() & Qt.ControlModifier) != 0 and e.key() == Qt.Key_Escape)
        if self._completer is None or not isShortcut:
            # Do not process the shortcut when we have a completer.
            super().keyPressEvent(e)

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if self._completer is None or (ctrlOrShift and len(e.text()) == 0):
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift
        completionPrefix = self.textUnderCursor()

        if not isShortcut and (hasModifier or len(e.text()) == 0 or len(completionPrefix) < 2 or e.text()[-1] in eow):
            self._completer.popup().hide()
            return

        if completionPrefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completionPrefix)
            self._completer.popup().setCurrentIndex(
                    self._completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
        self._completer.complete(cr)
    ####################################################################

class NumberBar(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.editor = parent
        layout = QVBoxLayout()
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().horizontalAdvance(str(string)) + 8
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)
            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1

                rect = QRect(0, block_top + 2, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, Qt.AlignRight, '%i'%number)

                if block_top > event.rect().bottom():
                    condition = False

                block = block.next()

            painter.end()