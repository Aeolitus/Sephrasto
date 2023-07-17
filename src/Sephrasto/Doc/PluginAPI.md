[Hilfe](Help.md) > Eigene Plugins schreiben

# Eigene Plugins schreiben
Durch die Plugin-Unterstützung kannst du tiefgehende Veränderungen an Sephrasto vornehmen, z.B. den Charaktereditor anpassen oder Berechnungen verändern. Plugins haben vollen Zugriff auf alle Sephrasto-Dateien und können Objekt-Zustände auslesen oder verändern. Für Nutzer-Interaktion können dem Hauptfenster Buttons und dem Charaktereditor Tabs hinzugefügt werden, die mittels Qt eigene UIs darstellen können. Um über künftige Sephrasto-Versionen hinweg und mit anderen Plugins kompatibel zu bleiben, sollten Plugins nach Möglichkeit nur über soganannte Actions und Filter mit Sephrasto interagieren und sonst nur lesend auf die Sephrasto-Objekte zugreifen.
<br />
## Vorbereitung
Theoretisch brauchst du nicht mehr als Notepad um loslegen zu können. Kleine Dinge wie die EP-Kosten für AsP oder die Anzahl der kostenlosen freien Fertigkeiten anzupassen geht so ohne Probleme. Sobald du aber etwas aufwändigere Dinge tun möchtest, insbesondere eigene Tabs/Fenster einbauen, solltest du Qt Creator, Python und eine Entwicklungsumgebung installieren und das Sephrasto-Repository klonen, siehe hier: https://github.com/Aeolitus/Sephrasto/blob/master/README.md
<br />
## Actions und Filter
Actions und Filter können verwendet werden auf Vorgänge zu reagieren oder Daten zu manipulieren. Das System funktioniert über die statische EventBus-Klasse. Actions und Filter haben beide als ersten Parameter immer den Namen, der natürlich einzigartig sein sollte. Um Actions oder Filter zu "abonnieren" muss neben dem Namen als zweiter Parameter immer ein Handler/Callback mitgereicht werden.
<br />
<br />
__Actions__ sind einfache Nachrichten, die optional mit einem Parameter-Dictionary versendet werden können.
<br />
<br />
__Action absenden:__
```python
EventBus.doAction("charaktereditor_oeffnet", { "neu" : False })
```
__Action abonnieren:__
```python
EventBus.addAction("charaktereditor_oeffnet", self.charakterEditorOeffnet)
def charakterEditorOeffnet(self, params):
    self.meinTab = MeinTabWrapper.MeinTabWrapper()
```

__Filter__ haben beim Absender als zweiten Parameter immer einen Wert, der durch den Handler modifiziert werden kann und returned werden muss. Optional kann als dritter Parameter ein Parameter-Dictionary mitgesendet werden. Da der zu filternde Wert durch mehrere Handler laufen kann, spielt die Reihenfolge der Filter eine Rolle. Daher kann beim Abonnieren zusätzlich eine Priorität hinzugefügt werden - je niedriger die Zahl, desto früher wird der Filter aufgerufen (default: 0).
<br />
<br />
__Filter absenden:__
```python
val = EventBus.applyFilter("talent_kosten", val, { "talent": tal })
```
__Filter abonnieren:__
```python
EventBus.addFilter("talent_kosten", self.talentKostenFilter)
def talentKostenFilter(self, val, params):
    if params["talent"] == "Schmieden":
        return val + 10
```

