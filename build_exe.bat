@echo off
setlocal
REM Build SM809 Wired Studio into one portable .exe from SM809WiredStudio.spec.
REM Every run deletes the previous build AND the runtime folders, then builds:
REM   build\SM809WiredStudio   PyInstaller work files
REM   dist                     previous exe plus its runtime data\config\logs
REM   data                     device tables copied from seed at first launch
REM A new data\ is recreated from seed on the next launch, so the exe starts
REM with the one factory "Profile". Your source config\ library is NOT touched.
REM Output: dist\SM809WiredStudio.exe
REM Requires PyInstaller in .venv (or on PATH), plus PySide6 + hidapi.

cd /d "%~dp0"

set "SPEC=SM809WiredStudio.spec"
set "APP=SM809WiredStudio"
set "EXE=dist\%APP%.exe"
set "WORK=build\%APP%"

if not exist "%SPEC%" (
    echo ERROR: %SPEC% was not found in "%CD%".
    echo Run this file from the folder that contains the spec.
    pause
    exit /b 1
)

REM Never delete anything while the app is running: Windows locks the exe and
REM a half-deleted data\ folder would be worse than an old build.
tasklist /FI "IMAGENAME eq %APP%.exe" 2>nul | "%SystemRoot%\System32\find.exe" /I "%APP%.exe" >nul
if not errorlevel 1 (
    echo ERROR: %APP%.exe is still running.
    echo Quit it from the tray icon, then run this again.
    pause
    exit /b 1
)

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

"%PY%" -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed for "%PY%".
    echo Install it with:  "%PY%" -m pip install pyinstaller
    pause
    exit /b 1
)

echo Removing the previous build and runtime folders...
if exist "%WORK%" rmdir /s /q "%WORK%"
if exist "dist" rmdir /s /q "dist"
if exist "data" rmdir /s /q "data"
if exist "dist" (
    echo ERROR: could not delete the dist folder.
    echo Close any app still using files in "%CD%\dist" and retry.
    pause
    exit /b 1
)
if exist "data" (
    echo ERROR: could not delete the data folder.
    echo Close the studio or a source run and retry.
    pause
    exit /b 1
)

echo Building %APP%.exe from %SPEC% ...
"%PY%" -m PyInstaller --noconfirm --clean "%SPEC%"
if errorlevel 1 (
    echo.
    echo BUILD FAILED. See the PyInstaller output above.
    pause
    exit /b 1
)

if not exist "%EXE%" (
    echo.
    echo ERROR: PyInstaller finished but "%EXE%" is missing.
    pause
    exit /b 1
)

echo.
echo Done: "%CD%\%EXE%"
echo A fresh data folder will be created from seed on first launch.
pause
endlocal
