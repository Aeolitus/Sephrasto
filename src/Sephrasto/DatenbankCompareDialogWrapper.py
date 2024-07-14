from PySide6 import QtWidgets, QtCore, QtGui
from Wolke import Wolke

class DatenbankCompareDialogWrapper():
    def __init__(self, databaseType, database, old, new):
        self.form = QtWidgets.QDialog()
        self.form.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)

        self.form.setWindowTitle("Sephrasto - " + databaseType.dataType.displayName + " vergleichen")
        
        rootLayout = QtWidgets.QVBoxLayout()
        rootLayout.setSpacing(10)
        self.form.setLayout(rootLayout)       

        contentLayout = QtWidgets.QHBoxLayout()
        rootLayout.addLayout(contentLayout)
        
        # Old editor (left)
        layoutLeft = QtWidgets.QVBoxLayout()
        header = QtWidgets.QLabel(self.getLabelLeft())
        header.setMinimumWidth(300)
        header.setProperty("class", "h2")
        layoutLeft.addWidget(header)
        self.editorOld = None
        if old is None:
            label = QtWidgets.QLabel("Gelöscht")
            spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
            layoutLeft.addWidget(label)
            layoutLeft.addItem(spacer)
        else:
            self.editorOld = databaseType.display(database, old)
            layoutLeft.addWidget(self.editorOld.form)
        contentLayout.addLayout(layoutLeft)
        
        # New editor (right)             
        layoutRight = QtWidgets.QVBoxLayout()
        header = QtWidgets.QLabel(self.getLabelRight())
        header.setMinimumWidth(300)
        header.setProperty("class", "h2")
        layoutRight.addWidget(header)                    
        self.editorNew = None
        if new is None:
            label = QtWidgets.QLabel("Gelöscht")
            spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
            layoutRight.addWidget(label)
            layoutRight.addItem(spacer)
        else:
            self.editorNew = databaseType.display(database, new)
            layoutRight.addWidget(self.editorNew.form)
        contentLayout.addLayout(layoutRight)
        
        # Buttons
     
    def getLabelInfo(self):
        pass

    def getLabelLeft(self):
        pass
    
    def getLabelRight(self):
        pass
    
class DatenbankMergeDialogWrapper(DatenbankCompareDialogWrapper):
    def __init__(self, databaseType, database, old, new):
        super().__init__(databaseType, database, old, new)
        
        name = old.name if old is not None else new.name
        info = QtWidgets.QLabel(databaseType.dataType.displayName + " " + name + " wurde sowohl in den bestehenden, "\
            "als auch in den neu geladenen Hausregeln geändert. Welche Version möchtest du beibehalten?\n"\
            "Hinweis: Sämtliche Änderungen die du machst, werden mit übernommen.")
        self.form.layout().insertWidget(0, info)

        self.chooseOld = False
        self.chooseNew = False
        buttonBox = QtWidgets.QDialogButtonBox()
        oldButton = buttonBox.addButton("Aktuell auswählen", QtWidgets.QDialogButtonBox.YesRole)
        oldButton.clicked.connect(lambda: setattr(self, "chooseOld", True))
        newButton = buttonBox.addButton("Neu auswählen", QtWidgets.QDialogButtonBox.YesRole)
        newButton.clicked.connect(lambda: setattr(self, "chooseNew", True))
        
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.form.accept)
        buttonBox.rejected.connect(self.form.accept)
        self.form.layout().addWidget(buttonBox)
              
        settingName = "WindowSize-DatenbankMergeDialog"
        windowSize = Wolke.Settings[settingName]
        self.form.resize(windowSize[0], windowSize[1])
        
        self.form.exec()
        
        Wolke.Settings[settingName] = [self.form.size().width(), self.form.size().height()]

        self.element = None
        if self.chooseNew and self.editorNew is not None:
            self.element = databaseType.dataType()
            self.editorNew.update(self.element)
        elif self.chooseOld and self.editorOld is not None:
            self.element = databaseType.dataType()
            self.editorOld.update(self.element)

    def getLabelLeft(self):
        return "Aktuell"
    
    def getLabelRight(self):
        return "Neu"
    
class DatenbankCompareRawDialogWrapper(DatenbankCompareDialogWrapper):
    def __init__(self, databaseType, database, old, new):
        super().__init__(databaseType, database, old, new)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)       
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.form.accept)
        buttonBox.rejected.connect(self.form.accept)
        self.form.layout().addWidget(buttonBox)
        
        self.editorOld.setReadOnly()
        self.editorNew.validationChanged.connect(lambda isValid: buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(isValid))
              
        settingName = "WindowSize-DatenbankMergeDialog"
        windowSize = Wolke.Settings[settingName]
        self.form.resize(windowSize[0], windowSize[1])
        
        ret = self.form.exec()
        
        Wolke.Settings[settingName] = [self.form.size().width(), self.form.size().height()]

        if ret == QtWidgets.QDialog.Accepted:
            self.element = databaseType.dataType()
            self.editorNew.update(self.element)
            self.element.finalize(database)
            if self.element.deepequals(new):
                self.element = None
        else:
            self.element = None
        
    def getLabelLeft(self):
        return "Original (nicht editierbar)"
    
    def getLabelRight(self):
        return "Hausregeln"