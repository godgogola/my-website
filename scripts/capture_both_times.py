import subprocess, os, time

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_path):
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

target_night = r'C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\260dc583-24b5-4191-9bc4-a8d043ef3d41\island_night_milkyway_verified.png'
target_dusk = r'C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\260dc583-24b5-4191-9bc4-a8d043ef3d41\island_dusk_sun_clouds_verified.png'

# 1. 截取星夜場景
cmd_night = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--screenshot=' + target_night,
    '--virtual-time-budget=5000',
    'http://localhost:4321/island?time=night'
]
subprocess.run(cmd_night, capture_output=True)
print('Night image size:', os.path.getsize(target_night) if os.path.exists(target_night) else 0)

# 2. 截取暮霞夕陽場景
cmd_dusk = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--screenshot=' + target_dusk,
    '--virtual-time-budget=5000',
    'http://localhost:4321/island?time=dusk'
]
subprocess.run(cmd_dusk, capture_output=True)
print('Dusk image size:', os.path.getsize(target_dusk) if os.path.exists(target_dusk) else 0)
