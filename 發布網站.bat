@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo =========================================
echo   自動同步與發布網站到 Vercel
echo =========================================
echo.

echo [1/4] 正在同步 Google Drive / Obsidian 文章與圖片...
call node scripts/sync-obsidian.js
call node scripts/sync-drive-images.js

echo.
echo [2/4] 正在編譯網站...
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] 編譯失敗，請檢查文章格式。
    pause
    exit /b %errorlevel%
)

echo.
echo [3/4] 正在同步文章與圖片網址至 Google Sheet...
call node scripts/sync-sheet.js

echo.
echo [4/4] 正在推送更新至 Vercel 雲端發布...
call git add .
call git commit -m "Auto update articles and images"
call git push origin main

echo.
echo =========================================
echo   發布完成！網站將於 1-2 分鐘內於線上更新：
echo   https://drhuanggi.vercel.app
echo =========================================
echo.
pause
