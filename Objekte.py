'''
In dieser Datei werden Waffen und Rüstungen definiert.
'''

import sys

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
        self.härte = -1
        
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

class Rüstung(Objekt):
    def __init__(self):
        super().__init__()
        self.be = -1
        self.rs = [-1,-1,-1,-1,-1,-1]