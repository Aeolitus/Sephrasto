from VoraussetzungenListe import VoraussetzungenListe
from EventBus import EventBus

class Regel():
    displayName = "Regel"
    serializationName = "Regel"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.typ = 0
        self.voraussetzungen = VoraussetzungenListe()
        self.probe = ''
        
        # Derived properties after deserialization
        self.anzeigename = ""

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def finalize(self, db):
        self.anzeigename = self.name
        for trim in [" (M)", " (L)", " (D)", " (FK)"]:
            if self.anzeigename.endswith(trim):
                self.anzeigename = self.anzeigename[:-len(trim)]

    def typname(self, db):
        typ = min(self.typ, len(db.einstellungen['Regeln: Typen'].wert) - 1)
        return db.einstellungen['Regeln: Typen'].wert[typ]

    def details(self, db):
        if self.probe:
            return f"Probe: {self.probe}. {self.text}"
        return self.text

    def serialize(self, ser):
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('voraussetzungen', self.voraussetzungen.text)
        ser.set('typ', self.typ)
        ser.set('probe', self.probe)
        EventBus.doAction("regel_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser):
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.voraussetzungen.compile(ser.get('voraussetzungen', ''))      
        self.typ = ser.getInt('typ')
        self.probe = ser.get('probe')
        EventBus.doAction("regel_deserialisiert", { "object" : self, "deserializer" : ser})