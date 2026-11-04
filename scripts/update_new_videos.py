import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update src/data/videos.ts
videos_ts_path = 'src/data/videos.ts'
with open(videos_ts_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Ep 04 and Ep 05 IDs
content = content.replace("id: 'GmEV0iZ8Vg8'", "id: 'wdZhOWHTfY4'")
content = content.replace("https://www.youtube.com/watch?v=GmEV0iZ8Vg8", "https://www.youtube.com/watch?v=wdZhOWHTfY4")
content = content.replace("id: 'HUJ2tP2_Vq0'", "id: '4-ImmRUP7DU'")
content = content.replace("https://www.youtube.com/watch?v=HUJ2tP2_Vq0", "https://www.youtube.com/watch?v=4-ImmRUP7DU")

# Check if Ep 06 or Ep 07 already exists
if 'xosqt7or5gQ' not in content:
    ep06_ep07_block = """  {
    id: 'xosqt7or5gQ',
    title: '拋硬幣畫出的圖形居然神準？技術分析只是隨機錯覺！隨機漫步理論大解密｜《漫步華爾街》Ep 06',
    description: '你還在熬夜看線圖找頭肩頂？學者讓學生丟硬幣隨機畫出走勢圖，技術分析大師居然狂讚這是絕佳買點！普林斯頓傳奇經濟學大師墨基爾用科學實證戳破華爾街技術派的神話：股市根本沒有記憶，過去的圖形對未來走勢毫無預測能力。',
    category: '漫步華爾街',
    duration: '0:40',
    url: 'https://www.youtube.com/watch?v=xosqt7or5gQ',
    featured: true,
    order: 6,
    thumbnail: '/images/06、隨機漫步華爾街.webp',
    articleSlug: '/books/漫步華爾街/06-隨機漫步華爾街',
    articleTitle: '06、隨機漫步華爾街',
  },
  {
    id: '6RTwkSlGaXs',
    title: '九成主動基金竟慘輸大盤？地上百元鈔早被撿走！效率市場假說大解密｜《漫步華爾街》Ep 07',
    description: '華爾街頂尖分析師天天拜訪公司、算盡財報，為什麼長期績效居然打不過隨機挑選的一籃子股票？SPIVA 權威報告揭密：高達九成以上主動型基金長期慘輸大盤！這就是著名的「效率市場假說」：地上如果有百元美鈔早就被撿走了，所有公開情報早已即時反映在股價裡。',
    category: '漫步華爾街',
    duration: '0:40',
    url: 'https://www.youtube.com/watch?v=6RTwkSlGaXs',
    featured: true,
    order: 7,
    thumbnail: '/images/07、效率市場假說.webp',
    articleSlug: '/books/漫步華爾街/07-效率市場假說',
    articleTitle: '07、效率市場假說',
  },
"""
    # Insert before export const videos = [
    # Find position of Ep 05 and insert after it
    ep05_marker = "articleTitle: '05、投資分析解析',\n  },"
    if ep05_marker in content:
        content = content.replace(ep05_marker, ep05_marker + "\n" + ep06_ep07_block)
        print("Inserted Ep 06 and Ep 07 into videos.ts")
    else:
        print("Warning: ep05_marker not found, inserting at start of videos array")
        content = content.replace("export const videos: VideoItem[] = [", "export const videos: VideoItem[] = [\n" + ep06_ep07_block)

with open(videos_ts_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated videos.ts successfully")

# 2. Update Markdown frontmatters
updates = {
    '04': ('04-世紀資產泡沫.md', '04、世紀資產泡沫.md', 'wdZhOWHTfY4'),
    '05': ('05-投資分析解析.md', '05、投資分析解析.md', '4-ImmRUP7DU'),
    '06': ('06-隨機漫步華爾街.md', '06、隨機漫步華爾街.md', 'xosqt7or5gQ'),
    '07': ('07-效率市場假說.md', '07、效率市場假說.md', '6RTwkSlGaXs'),
}

books_dir = 'src/content/books/漫步華爾街'
vault_dir = r'G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街'

def update_file(filepath, video_id):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'videoId:' in c:
        c = re.sub(r'videoId:\s*["\']?[^"\']+["\']?', f'videoId: "{video_id}"', c)
    else:
        # Add after title or after first ---
        c = c.replace('---', f'---\nvideoId: "{video_id}"', 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated {filepath} with videoId: {video_id}")

for prefix, (site_fn, vault_fn, vid) in updates.items():
    update_file(os.path.join(books_dir, site_fn), vid)
    update_file(os.path.join(vault_dir, vault_fn), vid)

print("All videoIds updated successfully!")

