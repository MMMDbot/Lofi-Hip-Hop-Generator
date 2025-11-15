# 🚀 INICIO RÁPIDO

## 📌 ¿Nuevo? ¡Empieza aquí!

Este documento te guiará paso a paso para usar el generador.

---

## 🪟 USUARIOS DE WINDOWS - OPCIÓN MÁS FÁCIL

### Paso 1: Instalar Python
1. Ve a https://www.python.org/downloads/
2. Descarga Python 3.8 o superior
3. **IMPORTANTE**: Durante instalación, marca ✅ "Add Python to PATH"
4. Instala

### Paso 2: Instalar FFmpeg
```cmd
winget install ffmpeg
```
*(O sigue las instrucciones manuales en WINDOWS_INSTALL.md)*

### Paso 3: Instalar el Proyecto
1. Descarga este repositorio (botón verde "Code" → Download ZIP)
2. Extrae a una carpeta (ej: `C:\LofiGenerator`)
3. Abre **Command Prompt** en esa carpeta
4. Ejecuta:
```cmd
install.bat
```

### Paso 4: Lanzar la GUI
```cmd
venv\Scripts\activate
python gui.py
```

**¡LISTO! Ya puedes usar la interfaz gráfica** 🎉

---

## 🐧 USUARIOS DE LINUX / MAC

### Instalación Rápida
```bash
# Clonar proyecto
git clone https://github.com/tu-usuario/Lofi-Hip-Hop-Generator.git
cd Lofi-Hip-Hop-Generator

# Ejecutar instalador
chmod +x install.sh
./install.sh

# Lanzar GUI
source venv/bin/activate
python gui.py
```

---

## 🖥️ USANDO LA INTERFAZ GRÁFICA (GUI)

### Ventana Principal

```
┌─────────────────────────────────────────────────────┐
│  Lofi Hip Hop Generator 🎵                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [🎵 Generate] [🎓 Train] [📺 Stream] [⚙️ Settings] [📋 Logs] │
│                                                     │
│  ┌───────────────────────────────────────────┐    │
│  │  🎵 GENERATE TAB                          │    │
│  │                                           │    │
│  │  Number of Notes:     [====●====]  500    │    │
│  │  Creativity:          [===●=====]  1.0    │    │
│  │  Tempo (BPM):         [====●====]  80     │    │
│  │  Duration (sec):      [300________]       │    │
│  │  Output:              [lofi_output.mp4__] │    │
│  │                                           │    │
│  │  [🎵 Music Only] [🌌 Aurora] [🎬 Complete] │    │
│  └───────────────────────────────────────────┘    │
│                                                     │
│  Status: Ready                                     │
└─────────────────────────────────────────────────────┘
```

### Pestañas Disponibles:

#### 1️⃣ **🎵 GENERATE** (Generar)
- **Mueve los sliders** para ajustar:
  - Número de notas (100-1000)
  - Creatividad (0.5 = conservador, 2.0 = experimental)
  - Tempo en BPM (60-140)
  - Duración del video
- **Botones**:
  - 🎵 Music Only: Solo genera MIDI
  - 🌌 Aurora Only: Solo video de aurora
  - 🎬 Complete: ¡Todo junto!

#### 2️⃣ **🎓 TRAIN MODEL** (Entrenar)
1. Haz clic en "📁 Open MIDI Folder"
2. Copia tus archivos .mid a esa carpeta
3. Ajusta Epochs y Batch Size si quieres
4. Haz clic en "🎓 Start Training"
5. **Espera** (puede tomar horas)

#### 3️⃣ **📺 STREAMING**
1. Genera un video primero (pestaña Generate)
2. Selecciona plataforma (YouTube/Twitch)
3. **Obtén tu Stream Key**:
   - YouTube: Studio → Emisión → Clave
   - Twitch: Dashboard → Configuración → Clave de transmisión
4. Pega la clave en "Stream Key"
5. Selecciona el video
6. ¡Haz clic en "▶️ Start Stream"!

#### 4️⃣ **⚙️ SETTINGS** (Configuración)
- Cambia resolución (1080p, 4K, etc.)
- Ajusta FPS (24, 30, 60)
- Personaliza colores de aurora
- Activa/desactiva estrellas
- Haz clic en "💾 Save Configuration"

