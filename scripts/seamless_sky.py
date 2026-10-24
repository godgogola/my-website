import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 替換 createMasterpieceSkyDome 為完全無縫 (Seamless 360) 畫卷：
# x=0, 4096: 深邃星空背影
# x=1024: 燦爛金色夕陽晚霞 (剛好位於畫面左側 -X)
# x=3072: 皎潔滿月與銀河星雲 (剛好位於畫面右側 +X)

new_sky_function = """  // 繪製 4096x2048 頂級全景雙景天幕 (無縫 360° 環景：左夕陽日冕雲霞飛鳥，右深空銀河繁星滿月)
  function createMasterpieceSkyDome() {
    const canvas = document.createElement('canvas');
    canvas.width = 4096;
    canvas.height = 2048;
    const ctx = canvas.getContext('2d');

    // 1. 底色：深邃午夜深空 (兩端完全平滑閉合，無任何裁切線)
    ctx.fillStyle = '#030714';
    ctx.fillRect(0, 0, 4096, 2048);

    // 2. 左半側 (以 x=1024 為中心)：燦爛夕陽晚霞
    const sunCenterX = 1024;
    const sunCenterY = 1180;

    // 廣角日落大氣輝光 (金黃 -> 暖橙 -> 暮紫 -> 宇宙黑)
    const sunsetGrad = ctx.createRadialGradient(sunCenterX, sunCenterY, 30, sunCenterX, sunCenterY, 1500);
    sunsetGrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');  // 白金日核
    sunsetGrad.addColorStop(0.07, 'rgba(255, 245, 180, 0.98)'); // 金黃日冕
    sunsetGrad.addColorStop(0.20, 'rgba(251, 191, 36, 0.92)');  // 燦爛金橙
    sunsetGrad.addColorStop(0.42, 'rgba(249, 115, 22, 0.72)');  // 暖橙晚霞
    sunsetGrad.addColorStop(0.65, 'rgba(190, 24, 93, 0.42)');   // 暮色玫瑰
    sunsetGrad.addColorStop(0.85, 'rgba(88, 28, 135, 0.15)');   // 暮紫流霞
    sunsetGrad.addColorStop(1.0, 'rgba(3, 7, 20, 0.0)');
    ctx.fillStyle = sunsetGrad;
    ctx.fillRect(0, 0, 2400, 2048);

    // 地平線柔金霞光帶
    const horizonGrad = ctx.createLinearGradient(0, 1020, 0, 1350);
    horizonGrad.addColorStop(0.0, 'rgba(255, 240, 190, 0.75)');
    horizonGrad.addColorStop(0.45, 'rgba(251, 146, 60, 0.55)');
    horizonGrad.addColorStop(1.0, 'rgba(251, 146, 60, 0.0)');
    ctx.fillStyle = horizonGrad;
    ctx.fillRect(100, 980, 1900, 370);

    // 金色夕陽晚霞卷雲 (Wispy Clouds)
    ctx.save();
    ctx.filter = 'blur(16px)';
    ctx.fillStyle = 'rgba(254, 215, 170, 0.38)';
    [
      [550, 880, 500, 42], [900, 820, 650, 48], [1300, 860, 580, 44],
      [750, 940, 480, 36], [1150, 920, 520, 40]
    ].forEach(([cx, cy, cw, ch]) => {
      ctx.beginPath();
      ctx.ellipse(cx, cy, cw, ch, -0.04, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();

    // 夕陽中的黑色飛鳥剪影群 (Flock of silhouette birds)
    ctx.fillStyle = '#18181b';
    [
      [1100, 850, 1.25], [1145, 835, 0.98], [1070, 870, 0.88], [1195, 865, 1.1],
      [1230, 840, 0.82], [1040, 890, 0.76], [1165, 890, 0.92], [1120, 820, 0.72]
    ].forEach(([bx, by, s]) => {
      ctx.beginPath();
      ctx.moveTo(bx - 14 * s, by - 6 * s);
      ctx.quadraticCurveTo(bx - 7 * s, by + 4 * s, bx, by);
      ctx.quadraticCurveTo(bx + 7 * s, by + 4 * s, bx + 14 * s, by - 6 * s);
      ctx.quadraticCurveTo(bx + 7 * s, by + 1 * s, bx, by + 2 * s);
      ctx.quadraticCurveTo(bx - 7 * s, by + 1 * s, bx - 14 * s, by - 6 * s);
      ctx.fill();
    });

    // 3. 右半側 (以 x=3072 為中心)：壯麗高密度銀河系星雲帶 (Milky Way Nebula Arc)
    ctx.save();
    ctx.translate(3072, 1024);
    ctx.rotate(-0.55);

    // 銀河多層柔光星雲輝光
    const nebulaGrad1 = ctx.createLinearGradient(-1600, 0, 1600, 0);
    nebulaGrad1.addColorStop(0.0, 'rgba(147, 51, 234, 0.0)');
    nebulaGrad1.addColorStop(0.35, 'rgba(168, 85, 247, 0.32)');
    nebulaGrad1.addColorStop(0.5, 'rgba(236, 72, 153, 0.38)');
    nebulaGrad1.addColorStop(0.65, 'rgba(96, 165, 250, 0.28)');
    nebulaGrad1.addColorStop(1.0, 'rgba(59, 130, 246, 0.0)');

    ctx.filter = 'blur(60px)';
    ctx.fillStyle = nebulaGrad1;
    ctx.fillRect(-1600, -240, 3200, 480);

    // 銀河核心明亮白粉星塵
    const nebulaGrad2 = ctx.createLinearGradient(-1300, 0, 1300, 0);
    nebulaGrad2.addColorStop(0.2, 'rgba(255, 255, 255, 0.0)');
    nebulaGrad2.addColorStop(0.5, 'rgba(255, 240, 255, 0.45)');
    nebulaGrad2.addColorStop(0.8, 'rgba(255, 255, 255, 0.0)');
    ctx.filter = 'blur(35px)';
    ctx.fillStyle = nebulaGrad2;
    ctx.fillRect(-1300, -100, 2600, 200);
    ctx.restore();

    // 4. 右側浩瀚繁星 (3,000+ 顆高密度大小星辰)
    const seed = 42;
    let rnd = seed;
    function pseudoRandom() {
      rnd = (rnd * 9301 + 49297) % 233280;
      return rnd / 233280;
    }

    for (let i = 0; i < 3400; i++) {
      const sx = 2100 + pseudoRandom() * 1950;
      const sy = pseudoRandom() * 1350;
      const sr = pseudoRandom() * 1.9 + 0.4;
      const op = pseudoRandom() * 0.88 + 0.12;

      const starType = pseudoRandom();
      if (starType < 0.6) {
        ctx.fillStyle = `rgba(255, 255, 255, ${op})`;
      } else if (starType < 0.85) {
        ctx.fillStyle = `rgba(191, 219, 254, ${op})`;
      } else {
        ctx.fillStyle = `rgba(254, 240, 138, ${op})`;
      }

      ctx.beginPath();
      ctx.arc(sx, sy, sr, 0, Math.PI * 2);
      ctx.fill();

      if (sr > 1.85 && pseudoRandom() < 0.28) {
        ctx.strokeStyle = `rgba(255, 255, 255, ${op * 0.75})`;
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.moveTo(sx - sr * 3.6, sy); ctx.lineTo(sx + sr * 3.6, sy);
        ctx.moveTo(sx, sy - sr * 3.6); ctx.lineTo(sx, sy + sr * 3.6);
        ctx.stroke();
      }
    }

    // 5. 皎潔立體滿月 (位於 x=3120, y=340，與示意圖右上方完全同款)
    const mx = 3120, my = 340, mr = 100;

    // 月亮外圍幽藍銀白月光暈輪 (Lunar Halo)
    const haloGrad = ctx.createRadialGradient(mx, my, mr * 0.8, mx, my, mr * 3.8);
    haloGrad.addColorStop(0.0, 'rgba(219, 234, 254, 0.72)');
    haloGrad.addColorStop(0.35, 'rgba(147, 197, 253, 0.35)');
    haloGrad.addColorStop(0.7, 'rgba(96, 165, 250, 0.14)');
    haloGrad.addColorStop(1.0, 'rgba(0, 0, 0, 0.0)');
    ctx.fillStyle = haloGrad;
    ctx.beginPath();
    ctx.arc(mx, my, mr * 3.8, 0, Math.PI * 2);
    ctx.fill();

    // 月面本體
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
    ctx.clip();

    ctx.fillStyle = 'rgba(148, 163, 184, 0.58)';
    [
      [mx - 25, my - 18, 30], [mx + 20, my - 26, 25], [mx - 36, my + 16, 32],
      [mx + 6, my + 30, 26], [mx + 38, my + 9, 22], [mx - 6, my - 42, 18]
    ].forEach(([cx, cy, cr]) => {
      ctx.beginPath();
      ctx.arc(cx, cy, cr, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();

    // 建立 Three.js Texture
    const skyTex = new THREE.CanvasTexture(canvas);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyTex.wrapS = THREE.RepeatWrapping; // 完美連續重複環景
    skyTex.wrapT = THREE.ClampToEdgeWrapping;

    const skyGeo = new THREE.SphereGeometry(220, 64, 32);
    const skyMat = new THREE.MeshBasicMaterial({
      map: skyTex,
      side: THREE.BackSide,
      depthWrite: false
    });

    skyDomeMesh = new THREE.Mesh(skyGeo, skyMat);
    // 旋轉 0 度：x=1024 (夕陽) 剛好位在左側 (-X)，x=3072 (滿月銀河) 剛好位在右側 (+X)！
    skyDomeMesh.rotation.y = 0;
    scene.add(skyDomeMesh);
  }"""

code = re.sub(
    r"// 繪製 4096x2048 頂級全景雙景天幕[\s\S]*?scene\.add\(skyDomeMesh\);\s*\}",
    new_sky_function,
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated seamless 360 panoramic sky dome successfully.")
