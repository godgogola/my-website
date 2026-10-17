import os, re

updates = [
    {
        "post": "下消化道出血實證大腸息肉術後出血處理原則.md",
        "vault_sub": r"內視鏡檢查\【下消化道出血】【實證】大腸息肉術後出血處理原則.md",
        "cover": "【下消化道出血】【實證】大腸息肉術後出血處理原則.webp"
    },
    {
        "post": "內視鏡充氣量對食道界線判讀之影響.md",
        "vault_sub": r"內視鏡檢查\內視鏡充氣量對食道界線判讀之影響.md",
        "cover": "內視鏡充氣量對食道界線判讀之影響.webp"
    },
    {
        "post": "實證p-cab-vs-ppi.md",
        "vault_sub": r"藥物介紹\【實證】P-CAB vs PPI.md",
        "cover": "【實證】P-CAB vs PPI.webp"
    }
]

def update_fm(path, cover):
    if not os.path.exists(path):
        print(f"Not found: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "coverImage:" in content:
        content = re.sub(r'coverImage:\s*.*', f'coverImage: "{cover}"', content)
    else:
        content = re.sub(r'(---\n)', f'\\1coverImage: "{cover}"\n', content, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {os.path.basename(path)}")

posts_dir = r"C:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\content\posts"
vault_dir = r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫"

for u in updates:
    update_fm(os.path.join(posts_dir, u["post"]), u["cover"])
    update_fm(os.path.join(vault_dir, u["vault_sub"]), u["cover"])

print("Frontmatters updated successfully!")
