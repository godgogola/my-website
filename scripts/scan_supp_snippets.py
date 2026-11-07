import os, json, sys

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain"
conv = "c917a291-f072-4304-8a6a-e706feb550ad"
t_full = os.path.join(brain_dir, conv, ".system_generated", "logs", "transcript.jsonl")

found = []
if os.path.exists(t_full):
    with open(t_full, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            if any(k in line for k in ["補足片段1", "補足片段2", "補足片段3"]) and any(k in line for k in ["胃", "膽", "息肉", "幽門", "腸", "clip"]):
                data = json.loads(line)
                content = data.get("content", "")
                if len(content) > 100:
                    found.append((idx, content[:500]))

sys.stdout.buffer.write(f"Found {len(found)} snippets\n".encode('utf-8'))
for idx, s in found[:8]:
    sys.stdout.buffer.write(f"--- Line {idx} ---\n{s}\n\n".encode('utf-8'))
