import glob
import sys

for p in glob.glob('c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/**/*.py', recursive=True):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if '補足片段' in c:
        sys.stdout.buffer.write(f"Uses 補足片段: {p}\n".encode('utf-8'))
