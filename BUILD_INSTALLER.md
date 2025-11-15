# 📦 Crear Instalador para Windows

Guía completa para crear un instalador .exe profesional del Lofi Hip Hop Generator.

---

## 🎯 Dos Opciones de Distribución

### Opción A: Instalador Completo (Recomendado)
- ✅ Un solo .exe que instala todo
- ✅ Descarga FFmpeg automáticamente
- ✅ Crea accesos directos
- ✅ Registro en Windows
- ⏱️ Tiempo: 30-60 minutos

### Opción B: Ejecutable Portable
- ✅ Solo empaqueta la aplicación
- ⚠️ Usuario debe instalar dependencias
- ⚠️ No crea accesos directos
- ⏱️ Tiempo: 10-15 minutos

---

## 📋 OPCIÓN A: Instalador Completo (NSIS)

### Requisitos Previos

1. **Python 3.8+** instalado
2. **NSIS (Nullsoft Scriptable Install System)**
   - Descarga: https://nsis.sourceforge.io/Download
   - Instala la versión completa

3. **Plugins NSIS adicionales:**
   - **Inetc** (para descargar archivos)
     ```
     https://nsis.sourceforge.io/Inetc_plug-in
     ```
   - **nsisunz** (para extraer ZIP)
     ```
     https://nsis.sourceforge.io/NsisUnz_plug-in
     ```
   - **EnVar** (para modificar PATH)
     ```
     https://nsis.sourceforge.io/EnVar_plug-in
     ```

   **Instalación de plugins:**
   - Descarga cada plugin
   - Copia archivos .dll a: `C:\Program Files (x86)\NSIS\Plugins\x86-unicode\`

### Paso 1: Preparar el Proyecto

```cmd
cd C:\ruta\a\Lofi-Hip-Hop-Generator

# Crear entorno de build
python -m venv build_env
build_env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install pyinstaller
```

### Paso 2: Crear el Ejecutable

```cmd
# Ejecutar el script de build
build_exe.bat
```

Esto creará:
- `dist\LofiGenerator\` - Carpeta con todos los archivos
- `dist\LofiGenerator\LofiGenerator.exe` - Ejecutable principal

**Verificar que funciona:**
```cmd
cd dist\LofiGenerator
LofiGenerator.exe
```

### Paso 3: Crear el Instalador

```cmd
# Volver a la raíz del proyecto
cd ..\..

# Compilar el instalador NSIS
makensis installer.nsi
```

**Salida:**
```
Output: "LofiGenerator-Setup.exe"
Install: 3 pages (448 bytes), 1 section (1 required) (104 bytes), 125 instructions (3500 bytes)
Uninstall: 2 pages (320 bytes), 1 section (40 bytes), 37 instructions (1036 bytes)
```

**¡Listo!** Ahora tienes `LofiGenerator-Setup.exe`

### Paso 4: Probar el Instalador

1. **Ejecuta** `LofiGenerator-Setup.exe`
2. **Sigue el asistente:**
   - Welcome → Next
   - Elige carpeta de instalación
   - Instala
3. **Verifica:**
   - Acceso directo en Escritorio
   - Entrada en Menú Inicio
   - Programa en Panel de Control

---

## 📦 OPCIÓN B: Ejecutable Portable

Más simple, pero sin instalador.

### Paso 1: Crear Ejecutable

```cmd
# Ejecutar build
build_exe.bat
```

### Paso 2: Empaquetar

```cmd
# Crear ZIP para distribución
powershell Compress-Archive -Path dist\LofiGenerator\* -DestinationPath LofiGenerator-Portable.zip
```

### Paso 3: Crear README para el ZIP

Crea un archivo `PORTABLE_README.txt`:

```
LOFI HIP HOP GENERATOR - PORTABLE VERSION

QUICK START:
1. Extract this ZIP to any folder
2. Run LofiGenerator.exe
3. First time will show installation instructions

REQUIREMENTS:
- Windows 10/11
- FFmpeg (install instructions shown in app)
- FluidSynth (optional, for audio)

For full installation instructions, see WINDOWS_INSTALL.md

