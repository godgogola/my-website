import fs from 'fs';
import { execSync } from 'child_process';
import path from 'path';

const psScript = `
$ws = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath('Desktop')

$s1 = $ws.CreateShortcut([System.IO.Path]::Combine($desktop, "更新文章.lnk"))
$s1.TargetPath = "c:\\Users\\X1 Yoga Gen7\\Desktop\\Antigravity_Projects\\個人網站\\更新文章.bat"
$s1.WorkingDirectory = "c:\\Users\\X1 Yoga Gen7\\Desktop\\Antigravity_Projects\\個人網站"
$s1.Save()

$s2 = $ws.CreateShortcut([System.IO.Path]::Combine($desktop, "發布網站.lnk"))
$s2.TargetPath = "c:\\Users\\X1 Yoga Gen7\\Desktop\\Antigravity_Projects\\個人網站\\發布網站.bat"
$s2.WorkingDirectory = "c:\\Users\\X1 Yoga Gen7\\Desktop\\Antigravity_Projects\\個人網站"
$s2.Save()
`;

fs.writeFileSync('scripts/_make_shortcuts.ps1', psScript, 'utf16le');
execSync('powershell -NoProfile -ExecutionPolicy Bypass -File scripts/_make_shortcuts.ps1');
fs.unlinkSync('scripts/_make_shortcuts.ps1');
console.log('Shortcuts created successfully on Desktop!');
