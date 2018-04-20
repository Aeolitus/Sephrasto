echo "NICHT VERGESSEN, DIE SETTINGS ZU BEREINIGEN"
del Build
py "C:\Program Files (x86)\Python36-32\Scripts\cxfreeze" --target-dir=C:\Users\Lennart\Desktop\Sephrasto\Build ^
--base-name=Win32GUI ^
--include-modules=lxml._elementpath,os --icon=icon_multi.ico ^
C:\Users\Lennart\Desktop\Sephrasto\Sephrasto.py
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\IncludeInBuildFolder\* C:\Users\Lennart\Desktop\Sephrasto\Build
mkdir Build\Library\plugins\platforms
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\IncludeInBuildFolder\Library\plugins\platforms\* ^
C:\Users\Lennart\Desktop\Sephrasto\Build\Library\plugins\platforms
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\datenbank.xml C:\Users\Lennart\Desktop\Sephrasto\Build
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\Charakterbogen.pdf C:\Users\Lennart\Desktop\Sephrasto\Build
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\Gebrauchsanleitung.pdf C:\Users\Lennart\Desktop\Sephrasto\Build
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\ExtraSpells.pdf C:\Users\Lennart\Desktop\Sephrasto\Build
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\icon_large.png C:\Users\Lennart\Desktop\Sephrasto\Build
COPY /Y C:\Users\Lennart\Desktop\Sephrasto\icon_multi.ico C:\Users\Lennart\Desktop\Sephrasto\Build