@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ==========================================
echo   黃醫師個人網站  一鍵更新發布
echo ==========================================
echo.

echo [1/5] 同步 Obsidian 文章（新增 / 刪除 / 標題 / 排序）...
node scripts/sync-obsidian.js
if %errorlevel% neq 0 (
    echo [錯誤] 文章同步失敗，請確認 Google Drive 路徑。
    pause
    exit /b 1
)
echo.

echo [2/5] 同步 Google Drive 圖片...
node scripts/sync-drive-images.js
echo.

echo [3/5] 編譯網站...
npm run build
if %errorlevel% neq 0 (
    echo [錯誤] 編譯失敗，請確認文章格式。
    pause
    exit /b 1
)
echo.

echo [4/5] 將文章網址寫回 Google Sheet...
node scripts/sync-sheet.js
echo.

echo [5/5] 推送到 GitHub，Vercel 自動部署...
git add -A
git commit -m "Auto update: articles + images"
git push origin main
echo.

echo ==========================================
echo   完成！網站約 1~2 分鐘後更新：
echo   https://drhuanggi.vercel.app
echo ==========================================
echo.
pause
