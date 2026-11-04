import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\1e943372-efc6-4031-9eed-12718942505c\.system_generated\logs\transcript.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        c = d.get('content')
        if c and 'Prompt:' in str(c):
            print(c)
        tc = d.get('tool_calls')
        if tc:
            for item in tc:
                print('TOOL:', item)

