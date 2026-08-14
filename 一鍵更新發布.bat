@echo off
chcp 950 > nul
cd /d "%~dp0"

REM Do not kill node.exe - avoid killing bat own node subprocesses

set LOGFILE=C:\Users\%USERNAME%\Desktop\update-log.txt
echo Started: %date% %time% > "%LOGFILE%"

echo.
echo ==========================================
echo   Dr Huang - Update and Publish
echo ==========================================
echo.

echo [1/7] Syncing Obsidian articles...
echo [1/7] Syncing Obsidian articles >> "%LOGFILE%"
node scripts/sync-obsidian.js
if %errorlevel% neq 0 (
    echo [ERROR] Step 1 failed
    pause
    exit /b 1
)
echo.

echo [2/7] Applying manual cover image mappings...
echo [2/7] Applying cover mappings >> "%LOGFILE%"
node scripts/apply-mapping.js
echo.

echo [3/7] Matching remaining cover images...
echo [3/7] Matching cover images >> "%LOGFILE%"
node scripts/auto-cover-image-v2.js
echo.

echo [4/7] Syncing Google Drive images (final authority)...
echo [4/7] Syncing Drive images >> "%LOGFILE%"
node scripts/sync-drive-images.js
echo.

echo [5/7] Building website...
echo [5/7] Building >> "%LOGFILE%"
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Step 5 Build failed
    pause
    exit /b 1
)
echo.

echo [6/7] Writing to Google Sheet...
echo [6/7] Sync sheet >> "%LOGFILE%"
node scripts/sync-sheet.js
echo.

echo [7/7] Deploying to Vercel...
echo [7/7] Deploying >> "%LOGFILE%"
git add -A
git commit -m "auto: sync %date% %time%"
if %errorlevel% neq 0 (
    echo [INFO] Nothing new to commit, continuing...
    echo [INFO] Nothing to commit >> "%LOGFILE%"
)
git push origin main
if %errorlevel% neq 0 (
    echo [ERROR] git push failed! Please check the error above.
    pause
    exit /b 1
)
npx vercel --prod --yes
if %errorlevel% neq 0 (
    echo [ERROR] Vercel deploy failed! Please check the error above.
    pause
    exit /b 1
)
echo.

echo Finished: %date% %time% >> "%LOGFILE%"

echo ==========================================
echo   Done! https://drhuanggi.vercel.app
echo ==========================================
echo.
echo Log saved to: %LOGFILE%
echo.
pause

