# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:02:26 2017

@author: Aeolitus
"""

class _DefaultSettings:
    WindowSizeDefault1Col = [461, 522]
    WindowSizeDefault2Col = [928, 522]

class CharakterbogenInfo:
    def __init__(self):
        self.filePath = ""
        self.maxVorteile = 0
        self.maxKampfVorteile = 0
        self.maxÜberVorteile = 0
        self.maxFreie = 0
        self.maxFertigkeiten = 0
        self.maxÜberFertigkeiten = 0
        self.maxÜberTalente = 0
        self.seitenProfan = 0
        self.kurzbogenHack = False
        self.beschreibungDetails = False
        self.bild = False
        self.bildOffset = [0, 0]

class Wolke:
    Char = None
    DB = None
    Charakterbögen = {}
    Settings = {
        'Version' : 2,
        'Bogen': "Standard Charakterbogen", 
        'Datenbank': None, 
        'Charakter-Assistent' : True,
        'Cheatsheet': True, 
        'Cheatsheet-Fontsize' : 0,
        'Pfad-Chars': '',
        'Pfad-Regeln': '',
        'Pfad-Plugins': '',
        'Pfad-Charakterbögen': '',
        'Deaktivierte-Plugins': ['CharakterBeschreibungExt'],
        'Logging': 1,
        'PDF-Open': True,
        'UpdateCheck_Disable' : False,
        'UpdateCheck_DisableFor' : '',
        'Theme' : "Ilaris",
        'Font' : "",
        'FontSize' : 0,
        'FontHeading' : "",
        'FontHeadingSize' : 0,
        'IconSize' : 0,
        'WindowSize-Main' : [286, 346],
        'WindowSize-Charakter' : [1130, 903],
        'WindowSize-TalentProfan' : [650, 366],
        'WindowSize-TalentUeber' : _DefaultSettings.WindowSizeDefault2Col,
        'WindowSize-FreieFert' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-Waffen' : _DefaultSettings.WindowSizeDefault2Col,
        'WindowSize-Ruestungen' : _DefaultSettings.WindowSizeDefault2Col,
        'WindowSize-Datenbank' : [661, 582],
        'WindowSize-DBEinstellung' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBFertigkeitProfan' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBFertigkeitUeber' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBFreieFert' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBManoever' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBRuestung' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBTalent' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBVorteil' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBWaffeneigenschaft' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-DBWaffe' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-Einstellungen' : [589, 903],
    }
    FontHeadingSizeL1 = 0
    FontHeadingSizeL3 = 0
    HeadingColor = "#000000"
    BorderColor = "rgba(0,0,0,0.2)"
    DefaultOSFont = "Segoe UI"
    DefaultOSFontSize = 9