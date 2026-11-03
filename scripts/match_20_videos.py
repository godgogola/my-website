import json
import os
import glob
import re

with open('scripts/today_20_new_videos.json', encoding='utf-8') as f:
    videos = json.load(f)

# Find all articles in src/content/posts
articles = []
for p in glob.glob('src/content/posts/**/*.md', recursive=True):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    slug_m = re.search(r'^slug:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    category_m = re.search(r'^category:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else os.path.basename(p)[:-3]
    cover = cover_m.group(1).strip() if cover_m else ''
    slug = slug_m.group(1).strip() if slug_m else os.path.basename(p)[:-3]
    cat = category_m.group(1).strip() if category_m else ''
    articles.append({
        'path': p,
        'title': title,
        'cover': cover,
        'slug': slug,
        'category': cat
    })

print(f"Loaded {len(articles)} articles.")

# Check public/images
images = os.listdir('public/images')

for v in videos:
    vid = v['id']
    vtitle = v['title']
    
    # Try to find best matching article
    best_match = None
    best_score = 0
    
    # Extract keywords
    for a in articles:
        score = 0
        at = a['title']
        # check overlap
        if at in vtitle:
            score += len(at) * 2
        for word in ['膳食纖維', '水溶性', '內臟脂肪', '體重設定點', '打嗝', '痛風', '高尿酸', '瘦瘦針', '復胖', 
                     '好膽固醇', 'HDL', '壞膽固醇', 'LDL', '低腹敏', 'FODMAP', '腸躁症', '三酸甘油脂', 
                     '痔瘡', '黑腸症', '大腸癌', '腺瘤偵測率', '高品質大腸鏡', '保可淨', '耐福力散', '清腸劑',
                     '胃食道逆流', '賁門', '脂肪肝', '果糖', '飲食指南', '酒精性肝病變', '腸腦軸', '內臟高敏感',
                     '功能性消化不良', '排便酵素', '番瀉葉']:
            if word in vtitle and word in at:
                score += len(word)
        if score > best_score:
            best_score = score
            best_match = a
            
    print(f"\nVideo: {vid} | {vtitle}")
    if best_match:
        # Check if cover image exists
        cname = best_match['cover']
        exists = cname in images
        print(f"  -> Matched Article: {best_match['title']} (slug: {best_match['slug']}, cat: {best_match['category']})")
        print(f"  -> CoverImage: {cname} (exists in public/images: {exists})")
    else:
        print("  -> NO MATCH FOUND")

