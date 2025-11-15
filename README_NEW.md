# 🎵 Lofi Hip Hop Generator with Aurora Borealis Streaming

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10+-orange)

Un generador de música lofi hip hop con visualizaciones de aurora boreal y capacidad de streaming en vivo a YouTube/Twitch.

## ✨ Características

- 🎹 **Generación de Música IA**: Usa LSTM para generar música lofi hip hop original
- 🌌 **Visualización Aurora Boreal**: Genera videos procedurales de auroras boreales sincronizadas con la música
- 🎥 **Conversión MIDI a Audio**: Convierte automáticamente MIDI a archivos de audio de alta calidad
- 📺 **Streaming en Vivo**: Stream directo a YouTube Live, Twitch u otros servicios RTMP
- ⚙️ **Configuración Flexible**: Sistema de configuración YAML centralizado
- 🔄 **Arquitectura Modular**: Código limpio y bien organizado
- 📊 **Logging Completo**: Monitoreo detallado de todas las operaciones

## 🆕 Novedades en v2.0

### Correcciones de Código Original
- ✅ Migrado a TensorFlow 2.x/Keras moderno
- ✅ Manejo robusto de excepciones (no más `except:` genéricos)
- ✅ Validación de datos y archivos
- ✅ Eliminación de código duplicado
- ✅ Paths configurables (no hardcoded)
- ✅ Logging profesional con módulo `logging`

### Nuevas Funcionalidades
- 🎨 Generador de visualización de aurora boreal
- 🔊 Conversión automática de MIDI a audio
- 🎬 Sincronización de audio y video
- 📡 Sistema de streaming a múltiples plataformas
- 📋 Configuración centralizada en YAML
- 🧩 Arquitectura modular y extensible

## 📋 Requisitos del Sistema

### Software Requerido

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    fluidsynth \
    fluid-soundfont-gm \
    timidity \
    ffmpeg

# macOS (con Homebrew)
brew install python3 fluidsynth timidity ffmpeg
```

### Dependencias de Python

```bash
pip install -r requirements.txt
```

Principales dependencias:
- TensorFlow >= 2.10.0
- music21 >= 8.1.0
- opencv-python >= 4.6.0
- numpy, scipy, soundfile
- PyYAML

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Lofi-Hip-Hop-Generator.git
cd Lofi-Hip-Hop-Generator
```

### 2. Instalar Dependencias

```bash
# Instalar dependencias del sistema
sudo apt-get install -y fluidsynth fluid-soundfont-gm timidity ffmpeg

# Instalar dependencias de Python
pip install -r requirements.txt
```

### 3. Configurar

Edita `config.yaml` según tus necesidades:

```yaml
# Ajusta parámetros del modelo, video, streaming, etc.
model:
  epochs: 100
  batch_size: 64

video:
  resolution: [1920, 1080]
  fps: 30

streaming:
  platform: 'youtube'
  # Añade tus credenciales de streaming
```

## 📖 Uso

### Entrenamiento del Modelo

Primero, entrena el modelo con tus archivos MIDI:

```bash
# Asegúrate de tener archivos MIDI en midi_songs/
python main.py train
```

### Generar Música y Video

```bash
# Generación básica (usa config.yaml)
python main.py generate

# Con parámetros personalizados
python main.py generate \
    --notes 500 \
    --temperature 1.2 \
    --duration 300

# Especificar archivo de salida
python main.py generate --output mi_lofi_video.mp4
```

### Streaming en Vivo

```bash
# Preparar: genera primero el video
python main.py generate --output stream_video.mp4

# Stream a YouTube
python main.py stream stream_video.mp4 \
    --platform youtube \
    --key TU_STREAM_KEY_AQUI

# Stream a Twitch
python main.py stream stream_video.mp4 \
    --platform twitch \
    --key TU_STREAM_KEY_AQUI
```

### Pipeline Completo (Generar + Stream)

```bash
python main.py full \
    --notes 500 \
    --temperature 1.0 \
    --platform youtube \
    --key TU_STREAM_KEY
```

## 🎛️ Configuración Avanzada

### config.yaml

```yaml
# Configuración del Modelo
model:
  sequence_length: 32      # Longitud de secuencia para LSTM
  lstm_units: 512          # Unidades LSTM
  dropout_rate: 0.3        # Tasa de dropout
  epochs: 100              # Épocas de entrenamiento
  batch_size: 64           # Tamaño de lote

# Generación de Música
generation:
  num_notes: 500           # Notas a generar
  temperature: 1.0         # 0.5-2.0 (menor=conservador, mayor=creativo)
  tempo: 80                # BPM

# Configuración de Video
video:
  resolution: [1920, 1080] # Resolución
  fps: 30                  # Frames por segundo
  duration: 300            # Duración en segundos
  aurora:
    colors:
      - [0, 255, 159]      # Verde
      - [0, 191, 255]      # Azul
      - [138, 43, 226]     # Púrpura
    wave_speed: 0.02       # Velocidad de ondas
    stars_enabled: true    # Mostrar estrellas
    stars_count: 200       # Número de estrellas

# Streaming
streaming:
  enabled: false
  platform: 'youtube'      # youtube, twitch, custom
  rtmp_url: null           # Para custom RTMP
  stream_key: null         # Tu clave de stream
  bitrate_video: '4500k'   # Bitrate de video
  bitrate_audio: '128k'    # Bitrate de audio
```

