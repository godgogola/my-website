import json, os, sys

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain"
conv = "c917a291-f072-4304-8a6a-e706feb550ad"
t_full = os.path.join(brain_dir, conv, ".system_generated", "logs", "transcript_full.jsonl")

if os.path.exists(t_full):
    with open(t_full, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            if idx == 1696:
                data = json.loads(line)
                sys.stdout.buffer.write(data.get("content", "")[:2000].encode('utf-8'))
                break
