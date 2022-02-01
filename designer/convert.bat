@ECHO OFF

cd /d %0\..

for /r %%f in (*.ui) do (
    ECHO pyuic5.exe -x %%~nf.ui -o ../src/Sephrasto/UI/%%~nf.py
    CALL pyuic5.exe -x %%~nf.ui -o ../src/Sephrasto/UI/%%~nf.py
)

PAUSE