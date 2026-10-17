import fs from 'fs';
import { execSync } from 'child_process';

const junctionDir = 'C:\\Users\\X1 Yoga Gen7\\drhuang-website';
const scriptPath = `${junctionDir}\\scripts\\auto-sync-service.js`;

const psScript = `
$ErrorActionPreference = 'Stop'

# 移除舊工作
Unregister-ScheduledTask -TaskName 'DrHuang-Obsidian-AutoSync' -Confirm:$false -ErrorAction SilentlyContinue

$nodeExe = 'C:\\Program Files\\nodejs\\node.exe'
if (-not (Test-Path $nodeExe)) {
    $nodeExe = (Get-Command node).Source
}

$action = New-ScheduledTaskAction -Execute $nodeExe -Argument '"${scriptPath}" --check' -WorkingDirectory '${junctionDir}'

# 觸發條件：開機登入時觸發，並且每 5 分鐘執行一次
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn
$triggerRepeat = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -Hidden -Priority 7

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

Register-ScheduledTask -TaskName 'DrHuang-Obsidian-AutoSync' -Action $action -Trigger @($triggerLogon, $triggerRepeat) -Settings $settings -Principal $principal -Description 'Auto sync Obsidian articles and books to Google Sheet' -Force

Write-Host "DrHuang-Obsidian-AutoSync task registered successfully!"
`;

fs.writeFileSync('scripts/_reg_task.ps1', '\ufeff' + psScript, 'utf16le');
try {
  const result = execSync('powershell -NoProfile -ExecutionPolicy Bypass -File scripts/_reg_task.ps1', { encoding: 'utf8' });
  console.log(result);
} finally {
  if (fs.existsSync('scripts/_reg_task.ps1')) {
    fs.unlinkSync('scripts/_reg_task.ps1');
  }
}