#### 5️⃣ **📋 LOGS**
- Ve todo lo que está pasando en tiempo real
- Mensajes de error aparecen aquí
- Haz clic en "🗑️ Clear Logs" para limpiar

---

## 🎯 GUÍA RÁPIDA: TU PRIMER VIDEO

### Opción A: Usar Video de Prueba (Más Rápido)

Si NO quieres entrenar (se usa modelo pre-entrenado):

```cmd
# Windows
venv\Scripts\activate
python gui.py
```

1. Abre GUI
2. Ve a pestaña **🎵 Generate**
3. Ajusta sliders a tu gusto
4. Haz clic en **🎬 Generate Complete Video**
5. **Espera** 5-15 minutos
6. ¡Listo! Tu video estará en la carpeta `output\`

### Opción B: Entrenar Tu Propio Modelo

Para crear música MÁS personalizada:

1. **Consigue archivos MIDI** (busca "free lofi midi" en Google)
2. Abre GUI → pestaña **🎓 Train Model**
3. Haz clic en "📁 Open MIDI Folder"
4. **Copia** tus archivos .mid ahí (mínimo 10-20 archivos)
5. Haz clic en "🎓 Start Training"
6. **Espera 2-6 horas** (según tu PC)
7. Luego usa pestaña **🎵 Generate**

---

## ❓ PREGUNTAS FRECUENTES

### ¿Cuánto tarda en generar?
- **Solo música (MIDI)**: 1-2 minutos
- **Video completo**: 5-15 minutos
- **Entrenamiento**: 2-6 horas (solo una vez)

### ¿Necesito entrenar el modelo?
**NO** si usas los pesos pre-entrenados incluidos.
**SÍ** si quieres música personalizada basada en tus MIDIs.

### ¿Funciona sin GPU?
**SÍ**, pero será más lento. GPU acelera 5-10x.

### ¿Dónde están mis archivos generados?
En la carpeta `output\` del proyecto.

### ¿Qué significa "Temperature"?
- **0.5-0.8**: Música predecible y segura
- **0.9-1.1**: Balance (recomendado)
- **1.2-2.0**: Música experimental y creativa

### Error: "Weights file not found"
Necesitas entrenar primero o descargar pesos pre-entrenados.

### Error: "FFmpeg not found"
```cmd
winget install ffmpeg
```

### ¿Cómo streaming 24/7?
1. Genera un video largo (1-2 horas)
2. Activa "Loop" en streaming
3. El video se repetirá automáticamente

---

## 🆘 AYUDA Y SOPORTE

### Documentación Completa
- **README_NEW.md**: Guía completa del proyecto
- **WINDOWS_INSTALL.md**: Instalación detallada para Windows
- **config.yaml**: Todos los parámetros configurables

### ¿Problemas?
1. Revisa pestaña **📋 Logs** en la GUI
2. Lee **WINDOWS_INSTALL.md** sección "Solución de Problemas"
3. Abre un Issue en GitHub con:
   - Captura de pantalla del error
   - Salida de `python --version`
   - Sistema operativo

### Comunidad
- GitHub Issues: Para reportar bugs
- GitHub Discussions: Para preguntas generales

---

## 🎨 TIPS Y TRUCOS

### Mejores Resultados de Música
- Entrena con 20+ archivos MIDI similares en estilo
- Usa temperature 0.9-1.1 para balance
- Genera 500-800 notas para videos de 5 minutos

### Mejores Videos
- 1080p @ 30fps es el sweet spot
- 4K @ 60fps si tienes GPU potente
- Personaliza colores de aurora en Settings

### Streaming Óptimo
- Bitrate de video: 4500k para 1080p
- Bitrate de audio: 128k es suficiente
- Usa cable ethernet (no WiFi) para estabilidad

### Acelerar Generación
- Reduce FPS a 24
- Reduce resolución a 720p
- Genera menos notas (300-400)
- Habilita GPU (NVIDIA CUDA)

---

## 🎉 ¡DIVIÉRTETE!

Experimenta con diferentes parámetros. No hay forma "correcta" - es arte generativo.

**Comparte tus creaciones:**
- YouTube: Crea tu propio canal lofi 24/7
- SoundCloud: Comparte tus tracks
- Instagram: Clips cortos con auroras

---

**¿Listo para empezar?**

```cmd
# Windows
python gui.py

# Linux/Mac
python gui.py
```

🎵 ¡Que disfrutes creando música lofi! 🌌