## Actions, die Sephrasto absendet
- "charakter_instanziiert" (Parameter: { "charakter" : Char })<br />
Zweck: Charakter modifizieren, nachdem er instanziiert, aber bevor er geladen und aktualisiert wurde. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "charaktereditor_oeffnet" (Parameter: { "neu" : bool, "filepath" : string })<br />
Zweck: Form und Wrapper für eigene Charakter-Editor Tabs initialisieren. Der neu Parameter enthält die Information, ob es sich um einen neuen Charakter handelt. Der filepath Parameter enthält den Pfad der Charakterdatei oder einen leeren string, falls ein neuer Charakter erstellt wird.
- "charaktereditor_geoeffnet" (Parameter: { "neu" : bool, "filepath" : string })<br />
Zweck: Beliebige Aktion durchführen, nachdem der CharakterEditor vollständig initialisiert wurde. Der neu Parameter enthält die Information, ob es sich um einen neuen Charakter handelt. Der filepath Parameter enthält den Pfad der Charakterdatei oder einen leeren string, falls ein neuer Charakter erstellt wurde.
- "charakter_xml_geladen" (Parameter: { "charakter" : Char, "xmlRoot" : etree.Element })<br />
Zweck: Daten aus der Charakterdatei auslesen oder modifizieren, nachdem Sephrasto sie gelesen hat. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "plugins_geladen"<br />
Zweck: Nach dieser Action sind alle Plugins initialisiert. Kann verwendet werden um mit anderen Plugins zu kommunizieren, um z.B. mit einer Action andere Plugins darüber in Kenntnis zu setzen, dass dieses Plugin vorhanden ist.
- "pre_charakter_aktualisieren" (Parameter: { "charakter" : Char })<br />
Zweck: Beliebige Aktion durchführen, nachdem die Charakterwerte in irgendeiner Form modifiziert wurden, aber bevor die Veränderungen berechnet werden. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "charakter_aktualisieren_vorteilscripts" (Parameter: { "charakter" : Char })<br />
Zweck: Wird während der Charakteraktualisierung nach der Berechnung des Basiswerte und vor der Ausführung der Vorteilskripte aufgerufen. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "charakter_aktualisieren_fertigkeiten" (Parameter: { "charakter" : Char })<br />
Zweck: Wird während der Charakteraktualisierung nach der Ausführung der Vorteilskripte und vor der Aktualisierung der Fertigkeiten aufgerufen. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "charakter_aktualisieren_waffenwerte" (Parameter: { "charakter" : Char })<br />
Zweck: Wird während der Charakteraktualisierung nach allen Berechnungen außer den Waffenwerten aufgerufen. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "post_charakter_aktualisieren" (Parameter: { "charakter" : Char })<br />
Zweck: Beliebige Aktion durchführen, nachdem die Charakterwerte in irgendeiner Form modifiziert und berechnet wurden. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "vorteil_entfernt" (Parameter:  { "charakter" : Char, "name" : string })<br />
Zweck: Aktionen durchführen, die nicht mit der Vorteil-Script-API möglich sind. Der "name" Parameter enthält den Namen des Vorteils. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "vorteil_gekauft" (Parameter: { "charakter" : Char, "name" : string })<br />
Zweck: Aktionen durchführen, die nicht mit der Vorteil-Script-API möglich sind. Der "name" Parameter enthält den Namen des Vorteils. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "pdf_geschrieben" (Parameter: { "filepath" : string })<br />
Zweck: Aktion durchführen, nachdem die Charakter-PDF geschrieben wurde, z.B. eine weitere PDF schreiben. Der Parameter enthält den Dateinamen der Charakter-PDF mit absolutem Pfad.
- "basisdatenbank_geladen" (Parameter: { "datenbank" : Datenbank, "isCharakterEditor" : bool })<br />
Zweck: Elemente der Basisdatenbank anpassen/hinzufügen/löschen, bevor die Hausregel-Datenbank geladen wird. Ein übliches Beispiel ist das Hinzufügen von DatenbankEinstellung-Elementen, mit welchen das Plugin konfiguriert werden kann.
- "datenbank_geladen" (Parameter: { "datenbank" : Datenbank, "isCharakterEditor" : bool })<br />
Zweck: Aktion durchführen, nachdem die Datenbank inkl. Hausregeldatenbank komplett geladen wurde. Eine Referenz auf das Datenbank-Objekt erhalten.
- "regelanhang_anfuegen" (Parameter: { "reihenfolge" : string, "appendCallback" : Python-Funktion })<br />
Zweck: Dem Regelanhang weiteren Text hinzufügen. Dies geschieht über den Parameter "appendCallback", einer Pythonfunktion die den Kategorienamen und den Text als Funktionsparameter hat. Der Kategoriename kann auch auf einen leeren string gesetzt werden. Die Action wird mehrmals aufgerufen, der "reihenfolge" Parameter sollte genutzt werden, um den Text an der richtigen Stelle einzufügen. Er entspricht einem Eintrag in der Datenbank-Einstellung "Regelanhang: Reihenfolge".
- "dbe_menuitems_erstellen" (Parameter: { "addMenuItemCB" : Python-Funktion })<br />
Zweck: Dem Datenbankeditor-Menu Einträge hinzufügen. Rufe dazu den addMenuItemCB auf. Er benötigt zwei Parameter: Der erste ist der Name des Menus, der zweite eine QAction.
<br />
## Actions, die Sephrasto abonniert
- "charaktereditor_reload" (Parameter: { "name" : string })<br />
Zweck: Einen Toplevel-Tab des Charaktereditors neu initialisieren. Der name Parameter enthält den Namen des Tabs.
- "charaktereditor_modified"<br />
Zweck: Aktualisiert den Charakter und die EP und beim Schließen des Charaktereditors wird ein Popup angezeigt, das über ungespeicherte Änderungen mitteilt
<br />
## Filter, die Sephrasto absendet
- "pdf_concat" (Filter: filePaths : array of string)<br />
Zweck: Sephrasto fügt zum Schluss alle generierten Einzelseiten zusammen. Diese Liste von Einzelseiten kann hiermit manipuliert werden, z.B. um weitere Seiten einzufügen.
- "pdf_export" (Filter: pdfFields : dict of {string : string})<br />
Zweck: von Sephrasto generierte PDF-Felder vor dem Exportieren der PDF modifizieren
- "pdf_export_extrapage" (Filter: pdfFields : dict of {string : string})<br />
Zweck: von Sephrasto generierte PDF-Felder vor dem Exportieren der PDF modifizieren. Wird nur für Extraseiten aufgerufen, wenn diese nötig sind. Sie enthalten nur die Felder für übernatürliche Fertigkeiten, Talente und Vorteile.
- "charakter_xml_laden" (Filter: xmlRoot : etree.Element, Parameter: { "charakter" : Char })<br />
Zweck: Daten aus der Charakterdatei auslesen oder modifizieren, bevor Sephrasto sie liest. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "charakter_xml_schreiben" (Filter: xmlRoot : etree.Element, Parameter: { "charakter" : Char, "filepath" : string })<br />
Zweck: Der Charakterdatei Daten hinzufügen oder Daten modifizieren, bevor Sephrasto die Datei schreibt. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "datenbank_xml_laden" (Filter: xmlRoot : etree.Element, Parameter: { "datenbank" : Datenbank, "basisdatenbank" : bool, "conflictCallback" : Python-Funktion })<br />
Zweck: Datenbank-Datei auslesen, nachdem Sephrasto sie gelesen hat. Der "basisdatenbank"-Parameter enthält die Information, ob es sich um die Basisdatenbank- oder eine Hausregeldatenbank-Datei handelt. Der "conflictCallback"-Parameter ist nur gesetzt wenn basisdatenbank=false und kann ausgeführt werden, um beim Laden mehrerer Hausregeldatenbanken Konflikte eigener Datenbanktypen aufzulösen. Hierzu werden dem Callback der Name des Datenbanktyps, die alte sowie die neue Version des Elements als parameter übergeben, siehe Datenbank.py.
- "datenbank_xml_schreiben" (Filter: xmlRoot : etree.Element, Parameter: { "datenbank" : Datenbank })<br />
Zweck: Der Datenbankdatei Daten hinzufügen oder Daten modifizieren, bevor Sephrasto die Datei schreibt.
- "datenbank_verify", (Filter: loadingErrors : array, Parameter: { "datenbank" : Datenbank, "isCharakterEditor" : bool }) <br />
Zweck: Eigene Datentypen verifizieren und bei Fehlern dem loadingErrors array hinzufügen, damit diese in der Fehlerliste des Datenbankeditors erscheinen.
- "datenbank_editor_typen" (Filter: databaseTypes : dict of { Class : DatenbankEdit.DatenbankTypWrapper } )<br />
Zweck: Dem Datenbankeditor weitere Datentypen hinzufügen. Zusätzlich muss via datenbank_geladen in datenbank.tablesByType die Datenbankelement-Tabelle eingetragenwerden.
- "set_charakterbogen" (Filter: filePath : string)<br />
Zweck: Den vom Nutzer gewählten Charakterbogen modifizieren, z.B. den Pfad der Datei anpassen um einen Charakterbogen aus dem Plugin zu verwenden. Achtung: Im Ordner des Charakterbogens muss sich eine gleichnamige Datei mit der Endung ".ini" befinden. Siehe Sephrasto/Data/Charakterbögen/Standard Charakterbogen.ini als Beispiel für deren Inhalt.
- "energie_kosten" (Filter: kosten: int, Parameter: { "charakter" : Char, "wertVon" : int, "wertAuf" : int })<br />
Zweck: Die Kosten für AsP-Steigerungen anpassen. Der "wert" Parameter enthält die Anzahl zugekaufter AsP. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "attribut_kosten" (Filter: kosten: int, Parameter: { "charakter" : Char, "attribut" : string, "wertVon" : int, "wertAuf" : int })<br />
Zweck: Die Kosten für Attributs-Steigerungen anpassen. Die Parameter enthalten den Namen des Attributs und dessen Wert. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "fertigkeit_kosten" (Filter: kosten: int, Parameter: { "charakter" : Char, "name" : string, "wertVon" : int, "wertAuf" : int })<br />
- "freiefertigkeit_kosten" (Filter: kosten: int, Parameter: { "charakter" : Char, "name" : string, "wertVon" : int, "wertAuf" : int })<br />
Zweck: Die Kosten für freie Fertigkeiten anpassen. Die Parameter enthalten den Namen der freien Fertigkeit und die Stufe. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "talent_kosten" (Filter: kosten: int, Parameter: { "charakter" : Char, "talent" : string })<br />
Zweck: Die Kosten für Talente anpassen. Der "talent" Parameter enthält den Namen des Talents. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "vorteil_kosten" (Filter: kosten: int, Parameter: { "charakter" : Char, "vorteil" : string })<br />
Zweck: Die Kosten für Vorteile anpassen. Der "vorteil" Parameter enthält den Namen des Vorteils. Auf den Charakter sollte nur über den "charakter" Parameter zugegriffen werden, nicht über Wolke.Char.
- "ruestung_be" (Filter: be: int, Parameter: { "name" : string })<br />
Zweck: Die BE einer Rüstung des Rüstungauswahlfensters anpassen. Achtung: Da Rüstungen ergänzt werden können und die Namen dann konkateniert werden, sollte der name via "in" abgefragt werden (bspw. if "Leichte Platte" in name).
- "regelanhang_reihenfolge_name" (Filter: name : string)<br />
Zweck: Wenn der Datenbank-Einstellung "Regelanhang: Reihenfolge" neue Kürzel hinzugefügt werden, kann mit diesem Filter der volle Name für das Kürzel angegeben werden, damit es im Info-Tab bei den Regelanhangkategorien verständlich dargestellt wird. Der anfängliche Filterwert entspricht dem Kürzel.
- Die folgenden Filter haben alle eine Gemeinsamkeit:  Der Filterwert ist eine Wrapperklasse eines der UI-Tabs oder Auswahlfenster. Im Filter kann der Wrapper komplett ersetzt oder beerbt werden, um die Sephrasto-UI anzupassen.
	* "class_beschreibung_wrapper" (Filter: BeschrWrapper : class)
	* "class_beschreibung_details_wrapper" (Filter: CharakterBeschreibungDetailsWrapper : class)
	* "class_attribute_wrapper" (Filter: AttrWrapper : class)
	* "class_fertigkeiten_wrapper" (Filter: FertigkeitenWrapper : class)
	* "class_profanefertigkeiten_wrapper" (Filter: ProfaneFertigkeitenWrapper : class)
	* "class_freiefertigkeiten_wrapper" (Filter: CharakterFreieFertWrapper : class)
	* "class_uebernatuerlichefertigkeiten_wrapper" (Filter: UebernatuerlichWrapper : class)
	* "class_ausruestung_wrapper" (Filter: EquipWrapper : class)
	* "class_waffen_wrapper" (Filter: CharakterWaffenWrapper : class)
	* "class_inventar_wrapper" (Filter: CharakterInventarWrapper : class)
	* "class_vorteile_wrapper" (Filter: CharakterVorteileWrapper : class)
	* "class_info_wrapper" (Filter: InfoWrapper : class)
	* "class_waffenpicker_wrapper" (Filter: WaffenPicker : class)
	* "class_ruestungspicker_wrapper" (Filter: RuestungPicker : class)
	* "class_freiefertigkeitenpicker_wrapper" (Filter: CharakterFreieFertigkeitenPickerWrapper : class)
	* "class_talentpicker_wrapper" (Filter: TalentPicker : class)
