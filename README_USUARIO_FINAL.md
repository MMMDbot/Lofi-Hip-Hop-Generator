# 🎵 Lofi Hip Hop Generator - Para Usuarios Finales

**Versión 2.1 - Interfaz Gráfica Completa**

Genera música lofi hip hop con visualizaciones de aurora boreal y haz streaming a YouTube/Twitch.

---

## 🚀 INICIO RÁPIDO (3 Pasos)

### 📥 Paso 1: Descargar

**OPCIÓN A - Instalador (Recomendado):**
1. Descarga `LofiGenerator-Setup.exe`
2. Doble click → Siguiente → Siguiente → Instalar
3. ¡Listo! Acceso directo en tu escritorio

**OPCIÓN B - Versión Portable:**
1. Descarga `LofiGenerator-Portable.zip`
2. Extrae a una carpeta
3. Ejecuta `EASY_INSTALL.bat`

---

### ⚙️ Paso 2: Configuración Inicial (Solo Primera Vez)

Si descargaste el **instalador**, salta este paso (ya está todo configurado).

Si descargaste la **versión portable**:

```
Doble click en: EASY_INSTALL.bat
```

Esto instalará automáticamente:
- ✅ Paquetes de Python necesarios
- ✅ FFmpeg (para videos y streaming)
- ✅ Configuración de directorios

**Tiempo:** 5-10 minutos

---

### 🎮 Paso 3: Abrir la Aplicación

**Instalador:**
- Doble click en el icono del escritorio "Lofi Generator"

**Portable:**
- Doble click en `LAUNCH_GUI.bat`

---

## 🖥️ USANDO LA APLICACIÓN

### Ventana Principal - 5 Pestañas:

#### 1️⃣ 🎵 GENERATE (Generar)
**Para crear música y videos**

- **Mueve los sliders:**
  - **Notes:** Cantidad de música (100-1000)
  - **Creativity:** Qué tan experimental (0.5 = seguro, 2.0 = loco)
  - **Tempo:** Velocidad en BPM (60-140)
  - **Duration:** Duración del video en segundos

- **Botones:**
  - **🎵 Music Only:** Solo crea archivo MIDI
  - **🌌 Aurora Only:** Solo video de aurora (sin música)
  - **🎬 Complete Video:** ¡TODO JUNTO! (música + aurora)

**Primera vez, prueba:**
1. Notes: 100
2. Creativity: 1.0
3. Tempo: 80
4. Click "🎵 Music Only"
5. Espera 1-2 minutos
6. ¡Tu archivo .mid estará en la carpeta `output`!

---

#### 2️⃣ 🎓 TRAIN MODEL (Entrenar)
**Para personalizar la música con tus archivos MIDI**

1. Click "📁 Open MIDI Folder"
2. Copia tus archivos `.mid` ahí (mínimo 10-20 archivos)
3. Ajusta Epochs (100 = bueno, más = mejor pero más lento)
4. Click "🎓 Start Training"
5. **Espera 2-6 horas** (sí, es largo, pero solo una vez)

**¿Dónde conseguir MIDI files?**
- Busca "free lofi midi files" en Google
- https://freemidi.org
- https://bitmidi.com

---

#### 3️⃣ 📺 STREAMING (Transmitir)
**Para hacer stream 24/7 en YouTube/Twitch**

**Primero, necesitas:**
- ✅ Video generado (usa pestaña Generate primero)
- ✅ Stream Key de YouTube/Twitch

**Obtener Stream Key:**

**YouTube:**
1. Ve a YouTube Studio
2. Click "Emisión en directo" → "Transmitir"
3. Copia la "Clave de transmisión"

**Twitch:**
1. Ve a tu Dashboard
2. Configuración → Canal
3. Copia "Clave de transmisión principal"

**En la aplicación:**
1. Selecciona plataforma (YouTube o Twitch)
2. Pega tu Stream Key
3. Click "Browse" y selecciona tu video
4. Click "▶️ Start Stream"
5. **¡Estás en vivo!**

Para detener: Click "⏹️ Stop Stream"

---

#### 4️⃣ ⚙️ SETTINGS (Configuración)
**Para personalizar colores y calidad**

- **Resolution:** 1080p es el mejor balance
- **FPS:** 30 es perfecto (60 si tienes PC potente)
- **Stars:** Activa/desactiva estrellas en aurora
- **Wave Speed:** Qué tan rápido se mueve la aurora

**Cambiar colores de aurora:**
Los colores ya están configurados, pero si quieres cambiarlos:
1. Abre `config.yaml` con Notepad
2. Busca la sección `aurora: colors:`
3. Cambia los números RGB (0-255)

