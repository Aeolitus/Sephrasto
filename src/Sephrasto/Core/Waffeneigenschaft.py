from EventBus import EventBus

class Waffeneigenschaft():
    displayName = "Waffeneigenschaft"
    serializationName = "Waffeneigenschaft"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.script = ''
        self.scriptPrio = 0

        # Derived properties after deserialization
        self.scriptCompiled = ''

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        self.scriptCompiled = compile(self.script or "", self.name + " Script", "exec")

    def executeScript(self, api):
        exec(self.scriptCompiled, api)

    def details(self, db):
        if self.script:
            return f"{self.text}\nScript: {self.script}"
        return self.text

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        if self.script:
            ser.set('script', self.script)
        if self.scriptPrio != 0:
            ser.set('scriptPrio', self.scriptPrio)
        EventBus.doAction("waffeneigenschaft_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.script = ser.get('script', self.script)
        self.scriptPrio = ser.getInt('scriptPrio', self.scriptPrio)
        EventBus.doAction("waffeneigenschaft_deserialisiert", { "object" : self, "deserializer" : ser})