@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto use_python
py -3 run.py --demo %*
if errorlevel 1 pause
goto :eof

:use_python
python run.py --demo %*
if errorlevel 1 pause
