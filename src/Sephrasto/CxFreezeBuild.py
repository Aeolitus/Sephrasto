import sys
from cx_Freeze import setup, Executable
import Version
import os
import shutil
from distutils.dir_util import copy_tree
import platform
import subprocess

print("Cleaning build folder")
dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.join(dir_path, "..", "..")
build_path_root = os.path.join(project_path,  "build")
build_path = os.path.join(build_path_root, "Sephrasto")
doc_path = os.path.join(build_path, "Doc")
bin_path = os.path.join(build_path, "Bin")
data_path = os.path.join(build_path, "Data")

system = platform.system()

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
    "bin_excludes": ["Qt6Pdf.dll", "Qt6PdfWidgets.dll", "Qt6PdfQuick.dll", "Qt6Svg.dll", "Qt6VirtualKeyboard.dll", "Qt6WebSockets.dll", "Qt6WebEngineQuick.dll"],
    "includes" : ["multiprocessing", "PySide6.QtPrintSupport", "PySide6.QtWebChannel", "PySide6.QtWebEngineWidgets", "QtUtils.SimpleSettingsDialog", "json"],
    "excludes" : ["tkinter", "distutils", "html", "unittest", "pydoc", "bz2", "pyexpat", "lzma", "email", "xml", "ssl", "socket", "_hashlib", "http", "test", "asyncio", "queue", "select", "xmlrpc", "PySide6.QtSvg", "PySide6.QtVirtualKeyboard", "PySide6.QtWebSockets", "PySide6.QtWebEngineQuick"],
    "optimize" : 2,
    "zip_include_packages" : "*",
    "zip_exclude_packages" : [],
    "include_msvcr" : True,
    "include_files" : ["Data", "Doc", "icon_large.png", "icon_multi.ico", ["Bin/" + system, "Bin/" + system]]
}

base = None
if system == "Windows":
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
    "frozen_application_license.txt", #we already have that in Acknowledgements.md
    "lib/PySide6/opengl32sw.dll",
    "lib/PySide6/QtWebSockets.pyd",
    "lib/PySide6/QtSvg.pyd",
    "lib/PySide6/QtWebEngineQuick.pyd",
    "lib/PySide6/resources/qtwebengine_devtools_resources.pak",
    "lib/PySide6/resources/qtwebengine_resources_100p.pak",
    "lib/PySide6/resources/qtwebengine_resources_200p.pak",
    "lib/PySide6/translations",
    "lib/PySide6/bin",
    "lib/PySide6/plugins/tls",
    "lib/PySide6/plugins/platforminputcontexts",
    "lib/PySide6/plugins/networkinformation",
    "lib/PySide6/plugins/iconengines",
    "lib/PySide6/plugins/generic",
    "lib/PySide6/d3dcompiler_47.dll",
    "lib/D3DCOMPILER_47.dll",
]

for filename in removeFiles:
    print(filename)
    filepath = os.path.join(build_path, filename)
    if os.path.isdir(filepath) or os.path.isfile(filepath):
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)
             
# Zip the build
archiveName = "Sephrasto_v" + str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build)
print("Creating archive " + archiveName + ".zip")


if system == "Windows":
    # We are using 7-zip for better compression with deflate64. This compression is natively supported by windows 7+.
    # This is a nice tool for building the commandline args: https://axelstudios.github.io/7z/#!/
    # Note: Windows 11 now natively supports .7z, sometime in the future we can maybe switch...
    sevenZip = os.path.join(project_path, "tools", "7-zip", "7za.exe")
    subprocess.check_output([sevenZip, "a", "-tzip", "-mx7", "-mm=Deflate64", os.path.join(dir_path, archiveName) + ".zip", build_path], stderr=subprocess.STDOUT)
else:
    shutil.make_archive(os.path.join(dir_path, archiveName), 'zip', build_path_root)

shutil.move(os.path.join(dir_path, archiveName) + ".zip", os.path.join(build_path_root, archiveName) + ".zip")

print("Build completed")