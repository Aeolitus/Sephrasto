del Build
python "C:\Users\Aeolitus\Anaconda3\Scripts\cxfreeze" --target-dir=C:\Users\Aeolitus\Desktop\Sephrasto\Build ^
--base-name=Win32GUI ^
--include-modules=lxml._elementpath,os --icon=icon_multi.ico ^
C:\Users\Aeolitus\Desktop\Sephrasto\Sephrasto.py
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\IncludeInBuildFolder\* C:\Users\Aeolitus\Desktop\Sephrasto\Build
mkdir Build\Library\plugins\platforms
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\IncludeInBuildFolder\Library\plugins\platforms\* ^
C:\Users\Aeolitus\Desktop\Sephrasto\Build\Library\plugins\platforms
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\datenbank.xml C:\Users\Aeolitus\Desktop\Sephrasto\Build
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\Charakterbogen.pdf C:\Users\Aeolitus\Desktop\Sephrasto\Build
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\Gebrauchsanleitung.pdf C:\Users\Aeolitus\Desktop\Sephrasto\Build
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\ExtraSpells.pdf C:\Users\Aeolitus\Desktop\Sephrasto\Build
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\icon_large.png C:\Users\Aeolitus\Desktop\Sephrasto\Build
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\icon_multi.ico C:\Users\Aeolitus\Desktop\Sephrasto\Build