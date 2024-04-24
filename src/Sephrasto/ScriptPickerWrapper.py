import UI.ScriptPicker
from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import logging
import copy
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden
from QtUtils.TreeExpansionHelper import TreeExpansionHelper
from Hilfsmethoden import SortedCategoryToListDict
from QtUtils.TextTagCompleter import TextTagCompleter
from functools import partial
from RestrictedPython import compile_restricted
from QtUtils.PyEdit2 import TextEdit, NumberBar
from QtUtils.RichTextButton import RichTextPushButton

class ScriptParameter:
    def __init__(self, name, typ, defaultValue=None, completionTable = None):
        self.name = name
        self.typ = typ
        self.defaultValue = defaultValue
        self.completionTable = completionTable
        if isinstance(self.completionTable, dict):
            self.completionTable = list(self.completionTable.keys())

class Script:
    def __init__(self, name, identifier, kategorie = "", beschreibung = "", castType=None):
        self.name = name
        self.identifier = identifier
        self.kategorie = kategorie
        self.parameter = []
        self.beschreibung = beschreibung
        self.castType = castType

    # overrides need to be strings and literals need to be already enclosed in quotation marks
    def buildCode(self, paramOverrides = {}):
        paramsEvaluated = []
        for param in self.parameter:
            if param.name in paramOverrides:
                value = str(paramOverrides[param.name])
            else:
                value = str(param.defaultValue)
                if param.typ == str:
                    value = f'"{value}"'
            paramsEvaluated.append(value)
        code = f"{self.identifier}({', '.join(paramsEvaluated)})"
        if self.castType is not None:
            code = f"{self.castType.__name__}({code})"
        return code


class ScriptContext:
    Charakter = 0
    Waffeneigenschaften = 1

