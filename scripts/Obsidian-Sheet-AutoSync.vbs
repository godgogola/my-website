Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
WshShell.Run """C:\Program Files\nodejs\node.exe"" ""C:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\scripts\auto-sync-service.js"" --watch", 0, False
