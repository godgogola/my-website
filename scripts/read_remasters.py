import sys
for p in ['c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/remaster_partA_four.py', 'c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/remaster_partB_six.py']:
    sys.stdout.buffer.write(f"=== {p} ===\n".encode('utf-8'))
    try:
        with open(p, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for l in lines[:60]:
                sys.stdout.buffer.write(l.encode('utf-8'))
    except Exception as e:
        sys.stdout.buffer.write(str(e).encode('utf-8'))
    sys.stdout.buffer.write(b"\n\n")
