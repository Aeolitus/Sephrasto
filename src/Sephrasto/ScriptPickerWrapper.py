import UI.ScriptPicker
from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import logging
import copy
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden, SortedCategoryToListDict
from QtUtils.TreeExpansionHelper import TreeExpansionHelper
from QtUtils.TextTagCompleter import TextTagCompleter
from functools import partial
from RestrictedPython import compile_restricted
from QtUtils.PyEdit2 import TextEdit, NumberBar
from QtUtils.RichTextButton import RichTextPushButton
from QtUtils.AutoResizingTextBrowser import TextEditAutoResizer
from Scripts import Scripts, ScriptContext
from WebEngineWrapper import WebEngineWrapper

class ParameterWidget(QtWidgets.QWidget):
    def __init__(self, parameter, scripts, showLabel = False):
        super().__init__()
        self.parameter = parameter
        self.scripts = scripts

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(layout)

        self.childLayout = QtWidgets.QGridLayout()
        layout.addLayout(self.childLayout)

        if showLabel:
            self.subParamLabel = QtWidgets.QLabel()
            self.subParamLabel.setText(parameter.name)
            self.childLayout.addWidget(self.subParamLabel, 0, 0)

        self.getterButton = QtWidgets.QToolButton()
        self.getterButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.childLayout.addWidget(self.getterButton, 0, 1)

        self.valueWidget = None

        if parameter.typ == str:
            self.setMenu(self.scripts.stringGetterByKategorie)             
        elif parameter.typ == int or parameter.typ == float:
            self.setMenu(self.scripts.numberGetterByKategorie)
        elif parameter.typ == bool:
            self.setMenu(self.scripts.boolGetterByKategorie)

    def setMenu(self, scriptsByKategorie):
        self.menu = QtWidgets.QMenu()
        action = self.menu.addAction("Konstante")
        action.triggered.connect(partial(self.onGetterButtonClicked, script="Konstante"))
        for kategorie, scripts in scriptsByKategorie.items():
            if len(scripts) == 0:
                continue
            subMenu = self.menu.addMenu(kategorie)
            for script in scripts:
                action = subMenu.addAction(script.name)
                action.triggered.connect(partial(self.onGetterButtonClicked, script=script))
        self.getterButton.setMenu(self.menu)
        self.onGetterButtonClicked("Konstante")

    def onGetterButtonClicked(self, script):
        if self.valueWidget:
            self.valueWidget.setParent(None)
            self.valueWidget.deleteLater()
            self.valueWidget = None
        self.childLayout.setColumnStretch(3, 1)
        if script == "Konstante":
            self.getterButton.setText("Konstante  ")        
            if self.parameter.typ == int:
                self.valueWidget = QtWidgets.QSpinBox()
                self.valueWidget.setMinimum(-999)
                self.valueWidget.setMaximum(999)
                self.valueWidget.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                self.valueWidget.setValue(self.parameter.defaultValue or 0)
                self.childLayout.addWidget(self.valueWidget, 0, 2)
            elif self.parameter.typ == float:
                self.valueWidget = QtWidgets.QDoubleSpinBox()
                self.valueWidget.setMinimum(-999)
                self.valueWidget.setMaximum(999)
                self.valueWidget.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                self.valueWidget.setValue(self.parameter.defaultValue or 0.0)
                self.childLayout.addWidget(self.valueWidget, 0, 2)
            elif self.parameter.typ == str:
                self.valueWidget = QtWidgets.QLineEdit()
                self.valueWidget.setText(self.parameter.defaultValue or "")      
                if self.parameter.completionTable is not None:
                    self.completer = TextTagCompleter(self.valueWidget, self.parameter.completionTable)
                self.childLayout.addWidget(self.valueWidget, 0, 2)
                self.childLayout.setColumnStretch(3, 0)
            elif self.parameter.typ == bool:
                self.valueWidget = QtWidgets.QCheckBox()
                self.valueWidget.setChecked(self.parameter.defaultValue or False)
                self.childLayout.addWidget(self.valueWidget, 0, 2)  
            return

        self.getterButton.setText(script.name + "  ")
        if len(script.parameter) > 0:
            subParam = script.parameter[0]
            self.valueWidget = ParameterWidget(subParam, self.scripts, showLabel=True)
            self.layout().addWidget(self.valueWidget)

    def text(self):
        getterName = self.getterButton.text().strip()
        params = {}
        if self.parameter.typ == str:
            if getterName == "Konstante":
                return '"' + self.valueWidget.text() + '"'
            else:
                script = self.scripts.stringGetter[getterName]
                if len(script.parameter) > 0:
                    params[script.parameter[0].name] = self.valueWidget.text()
                return script.buildCode(params) 
        elif self.parameter.typ == int:
            if getterName == "Konstante":
                return str(self.valueWidget.value())
            else:
                script = self.scripts.numberGetter[getterName]
                if len(script.parameter) > 0:
                    params[script.parameter[0].name] = self.valueWidget.text()
                return script.buildCode(params) 
        elif self.parameter.typ == float:
            if getterName == "Konstante":
                return str(self.valueWidget.value())
            else:
                script = self.scripts.numberGetter[getterName]
                if len(script.parameter) > 0:
                    params[script.parameter[0].name] = self.valueWidget.text()
                return script.buildCode(params) 
        elif self.parameter.typ == bool:
            if getterName == "Konstante":
                return str(self.valueWidget.isChecked())
            else:
                script = self.scripts.boolGetter[getterName]
                if len(script.parameter) > 0:
                    params[script.parameter[0].name] = self.valueWidget.text()
                return script.buildCode(params)
        return ""

