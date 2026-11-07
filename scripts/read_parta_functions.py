import sys
with open('c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/remaster_partA_four.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(450, min(580, len(lines))):
    sys.stdout.buffer.write(lines[i].encode('utf-8'))
