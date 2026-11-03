import json
import re
import os

print("=== Starting Video Pipeline Update ===")

# 1. Load prepared 20 videos
with open('scripts/prepared_20_videos.json', encoding='utf-8') as f:
    new_20 = json.load(f)

# 2. Update src/data/videos.ts
with open('src/data/videos.ts', encoding='utf-8') as f:
    v_text = f.read()

# Fix broken thumbnail paths in existing videos
v_text = v_text.replace('/images/糞便潛血陽性就一定是大腸癌嗎.webp', '/images/【糞便潛血】陽性就一定是大腸癌嗎.webp')
v_text = v_text.replace('/images/糖尿病腎病變-uacr-處置.webp', '/images/糖尿病腎病變 uACR 處置.webp')
v_text = v_text.replace('/images/護胃食物.webp', '/images/【護胃食物】.webp')
v_text = v_text.replace('/images/早期肝纖維化.webp', '/images/【早期】肝纖維化.webp')
v_text = v_text.replace('/images/傷胃食物.webp', '/images/【地雷食物】各種會讓胃食道逆流的食物.webp')
v_text = v_text.replace('/images/ppi要空腹吃.webp', '/images/【PPI】要空腹吃.webp')

# Remove any old duplicates whose ID or title overlaps with new 20
new_20_ids = {item['id'] for item in new_20}
old_ids_to_purge = {
    'S2QcETFlIxI', 'hBuG7IPxWRQ', 'z-gNT0nBsZU', 'Eo7sb0VvcTs', 'c7jElX1VEbE',
    'VeS9ab3m4eY', '0Ix8__RylaU', 'wX_x4coVRdo', 'HAnVmVkq9tA', 'fzSfjOyjO3I',
    'iiiWL3Cym5c', 'mh6heUd_KL8', 'L5K_BmeQhdk', 'rW2WJlv-6u8', 'VHAj3C0k-9U',
    'NofolUg41VI', 'sseuG7b9Weo', 'YsSXPMT3oHk', '9LZW5TyMJN8', 'Pxr4JXd-hRg',
    'wvF-j4jZOxU', '7M9UeRu2KT0', 'TJLqk1pfn7Q', 'gkBta3p1_Jo'
}

# Regex to remove video objects by ID
def remove_video_by_id(text, vid):
    # Pattern matching an object with this id
    pattern = rf"\s*\{{[^{{}}]*?id:\s*'{re.escape(vid)}'[^{{}}]*?\}},?"
    return re.sub(pattern, '', text)

removed_count = 0
for vid in (new_20_ids | old_ids_to_purge):
    if f"id: '{vid}'" in v_text:
        v_text = remove_video_by_id(v_text, vid)
        removed_count += 1
print(f"Purged {removed_count} old/duplicate video entries from videos.ts.")

# Format new 20 items to TypeScript objects
ts_items = []
for it in new_20:
    ts = f"""  {{
    id: '{it["id"]}',
    title: '{it["title"]}',
    description: '{it["description"]}',
    category: '{it["category"]}',
    duration: '{it["duration"]}',
    url: '{it["url"]}',
    featured: {str(it["featured"]).lower()},
    order: {it["order"]},
    thumbnail: '{it["thumbnail"]}',
    articleSlug: '{it["articleSlug"]}',
    articleTitle: '{it["articleTitle"]}',
  }},"""
    ts_items.append(ts)

new_entries_code = "\n".join(ts_items)

# Insert right after `export const videos: VideoItem[] = [`
target = "export const videos: VideoItem[] = ["
if target in v_text:
    v_text = v_text.replace(target, target + "\n" + new_entries_code, 1)
    print("Inserted 20 new videos at the top of export const videos.")
else:
    print("ERROR: Could not find target in videos.ts")

with open('src/data/videos.ts', 'w', encoding='utf-8') as f:
    f.write(v_text)
print("Updated src/data/videos.ts successfully.")


# 3. Update src/components/EndoscopyPageContent.astro
with open('src/components/EndoscopyPageContent.astro', encoding='utf-8') as f:
    e_text = f.read()

