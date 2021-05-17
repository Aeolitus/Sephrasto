
# Plugin API

## Was kann ich mit Plugins machen?
Plugins haben vollen Zugriff auf alle Sephrasto und können Objekt-Zustände auslesen oder verändern. Für Nutzer-Interaktion können dem Hauptfenster Buttons und dem Charaktereditor Tabs hinzugefügt werden, die mittels Qt eigene UIs darstellen können. Um über künftige Sephrasto-Versionen hinweg und mit anderen Plugins kompatibel zu bleiben, sollten Plugins nach Möglichkeit nur über soganannte Actions und Filter mit Sephrasto interagieren und sonst nur lesend auf die Sephrasto-Objekte zugreifen.

## Vorbereitung
Theoretisch brauchst du nicht mehr als Notepad um loslegen zu können. Kleine Dinge wie die EP-Kosten für AsP oder die Anzahl der kostenlosen freien Fertigkeiten anzupassen geht so ohne Probleme. Sobald du aber etwas aufwändigere Dinge tun möchtest, insbesondere eigene Tabs/Fenster einbauen, solltest du Qt Creator, Python und eine Entwicklungsumgebung installieren und das Sephrasto-Repository klonen, siehe hier: https://github.com/Aeolitus/Sephrasto/blob/master/README.md

## Actions und Filter
Actions und Filter können verwendet werden auf Vorgänge zu reagieren oder Daten zu manipulieren. Das System funktioniert über die statische EventBus-Klasse. Actions und Filter haben beide als ersten Parameter immer den Namen, der natürlich einzigartig sein sollte. Um Actions oder Filter zu "abonnieren" muss neben dem Namen als zweiter Parameter immer ein Handler/Callback mitgereicht werden.

__Actions__ sind einfache Nachrichten, die optional mit einem Parameter-Dictionary versendet werden können.

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

## Vorhandene Actions
- "charakter_geladen"
Zweck: Beliebige Aktion durchführen, nachdem eine Charakterdatei vollständig geladen wurde.
- "charaktereditor_oeffnet" (Parameter: { "neu" : bool })
Zweck: Form und Wrapper für eigene Charakter-Editor Tabs initialisieren. Der Parameter enthält die Information, ob es sich um einen neuen Charakter handelt.
- "plugins_geladen"
Zweck: Nach dieser Action sind alle Plugins initialisiert. Kann verwendet werden um mit anderen Plugins zu kommunizieren, um z.B. mit einer Action andere Plugins darüber in Kenntnis zu setzen, dass dieses Plugin vorhanden ist.
- "pre_charakter_aktualisieren"
Zweck: Beliebige Aktion durchführen, nachdem die Charakterwerte in irgendeiner Form modifiziert wurden, aber bevor die Veränderungen berechnet werden.
- "post_charakter_aktualisieren"
Zweck: Beliebige Aktion durchführen, nachdem die Charakterwerte in irgendeiner Form modifiziert und berechnet wurden.
- "vorteil_entfernt"  (Parameter:  { "name" : string })
Zweck: Aktionen durchführen, die nicht mit der Vorteil-Script-API möglich sind. Der Parameter enthält den Namen des Vorteils.
- "vorteil_gekauft"  (Parameter: { "name" : string })
Zweck: Aktionen durchführen, die nicht mit der Vorteil-Script-API möglich sind. Der Parameter enthält den Namen des Vorteils.
- "pdf_geschrieben" (Parameter: { "filename" : string })
Zweck: Aktion durchführen, nachdem die Charakter-PDF geschrieben wurde, z.B. eine weitere PDF schreiben. Der Parameter enthält den Dateinamen der Charakter-PDF mit absolutem Pfad.

