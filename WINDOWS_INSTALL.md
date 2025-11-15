# 🪟 Instalación para Windows

Guía completa para instalar y usar el Lofi Hip Hop Generator en Windows.

## 📋 Requisitos Previos

### 1. Python 3.8 o superior

**Descargar e instalar:**
1. Ve a https://www.python.org/downloads/
2. Descarga Python 3.8+ para Windows
3. **IMPORTANTE**: Durante la instalación, marca "Add Python to PATH"
4. Completa la instalación

**Verificar instalación:**
```cmd
python --version
```

### 2. FFmpeg (Para procesamiento de video/audio)

**⚠️ IMPORTANTE: FFmpeg es REQUERIDO para streaming y videos completos**

**Ver guía detallada**: [INSTALL_FFMPEG_WINDOWS.md](INSTALL_FFMPEG_WINDOWS.md)

**Instalación rápida:**

**Opción A - Con winget (Recomendado):**
```cmd
winget install ffmpeg
```

**Opción B - Manual:**
```cmd
# 1. Descargar de: https://www.gyan.dev/ffmpeg/builds/
# 2. Descargar "ffmpeg-release-essentials.zip"
# 3. Extraer a C:\ffmpeg
# 4. Añadir C:\ffmpeg\bin al PATH (ver guía completa)
```

**Verificar instalación:**
```cmd
# Cerrar y abrir NUEVA ventana de CMD, luego:
ffmpeg -version
```

**Si ves la versión → ✅ Instalado correctamente**
**Si dice "no se reconoce" → Sigue la guía completa en INSTALL_FFMPEG_WINDOWS.md**

### 3. FluidSynth (Para convertir MIDI a audio)

**Opción A - Instalador oficial:**
1. Descarga desde: https://github.com/FluidSynth/fluidsynth/releases
2. Busca el archivo `.exe` más reciente
3. Instala siguiendo el asistente
4. Añade la carpeta de instalación al PATH

**Opción B - Con MSYS2/MinGW:**
```cmd
pacman -S mingw-w64-x86_64-fluidsynth
```

### 4. SoundFont (Para calidad de audio)

1. Descarga GeneralUser GS: https://schristiancollins.com/generaluser.php
2. Extrae el archivo `.sf2` a `C:\soundfonts\`
3. Edita `config.yaml` y añade:
```yaml
audio:
  soundfont: 'C:\soundfonts\GeneralUser GS v1.471.sf2'
```

## 🚀 Instalación Rápida

### Método 1: Script Automático (Recomendado)

1. **Descarga el proyecto:**
```cmd
git clone https://github.com/tu-usuario/Lofi-Hip-Hop-Generator.git
cd Lofi-Hip-Hop-Generator
```

2. **Ejecuta el instalador:**
```cmd
install.bat
```

3. **Sigue las instrucciones en pantalla**

### Método 2: Manual

1. **Clona el repositorio:**
```cmd
git clone https://github.com/tu-usuario/Lofi-Hip-Hop-Generator.git
cd Lofi-Hip-Hop-Generator
```

2. **Crea entorno virtual:**
```cmd
python -m venv venv
venv\Scripts\activate
```

3. **Instala dependencias:**
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. **Crea directorios:**
```cmd
mkdir output
mkdir data
mkdir midi_songs
```

## 🎵 Uso en Windows

### Opción 1: Interfaz Gráfica (GUI) - MÁS FÁCIL ✨

**Inicia la GUI:**
```cmd
venv\Scripts\activate
python gui.py
```

La GUI te permite:
- ✅ Configurar todos los parámetros visualmente
- ✅ Generar música con un clic
- ✅ Entrenar el modelo
- ✅ Hacer streaming a YouTube/Twitch
- ✅ Ver logs en tiempo real
- ✅ No necesitas línea de comandos

### Opción 2: Línea de Comandos (PowerShell/CMD)

**Activar entorno virtual:**
```cmd
venv\Scripts\activate
```

**Entrenar el modelo:**
```cmd
python main.py train
```

**Generar video:**
```cmd
python main.py generate --notes 500 --temperature 1.0
```

**Hacer streaming:**
```cmd
python main.py stream output\video.mp4 --platform youtube --key TU_STREAM_KEY
```

## 🖥️ Guía de la GUI

### Pestaña "Generate" (Generar)

![Generate Tab](docs/images/generate_tab.png)

1. **Number of Notes**: Cantidad de notas a generar (100-1000)
2. **Creativity (Temperature)**: Nivel de creatividad (0.5 = conservador, 2.0 = experimental)
3. **Tempo (BPM)**: Velocidad de la música (60-140 BPM)
4. **Video Duration**: Duración del video en segundos
5. **Output Filename**: Nombre del archivo de salida

**Botones:**
- 🎵 Generate Music Only: Solo genera MIDI
- 🌌 Generate Aurora Only: Solo genera video de aurora
- 🎬 Generate Complete Video: Genera todo completo

### Pestaña "Train Model" (Entrenar)

1. Añade archivos MIDI a la carpeta `midi_songs\`
2. Haz clic en "📁 Open MIDI Folder" para abrir la carpeta
3. Configura Epochs y Batch Size
4. Haz clic en "🎓 Start Training"

### Pestaña "Streaming"

1. Selecciona plataforma (YouTube/Twitch/Custom)
2. Ingresa tu Stream Key
3. Selecciona el video a transmitir
4. Haz clic en "▶️ Start Stream"

**Obtener Stream Key de YouTube:**
1. Ve a YouTube Studio
2. Clic en "Emisión en directo" → "Transmitir"
3. Copia la "Clave de transmisión"

### Pestaña "Settings" (Configuración)

- Ajusta resolución del video
- Configura FPS
- Personaliza efectos de aurora
- Habilita/deshabilita estrellas

### Pestaña "Logs"

- Monitorea el progreso en tiempo real
- Ve mensajes de error
- Depura problemas

## 🔧 Solución de Problemas (Windows)

### Error: "Python no reconocido como comando"

**Solución:**
1. Reinstala Python marcando "Add to PATH"
2. O añade manualmente:
   - Busca donde se instaló Python (ej: `C:\Python310`)
   - Añade al PATH del sistema

### Error: "FFmpeg no encontrado"

**Solución:**
```cmd
# Verifica si está en PATH
where ffmpeg

