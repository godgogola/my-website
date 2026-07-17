@echo off
chcp 65001 > nul
title 🚀 豐田診所網站 — 一鍵更新文章
color 0A

echo.
echo  ╔═══════════════════════════════════════╗
echo  ║   🏥 豐田診所個人網站 — 文章更新工具  ║
echo  ╚═══════════════════════════════════════╝
echo.

:: 切換到腳本所在的專案根目錄
cd /d "%~dp0"

echo  📂 目前專案目錄：%CD%
echo.

:: ─── Step 1：同步 Obsidian 文章 ───
echo  ⏳ [Step 1/2] 正在同步 Obsidian 文章...
echo  ─────────────────────────────────────────
node scripts/sync-obsidian.js
if %errorlevel% neq 0 (
    echo.
    echo  ❌ 同步失敗！請確認：
    echo     - Google 雲端硬碟已同步（G 槽有最新文章）
    echo     - .env 檔案中的路徑設定正確
    pause
    exit /b 1
)
echo.
echo  ✅ 文章同步完成！
echo.

:: ─── Step 2：自動配對封面圖片 ───
echo  ⏳ [Step 2/2] 正在自動配對封面圖片...
echo  ─────────────────────────────────────────
node scripts/auto-cover-image-v2.js
if %errorlevel% neq 0 (
    echo.
    echo  ⚠️  封面圖片配對異常，但不影響文章發布，可手動補上。
)
echo.
echo  ✅ 封面圖片配對完成！
echo.

:: ─── 完成 ───
echo  ╔═══════════════════════════════════════╗
echo  ║         🎉 文章更新流程完成！          ║
echo  ╠═══════════════════════════════════════╣
echo  ║                                       ║
echo  ║  接下來請手動執行：                    ║
echo  ║                                       ║
echo  ║  【預覽】 npm run dev                  ║
echo  ║           → localhost:4321            ║
echo  ║                                       ║
echo  ║  【部署】 npm run build                ║
echo  ║                                       ║
echo  ╚═══════════════════════════════════════╝
echo.
pause
