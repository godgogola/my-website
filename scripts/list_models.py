import os
import requests

api_key = ''
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('GEMINI_API_KEY='):
            api_key = line.strip().split('=', 1)[1]

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
res = requests.get(url)
data = res.json()
print("Total models:", len(data.get('models', [])))
for m in data.get('models', []):
    name = m.get('name')
    methods = m.get('supportedGenerationMethods')
    if 'image' in name.lower() or 'predict' in str(methods).lower():
        print(name, methods)