## Vorhandene Filter
- "pdf_export" (Filter: pdfFields : dict)
Zweck: von Sephrasto generierte PDF-Felder vor dem Exportieren der PDF modifizieren
- "charakter_xml_laden" (Filter: xmlRoot : etree.Element)
Zweck: Daten aus der Charakterdatei auslesen oder modifizieren, bevor Sephrasto sie liest.
- "charakter_xml_schreiben" (Filter: xmlRoot : etree.Element)
Zweck: Der Charakterdatei Daten hinzufügen oder Daten modifizieren, bevor Sephrasto die Datei schreibt.
- "freiefertigkeit_num_kostenlos" (Filter: num : int)
Zweck: Die Anzahl der kostenlosen Freien Fertigkeiten modifizieren
- "set_charakterbogen" (Filter: charakterBogen : CharakterBogenInfo)
Zweck: Den vom Nutzer gewählten Charakterbogen modifizieren, z.B. den Pfad der Datei anpassen um einen Charakterbogen aus dem Plugin zu verwenden.
- "asp_kosten" (Filter: kosten: int, Parameter: { "wert" : int }).
Zweck: Die Kosten für AsP-Steigerungen anpassen. Der Parameter enthält die Anzahl zugekaufter AsP.
- "kap_kosten" (Filter: kosten: int, Parameter: { "wert" : int })
Zweck: Die Kosten für KaP-Steigerungen anpassen. Der Parameter enthält die Anzahl zugekaufter KaP.
- "attribut_kosten" (Filter: kosten: int, Parameter: { "attribut" : string, "wert" : int })
Zweck: Die Kosten für Attributs-Steigerungen anpassen. Die Parameter enthalten den Namen des Attributs und dessen Wert.
- "freiefertigkeit_kosten" (Filter: kosten: int, Parameter: { "name" : string, "wert" : int })
Zweck: Die Kosten für freie Fertigkeiten anpassen. Die Parameter enthalten den Namen der freien Fertigkeit und die Stufe.
- "talent_kosten" (Filter: kosten: int, Parameter: { "talent" : string })
Zweck: Die Kosten für Talente anpassen. Der Parameter enthält den Namen des Talents.
- "waffe_haerte_wsstern" (Filter: applizieren: bool, Parameter: { "waffe" : Waffe })
Zweck: Bei bestimmten Waffen die Härte auf WS* setzen oder dies verhindern. Default: wird bei der Waffe Unbewaffnet appliziert. Der Parameter enthält das Waffe-Objekt (siehe Objekte.py), um das es geht.
- "waffe_vt_erlaubt" (Filter: vtErlaubt: bool, Parameter: { "waffe" : Waffe })
Zweck: Bei bestimmten Waffen die VT erlauben oder nicht erlauben (= in der PDF auf "-" setzen). Default: wird bei Fernkampfwaffen und Lanzenreiten nicht erlaubt. Der Parameter enthält das Waffe-Objekt (siehe Objekte.py), um das es geht.
- "waffe_schadensbonus_wirkt" (Filter: wirkt: bool, Parameter: { "waffe" : Waffe })
Zweck: Bei bestimmten Waffen den Schadensbonus applizieren oder entfernen. Default: wirkt bei Nahkampfwaffen. Der Parameter enthält das Waffe-Objekt (siehe Objekte.py), um das es geht.
- Die folgenden Filter haben alle eine Gemeinsamkeit:  Der Filterwert ist eine Wrapperklasse eines der UI-Tabs. Im Filter kann der Wrapper komplett ersetzt oder beerbt werden, um die Sephrasto-UI anzupassen.
-- "class_beschreibung_wrapper" (Filter: BeschrWrapper : class)
-- "class_attribute_wrapper" (Filter: AttrWrapper : class)
-- "class_fertigkeiten_wrapper" (Filter: FertigkeitenWrapper : class)
-- "class_freiefertigkeiten_wrapper" (Filter: CharakterFreieFertWrapper : class)
-- "class_uebernatuerlichefertigkeiten_wrapper" (Filter: UebernatuerlichWrapper : class)
-- "class_ausruestung_wrapper" (Filter: EquipWrapper : class)
-- "class_vorteile_wrapper" (Filter: CharakterVorteileWrapper : class)
-- "class_items_wrapper" (Filter: CharakterItemsWrapper : class)
-- "class_ep_wrapper" (Filter: EPWrapper : class)

