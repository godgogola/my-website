import json
import re

with open('scripts/islands_24_data.json', encoding='utf-8') as f:
    islands_data = json.load(f)

# 讀取現有的 island.astro
with open('src/pages/island.astro', encoding='utf-8') as f:
    content = f.read()

# 1. 產生 Frontmatter 的 ISLAND_ARTICLES_MAP
frontmatter_map_lines = ["const ISLAND_ARTICLES_MAP: Record<string, any[]> = {"]
for isl in islands_data:
    isl_id = isl["id"]
    if isl["realm"] == "health":
        cat = isl["category"]
        extra = []
        if isl_id == "chronic":
            extra = ["疑難雜症"]
        elif isl_id == "stomach":
            extra = ["消化道癌症專區"]
        elif isl_id == "endoscopy":
            extra = ["診間隨筆"]
        cats = [cat] + extra
        frontmatter_map_lines.append(f"  '{isl_id}': extractPosts({json.dumps(cats, ensure_ascii=False)}),")
    else:
        book = isl["book"]
        frontmatter_map_lines.append(f"  '{isl_id}': extractBookChapters(['{book}']),")
frontmatter_map_lines.append("};")
new_frontmatter_map = "\n".join(frontmatter_map_lines)

# 替換 Frontmatter 中的 const ISLAND_ARTICLES_MAP
content = re.sub(
    r'const ISLAND_ARTICLES_MAP: Record<string, any\[\]> = \{[\s\S]*?\n\};',
    new_frontmatter_map,
    content
)

# 2. 更新 HUD 中的群島數量與 Tab 標籤
content = re.sub(
    r'<span class="dot all"></span>全部星系 \(\d+\)',
    '<span class="dot all"></span>全部星系 (24)',
    content
)
content = re.sub(
    r'<span class="dot health"></span>🏥 人體健康 \(\d+\)',
    '<span class="dot health"></span>🏥 人體健康 (16)',
    content
)
content = re.sub(
    r'<span class="dot wisdom"></span>📚 知識宇宙 \(\d+\)',
    '<span class="dot wisdom"></span>📚 知識宇宙 (8)',
    content
)
content = re.sub(
    r'地球地平線弧度·雙星 \d+ 島·\d+ 篇全收錄',
    '微縮群島景觀·雙星系 24 座主題島·348 篇全收錄',
    content
)
content = re.sub(
    r'<span class="nav-count">\d+ 座群島</span>',
    '<span class="nav-count">24 座群島</span>',
    content
)
content = re.sub(
    r'12 座群島',
    '24 座群島',
    content
)

# 3. 產生 Three.js 客戶端的 ISLAND_META
js_meta_lines = ["  const ISLAND_META = ["]
for isl in islands_data:
    js_meta_lines.append("    {")
    js_meta_lines.append(f"      id: '{isl['id']}',")
    js_meta_lines.append(f"      realm: '{isl['realm']}',")
    js_meta_lines.append(f"      q: {isl['q']}, r: {isl['r']},")
    js_meta_lines.append(f"      name: '{isl['name']}',")
    js_meta_lines.append(f"      shortName: '{isl['shortName']}',")
    js_meta_lines.append(f"      icon: '{isl['icon']}',")
    js_meta_lines.append(f"      color: {isl['color']},")
    js_meta_lines.append(f"      roofColor: {isl['roofColor']},")
    js_meta_lines.append(f"      accentColor: {isl['accentColor']},")
    js_meta_lines.append(f"      subtitle: '{isl['subtitle']}',")
    js_meta_lines.append(f"      desc: '{isl['desc']}',")
    cta_url = "/health-column" if isl["realm"] == "health" else "/books"
    cta_text = f"探索更多「{isl['shortName']}」專題文章"
    js_meta_lines.append(f"      ctaUrl: '{cta_url}',")
    js_meta_lines.append(f"      ctaText: '{cta_text}',")
    js_meta_lines.append(f"      landmark: '{isl['landmark']}'")
    js_meta_lines.append("    },")
# 移除最後一項的多餘逗號
js_meta_lines[-1] = "    }"
js_meta_lines.append("  ];")
new_js_meta = "\n".join(js_meta_lines)

content = re.sub(
    r'  const ISLAND_META = \[[\s\S]*?\n  \];',
    new_js_meta,
    content
)

# 4. 更新建構島嶼裝飾地標的邏輯 (buildIslands) 讓不同 landmark 產生對應地標
# 檢查 buildIslands 是否已經呼叫 buildIslandDecorations
with open('src/pages/island.astro', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY_UPDATED_24_ISLANDS")
