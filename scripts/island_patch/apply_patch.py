import re, sys, io
sys.stdout.reconfigure(encoding='utf-8')

P = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"
N = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\scripts\island_patch\new_systems.js"

raw = open(P, 'r', encoding='utf-8', newline='').read()
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n')
new_code = open(N, 'r', encoding='utf-8', newline='').read().replace('\r\n', '\n')

def must_replace(src, old, new, count=1):
    assert src.count(old) >= 1, 'NOT FOUND: ' + old[:60]
    return src.replace(old, new, count)

# 1. remove old createLowPolyClouds block (header + function)
a = s.index('  function createLowPolyClouds() {')
hdr = s.rfind('  // ══', 0, a)
hdr = s.rfind('  // ══', 0, hdr) if s[hdr:a].count('// ══') < 2 else hdr
# header block = two ═ lines + title; find the first ═ line of the header block
h1 = s.rfind('\n', 0, a)
blk_start = s.index('  // ══', s.rfind('  // 系統 3', 0, a) - 200)
# walk back to the ═ line immediately before "系統 3"
t3 = s.rfind('  // 系統 3', 0, a)
blk_start = s.rfind('  // ══', 0, t3)
t4 = s.index('  // 系統 4', a)
blk_end = s.rfind('  // ══', 0, t4)
s = s[:blk_start] + s[blk_end:]

# 2. bridges
f = s.index('    BRIDGE_PAIRS.forEach(([idA, idB]) => {')
sec8 = s.index('  // 8. 沿大氣層升起之跨領域能量光索')
sec8_hdr = s.rfind('  // ══', 0, sec8)
close_fn = s.rfind('\n  }\n', 0, sec8_hdr) + 1  # index of the "  }" line start
s = s[:f] + '    buildArchBridges(BRIDGE_PAIRS);\n' + s[close_fn:close_fn + len('  }\n')] + '\n' + new_code + s[close_fn + len('  }\n'):]

# 3. init calls
s = must_replace(s, "    // createLowPolyClouds(); // 停用低空漂浮雲塊，徹底消除遮擋島嶼的霧氣與灰白厚雲\n",
    "    createMountainRing();     // 3a. 環湖群山 + 松林 + 山坡小屋\n    createIslets();           // 3b. 湖心沙洲與燈塔\n    createLowPolyClouds();    // 3c. 群山之上的雲海\n    createBoats();            // 3d. 湖上帆船\n")

# 4. cloud update
c0 = s.index('    // 2. 雲朵慢速飄移')
c1 = s.index('\n    }\n', c0) + len('\n    }\n')
s = s[:c0] + '    // 2. 雲海漂移與湖上帆船\n    updateCloudDrift(elapsedTime);\n    updateBoats(elapsedTime);\n' + s[c1:]

# 5. HUD button
r0 = s.index('id="resetCamBtn"')
r1 = s.index('</button>', r0) + len('</button>')
btn = ('\n\n        <button class="hud-action-btn" id="birdViewBtn" title="鳥瞰：升空俯視環湖群山，並緩慢環繞">\n'
       '          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"></path><circle cx="12" cy="12" r="3"></circle></svg>\n'
       '          <span class="btn-text">鳥瞰</span>\n'
       '        </button>')
s = s[:r1] + btn + s[r1:]

# 6. setupUI listener
s = must_replace(s, "    document.getElementById('resetCamBtn').addEventListener('click', resetView);\n",
    "    document.getElementById('resetCamBtn').addEventListener('click', resetView);\n\n"
    "    // 鳥瞰模式 (升空 + 緩慢環繞；使用者一拖曳即停止自轉)\n"
    "    document.getElementById('birdViewBtn').addEventListener('click', () => setBirdView(!isBirdView));\n"
    "    controls.addEventListener('start', () => { if (isBirdView) controls.autoRotate = false; });\n")

# 7. resetView / focusIsland
s = must_replace(s, "  function resetView() {\n    activeIsland = null;\n", "  function resetView() {\n    exitBirdViewSilently();\n    activeIsland = null;\n")
s = must_replace(s, "  function focusIsland(islandId) {\n", "  function focusIsland(islandId) {\n    exitBirdViewSilently();\n")

# 8. flight hooks
s = must_replace(s, "    isFlightActive = true;\n    controls.enabled = false;\n", "    isFlightActive = true;\n    controls.enabled = false;\n    controls.autoRotate = false;\n")
s = must_replace(s, "      isFlightActive = false;\n      controls.enabled = true;\n    }\n", "      isFlightActive = false;\n      controls.enabled = true;\n      if (isBirdView) { controls.autoRotate = true; controls.autoRotateSpeed = 0.6; }\n    }\n")

if crlf:
    s = s.replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(s)
print('patched OK')
