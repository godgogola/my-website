import sys
with open('c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/supplement_search.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sys.stdout.buffer.write(text[:3000].encode('utf-8'))
