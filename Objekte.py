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
        self.W6 = 2
        self.plus = 2
        self.eigenschaften = ''
        self.haerte = 7
        
class Nahkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()
        self.rw = 0
        self.wm = 0

class Fernkampfwaffe(Waffe):
    def __init__(self):
        super().__init__()
        self.rwnah = 0
        self.rwfern = 0
        self.lz = 1

class Ruestung(Objekt):
    def __init__(self):
        super().__init__()
        self.be = -1
        self.rs = [-1,-1,-1,-1,-1,-1]
        # Bein LArm RArm Bauch Brust Kopf