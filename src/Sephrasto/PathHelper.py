import json
import os
import sys
from os import walk

from PyQt5.QtCore import QStandardPaths


def getSettingsFolder():
    return os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation), 'Sephrasto')

def getDefaultUserFolder():
    return os.path.join(os.path.expanduser('~'), 'Sephrasto')


def createFolder(basePath):
    if not os.path.isdir(basePath):
        try:
            # makedirs in case parent folder does not exist
            os.makedirs(basePath)
            return True
        except:
            return False


def getThemes():
    result = []
    try:
        settings = getSettingsFolder()
        themeFolder = os.path.join(settings, "themes")
        createFolder(themeFolder)
        filenames = next(walk(themeFolder), (None, None, []))[2]
        themes = [x for x in filenames if x.endswith(".json")]
        for path in themes:
            file = open(os.path.join(themeFolder, path), )
            theme = json.load(file)
            if ('name' in theme):
                result.append(theme)
    except:
        pass
    return result
