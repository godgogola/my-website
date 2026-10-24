import glob
import re
import os

posts_no_cover = []
for p in glob.glob('src/content/posts/*.md'):
    with open(p, encoding='utf-8', errors='ignore') as f:
        text = f.read(1200)
    m = re.search(r'^coverImage:\s*["\']?([^"\'\r\n]+)', text, re.M)
    if not m or not m.group(1).strip():
        mt = re.search(r'^title:\s*["\']?([^"\'\r\n]+)', text, re.M)
        title = mt.group(1).strip() if mt else os.path.basename(p)
        posts_no_cover.append((p, title))

books_no_cover = []
for b in glob.glob('src/content/books/**/*.md', recursive=True):
    with open(b, encoding='utf-8', errors='ignore') as f:
        text = f.read(1200)
    m = re.search(r'^coverImage:\s*["\']?([^"\'\r\n]+)', text, re.M)
    if not m or not m.group(1).strip():
        mt = re.search(r'^title:\s*["\']?([^"\'\r\n]+)', text, re.M)
        title = mt.group(1).strip() if mt else os.path.basename(b)
        books_no_cover.append((b, title))

with open('scripts/missing_covers_summary.txt', 'w', encoding='utf-8') as out:
    out.write(f'未設封面圖衛教專文: {len(posts_no_cover)} 篇\n')
    out.write(f'未設封面圖書籍章節: {len(books_no_cover)} 篇\n\n')
    out.write('=== 未設封面圖書籍章節列表 ===\n')
    for b, t in books_no_cover:
        out.write(f'{b} -> {t}\n')
    out.write('\n=== 未設封面圖衛教專文列表 (前 30 篇) ===\n')
    for p, t in posts_no_cover[:30]:
        out.write(f'{p} -> {t}\n')

print("SCAN_COMPLETE")
