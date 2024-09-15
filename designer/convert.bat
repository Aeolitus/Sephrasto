@ECHO OFF

cd /d %0\..

for /r %%f in (*.ui) do (
    ECHO ..\venv\Scripts\pyside6-uic.exe %%~nf.ui -o ../src/Sephrasto/UI/%%~nf.py
    CALL ..\venv\Scripts\pyside6-uic.exe %%~nf.ui -o ../src/Sephrasto/UI/%%~nf.py
)

PAUSE