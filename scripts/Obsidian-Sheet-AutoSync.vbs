Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\X1 Yoga Gen7\drhuang-website"
WshShell.Run """C:\Program Files\nodejs\node.exe"" ""C:\Users\X1 Yoga Gen7\drhuang-website\scripts\auto-sync-service.js"" --watch", 0, False
