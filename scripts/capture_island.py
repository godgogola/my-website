import subprocess, os, sys, tempfile, shutil

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome):
    chrome = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

query = sys.argv[1] if len(sys.argv) > 1 else '?a=1'
name = sys.argv[2] if len(sys.argv) > 2 else 'island_shot'
budget = sys.argv[3] if len(sys.argv) > 3 else '9000'
out = os.path.join(r'C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\260dc583-24b5-4191-9bc4-a8d043ef3d41', name + '.png')
if os.path.exists(out):
    os.remove(out)
prof = tempfile.mkdtemp(prefix='chrome_prof_')
try:
    subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
                    '--window-size=1600,900', '--screenshot=' + out, '--virtual-time-budget=' + budget,
                    'http://localhost:4321/island' + query], capture_output=True, timeout=60)
except subprocess.TimeoutExpired:
    print('timeout')
shutil.rmtree(prof, ignore_errors=True)
print(out, os.path.exists(out))
