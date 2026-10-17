@echo off
cd /d "%~dp0\.."
"C:\Program Files\nodejs\node.exe" scripts\auto-sync-service.js %*
