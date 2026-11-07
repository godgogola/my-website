import sys
for p in ['c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/find_supp_details.py', 'c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/check_ten_selected.py']:
    sys.stdout.buffer.write(f"=== {p} ===\n".encode('utf-8'))
    try:
        with open(p, 'r', encoding='utf-8') as f:
            sys.stdout.buffer.write(f.read().encode('utf-8'))
    except Exception as e:
        sys.stdout.buffer.write(str(e).encode('utf-8'))
    sys.stdout.buffer.write(b"\n\n")