- Das gleiche gilt für die Hausregeleditor-Fenster:
    * "dbe_class_abgeleiteterwertdefinition_wrapper" (Filter: DatenbankEditAbgeleiteterWertWrapper : class)
    * "dbe_class_attributdefinition_wrapper" (Filter: DatenbankEditAttributWrapper : class)
    * "dbe_class_datenbankeinstellung_wrapper" (Filter: DatenbankEditEinstellungWrapper : class)
    * "dbe_class_energiedefinition_wrapper" (Filter: DatenbankEditEnergieWrapper : class)
    * "dbe_class_profanefertigkeitdefinition_wrapper" (Filter: DatenbankEditProfaneFertigkeitWrapper : class)
    * "dbe_class_uebernatuelichefertigkeitdefinition_wrapper" (Filter: DatenbankEditUebernatürlicheFertigkeitWrapper : class)
    * "dbe_class_freiefertigkeitdefinition_wrapper" (Filter: DatenbankEditFreieFertigkeitWrapper : class)
    * "dbe_class_regel_wrapper" (Filter: DatenbankEditRegelWrapper : class)
    * "dbe_class_ruestungdefinition_wrapper" (Filter: DatenbankEditRuestungWrapper : class)
    * "dbe_class_talentdefinition_wrapper" (Filter: DatenbankEditTalentWrapper : class)
    * "dbe_class_vorteildefinition_wrapper" (Filter: DatenbankEditVorteilWrapper : class)
    * "dbe_class_waffedefinition_wrapper" (Filter: DatenbankEditWaffeWrapper : class)
    * "dbe_class_waffeneigenschaftdefinition_wrapper" (Filter: DatenbankEditWaffeneigenschaftWrapper : class)