# Si no, añade al PATH o reinstala
winget install ffmpeg
```

### Error: "FluidSynth failed"

**Solución:**
1. Instala FluidSynth (ver arriba)
2. O el programa usará TiMidity++ como alternativa

### Error: "No module named 'tensorflow'"

**Solución:**
```cmd
venv\Scripts\activate
pip install tensorflow
```

### Error: "MIDI to audio conversion failed"

**Solución:**
1. Instala FluidSynth
2. Descarga un SoundFont (.sf2)
3. Configura en `config.yaml`:
```yaml
audio:
  soundfont: 'C:\ruta\a\soundfont.sf2'
```

### GUI no se abre / Error de Tkinter

**Solución:**
Tkinter viene con Python, pero si falta:
```cmd
# Reinstala Python con componente tk/tcl
# O instala manualmente:
pip install tk
```

### Caracteres raros en la consola

**Solución:**
```cmd
# Cambia codificación de la consola
chcp 65001
```

## 📊 Rendimiento en Windows

### Hardware Recomendado

**Mínimo:**
- CPU: Intel i5 / AMD Ryzen 5
- RAM: 8 GB
- GPU: Integrada (funcionará, pero lento)
- Disco: 2 GB libres

**Recomendado:**
- CPU: Intel i7 / AMD Ryzen 7
- RAM: 16 GB
- GPU: NVIDIA GTX 1060 o superior (para acelerar TensorFlow)
- Disco: 5 GB libres (SSD preferido)

### Acelerar con GPU (NVIDIA)

1. **Instala CUDA Toolkit:**
   - Descarga: https://developer.nvidia.com/cuda-downloads
   - Versión compatible con TensorFlow 2.10+

2. **Instala cuDNN:**
   - Descarga: https://developer.nvidia.com/cudnn
   - Extrae archivos a carpeta CUDA

3. **Instala TensorFlow con GPU:**
```cmd
pip uninstall tensorflow
pip install tensorflow-gpu
```

4. **Verifica:**
```python
import tensorflow as tf
print("GPUs disponibles:", tf.config.list_physical_devices('GPU'))
```

## 🎯 Tips para Windows

### Usar PowerShell en lugar de CMD

PowerShell es más moderno:
```powershell
# Activar entorno virtual en PowerShell
.\venv\Scripts\Activate.ps1

# Si da error de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Crear acceso directo a la GUI

1. Clic derecho en el escritorio → Nuevo → Acceso directo
2. Ubicación:
```
C:\ruta\a\Lofi-Hip-Hop-Generator\venv\Scripts\pythonw.exe C:\ruta\a\Lofi-Hip-Hop-Generator\gui.py
```
3. Nombra: "Lofi Generator"
4. Doble clic para abrir la GUI directamente

### Programar generación automática

Usa el Programador de Tareas de Windows:
1. Abre "Programador de tareas"
2. Crear tarea básica
3. Acción: Iniciar programa
4. Programa: `C:\ruta\a\venv\Scripts\python.exe`
5. Argumentos: `C:\ruta\a\main.py generate`

## 🆘 Soporte

**Problemas comunes en Windows:**
- Permisos: Ejecuta como Administrador si es necesario
- Antivirus: Puede bloquear FFmpeg, añade excepción
- Firewall: Permite conexiones para streaming

**Logs de error:**
Los logs se guardan en la pestaña "Logs" de la GUI o en `output\logs\`

## 🎬 Video Tutorial

*(Próximamente - video tutorial de instalación en Windows)*

---

**¿Sigues teniendo problemas?**
Abre un issue en GitHub con:
- Versión de Windows
- Salida de `python --version`
- Mensaje de error completo
- Capturas de pantalla si aplica
