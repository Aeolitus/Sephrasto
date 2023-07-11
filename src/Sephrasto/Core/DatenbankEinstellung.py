class DatenbankEinstellung(object):
    displayName = "Einstellung"

    def __init__(self):
        # Serialized properties
        self.name = ''
        self.beschreibung = ''     
        self.text = ''
        self.typ = 'Text' #Text, Float, Int, Bool, TextList, IntList, TextDict
        self.separator = ","
        self.strip = True

        # Derived properties after deserialization
        self.wert = ''

    def deepequals(self, other): 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def __toList(self):
        val = []
        if self.text:
            if self.strip:
                val = [t.strip() for t in self.text.split(self.separator)]
            else:
                val = self.text.split(self.separator)
        return val

    def finalize(self, db):
        if self.typ == 'Float':
            self.wert = float(self.text or "0")
        elif self.typ == 'Int':
            self.wert = int(self.text or "0.0")
        elif self.typ == 'Bool':
            self.wert = self.text.lower() == "true" or self.text == '1'
        elif self.typ == 'Text':
            self.wert = self.text or ""
        elif self.typ == 'TextList':
            self.wert = self.__toList()
        elif self.typ == 'TextDict':
            textList = self.__toList()
            self.wert = {}
            for el in textList:
                if not el:
                    continue
                tmp = el.split("=")
                if self.strip:
                    self.wert[tmp[0].strip()] = tmp[1].strip()
                else:
                    self.wert[tmp[0]] = tmp[1]
        elif self.typ == 'IntList':
            textList = self.__toList()
            self.wert = [int(el) for el in textList]
        elif self.typ == 'Eval':
            self.wert = compile(self.text or "0", self.name, "eval")
        elif self.typ == 'Exec':
            self.wert = compile(self.text or "", self.name, "exec")

    def details(self, db):
        return f"{self.text}\n{self.beschreibung}"