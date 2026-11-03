import os
import glob
import re

print("=== Checking src/content/books ===")
missing_books = []
for p in sorted(glob.glob('src/content/books/**/*.md', recursive=True)):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else os.path.basename(p)
    cover = cover_m.group(1).strip() if cover_m else ''
    exists = os.path.exists(os.path.join('public/images', cover)) if cover else False
    if not cover or not exists:
        missing_books.append((p, title, cover, exists))
        print(f"Book: {p} | title: {title} | cover: {cover} (exists: {exists})")

print(f"\nTotal missing in books: {len(missing_books)}")

print("\n=== Checking src/content/posts ===")
missing_posts = []
for p in sorted(glob.glob('src/content/posts/**/*.md', recursive=True)):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?$', c, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else os.path.basename(p)
    cover = cover_m.group(1).strip() if cover_m else ''
    exists = os.path.exists(os.path.join('public/images', cover)) if cover else False
    if not cover or not exists:
        missing_posts.append((p, title, cover, exists))
        print(f"Post: {p} | title: {title} | cover: {cover} (exists: {exists})")

print(f"\nTotal missing in posts: {len(missing_posts)}")

# Also check Obsidian vault
env_path = '.env'
vault_path = ''
if os.path.exists(env_path):
    with open(env_path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('OBSIDIAN_VAULT_PATH='):
                vault_path = line.split('=', 1)[1].strip()

print(f"\nVault path from .env: {vault_path}")
if vault_path and os.path.exists(vault_path):
    missing_vault = []
    for root, dirs, files in os.walk(vault_path):
        for f in files:
            if f.endswith('.md'):
                fp = os.path.join(root, f)
                with open(fp, encoding='utf-8', errors='ignore') as fp_obj:
                    content = fp_obj.read()
                cover_m = re.search(r'^coverImage:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)
                title_m = re.search(r'^title:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)
                title = title_m.group(1).strip() if title_m else f[:-3]
                cover = cover_m.group(1).strip() if cover_m else ''
                exists = os.path.exists(os.path.join('public/images', cover)) if cover else False
                if not cover or not exists:
                    missing_vault.append((fp, title, cover))
    print(f"Total missing in Obsidian vault: {len(missing_vault)}")
    for item in missing_vault[:15]:
        print(f"  Vault: {item[0]} | title: {item[1]} | cover: {item[2]}")

