import importlib.util
import os
import os.path
import logging
import sys
from Hilfsmethoden import Hilfsmethoden

class PluginLoader:
    @staticmethod
    def getPlugins(path):
        plugins = []
        if not os.path.isdir(path):
            return plugins

        for i in Hilfsmethoden.listdir(path):
            location = os.path.join(path, i)
            if not os.path.isdir(location) or not "__init__.py" in Hilfsmethoden.listdir(location):
                continue
            plugins.append(i)
        return plugins

    @staticmethod
    def loadPlugin(basePath, pluginName):
        if not basePath in sys.path:
            sys.path.append(basePath)
        module = importlib.import_module(pluginName, basePath)

        try:
            plugin = module.Plugin()
        except:
            logging.critical("Couldn't load plugin because class Plugin is missing: " + pluginName)
            return
        return plugin