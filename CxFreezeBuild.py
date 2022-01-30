import sys
from cx_Freeze import setup, Executable
import Version
import os
import shutil

print("Cleaning build folder")
dir_path = os.path.dirname(os.path.realpath(__file__))
build_path_root = os.path.join(dir_path, "Build")
build_path = os.path.join(build_path_root, "Sephrasto")
platforms_path = os.path.join(build_path, "platforms")
styles_path = os.path.join(build_path, "styles")
doc_path = os.path.join(build_path, "Doc")
bin_path = os.path.join(build_path, "Bin")
env_python_path = os.path.dirname(sys.executable)
env_plugins_path = os.path.join(env_python_path, "Lib", "site-packages", "PyQt5", "Qt5", "plugins")
env_styles_path = os.path.join(env_plugins_path, "styles")
env_platforms_path = os.path.join(env_plugins_path, "platforms")
env_bin_path = os.path.join(env_python_path, "Lib", "site-packages", "PyQt5", "Qt5", "bin")

# Clean buildfolder and create build root folder
def cleanBuildFolder():
    for filename in os.listdir(build_path_root):
        filepath = os.path.join(build_path_root, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


if os.path.exists(build_path_root):
    cleanBuildFolder()
else:
    os.makedirs(build_path)

# Run cxfreeze to create the executable
print("Running cxfreeze")
build_exe_options = {
    "build_exe" : build_path,
    "includes" : ["multiprocessing"],
    "excludes" : ["distutils", "html", "unittest", "pydoc", "bz2", "pyexpat", "lzma"],
    "optimize" : 2,
    "zip_include_packages" : "*",
    "zip_exclude_packages" : ""
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = 'Sephrasto',
        description = 'Charakter-Generierungstool für Ilaris',
        version = str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build),
        options = {"build_exe" : build_exe_options },
        executables = [Executable("Sephrasto.py", base=base, icon="icon_multi.ico")])
        
# Remove unneeded files
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

# Copy additional files to build folder
print("Copying additional files to build folder")

includeFiles = {
    "datenbank.xml" : build_path,
    "Charakterbogen.pdf" : build_path,
    "Charakterbogen_lang.pdf" : build_path,
    "Regeln.pdf" : build_path,
    "ExtraSpells.pdf" : build_path,
    "icon_large.png" : build_path,
    "icon_multi.ico" : build_path,
}
if sys.platform == "win32":
    includeFiles.update({
        os.path.join(env_styles_path, "qwindowsvistastyle.dll"): styles_path,
        os.path.join(env_bin_path, "libEGL.dll"): build_path,
        "Bin/ImageMagick/convert.exe" : os.path.join(bin_path, "ImageMagick"),
        "Bin/ImageMagick/LICENSE.txt" : os.path.join(bin_path, "LICENSE.txt")
    })

# Include documentation
for file in os.listdir(os.path.join(dir_path, "Doc")):
    fullPath = os.path.join(dir_path, "Doc", file)
    if os.path.isfile(fullPath):
        includeFiles[fullPath] = os.path.join(build_path, "Doc")

for file in os.listdir(os.path.join(dir_path, "Doc", "Images")):
    fullPath = os.path.join(dir_path, "Doc", "Images", file)
    if os.path.isfile(fullPath):
        includeFiles[fullPath] = os.path.join(build_path, "Doc", "Images")

# Include plugins (beware, subfolders are not included)
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

# Now do the actual copying
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

# Zip the build
archiveName = "Sephrasto_v" + str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build)
print("Creating archive " + archiveName + ".zip")

shutil.make_archive(os.path.join(dir_path, archiveName), 'zip', build_path_root)
shutil.move(os.path.join(dir_path, archiveName) + ".zip", os.path.join(build_path_root, archiveName) + ".zip")

print("Build completed")
