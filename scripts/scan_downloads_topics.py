import os, sys

dl = r'C:\Users\X1 Yoga Gen7\Downloads'
mp4s = [f for f in os.listdir(dl) if f.endswith('.mp4')]

keywords = {
    "1_胃食道逆流": ["gerd", "逆流", "胃食道", "胃酸"],
    "2_膽結石": ["膽", "bile", "gall"],
    "3_大腸息肉": ["息肉", "polyp", "大腸息肉"],
    "4_幽門桿菌": ["幽門", "hp", "pylori", "h.pylori"],
    "5_急性腸胃炎": ["腸胃炎", "gi", "gastro"],
    "6_結腸激躁症": ["腸躁", "激躁", "ibs", "fodmap"]
}

for k, kw in keywords.items():
    matches = [f for f in mp4s if any(w in f.lower() for w in kw)]
    sys.stdout.buffer.write(f"=== {k} (found {len(matches)}) ===\n".encode('utf-8'))
    for m in sorted(matches)[:20]:
        sys.stdout.buffer.write(f"  {m}\n".encode('utf-8'))
