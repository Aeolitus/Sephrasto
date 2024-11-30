# Based on https://github.com/Axel-Erfurt/PyEdit2. Upgraded it to PySide6 and fixed some bugs.
# PyEdit2 adapted it from = https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting

import sys

from Wolke import Wolke
from PySide6.QtCore import QRegularExpression, QTimer
from PySide6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

quote = "%s%s%s" % (chr(39), chr(39), chr(39))
dquote = "%s%s%s" % (chr(34), chr(34), chr(34))

def format(color, style=''):
    '''Return a QTextCharFormat with the given attributes.
    '''
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    if 'italicbold' in style:
        _format.setFontItalic(True)
        _format.setFontWeight(QFont.Bold)
    return _format

class Highlighter(QSyntaxHighlighter):
    '''Syntax highlighter for the Python language.
    '''
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'super', 'try', 'while', 'yield',
        'None', 'True', 'False', 'self', 'sorted'
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        super().__init__(document)
        
        self.styles = {
            'keyword': format(Wolke.CodeKeywordColor, 'bold'),
            'operator': format(Wolke.CodeOperatorsBracesColor),
            'brace': format(Wolke.CodeOperatorsBracesColor),
            'defnext': format(Wolke.CodeDeclarationColor, 'bold'),
            'classnext': format(Wolke.CodeDeclarationColor, 'bold'),
            'string': format(Wolke.CodeStringColor),
            'comment': format(Wolke.CodeCommentColor),
            #'selfnext': format('#2e3436', 'bold'),
            'numbers': format(Wolke.CodeNumberColor),
        }

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegularExpression((quote)), 1, self.styles['string'])
        self.tri_double = (QRegularExpression((dquote)), 2, self.styles['string'])

        self.updateDynamicRules = True

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, self.styles['keyword'])
            for w in Highlighter.keywords]
        rules += [(r'%s' % o, 0, self.styles['operator'])
            for o in Highlighter.operators]
        rules += [(r'%s' % b, 0, self.styles['brace'])
            for b in Highlighter.braces]

        # All other rules
        rules += [
            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, self.styles['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, self.styles['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, self.styles['numbers']),

            # Double-quoted string, possibly containing escape sequences ### "\"([^\"]*)\"" ### "\"(\\w)*\""
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['string']),

            # 'def' followed by an word
            (r'\bdef\b\s*(\w+)', 1, self.styles['defnext']),

            # 'self.' followed by an word
            #(r'\bself.\b\s*(\w+)', 1, self.styles['selfnext']),

            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, self.styles['classnext']),

            # From '#' until a newline
            (r'#[^\n]*', 0, self.styles['comment']),
        ]

        # Build a QRegularExpression for each pattern
        self.rules = [(QRegularExpression(pat), index, fmt)
            for (pat, index, fmt) in rules]
        self.dynamicRules = []
        
        self.importRule = QRegularExpression(r"\b(?:import|class)\b (.*)")

    def rebuildDynamicRules(self, text):
        self.dynamicRules = []
        matchIt = self.importRule.globalMatch(text)
        while matchIt.hasNext():
            match = matchIt.next()
            for i in range(1, match.lastCapturedIndex() + 1):
                imports = list(map(str.strip, match.captured(i).split(",")))
                for imp in [i.strip(":") for i in imports if i]:
                    self.dynamicRules.append((QRegularExpression(r'\b' + imp + r'\b'), 0, self.styles['classnext']))

    def rehighlight(self):
        self.updateDynamicRules = False
        self.rebuildDynamicRules(self.document().toPlainText())
        super().rehighlight()
        self.updateDynamicRules = True

    def highlightBlock(self, text):
        # Apply syntax highlighting to the given block of text.   
        if self.updateDynamicRules and self.importRule.match(text).hasMatch():
            self.updateDynamicRules = False
            QTimer.singleShot(5000,self.rehighlight)

        # Do other syntax formatting
        for expression, nth, format in self.dynamicRules + self.rules:
            match = expression.match(text)
            while match.hasMatch():
                # We actually want the index of the nth match
                index = match.capturedStart(nth)
                length = len(match.captured(nth))
                self.setFormat(index, length, format)
                match = expression.match(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)


    def match_multiline(self, text, delimiter, in_state, style):
        '''Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegularExpression`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        '''
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            match = delimiter.match(text)
            start = match.capturedStart()
            # Move past this match
            add = match.capturedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            match = delimiter.match(text, start + add)
            end = match.capturedStart()
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + match.capturedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            match = delimiter.match(text, start + length)
            start = match.capturedStart()

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False