import sys
from cx_Freeze import setup, Executable
import Version
import os
import shutil

print("Cleaning build folder")
dir_path = os.path.dirname(os.path.realpath(__file__))
build_path = os.path.join(dir_path, "Build")

def cleanBuildFolder():
    for filename in os.listdir(build_path):
        filepath = os.path.join(build_path, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


if os.path.exists(build_path):
    cleanBuildFolder()
else:
    os.makedirs(build_path)

print("Running cxfreeze")
build_exe_options = {
    "build_exe" : build_path,
    "includes" : ["lxml._elementpath", "os", "binascii", "shutil", "tempfile", "PyQt5.sip"],
    "optimize" : 2,
    "zip_include_packages" : ["PyQt5"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = 'Sephrasto',
        description = 'Charakter-Generierungstool für Ilaris',
        version = str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build),
        options = {"build_exe" : build_exe_options },
        executables = [Executable("Sephrasto.py", base=base, icon="icon_multi.ico")])
        
print("Copying additional files to build folder")

platforms_path = os.path.join(build_path, "platforms")
styles_path = os.path.join(build_path, "styles")
env_python_path = os.path.dirname(sys.executable)
env_plugins_path = os.path.join(env_python_path, "Lib", "site-packages", "PyQt5", "Qt", "plugins")
env_styles_path = os.path.join(env_plugins_path, "styles")
env_platforms_path = os.path.join(env_plugins_path, "platforms")
env_bin_path = os.path.join(env_python_path, "Lib", "site-packages", "PyQt5", "Qt", "bin")

includeFiles = {
    "datenbank.xml" : build_path,
    "Charakterbogen.pdf" : build_path,
    "Charakterbogen_lang.pdf" : build_path,
    "Regeln.pdf" : build_path,
    "Gebrauchsanleitung.pdf" : build_path,
    "ExtraSpells.pdf" : build_path,
    "icon_large.png" : build_path,
    "icon_multi.ico" : build_path,
    "ScriptAPI.md" : build_path,
    os.path.join(env_bin_path, "libEGL.dll"): build_path,
    os.path.join(env_styles_path, "qwindowsvistastyle.dll"): styles_path,
    os.path.join(env_platforms_path, "qminimal.dll"): platforms_path,
    os.path.join(env_platforms_path, "qoffscreen.dll"): platforms_path,
    os.path.join(env_platforms_path, "qwindows.dll"): platforms_path
}

for file,targetDir in includeFiles.items():
    print(file)
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    if not os.path.isfile(file):
        print("Error, file not found: " + file)
        cleanBuildFolder()
        sys.exit()
    shutil.copy2(file, targetDir)