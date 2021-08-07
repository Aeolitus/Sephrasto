@ECHO OFF

cd /d %0\..

for /r %%f in (*.ui) do (
    ECHO pyuic5.exe -x %%~nf.ui -o ../%%~nf.py
    CALL pyuic5.exe -x %%~nf.ui -o ../%%~nf.py
)

PAUSE