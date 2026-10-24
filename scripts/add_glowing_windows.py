import re

with open('src/pages/island.astro', encoding='utf-8') as f:
    text = f.read()

# 在主屋與周圍小木屋上加上窗戶 (使用 nightGlowMaterial)
window_add_code = """      // 窗戶 (夜間亮燈)
      const winGeo = new THREE.BoxGeometry(0.18, 0.22, 0.04);
      const winFront = new THREE.Mesh(winGeo, nightGlowMaterial);
      winFront.position.set(0, HEX_HEIGHT + 0.35, 0.34);
      group.add(winFront);

      const winSide = new THREE.Mesh(winGeo, nightGlowMaterial);
      winSide.rotation.y = Math.PI / 2;
      winSide.position.set(0.39, HEX_HEIGHT + 0.35, 0);
      group.add(winSide);"""

# 檢查是否已在主屋後插入
if 'winFront.position.set(0, HEX_HEIGHT + 0.35, 0.34);' not in text:
    pos_roof = text.find('roof.castShadow = true;\n      group.add(roof);')
    if pos_roof != -1:
        text = text[:pos_roof + len('roof.castShadow = true;\n      group.add(roof);')] + "\n" + window_add_code + text[pos_roof + len('roof.castShadow = true;\n      group.add(roof);'):]
        print("ADDED_WINDOWS_TO_MAIN_HOUSE")

# 在周圍小房子上也加上小窗戶
mini_win_code = """        const miniWin = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.14, 0.03), nightGlowMaterial);
        miniWin.position.set(pos.x, HEX_HEIGHT + 0.22, pos.z + 0.25);
        miniWin.rotation.y = miniHouse.rotation.y;
        group.add(miniWin);"""

if 'const miniWin = new THREE.Mesh' not in text:
    pos_mini = text.find('miniRoof.castShadow = true;\n        group.add(miniRoof);')
    if pos_mini != -1:
        text = text[:pos_mini + len('miniRoof.castShadow = true;\n        group.add(miniRoof);')] + "\n" + mini_win_code + text[pos_mini + len('miniRoof.castShadow = true;\n        group.add(miniRoof);'):]
        print("ADDED_WINDOWS_TO_MINI_HOUSES")

with open('src/pages/island.astro', 'w', encoding='utf-8') as f:
    f.write(text)

print("HOUSE_WINDOWS_COMPLETE")
