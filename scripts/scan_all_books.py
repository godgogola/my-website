import os
import re

vault_books = 'G:/我的雲端硬碟/讀書筆記庫/讀書筆記'
missing = []
for root, dirs, files in os.walk(vault_books):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            with open(fp, encoding='utf-8', errors='ignore') as fp_obj:
                c = fp_obj.read()
            cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
            cover = cover_m.group(1).strip() if cover_m else ''
            if not cover or not os.path.exists(os.path.join('public/images', cover)):
                missing.append((fp, cover))

print(f"Total missing in vault_books: {len(missing)}")
for item in missing:
    print(item[0], "-->", repr(item[1]))

