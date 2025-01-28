from EventBus import EventBus
from RestrictedPython import compile_restricted
import json

class IndexableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def updateIndex(self):
        self.keyList = list(self.keys())
        self.valueList = list(self.values())
    def keyAtIndex(self, idx):
        return self.keyList[idx]
    def valueAtIndex(self, idx):
        return self.valueList[idx]

class DatenbankEinstellung:
    displayName = "Einstellung"
    serializationName = "Einstellung"


    def __init__(self):
        # Serialized properties
        self.name = ''
        self.beschreibung = ''     
        self.text = ''
        self.typ = 'Text' #Text, Float, Int, Bool, TextList, IntList, TextDict
        self.separator = "\n"
        self.strip = True

        # Derived properties after deserialization
        self.wert = None

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.name == other.name and \
            self.beschreibung == other.beschreibung and \
            self.text == other.text and \
            self.typ == other.typ and \
            self.separator == other.separator and \
            self.strip == other.strip

    def __toList(self):
        val = []
        if self.text:
            if self.strip:
                val = [t.strip() for t in self.text.split(self.separator)]
            else:
                val = self.text.split(self.separator)
        return val

    def finalize(self, db):
        self.__initWert()
        
    def __initWert(self):
        if self.wert is not None:
            return
        if self.typ == 'Float':
            self.wert = float(self.text or "0.0")
        elif self.typ == 'Int':
            self.wert = int(self.text or "0")
        elif self.typ == 'Bool':
            self.wert = self.text.lower() == "true" or self.text == '1'
        elif self.typ == 'Text':
            self.wert = self.text or ""
        elif self.typ == 'TextList':
            self.wert = self.__toList()
        elif self.typ == 'TextDict':
            textList = self.__toList()
            self.wert = IndexableDict()
            for el in textList:
                if not el:
                    continue
                tmp = el.split("=", 1)
                if self.strip:
                    self.wert[tmp[0].strip()] = tmp[1].strip()
                else:
                    self.wert[tmp[0]] = tmp[1]
            self.wert.updateIndex()
        elif self.typ == 'JsonDict':
            self.wert = IndexableDict(json.loads(self.text))
            self.wert.updateIndex()
        elif self.typ == 'IntList':
            textList = self.__toList()
            self.wert = [int(el) for el in textList]
        elif self.typ == 'Eval':
            self.wert = compile_restricted(self.text or "0", self.name, "eval")
        elif self.typ == 'Exec':
            self.wert = compile_restricted(self.text or "", self.name, "exec")

    def details(self, db):
        return f"{self.text}\n{self.beschreibung}"

    def executeScript(self, api):
        try:
            exec(self.wert, api)
        except Exception as e:
            raise type(e)(f"\nScriptfehler in Einstellung \"{self.name}\". Vermutlich hast du hier Änderungen in den Hausregeln vorgenommen, die das Problem verursachen.\n\nFehler: {str(e)}")

    def evaluateScript(self, api):
        try:
            return eval(self.wert, api)
        except Exception as e:
            raise type(e)(f"\nScriptfehler in Einstellung \"{self.name}\". Vermutlich hast du hier Änderungen in den Hausregeln vorgenommen, die das Problem verursachen.\n\nFehler: {str(e)}")

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        if ser.options["isMerge"]:
            ser.set('typ', self.typ)
            ser.set('beschreibung', self.beschreibung)
            ser.set('separator', self.separator)
            ser.set('strip', self.strip)
        EventBus.doAction("datenbankeinstellung_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, referenceDB = None):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.typ = ser.get('typ', self.typ)
        self.beschreibung = ser.get('beschreibung', self.beschreibung)
        self.separator = ser.get('separator', self.separator)
        self.strip = ser.getBool('strip', self.strip)
        
        if referenceDB is not None and self.name in referenceDB[DatenbankEinstellung]:
            reference = referenceDB[DatenbankEinstellung][self.name]
            self.typ = reference.typ
            self.beschreibung = reference.beschreibung
            self.strip = reference.strip
            self.separator = reference.separator
            
        self.__initWert() # its crucial to have access to .wert early on, finalize is too late

        EventBus.doAction("datenbankeinstellung_deserialisiert", { "object" : self, "deserializer" : ser})