class ScriptPickerWrapper(object):
    def __init__(self, datenbank, script, context = ScriptContext.Charakter, mode = "exec"):
        super().__init__()
        self.datenbank = datenbank
        self.current = ""
        self.mode = mode

        logging.debug("Initializing ScriptPicker...")

        self.form = QtWidgets.QDialog()
        self.ui = UI.ScriptPicker.Ui_Dialog()
        self.ui.setupUi(self.form)
        
        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)

        windowSize = Wolke.Settings["WindowSize-ScriptPicker"]
        self.form.resize(windowSize[0], windowSize[1])

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.4), int(width*0.6)])

        self.scripts = Scripts.create(datenbank, context)

        self.editor = TextEdit()
        self.numbers = NumberBar(self.editor)
        self.ui.codeLayout.layout().addWidget(self.numbers)
        self.ui.codeLayout.layout().addWidget(self.editor)

        self.ui.buttonInsert = RichTextPushButton(None, "<span style='" + Wolke.FontAwesomeCSS + f"'>\uf078</span>&nbsp;&nbsp;Einfügen&nbsp;&nbsp;<span style='" + Wolke.FontAwesomeCSS + f"'>\uf078</span>")
        self.ui.insertButtonLayout.addWidget(self.ui.buttonInsert)
        self.ui.buttonInsert.clicked.connect(self.insertClicked)

        self.ui.buttonHelp.setText("\uf059")
        self.ui.buttonHelp.clicked.connect(self.helpClicked)

        self.ui.treeScripts.setHeaderHidden(True)
        self.populateTree()
        self.ui.treeScripts.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeScripts.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Fixed)

        self.autoResizeHelper = TextEditAutoResizer(self.ui.teBeschreibung)
        self.expansionHelper = TreeExpansionHelper(self.ui.treeScripts, self.ui.buttonExpandToggle)

        self.editor.setPlainText(script)
        self.editor.textChanged.connect(self.scriptTextChanged)
        self.scriptTextChanged()

        self.ui.labelFilter.setText("\uf002")
        self.ui.nameFilterEdit.setFocus()

        self.shortcutSearch = QtGui.QAction()
        self.shortcutSearch.setShortcut("Ctrl+F")
        self.shortcutSearch.triggered.connect(self.ui.nameFilterEdit.setFocus)
        self.form.addAction(self.shortcutSearch)
        self.shortcutClearSearch = QtGui.QAction()
        self.shortcutClearSearch.setShortcut("Esc")
        self.shortcutClearSearch.triggered.connect(lambda: self.ui.nameFilterEdit.setText("") if self.ui.nameFilterEdit.hasFocus() and self.ui.nameFilterEdit.text() else self.form.reject())
        self.form.addAction(self.shortcutClearSearch)

        self.updateInfo()
        self.ui.nameFilterEdit.textChanged.connect(self.populateTree)

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()

        Wolke.Settings["WindowSize-ScriptPicker"] = [self.form.size().width(), self.form.size().height()]

        if hasattr(self, "hilfe"):
            self.hilfe.form.hide()
            self.hilfe.form.deleteLater()

        if self.ret == QtWidgets.QDialog.Accepted:
            self.script = self.editor.toPlainText()
        else:
            self.script = None

    def populateTree(self):
        currSet = self.current != ""
        self.ui.treeScripts.clear()

        self.scripts.setSetterFilter(self.ui.nameFilterEdit.text())

        for kategorie, scripts in self.scripts.settersByKategorie.items():
            if len(scripts) == 0:
                continue

            parent = QtWidgets.QTreeWidgetItem(self.ui.treeScripts)
            parent.setText(0, kategorie)
            parent.setExpanded(True)
            font = QtGui.QFont(Wolke.Settings["Font"], Wolke.FontHeadingSizeL3)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            parent.setFont(0, font)

            for script in scripts:
                if not currSet:
                    self.current = script.name
                    currSet = True
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, script.name)

        self.changeHandler()

    def changeHandler(self):
        self.current = ""
        for el in self.ui.treeScripts.selectedItems():
            if el.text(0) in self.scripts.kategorien:
                continue
            self.current = el.text(0)
            break
        self.updateInfo()

    def updateInfo(self):
        self.ui.lblName.setText("Kein Script ausgewählt")
        self.ui.teBeschreibung.setText("")
        while self.ui.layoutParameter.rowCount() > 0:
            self.ui.layoutParameter.removeRow(0)

        self.ui.buttonInsert.setEnabled(self.current != "")

        if not self.current:
            return
        script = self.scripts.setters[self.current]

        self.ui.lblName.setText(script.name)
        self.ui.teBeschreibung.setText(Hilfsmethoden.fixHtml(script.beschreibung))

        for parameter in script.parameter:
            paramWidget = ParameterWidget(parameter, self.scripts)
            label = QtWidgets.QLabel(parameter.name)
            label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            self.ui.layoutParameter.addRow(label, paramWidget)

    def insertClicked(self):
        if not self.current:
            return
        script = self.scripts.setters[self.current]
        params = {}
        for i in range(self.ui.layoutParameter.rowCount()):
            layoutItem = self.ui.layoutParameter.itemAt(i, QtWidgets.QFormLayout.LabelRole)
            paramId = layoutItem.widget().text()
            layoutItem = self.ui.layoutParameter.itemAt(i, QtWidgets.QFormLayout.FieldRole)
            widget = layoutItem.widget()
            params[paramId] = widget.text()
        self.editor.insertPlainText(script.buildCode(params))
        self.editor.setFocus()

    def helpClicked(self):
        if not hasattr(self, "hilfe"):
            self.hilfe = WebEngineWrapper("Hilfe", "./Doc/script_api.html", Wolke.MkDocsCSS, "WindowSize-Hilfe", parent=self.form)
            self.hilfe.form.show()
        else:
            self.hilfe.form.show()
            self.hilfe.form.activateWindow()

    def scriptTextChanged(self):
        error = ""

        if self.mode == "eval" and "\n" in self.editor.toPlainText():
            error = "Dieses Script muss einen Ausdruck in einer einzelnen Zeile enthalten."

        if not error:
            try:
                compile_restricted(self.editor.toPlainText(), "Script", self.mode)
            except SyntaxError as e:
                error = "\n".join(e.msg)

        if error:
            self.editor.setError(True)
            self.editor.setToolTip(error)
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.editor.setError(False)
            self.editor.setToolTip("")
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)