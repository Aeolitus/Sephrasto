from EventBus import EventBus
from RestrictedPython import compile_restricted
import uuid

class Waffeneigenschaft():
    displayName = "Waffeneigenschaft"
    serializationName = "Waffeneigenschaft"

    def __init__(self):
        # Serialized properties
        self.id = str(uuid.uuid4())  # Eindeutige ID für jedes neue Element
        self.name = ''
        self.text = ''
        self.script = ''
        self.scriptPrio = 0

        # Derived properties after deserialization
        self.scriptCompiled = ''

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.id == other.id and \
            self.name == other.name and \
            self.text == other.text and \
            self.script == other.script and \
            self.scriptPrio == other.scriptPrio

    def finalize(self, db):
        self.scriptCompiled = compile_restricted(self.script or "", self.name + " Script", "exec")

    def executeScript(self, api):
        try:
            exec(self.scriptCompiled, api)
        except Exception as e:
            raise type(e)(f"\nScriptfehler in Waffeneigenschaft \"{self.name}\". Vermutlich hast du hier Änderungen in den Hausregeln vorgenommen, die das Problem verursachen.\n\nFehler: {str(e)}")

    def details(self, db):
        if self.script:
            return f"{self.text}\nScript: {self.script}"
        return self.text

    def serialize(self, ser):
        ser.set('id', self.id)  # ID als erstes serialisieren
        ser.set('name', self.name)
        ser.set('text', self.text)
        if self.script:
            ser.set('script', self.script)
        if self.scriptPrio != 0:
            ser.set('scriptPrio', self.scriptPrio)
        EventBus.doAction("waffeneigenschaft_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, referenceDB = None):
        # ID laden oder neue generieren falls nicht vorhanden (für Rückwärtskompatibilität)
        self.id = ser.get('id', str(uuid.uuid4()))
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.script = ser.get('script', self.script)
        self.scriptPrio = ser.getInt('scriptPrio', self.scriptPrio)
        EventBus.doAction("waffeneigenschaft_deserialisiert", { "object" : self, "deserializer" : ser})