'''
In dieser Datei werden Waffen und Rüstungen definiert.
'''

class Objekt():
    def __init__(self):
        self.name = ''
        self.text = ''
        self.isUserAdded = True

    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__

class Waffeneigenschaft():
    def __init__(self):
        self.name = ''
        self.text = ''
        self.script = None
        self.scriptPrio = 0
        self.isUserAdded = True

    def __eq__(self, other) : 
        if self.__class__ != other.__class__: return False
        return self.__dict__ == other.__dict__
     
class Waffe(Objekt):
    def __init__(self):
        super().__init__()
        self.würfel = 0
        self.würfelSeiten = 6
        self.plus = 0
        self.eigenschaften = []
        self.härte = 6
        self.rw = 0
        self.wm = 0
        self.fertigkeit = ''
        self.talent = ''
        self.kampfstile = []
        self.kampfstil = ""
        self.anzeigename = ""
        
class Nahkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()

class Fernkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()
        self.lz = 1

class Ruestung(Objekt):
    def __init__(self):
        super().__init__()
        self.typ = 0
        self.system = 0
        self.be = 0
        self.rs = [0,0,0,0,0,0]
        # Bein LArm RArm Bauch Brust Kopf

    def getRSGesamt(self):
        return round(sum(self.rs) / 6, 2)

    def getRSGesamtInt(self):
        return int(sum(self.rs) / 6 + 0.5)