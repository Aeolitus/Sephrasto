import importlib.util
import os
import os.path
import logging
import sys
import PathHelper

class PluginData(object):
    def __init__(self, path, name):
        super().__init__()
        self.path = path
        self.name = name
        self.description = ""

        if not self.path in sys.path:
            sys.path.append(self.path)
        self.module = importlib.import_module(self.name, self.path)

        try:
            self.description = self.module.Plugin.getDescription()
        except Exception:
            self.description = ""

        self.plugin = None

    def load(self):
        try:
            self.plugin = self.module.Plugin()
            return True
        except:
            logging.critical("Couldn't load plugin because class Plugin is missing: " + self.name)
            return False

    def isLoaded(self): return self.plugin is not None

class PluginLoader:
    @staticmethod
    def getPlugins(path):
        plugins = []
        if not os.path.isdir(path):
            return plugins

        for file in PathHelper.listdir(path):
            location = os.path.join(path, file)
            if not os.path.isdir(location) or not "__init__.py" in PathHelper.listdir(location):
                continue
            plugins.append(PluginData(path, file))
        return plugins