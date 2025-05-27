from VoraussetzungenListe import VoraussetzungenListe
from EventBus import EventBus
import uuid

class Regel():
    displayName = "Regel"
    serializationName = "Regel"

    def __init__(self):
        # Serialized properties
        self.id = str(uuid.uuid4())  # Eindeutige ID für jedes neue Element
        self.name = ''
        self.text = ''
        self.kategorie = 0
        self.voraussetzungen = VoraussetzungenListe()
        self.probe = ''
        
        # Derived properties after deserialization
        self.anzeigename = ""

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.id == other.id and \
            self.name == other.name and \
            self.text == other.text and \
            self.kategorie == other.kategorie and \
            self.voraussetzungen == other.voraussetzungen and \
            self.probe == other.probe

    def finalize(self, db):
        self.anzeigename = self.name
        for trim in [" (M)", " (L)", " (D)", " (FK)"]:
            if self.anzeigename.endswith(trim):
                self.anzeigename = self.anzeigename[:-len(trim)]

    def kategorieName(self, db):
        kategorie = min(self.kategorie, len(db.einstellungen['Regeln: Kategorien'].wert) - 1)
        return db.einstellungen['Regeln: Kategorien'].wert.keyAtIndex(kategorie)

    def details(self, db):
        if self.probe:
            return f"Probe: {self.probe}. {self.text}"
        return self.text

    def serialize(self, ser):
        ser.set('id', self.id)  # ID als erstes serialisieren
        ser.set('name', self.name)
        ser.set('text', self.text)
        ser.set('voraussetzungen', self.voraussetzungen.text)
        ser.set('kategorie', self.kategorie)
        ser.set('probe', self.probe)
        EventBus.doAction("regel_serialisiert", { "object" : self, "serializer" : ser})

    def deserialize(self, ser, referenceDB = None):
        # ID laden oder neue generieren falls nicht vorhanden (für Rückwärtskompatibilität)
        self.id = ser.get('id', str(uuid.uuid4()))
        self.name = ser.get('name')
        self.text = ser.get('text')
        self.voraussetzungen.compile(ser.get('voraussetzungen', ''))      
        self.kategorie = ser.getInt('kategorie')
        self.probe = ser.get('probe')
        EventBus.doAction("regel_deserialisiert", { "object" : self, "deserializer" : ser})