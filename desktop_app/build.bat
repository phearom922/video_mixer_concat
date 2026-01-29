@echo off
REM Build script for VideoMixerConcat Desktop App
REM This script will:
REM 1. Create icon.ico from PNG logo
REM 2. Kill any running VideoMixerConcat.exe processes
REM 3. Remove old build files
REM 4. Run PyInstaller

echo ========================================
echo VideoMixerConcat Build Script
echo ========================================
echo.

REM Create icon.ico if it doesn't exist
echo [1/4] Creating icon.ico...
if not exist "icon.ico" (
    echo Creating icon.ico from logo128x128.png...
    python create_icon.py
    if errorlevel 1 (
        echo WARNING: Failed to create icon.ico. Building without icon.
    )
) else (
    echo icon.ico already exists, skipping...
)
echo.

REM Check if VideoMixerConcat.exe is running and kill it
echo [2/4] Checking for running processes...
tasklist /FI "IMAGENAME eq VideoMixerConcat.exe" 2>NUL | find /I /N "VideoMixerConcat.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Found running VideoMixerConcat.exe - closing it...
    taskkill /F /IM VideoMixerConcat.exe >NUL 2>&1
    timeout /t 1 /nobreak >NUL
    echo Process closed.
) else (
    echo No running processes found.
)
echo.

REM Remove old executable if it exists
echo [3/4] Cleaning old build files...
if exist "dist\VideoMixerConcat.exe" (
    echo Removing old executable...
    del /F /Q "dist\VideoMixerConcat.exe" 2>NUL
    if exist "dist\VideoMixerConcat.exe" (
        echo WARNING: Could not remove old executable. It may be in use.
        echo Please close VideoMixerConcat.exe manually and try again.
        pause
        exit /b 1
    )
    echo Old executable removed.
) else (
    echo No old executable found.
)
echo.

REM Run PyInstaller
echo [4/4] Building with PyInstaller...
echo.
python -m PyInstaller pyinstaller.spec

if "%ERRORLEVEL%"=="0" (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo Executable: dist\VideoMixerConcat.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Build failed! Check the error messages above.
    echo ========================================
    pause
    exit /b 1
)

pause
