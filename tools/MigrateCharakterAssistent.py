# Run this script to trigger a load/save on all charakter assistent files
# This will effectively apply any migrations, speeding up loading times

from pathlib import Path
import subprocess

python = "python"
sephrastoBase = "../src/Sephrasto/"
charAssistent = sephrastoBase + "Data/CharakterAssistent/"
sephrasto = sephrastoBase + "Sephrasto.py"

allFiles = [str(p.resolve()) for p in Path(charAssistent).rglob("*.xml")]

for file in allFiles:
    if file.endswith("_var.xml"):
        continue
    print("Migrating", file)
    subprocess.call([python, sephrasto, "--migrate=" + file, "--noplugins"])