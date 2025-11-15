@echo off
REM Installation script for Lofi Hip Hop Generator (Windows)
echo ==================================
echo Lofi Hip Hop Generator Installer
echo          WINDOWS
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Python found
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate and install packages
echo [3/5] Installing Python packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Python packages installed
echo.

REM Create directories
echo [4/5] Creating directories...
if not exist output mkdir output
if not exist data mkdir data
if not exist midi_songs mkdir midi_songs
echo Directories created
echo.

REM Check for MIDI files
echo [5/5] Checking MIDI files...
dir /b midi_songs\*.mid >nul 2>&1
if errorlevel 1 (
    echo WARNING: No MIDI files found in midi_songs\
    echo Please add MIDI files before training the model.
) else (
    for /f %%i in ('dir /b midi_songs\*.mid ^| find /c /v ""') do set count=%%i
    echo Found %count% MIDI files in midi_songs\
)
echo.

echo ==================================
echo Installation Complete!
echo ==================================
echo.
echo IMPORTANT: Install system dependencies manually:
echo.
echo 1. FFmpeg:
echo    - Download from: https://www.gyan.dev/ffmpeg/builds/
echo    - Extract and add to PATH
echo    - OR use: winget install ffmpeg
echo.
echo 2. FluidSynth (for MIDI to audio):
echo    - Download from: https://github.com/FluidSynth/fluidsynth/releases
echo    - Install and add to PATH
echo.
echo 3. SoundFont (optional):
echo    - Download GeneralUser GS from:
echo      https://schristiancollins.com/generaluser.php
echo.
echo Next steps:
echo 1. Install FFmpeg and FluidSynth (see above)
echo 2. Activate environment: venv\Scripts\activate.bat
echo 3. Add MIDI files to midi_songs\
echo 4. Train model: python main.py train
echo 5. OR use GUI: python gui.py
echo.
pause
