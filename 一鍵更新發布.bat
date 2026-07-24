@echo off
cd /d "%~dp0"

echo.
echo ==========================================
echo   Dr Huang - Update and Publish
echo ==========================================
echo.

echo [1/6] Syncing Obsidian articles...
node scripts/sync-obsidian.js
if %errorlevel% neq 0 (
    echo [ERROR] Article sync failed. Check Google Drive path in .env
    pause
    exit /b 1
)
echo.

echo [2/6] Syncing Google Drive images...
node scripts/sync-drive-images.js
echo.

echo [3/6] Matching cover images...
node scripts/auto-cover-image-v2.js
echo.

echo [4/6] Building website...
npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Build failed. Check article format.
    pause
    exit /b 1
)
echo.

echo [5/6] Writing URLs and images to Google Sheet...
node scripts/sync-sheet.js
echo.

echo [6/6] Pushing to GitHub and deploying to Vercel...
git add -A
git commit -m "auto: sync articles and images %date% %time%"
git push origin main
if %errorlevel% neq 0 (
    echo [WARNING] git push failed. Trying Vercel direct deploy...
)
call npx vercel --prod --yes
echo.

echo ==========================================
echo   Done! Website updated:
echo   https://drhuanggi.vercel.app
echo ==========================================
echo.
pause
