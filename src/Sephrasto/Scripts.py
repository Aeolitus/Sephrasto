from Hilfsmethoden import Hilfsmethoden, SortedCategoryToListDict
from EventBus import EventBus

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

    def __str__(self):
        return self.name

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

class Scripts:
    def __init__(self, setters, stringGetter, numberGetter, boolGetter):
        self.setters = setters
        self.stringGetter = stringGetter
        self.numberGetter = numberGetter
        self.boolGetter = boolGetter

    def finalize(self):
        kategorien = set()
        for script in self.numberGetter.values():
            kategorien.add(script.kategorie)
        for script in self.stringGetter.values():
            kategorien.add(script.kategorie)
        for script in self.setters.values():
            kategorien.add(script.kategorie)
        self.kategorien = {}
        i = 0
        for kategorie in sorted(list(kategorien), key=Hilfsmethoden.unicodeCaseInsensitive):
            self.kategorien[kategorie] = i
            i +=1

        self.numberGetterByKategorie = SortedCategoryToListDict(self.kategorien)
        for script in self.numberGetter.values():
            self.numberGetterByKategorie.appendByName(script.kategorie, script)
        self.numberGetterByKategorie.sortValues(lambda s: Hilfsmethoden.unicodeCaseInsensitive(s.name))

        self.stringGetterByKategorie = SortedCategoryToListDict(self.kategorien)
        for script in self.stringGetter.values():
            self.stringGetterByKategorie.appendByName(script.kategorie, script)
        self.stringGetterByKategorie.sortValues(lambda s: Hilfsmethoden.unicodeCaseInsensitive(s.name))

        self.boolGetterByKategorie = SortedCategoryToListDict(self.kategorien)
        for script in self.boolGetter.values():
            self.boolGetterByKategorie.appendByName(script.kategorie, script)
        self.boolGetterByKategorie.sortValues(lambda s: Hilfsmethoden.unicodeCaseInsensitive(s.name))

        self.categorizeSetters(None)

    def setSetterFilter(self, filter):
        if filter == self.settersByKategorie.nameFilter:
            return
        self.categorizeSetters(filter)

    def categorizeSetters(self, filter):
        self.settersByKategorie = SortedCategoryToListDict(self.kategorien)
        self.settersByKategorie.setNameFilter(filter)
        for script in self.setters.values():
            self.settersByKategorie.appendByName(script.kategorie, script)
        self.settersByKategorie.sortValues(lambda s: Hilfsmethoden.unicodeCaseInsensitive(s.name))

    @staticmethod
    def create(datenbank, context):
        scripts = {}
        def addScript(script):
            scripts[script.name] = script

        # ======================
        # Number getters (parameters afters the first only support default values)
        # ======================
        for attribut in datenbank.attribute:
            addScript(Script(f"{attribut} Wert", f"get{attribut}", "Attribute"))
            addScript(Script(f"{attribut} Probenwert", f"get{attribut}Probenwert", "Attribute"))
        for ab in datenbank.abgeleiteteWerte:
            addScript(Script(f"{ab} Basiswert", f"get{ab}Basis", "Abgeleitete Werte"))
            addScript(Script(f"{ab} Modifikator", f"get{ab}Mod", "Abgeleitete Werte"))
            addScript(Script(f"{ab} (Basis + Mod.)", f"get{ab}", "Abgeleitete Werte"))
        for en in datenbank.energien:
            addScript(Script(f"{en} Basiswert", f"get{en}Basis", "Energien"))
            addScript(Script(f"{en} Modifikator", f"get{en}Mod", "Energien"))
            addScript(Script(f"{en} Steigerungswert", f"get{en}", "Energien"))
            addScript(Script(f"{en} Gebunden", f"get{en}Gebunden", "Energien"))
            addScript(Script(f"{en} (Basis + Mod. + Steigerung)", f"get{en}Final", "Energien"))

        addScript(Script("Status (Index)", "getStatusIndex", "Hintergrund"))
        addScript(Script("Finanzen (Index)", "getFinanzenIndex", "Hintergrund"))
        addScript(Script("EP gesamt", "getEPGesamt", "Hintergrund"))
        addScript(Script("EP ausgegeben", "getEPAusgegeben", "Hintergrund"))

        script = Script(f"Fertigkeit Basiswert", f"getFertigkeitBasiswert", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.fertigkeiten))
        addScript(script)

        script = Script(f"Fertigkeit Probenwert ohne Talent", f"getFertigkeitProbenwert", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.fertigkeiten))
        addScript(script)

        script = Script(f"Fertigkeit Probenwert mit Talent", f"getFertigkeitProbenwertTalent", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.fertigkeiten))
        addScript(script)
            
        script = Script(f"Übernatürliche Fertigkeit Basiswert", f"getÜbernatürlicheFertigkeitBasiswert", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.übernatürlicheFertigkeiten))
        addScript(script)

        script = Script(f"Übernatürliche Fertigkeit Probenwert ohne Talent", f"getÜbernatürlicheFertigkeitProbenwert", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.übernatürlicheFertigkeiten))
        addScript(script)

        script = Script(f"Übernatürliche Fertigkeit Probenwert mit Talent", f"getÜbernatürlicheFertigkeitProbenwertTalent", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.übernatürlicheFertigkeiten))
        addScript(script)

        kampfstile = datenbank.einstellungen["Kampfstile"].wert.keys()
        script = Script(f"Kampfstil AT Modifikator", f"getKampfstilAT", "Kampfstile")
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        addScript(script)
        script = Script(f"Kampfstil VT Modifikator", f"getKampfstilVT", "Kampfstile")
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        addScript(script)
        script = Script(f"Kampfstil Bonusschaden Modifikator", f"getKampfstilTPPlus", "Kampfstile")
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        addScript(script)
        script = Script(f"Kampfstil Reichweite Modifikator", f"getKampfstilRW", "Kampfstile")
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        addScript(script)
        script = Script(f"Kampfstil BE Modifikator", f"getKampfstilBE", "Kampfstile")
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        addScript(script)

        zonen = ["Beine", "Arm links", "Arm rechts", "Bauch", "Brust", "Kopf"]

        script = Script(f"Rüstung RS", f"getRüstungRS", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)
        for i in range(len(zonen)):
            zone = zonen[i]
            script = Script(f"Rüstung RS {zone}", f"getRüstungRSZone", "Ausrüstung")
            script.parameter.append(ScriptParameter("Index", int))
            script.parameter.append(ScriptParameter("Zone", int, defaultValue=i))
            addScript(script)

        script = Script(f"Rüstung RS Final Gesamt (RS + Mod.)", f"getRüstungRSFinal", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)
        for i in range(len(zonen)):
            zone = zonen[i]
            script = Script(f"Rüstung RS Final {zone} (RS + Mod.)", f"getRüstungRSFinal", "Ausrüstung")
            script.parameter.append(ScriptParameter("Index", int))
            script.parameter.append(ScriptParameter("Zone", int, defaultValue=i))
            addScript(script)

        script = Script(f"Rüstung BE", f"getRüstungBE", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)
        script = Script(f"Rüstung BE Final (BE + Mod.)", f"getRüstungBEFinal", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)
        script = Script(f"Rüstung WS Final (WS + Gesamt-RS + Mod.)", f"getRüstungWSFinal", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe BE Slot", f"getWaffeBESlot", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)
        
        script = Script(f"Waffe WM", f"getWaffeWM", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Würfelseiten", f"getWaffeTPWürfelSeiten", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe AT Modifikator", f"getWaffeATMod", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe VT Modifikator", f"getWaffeVTMod", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe LZ", f"getWaffeLZ", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe LZ Modifikator", f"getWaffeLZMod", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Würfel", f"getWaffeTPWürfel", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Würfel Modifikator", f"getWaffeTPWürfelMod", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Bonusschaden", f"getWaffeTPPlus", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Bonusschaden Modifikator", f"getWaffeTPPlusMod", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Härte", f"getWaffeHärte", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Härte Modifikator", f"getWaffeHärteMod", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe RW", f"getWaffeRW", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe RW Modifikator", f"getWaffeRWMod", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        if context == ScriptContext.Waffeneigenschaften:
            script = Script(f"Waffeneigenschaft Parameter (Zahl)", f"getEigenschaftParam", "Waffeneigenschaften", castType = int)
            script.parameter.append(ScriptParameter("Index", int))
            addScript(script)

            addScript(Script("Index der Waffe mit der Eigenschaft", f"getWaffeIndex", "Waffeneigenschaften"))

        numberGetter = scripts

        # ======================
        # String getters (parameters afters the first only support default values)
        # ======================
        scripts = {}

        addScript(Script("Name", "getName", "Hintergrund"))
        addScript(Script("Spezies", "getSpezies", "Hintergrund"))
        addScript(Script("Kurzbeschreibung", "getKurzbeschreibung", "Hintergrund"))
        addScript(Script("Heimat", "getHeimat", "Hintergrund"))
        addScript(Script("Status", "getStatus", "Hintergrund"))
        addScript(Script("Finanzen", "getFinanzen", "Hintergrund"))

        script = Script(f"Eigenheit", f"getEigenheit", "Hintergrund")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Inventar", f"getInventar", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Rüstung Name", f"getRüstung", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Basiswaffen-Name", f"getWaffe", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Kampfstil", f"getWaffeKampfstil", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Fertigkeit", f"getWaffeFertigkeit", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe Talent", f"getWaffeTalent", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        if context == ScriptContext.Waffeneigenschaften:
            script = Script(f"Waffeneigenschaft Parameter (Text)", f"getEigenschaftParam", "Waffeneigenschaften")
            script.parameter.append(ScriptParameter("Index", int))
            addScript(script)
        
        stringGetter = scripts

        # ======================
        # Bool getters (parameters afters the first only support default values)
        # ======================
        scripts = {}

        script = Script(f"Charakter hat Fertigkeit", f"hasFertigkeit", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.fertigkeiten))
        addScript(script)

        script = Script(f"Charakter hat übernatürliche Fertigkeit", f"hasÜbernatürlicheFertigkeit", "Fertigkeiten")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.übernatürlicheFertigkeiten))
        addScript(script)

        script = Script(f"Charakter hat Talent", f"hasTalent", "Talente")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.talente))
        addScript(script)

        script = Script(f"Charakter hat Vorteil", f"hasVorteil", "Vorteile")
        script.parameter.append(ScriptParameter("Name", str, completionTable = datenbank.vorteile))
        addScript(script)

        script = Script(f"Waffe ist Nahkampfwaffe", f"isWaffeNahkampf", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        script = Script(f"Waffe ist Fernkampfwaffe", f"isWaffeFernkampf", "Ausrüstung")
        script.parameter.append(ScriptParameter("Index", int))
        addScript(script)

        boolGetter = scripts

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
            "wenn er größer als das angebene Maximum ist, Maximum."
        script.parameter.append(ScriptParameter("Wert", float))
        script.parameter.append(ScriptParameter("Minimum", float))
        script.parameter.append(ScriptParameter("Maximum", float))
        addScript(script)

        # Abgeleitete Werte
        for ab in datenbank.abgeleiteteWerte:
            script = Script(f"{ab} Modifikator setzen", f"set{ab}Mod", "Abgeleitete Werte")
            script.beschreibung = "Der Modifikator des abgeleiteten Werts wird auf den neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
            script.parameter.append(ScriptParameter("Neuer Wert", int))
            addScript(script)

            script = Script(f"{ab} modifizieren", f"modify{ab}", "Abgeleitete Werte")
            script.beschreibung = "Der abgeleitete Wert wird um den angegebenen Wert modifiziert."
            script.parameter.append(ScriptParameter("Modifikator", int))
            addScript(script)

        # Energien
        for en in datenbank.energien:
            script = Script(f"{en} Basiswert setzen", f"set{en}Basis", "Energien")
            script.beschreibung = "Der Basiswert der Energie wird auf den neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
            script.parameter.append(ScriptParameter("Neuer Wert", int))
            addScript(script)

            script = Script(f"{en} Basiswert modifizieren", f"modify{en}Basis", "Energien")
            script.beschreibung = "Der Basiswert der Energie wird um den angebenen Wert modifiziert. Dies wird in der Regel von Vorteilen verwendet, welche den Grundvorrat der Energie bereitstellen."
            script.parameter.append(ScriptParameter("Modifikator", int))
            addScript(script)

            script = Script(f"{en} Modifikator setzen", f"set{en}Mod", "Energien")
            script.beschreibung = "Der Modifikator der Energie wird auf den neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
            script.parameter.append(ScriptParameter("Neuer Wert", int))
            addScript(script)

            script = Script(f"{en} Modifikator modifizieren", f"modify{en}", "Energien")
            script.beschreibung = "Der Modifikator der Energie wird um den angebenen Wert modifiziert. Dies wird in der Regel von Vorteilen verwendet, welche die Energie zusätzlich zum Grundvorrat erhöhen."
            script.parameter.append(ScriptParameter("Modifikator", int))
            addScript(script)

        # Talente
        script = Script("Talent PW modifizieren", "modifyTalentProbenwert", "Talente")
        script.beschreibung = "Dieses Script ist nützlich, um permanente Erleichterungen auf ein Talent direkt in der Talentliste aufzuführen. "\
            "Ist das Talent noch nicht erworben, wird das ganze Talent mit der Modifizierung in Klammern gesetzt. Die Modifizierung wird ausschließlich im Charakterbogen eingerechnet!"
        script.parameter.append(ScriptParameter("Talent", str, completionTable = datenbank.talente))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Talent Info hinzufügen", "addTalentInfo", "Talente")
        script.beschreibung = "Dieses Script ist nützlich, um besondere Effekte wie beispielsweise von manchen Vorteilen direkt bei den Talenten im Charakterbogen aufzuführen."
        script.parameter.append(ScriptParameter("Talent", str, completionTable = datenbank.talente))
        script.parameter.append(ScriptParameter("Info", str))
        addScript(script)

        script = Script("Talent kaufen", "addTalent", "Talente")
        script.beschreibung = "Fügt dem Charakter das angegebene Talent zu regulären Kosten hinzu. Wenn das Script in einem Vorteil verwendet wird, wird der Vorteil dem neuen Talent, als Voraussetzung hinzugefügt. "
        "Sobald der Vorteil also abgewählt wird, verliert der Charakter auch das neue Talent. Wenn der Charakter das Talent bereits besitzt, werden Kosten und Kommentar angepasst, falls gesetzt.\n"\
        "<ul><li>Mit dem EP Kosten-Parameter können die Standard-Talentkosten geändert werden. Bei -1 werden sie nicht verändert.</li>"\
        "<li>Mit dem Kommentar-Parameter kann ein Kommentar hinzugefügt werden, falls das Talent dies unterstützt (optional).</li></ul>"
        script.parameter.append(ScriptParameter("Talent", str, completionTable = datenbank.talente))
        script.parameter.append(ScriptParameter("EP Kosten anpassen (optional)", int, -1))
        script.parameter.append(ScriptParameter("Kommentar setzen (optional)", str, ""))
        addScript(script)

        script = Script("Talent entfernen", "removeTalent", "Talente")
        script.beschreibung = "Entfernt das angegebene Talent, falls der Charakter es besitzt."
        script.parameter.append(ScriptParameter("Talent", str, completionTable = datenbank.talente))
        addScript(script)

        script = Script("Talent Voraussetzung hinzufügen", "addTalentVoraussetzung", "Talente")
        script.beschreibung = "Fügt dem angegebenen Talent die angegebene Voraussetzung hinzu (siehe Datenbankeditor-Dokumentation)."
        script.parameter.append(ScriptParameter("Talent", str, completionTable = datenbank.talente))
        script.parameter.append(ScriptParameter("Voraussetzung", str))
        addScript(script)

        # Fertigkeiten
        script = Script("Fertigkeit Basiswert modifizieren", "modifyFertigkeitBasiswert", "Fertigkeiten")
        script.beschreibung = "Dieses Script ist nützlich, um sich permanente Erleichterungen auf eine Fertigkeit nicht merken zu müssen. "\
            "Diese Modifikation wird nur im Charakterbogen eingerechnet!"
        script.parameter.append(ScriptParameter("Fertigkeit", str, completionTable = datenbank.fertigkeiten))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Übernatürliche Fertigkeit Basiswert modifizieren", "modifyÜbernatürlicheFertigkeitBasiswert", "Fertigkeiten")
        script.beschreibung = "Dieses Script ist nützlich, um sich permanente Erleichterungen auf eine übernatürliche Fertigkeit nicht merken zu müssen. "\
            "Diese Modifikation wird nur im Charakterbogen eingerechnet!"
        script.parameter.append(ScriptParameter("Fertigkeit", str, completionTable = datenbank.übernatürlicheFertigkeiten))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        # Vorteile
        script = Script("Vorteil kaufen", "addVorteil", "Vorteile")
        script.beschreibung = "Fügt dem Charakter den angegebenen Vorteil zu regulären Kosten hinzu. Wenn das Script in einem Vorteil verwendet wird, wird der Vorteil dem neuen Vorteil als Voraussetzung hinzugefügt. "
        "Sobald der Vorteil (der den neuen Vorteil verleiht) also abgewählt wird, verliert der Charakter auch den neuen Vorteil. Wenn der Charakter den Vorteil bereits besitzt, werden Kosten und Kommentar angepasst, falls gesetzt.\n"\
        "<ul><li>Mit dem EP Kosten-Parameter können die Standard-Vorteilkosten geändert werden. Bei -1 werden sie nicht verändert.</li>"\
        "<li>Mit dem Kommentar-Parameter kann ein Kommentar hinzugefügt werden, falls der Vorteil dies unterstützt.</li></ul>"
        script.parameter.append(ScriptParameter("Vorteil", str, completionTable = datenbank.vorteile))
        script.parameter.append(ScriptParameter("EP-Kosten anpassen (optional)", int, -1))
        script.parameter.append(ScriptParameter("Kommentar setzen (optional)", str, ""))
        addScript(script)

        script = Script("Vorteil entfernen", "removeVorteil", "Vorteile")
        script.beschreibung = "Entfernt den angegebenen Vorteil, falls der Charakter ihn besitzt."
        script.parameter.append(ScriptParameter("Vorteil", str, completionTable = datenbank.vorteile))
        addScript(script)

        script = Script("Vorteil Voraussetzung hinzufügen", "addTalentVoraussetzung", "Vorteile")
        script.beschreibung = "Fügt dem angegebenen Vorteil die angegebene Voraussetzung hinzu (siehe Datenbankeditor-Dokumentation)."
        script.parameter.append(ScriptParameter("Vorteil", str, completionTable = datenbank.vorteile))
        script.parameter.append(ScriptParameter("Voraussetzung", str))
        addScript(script)

        # Kampfstile
        script = Script("Kampfstil Werte setzen", "setKampfstil", "Kampfstile")
        script.beschreibung = "Mit diesem Script kannst du Werteveränderungen durch einen bestimmten Kampfstil auf einen festen Wert setzen. "\
            "Diese wirken nur für Waffen, die diesen Kampfstil aktiv gesetzt haben. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        script.parameter.append(ScriptParameter("AT", int))
        script.parameter.append(ScriptParameter("VT", int))
        script.parameter.append(ScriptParameter("Bonusschaden", int))
        script.parameter.append(ScriptParameter("RW", int))
        script.parameter.append(ScriptParameter("BE", int))
        addScript(script)

        script = Script("Kampfstilwerte modifizieren", "modifyKampfstil", "Kampfstile")
        script.beschreibung = "Mit diesem Script kannst du Werteveränderungen durch einen bestimmten Kampfstil modifizieren. "\
            "Diese wirken nur für Waffen, die diesen Kampfstil aktiv gesetzt haben."
        script.parameter.append(ScriptParameter("Kampfstil", str, completionTable = kampfstile))
        script.parameter.append(ScriptParameter("AT", int))
        script.parameter.append(ScriptParameter("VT", int))
        script.parameter.append(ScriptParameter("Bonusschaden", int))
        script.parameter.append(ScriptParameter("RW", int))
        script.parameter.append(ScriptParameter("BE", int))
        addScript(script)

        # Waffen
        script = Script("Waffeneigenschaft hinzufügen", "addWaffeneigenschaft", "Ausrüstung")
        script.beschreibung = "Alle Waffen mit der angegebenen Basiswaffe erhalten die angegebene Waffeneigenschaft (wenn sie diese nicht bereits haben)."
        script.parameter.append(ScriptParameter("Waffe", str, completionTable = datenbank.waffen))
        script.parameter.append(ScriptParameter("Eigenschaft", str, completionTable = datenbank.waffeneigenschaften))
        addScript(script)

        script = Script("Waffeneigenschaft entfernen", "removeWaffeneigenschaft", "Ausrüstung")
        script.beschreibung = "Alle Waffen mit der angegebenen Basiswaffe verlieren die angegebene Waffeneigenschaft (wenn sie diese überhaupt haben)."
        script.parameter.append(ScriptParameter("Waffe", str, completionTable = datenbank.waffen))
        script.parameter.append(ScriptParameter("Eigenschaft", str, completionTable = datenbank.waffeneigenschaften))
        addScript(script)

        script = Script("Waffe AT Wert setzen", "setWaffeAT", "Ausrüstung")
        script.beschreibung = "Die AT der Waffe wird auf einen neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe AT modifizieren", "modifyWaffeAT", "Ausrüstung")
        script.beschreibung = "Die AT der Waffe wird um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe VT Wert setzen", "setWaffeVT", "Ausrüstung")
        script.beschreibung = "Die VT der Waffe wird auf einen neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe VT modifizieren", "modifyWaffeVT", "Ausrüstung")
        script.beschreibung = "Die VT der Waffe wird um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe LZ Wert setzen", "setWaffeLZ", "Ausrüstung")
        script.beschreibung = "Die LZ der Waffe wird auf einen neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe LZ modifizieren", "modifyWaffeLZ", "Ausrüstung")
        script.beschreibung = "Die LZ der Waffe wird um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Schadenswürfel Wert setzen", "setWaffeTPWürfel", "Ausrüstung")
        script.beschreibung = "Die Schadenswürfel der Waffe werden auf einen neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Schadenswürfel modifizieren", "modifyWaffeTPWürfel", "Ausrüstung")
        script.beschreibung = "Die Schadenswürfel der Waffe werden um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Bonusschaden Wert setzen", "setWaffeTPPlus", "Ausrüstung")
        script.beschreibung = "Der Bonusschaden der Waffe wird auf einen neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Bonusschaden modifizieren", "modifyWaffeTPPlus", "Ausrüstung")
        script.beschreibung = "Der Bonusschaden der Waffe wird um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Härte Wert setzen", "setWaffeHärte", "Ausrüstung")
        script.beschreibung = "Die Härte der Waffe wird auf einen neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Härte modifizieren", "modifyWaffeHärte", "Ausrüstung")
        script.beschreibung = "Die Härte der Waffe wird um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        script = Script("Waffe Reichweite Wert setzen", "setWaffeRW", "Ausrüstung")
        script.beschreibung = "Die Reichweite der Waffe wird auf einen neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Neuer Wert", int))
        addScript(script)

        script = Script("Waffe Reichweite modifizieren", "modifyWaffeRW", "Ausrüstung")
        script.beschreibung = "Die Reichweite der Waffe wird um den angebenenen Wert modifiziert."
        script.parameter.append(ScriptParameter("Index", int))
        script.parameter.append(ScriptParameter("Modifikator", int))
        addScript(script)

        #Regeln
        script = Script("Regel Info hinzufügen", "addRegelInfo", "Regeln")
        script.beschreibung = "Dieses Script ist nützlich, um besondere Effekte wie beispielsweise von manchen Vorteilen direkt bei den Regeln im Regelanhang des Charakterbogens aufzuführen."
        script.parameter.append(ScriptParameter("Regel", str, completionTable = datenbank.regeln))
        script.parameter.append(ScriptParameter("Info", str))
        addScript(script)

        setters = scripts
        
        scripts = EventBus.applyFilter("scripts_available", Scripts(setters, stringGetter, numberGetter, boolGetter), { "context" : context }) 
        scripts.finalize()
        return scripts