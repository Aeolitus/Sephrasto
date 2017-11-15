# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:02:26 2017

@author: Aeolitus
"""
class Wolke:
    Char = None
    DB = None
    Reqs = True
    Debug = False
    Fehlercode = 0
    ''' Available Error Codes:
         0: No Error
        -1: General, unspecified Error
        
        ### Database Errors
            -20: Cannot parse database
            
            -21: Error loading Vorteile
            -22: Error loading Talente
            -23: Error loading Fertigkeiten
            -24: Error loading Übernatürliches
            -25: Error loading Waffen
            
            -26: General Error writing database
            -27: Error writing Vorteile
            -28: Error writing Talente
            -29: Error writing Fertigkeiten
            -30: Error writing Übernatürliches
            -31: Error writing Waffen
            -32: Error writing database to file systems
            
        ### Character Errors
            -41: Error clearing character
            -42: Error parsing character
            -43: Error reading general info
            -44: Error reading attributes
            -45: Error reading vorteile
            -46: Error reading Fertigkeiten
            -47: Error reading Freie Fertigkeiten
            -48: Error reading Rüstungen
            -49: Error reading Waffen
            -50: Error reading Ausrüstung
            -51: Error reading Übernatürliches
            -52: Error reading EP
            
            -53: Error starting character saving
            -54: Error writing general info
            -55: Error writing attributes
            -56: Error writing Vorteile
            -57: Error writing Fertigkeiten
            -58: Error writing Freie Fertigkeiten
            -59: Error writing Rüstungen
            -60: Error writing Waffen
            -61: Error writing Ausrüstung
            -62: Error writing Übernatürliches
            -63: Error writing EP
            -64: Error writing character to file system
            
        ### 
            -80:
    '''
