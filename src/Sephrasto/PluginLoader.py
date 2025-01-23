import importlib.util
import os
import os.path
import logging
import sys
import PathHelper
import Version
import json

class PluginData(object):
    def __init__(self, path, name, loadable):
        super().__init__()
        self.path = path
        self.loadable = loadable
        self.name = name
        self.anzeigename = name
        self.beschreibung = ""
        self.autor = "Unbekannt"
        self.version = [1, 0, 0, 0]
        self.hasSettings = False
        self.dependencies = []
        with open(os.path.join(path, name, "manifest.json"), "r", encoding='utf8') as f:
            manifest = json.load(f)
            if "version" in manifest:
                self.version = Version.fromString(manifest["version"])
            if "description" in manifest:
                self.beschreibung = manifest["description"]
            if "name" in manifest:
                self.anzeigename = manifest["name"]
            if "author" in manifest:
                self.autor = manifest["author"]
            if "hasSettings" in manifest:
                self.hasSettings = manifest["hasSettings"]
            if "dependencies" in manifest:
                self.dependencies = manifest["dependencies"]
                for dep in self.dependencies:
                    dep["version"] = Version.fromString(dep["version"])
        self.plugin = None

    def load(self):
        if not self.loadable:
            return False
        try:
            if not self.path in sys.path:
                sys.path.append(self.path)
            module = importlib.import_module(self.name, self.path)
            self.plugin = module.Plugin()
            return True
        except Exception as e:
            logging.critical("Couldn't load plugin, most likely because class Plugin is missing: " + self.name)
            logging.critical(str(e))
            return False

    def isLoaded(self): return self.plugin is not None
    def showSettings(self): self.plugin.showSettings()

class PluginLoader:
    @staticmethod
    def getPlugins(path):
        plugins = []
        if not os.path.isdir(path):
            return plugins

        for file in PathHelper.listdir(path):
            location = os.path.join(path, file)
            if not os.path.isdir(location):
                continue
            contents = PathHelper.listdir(location)
            if not "manifest.json" in contents:
                continue
            plugins.append(PluginData(path, file, "__init__.py" in contents))
        return plugins