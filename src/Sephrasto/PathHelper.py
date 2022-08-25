import os
import platform
import unicodedata

def getSettingsFolder():
    system = platform.system()
    if system == 'Windows':
        return getDefaultUserFolder()
    elif system == 'Darwin':
        path = os.path.expanduser('~/Library/Preferences/')
        return os.path.join(path, "Sephrasto")
    else:
        path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))
        return os.path.join(path, "Sephrasto")
    return path

def getDefaultUserFolder():
    userFolder = os.path.expanduser('~')
    system = platform.system()
    if system == 'Windows':
        import ctypes.wintypes
        CSIDL_PERSONAL = 5       # My Documents
        SHGFP_TYPE_CURRENT = 0   # Get current, not default value
        buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        userFolder = buf.value or userFolder
        return os.path.join(userFolder,'Sephrasto')
    elif system == 'Linux':
        if os.path.isdir(os.path.join(userFolder,'.sephrasto')):
            return os.path.join(userFolder,'.sephrasto') # allow users to rename the folder to a hidden folder
        else:
            return os.path.join(userFolder,'sephrasto')
    elif system == 'Darwin':
        return os.path.join(userFolder, 'Documents', 'Sephrasto') # the documents folder is language-independent on macos
    else:
        return os.path.join(userFolder,'Sephrasto')

def createFolder(basePath):
    if not os.path.isdir(basePath):
        try:
            # makedirs in case parent folder does not exist
            os.makedirs(basePath)
            return True
        except:
            return False

# The os.listdir implementation is having encoding issues. On OSX the paths are non normalized utf-8, on Unix the paths might be multibyte.
def listdir(path):
    return [unicodedata.normalize('NFC', f.decode("utf-8") if isinstance(f, bytes) else f) for f in os.listdir(path)]
