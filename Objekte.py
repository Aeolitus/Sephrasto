'''
In dieser Datei werden Waffen und Rüstungen definiert.
'''

class Objekt():
    def __init__(self):
        self.name = ''
        self.text = ''
        
class Waffe(Objekt):
    def __init__(self):
        super().__init__()
        self.W6 = -1
        self.plus = -1
        self.eigenschaften = ''
        self.haerte = -1
        
class Nahkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()
        self.rw = -1
        self.wm = -1

class Fernkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()
        self.rwnah = -1
        self.rwfern = -1
        self.lz = -1

class Ruestung(Objekt):
    def __init__(self):
        super().__init__()
        self.be = -1
        self.rs = [-1,-1,-1,-1,-1,-1]
        # Bein LArm RArm Bauch Brust Kopf