from PySide6 import QtWidgets, QtCore, QtGui

class DatenbankMergeDialogWrapper():
    def __init__(self, databaseType, database, old, new):
        compareDialog = QtWidgets.QDialog()
        compareDialog.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint)

        compareDialog.setWindowTitle("Sephrasto - " + databaseType.dataType.displayName + " vergleichen")
        
        rootLayout = QtWidgets.QVBoxLayout()
        rootLayout.setSpacing(10)
        compareDialog.setLayout(rootLayout)       

        name = old.name if old is not None else new.name
        info = QtWidgets.QLabel(databaseType.dataType.displayName + " " + name + " wurde sowohl in den bestehenden, "\
            "als auch in den neu geladenen Hausregeln geändert. Welche Version möchtest du beibehalten?\n"\
            "Hinweis: Sämtliche Änderungen die du machst, werden mit übernommen.")
        rootLayout.addWidget(info)

        contentLayout = QtWidgets.QHBoxLayout()
        rootLayout.addLayout(contentLayout)
        
        # Old editor (left)
        layoutLeft = QtWidgets.QVBoxLayout()
        header = QtWidgets.QLabel("Aktuell")
        header.setMinimumWidth(300)
        header.setProperty("class", "h2")
        layoutLeft.addWidget(header)
        editorOld = None
        if old is None:
            label = QtWidgets.QLabel("Gelöscht")
            spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
            layoutLeft.addWidget(label)
            layoutLeft.addItem(spacer)
        else:
            editorOld = databaseType.display(database, old, True)
            layoutLeft.addWidget(editorOld.form)
        contentLayout.addLayout(layoutLeft)
        
        # New editor (right)             
        layoutRight = QtWidgets.QVBoxLayout()
        header = QtWidgets.QLabel("Neu")
        header.setMinimumWidth(300)
        header.setProperty("class", "h2")
        layoutRight.addWidget(header)                    
        editorNew = None
        if new is None:
            label = QtWidgets.QLabel("Gelöscht")
            spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
            layoutRight.addWidget(label)
            layoutRight.addItem(spacer)
        else:
            editorNew = databaseType.display(database, new, True)
            layoutRight.addWidget(editorNew.form)
        contentLayout.addLayout(layoutRight)
        
        # Buttons
        self.chooseOld = False
        self.chooseNew = False
        buttonBox = QtWidgets.QDialogButtonBox()
        oldButton = buttonBox.addButton("Aktuell auswählen", QtWidgets.QDialogButtonBox.YesRole)
        oldButton.clicked.connect(lambda: setattr(self, "chooseOld", True))
        newButton = buttonBox.addButton("Neu auswählen", QtWidgets.QDialogButtonBox.YesRole)
        newButton.clicked.connect(lambda: setattr(self, "chooseNew", True))
        
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(compareDialog.accept)
        buttonBox.rejected.connect(compareDialog.accept)
        rootLayout.addWidget(buttonBox)
              
        self.element = databaseType.dataType()
        compareDialog.exec()

        self.element = None
        if self.chooseNew and editorNew is not None:
            self.element = databaseType.dataType()
            editorNew.update(self.element)
            self.element.finalize(database)
        elif self.chooseOld and editorOld is not None:
            self.element = databaseType.dataType()
            editorOld.update(self.element)
            self.element.finalize(database)