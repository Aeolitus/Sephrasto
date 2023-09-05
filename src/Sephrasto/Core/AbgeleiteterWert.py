from Wolke import Wolke
import copy

# Implementation for abgeleitete Werte (WS, INI etc.). Using the type object pattern.
# AbgeleiteterWertDefinition: type object, initialized with database values
# AbgeleiteterWert: character editor values, initialised with definition but supports overrides
class AbgeleiteterWertDefinition:
    displayName = "Abgeleiteter Wert"

    def __init__(self):
        # Serialized properties
        self.name = ""
        self.anzeigename = ""
        self.anzeigen = True
        self.text = ""
        self.formel = ""
        self.script = ""
        self.finalscript = ""
        self.sortorder = 0

        # Derived properties after deserialization
        self.scriptCompiled = ""
        self.finalscriptCompiled = ""

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        self.scriptCompiled = compile(self.script or "0", self.name + " Script", "eval")
        self.finalscriptCompiled = compile(self.finalscript or "0", self.name + " Finalscript", "eval")

    def details(self, db):
        details = []
        if self.script and self.finalscript:
            return f"{self.text}\nScript: {self.script}\nFinalscript: {self.finalscript}"
        elif self.script:
            return f"{self.text}\nScript: {self.script}"
        return self.text

class AbgeleiteterWert:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter
        self.basiswert = 0
        self.mod = 0
        self.finalwert = 0

    def __deepcopy__(self, memo=""):
        A = AbgeleiteterWert(self.definition, self.charakter)
        A.basiswert = self.basiswert
        A.mod = self.mod
        A.finalwert = self.finalwert
        return A

    @property
    def name(self):
        return self.definition.name

    @property
    def anzeigename(self):
        return self.definition.anzeigename

    @property
    def anzeigen(self):
        return self.definition.anzeigen

    @property
    def text(self):
        return self.definition.text

    @property
    def formel(self):
        return self.definition.formel

    @property
    def script(self):
        return self.definition.script

    @property
    def finalscript(self):
        return self.definition.finalscript

    @property
    def wert(self):
        return max(self.basiswert + self.mod, 0)

    @property
    def sortorder(self):
        return self.definition.sortorder

    def aktualisieren(self):
        self.mod = 0
        self.finalwert = 0
        scriptAPI = {
            'getAttribut' : lambda attribut: self.charakter.attribute[attribut].wert,
            'getRüstung' : lambda: copy.deepcopy(self.charakter.rüstung)
        }
        self.basiswert = eval(self.definition.scriptCompiled, scriptAPI)

    def diffBasiswert(self, attribute):
        scriptAPI = {
            'getAttribut' : lambda attribut: attribute[attribut].wert,
            'getRüstung' : lambda: copy.deepcopy(self.charakter.rüstung)
        }
        return eval(self.definition.scriptCompiled, scriptAPI) - self.basiswert

    def aktualisierenFinal(self):
        if not self.finalscript:
            self.finalwert = self.wert
            return
        self.finalwert = eval(self.definition.finalscriptCompiled, self.charakter.charakterScriptAPI)