## Neues Plugin erstellen
- Gehe in deinen `Dokumente/Sephrasto/Plugins` Ordner
- Lege einen neuen Ordner mit deinem Pluginnamen an (keine Leerzeichen)
- Erstelle in diesem Ordner eine Datei mit dem Namen `__init__.py`
- Erstelle in dieser Datei eine Klasse mit dem Namen `Plugin` und importiere den `EventBus`
- Falls du Action oder Filter Handler registrieren möchtest, stelle sicher, dass sie über die gesamte Programm-Dauer bestehen bleiben. Vermeide es also beispielsweise Handler in einem UI Wrapper zu registrieren, den du jedes mal neu erstellst, wenn ein neuer Charakter geladen wird oder ein Hauptfenster-Button geclickt wird. Stattdessen kannst du den Handler in deiner `__init__.py` registrieren und dann eine Funktion auf dem aktuellen Wrapper aufrufen.
- Optional: Füge die Funktion getDescription ein und gib einen Beschreibungs-String zurück - dieser wird in den Sephrasto-Einstellungen als Tooltip angezeigt.
- Optional: Füge die Funktion changesCharacter ein und gib True zurück, falls dein Plugin die Charakterdaten ändert. Falls ein Charakter mit diesem Plugin erstellt wurde und dann ohne Plugin geöffnet wird, erscheint dann ein Warndialog.
- Optional: Füge die Funktion changesDatabase ein und gib True zurück, falls dein Plugin die Datenbank ändert. Falls Hausregeln mit diesem Plugin erstellt wurden und dann ohne Plugin geöffnet werden, erscheint dann ein Warndialog.
<br />
```python
from EventBus import EventBus

class Plugin:
    def __init__(self):
        EventBus.addAction(...
		
	@staticmethod
	def getDescription():
		return "Mein erstes Plugin"
		
	def changesCharacter(self):
        return True
        
    def changesDatabase(self):
        return True
```

