import subprocess

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--enable-logging=stderr',
    '--v=1',
    '--virtual-time-budget=6000',
    'http://localhost:4321/island'
]
res = subprocess.run(cmd, capture_output=True)
stderr_text = res.stderr.decode('utf-8', errors='ignore')
with open('scripts/browser_errors.txt', 'w', encoding='utf-8') as f:
    for line in stderr_text.splitlines():
        if any(k in line.lower() for k in ['uncaught', 'error', 'console', 'syntax', 'reference']):
            f.write(line + '\n')

print("DONE_COLLECTING_ERRORS")
