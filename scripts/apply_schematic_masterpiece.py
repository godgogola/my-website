import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# ── 1. 替換 setupLightingAndCelestial, create3DSunOnLeft, create3DMoonOnRight, createBirdFlock, createCinematicSkyDome, createCosmicStarfield ──
# 我們將其替換為超高解析度雙景畫卷全景天幕系統

sky_replacement = """  // ══════════════════════════════════════════════════════════════════════
  // 4. 系統一：極致 4K 電影級雙景天幕 (左側金金日落霞光 × 右側浩瀚銀河明月)
  // ══════════════════════════════════════════════════════════════════════
  let skyDomeMesh;
  const FEATURED_ISLANDS = new Set([
    'stomach', 'colon', 'endoscopy', 'liver', 'hypertension',
    'drugs', 'weight-loss', 'glucose-goddess', 'wealth-ladder',
    'random-walk', 'investing-pillars', 'die-with-zero'
  ]);

  function setupLightingAndCelestial() {
    // 1. 全球柔和環境天光 (兼顧左暖右冷色溫)
    ambientLight = new THREE.AmbientLight(0xfff5ea, 0.92);
    lightsGroup.add(ambientLight);

    hemiLight = new THREE.HemisphereLight(0xffedd5, 0x1e293b, 0.85);
    lightsGroup.add(hemiLight);

    // 2. 左側金色夕陽主平行光
    dirLight = new THREE.DirectionalLight(0xffe4b5, 2.2);
    dirLight.position.set(-36, 22, 16);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 5;
    dirLight.shadow.camera.far = 120;
    const d = 34;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    dirLight.shadow.bias = -0.0003;
    lightsGroup.add(dirLight);

    // 3. 右側銀河明月皎潔冷光 (在海面形成波光月影)
    moonLight = new THREE.DirectionalLight(0xbfdbfe, 1.45);
    moonLight.position.set(38, 26, 16);
    moonLight.castShadow = false;
    lightsGroup.add(moonLight);

    // 4. 建立 4K 電影級全景畫卷天幕 (100% 示意圖規格)
    createMasterpieceSkyDome();
  }

  // 繪製 4096x2048 頂級全景雙景天幕 (左夕陽日冕雲霞飛鳥，右深空銀河繁星滿月)
  function createMasterpieceSkyDome() {
    const canvas = document.createElement('canvas');
    canvas.width = 4096;
    canvas.height = 2048;
    const ctx = canvas.getContext('2d');

    // 1. 鋪設左右漸變宇宙大氣底色
    const baseGrad = ctx.createLinearGradient(0, 0, 4096, 0);
    baseGrad.addColorStop(0.0, '#3b1828'); // 左側高空暮紫
    baseGrad.addColorStop(0.25, '#2e122b');
    baseGrad.addColorStop(0.48, '#0b132b'); // 中央過渡深青
    baseGrad.addColorStop(0.70, '#040816'); // 右側宇宙深黑
    baseGrad.addColorStop(1.0, '#020510');
    ctx.fillStyle = baseGrad;
    ctx.fillRect(0, 0, 4096, 2048);

    // 2. 左半側：耀眼夕陽晚霞、金黃地平線光芒與暖橙暮色
    const sunsetGrad = ctx.createRadialGradient(850, 1150, 40, 850, 1150, 1450);
    sunsetGrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');  // 白金日核
    sunsetGrad.addColorStop(0.08, 'rgba(255, 243, 176, 0.98)'); // 金黃日冕
    sunsetGrad.addColorStop(0.22, 'rgba(251, 191, 36, 0.92)');  // 燦爛金橙
    sunsetGrad.addColorStop(0.42, 'rgba(249, 115, 22, 0.75)');  // 溫暖赤橙
    sunsetGrad.addColorStop(0.65, 'rgba(225, 29, 72, 0.45)');   // 暮色玫瑰
    sunsetGrad.addColorStop(0.88, 'rgba(124, 58, 237, 0.18)');  // 暮紫流霞
    sunsetGrad.addColorStop(1.0, 'rgba(0, 0, 0, 0.0)');
    ctx.fillStyle = sunsetGrad;
    ctx.fillRect(0, 0, 2400, 2048);

    // 地平線強烈金光光弧
    const horizonGrad = ctx.createLinearGradient(0, 1000, 0, 1300);
    horizonGrad.addColorStop(0.0, 'rgba(255, 240, 180, 0.85)');
    horizonGrad.addColorStop(0.4, 'rgba(251, 146, 60, 0.65)');
    horizonGrad.addColorStop(1.0, 'rgba(251, 146, 60, 0.0)');
    ctx.fillStyle = horizonGrad;
    ctx.fillRect(0, 950, 2000, 350);

    // 飄逸的金色夕陽晚霞卷雲 (Wispy Cirrus Clouds)
    ctx.save();
    ctx.filter = 'blur(16px)';
    ctx.fillStyle = 'rgba(254, 215, 170, 0.35)';
    [[200, 850, 600, 45], [500, 780, 750, 55], [350, 920, 500, 40], [1000, 720, 650, 50], [800, 880, 700, 45]].forEach(([cx, cy, cw, ch]) => {
      ctx.beginPath();
      ctx.ellipse(cx, cy, cw, ch, -0.05, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();

    // 夕陽中的黑色飛鳥剪影群 (Flock of silhouette birds)
    ctx.fillStyle = '#1c1917';
    [[920, 820, 1.2], [960, 805, 0.95], [890, 840, 0.85], [1010, 835, 1.1], [1050, 810, 0.8],
     [860, 860, 0.75], [980, 860, 0.9], [935, 790, 0.7], [1090, 830, 0.75], [840, 880, 0.65]].forEach(([bx, by, s]) => {
      ctx.beginPath();
      ctx.moveTo(bx - 14 * s, by - 6 * s);
      ctx.quadraticCurveTo(bx - 7 * s, by + 4 * s, bx, by);
      ctx.quadraticCurveTo(bx + 7 * s, by + 4 * s, bx + 14 * s, by - 6 * s);
      ctx.quadraticCurveTo(bx + 7 * s, by + 1 * s, bx, by + 2 * s);
      ctx.quadraticCurveTo(bx - 7 * s, by + 1 * s, bx - 14 * s, by - 6 * s);
      ctx.fill();
    });

    // 3. 右半側：壯麗高密度銀河系星雲帶 (Milky Way Nebula Arc)
    ctx.save();
    ctx.translate(3050, 1024);
    ctx.rotate(-0.58); // 斜貫星空角度

    // 銀河多層柔光星雲輝光
    const nebulaGrad1 = ctx.createLinearGradient(-1500, 0, 1500, 0);
    nebulaGrad1.addColorStop(0.0, 'rgba(147, 51, 234, 0.0)');
    nebulaGrad1.addColorStop(0.35, 'rgba(168, 85, 247, 0.28)');
    nebulaGrad1.addColorStop(0.5, 'rgba(236, 72, 153, 0.35)');
    nebulaGrad1.addColorStop(0.65, 'rgba(96, 165, 250, 0.26)');
    nebulaGrad1.addColorStop(1.0, 'rgba(59, 130, 246, 0.0)');

    ctx.filter = 'blur(60px)';
    ctx.fillStyle = nebulaGrad1;
    ctx.fillRect(-1500, -220, 3000, 440);

    // 銀河核心明亮白粉星塵
    const nebulaGrad2 = ctx.createLinearGradient(-1200, 0, 1200, 0);
    nebulaGrad2.addColorStop(0.2, 'rgba(255, 255, 255, 0.0)');
    nebulaGrad2.addColorStop(0.5, 'rgba(255, 240, 255, 0.42)');
    nebulaGrad2.addColorStop(0.8, 'rgba(255, 255, 255, 0.0)');
    ctx.filter = 'blur(35px)';
    ctx.fillStyle = nebulaGrad2;
    ctx.fillRect(-1200, -90, 2400, 180);
    ctx.restore();

    // 4. 右側浩瀚繁星 (3,000+ 顆高密度大小星辰)
    const seed = 42;
    let rnd = seed;
    function pseudoRandom() {
      rnd = (rnd * 9301 + 49297) % 233280;
      return rnd / 233280;
    }

    for (let i = 0; i < 3200; i++) {
      const sx = 2000 + pseudoRandom() * 2050;
      const sy = pseudoRandom() * 1250;
      const sr = pseudoRandom() * 1.8 + 0.4;
      const op = pseudoRandom() * 0.85 + 0.15;

      const starType = pseudoRandom();
      if (starType < 0.6) {
        ctx.fillStyle = `rgba(255, 255, 255, ${op})`;
      } else if (starType < 0.85) {
        ctx.fillStyle = `rgba(191, 219, 254, ${op})`; // 幽藍星芒
      } else {
        ctx.fillStyle = `rgba(254, 240, 138, ${op})`; // 金黃星芒
      }

      ctx.beginPath();
      ctx.arc(sx, sy, sr, 0, Math.PI * 2);
      ctx.fill();

      // 部分亮星帶有十字微星芒
      if (sr > 1.8 && pseudoRandom() < 0.25) {
        ctx.strokeStyle = `rgba(255, 255, 255, ${op * 0.7})`;
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.moveTo(sx - sr * 3.5, sy); ctx.lineTo(sx + sr * 3.5, sy);
        ctx.moveTo(sx, sy - sr * 3.5); ctx.lineTo(sx, sy + sr * 3.5);
        ctx.stroke();
      }
    }

    // 5. 右上方立體逼真皎潔滿月 (Full Moon with Craters & Lunar Halo)
    const mx = 3280, my = 360, mr = 88;

    // 月亮外圍幽藍銀白月光暈輪 (Lunar Halo)
    const haloGrad = ctx.createRadialGradient(mx, my, mr * 0.8, mx, my, mr * 3.6);
    haloGrad.addColorStop(0.0, 'rgba(219, 234, 254, 0.65)');
    haloGrad.addColorStop(0.35, 'rgba(147, 197, 253, 0.32)');
    haloGrad.addColorStop(0.7, 'rgba(96, 165, 250, 0.12)');
    haloGrad.addColorStop(1.0, 'rgba(0, 0, 0, 0.0)');
    ctx.fillStyle = haloGrad;
    ctx.beginPath();
    ctx.arc(mx, my, mr * 3.6, 0, Math.PI * 2);
    ctx.fill();

    // 月面本體 (明亮米白底色)
    const moonBodyGrad = ctx.createRadialGradient(mx - mr * 0.25, my - mr * 0.25, mr * 0.1, mx, my, mr);
    moonBodyGrad.addColorStop(0.0, '#ffffff');
    moonBodyGrad.addColorStop(0.75, '#f1f5f9');
    moonBodyGrad.addColorStop(1.0, '#cbd5e1');
    ctx.fillStyle = moonBodyGrad;
    ctx.beginPath();
    ctx.arc(mx, my, mr, 0, Math.PI * 2);
    ctx.fill();

    // 繪製月海暗斑地貌 (Lunar Maria)
    ctx.save();
    ctx.beginPath();
    ctx.arc(mx, my, mr, 0, Math.PI * 2);
    ctx.clip(); // 限制在月球內部

    ctx.fillStyle = 'rgba(148, 163, 184, 0.55)';
    [
      [mx - 22, my - 16, 26], [mx + 18, my - 24, 22], [mx - 32, my + 15, 28],
      [mx + 5, my + 26, 24], [mx + 34, my + 8, 20], [mx - 5, my - 38, 16]
    ].forEach(([cx, cy, cr]) => {
      ctx.beginPath();
      ctx.arc(cx, cy, cr, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();

    // 6. 大氣地平線光弧 (Atmospheric limb glow)
    const limbGrad = ctx.createLinearGradient(0, 1010, 0, 1050);
    limbGrad.addColorStop(0.0, 'rgba(255, 255, 255, 0.55)');
    limbGrad.addColorStop(0.5, 'rgba(96, 165, 250, 0.35)');
    limbGrad.addColorStop(1.0, 'rgba(0, 0, 0, 0.0)');
    ctx.fillStyle = limbGrad;
    ctx.fillRect(0, 1010, 4096, 40);

    // 建立 Three.js Texture
    const skyTex = new THREE.CanvasTexture(canvas);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyTex.wrapS = THREE.ClampToEdgeWrapping;
    skyTex.wrapT = THREE.ClampToEdgeWrapping;

    const skyGeo = new THREE.SphereGeometry(180, 64, 32);
    const skyMat = new THREE.MeshBasicMaterial({
      map: skyTex,
      side: THREE.BackSide,
      depthWrite: false
    });

    skyDomeMesh = new THREE.Mesh(skyGeo, skyMat);
    scene.add(skyDomeMesh);
  }

  function createCosmicStarfield() {
    // 4K Masterpiece SkyDome 已完整內建超高解析度銀河、星空、日落與滿月
  }
"""

# 我們把 setupLightingAndCelestial 到 createCosmicStarfield 的整段取代掉
pattern = r"let skyDomeMesh, sunMeshGroup, moonMeshGroup;[\s\S]*?function createCosmicStarfield\(\) \{[\s\S]*?scene\.add\(milkyWayPoints\);\s*\}"

if re.search(pattern, code):
    code = re.sub(pattern, sky_replacement, code)
    print("Replaced Sky & Lighting with Masterpiece SkyDome successfully.")
else:
    print("Pattern for SkyDome not found, searching alternative...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)
