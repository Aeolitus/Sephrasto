'''
In dieser Datei werden Waffen und Rüstungen definiert.
'''

class Objekt():
    def __init__(self):
        self.name = ''
        self.text = ''
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
        self.W6 = 2
        self.plus = 2
        self.eigenschaften = []
        self.haerte = 7
        self.rw = 0
        self.wm = 0
        self.fertigkeit = ''
        self.talent = ''
        self.kampfstile = []
        self.kampfstil = ""
        self.anzeigename = ""
        self.isUserAdded = True
        
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
        self.be = -1
        self.rs = [-1,-1,-1,-1,-1,-1]
        # Bein LArm RArm Bauch Brust Kopf