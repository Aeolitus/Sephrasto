python C:\Users\Aeolitus\Anaconda3\Scripts\cxfreeze --target-dir=C:\Users\Aeolitus\Desktop\Sephrasto\Build ^
--include-modules=lxml._elementpath,os C:\Users\Aeolitus\Desktop\Sephrasto\Sephrasto.py
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\IncludeInBuildFolder\* C:\Users\Aeolitus\Desktop\Sephrasto\Build
mkdir Build\Library\plugins\platforms
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\IncludeInBuildFolder\Library\plugins\platforms\* ^
C:\Users\Aeolitus\Desktop\Sephrasto\Build\Library\plugins\platforms
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\datenbank.xml C:\Users\Aeolitus\Desktop\Sephrasto\Build
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\Charakterbogen.pdf C:\Users\Aeolitus\Desktop\Sephrasto\Build
COPY /Y C:\Users\Aeolitus\Desktop\Sephrasto\pdftk_server-2.02-win-setup.exe C:\Users\Aeolitus\Desktop\Sephrasto\Build