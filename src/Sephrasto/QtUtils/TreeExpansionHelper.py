from PySide6 import QtWidgets, QtCore, QtGui
from Wolke import Wolke

class TreeExpansionHelper:
    def __init__(self, treeWidget, button, singleRoot=False):
        self.singleRoot = singleRoot
        self.treeWidget = treeWidget
        self.treeWidget.itemExpanded.connect(self.updateButton)
        self.treeWidget.itemCollapsed.connect(self.updateButton)

        self.button = button
        self.button.clicked.connect(self.toggleTreeExpansion)

        self.expandTooltip = "<html><body>Alle Kategorien ausklappen<br>"\
            "Strg+<span style='" + Wolke.FontAwesomeCSS + "'>\uf30c</span> (einklappen)<br>Strg+<span style='" + Wolke.FontAwesomeCSS + "'>\uf309</span> (ausklappen)</body></html>"
        self.collapseTooltip = "<html><body>Alle Kategorien einklappen<br>"\
            "Strg+<span style='" + Wolke.FontAwesomeCSS + "'>\uf30c</span> (einklappen)<br>Strg+<span style='" + Wolke.FontAwesomeCSS + "'>\uf309</span> (ausklappen)</body></html>"

        self.button.setText("\uf102")
        self.button.setToolTip(self.collapseTooltip)

        self.shortcutExpand = QtGui.QAction()
        self.shortcutExpand.setShortcut("Ctrl+Down")
        self.shortcutExpand.triggered.connect(self.expandAll)
        self.treeWidget.addAction(self.shortcutExpand)
        self.shortcutCollapse = QtGui.QAction()
        self.shortcutCollapse.setShortcut("Ctrl+Up")
        self.shortcutCollapse.triggered.connect(self.collapseAll)
        self.treeWidget.addAction(self.shortcutCollapse)

    def willExpand(self):
        allCollapsed = True
        for i in range(self.treeWidget.topLevelItemCount()):
            itm = self.treeWidget.topLevelItem(i)
            if type(itm) != QtWidgets.QTreeWidgetItem:
                continue
            if itm.isExpanded():
                allCollapsed = False
        return allCollapsed

    def updateButton(self):
        if self.willExpand():
            self.button.setText("\uf103")
            self.button.setToolTip(self.expandTooltip)
        else:
            self.button.setText("\uf102")
            self.button.setToolTip(self.collapseTooltip)

    def toggleTreeExpansion(self):
        if self.willExpand():
            self.expandAll()
        else:
            self.collapseAll()

    def expandAll(self):
        self.treeWidget.expandAll()

    def collapseAll(self):
        self.treeWidget.collapseAll()
        if self.singleRoot:
            self.treeWidget.topLevelItem(0).setExpanded(True)