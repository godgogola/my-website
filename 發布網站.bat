@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo =========================================
echo   Build and Deploy to Vercel
echo =========================================
echo.

echo [1/2] Building...
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/2] Deploying to Vercel...
cd dist
call npx vercel --prod --yes
cd ..

echo.
echo =========================================
echo   Live at: https://drhuanggi.vercel.app
echo =========================================
echo.
pause
