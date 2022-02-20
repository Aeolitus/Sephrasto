from PyQt5 import QtWidgets, QtCore, QtGui
from EventBus import EventBus
from CharakterEditor import Tab
from LangerBogenBeschreibung import CharakterBeschreibungExtWrapper
from LangerBogenBeschreibung import CharakterBeschreibungExt

class Plugin:
    def __init__(self):
        self.charakterBeschreibungExtTab = None
        EventBus.addFilter("class_beschreibung_wrapper", self.classBeschreibungWrapperHandler)
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
        self.charakterBeschreibungExtTab.init()
        beschreibungExtTab = Tab(15, self.charakterBeschreibungExtTab, self.charakterBeschreibungExtTab.form, "Beschreibung")
        return [beschreibungExtTab]

    def classBeschreibungWrapperHandler(self, wrapper, params):
        return None

    def charakterEditorOpenHandler(self, params):
        self.charakterBeschreibungExtTab = CharakterBeschreibungExtWrapper.CharakterBeschreibungExtWrapper()

    def charakterXmlLadenHook(self, root, params):
        if self.charakterBeschreibungExtTab is None:
            return root
        return self.charakterBeschreibungExtTab.charakterXmlLadenHook(root)

    def charakterXmlSchreibenHook(self, root, params):
        if self.charakterBeschreibungExtTab is None:
            return root
        return self.charakterBeschreibungExtTab.charakterXmlSchreibenHook(root)

    def pdfExportHook(self, fields, params):
        if self.charakterBeschreibungExtTab is None:
            return fields
        return self.charakterBeschreibungExtTab.pdfExportHook(fields)

    def pdfConcatHook(self, pages, params):
        if self.charakterBeschreibungExtTab is None:
            return pages
        return self.charakterBeschreibungExtTab.pdfConcatHook(pages)

    def vorteilGekauftHandler(self, params):
        if self.charakterBeschreibungExtTab is None:
            return
        self.charakterBeschreibungExtTab.vorteilGekauftHandler(params["name"])

    def vorteilEntferntHandler(self, params):
        if self.charakterBeschreibungExtTab is None:
            return
        self.charakterBeschreibungExtTab.vorteilEntferntHandler(params["name"])
        
    def cbextUpdateHandler(self, params):
        if self.charakterBeschreibungExtTab is None:
            return
        self.charakterBeschreibungExtTab.cbextUpdateHandler(params["name"], params["value"])
        
    def cbextGetHook(self, value, params):
        if self.charakterBeschreibungExtTab is None:
            return value
        return self.charakterBeschreibungExtTab.cbextGetHook(params["name"])

    def cbextAddWidgetHandler(self, params):
        if self.charakterBeschreibungExtTab is None:
            return
        self.charakterBeschreibungExtTab.addWidgetHandler(params["widget"], params["row"], params["column"])