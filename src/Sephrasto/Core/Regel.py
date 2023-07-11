class Regel():
    displayName = "Regel"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.text = ''
        self.typ = 0
        self.voraussetzungen = []
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