## Neues Plugin erstellen
- Gehe in deinen `Dokumente/Sephrasto/Plugins` Ordner
- Lege einen neuen Ordner mit deinem Pluginnamen an (keine Leerzeichen)
- Erstelle in diesem Ordner eine Datei mit dem Namen `__init__.py`
- Erstelle in dieser Datei eine Klasse mit dem Namen `Plugin` und importiere den `EventBus`:
- Falls du Action oder Filter Handler registrieren möchtest, stelle sicher, dass sie über die gesamte Programm-Dauer bestehen bleiben. Vermeide es also beispielsweise Handler in einem UI Wrapper zu registrieren, den du jedes mal neu erstellst, wenn ein neuer Charakter geladen wird oder ein Hauptfenster-Button geclickt wird. Stattdessen kannst du den Handler in deiner `__init__.py` registrieren und dann eine Funktion auf dem aktuellen Wrapper aufrufen.

```python
from EventBus import EventBus

class Plugin:
    def __init__(self):
        pass
```

## Charaktereditor Tab hinzufügen
Implementiere in deiner Plugin-Klasse eine Funktion mit dem Namen `createCharakterTabs` und returne eine Liste von Tabs. Importiere hierzu die Tab-Klasse aus dem Charaktereditor. Der erste Konstruktor-Parameter der Tabklasse legt die relative Reihenfolge fest, in welcher der Tab eingefügt wird - die Sephrasto Tabs haben Reihenfolge-Werte in 10er-Schritten, beginnend bei 10. Der zweite Parameter ist deine UI-Wrapper-Klasse, die optional ein `modified` Signal definieren. Mit dem Signal kann Sephrasto darüber in Kenntnis gesetzt werden, dass sich etwas am Charakter verändert hat, um bei Bedarf das Warn-Popup zu öffnen, wenn der Charakter geschlossen wird oder um das EP-Widget zu aktualisieren. Der dritte Parameter ist die vom QtCreator generierte UI Form. Der vierte Parameter ist der Titel des Tabs.

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
from PyQt5 import QtWidgets, QtCore, QtGui
from MeinPlugin import MeinTab

class MeinTabWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = MeinTab.Ui_Form()
        self.ui.setupUi(self.form)
        self.ui.lineEditName.textChanged.connect(self.changed)
    
    def changed(self):
        self.modified.emit()
```

## Hauptfenster oder Charaktereditor Button hinzufügen
Implementiere in deiner Plugin-Klasse eine Funktion mit dem Namen `createMainWindowButtons` oder `createCharakterButtons` und returne eine Liste von (Button) Widgets. Im `clicked` Event der widgets kannst du einen Handler registrieren, der dann beispielsweise ein neues Fenster zeigt.

```python
from PyQt5 import QtWidgets, QtCore, QtGui
from EventBus import EventBus
from MeinPlugin import MeinFensterWrapper

class Plugin:
    def __init__(self):
        self.meinFensterButton = None
        self.meinFenster = None

    def createMainWindowButtons(self):
        self.meinFensterButton = QtWidgets.QPushButton()
        self.meinFensterButton.setObjectName("buttonPlugin")
        self.meinFensterButton.setText("Mein Fenster")
        self.meinFensterButton.clicked.connect(self.createMeinFenster)
        return [self.meinFensterButton]
        
    def createMeinFenster(self):
        self.meinFenster = MeinFensterWrapper.MeinFensterWrapper()
        self.meinFenster.form.show()

#Datei MeinFensterWrapper.py im Plugin-Ordner
from PyQt5 import QtWidgets, QtCore, QtGui
from MeinPlugin import MeinFenster

class MeinFensterWrapper(QtCore.QObject):   
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = MeinFenster.Ui_Form()
        self.ui.setupUi(self.form)
```
## Existierende UI anpassen
Implementiere einen der "class_xx_wrapper" Filter, die UI-Wrapper-Klasse wird als Parameter gereicht. Du kannst diesen Parameter im Handler beerben und diese oder eine ganz neue Klasse returnen. Im folgenden Beispiel wird bei den freien Fertigkeiten die dritte Stufe entfernt.

```python
from PyQt5 import QtWidgets, QtCore, QtGui
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