# Based on https://github.com/MichaelVoelkel/qt-collapsible-section
# Improved to support self-resizing content such as the AutoResitingTextBrowser
'''
    Elypson/qt-collapsible-section
    (c) 2016 Michael A. Voelkel - michael.alexander.voelkel@gmail.com
    This file is part of Elypson/qt-collapsible section.
    Elypson/qt-collapsible-section is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License, or
    (at your option) any later version.
    Elypson/qt-collapsible-section is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Elypson/qt-collapsible-section. If not, see <http:#www.gnu.org/licenses/>.
'''

import PySide6.QtCore as cr
import PySide6.QtWidgets as wd
import sys
from QtUtils.RichTextButton import RichTextToolButton

class Section(wd.QWidget):
    def __init__(self, title="", animationDuration=100, parent=None):
        super().__init__(parent)
        self.animationDuration = animationDuration
        self.toggleButton = RichTextToolButton(self, None)
        self.toggleAnimation = cr.QParallelAnimationGroup(self)
        self.contentArea = wd.QScrollArea(self)
        self.mainLayout = wd.QGridLayout(self)
    
        self.toggleButton.setStyleSheet("QToolButton {border: none;}")
        self.toggleButton.setToolButtonStyle(cr.Qt.ToolButtonTextBesideIcon)
        self.toggleButton.setArrowType(cr.Qt.RightArrow)
        self.toggleButton.setText(2*"&nbsp;" + title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)

        self.contentArea.setSizePolicy(wd.QSizePolicy.Expanding, wd.QSizePolicy.Maximum)

        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
    
        # let the entire widget grow and shrink with its content
        self.toggleAnimation.addAnimation(cr.QPropertyAnimation(self, b"minimumHeight"))
        self.toggleAnimation.addAnimation(cr.QPropertyAnimation(self, b"maximumHeight"))
        self.toggleAnimation.addAnimation(cr.QPropertyAnimation(self.contentArea, b"maximumHeight"))
    
        self.mainLayout.setVerticalSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
    
        row = 0
        self.mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, cr.Qt.AlignLeft)
        self.mainLayout.addWidget(self.contentArea, row+1, 0, 1, 3)
        self.setLayout(self.mainLayout)
    
        self.toggleButton.toggled.connect(self.toggle)
        self.animStartValue = 0
        self.animEndValue = 0
        self.collapsedHeight = 0
        
    def setContentLayout(self, contentLayout):
        layout = self.contentArea.layout()
        del layout
        self.contentArea.setLayout(contentLayout)
        self.collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        self.updateHeight(contentLayout.sizeHint().height())

    def updateHeight(self, height, immediate = False):
        if self.toggleAnimation.state() != cr.QAbstractAnimation.Stopped:
            return

        contentLayout = self.contentArea.layout()
        contentHeight = height + contentLayout.contentsMargins().top() + contentLayout.contentsMargins().bottom()
        for i in range(0, self.toggleAnimation.animationCount()-1):
            sectionAnimation = self.toggleAnimation.animationAt(i)
            sectionAnimation.setDuration(self.animationDuration)
            sectionAnimation.setStartValue(self.collapsedHeight)
            sectionAnimation.setEndValue(self.collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

        if immediate and self.toggleButton.isChecked():
            self.setMinimumHeight(self.collapsedHeight + contentHeight)
            self.setMaximumHeight(self.collapsedHeight + contentHeight)
            self.contentArea.setMaximumHeight(contentHeight)

    def toggle(self, collapsed):
        if collapsed:
            self.toggleButton.setArrowType(cr.Qt.DownArrow)
            self.toggleAnimation.setDirection(cr.QAbstractAnimation.Forward)
        else:
            self.toggleButton.setArrowType(cr.Qt.RightArrow)
            self.toggleAnimation.setDirection(cr.QAbstractAnimation.Backward)
        self.toggleAnimation.start()