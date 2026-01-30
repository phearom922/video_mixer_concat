# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import logging
import shutil
from pathlib import Path

# Setup logging for spec file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

block_cipher = None

# Get the directory where this spec file is located
spec_dir = Path(SPECPATH)
dist_dir = spec_dir / 'dist'
exe_path = dist_dir / 'VideoMixerConcat.exe'

# Try to remove old executable if it exists (to avoid PermissionError)
if exe_path.exists():
    try:
        # Try to remove the file
        os.chmod(exe_path, 0o777)  # Make it writable
        exe_path.unlink()
        logger.info(f"Removed old executable: {exe_path}")
    except PermissionError:
        logger.warning(
            f"Cannot remove {exe_path}. The file may be in use.\n"
            "Please close VideoMixerConcat.exe if it's running and try again."
        )
        # Don't fail, just warn - PyInstaller will try to overwrite it
    except Exception as e:
        logger.warning(f"Error removing old executable: {e}")

# Get the directory where this spec file is located
spec_dir = Path(SPECPATH)

# Assets directory path
assets_dir = spec_dir / 'app' / 'ui' / 'assets'

# Icon file path
icon_file = spec_dir / 'icon.ico'

# FFmpeg directory path - check both possible locations
ffmpeg_dir = spec_dir / 'ffmpeg'
ffmpeg_dir_alt = spec_dir / 'app' / 'ffmpeg'  # Alternative location

# Collect all assets files
datas = []
if assets_dir.exists():
    # Include all files in assets directory
    # PyInstaller datas format: (source_path, destination_path_in_exe)
    datas.append((str(assets_dir), 'app/ui/assets'))

# Include FFmpeg if it exists (check both locations)
ffmpeg_found = False
if ffmpeg_dir.exists() and (ffmpeg_dir / 'bin' / 'ffmpeg.exe').exists():
    # Include FFmpeg binaries from desktop_app/ffmpeg/
    datas.append((str(ffmpeg_dir), 'ffmpeg'))
    logger.info(f"Including FFmpeg from: {ffmpeg_dir}")
    ffmpeg_found = True
elif ffmpeg_dir_alt.exists() and (ffmpeg_dir_alt / 'bin' / 'ffmpeg.exe').exists():
    # Include FFmpeg binaries from desktop_app/app/ffmpeg/
    datas.append((str(ffmpeg_dir_alt), 'ffmpeg'))
    logger.info(f"Including FFmpeg from: {ffmpeg_dir_alt}")
    ffmpeg_found = True

if not ffmpeg_found:
    logger.warning(f"FFmpeg not found at {ffmpeg_dir} or {ffmpeg_dir_alt}. FFmpeg will not be bundled.")

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
    upx=False,  # Disable UPX to preserve icon quality
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_file) if icon_file.exists() else None,  # Use icon.ico if it exists
)
