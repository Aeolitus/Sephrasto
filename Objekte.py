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
        
class Waffe(Objekt):
    def __init__(self):
        super().__init__()
        self.W6 = 2
        self.plus = 2
        self.eigenschaften = ''
        self.haerte = 7
        self.fertigkeit = ''
        self.talent = ''
        self.beid = 0
        self.pari = 0
        self.reit = 0
        self.schi = 0
        self.kraf = 0
        self.schn = 0
        self.kampfstil = 0    
        
class Nahkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()
        self.rw = 0
        self.wm = 0

class Fernkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()
        self.rw = 0
        self.lz = 1

class Ruestung(Objekt):
    def __init__(self):
        super().__init__()
        self.be = -1
        self.rs = [-1,-1,-1,-1,-1,-1]
        # Bein LArm RArm Bauch Brust Kopf