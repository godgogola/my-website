import os
import re
import glob

# 1. Map all article slugs to cover images
article_covers = {}
for p in glob.glob('src/content/posts/**/*.md', recursive=True):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    slug_m = re.search(r'^slug:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    if slug_m and cover_m:
        slug = slug_m.group(1).strip()
        cover = cover_m.group(1).strip()
        if cover:
            article_covers[slug] = cover
            # Also map by filename without .md
            fname = os.path.basename(p)[:-3]
            article_covers[fname] = cover

for p in glob.glob('src/content/books/**/*.md', recursive=True):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    slug_m = re.search(r'^slug:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    if slug_m and cover_m:
        slug = slug_m.group(1).strip()
        cover = cover_m.group(1).strip()
        if cover:
            article_covers[slug] = cover
            fname = os.path.basename(p)[:-3]
            article_covers[fname] = cover

print(f"Loaded {len(article_covers)} article covers.")

# Images in public/images
imgs = set(os.listdir('public/images'))

with open('src/data/videos.ts', encoding='utf-8') as f:
    text = f.read()

# IDs to delete (old duplicates)
ids_to_delete = {
    'Dh9Jw6_vjeE', 'rIjNaG6bC-4',  # Old 112年癌症報告
    'nm3keREnygc', 'hgCnVzCK2pU',  # Old ADA CKM and ADA 減重
    'QxOiC07S_5U', 'B075tkOgJsU',  # Old 肥胖症併發症 / 成因
    'ejbWIapWkOg',                 # Old 低普林飲食
    'Uc2noq__XRI',                 # Old 腸躁症 FODMAP
    'QjjcFWusVuo',                 # Old 痔瘡搔癢
    '0_rTHkFiWCg',                 # Old 功能性消化不良
    '5QzZgF4Walk',                 # Old 胃食道逆流地雷食物
    'ccNwVrnfOdU',                 # Old 2025-2030 美國飲食指南
    'AwR8aWhIF8Q',                 # Old 酒精性肝病變
    'qXkyGWRIDE4',                 # Old 糖尿病腎病變 uACR
    '2kJNETkTM8g',                 # Old GI 值
    'ogqU3y1DJ8c',                 # Old 護胃食物
    'a_XLn5Ld5c0',                 # Old 膽囊息肉
    'y2E0G9_vBNE',                 # Old 一份蛋白質要怎麼吃
    'ByaMQ7Sopno',                 # Old 跑步五大心率區間
    'PV2xcZVN6No',                 # Old 各種會讓胃食道逆流的食物
    '-Nfxr0NGDQ0',                 # Old 無痛腸胃鏡
    'x24UTTkEBLs'                  # Old 荷爾蒙複合療法 / 內臟脂肪
}

# Regex to delete video objects by ID
for vid in ids_to_delete:
    pattern = rf"\s*\{{[^{{}}]*?id:\s*'{re.escape(vid)}'[^{{}}]*?\}},?"
    text, n = re.subn(pattern, '', text)
    if n > 0:
        print(f"Deleted old duplicate: {vid}")

# Specific fixes for the 2 ADA videos in Fig 2:
# 1. _HUpicLz4QI
# 2. dAs0r8vuxGM
ada_ckm_cover = "【2026 ADA】 糖尿病照護_心血管-腎臟-代謝（CKM）綜合風險管理.webp"
ada_weight_cover = "【2026 ADA】合法且具實證基礎的減重方法.webp"

if ada_ckm_cover not in imgs:
    # check without space
    alt = "【2026 ADA】糖尿病照護_心血管-腎臟-代謝（CKM）綜合風險管理.webp"
    if alt in imgs:
        ada_ckm_cover = alt

print(f"Using ADA CKM cover: {ada_ckm_cover} (exists: {ada_ckm_cover in imgs})")
print(f"Using ADA Weight cover: {ada_weight_cover} (exists: {ada_weight_cover in imgs})")

# Add/replace thumbnail in _HUpicLz4QI block
pattern_ckm = r"(\{\s*id:\s*'_HUpicLz4QI'[\s\S]*?)(\n\s*featured:)"
text = re.sub(pattern_ckm, rf"\1\n    thumbnail: '/images/{ada_ckm_cover}',\2", text)

# Add/replace thumbnail in dAs0r8vuxGM block
pattern_weight = r"(\{\s*id:\s*'dAs0r8vuxGM'[\s\S]*?)(\n\s*featured:)"
text = re.sub(pattern_weight, rf"\1\n    thumbnail: '/images/{ada_weight_cover}',\2", text)

# Now, for any remaining video blocks in text that have articleSlug but NO thumbnail:
def add_thumbnail_if_missing(match):
    block = match.group(0)
    if 'thumbnail:' in block:
        return block
    slug_m = re.search(r"articleSlug:\s*'([^']+)'", block)
    if not slug_m:
        return block
    slug = slug_m.group(1).replace('/posts/', '').replace('/books/', '').strip('/')
    if '/' in slug:
        slug = slug.split('/')[-1]
    
    cover = article_covers.get(slug)
    if not cover:
        # try matching
        for k, v in article_covers.items():
            if k in slug or slug in k:
                cover = v
                break
                
    if cover and cover in imgs:
        print(f"Adding thumbnail to {slug_m.group(1)} -> /images/{cover}")
        # Insert before featured: or order:
        if 'featured:' in block:
            return block.replace('featured:', f"thumbnail: '/images/{cover}',\n    featured:")
        elif 'order:' in block:
            return block.replace('order:', f"thumbnail: '/images/{cover}',\n    order:")
    return block

video_obj_pattern = re.compile(r'\{\s*id:\s*\'[^\']+\'[\s\S]*?\n\s*\}')
text = video_obj_pattern.sub(add_thumbnail_if_missing, text)

with open('src/data/videos.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("=== Successfully updated src/data/videos.ts ===")
