# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:02:26 2017

@author: Aeolitus
"""

import os

class _DefaultSettings:
    WindowSizeDefault1Col = [461, 522]
    WindowSizeDefault2Col = [928, 522]

class Wolke:
    Char = None
    DB = None
    CmdArgs = None
    Charakterbögen = {}
    Themes = {}
    Settings = {
        'Version' : 3,
        'Bogen': "Standard Charakterbogen", 
        'Datenbank': None, 
        'Charakter-Assistent' : True,
        'Cheatsheet': True, 
        'Cheatsheet-Fontsize' : 8,
        'Formular-Editierbarkeit' : True,
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
        'Font' : "Crimson Pro",
        'FontSize' : 0, # we default this to os font size after start
        'FontHeading' : "Aniron",
        'FontHeadingSize' : 8,
        'CharListCols' : 1,
        'CharListRows' : 5,
        'DPI-Skalierung' : False,
        'WindowSize-Main' : [426, 594],
        'WindowSize-Charakter' : [1230, 970],
        'WindowSize-TalentProfan' : [650, 366],
        'WindowSize-TalentUeber' : _DefaultSettings.WindowSizeDefault2Col,
        'WindowSize-FreieFert' : _DefaultSettings.WindowSizeDefault1Col,
        'WindowSize-Waffen' : _DefaultSettings.WindowSizeDefault2Col,
        'WindowSize-Ruestungen' : _DefaultSettings.WindowSizeDefault2Col,
        'WindowSize-Datenbank' : [1056, 738],
        'WindowSize-Einstellungen' : [701, 956],
        'WindowSize-Regelanhang' : _DefaultSettings.WindowSizeDefault1Col,
        'Letzte-Chars' : [],
    }
    FontHeadingSizeL1 = 0
    FontHeadingSizeL3 = 0
    HeadingColor = "#000000"
    BorderColor = "rgba(0,0,0,0.2)"
    ReadonlyColor = "#ffffff"
    PanelColor = "#b3b3b3"
    DefaultOSFont = ""
    DefaultOSFontSize = 9
    FontAwesomeCSS = "" # Qt does not support 'class' in span tags (yet), so we store the style here for reuse in the app
    FontAwesomeFont = None
    FontAwesomeRegularFont = None
    CharImageSize = [260.0, 340.0]