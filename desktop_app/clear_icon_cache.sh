#!/bin/bash
# Clear Windows Icon Cache (for Git Bash)
# Note: This requires Windows commands, so it may not work in Git Bash
# Use clear_icon_cache.bat instead

echo "Clearing Windows Icon Cache..."
echo ""
echo "⚠️  Note: This script requires Windows commands."
echo "   Please use clear_icon_cache.bat instead, or run these commands manually:"
echo ""
echo "   taskkill /f /im explorer.exe"
echo "   del /a /q /f \"%LOCALAPPDATA%\\IconCache.db\""
echo "   del /a /q /f \"%LOCALAPPDATA%\\Microsoft\\Windows\\Explorer\\iconcache*.db\""
echo "   start explorer.exe"
echo ""
