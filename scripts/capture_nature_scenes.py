import subprocess, os, time

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_path):
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

target_day = r'C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\260dc583-24b5-4191-9bc4-a8d043ef3d41\island_final_day_clean.png'

cmd_day = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--screenshot=' + target_day,
    '--virtual-time-budget=5000',
    'http://localhost:4321/island'
]
subprocess.run(cmd_day, capture_output=True)
print('Day image size:', os.path.getsize(target_day) if os.path.exists(target_day) else 0)
