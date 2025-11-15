@echo off
REM ============================================
REM  LOFI HIP HOP GENERATOR
REM  Instalación Automática con Un Click
REM ============================================

echo.
echo  ========================================
echo   LOFI HIP HOP GENERATOR - AUTO INSTALL
echo  ========================================
echo.
echo  Este instalador configurara TODO automaticamente:
echo  - Python packages
echo  - FFmpeg (video/streaming)
echo  - Directorios necesarios
echo.
echo  Tiempo estimado: 5-10 minutos
echo.
pause

REM Check Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python no esta instalado!
    echo.
    echo  Por favor instala Python 3.8+ desde:
    echo  https://www.python.org/downloads/
    echo.
    echo  IMPORTANTE: Marca "Add Python to PATH" durante instalacion
    echo.
    pause
    exit /b 1
)

python --version
echo  OK - Python encontrado
echo.

REM Install Python packages
echo [2/4] Instalando paquetes de Python...
echo  (Esto puede tomar varios minutos...)
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo  ADVERTENCIA: Algunos paquetes fallaron
    echo  Intentando de nuevo...
    pip install -r requirements.txt
)

echo  OK - Paquetes instalados
echo.

REM Create directories
echo [3/4] Creando directorios...
if not exist output mkdir output
if not exist data mkdir data
if not exist midi_songs mkdir midi_songs
echo  OK - Directorios creados
echo.

REM Install FFmpeg
echo [4/4] Instalando FFmpeg...
echo.
echo  Opcion 1: Winget (automatico)
echo  Opcion 2: Manual (seguir instrucciones)
echo  Opcion 3: Omitir (instalar despues)
echo.
choice /C 123 /M "Elige opcion"

if errorlevel 3 goto skip_ffmpeg
if errorlevel 2 goto manual_ffmpeg
if errorlevel 1 goto winget_ffmpeg

:winget_ffmpeg
echo  Instalando FFmpeg con winget...
winget install ffmpeg --silent
if errorlevel 1 (
    echo  Winget no disponible, usando metodo manual...
    goto manual_ffmpeg
)
echo  OK - FFmpeg instalado
goto check_ffmpeg

:manual_ffmpeg
echo.
echo  Ejecutando instalador Python de dependencias...
python setup_dependencies.py
goto check_ffmpeg

:skip_ffmpeg
echo  FFmpeg omitido - puedes instalarlo despues
goto finish

:check_ffmpeg
echo.
echo  Verificando FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ADVERTENCIA: FFmpeg no detectado en PATH
    echo  Puede que necesites reiniciar tu PC
    echo  o seguir las instrucciones en INSTALL_FFMPEG_WINDOWS.md
) else (
    echo  OK - FFmpeg funcionando
)

:finish
echo.
echo  ========================================
echo   INSTALACION COMPLETA!
echo  ========================================
echo.
echo  Proximos pasos:
echo.
echo  1. Si instalaste FFmpeg, REINICIA tu PC
echo     (para que PATH se actualice)
echo.
echo  2. Abre una NUEVA ventana de Command Prompt
echo.
echo  3. Ejecuta la GUI:
echo     cd %CD%
echo     python gui.py
echo.
echo  4. O ejecuta el launcher:
echo     LAUNCH_GUI.bat
echo.
echo  Para ayuda, lee: START_HERE.md
echo.
echo  ========================================
echo.
pause
