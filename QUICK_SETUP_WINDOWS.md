# ⚡ CONFIGURACIÓN RÁPIDA - WINDOWS

## 🎯 Instalación en 10 Minutos

Sigue estos pasos **EN ORDEN** para tener todo funcionando.

---

## ✅ CHECKLIST DE INSTALACIÓN

### Paso 1: Python ✅
```cmd
python --version
```
**¿Sale la versión?** → ✅ Tienes Python
**¿Error?** → Instala Python 3.8+ desde https://www.python.org/downloads/
- ⚠️ **MARCA "Add Python to PATH"** durante instalación

---

### Paso 2: FFmpeg ⚡ **REQUERIDO**
```cmd
ffmpeg -version
```
**¿Sale la versión?** → ✅ Tienes FFmpeg
**¿Error?** → Instala FFmpeg:

**MÉTODO RÁPIDO (2 minutos):**
```cmd
winget install ffmpeg
```

**¿No funciona winget?**
→ Sigue: [INSTALL_FFMPEG_WINDOWS.md](INSTALL_FFMPEG_WINDOWS.md)

---

### Paso 3: Proyecto
```cmd
# Descarga el proyecto
git clone https://github.com/tu-usuario/Lofi-Hip-Hop-Generator.git
cd Lofi-Hip-Hop-Generator

# Ejecuta instalador
install.bat
```

**Espera a que termine** (descarga paquetes de Python)

---

### Paso 4: FluidSynth (Opcional - para mejor audio)
```cmd
fluidsynth --version
```
**¿Sale la versión?** → ✅ Tienes FluidSynth
**¿Error?** → Es opcional, pero recomendado

**Para instalarlo:**
→ Sigue: Busca "FluidSynth Windows" en Google

**¿Para qué sirve?**
- ✅ Con FluidSynth: Videos con audio de alta calidad
- ⚠️ Sin FluidSynth: Solo MIDI (puedes convertir online después)

---

## 🚀 LANZAR LA GUI

```cmd
# 1. Ve a la carpeta del proyecto
cd C:\ruta\a\Lofi-Hip-Hop-Generator

# 2. Activa entorno virtual
venv\Scripts\activate

# 3. Lanza GUI
python gui.py
```

**¿Abre la ventana?** → ✅ ¡TODO LISTO!

---

## 📊 ¿QUÉ PUEDES HACER?

### ✅ CON FFmpeg + Python (MÍNIMO REQUERIDO):
- ✅ Generar MIDI
- ✅ Generar videos de aurora (sin audio)
- ✅ Entrenar modelo
- ❌ Streaming (necesitas FFmpeg)
- ❌ Videos con audio (necesitas FluidSynth)

### ✅ CON FFmpeg + FluidSynth (COMPLETO):
- ✅ Generar MIDI
- ✅ Generar videos con AUDIO
- ✅ Entrenar modelo
- ✅ Streaming a YouTube/Twitch
- ✅ Todo funciona al 100%

---

## 🎬 PRIMER VIDEO (TEST RÁPIDO)

1. **Abre GUI:**
```cmd
python gui.py
```

2. **Pestaña 🎵 Generate**
   - Notes: **50** (prueba rápida)
   - Creativity: **1.0**
   - Tempo: **80**

3. **Click en uno de estos botones:**

**Solo MIDI (siempre funciona):**
```
🎵 Generate Music Only
```
→ Crea archivo `.mid` en carpeta `output\`

**Video de aurora SIN audio:**
```
🌌 Generate Aurora Only
```
→ Crea video mudo en `output\`

**Video completo CON audio:**
```
🎬 Generate Complete Video
```
→ ⚠️ Necesitas FluidSynth instalado

4. **Espera 2-5 minutos**

5. **Revisa carpeta `output\`**

**¿Encontraste tu archivo?** → ✅ ¡Funciona!

---

## 🔴 STREAMING A YOUTUBE

### Requisitos:
- ✅ FFmpeg instalado
- ✅ Video generado
- ✅ Stream Key de YouTube

### Pasos:

**1. Obtener Stream Key:**
- Ve a YouTube Studio
- Click **Emisión en directo** → **Transmitir**
- Copia la **Clave de transmisión**

**2. En la GUI:**
- Pestaña **📺 Streaming**
- Platform: **YouTube**
- Stream Key: **Pega tu clave**
- Video file: **Selecciona tu video**
- Click **▶️ Start Stream**

**¿Ves "Stream started successfully"?** → ✅ ¡Estás en vivo!

---

## ❌ ERRORES COMUNES

### Error: "python no se reconoce"
**Solución:**
1. Reinstala Python
2. **MARCA** "Add Python to PATH"
3. Reinicia PC

### Error: "ffmpeg no se reconoce"
**Solución:**
1. Instala FFmpeg: `winget install ffmpeg`
2. Cierra TODAS las ventanas de CMD
3. Abre NUEVA ventana
4. Prueba: `ffmpeg -version`

### Error: "TiMidity conversion failed"
**Explicación:** No tienes FluidSynth
**Solución:**
- **Opción A:** Instala FluidSynth (ver guía)
- **Opción B:** Genera solo MIDI y conviértelo online

### Error: "Streaming failed: WinError 2"
**Explicación:** No tienes FFmpeg
**Solución:** Instala FFmpeg (ver arriba)

---

## 🆘 MATRIZ DE TROUBLESHOOTING

| Síntoma | Causa | Solución |
|---------|-------|----------|
| "python no se reconoce" | Python no en PATH | Reinstala marcando PATH |
| "ffmpeg no se reconoce" | FFmpeg no instalado | `winget install ffmpeg` |
| Video sin audio | Sin FluidSynth | Instala FluidSynth (opcional) |
| Streaming falla | Sin FFmpeg | Instala FFmpeg (obligatorio) |
| GUI no abre | Falta dependencias | `pip install -r requirements.txt` |

---

## 📚 GUÍAS DETALLADAS

Para más información:

- **FFmpeg:** [INSTALL_FFMPEG_WINDOWS.md](INSTALL_FFMPEG_WINDOWS.md)
- **FluidSynth:** Busca online "Install FluidSynth Windows"
- **Todo completo:** [WINDOWS_INSTALL.md](WINDOWS_INSTALL.md)
- **Inicio rápido:** [START_HERE.md](START_HERE.md)

---

## ⏱️ TIEMPO ESTIMADO

| Tarea | Sin experiencia | Con experiencia |
|-------|----------------|-----------------|
| Instalar Python | 5 min | 2 min |
| Instalar FFmpeg | 5 min | 1 min |
| Instalar proyecto | 3 min | 1 min |
| Generar primer MIDI | 2 min | 1 min |
| Generar primer video | 5-10 min | 3-5 min |
| **TOTAL** | **20-25 min** | **8-10 min** |

---

## 🎉 CHECKLIST FINAL

Antes de empezar a crear:

- [ ] `python --version` funciona
- [ ] `ffmpeg -version` funciona
- [ ] `install.bat` ejecutado
- [ ] `python gui.py` abre la ventana
- [ ] Primer MIDI generado exitosamente
- [ ] Primer video (con o sin audio) generado

**¿Todos ✅?** → ¡Estás listo para crear música lofi! 🎵

---

## 💡 PRÓXIMOS PASOS

1. **Añade MIDI files** para entrenar
2. **Personaliza colores** de aurora
3. **Genera videos** para YouTube
4. **Haz streaming** 24/7

**¡Disfruta creando!** 🌌🎵
