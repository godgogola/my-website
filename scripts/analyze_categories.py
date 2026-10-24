import glob
import re

def get_cat(file_path):
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        text = f.read(1000)
    m = re.search(r'^category:\s*["\']?([^"\'\r\n]+)', text, re.M)
    return m.group(1).strip() if m else '未分類'

def get_book(file_path):
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        text = f.read(1000)
    m = re.search(r'^book:\s*["\']?([^"\'\r\n]+)', text, re.M)
    return m.group(1).strip() if m else '未分類書籍'

cats = {}
for p in glob.glob('src/content/posts/*.md'):
    c = get_cat(p)
    cats[c] = cats.get(c, 0) + 1

books = {}
for b in glob.glob('src/content/books/**/*.md', recursive=True):
    bk = get_book(b)
    books[bk] = books.get(bk, 0) + 1

with open('scripts/categories_result.txt', 'w', encoding='utf-8') as out:
    out.write('=== 醫學筆記文章分類 ===\n')
    total_p = 0
    for k, v in sorted(cats.items(), key=lambda x: -x[1]):
        out.write(f'{k}: {v} 篇\n')
        total_p += v
    out.write(f'總文章數: {total_p}\n\n')

    out.write('=== 讀書筆記書籍分類 ===\n')
    total_b = 0
    for k, v in sorted(books.items(), key=lambda x: -x[1]):
        out.write(f'{k}: {v} 篇\n')
        total_b += v
    out.write(f'總書籍章節數: {total_b}\n')
