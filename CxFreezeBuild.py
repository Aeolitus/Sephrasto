import sys
from cx_Freeze import setup, Executable
import Version

build_exe_options = {
    "build_exe" : "Build/",
    "includes" : ["lxml._elementpath", "os", "binascii", "shutil", "tempfile"],
    "optimize" : 2
    #"zip_include_packages" : ["PyQt5"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = 'Sephrasto',
        description = 'Charakter-Generierungstool für Ilaris',
        version = str(Version._sephrasto_version_major) + "." + str(Version._sephrasto_version_minor) + "." + str(Version._sephrasto_version_build),
        options = {"build_exe" : build_exe_options },
        executables = [Executable("Sephrasto.py", base=base, icon="icon_multi.ico")])