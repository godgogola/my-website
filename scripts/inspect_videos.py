import re

with open('src/data/videos.ts', encoding='utf-8') as f:
    text = f.read()

# match video objects
pattern = re.compile(r"id:\s*'([^']+)',\s*title:\s*'([^']+)'", re.MULTILINE)
matches = pattern.findall(text)
print(f"Total videos in videos.ts: {len(matches)}")
for vid, title in matches:
    if any(k in title for k in ['腸鏡', '胃鏡', '瘦', '減重', '脂肪', '潛血', '保可淨', '耐福力', '低渣', '膽固醇', '三酸甘油脂', '痛風', '纖維', '打嗝', '黑腸', '痔瘡']):
        print(f"{vid} | {title}")

