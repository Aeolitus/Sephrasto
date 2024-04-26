@ECHO OFF

CALL venv\Scripts\activate.bat
cd /d %0\..\src\Sephrasto\
python CxFreezeBuild.py build
@pause