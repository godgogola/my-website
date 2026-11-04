import os, sys
sys.stdout.reconfigure(encoding='utf-8')

vault = r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫"
for d in os.listdir(vault):
    full = os.path.join(vault, d)
    if os.path.isdir(full):
        print(f"Directory: {d}")

