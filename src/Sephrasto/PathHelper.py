import json
import os
import sys
from os import walk


def getSettingsFolder():
    if sys.platform == "win32":
        path = os.getenv('LOCALAPPDATA', os.path.expanduser("~/AppData/Local"))
    elif sys.platform == 'darwin':
        path = os.path.expanduser('~/Library/Preferences')
    else:
        path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))
    path = os.path.join(path, 'Sephrasto')
    return path


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
        themeFolder = os.path.join(getSettingsFolder(), "themes")
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