class ScriptPickerWrapper(object):

    def __init__(self, datenbank, script, context = ScriptContext.Charakter, mode = "exec"):
        super().__init__()
        self.datenbank = datenbank
        self.current = ""
        self.mode = mode
        self.completer = []

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

        self.initScripts(context)

        self.editor = TextEdit()
        self.numbers = NumberBar(self.editor)
        self.ui.codeLayout.layout().addWidget(self.numbers)
        self.ui.codeLayout.layout().addWidget(self.editor)

        self.ui.buttonInsert = RichTextPushButton(None, "<span style='" + Wolke.FontAwesomeCSS + f"'>\uf078</span>&nbsp;&nbsp;Einfügen&nbsp;&nbsp;<span style='" + Wolke.FontAwesomeCSS + f"'>\uf078</span>")
        self.ui.horizontalLayout.addWidget(self.ui.buttonInsert)
        self.ui.buttonInsert.clicked.connect(self.insertClicked)

        self.ui.treeScripts.setHeaderHidden(True)
        self.populateTree()
        self.ui.treeScripts.itemSelectionChanged.connect(self.changeHandler)
        self.ui.treeScripts.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Fixed)

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

        if self.ret == QtWidgets.QDialog.Accepted:
            self.script = self.editor.toPlainText()
        else:
            self.script = None

    def populateTree(self):
        currSet = self.current != ""
        self.ui.treeScripts.clear()

        scriptsByKategorie = SortedCategoryToListDict(self.scriptKategorien)
        scriptsByKategorie.setNameFilter(self.ui.nameFilterEdit.text())
        for script in self.setters.values():
            scriptsByKategorie.appendByName(script.kategorie, script.name)
        scriptsByKategorie.sortValues()

        for kategorie, scripts in scriptsByKategorie.items():
            if len(scripts) == 0:
                continue

            parent = QtWidgets.QTreeWidgetItem(self.ui.treeScripts)
            parent.setText(0, kategorie)
            parent.setExpanded(True)
            font = QtGui.QFont(Wolke.Settings["Font"], Wolke.FontHeadingSizeL3)
            font.setBold(True)
            font.setCapitalization(QtGui.QFont.SmallCaps)
            parent.setFont(0, font)

            for el in scripts:
                if not currSet:
                    self.current = el
                    currSet = True
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, el)

        self.changeHandler()

    def changeHandler(self):
        self.current = ""
        for el in self.ui.treeScripts.selectedItems():
            if el.text(0) in self.scriptKategorien:
                continue
            self.current = el.text(0)
            break
        self.updateInfo()

    def updateText(self, button, text, plusLabel):
        button.setText(text + "  ")
        plusLabel.setVisible(text != "Konstante")
        
    def setMenu(self, button, plusLabel, scriptsByKategorie):
        menu = QtWidgets.QMenu()
        action = menu.addAction("Konstante")
        action.triggered.connect(partial(self.updateText, button=button, text="Konstante", plusLabel=plusLabel))
        for kategorie, scripts in scriptsByKategorie.items():
            if len(scripts) == 0:
                continue
            subMenu = menu.addMenu(kategorie)
            for script in scripts:
                action = subMenu.addAction(script)
                action.triggered.connect(partial(self.updateText, button=button, text=script, plusLabel=plusLabel))
        button.setMenu(menu)
        self.menus.append(menu)

    def updateInfo(self):
        self.ui.lblName.setText("Kein Script ausgewählt")
        while self.ui.layoutParameter.rowCount() > 0:
            self.ui.layoutParameter.removeRow(0)
        self.completer = []
        self.menus = []

        self.ui.buttonInsert.setEnabled(self.current != "")

        if not self.current:
            return
        script = self.setters[self.current]

        self.ui.lblName.setText(script.name)
        self.ui.teBeschreibung.setText(Hilfsmethoden.fixHtml(script.beschreibung))
        
        for parameter in script.parameter:
            layout = QtWidgets.QHBoxLayout()
            getterButton = QtWidgets.QToolButton()
            getterButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
            getterButton.setText("Konstante  ")
            layout.addWidget(getterButton)

            plusLabel = QtWidgets.QLabel("+")
            plusLabel.setVisible(False)
            plusLabel.setFixedWidth(Hilfsmethoden.emToPixels(2))
            layout.addWidget(plusLabel)
            
            if parameter.typ == str:
                self.setMenu(getterButton, plusLabel, self.stringGetterByKategorie)
                widget = QtWidgets.QLineEdit()
                if parameter.completionTable is not None:
                    self.completer.append(TextTagCompleter(widget, parameter.completionTable))
                if parameter.defaultValue is not None:
                    widget.setText(parameter.defaultValue)
            elif parameter.typ == int or parameter.typ == float:
                self.setMenu(getterButton, plusLabel, self.numberGetterByKategorie)
                widget = QtWidgets.QSpinBox() if parameter.typ == int else QtWidgets.QDoubleSpinBox()
                widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
                widget.setMinimum(-999)
                widget.setMaximum(999)
                if parameter.defaultValue is not None:
                    widget.setValue(parameter.defaultValue)
            elif parameter.typ == bool:
                widget = QtWidgets.QCheckBox()
                if parameter.default is not None:
                    widget.setChecked(parameter.defaultValue)
            layout.addWidget(widget)
            self.ui.layoutParameter.addRow(parameter.name, layout)

    def insertClicked(self):
        if not self.current:
            return
        script = self.setters[self.current]
        params = {}
        for i in range(self.ui.layoutParameter.rowCount()):
            layoutItem = self.ui.layoutParameter.itemAt(i, QtWidgets.QFormLayout.LabelRole)
            paramId = layoutItem.widget().text()
            layoutItem = self.ui.layoutParameter.itemAt(i, QtWidgets.QFormLayout.FieldRole)
            getterName = layoutItem.layout().itemAt(0).widget().text().strip()
            widget = layoutItem.layout().itemAt(2).widget()
            if isinstance(widget, QtWidgets.QLineEdit):
                if getterName == "Konstante":
                    params[paramId] = f'"{widget.text()}"'
                else:
                    params[paramId] = self.stringGetter[getterName].buildCode() 
                    if widget.text():
                        params[paramId] += " + " + f'"{widget.text()}"'
            elif isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
                if getterName == "Konstante":
                    params[paramId] = str(widget.value())
                else:
                    params[paramId] = self.numberGetter[getterName].buildCode() 
                    if widget.value() != 0:
                        params[paramId] +=  ("+" if widget.value() >= 0 else "") + str(widget.value())
            elif isinstance(widget, QtWidgets.QCheckBox):
                params[paramId] = str(widget.isChecked())
        self.editor.insertPlainText(script.buildCode(params))
        self.editor.setFocus()

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

    def initScripts(self, context):
        filter = []
        if context == ScriptContext.Charakter:
            filter = ['getEigenschaftParam', 'getWaffeAT', 'getWaffeVT', 'getWaffeWürfel', 'getWaffePlus',
                      'getWaffeAT', 'getWaffeKampfstil',
                      'getEigenschaftParam', 'getWaffe', 'modifyWaffeAT', 'modifyWaffeVT', 'modifyWaffeTPWürfel',
                      'modifyWaffeTPPlus', 'modifyWaffeHärte', 'modifyWaffeRW', 'setWaffeAT', 'setWaffeVT',
                      'setWaffeTPWürfel', 'setWaffeTPPlus', 'setWaffeHärte', 'setWaffeRW', 'getWaffenWerte']
        elif context == ScriptContext.Waffeneigenschaften:
            filter = ['setSB', 'modifySB', 'setBE', 'modifyBE', 'setRS', 'modifyRS',
                      'modifyFertigkeitBasiswert', 'setKampfstil', 'modifyKampfstil', 
                      'addWaffeneigenschaft', 'removeWaffeneigenschaft']

        scripts = {}
        def addScript(script):
            if script.identifier in filter:
                return
            scripts[script.name] = script

        # ======================
        # Number getters (parameters only support default values)
        # ======================
        for attribut in self.datenbank.attribute:
            addScript(Script(f"{attribut} (Wert)", f"get{attribut}", "Attribute"))
        for ab in self.datenbank.abgeleiteteWerte:
            addScript(Script(f"{ab} (Basiswert)", f"get{ab}Basis", "Abgeleitete Werte"))
            addScript(Script(f"{ab} (mod. Wert)", f"get{ab}", "Abgeleitete Werte"))
        for en in self.datenbank.energien:
            addScript(Script(f"{en} (Basiswert)", f"get{en}Basis", "Energien"))
            addScript(Script(f"{en} (mod. Wert)", f"get{en}Mod", "Energien"))

        addScript(Script("Status", "getStatus", "Hintergrund"))
        addScript(Script("Finanzen", "getFinanzen", "Hintergrund"))
        addScript(Script("EP gesamt", "getEPGesamt", "Hintergrund"))
        addScript(Script("EP ausgegeben", "getEPAusgegeben", "Hintergrund"))

        kampfstile = ["Nahkampf", "Fernkampf"] + self.datenbank.findKampfstile()
        for kampfstil in kampfstile:
            script = Script(f"{kampfstil} AT-Mod.", f"getKampfstilAT", "Kampfstile")
            script.parameter.append(ScriptParameter("Kampfstil", str, kampfstil))
            addScript(script)
            script = Script(f"{kampfstil} VT-Mod.", f"getKampfstilVT", "Kampfstile")
            script.parameter.append(ScriptParameter("Kampfstil", str, kampfstil))
            addScript(script)
            script = Script(f"{kampfstil} Bonusschaden-Mod.", f"getKampfstilPlus", "Kampfstile")
            script.parameter.append(ScriptParameter("Kampfstil", str, kampfstil))
            addScript(script)
            script = Script(f"{kampfstil} Reichweite-Mod.", f"getKampfstilRW", "Kampfstile")
            script.parameter.append(ScriptParameter("Kampfstil", str, kampfstil))
            addScript(script)
            script = Script(f"{kampfstil} BE-Mod.", f"getKampfstilBE", "Kampfstile")
            script.parameter.append(ScriptParameter("Kampfstil", str, kampfstil))
            addScript(script)

        for i in range(1,4):
            script = Script(f"Waffeneigenschaft Parameter {i} (Zahl)", f"getEigenschaftParam", "Waffen", castType = int)
            script.parameter.append(ScriptParameter("index", int, i))
            addScript(script)
        addScript(Script("Waffe berechnete AT", f"getWaffeAT", "Waffen"))
        addScript(Script("Waffe berechnete VT", f"getWaffeVT", "Waffen"))
        addScript(Script("Waffe berechnete RW", f"getWaffeRW", "Waffen"))
        addScript(Script("Waffe berechnete Schadenswürfel", f"getWaffeWürfel", "Waffen"))
        addScript(Script("Waffe berechneter Bonusschaden", f"getWaffePlus", "Waffen"))
        addScript(Script("Waffe berechnete Härte", f"getWaffeAT", "Waffen"))

        self.numberGetter = scripts

        # ======================
        # String getters (parameters only support default values)
        # ======================
        scripts = {}

        addScript(Script("Name", "getName", "Hintergrund"))
        addScript(Script("Spezies", "getSpezies", "Hintergrund"))
        addScript(Script("Kurzbeschreibung", "getKurzbeschreibung", "Hintergrund"))
        addScript(Script("Heimat", "getHeimat", "Hintergrund"))
        for i in range(1,9):
            script = Script(f"Eigenheit {i}", f"getEigenheit", "Hintergrund")
            script.parameter.append(ScriptParameter("index", int, i))
            addScript(script)
        for i in range(1,21):
            script = Script(f"Inventar {i}", f"getInventar", "Ausrüstung")
            script.parameter.append(ScriptParameter("index", int, i))
            addScript(script)

        for i in range(1,4):
            script = Script(f"Waffeneigenschaft Parameter {i} (Text)", f"getEigenschaftParam", "Waffen")
            script.parameter.append(ScriptParameter("index", int, i))
            addScript(script)
        addScript(Script("Waffe aktiver Kampfstil", f"getWaffeKampfstil", "Waffen"))
        
        self.stringGetter = scripts

        # ======================
        # Setters
        # ======================

        scripts = {}

        script = Script("Wert abrunden", "roundDown", "Arithmetik")
        script.beschreibung = "Rundet auf die nächste ganze Zahl in Richtung 0 ab."
        script.parameter.append(ScriptParameter("Wert", float))
        addScript(script)
        script = Script("Wert aufrunden", "roundUp", "Arithmetik")
        script.beschreibung = "Rundet auf die nächst-größere (positive Zahlen)/-kleinere (negative Zahlen) ganze Zahl auf."
        script.parameter.append(ScriptParameter("Wert", float))
        addScript(script)
        script = Script("Wert runden", "round", "Arithmetik")
        script.beschreibung = "Rundet kaufmännisch zur nächsten ganzen Zahl (ab .5 auf, darunter ab)."
        script.parameter.append(ScriptParameter("Wert", float))
        addScript(script)
        script = Script("Mindestwert beschränken", "max", "Arithmetik")
        script.beschreibung = "Wenn der Wert niedriger als das angegebene Minimum ist, wird das Minimum zurückgegeben."
        script.parameter.append(ScriptParameter("Wert", float))
        script.parameter.append(ScriptParameter("Minimum", float))
        addScript(script)
        script = Script("Maximalwert beschränken", "min", "Arithmetik")
        script.beschreibung = "Wenn der Wert größer als das angegebene Maximum ist, wird das Maximum zurückgegeben."
        script.parameter.append(ScriptParameter("Wert", float))
        script.parameter.append(ScriptParameter("Maximum", float))
        addScript(script)
        script = Script("Mindest- und Maximalwert beschränken", "clamp", "Arithmetik")
        script.beschreibung = "Wenn der Wert niedriger als das angegebene Minimum ist, wird das Minimum zurückgegeben, "\
            "wenn er größer als das angebene Maximum ist das Maximum."
        script.parameter.append(ScriptParameter("Wert", float))
        script.parameter.append(ScriptParameter("Minimum", float))
        script.parameter.append(ScriptParameter("Maximum", float))
        addScript(script)

        # Abgeleitete Werte
        for ab in self.datenbank.abgeleiteteWerte:
            script = Script(f"{ab} auf neuen Wert setzen", f"set{ab}", "Abgeleitete Werte")
            script.beschreibung = "Der abgeleitete Wert wird auf den neuen Wert gesetzt, Modifikatoren werden damit ignoriert."
            script.parameter.append(ScriptParameter("Neuer Wert", int))
            addScript(script)

            script = Script(f"{ab} modifizieren", f"modify{ab}", "Abgeleitete Werte")
            script.beschreibung = "Der abgeleitete Wert wird um den angegebenen Wert modifiziert."
            script.parameter.append(ScriptParameter("Modifikator", int))
            addScript(script)

        # Energien
        for en in self.datenbank.energien:
            script = Script(f"{en} Basiswert auf neuen Wert setzen", f"set{en}Basis", "Energien")
            script.beschreibung = "Der Basiswert der Energie wird auf den neuen Wert gesetzt. Modifikatoren werden damit ignoriert."
            script.parameter.append(ScriptParameter("Neuer Wert", int))
            addScript(script)

            script = Script(f"{en} Basiswert modifizieren", f"modify{en}Basis", "Energien")
            script.beschreibung = "Der Basiswert der Energie wird um den angebenen Wert modifiziert."
            script.parameter.append(ScriptParameter("Modifikator", int))
            addScript(script)

            script = Script(f"{en} Modifikator auf neuen Wert setzen", f"set{en}Mod", "Energien")
            script.beschreibung = "Der Modifikator der Energie wird auf den neuen Wert gesetzt. Modifikatoren werden damit ignoriert."
            script.parameter.append(ScriptParameter("Neuer Wert", int))
            addScript(script)

            script = Script(f"{en} Modifikator modifizieren", f"modify{en}Mod", "Energien")
            script.beschreibung = "Der Modifikator der Energie wird um den angebenen Wert modifiziert."
            script.parameter.append(ScriptParameter("Modifikator", int))
            addScript(script)

        # Talente
        script = Script("Talent PW modifizieren", "modifyTalentProbenwert", "Talente")
        script.beschreibung = "Dieses Script ist nützlich, um permanente Erleichterungen auf ein Talent direkt in der Talentliste aufzuführen. "\
            "Ist das Talent noch nicht erworben, wird das ganze Talent mit der Modifizierung in Klammern gesetzt. Die Modifizierung wird ausschließlich im Charakterbogen eingerechnet!"
        script.parameter.append(ScriptParameter("Talent", str, completionTable = self.datenbank.talente))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Talent Info hinzufügen", "addTalentInfo", "Talente")
        script.beschreibung = "Dieses Script ist nützlich, um besondere Effekte wie beispielsweise von manchen Vorteilen direkt bei den Talenten im Charakterbogen aufzuführen."
        script.parameter.append(ScriptParameter("Talent", str, completionTable = self.datenbank.talente))
        script.parameter.append(ScriptParameter("Info", str))
        addScript(script)

        script = Script("Talent kaufen", "addTalent", "Talente")
        script.beschreibung = "Das Script fügt dem Charakter das angegebene Talent zu regulären Kosten hinzu. Wenn es in einem Vorteil verwendet wird, wird der Vorteil dem Talent, als Voraussetzung hinzugefügt. "
        "Sobald der Vorteil also abgewählt wird, verliert der Charakter auch das Talent.\n"\
        "<ul><li>Mit dem EP Kosten-Parameter können die Standard-Talentkosten geändert werden. Bei -1 werden sie nicht verändert.</li>"\
        "<li>Es kann eine übernatürliche Fertigkeit mit angegeben werden, die benötigt wird - falls der Charakter sie nicht besitzt, macht das Script nichts; diese wird dannauch als Voraussetzung hinzugefügt.</li></ul>"
        script.parameter.append(ScriptParameter("Talent", str, completionTable = self.datenbank.talente))
        script.parameter.append(ScriptParameter("EP Kosten anpassen (optional)", int, -1))
        script.parameter.append(ScriptParameter("Übern. Fertigkeit voraussetzen (optional)", str, completionTable = self.datenbank.übernatürlicheFertigkeiten))
        addScript(script)

        # Fertigkeiten
        script = Script("Fertigkeit Basiswert modifizieren", "modifyFertigkeitBasiswert", "Fertigkeiten")
        script.beschreibung = "Dieses Script ist nützlich, um sich permanente Erleichterungen auf eine Fertigkeit nicht merken zu müssen. "\
            "Diese Modifikation wird bei Voraussetzungen der Typen \"Fertigkeit\" und \"Talent\" nicht eingerechnet!"
        script.parameter.append(ScriptParameter("Fertigkeit", str, completionTable = self.datenbank.fertigkeiten))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Übernatürliche Fertigkeit Basiswert modifizieren", "modifyÜbernatürlicheFertigkeitBasiswert", "Fertigkeiten")
        script.beschreibung = "Dieses Script ist nützlich, um sich permanente Erleichterungen auf eine übernatürliche Fertigkeit nicht merken zu müssen. "\
            "Diese Modifikation wird bei Voraussetzungen der Typen \"Fertigkeit\" und \"Talent\" nicht eingerechnet!"
        script.parameter.append(ScriptParameter("Fertigkeit", str, completionTable = self.datenbank.übernatürlicheFertigkeiten))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        # Kampfstile
        script = Script("Kampfstil auf neue Werte setzen.", "setKampfstil", "Kampfstile")
        script.beschreibung = "Mit diesem Script kannst du Werteveränderungen durch einen bestimmten Kampfstil auf einen festen Wert setzen. "\
            "Diese wirken nur für Waffen, die diesen Kampfstil aktiv gesetzt haben. Modifikatoren werden damit ignoriert.\n\n"\
            "Statt eines Kampfstil-Namens kann auch \"Nahkampf\" oder \"Fernkampf\" angegeben werden, um globale Modifikationen für alle Nah-/Fernkampfwaffen anzugeben. "\
            "Diese werden dann zum tatsächlichen Kampfstil einer Waffe addiert."
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        script.parameter.append(ScriptParameter("AT", int))
        script.parameter.append(ScriptParameter("VT", int))
        script.parameter.append(ScriptParameter("Bonusschaden", int))
        script.parameter.append(ScriptParameter("RW", int))
        script.parameter.append(ScriptParameter("BE", int))
        addScript(script)

        script = Script("Kampfstilwerte modifizieren", "modifyKampfstil", "Kampfstile")
        script.beschreibung = "Mit diesem Script kannst du Werteveränderungen durch einen bestimmten Kampfstil modifizieren. "\
            "Diese wirken nur für Waffen, die diesen Kampfstil aktiv gesetzt haben.\n\n"\
            "Statt eines Kampfstil-Namens kann auch \"Nahkampf\" oder \"Fernkampf\" angegeben werden, um globale Modifikationen für alle Nah-/Fernkampfwaffen anzugeben. "\
            "Diese werden dann zum tatsächlichen Kampfstil einer Waffe addiert."
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        script.parameter.append(ScriptParameter("AT", int))
        script.parameter.append(ScriptParameter("VT", int))
        script.parameter.append(ScriptParameter("Bonusschaden", int))
        script.parameter.append(ScriptParameter("RW", int))
        script.parameter.append(ScriptParameter("BE", int))
        addScript(script)

        # Waffen
        script = Script("Waffeneigenschaft hinzufügen", "addWaffeneigenschaft", "Waffen")
        script.beschreibung = "Alle Waffen mit der angegebenen Basiswaffe erhalten die angegebene Waffeneigenschaft (wenn sie diese nicht bereits haben)."
        script.parameter.append(ScriptParameter("Waffe", str, completionTable = self.datenbank.waffen))
        script.parameter.append(ScriptParameter("Eigenschaft", str, completionTable = self.datenbank.waffeneigenschaften))
        addScript(script)

        script = Script("Waffeneigenschaft entfernen", "removeWaffeneigenschaft", "Waffen")
        script.beschreibung = "Alle Waffen mit der angegebenen Basiswaffe verlieren die angegebene Waffeneigenschaft (wenn sie diese überhaupt haben)."
        script.parameter.append(ScriptParameter("Waffe", str, completionTable = self.datenbank.waffen))
        script.parameter.append(ScriptParameter("Eigenschaft", str, completionTable = self.datenbank.waffeneigenschaften))
        addScript(script)

        weDisclaimer = " Es sind nur Waffen betroffen, die die Waffeneigenschaft mit diesesm Script haben."

        script = Script("Waffe AT auf neuen Wert setzen", "setWaffeAT", "Waffen")
        script.beschreibung = "Die AT der Waffe wird auf einen neuen Wert gesetzt. Modifikatoren werden damit ignoriert." + weDisclaimer
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe AT modifizieren", "modifyWaffeAT", "Waffen")
        script.beschreibung = "Die AT der Waffe wird um den angebenenen Wert modifiziert." + weDisclaimer
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe VT auf neuen Wert setzen", "setWaffeVT", "Waffen")
        script.beschreibung = "Die VT der Waffe wird auf einen neuen Wert gesetzt. Modifikatoren werden damit ignoriert." + weDisclaimer
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe VT modifizieren", "modifyWaffeVT", "Waffen")
        script.beschreibung = "Die VT der Waffe wird um den angebenenen Wert modifiziert." + weDisclaimer
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Schadenswürfel auf neuen Wert setzen", "setWaffeTPWürfel", "Waffen")
        script.beschreibung = "Die Schadenswürfel der Waffe werden auf einen neuen Wert gesetzt. Modifikatoren werden damit ignoriert." + weDisclaimer
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Schadenswürfel modifizieren", "modifyWaffeTPWürfel", "Waffen")
        script.beschreibung = "Die Schadenswürfel der Waffe werden um den angebenenen Wert modifiziert." + weDisclaimer
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Bonusschaden auf neuen Wert setzen", "setWaffeTPPlus", "Waffen")
        script.beschreibung = "Der Bonusschaden der Waffe wird auf einen neuen Wert gesetzt. Modifikatoren werden damit ignoriert." + weDisclaimer
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Bonusschaden modifizieren", "modifyWaffeTPPlus", "Waffen")
        script.beschreibung = "Der Bonusschaden der Waffe wird um den angebenenen Wert modifiziert." + weDisclaimer
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Härte auf neuen Wert setzen", "setWaffeHärte", "Waffen")
        script.beschreibung = "Die Härte der Waffe wird auf einen neuen Wert gesetzt. Modifikatoren werden damit ignoriert." + weDisclaimer
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Härte modifizieren", "modifyWaffeHärte", "Waffen")
        script.beschreibung = "Die Härte der Waffe wird um den angebenenen Wert modifiziert." + weDisclaimer
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Reichweite auf neuen Wert setzen", "setWaffeRW", "Waffen")
        script.beschreibung = "Die Reichweite der Waffe wird auf einen neuen Wert gesetzt. Modifikatoren werden damit ignoriert." + weDisclaimer
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Reichweite modifizieren", "modifyWaffeRW", "Waffen")
        script.beschreibung = "Die Reichweite der Waffe wird um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        self.setters = scripts

        # And some finalization work (treat categories as if it were a setting of the regular database types)...
        scriptKategorien = set()
        for script in self.numberGetter.values():
            scriptKategorien.add(script.kategorie)
        for script in self.stringGetter.values():
            scriptKategorien.add(script.kategorie)
        for script in self.setters.values():
            scriptKategorien.add(script.kategorie)
        self.scriptKategorien = {}
        i = 0
        for kategorie in sorted(list(scriptKategorien), key=Hilfsmethoden.unicodeCaseInsensitive):
            self.scriptKategorien[kategorie] = i
            i +=1

        self.numberGetterByKategorie = SortedCategoryToListDict(self.scriptKategorien)
        for script in self.numberGetter.values():
            self.numberGetterByKategorie.appendByName(script.kategorie, script.name)
        self.numberGetterByKategorie.sortValues()

        self.stringGetterByKategorie = SortedCategoryToListDict(self.scriptKategorien)
        for script in self.stringGetter.values():
            self.stringGetterByKategorie.appendByName(script.kategorie, script.name)
        self.stringGetterByKategorie.sortValues()