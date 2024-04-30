from Wolke import Wolke
import copy
from EventBus import EventBus
from RestrictedPython import compile_restricted
from Hilfsmethoden import Hilfsmethoden

# Implementation for abgeleitete Werte (WS, INI etc.). Using the type object pattern.
# AbgeleiteterWertDefinition: type object, initialized with database values
# AbgeleiteterWert: character editor values, initialised with definition but supports overrides
class AbgeleiteterWertDefinition:
    displayName = "Abgeleiteter Wert"
    serializationName = "AbgeleiteterWert"

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
        self.scriptCompiled = compile_restricted(self.script or "0", self.name + " Script", "eval")
        self.finalscriptCompiled = compile_restricted(self.finalscript or "0", self.name + " Finalscript", "eval")

    def details(self, db):
        details = []
        if self.script and self.finalscript:
            return f"{self.text}\nScript: {self.script}\nFinalscript: {self.finalscript}"
        elif self.script:
            return f"{self.text}\nScript: {self.script}"
        return self.text

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('anzeigename', self.anzeigename)
        ser.set('anzeigen', self.anzeigen)
        ser.set('formel', self.formel)
        if self.script:
            ser.set('script', self.script)
        if self.finalscript:
            ser.set('finalscript', self.finalscript)
        ser.set('sortorder', self.sortorder)
        EventBus.doAction("abgeleiteterwertdefinition_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.anzeigename = ser.get('anzeigename')
        self.anzeigen = ser.getBool('anzeigen')
        self.formel = ser.get('formel')
        self.script = ser.get('script', '')
        self.finalscript = ser.get('finalscript', '')
        self.sortorder = ser.getInt('sortorder')
        EventBus.doAction("abgeleiteterwertdefinition_deserialisiert", { "object" : self, "deserializer" : ser})

class AbgeleiteterWert:
    def __init__(self, definition, charakter):
        self.definition = definition
        self.charakter = charakter
        self.basiswert = 0
        self.mod = 0
        self.finalwert = 0

    def __deepcopy__(self, memo=""):
        # create new object
        cls = self.__class__
        result = cls.__new__(cls)
        # deepcopy everything except for self, charakter and definition
        memo[id(self)] = result
        memo[id(self.charakter)] = self.charakter
        memo[id(self.definition)] = self.definition
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

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
        return self.basiswert + self.mod

    @property
    def sortorder(self):
        return self.definition.sortorder

    def aktualisieren(self):
        self.mod = 0
        self.finalwert = 0
        try:
            self.basiswert = eval(self.definition.scriptCompiled, self.charakter.charakterScriptAPI)
        except Exception as e:
            raise type(e)(f"\nScriptfehler in Abgeleiteter Wert \"{self.name}\". Vermutlich hast du hier Änderungen in den Hausregeln vorgenommen, die das Problem verursachen.\n\nFehler: {str(e)}")

    def diffBasiswert(self, attribute):      
        try:
            return eval(self.definition.scriptCompiled, self.charakter.charakterScriptAPI) - self.basiswert
        except Exception as e:
            raise type(e)(f"\nScriptfehler in Abgeleiteter Wert \"{self.name}\". Vermutlich hast du hier Änderungen in den Hausregeln vorgenommen, die das Problem verursachen.\n\nFehler: {str(e)}")

    def aktualisierenFinal(self):
        if not self.finalscript:
            self.finalwert = self.wert
            return       
        try:
            self.finalwert = eval(self.definition.finalscriptCompiled, self.charakter.charakterScriptAPI)
        except Exception as e:
            raise type(e)(f"\nScriptfehler in Abgeleiteter Wert \"{self.name}\". Vermutlich hast du hier Änderungen in den Hausregeln vorgenommen, die das Problem verursachen.\n\nFehler: {str(e)}")