import sys
from cx_Freeze import setup, Executable
import Version
import os
import shutil

print("Cleaning build folder")
dir_path = os.path.dirname(os.path.realpath(__file__))
build_path = os.path.join(dir_path, "Build")
platforms_path = os.path.join(build_path, "platforms")
styles_path = os.path.join(build_path, "styles")
env_python_path = os.path.dirname(sys.executable)
env_plugins_path = os.path.join(env_python_path, "Lib", "site-packages", "PyQt5", "Qt5", "plugins")
env_styles_path = os.path.join(env_plugins_path, "styles")
env_platforms_path = os.path.join(env_plugins_path, "platforms")
env_bin_path = os.path.join(env_python_path, "Lib", "site-packages", "PyQt5", "Qt5", "bin")

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
    "excludes" : ["distutils", "html", "http", "email", "unittest", "pydoc", "socket", "bz2", "select", "pyexpat", "lzma"],
    "optimize" : 2,
    "zip_include_packages" : "*",
    "zip_exclude_packages" : "",
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = 'Sephrasto',
        description = 'Charakter-Generierungstool für Ilaris',
        version = str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build),
        options = {"build_exe" : build_exe_options },
        executables = [Executable("Sephrasto.py", base=base, icon="icon_multi.ico")])
        


print("Removing unneeded files")
removeFiles = [
    "imageFormats"
]

for filename in removeFiles:
    print(filename)
    filepath = os.path.join(build_path, filename)
    if os.path.isdir(filepath) or os.path.isfile(filepath):
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


print("Copying additional files to build folder")

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
    "PluginAPI.md" : build_path,
    os.path.join(env_styles_path, "qwindowsvistastyle.dll"): styles_path,
    os.path.join(env_bin_path, "libEGL.dll"): build_path,
}

#beware, subfolders are not included
def includePlugin(name):
    path = os.path.join(dir_path, "Plugins", name)
    if not os.path.isdir(path):
        return

    files = os.listdir(path)
    for i in files:
        file = os.path.join(path, i)

        if not os.path.basename(file) == "__pycache__" and not os.path.basename(file) == "UI":
            includeFiles[file] = os.path.join(build_path, "Plugins", name)

for dirName in os.listdir(os.path.join(dir_path, "Plugins")):
    if os.path.isdir(os.path.join(dir_path, "Plugins", dirName)):
        includePlugin(dirName)

for file,targetDir in includeFiles.items():
    print(file)
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    if not os.path.isfile(file) and not os.path.isdir(file):
        print("Error, file not found: " + file)
        cleanBuildFolder()
        sys.exit()

    if os.path.isfile(file):
        shutil.copy2(file, targetDir)
    else:
        shutil.copytree(file, os.path.join(targetDir, os.path.basename(file)))

print("Build completed")