import appdirs
import json
import os
from os import walk


def getSettingsFolder():
    return appdirs.user_config_dir(appname='Sephrasto', appauthor='Ilaris')


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
