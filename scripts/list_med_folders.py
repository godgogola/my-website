import os, sys
base = r'c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工'
items = os.listdir(base)
topics = ['胃食道逆流', '膽結石', '大腸息肉', '幽門桿菌', '腸胃炎', '腸躁症', '結腸激躁症', '息肉', '胃', '腸', '膽']
found = set()
for it in items:
    for t in topics:
        if t in it:
            found.add(it)

for f in sorted(found):
    sys.stdout.buffer.write(f"{f}\n".encode('utf-8'))
