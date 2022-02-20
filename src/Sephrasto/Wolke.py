# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:02:26 2017

@author: Aeolitus
"""

class _DefaultSettings:
    WindowSizeDefault1Col = [461, 522]
    WindowSizeDefault2Col = [928, 522]

class Wolke:
    Char = None
    DB = None
    Reqs = True
    Fehlercode = 0
    Settings = {
        'Version' : 2,
        'Bogen': 0, 
        'Datenbank': None, 
        'Cheatsheet': True, 
        'Cheatsheet-Fontsize' : 0,
        'Pfad-Chars': '',
        'Pfad-Regeln': '',
        'Pfad-Plugins': '',
        'Deaktivierte-Plugins': ['CharakterBeschreibungExt'],
        'Logging': 1,
        'PDF-Open': True,
        'UpdateCheck_Disable' : False,
        'UpdateCheck_DisableFor' : '',
        'Theme' : "Ilaris",
        'Font' : "Crimson Pro",
        'FontSize' : 9,
        'FontHeading' : "Aniron",
        'FontHeadingSize' : 7,
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

    }
    HeadingColor = "#000000"
    BorderColor = "rgba(0,0,0,0.2)"
    ErrorCode = {
         0: 'No Error. You really shouldnt be seeing this.',
        -1: 'General, unspecified Error. Contact Aeolitus.',
        
    ### Database Errors
        -20: 'Cannot parse database. Is the database file intact?',
        
        -21: 'Error loading Vorteile. Is the database file empty?',
        -22: 'Error loading Talente. Please check the database file!',
        -23: 'Error loading Fertigkeiten. Please check the database file!',
        -24: 'Error loading Übernatürliches. Please check the database file!',
        -25: 'Error loading Waffen. Please check the database file!',
        -26: 'Error loading Manöver. Please check the database file!',
        -33: '''The Database file seems to be empty or not a database file! Please \
check if you have correctly selected your rulebase and whether the file contains \
any content.''',
        
        -26: 'General Error writing database. Please check your input!',
        -27: 'Error writing Vorteile. Please check your input!',
        -28: 'Error writing Talente. Please check your input!',
        -29: 'Error writing Fertigkeiten. Please check your input!',
        -30: 'Error writing Übernatürliches. Please check your input!',
        -31: 'Error writing Waffen. Please check your input!',
        -32: 'Error writing database to file systems. Do you have writing permissions?',
        -34: 'Error writing Manöver. Please check your input!',
    ### Character Errors
        -41: 'Error clearing character. Please restart Sephrasto.',
        -42: 'Error parsing character. Is the file intact, readable and valid?',
        -43: '''The file you have selected does not seem to be a valid character \
file. Is it the file you intended, created with a recent version of Sephrasto, \
and not damaged or empty?''',
        -44: 'Error reading attributes. Is the file outdated or damaged?',
        -45: 'Error reading vorteile. Is the file outdated or damaged?',
        -46: 'Error reading Fertigkeiten. Is the file outdated or damaged?',
        -47: 'Error reading Freie Fertigkeiten. Is the file outdated or damaged?',
        -48: 'Error reading Rüstungen. Is the file outdated or damaged?',
        -49: 'Error reading Waffen. Is the file outdated or damaged?',
        -50: 'Error reading Ausrüstung. Is the file outdated or damaged?',
        -51: 'Error reading Übernatürliches. Is the file outdated or damaged?',
        -52: 'Error reading EP. Is the file outdated or damaged?',
        
        -53: 'Error starting character saving. Please contact Aeolitus.',
        -54: 'Error writing general info. Are your inputs valid?',
        -55: 'Error writing attributes. Are your inputs valid?',
        -56: 'Error writing Vorteile. Are your inputs valid?',
        -57: 'Error writing Fertigkeiten. Are your inputs valid?',
        -58: 'Error writing Freie Fertigkeiten. Are your inputs valid?',
        -59: 'Error writing Rüstungen. Are your inputs valid?',
        -60: 'Error writing Waffen. Are your inputs valid?',
        -61: 'Error writing Ausrüstung. Are your inputs valid?',
        -62: 'Error writing Übernatürliches. Are your inputs valid?',
        -63: 'Error writing EP. Are your inputs valid?',
        -64: 'Error writing character to file system. Do you have writing permissions?',
        
    ### PDF writing errors
        -80: 'General Error when trying to write to pdf. Please contact Aeolitus.',
        -81: '''PDFtk-Error: The empty Charactersheet could not be loaded. Is \
PDFtk installed and working; have you restarted Sephrasto; and is the selected \
Character sheet a valid empty Charactersheet? Note that if you have a file called \
Charakterbogen.pdf in your Sephrasto folder that is not an empty character sheet, \
the export may not work or produce unforeseen results. \
PDFtk can be obtained at \n
pdflabs.com/tools/pdftk-server/\n
Note that Sephrasto must be restarted after the installation.''',
        -82: 'Error when filling Charactersheet at Name / Beschreibung.',
        -83: 'Error when filling Charactersheet at Attribute / Abgeleitete Werte.',
        -84: 'Error when filling Charactersheet at Vorteile.',
        -85: 'Error when filling Charactersheet at Fertigkeiten.',
        -86: 'Error when filling Charactersheet at Waffen / Rüstungen / Ausrüstung.',
        -87: 'Error when filling Charactersheet at Übernatürliche Fertigkeiten.',
        -88: 'Error when filling Charactersheet at Erfahrungspunkte.',
        -89: 'PDFtk-Error: The new Charactersheet could not be created. Do you \
have writing permissions? If you cannot get it to work, send me a copy of the \
character and the database and Ill take a look.',
        -91: 'Error reading ExtraSpells.pdf. Please do not rename or remove the \
File called ExtraSpells.pdf in your Sephrasto folder!',
        -92: 'Error assigning extra fields!', 
        -93: 'Error writing temporary extra page to pdf!', 
        -94: 'Error merging pdf files!',
        -95: 'Error deleting or renaming files on file system. \
Please check the created PDFs to see which one is your character!',
        -96: 'Error cutting of last page of the PDF. This shouldnt really matter.',
        -97: 'Error merging the rules page!',
        -98: 'Could not automatically open the PDF! Everything else works though.',
        -99: 'Error when trying to execute export plugin',
    ### Other Errors
        -200: 'General Error you shouldnt see. Please contact Aeolitus.'
    }
