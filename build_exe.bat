@echo off
REM Script to build Windows executable for Lofi Hip Hop Generator

echo ========================================
echo  Lofi Hip Hop Generator - Build Script
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment for build...
if not exist build_env (
    python -m venv build_env
)

echo [2/5] Activating environment...
call build_env\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo [4/5] Building executable with PyInstaller...
pyinstaller LofiGenerator.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo [5/5] Cleaning up...
REM Keep dist folder with the exe

echo.
echo ========================================
echo  Build Complete!
echo ========================================
echo.
echo Executable location: dist\LofiGenerator\LofiGenerator.exe
echo.
echo To create installer, run: makensis installer.nsi
echo.
pause
