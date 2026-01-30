#!/bin/bash
# Build script for VideoMixerConcat Desktop App
# This script will:
# 1. Create icon.ico from PNG logo
# 2. Kill any running VideoMixerConcat.exe processes (if on Windows)
# 3. Remove old build files
# 4. Run PyInstaller

echo "========================================"
echo "VideoMixerConcat Build Script"
echo "========================================"
echo ""

# Create icon.ico if it doesn't exist
echo "[1/4] Creating icon.ico..."
if [ ! -f "icon.ico" ]; then
    # Try to combine existing ICO files first
    if [ -f "app/ui/assets/256x256.ico" ] && [ -f "app/ui/assets/16x16.ico" ]; then
        echo "Combining existing ICO files into icon.ico..."
        python combine_ico.py
        if [ $? -ne 0 ]; then
            echo "Failed to combine ICO files, trying create_icon.py..."
            python create_icon.py
        fi
    else
        echo "Creating icon.ico from logo128x128.png..."
        python create_icon.py
    fi
    if [ $? -ne 0 ]; then
        echo "WARNING: Failed to create icon.ico. Building without icon."
    fi
else
    echo "icon.ico already exists, skipping..."
fi
echo ""

# Check if VideoMixerConcat.exe is running and kill it (Windows only)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "[2/4] Checking for running processes..."
    if tasklist //FI "IMAGENAME eq VideoMixerConcat.exe" 2>/dev/null | grep -q "VideoMixerConcat.exe"; then
        echo "Found running VideoMixerConcat.exe - closing it..."
        taskkill //F //IM VideoMixerConcat.exe >/dev/null 2>&1
        sleep 1
        echo "Process closed."
    else
        echo "No running processes found."
    fi
    echo ""
fi

# Remove old executable if it exists
echo "[3/4] Cleaning old build files..."
if [ -f "dist/VideoMixerConcat.exe" ]; then
    echo "Removing old executable..."
    rm -f "dist/VideoMixerConcat.exe"
    if [ -f "dist/VideoMixerConcat.exe" ]; then
        echo "WARNING: Could not remove old executable. It may be in use."
        echo "Please close VideoMixerConcat.exe manually and try again."
        exit 1
    fi
    echo "Old executable removed."
else
    echo "No old executable found."
fi
echo ""

# Run PyInstaller
echo "[4/4] Building with PyInstaller..."
echo ""
python -m PyInstaller pyinstaller.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Build completed successfully!"
    echo "Executable: dist/VideoMixerConcat.exe"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Build failed! Check the error messages above."
    echo "========================================"
    exit 1
fi
