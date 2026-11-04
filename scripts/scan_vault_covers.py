import os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

vault = r"G:\我的雲端硬碟\衛教文章庫"
mds = glob.glob(os.path.join(vault, "**", "*.md"), recursive=True)

print(f"Total in {vault}: {len(mds)}")
no_cover = []
for m in mds:
    rel = os.path.relpath(m, vault)
    with open(m, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    has_cover = 'coverImage:' in content
    if not has_cover:
        no_cover.append(rel)

print(f"Total without cover: {len(no_cover)}")
for nc in no_cover:
    print(f"  - {nc}")
