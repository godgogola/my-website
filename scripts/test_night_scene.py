import subprocess, os, time

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_path):
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

target_night = r'C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\260dc583-24b5-4191-9bc4-a8d043ef3d41\island_night_milkyway_moon.png'

# 注入點擊星夜按鈕的 JS
js_click_night = """
const btn = document.querySelector('[data-time="night"]');
if (btn) btn.click();
"""

cmd_night = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--screenshot=' + target_night,
    '--virtual-time-budget=6000',
    'http://localhost:4321/island'
]

# 我們寫一個帶有 DOM 點擊的 python playwright 或簡單的頁面參數
print("Testing capture...")
