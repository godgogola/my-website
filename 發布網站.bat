@echo off
chcp 65001 >nul
echo =========================================
echo   🚀 開始打包並自動發布網站至 Vercel...
echo =========================================
echo.

echo [1/3] 正在進行 Astro 專案打包與圖片優化...
call npm run build
if %errorlevel% neq 0 (
    echo.
    echo ❌ 打包失敗，請檢查 error 訊息。
    pause
    exit /b %errorlevel%
)

echo.
echo [2/3] 正在上傳至 Vercel 雲端伺服器...
call npx vercel dist --prod --yes > vercel_deploy.tmp 2>&1
type vercel_deploy.tmp

for /f "tokens=*" %%a in ('powershell -Command "Select-String -Path vercel_deploy.tmp -Pattern 'https://dist-[a-zA-Z0-9-]+\.vercel\.app' | ForEach-Object { $_.Matches.Value } | Select-Object -First 1"') do (
    set DEPLOY_URL=%%a
)

if exist vercel_deploy.tmp del vercel_deploy.tmp

if defined DEPLOY_URL (
    echo.
    echo [3/3] 正在更新網址別名至 https://drhuanggi.vercel.app ...
    call npx vercel alias set %DEPLOY_URL% drhuanggi.vercel.app
)

echo.
echo =========================================
echo   🎉 發布完成！網站已更新上線：
echo   👉 https://drhuanggi.vercel.app
echo =========================================
echo.
pause