## Charaktereditor Tab hinzufügen
Implementiere in deiner Plugin-Klasse eine Funktion mit dem Namen `createCharakterTabs` und returne eine Liste von Tabs. Importiere hierzu die Tab-Klasse aus dem Charaktereditor.
- Der erste Konstruktor-Parameter der Tabklasse legt die relative Reihenfolge fest, in welcher der Tab eingefügt wird - die Sephrasto Tabs haben Reihenfolge-Werte in 10er-Schritten, beginnend bei 10.
- Der zweite Parameter ist deine UI-Wrapper-Klasse, die optional ein `modified` Signal definieren kann. Mit dem Signal kann Sephrasto darüber in Kenntnis gesetzt werden, dass sich etwas am Charakter verändert hat, um bei Bedarf das Warn-Popup zu öffnen, wenn der Charakter geschlossen wird oder um das EP-Widget zu aktualisieren. Zudem kann sie optional die Funktionen load und update implementieren. Beide werden von Sephrasto zu passenden Zeitpunkten aufgerufen und sollten genutzt werden, um die UI Widgets zu befüllen (load) oder den Charakter mit den UI Widget-Werten zu aktualisieren (update).
- Der dritte Parameter ist die vom QtCreator generierte UI Form.
- Der vierte Parameter ist der Titel des Tabs.
<br />
```python
from EventBus import EventBus
from MeinPlugin import MeinTabWrapper

class Plugin:
    def __init__(self):
	self.meinTab = None
        EventBus.addAction("charaktereditor_oeffnet", self.charakterEditorOeffnet)
        
    def charakterEditorOeffnet(self, params):
        self.meinTab = MeinTabWrapper.MeinTabWrapper()

    def createCharakterTabs(self):
        #Füge einen Tab mit Titel "Mein Tab" an zweiter Stelle ein.
        tab = Tab(15, self.meinTab, self.meinTab.form, "Mein Tab")
        return [tab]

#Datei MeinTabWrapper.py im Plugin-Ordner
from PySide6 import QtWidgets, QtCore, QtGui
from MeinPlugin import MeinTab

class MeinTabWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = MeinTab.Ui_Form()
        self.ui.setupUi(self.form)
        self.ui.lineEditName.textChanged.connect(self.changed)
    
    def changed(self):
        self.modified.emit()
		
	def load(self):
	    pass
		
	def update(self):
	    pass
```

