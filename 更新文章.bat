@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo =========================================
echo   Article Sync Tool
echo =========================================
echo.

echo [1/2] Syncing Obsidian articles...
node scripts/sync-obsidian.js
if %errorlevel% neq 0 (
    echo [ERROR] Sync failed. Check Google Drive path in .env
    pause
    exit /b 1
)
echo.

echo [2/3] Matching cover images...
node scripts/auto-cover-image-v2.js
echo.

echo [3/3] Syncing URLs to Google Sheet...
node scripts/sync-sheet.js
echo.

echo =========================================
echo   Done! Next: double-click publish.bat
echo =========================================
echo.
pause
