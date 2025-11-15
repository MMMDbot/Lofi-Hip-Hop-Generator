@echo off
REM Simple launcher for Lofi Hip Hop Generator GUI

title Lofi Hip Hop Generator

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please run EASY_INSTALL.bat first
    echo.
    pause
    exit /b 1
)

REM Launch GUI
echo Starting Lofi Hip Hop Generator...
echo.

python gui.py

REM If GUI closes with error, show message
if errorlevel 1 (
    echo.
    echo GUI closed with an error.
    echo Check the error message above.
    echo.
    pause
)
