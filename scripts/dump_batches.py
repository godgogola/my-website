import json

with open('scripts/21lessons_prompts.json', 'r', encoding='utf-8') as f:
    prompts = json.load(f)

print('=== BATCH 1 ===')
for i in range(4):
    p = prompts[i]
    print(f"Image {i+1}:")
    print(f"Title: {p['title']}")
    print(f"ImageName: {p['imageName']}")
    print(f"Prompt:\n{p['prompt']}\n")

print('=== BATCH 2 ===')
for i in range(4, 8):
    p = prompts[i]
    print(f"Image {i-3}:")
    print(f"Title: {p['title']}")
    print(f"ImageName: {p['imageName']}")
    print(f"Prompt:\n{p['prompt']}\n")

