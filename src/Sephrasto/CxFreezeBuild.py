import sys
from cx_Freeze import setup, Executable
import Version
import os
import shutil
from distutils.dir_util import copy_tree

print("Cleaning build folder")
dir_path = os.path.dirname(os.path.realpath(__file__))
build_path_root = os.path.join(dir_path, "..", "..", "build")
build_path = os.path.join(build_path_root, "Sephrasto")
platforms_path = os.path.join(build_path, "platforms")
styles_path = os.path.join(build_path, "styles")
doc_path = os.path.join(build_path, "Doc")
bin_path = os.path.join(build_path, "Bin")
data_path = os.path.join(build_path, "Data")

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
    "excludes" : ["tkinter", "distutils", "html", "unittest", "pydoc", "bz2", "pyexpat", "lzma", "PySide6.QtNetwork"],
    "optimize" : 2,
    "zip_include_packages" : "*",
    "zip_exclude_packages" : "",
    "include_msvcr" : True
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = 'Sephrasto',
        description = 'Charakter-Generierungstool für Ilaris',
        version = str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build),
        options = {"build_exe" : build_exe_options },
        py_modules = [],
        executables = [Executable("Sephrasto.py", base=base, icon="icon_multi.ico")])
        
# Remove unneeded files
print("Removing unneeded files")
removeFiles = [
    # none atm
]

for filename in removeFiles:
    print(filename)
    filepath = os.path.join(build_path, filename)
    if os.path.isdir(filepath) or os.path.isfile(filepath):
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)

# The python dlls need to be ALSO present inside the lib folder for Sephrasto to work on non-dev PCs
# TODO: remove this once newer cx_freeze versions fix the issue
shutil.copy2(os.path.join(build_path, "python3.dll"), os.path.join(build_path, "lib", "python3.dll"))
shutil.copy2(os.path.join(build_path, "python37.dll"), os.path.join(build_path, "lib", "python37.dll"))
             
# Copy additional files and folders to build folder
print("Copying additional files and folders to build folder")

includeFiles = {
    "Data" : data_path,
    "Doc" : doc_path,
    "icon_large.png" : build_path,
    "icon_multi.ico" : build_path,
}

if sys.platform == "win32":
    includeFiles.update({
        "Bin/ImageMagick" : os.path.join(bin_path, "ImageMagick")
    })

# Now do the actual copying
for file,targetDir in includeFiles.items():
    if not os.path.isfile(file) and not os.path.isdir(file):
        print("Error, file not found: " + file)
        cleanBuildFolder()
        sys.exit()

    if os.path.isfile(file):
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        shutil.copy2(file, targetDir)
    else:
        if not os.path.exists(os.path.dirname(targetDir)):
            os.makedirs(os.path.dirname(targetDir))
        shutil.copytree(file, targetDir)

# Zip the build
archiveName = "Sephrasto_v" + str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build)
print("Creating archive " + archiveName + ".zip")

shutil.make_archive(os.path.join(dir_path, archiveName), 'zip', build_path_root)
shutil.move(os.path.join(dir_path, archiveName) + ".zip", os.path.join(build_path_root, archiveName) + ".zip")

print("Build completed")