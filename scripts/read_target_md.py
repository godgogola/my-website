import os, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫\代謝異常相關脂肪性肝病與大腸腺瘤.md"
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read()[:1000])
else:
    print("File not found at", path)

