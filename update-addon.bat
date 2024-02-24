@echo off

set AnkiPath="D:\Program Files\Anki\anki.exe"
set AddonPath="C:\Users\feath\AppData\Roaming\Anki2\addons21"
set AddonName="KBjoint"
REM set FFSPath="C:\Program Files\FreeFileSync\FreeFileSync.exe"

REM Close Anki if the process exists
tasklist /FI "IMAGENAME eq anki.exe" 2>NUL | find /I /N "anki.exe">NUL
if "%ERRORLEVEL%"=="0" taskkill /f /im anki.exe

REM Update Addon files
if exist "%AddonPath%\%AddonName%" (
    rmdir /s /q "%AddonPath%\%AddonName%"
    echo Addon files exist.
    )
xcopy ".\%AddonName%" "%AddonPath%\%AddonName%" /E /I /Y
REM %FFSPath% ".\UpdateAddon.ffs_batch"

REM Wait for a moment before reopening Anki (optional)
REM timeout /t 2 /nobreak >nul

REM Reopen Anki
start "" %AnkiPath%