@echo off
cd /d "%~dp0"

set LOGFILE=%~dp0update-log.txt
echo Started: %date% %time% > "%LOGFILE%"

echo.
echo ==========================================
echo   Dr Huang - Update and Publish
echo ==========================================
echo.

echo [1/6] Syncing Obsidian articles...
echo [1/6] Syncing Obsidian articles >> "%LOGFILE%"
node scripts/sync-obsidian.js 1>> "%LOGFILE%" 2>> "%LOGFILE%"
if %errorlevel% neq 0 (
    echo [ERROR] Step 1 failed - see update-log.txt for details
    pause
    exit /b 1
)
echo.

echo [2/6] Syncing Google Drive images...
echo [2/6] Syncing Drive images >> "%LOGFILE%"
node scripts/sync-drive-images.js 1>> "%LOGFILE%" 2>> "%LOGFILE%"
echo.

echo [3/6] Matching cover images...
echo [3/6] Matching cover images >> "%LOGFILE%"
node scripts/auto-cover-image-v2.js 1>> "%LOGFILE%" 2>> "%LOGFILE%"
echo.

echo [4/6] Building website...
echo [4/6] Building >> "%LOGFILE%"
npm run build 1>> "%LOGFILE%" 2>> "%LOGFILE%"
if %errorlevel% neq 0 (
    echo [ERROR] Step 4 failed - see update-log.txt for details
    pause
    exit /b 1
)
echo.

echo [5/6] Writing to Google Sheet...
echo [5/6] Sync sheet >> "%LOGFILE%"
node scripts/sync-sheet.js 1>> "%LOGFILE%" 2>> "%LOGFILE%"
echo.

echo [6/6] Deploying to Vercel...
echo [6/6] Deploying >> "%LOGFILE%"
git add -A 1>> "%LOGFILE%" 2>> "%LOGFILE%"
git commit -m "auto: sync %date% %time%" 1>> "%LOGFILE%" 2>> "%LOGFILE%"
start /b git push origin main
npx vercel --prod --yes 1>> "%LOGFILE%" 2>> "%LOGFILE%"
echo.

echo Finished: %date% %time% >> "%LOGFILE%"

echo ==========================================
echo   Done! https://drhuanggi.vercel.app
echo ==========================================
echo.
echo Log saved to: %LOGFILE%
echo.
pause