## Hauptfenster oder Charaktereditor Button hinzufügen
Implementiere in deiner Plugin-Klasse eine Funktion mit dem Namen `createMainWindowButtons` oder `createCharakterButtons` und returne eine Liste von (Button) Widgets. Im `clicked` Event der widgets kannst du einen Handler registrieren, der dann beispielsweise ein neues Fenster zeigt.
<br />
```python
from PySide6 import QtWidgets, QtCore, QtGui
from EventBus import EventBus
from MeinPlugin import MeinFensterWrapper

class Plugin:
    def __init__(self):
        self.meinFensterButton = None
        self.meinFenster = None

    def createMainWindowButtons(self):
        self.meinFensterButton = QtWidgets.QPushButton()
        self.meinFensterButton.setProperty("class", "icon")
        self.meinFensterButton.setText("\uf6f0") #font awesome icon
        self.meinFensterButton.clicked.connect(self.createMeinFenster)
        return [self.meinFensterButton]
        
    def createMeinFenster(self):
        self.meinFenster = MeinFensterWrapper.MeinFensterWrapper()
        self.meinFenster.form.show()

#Datei MeinFensterWrapper.py im Plugin-Ordner
from PySide6 import QtWidgets, QtCore, QtGui
from MeinPlugin import MeinFenster

class MeinFensterWrapper(QtCore.QObject):   
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = MeinFenster.Ui_Form() # mit qt creator erstellte form
        self.ui.setupUi(self.form)
```

