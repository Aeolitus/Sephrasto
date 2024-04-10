from PySide6 import QtWidgets, QtCore, QtGui

class TreeExpansionHelper:
    def __init__(self, treeWidget, button):
        self.treeWidget = treeWidget
        self.treeWidget.itemExpanded.connect(self.updateButton)
        self.treeWidget.itemCollapsed.connect(self.updateButton)

        self.button = button
        self.button.setText("\uf102")
        self.button.clicked.connect(self.toggleTreeExpansion)

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
            self.button.setToolTip("Alle Kategorien ausklappen")
        else:
            self.button.setText("\uf102")
            self.button.setToolTip("Alle Kategorien einklappen")

    def toggleTreeExpansion(self):
        if self.willExpand():
            self.treeWidget.expandAll()
        else:
            self.treeWidget.collapseAll()