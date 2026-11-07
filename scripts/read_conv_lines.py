import json, os, sys

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain"
conv = "c917a291-f072-4304-8a6a-e706feb550ad"
t_full = os.path.join(brain_dir, conv, ".system_generated", "logs", "transcript.jsonl")

if os.path.exists(t_full):
    with open(t_full, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            if 1340 <= idx <= 1400:
                try:
                    data = json.loads(line)
                    c = data.get("content", "")
                    if any(w in c for w in ["Canva", "下載", "片段", "部", "清單", "補足"]):
                        sys.stdout.buffer.write(f"Line {idx}: {c[:250]}\n\n".encode('utf-8'))
                except:
                    pass
