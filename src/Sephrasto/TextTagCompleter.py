# Based on https://nachtimwald.com/2009/07/04/qcompleter-and-comma-separated-tags/

'''
Copyright (c) 2009 John Schember

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QCompleter

class TextTagCompleter(QCompleter):
    def __init__(self, parent, tags):
        QCompleter.__init__(self, tags, parent)
        self.setTags(tags)
        self.setWidget(parent)

        # Bidirectional dependency is meh but easier to use this way 
        # than having to subclass line edit too as in the original solution
        parent.textChanged.connect(self.handleLineEditTextChanged)
        self.activated.connect(self.handleSelfActivated)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.setFilterMode(QtCore.Qt.MatchContains)

    def __cursorPos(self):
        if hasattr(self.widget(), "cursorPosition"):
            return self.widget().cursorPosition()
        else:
            return self.widget().textCursor().position()

    def __setCursorPos(self, pos):
        if hasattr(self.widget(), "setCursorPosition"):
            self.widget().setCursorPosition(pos)
        else:
            cursor = self.widget().textCursor()
            cursor.setPosition(pos)
            self.widget().setTextCursor(cursor)

    def __setText(self, text):
        if hasattr(self.widget(), "setText"):
            self.widget().setText(text)
        else:
            self.widget().setPlainText(text)

    def __text(self):
        if hasattr(self.widget(), "text"):
            return self.widget().text()
        else:
            return self.widget().toPlainText()

    def setTags(self, tags):
        self.tags = set(tags)

    def handleLineEditTextChanged(self):
        text = self.__text()[:self.__cursorPos()]
        prefix = text.split(',')[-1].strip()

        textTags = []
        for t in self.__text().split(','):
            t1 = t.strip()
            if t1 != '':
                textTags.append(t1)
        textTags = list(set(textTags))

        tags = list(self.tags.difference(textTags))
        model = QStringListModel(tags, self)
        self.setModel(model)

        self.setCompletionPrefix(prefix)
        if prefix.strip() != '':
            self.complete()

    def handleSelfActivated(self, text):
        cursor_pos = self.__cursorPos()
        before_text = self.__text()[:cursor_pos]
        after_text = self.__text()[cursor_pos:]
        prefix_len = len(before_text.split(',')[-1].strip())
        self.__setText('%s%s, %s' % (before_text[:cursor_pos - prefix_len], text, after_text))
        self.__setCursorPos(cursor_pos - prefix_len + len(text) + 2)