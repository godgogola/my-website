import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/videos.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '漫步華爾街' in line and 'title:' in line:
        for j in range(max(0, i-2), min(len(lines), i+15)):
            print(lines[j], end='')
        print('='*30)

