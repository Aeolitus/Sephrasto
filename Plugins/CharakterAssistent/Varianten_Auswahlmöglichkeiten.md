
# Varianten und Auswahlmöglichkeiten

Es ist möglich, dem Nutzer Auswahlmöglichkeiten via Popup anzubieten. Dies ist eine zweite XML-Datei, die gleich benannt ist, wie die jeweilige S/K/P, enthält aber zusätzlich "_var" am Ende, z.B. "Halbelf_var.xml". Diese Datei muss leider von Hand geschrieben werden. Es folgen einige Beispiele, weitere können im Ilaris Advanced Baukasten gefunden werden.

**Beispiel 1:**

```
<Charakter>
  <Auswahl>
    <Attribut name="KK" wert="3"/>
    <Fertigkeit name="Schusswaffen" wert="2"/>
    <Übernatürliche-Fertigkeit name="Einfluss" wert="2"/>
    <Freie-Fertigkeit name="Sprache: Garethi" wert="2"/>
    <Talent name="Armbrüste"/>
    <Talent name="Adlerschwinge Wolfsgestalt" wert="40" kommentar="Wolf"/>
    <Vorteil name="Schildkampf I"/>
    <Vorteil name="Tierempathie" wert="20" kommentar="Pferde"/>
    <Eigenheit name="Streiter der Göttin"/> 
  </Auswahl>
  <Auswahl>
    <Fertigkeit name="Schusswaffen" wert="1"/>
    <Fertigkeit name="Athletik" wert="2"/>
  </Auswahl>
</Charakter>
```

Es erscheint ein Popup, bei dem der Nutzer sich zwischen KK +3, Schusswaffen +2, etc. entscheiden muss. Die Attribute "wert" und "kommentar" werden nur bei Talenten und Vorteilen mit variablen Kosten benötigt.
Danach erscheint ein weiteres Popup, bei dem er sich zwischen Schusswaffen +1 und Athletik +2 entscheiden muss. Hat er bei der ersten Auswahl bereits Schusswaffen gewählt, so wird diese Fertigkeit aus Folge-Auswahlen entfernt. Da in diesem Fall die zweite Auswhal nur noch Athletik +2 enthält, wird dies automatisch appliziert und es erscheint kein zweites Popup.

**Beispiel 2, Spezies Halbelf:**

```
<Charakter>
  <Varianten>
    <Variante name="Firnelfische Abstammung">
      <Vorteil name="Resistenz gegen Kälte"/>
      <Fertigkeit name="Überleben" wert="1"/>
    </Variante>
    <Variante name="Nivesische Abstammung">
      <Attribut name="IN" wert="1"/>
    </Variante>
    <Variante name="Thorwalsche Abstammung">
      <Attribut name="GE" wert="-1"/>
      <Attribut name="KK" wert="1"/>
    </Variante>
  </Varianten>

  <Auswahl keine-varianten="0,1">
    <Vorteil name="Gut Aussehend"/>
  </Auswahl>
   
  <Auswahl varianten="2">
    <Vorteil name="Selbstbeherrschung" wert="1"/>
    <Vorteil name="Athletik" wert="1"/>
  </Auswahl>
</Charakter>
```
Eine Variante kann nur in einem Varianten-Element existieren. Sie verhält sich gleich wie eine Auswahl, nur werden alle Child-Elemente appliziert. Es erscheint ein Popup, bei dem der Nutzer die drei Varianten Firnelfische, Nivesische und Thorwalsche Abstammung zur Auswahl erhält, hierbei kann er auch keine oder mehrere auswählen.
Die erste Auswahl hat nur ein Element, zeigt also niemals ein Popup. Durch das Attribut "keine-varianten" wird Gut Aussehend allerdings nur appliziert, wenn nicht die Variante an Index 0 (Firnelfische Abstammung) oder 1 (Nivesische Abstammung) ausgewählt wurde. Es wird auch dann appliziert, wenn garkeine Variante ausgewählt wurde.
Die zweite Auswahl ist nur aktiv, wenn die Variante an Index 2 (Thorwalsche Abstammung) gewählt wurde - nur dann erscheint ein Popup, bei dem der Nutzer sich zwischen Selbstbeherrschung und Athletik entscheiden muss. Innerhalb von "Variante" ist keine Auswahl möglich (Variante appliziert immer alle Elemente) - mit dieser Methode können auch Varianten Auswahlmöglichkeiten bieten.

**Beispiel 3, Spezies Orks:**
```
<Charakter>
  <Varianten pflichtwahl="1">
    <Variante name="Mann" beschreibung="" geschlecht="männlich">
      <Eigenheit name="Jähzorn"/>
    </Variante>
    <Variante name="Frau" beschreibung="" geschlecht="weiblich">
      <Attribut name="MU" wert="-2"/>
      <Attribut name="KO" wert="-1"/>
      <Attribut name="KK" wert="-1"/>
    </Variante>
  </Varianten>
</Charakter>
```
Durch das Attribut "pflichtwahl" muss eine der Varianten ausgewählt werden, eine Mehrfachauswahl ist nicht möglich.
Das Attribut "geschlecht" kann mit den "männlich" oder "weiblich" bei Variante und Auswahl genutzt werden, um diese zu entfernen, wenn im Hauptfenster das entsprechende Geschlecht nicht ausgewählt wurde.
Das Attribut "beschreibung" kann genutzt werden um im Spezies-/Kurzbeschreibungsfeld neben dem Namen eine zusätzliche Beschreibung einzufügen, die nicht um Popup angezeigt wird. Falls das Attribut wie hier mit einem leeren Inhalt eingefügt wird, dann wird die Variante überhaupt nicht in das entsprechende Feld eingetragen.
Da es sich in diesem Beispiel um eine Pflichtwahl handelt, bei der immer nur eine Variante - Mann oder Frau - bestehen bleiben kann, wird die entsprechende Variante automatisch appliziert und kein Popup angezeigt.