---

#### 5️⃣ 📋 LOGS (Registros)
**Para ver qué está pasando**

- Todo lo que hace la aplicación aparece aquí
- Si hay errores, se muestran en rojo
- Click "🗑️ Clear Logs" para limpiar

---

## ❓ PREGUNTAS FRECUENTES

### ¿Cuánto espacio necesito?
- **Aplicación:** ~200 MB
- **Por cada video de 5 min:** ~50-100 MB
- **Recomendado:** 2 GB libres

### ¿Qué tan rápido es?
Depende de tu PC:

| Tarea | PC Lento | PC Normal | PC Rápido |
|-------|----------|-----------|-----------|
| Generar MIDI | 2 min | 1 min | 30 seg |
| Video completo | 15 min | 5 min | 2 min |
| Entrenar modelo | 8 horas | 4 horas | 2 horas |

### ¿Necesito Internet?
- **Para usar:** NO (funciona offline)
- **Para streaming:** SÍ (obvio, para transmitir)
- **Para instalar:** SÍ (para descargar dependencias)

### ¿Es gratis?
- **100% gratis**
- **Open source**
- **Sin publicidad**
- **Sin limitaciones**

### ¿Puedo monetizar los videos?
**SÍ**, la música generada es tuya. Puedes:
- ✅ Subirla a YouTube/Spotify
- ✅ Monetizarla
- ✅ Usarla comercialmente
- ✅ Hacer lo que quieras

### Error: "FFmpeg not found"
1. Cierra la aplicación
2. Ejecuta `EASY_INSTALL.bat` otra vez
3. Elige opción de instalar FFmpeg
4. **Reinicia tu PC**
5. Abre la aplicación de nuevo

### Error: "No MIDI files found"
1. Necesitas archivos MIDI para entrenar
2. Descarga gratis de Internet
3. Ponlos en carpeta `midi_songs`

### Video sin audio
- Necesitas FluidSynth instalado
- O simplemente genera el MIDI y conviértelo online:
  - https://www.zamzar.com/convert/midi-to-mp3/

---

## 💡 TIPS Y TRUCOS

### Para Mejores Resultados:

**Música:**
- Usa Creativity 0.9-1.1 para música coherente
- Usa Creativity 1.5-2.0 para experimentar
- Genera 500-800 notes para canciones de 3-5 min

**Videos:**
- 1080p @ 30 FPS es perfecto
- 4K @ 60 FPS solo si tienes PC gaming
- Reduce FPS a 24 para generar más rápido

**Streaming:**
- Genera videos de 1-2 horas
- Activa Loop para repetir automáticamente
- Usa cable ethernet, no WiFi

### Acelerar Generación:

1. **Reduce resolución** a 720p
2. **Reduce FPS** a 24
3. **Genera menos notes** (300-400)
4. **Cierra otros programas**

---

## 📁 ARCHIVOS Y CARPETAS

```
📁 LofiGenerator/
├── 🎵 midi_songs/        ← Pon tus MIDI aquí para entrenar
├── 📦 output/            ← Videos y música generados aparecen aquí
├── 📊 data/              ← Datos del modelo (no tocar)
├── 🎬 LofiGenerator.exe  ← Abre esto para usar la aplicación
└── 📖 Documentación/     ← Guías y ayuda
```

---

## 🆘 SOPORTE

### Algo no funciona?

1. **Mira los Logs** (pestaña 📋 Logs en la app)
2. **Lee el error** - normalmente dice qué falta
3. **Busca en las guías:**
   - `START_HERE.md` - Inicio rápido
   - `WINDOWS_INSTALL.md` - Instalación completa
   - `INSTALL_FFMPEG_WINDOWS.md` - Solo FFmpeg

### ¿Necesitas ayuda?

- **GitHub Issues:** https://github.com/MMMDbot/Lofi-Hip-Hop-Generator/issues
- Describe tu problema con:
  - Captura de pantalla
  - Lo que intentaste hacer
  - El error completo de los Logs

---

## 🎉 ¡COMIENZA A CREAR!

1. Abre la aplicación
2. Ve a pestaña **🎵 Generate**
3. Configura:
   - Notes: 100
   - Creativity: 1.0
   - Tempo: 80
4. Click **🎵 Generate Music Only**
5. Espera 1-2 minutos
6. **¡Tu primera canción lofi está lista!**

Encuéntrala en: `output\lofi_output_[fecha].mid`

---

**¿Preguntas? ¿Ideas? ¡Comparte tus creaciones en redes sociales!** 🌌🎵

**Hashtags:** #LofiGenerator #AIMusic #LofiHipHop #AuroraVisualization
