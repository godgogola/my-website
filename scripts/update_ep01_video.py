import os

# 1. Update src/data/videos.ts
with open('src/data/videos.ts', encoding='utf-8') as f:
    text = f.read()

text = text.replace("id: 'hlq0SK8saI0'", "id: 'll_paSBryWo'")
text = text.replace("https://www.youtube.com/watch?v=hlq0SK8saI0", "https://www.youtube.com/watch?v=ll_paSBryWo")

with open('src/data/videos.ts', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated src/data/videos.ts")

# 2. Update local book markdown
md_local = "src/content/books/漫步華爾街/01-磐石與空中樓閣.md"
if os.path.exists(md_local):
    with open(md_local, encoding='utf-8') as f:
        c = f.read()
    c = c.replace('videoId: "hlq0SK8saI0"', 'videoId: "ll_paSBryWo"')
    c = c.replace("videoId: 'hlq0SK8saI0'", "videoId: 'll_paSBryWo'")
    with open(md_local, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated {md_local}")

# 3. Update Obsidian vault book markdown
md_vault = r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\01、磐石與空中樓閣.md"
if os.path.exists(md_vault):
    with open(md_vault, encoding='utf-8') as f:
        vc = f.read()
    vc = vc.replace('videoId: "hlq0SK8saI0"', 'videoId: "ll_paSBryWo"')
    vc = vc.replace("videoId: 'hlq0SK8saI0'", "videoId: 'll_paSBryWo'")
    with open(md_vault, 'w', encoding='utf-8') as f:
        f.write(vc)
    print(f"Updated {md_vault}")

print("=== Successfully updated Ep.01 video to ll_paSBryWo ===")

