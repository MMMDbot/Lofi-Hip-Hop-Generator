# 🎬 GUÍA PASO A PASO: Instalar FFmpeg en Windows

## ¿Qué es FFmpeg?

FFmpeg es una herramienta que convierte y procesa video/audio. **Es necesario para:**
- ✅ Generar videos completos (combinar audio + aurora)
- ✅ Hacer streaming a YouTube/Twitch
- ✅ Optimizar videos para web

---

## 🚀 MÉTODO 1: Winget (MÁS FÁCIL - Recomendado)

### Requisitos
- Windows 10 (versión 1809 o superior) o Windows 11
- Winget instalado (viene por defecto en Windows 11)

### Pasos

**1. Abrir PowerShell o Command Prompt**
- Presiona `Windows + R`
- Escribe: `cmd`
- Presiona Enter

**2. Instalar FFmpeg**
```cmd
winget install ffmpeg
```

**3. Esperar a que termine**
Verás algo como:
```
Successfully installed
```

**4. Verificar instalación**
Cierra y abre una **NUEVA** ventana de CMD, luego:
```cmd
ffmpeg -version
```

**Si funciona, verás:**
```
ffmpeg version 2024-11-07-git-...
built with gcc ...
configuration: --enable-gpl ...
```

**¡LISTO!** FFmpeg está instalado. Pasa al [PASO 5: Probar](#-paso-5-probar-que-todo-funciona).

---

## 🛠️ MÉTODO 2: Instalación Manual (Si Winget no funciona)

### PASO 1: Descargar FFmpeg

**1.1 Ir a la página oficial**
- Abre tu navegador
- Ve a: https://www.gyan.dev/ffmpeg/builds/

**1.2 Descargar el archivo correcto**
Busca y descarga: **"ffmpeg-release-essentials.zip"**

```
✅ ffmpeg-release-essentials.zip  (Este)
❌ ffmpeg-release-full.zip         (Muy grande, no necesario)
```

Click en el enlace para descargar (~70-90 MB)

---

### PASO 2: Extraer FFmpeg

**2.1 Crear carpeta de destino**
1. Abre el **Explorador de archivos**
2. Ve a **Disco C:** (`C:\`)
3. Click derecho → **Nuevo** → **Carpeta**
4. Nómbrala: `ffmpeg`

**2.2 Extraer archivos**
1. Ve a tu carpeta de **Descargas**
2. Encuentra `ffmpeg-release-essentials.zip`
3. **Click derecho** → **Extraer todo...**
4. Cambia la ubicación a: `C:\ffmpeg`
5. Click **Extraer**

**2.3 Verificar estructura**
Deberías tener:
```
C:\ffmpeg\
    └── ffmpeg-7.1-essentials_build\    (o similar)
        ├── bin\
        │   ├── ffmpeg.exe   ← ESTE ES EL IMPORTANTE
        │   ├── ffplay.exe
        │   └── ffprobe.exe
        ├── doc\
        └── presets\
```

**2.4 Simplificar ruta (Opcional pero recomendado)**
1. Entra a `C:\ffmpeg\ffmpeg-7.1-essentials_build\`
2. Copia la carpeta `bin\`
3. Pégala directamente en `C:\ffmpeg\`
4. Ahora deberías tener: `C:\ffmpeg\bin\ffmpeg.exe`

---

### PASO 3: Añadir FFmpeg al PATH

**3.1 Abrir Variables de Entorno**

**Windows 11:**
1. Click derecho en **Inicio**
2. Click en **Sistema**
3. Scroll abajo → **Configuración avanzada del sistema**
4. Click **Variables de entorno...**

**Windows 10:**
1. Click derecho en **Este equipo**
2. **Propiedades**
3. **Configuración avanzada del sistema**
4. **Variables de entorno...**

**Atajo rápido (cualquier Windows):**
1. Presiona `Windows + R`
2. Escribe: `sysdm.cpl`
3. Enter
4. Pestaña **Opciones avanzadas**
5. Click **Variables de entorno...**

**3.2 Editar PATH**

En la ventana **Variables de entorno**:

1. Sección **"Variables del sistema"** (abajo):
   - Busca y selecciona **Path**
   - Click **Editar...**

2. En la nueva ventana:
   - Click **Nuevo**
   - Escribe: `C:\ffmpeg\bin`
   - Presiona **Enter**

3. Click **Aceptar** (en las 3 ventanas)

**3.3 Verificar PATH**

**IMPORTANTE:** Cierra TODAS las ventanas de CMD/PowerShell abiertas.

1. Abre una **NUEVA** ventana de Command Prompt:
   - `Windows + R` → `cmd` → Enter

2. Escribe:
```cmd
ffmpeg -version
```

3. Presiona Enter

**Si funciona:**
```
ffmpeg version 7.1-essentials_build
Copyright (c) 2000-2024 the FFmpeg developers
...
```

**Si NO funciona:**
```
'ffmpeg' no se reconoce como un comando interno o externo...
```
→ Repite el PASO 3, asegúrate de:
- Cerrar TODAS las ventanas de CMD
- Verificar que `C:\ffmpeg\bin\ffmpeg.exe` existe
- Reiniciar tu PC si es necesario

---

## ✅ PASO 5: Probar que Todo Funciona

### Test 1: Verificar comando básico
```cmd
ffmpeg -version
```
Debe mostrar la versión.

### Test 2: Probar conversión simple
```cmd
# Crear archivo de prueba (10 segundos de video negro)
ffmpeg -f lavfi -i color=black:s=640x480:d=10 -f mp4 test.mp4
```

Si crea `test.mp4` → ✅ **¡FFmpeg funciona!**

### Test 3: Probar con la GUI

1. Abre la GUI:
```cmd
cd C:\Users\TU_USUARIO\Documents\Lofi-Hip-Hop-Generator
venv\Scripts\activate
python gui.py
```

2. Intenta generar video completo:
   - Pestaña **🎵 Generate**
   - Notes: 50 (prueba rápida)
   - Click **🎬 Generate Complete Video**

3. Revisa los **Logs** (pestaña 📋):
   - Si NO hay error de FFmpeg → ✅ Funciona

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "ffmpeg no se reconoce"

**Solución 1: Verificar PATH**
```cmd
echo %PATH%
```
Debes ver `C:\ffmpeg\bin` en alguna parte de la lista.

**Solución 2: Verificar que ffmpeg.exe existe**
1. Abre explorador
2. Ve a `C:\ffmpeg\bin\`
3. Busca `ffmpeg.exe`
4. Si no está → Repite PASO 2

**Solución 3: Reiniciar PC**
A veces Windows necesita reiniciar para que PATH se actualice.

**Solución 4: Usar ruta completa**
Como solución temporal:
```cmd
C:\ffmpeg\bin\ffmpeg -version
```

### ❌ Error: "missing vcruntime140.dll"

FFmpeg necesita Visual C++ Redistributable:

1. Descarga e instala:
https://aka.ms/vs/17/release/vc_redist.x64.exe

2. Reinicia
3. Prueba ffmpeg otra vez

### ❌ Error: "Access denied" o "Permission denied"

**Solución:**
1. Click derecho en **Command Prompt**
2. **Ejecutar como administrador**
3. Repite la instalación

### ❌ Winget no funciona

**Error común:** `winget: command not found`

**Solución:**
1. Actualiza Windows a la última versión
2. Instala App Installer desde Microsoft Store:
   https://apps.microsoft.com/store/detail/app-installer/9NBLGGH4NNS1

3. O usa MÉTODO 2 (instalación manual)

---

## 🎯 VERIFICACIÓN FINAL

Antes de continuar, verifica:

- [ ] FFmpeg descargado
- [ ] Extraído a `C:\ffmpeg\bin\`
- [ ] Añadido a PATH
- [ ] CMD nueva abierta
- [ ] `ffmpeg -version` funciona
- [ ] Test de video creado

**Si todos ✅ → ¡Listo para streaming!**

---

## 💡 COMANDOS ÚTILES DE FFMPEG

### Ver información de video
```cmd
ffmpeg -i video.mp4
```

### Convertir MIDI a MP3 (si tienes soundfont)
```cmd
ffmpeg -i input.mid -soundfont soundfont.sf2 output.mp3
```

### Combinar audio + video manualmente
```cmd
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4
```

### Crear loop de video
```cmd
ffmpeg -stream_loop 10 -i input.mp4 -c copy output.mp4
```

---

## 🆘 NECESITAS MÁS AYUDA?

### Documentación oficial
- FFmpeg Windows: https://www.ffmpeg.org/download.html#build-windows
- Gyan.dev builds: https://www.gyan.dev/ffmpeg/builds/

### Verificar instalación
```cmd
where ffmpeg
```
Debe mostrar: `C:\ffmpeg\bin\ffmpeg.exe`

### Video tutoriales
Busca en YouTube: "Install FFmpeg Windows 10" o "FFmpeg installation tutorial"

---

## 📊 COMPARACIÓN DE MÉTODOS

| Aspecto | Winget | Manual |
|---------|--------|--------|
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Velocidad** | 2 minutos | 10 minutos |
| **PATH automático** | ✅ Sí | ❌ No (manual) |
| **Actualizaciones** | ✅ Fácil | ⚠️ Manual |
| **Requisitos** | Windows 10+ | Cualquier Windows |

---

## 🎉 PRÓXIMOS PASOS

Una vez FFmpeg instalado:

### Para Streaming:
```cmd
python gui.py
```
1. Pestaña **📺 Streaming**
2. Selecciona plataforma
3. Ingresa Stream Key
4. Selecciona video
5. **▶️ Start Stream**

### Para Generar Videos:
```cmd
python gui.py
```
1. Pestaña **🎵 Generate**
2. Configura parámetros
3. **🎬 Generate Complete Video**

---

## ✅ CHECKLIST FINAL

- [ ] FFmpeg instalado
- [ ] `ffmpeg -version` funciona
- [ ] PATH configurado
- [ ] Test de video exitoso
- [ ] GUI abre sin errores
- [ ] Listo para generar/streamear

---

**¿Todo funcionó?** 🎉

¡Ahora puedes generar videos completos y hacer streaming a YouTube/Twitch!

**¿Problemas?** Abre un issue en GitHub con:
- Salida de `ffmpeg -version`
- Salida de `echo %PATH%`
- Captura de pantalla del error
