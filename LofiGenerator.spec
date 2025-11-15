# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Lofi Hip Hop Generator GUI
Creates standalone executable for Windows
"""

import os

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.yaml', '.'),
        ('README_NEW.md', '.'),
        ('START_HERE.md', '.'),
        ('WINDOWS_INSTALL.md', '.'),
        ('INSTALL_FFMPEG_WINDOWS.md', '.'),
        ('lofi-hip-hop-weights-improvement-100-0.6290.hdf5', '.'),
        ('weights.hdf5', '.'),
    ],
    hiddenimports=[
        'tensorflow',
        'keras',
        'music21',
        'numpy',
        'yaml',
        'cv2',
        'tkinter',
        'PIL',
        'soundfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LofiGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version_info={
        'FileVersion': '2.1.0.0',
        'ProductVersion': '2.1.0.0',
        'FileDescription': 'Lofi Hip Hop Generator with Aurora Visualization',
        'ProductName': 'Lofi Generator',
        'CompanyName': 'Open Source',
        'LegalCopyright': 'MIT License',
    }
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LofiGenerator',
)