# Replace mainVideo
e_text = re.sub(
    r"const mainVideo = \{[\s\S]*?\};",
    """const mainVideo = {
  id: 'v_jzqjKDcH8',
  title: '怕痛怕吐不敢照腸胃鏡？無痛舒眠內視鏡全解析',
  subtitle: '安心睡眠中完成 · 肝膽腸胃專科團隊親自操作',
  description: '您對做胃鏡、大腸鏡感到恐懼嗎？豐田診所採用專業舒眠鎮靜麻醉技術與醫療級 CO2 充氣，讓您在如同小睡片刻的平穩放鬆狀態下，精準完成全消化道防癌檢查。'
};""",
    e_text,
    count=1
)

# In coreBowelVideos, update 清腸劑比較 id to 'ZBbCRg9-p8c'
e_text = e_text.replace("id: 'hBuG7IPxWRQ'", "id: 'ZBbCRg9-p8c'")

# In extraVideos:
# 高品質大腸鏡: VeS9ab3m4eY -> ec2MtIG8ygY
e_text = e_text.replace("id: 'VeS9ab3m4eY'", "id: 'ec2MtIG8ygY'")
# 黑腸症: c7jElX1VEbE -> -gQ2sZLsmbA
e_text = e_text.replace("id: 'c7jElX1VEbE'", "id: '-gQ2sZLsmbA'")
# 糞便潛血陽性: 0Ix8__RylaU -> _MFumV4dbgs
e_text = e_text.replace("id: '0Ix8__RylaU'", "id: '_MFumV4dbgs'")

with open('src/components/EndoscopyPageContent.astro', 'w', encoding='utf-8') as f:
    f.write(e_text)
print("Updated src/components/EndoscopyPageContent.astro successfully.")


# 4. Update src/pages/weight-loss.astro and src/pages/weight-loss/embed.astro
def update_weight_loss_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        w_text = f.read()

    # Step 1: B075tkOgJsU -> WFkqFR6V3E4
    w_text = w_text.replace("id: 'B075tkOgJsU'", "id: 'WFkqFR6V3E4'")
    # Step 2: QxOiC07S_5U -> JhMbwCXk6g8
    w_text = w_text.replace("id: 'QxOiC07S_5U'", "id: 'JhMbwCXk6g8'")
    # Step 3: x24UTTkEBLs -> ZjiOi4Ez_eM
    w_text = w_text.replace("id: 'x24UTTkEBLs'", "id: 'ZjiOi4Ez_eM'")
    # Step 8: HAnVmVkq9tA -> XeQxvq-WvC4
    w_text = w_text.replace("id: 'HAnVmVkq9tA'", "id: 'XeQxvq-WvC4'")
    # Step 9: fzSfjOyjO3I -> XeQxvq-WvC4
    w_text = w_text.replace("id: 'fzSfjOyjO3I'", "id: 'XeQxvq-WvC4'")
    # Step 11: ccNwVrnfOdU -> syjGKVpqUQc
    w_text = w_text.replace("id: 'ccNwVrnfOdU'", "id: 'syjGKVpqUQc'")
    # Step 12: y2E0G9_vBNE -> GEarPGa3Wso
    w_text = w_text.replace("id: 'y2E0G9_vBNE'", "id: 'GEarPGa3Wso'")
    # Step 16: ByaMQ7Sopno -> HKeYzNAzvLE
    w_text = w_text.replace("id: 'ByaMQ7Sopno'", "id: 'HKeYzNAzvLE'")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(w_text)
    print(f"Updated {filepath} successfully.")

update_weight_loss_file('src/pages/weight-loss.astro')
update_weight_loss_file('src/pages/weight-loss/embed.astro')


# 5. Update src/components/VideoCard.astro with fallback onerror
with open('src/components/VideoCard.astro', encoding='utf-8') as f:
    card_text = f.read()

old_img_tag = """    <img
      src={thumbnail}
      alt={video.title}
      class="thumbnail-img"
      loading="lazy"
    />"""

new_img_tag = """    <img
      src={thumbnail}
      alt={video.title}
      class="thumbnail-img"
      loading="lazy"
      onerror={`this.onerror=null; this.src='https://i.ytimg.com/vi/${video.id}/hqdefault.jpg';`}
    />"""

if old_img_tag in card_text:
    card_text = card_text.replace(old_img_tag, new_img_tag, 1)
    with open('src/components/VideoCard.astro', 'w', encoding='utf-8') as f:
        f.write(card_text)
    print("Updated src/components/VideoCard.astro with onerror fallback.")
else:
    print("Note: old_img_tag format in VideoCard.astro didn't match exactly or was already updated.")

print("=== Video Pipeline Update Complete ===")

