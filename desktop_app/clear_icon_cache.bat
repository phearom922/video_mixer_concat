@echo off
REM Clear Windows Icon Cache to refresh EXE icons
echo Clearing Windows Icon Cache...
echo.

REM Stop Windows Explorer to clear cache
taskkill /f /im explorer.exe >nul 2>&1

REM Clear icon cache
del /a /q /f "%LOCALAPPDATA%\IconCache.db" >nul 2>&1
del /a /q /f "%LOCALAPPDATA%\Microsoft\Windows\Explorer\iconcache*.db" >nul 2>&1
del /a /q /f "%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db" >nul 2>&1

REM Restart Windows Explorer
start explorer.exe

echo.
echo Icon cache cleared!
echo Please refresh File Explorer (F5) or restart your computer.
echo.
pause
