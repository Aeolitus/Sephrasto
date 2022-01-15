from PyQt5 import QtWidgets, QtCore, QtGui
from EventBus import EventBus
from CharakterEditor import Tab
from LangerBogenBeschreibung import CharakterBeschreibungExtWrapper
from LangerBogenBeschreibung import CharakterBeschreibungExt

class Plugin:
    def __init__(self):
        self.charakterBeschreibungExtTab = None
        EventBus.addAction("charaktereditor_oeffnet", self.charakterEditorOpenHandler)
        EventBus.addFilter("charakter_xml_laden", self.charakterXmlLadenHook)
        EventBus.addFilter("charakter_xml_schreiben", self.charakterXmlSchreibenHook)
        EventBus.addFilter("pdf_export", self.pdfExportHook)
        EventBus.addFilter("pdf_concat", self.pdfConcatHook)
        EventBus.addAction("cbext_update", self.cbextUpdateHandler)
        EventBus.addFilter("cbext_get", self.cbextGetHook)
        EventBus.addAction("cbext_add_widget", self.cbextAddWidgetHandler)

    @staticmethod
    def getDescription():
        return "Fügt dem Charaktereditor einen zweiten Beschreibungs-Tab hinzu, in welchem die zusätzlichen Felder des langen Charakterbogens befüllt werden können."

    def changesCharacter(self):
        return True

    def createCharakterTabs(self):
        beschreibungExtTab = Tab(15, self.charakterBeschreibungExtTab, self.charakterBeschreibungExtTab.form, "Beschreibung 2")
        return [beschreibungExtTab]

    def charakterEditorOpenHandler(self, params):
        self.charakterBeschreibungExtTab = CharakterBeschreibungExtWrapper.CharakterBeschreibungExtWrapper()

    def charakterXmlLadenHook(self, root, params):
        return self.charakterBeschreibungExtTab.charakterXmlLadenHook(root)

    def charakterXmlSchreibenHook(self, root, params):
        return self.charakterBeschreibungExtTab.charakterXmlSchreibenHook(root)

    def pdfExportHook(self, fields, params):
        return self.charakterBeschreibungExtTab.pdfExportHook(fields)

    def pdfConcatHook(self, pages, params):
        return self.charakterBeschreibungExtTab.pdfConcatHook(pages)

    def vorteilGekauftHandler(self, params):
        self.charakterBeschreibungExtTab.vorteilGekauftHandler(params["name"])

    def vorteilEntferntHandler(self, params):
        self.charakterBeschreibungExtTab.vorteilEntferntHandler(params["name"])
        
    def cbextUpdateHandler(self, params):
        self.charakterBeschreibungExtTab.cbextUpdateHandler(params["name"], params["value"])
        
    def cbextGetHook(self, value, params):
        return self.charakterBeschreibungExtTab.cbextGetHook(params["name"])

    def cbextAddWidgetHandler(self, params):
        self.charakterBeschreibungExtTab.addWidgetHandler(params["widget"], params["row"], params["column"])