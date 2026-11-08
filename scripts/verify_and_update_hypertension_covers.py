import os
import glob
import re

targets = [
    "S-ABCDE 高血壓生活型態調整",
    "最新高血壓診斷分級與 722 量測準則",
    "次發性高血壓",
    "長期血壓控制不良的併發症",
    "高血壓藥物介紹",
    "高血壓藥物在一般族群及共病族群的選擇",
    "高血壓藥物效果",
]

# Check Obsidian vault first
vault_dir = r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫"
posts_dir = r"src\content\posts"

for base_dir, label in [(vault_dir, "Obsidian Vault"), (posts_dir, "Website Posts")]:
    print(f"\nChecking {label} in {base_dir}...")
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} does not exist.")
        continue
    for root, _, files in os.walk(base_dir):
        for f in files:
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except Exception:
                continue
            
            for t in targets:
                if f"title: \"{t}\"" in content or f"title: '{t}'" in content or f"title: {t}" in content:
                    # Check coverImage
                    match = re.search(r'coverImage:\s*["\']?(.*?)["\']?\s*\n', content)
                    current_cover = match.group(1) if match else "None"
                    expected_cover = f"{t}.webp"
                    print(f"  [{t}] -> coverImage: '{current_cover}' (expected: '{expected_cover}')")
                    
                    if current_cover != expected_cover:
                        print(f"    Updating {path}...")
                        if match:
                            new_content = re.sub(r'coverImage:\s*["\']?.*?["\']?\s*\n', f'coverImage: "{expected_cover}"\n', content, count=1)
                        else:
                            new_content = re.sub(r'(---\n)', f'---\ncoverImage: "{expected_cover}"\n', content, count=1)
                        with open(path, 'w', encoding='utf-8') as file:
                            file.write(new_content)
                        print("    Updated!")

