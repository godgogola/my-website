import glob
import re

articles = []
for p in glob.glob('src/content/posts/**/*.md', recursive=True):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    slug_m = re.search(r'^slug:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else ''
    cover = cover_m.group(1).strip() if cover_m else ''
    slug = slug_m.group(1).strip() if slug_m else ''
    articles.append((title, cover, slug))

queries = ['纖維', '便秘', '內臟脂肪', '體重', '肥胖', '痔瘡', '肛門', '功能性消化不良', '敏感', '逆流', '賁門', '胃藥']
for q in queries:
    matched = [a for a in articles if q in a[0]]
    print(f"\n=== Query: {q} ({len(matched)}) ===")
    for t, c, s in matched:
        print(f"  {t} | cover: {c} | slug: {s}")

