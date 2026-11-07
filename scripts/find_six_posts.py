import glob, sys

posts = glob.glob('src/content/posts/**/*.md', recursive=True)
targets = ['胃食道逆流', '膽結石', '大腸息肉', '幽門桿菌', '急性腸胃炎', '結腸激躁症']

for t in targets:
    sys.stdout.buffer.write(f"=== Target: {t} ===\n".encode('utf-8'))
    for p in posts:
        if t in p:
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            first_lines = c.split('\n')[:8]
            sys.stdout.buffer.write(f"  {p}\n".encode('utf-8'))
            for l in first_lines:
                sys.stdout.buffer.write(f"    {l}\n".encode('utf-8'))
