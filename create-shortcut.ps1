$ws = New-Object -ComObject WScript.Shell
$desktop = [System.Environment]::GetFolderPath('Desktop')
$batFile = Join-Path $desktop "Antigravity_Projects\個人網站\一鍵更新發布.bat"
$workDir = Join-Path $desktop "Antigravity_Projects\個人網站"
$shortcutPath = Join-Path $desktop "Update-Website.lnk"
$shortcut = $ws.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "cmd.exe"
$shortcut.Arguments = "/k `"$batFile`""
$shortcut.WorkingDirectory = $workDir
$shortcut.Save()
Write-Host "Done: $shortcutPath"
