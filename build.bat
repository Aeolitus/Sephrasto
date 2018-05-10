@ECHO OFF

cd /d %0\..

rmdir /s /q Build

python CxFreezeBuild.py build

if %errorlevel% neq 0 (
    ECHO Canceling build due to error.
    PAUSE
    exit /b %errorlevel%
)

COPY /Y IncludeInBuildFolder\* Build
mkdir Build\Library\plugins\platforms
COPY /Y IncludeInBuildFolder\Library\plugins\platforms\* Build\Library\plugins\platforms
COPY /Y datenbank.xml Build
COPY /Y Charakterbogen.pdf Build
COPY /Y Charakterbogen_lang.pdf Build
COPY /Y Regeln.pdf Build
COPY /Y Gebrauchsanleitung.pdf Build
COPY /Y ExtraSpells.pdf Build
COPY /Y icon_large.png Build
COPY /Y icon_multi.ico Build

PAUSE