## Datenbankeditor Menueintrag hinzufügen
Für in deiner Plugin-Klasse einen handler für die Action `dbe_menuitems_erstellen` hinzu und hole den addMenuItemCB aus den parametern. Mit diesem Callback kannst du QActions in ein beliebiges Menu des Datenbankeditors einfügen.
<br />
```python
from PySide6 import QtGui
from EventBus import EventBus
class Plugin:
    def __init__(self):
        EventBus.addAction("dbe_menuitems_erstellen", self.menusErstellen)

    def menusErstellen(self, params):
        addMenuItemCB = params["addMenuItemCB"]
        self.exportDB = QtGui.QAction("Mein Export")
        self.exportDB.triggered.connect(self.export)
        addMenuItemCB("Export", self.export)
        
    def export(self):
        [...]
```

## Dem Plugin in den Sephrasto-Einstellungen einen eigenen Einstellungsdialog hinzufügen
Füge die Funktion showSettings ein und zeige ein beliebiges Fenster oder nutze Sephrastos SimpleSettingsDialog. Dieser kümmert sich automatisch um das Darstellen, Laden und Speichern der Einstellungen in der Sephrasto.ini über die `addSetting` Funktion.
<br />
```python
from PySide6 import QtWidgets
from QtUtils.SimpleSettingsDialog import SimpleSettingsDialog
class Plugin:
    def showSettings(self):
        dlg = SimpleSettingsDialog("Mein Plugin Einstellungen")
        dlg.addSetting("MeinPlugin_Checkbox", "Checkboxoption", QtWidgets.QCheckBox())
        dlg.addSetting("MeinPlugin_Spinbox", "Spinboxoption", QtWidgets.QSpinBox())
        dlg.addSetting("MeinPlugin_Text", "Textoption", QtWidgets.QLineEdit())
        combobox = QtWidgets.QComboBox()
        combobox.addItems(["OptionA", "Option B", "Option C"])
        dlg.addSetting("MeinPlugin_Combobox", "Comboboxoption", combobox)
        dlg.show()
```

## Existierende UI anpassen
Implementiere einen der "class_xx_wrapper" Filter, die UI-Wrapper-Klasse wird als Parameter gereicht. Du kannst diesen Parameter im Handler beerben und diese oder eine ganz neue Klasse returnen. Im folgenden Beispiel wird bei den freien Fertigkeiten die dritte Stufe entfernt.
<br />
```python
from PySide6 import QtWidgets, QtCore, QtGui
from EventBus import EventBus

class Plugin:
    def __init__(self):
	EventBus.addFilter("class_freiefertigkeiten_wrapper", self.provideFreieFertigkeitenWrapper)
	
    def provideFreieFertigkeitenWrapper(self, base, params):
        class MeinFreieFertigkeitenWrapper(base):
            def __init__(self):
                super().__init__()
                ffCount = 0
                for row in range(1,8):
                    for column in range(1,5):
                        ffCount +=1
                        combo = getattr(self.uiFert, "comboFF" + str(ffCount))
                        combo.clear()
                        combo.addItem("I")
                        combo.addItem("II")

        return MeinFreieFertigkeitenWrapper
```