import os
import re

astro_file = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(astro_file, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read island.astro, length: {len(content)}")
