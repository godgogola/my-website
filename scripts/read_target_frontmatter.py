import os, sys
sys.stdout.reconfigure(encoding='utf-8')

src = r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫\代謝異常相關脂肪性肝病與大腸腺瘤.md"
with open(src, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()[:25]
    for line in lines:
        print(line, end='')

