import sys
import glob
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

print("--- POSTS ---")
for p in sorted(glob.glob('src/content/posts/*.md')):
    with open(p, encoding='utf-8', errors='ignore') as f:
        content = f.read(2000)
    m = re.search(r'^coverImage:\s*["\']?([^"\'\r\n]+)', content, re.M)
    mt = re.search(r'^title:\s*["\']?([^"\'\r\n]+)', content, re.M)
    title = mt.group(1).strip() if mt else os.path.basename(p)
    if not m or not m.group(1).strip():
        print('MISSING_FIELD:', p, '->', title)
    else:
        img = m.group(1).strip()
        imgPath = os.path.join('public', 'images', img)
        if not os.path.exists(imgPath):
            print('MISSING_FILE:', p, '->', title, '->', img)

print("\n--- BOOKS ---")
for b in sorted(glob.glob('src/content/books/**/*.md', recursive=True)):
    with open(b, encoding='utf-8', errors='ignore') as f:
        content = f.read(2000)
    m = re.search(r'^coverImage:\s*["\']?([^"\'\r\n]+)', content, re.M)
    mt = re.search(r'^title:\s*["\']?([^"\'\r\n]+)', content, re.M)
    title = mt.group(1).strip() if mt else os.path.basename(b)
    if not m or not m.group(1).strip():
        print('MISSING_FIELD:', b, '->', title)
    else:
        img = m.group(1).strip()
        imgPath = os.path.join('public', 'images', img)
        if not os.path.exists(imgPath):
            print('MISSING_FILE:', b, '->', title, '->', img)