### Parámetros de Temperature

- **0.5-0.8**: Música más predecible y coherente
- **0.9-1.1**: Balance entre creatividad y coherencia
- **1.2-2.0**: Música más experimental y aleatoria

## 🏗️ Arquitectura del Proyecto

```
Lofi-Hip-Hop-Generator/
├── main.py                 # Script principal
├── config.py               # Gestión de configuración
├── config.yaml             # Archivo de configuración
├── model.py                # Modelo LSTM
├── data_processor.py       # Procesamiento de datos MIDI
├── music_generator.py      # Generación de música
├── audio_processor.py      # Conversión MIDI a audio
├── aurora_visualizer.py    # Generación de visualización
├── video_composer.py       # Composición de video
├── streamer.py             # Sistema de streaming
├── lstm.py                 # (Legacy) Entrenamiento
├── predict.py              # (Legacy) Predicción
├── requirements.txt        # Dependencias
├── midi_songs/             # Archivos MIDI de entrenamiento
├── data/                   # Datos procesados
├── output/                 # Archivos generados
└── waveform/               # Audio adicional (opcional)
```

## 🔧 Uso Programático

### Generar Música

```python
from music_generator import MusicGenerator

generator = MusicGenerator()
midi_file = generator.generate_music(
    num_notes=500,
    temperature=1.0,
    bpm=80
)
print(f"Generated: {midi_file}")
```

### Crear Visualización

```python
from aurora_visualizer import AuroraVisualizer

visualizer = AuroraVisualizer()
video_file = visualizer.generate_video(
    duration=300,  # 5 minutos
    output_filename='aurora.mp4'
)
```

### Pipeline Completo

```python
from main import LofiStreamGenerator

generator = LofiStreamGenerator()
results = generator.generate_complete_video(
    num_notes=500,
    temperature=1.0,
    duration=300
)

print(f"MIDI: {results['midi']}")
print(f"Audio: {results['audio']}")
print(f"Video: {results['final_video']}")
```

## 📊 Monitoreo de Streaming

Durante el streaming, puedes monitorear el estado:

```python
from streamer import LiveStreamer

streamer = LiveStreamer()
process = streamer.stream_youtube('video.mp4', 'STREAM_KEY')

# Ver estado
status = streamer.get_stream_status()
print(status)

# Detener
streamer.stop_stream()
```

## 🎨 Personalizar Visualización

Edita los colores de la aurora en `config.yaml`:

```yaml
video:
  aurora:
    colors:
      - [R, G, B]  # Color 1
      - [R, G, B]  # Color 2
      - [R, G, B]  # Color 3
```

Ejemplos de paletas de colores:
- **Clásica**: Verde ([0, 255, 159]), Azul ([0, 191, 255])
- **Violeta**: Púrpura ([138, 43, 226]), Rosa ([255, 20, 147])
- **Cálida**: Naranja ([255, 140, 0]), Rojo ([255, 69, 0])

## 🔍 Solución de Problemas

### Error: "FluidSynth not found"

```bash
sudo apt-get install fluidsynth fluid-soundfont-gm
```

### Error: "No MIDI files found"

Asegúrate de tener archivos `.mid` en el directorio `midi_songs/`.

### Error: "Weights file not found"

Primero entrena el modelo:

```bash
python main.py train
```

### Video sin Audio

Verifica que FFmpeg esté instalado:

```bash
ffmpeg -version
```

### Streaming Falla

1. Verifica tu stream key
2. Comprueba tu conexión a internet
3. Revisa los logs en tiempo real

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto mantiene la licencia original. Ver `LICENSE` para más detalles.

## 🙏 Créditos

- **Código Original**: [Sigurður Skúli](https://github.com/Skuldur/Classical-Piano-Composer)
- **Mejoras y Streaming**: Esta versión extendida
- **Música**: Generada por IA usando LSTM
- **Visualizaciones**: Algoritmos procedurales de aurora boreal

## 📚 Recursos Adicionales

- [TensorFlow Documentation](https://www.tensorflow.org/)
- [music21 Documentation](https://web.mit.edu/music21/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [YouTube Live Streaming API](https://developers.google.com/youtube/v3/live)

## 🎯 Roadmap

- [ ] Soporte para más instrumentos
- [ ] Generación de beats/drums
- [ ] Interfaz web
- [ ] Más estilos de visualización
- [ ] Integración con Spotify
- [ ] Generación automática de playlist
- [ ] Docker support
- [ ] Cloud deployment

## 📞 Soporte

¿Problemas? Abre un issue en GitHub o contacta al mantenedor del proyecto.

---

**Hecho con ❤️ para la comunidad lofi hip hop**
