import json, os, sys

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain"
conv = "c917a291-f072-4304-8a6a-e706feb550ad"
t_full = os.path.join(brain_dir, conv, ".system_generated", "logs", "transcript.jsonl")

if os.path.exists(t_full):
    with open(t_full, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            if any(k in line for k in ["胃食道逆流", "膽結石", "大腸息肉", "幽門桿菌", "急性腸胃炎", "腸躁症", "結腸激躁症"]):
                data = json.loads(line)
                content = data.get("content", "")
                if "clip_" in content or "part" in content or "片段" in content:
                    sys.stdout.buffer.write(f"Line {idx}: {content[:300]}\n\n".encode('utf-8'))
