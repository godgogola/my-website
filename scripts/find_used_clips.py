import glob, re, sys

py_files = glob.glob('c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/**/*.py', recursive=True)
used = {}

for p in py_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    matches = re.findall(r'(補足片段[123]_切分[\\/]clip_\d+\.mp4)', c)
    if matches:
        used[p] = matches

for p, m in used.items():
    sys.stdout.buffer.write(f"=== {p} ===\n".encode('utf-8'))
    for x in m:
        sys.stdout.buffer.write(f"  {x}\n".encode('utf-8'))