Enjoy creating lofi music!
```

---

## 🔧 Personalización

### Cambiar Icono

1. **Crear o descargar icono** (.ico, 256x256)
2. **Guardar como** `icon.ico` en la raíz del proyecto
3. **Modificar** `LofiGenerator.spec`:
   ```python
   icon='icon.ico'
   ```

### Cambiar Nombre

En `installer.nsi`:
```nsi
Name "Tu Nombre de Aplicación"
OutFile "TuApp-Setup.exe"
```

En `LofiGenerator.spec`:
```python
name='TuNombreApp',
```

### Agregar Licencia

Crea archivo `LICENSE` en la raíz:
```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge...
```

---

## 🚀 Distribución

### Subir a GitHub Releases

```cmd
# Crear tag
git tag v2.1.0
git push origin v2.1.0

# Subir en GitHub:
# 1. Ve a Releases
# 2. Draft new release
# 3. Sube LofiGenerator-Setup.exe
# 4. Publica
```

### Sitio Web de Descarga

Puedes hospedar en:
- **GitHub Pages** (gratis)
- **Google Drive** (link de descarga directa)
- **MediaFire** / **MEGA**

---

## 📊 Tamaños Esperados

| Componente | Tamaño |
|------------|--------|
| Ejecutable (.exe) | ~150-200 MB |
| Instalador (setup.exe) | ~180-250 MB |
| ZIP Portable | ~150-200 MB |

**Grande debido a:**
- TensorFlow/Keras
- Modelo de pesos (~65 MB)
- Dependencias de Python

---

## 🔍 Solución de Problemas

### Error: "ImportError: DLL load failed"

**Causa:** Faltan DLLs de Visual C++

**Solución:**
Incluir en el spec:
```python
binaries=[
    ('C:\\Windows\\System32\\vcruntime140.dll', '.'),
],
```

### Error: "Failed to execute script"

**Causa:** Falta archivo de datos

**Solución:**
Agregar a `datas` en el spec:
```python
datas=[
    ('archivo.ext', '.'),
],
```

### Instalador NSIS no compila

**Causa:** Plugins faltantes

**Solución:**
1. Verifica plugins en: `C:\Program Files (x86)\NSIS\Plugins\`
2. Reinstala NSIS
3. Descarga plugins manualmente

### Ejecutable muy grande

**Optimización:**
```python
# En el spec
excludes=[
    'matplotlib',  # Si no se usa
    'scipy',       # Si no se usa
],
upx=True,  # Comprimir
```

---

## ✅ Checklist de Release

Antes de publicar:

- [ ] Ejecutable funciona en PC limpio (sin Python)
- [ ] Instalador crea accesos directos
- [ ] Desinstalador funciona correctamente
- [ ] Instrucciones de FFmpeg claras
- [ ] README incluido
- [ ] Versión actualizada en todos los archivos
- [ ] Probado en Windows 10 y 11
- [ ] Sin errores en antivirus (VirusTotal)

---

## 🎨 Mejoras Futuras

### Auto-update

Agregar verificación de versiones:
```python
import requests

def check_for_updates():
    response = requests.get('https://api.github.com/repos/user/repo/releases/latest')
    latest = response.json()['tag_name']
    if latest > current_version:
        show_update_dialog()
```

### Instalador Multi-idioma

En `installer.nsi`:
```nsi
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "French"
```

### Firma Digital

Para evitar advertencias de SmartScreen:
1. Compra certificado de firma de código
2. Firma con `signtool`:
```cmd
signtool sign /f cert.pfx /p password /t http://timestamp.digicert.com LofiGenerator-Setup.exe
```

---

## 📚 Recursos Adicionales

- **PyInstaller Docs:** https://pyinstaller.org/
- **NSIS Docs:** https://nsis.sourceforge.io/Docs/
- **GitHub Actions para builds automáticos:** `.github/workflows/build.yml`

---

## 🆘 Ayuda

**¿Problemas?**
1. Revisa logs de PyInstaller: `build\LofiGenerator\warn-LofiGenerator.txt`
2. Prueba en máquina virtual limpia
3. Abre issue en GitHub con:
   - Salida completa de error
   - Versión de Python
   - Versión de PyInstaller
   - Sistema operativo

---

**¡Listo para crear tu instalador profesional!** 🚀
