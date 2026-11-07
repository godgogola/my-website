import glob, re, sys

py_files = glob.glob('c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/**/*.py', recursive=True)
for p in py_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'clip_' in c:
        matches = re.findall(r'clip_\d+', c)
        sys.stdout.buffer.write(f"=== {p} ===\n".encode('utf-8'))
        for m in sorted(set(matches)):
            sys.stdout.buffer.write(f"  {m}\n".encode('utf-8'))
