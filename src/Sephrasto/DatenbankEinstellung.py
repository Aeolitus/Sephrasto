class DatenbankEinstellung(object):
    def __init__(self):
        self.name = ''
        self.beschreibung = ''
        self.wert = ''
        self.typ = 'Text' #Text, Float, Int oder Bool
        self.isUserAdded = True

    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

    def toFloat(self):
        assert self.typ == 'Float'
        return float(self.wert)

    def toInt(self):
        assert self.typ == 'Int'
        return int(self.wert)

    def toBool(self):
        assert self.typ == 'Bool'
        return self.wert.lower() == 'true' or self.wert == '1'

    def toText(self):
        assert self.typ == 'Text'
        return self.wert

    def toTextList(self, seperator=',', strip=True):
        if not self.toText():
            return []
        if strip:
            return [t.strip() for t in self.toText().split(seperator)]
        else:
            return self.toText().split(seperator)

    def toTextDict(self, seperator=',', strip=True):
        list = self.toTextList(seperator, strip)
        dict = {}
        for el in list:
            tmp = el.split("=")
            if strip:
                dict[tmp[0].strip()] = tmp[1].strip()
            else:
                dict[tmp[0]] = tmp[1]
        return dict