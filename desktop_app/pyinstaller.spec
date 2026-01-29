# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

# Get the directory where this spec file is located
spec_dir = Path(SPECPATH)

# Assets directory path
assets_dir = spec_dir / 'app' / 'ui' / 'assets'

# Collect all assets files
datas = []
if assets_dir.exists():
    # Include all files in assets directory
    # PyInstaller datas format: (source_path, destination_path_in_exe)
    datas.append((str(assets_dir), 'app/ui/assets'))

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    name='VideoMixerConcat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Note: PyInstaller requires .ico format. Convert logo128x128.png to .ico if needed.
)
