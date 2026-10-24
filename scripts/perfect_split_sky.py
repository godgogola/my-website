import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 在 4096 的畫布上：
# 讓畫面中心在 x = 1100：
# - 左側夕陽在 x = 750 (畫面左上方，金光四射、飛鳥卷雲)
# - 右側銀河星空跨越 x = 1100 ~ 1500
# - 右側皎潔滿月在 x = 1420 (畫面右上方，立體月海與銀藍月暈)
# - 畫面兩端 (x=0 與 x=4096) 均為深空深黑，無縫過渡

perfect_split_sky = """  // 繪製 4096x2048 頂級全景雙景天幕 (同框震撼視界：左側金金日落霞光 × 右側浩瀚銀河明月)
  function createMasterpieceSkyDome() {
    const canvas = document.createElement('canvas');
    canvas.width = 4096;
    canvas.height = 2048;
    const ctx = canvas.getContext('2d');

    // 1. 底色：深邃午夜深空 (#030714)
    ctx.fillStyle = '#030714';
    ctx.fillRect(0, 0, 4096, 2048);

    // 2. 左側：耀眼夕陽晚霞 (中心位於 x = 780, y = 1160)
    const sunCenterX = 780;
    const sunCenterY = 1160;

    const sunsetGrad = ctx.createRadialGradient(sunCenterX, sunCenterY, 25, sunCenterX, sunCenterY, 950);
    sunsetGrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');  // 白金日核
    sunsetGrad.addColorStop(0.08, 'rgba(255, 245, 180, 0.98)'); // 金黃日冕
    sunsetGrad.addColorStop(0.22, 'rgba(251, 191, 36, 0.92)');  // 燦爛金橙
    sunsetGrad.addColorStop(0.45, 'rgba(249, 115, 22, 0.72)');  // 暖橙晚霞
    sunsetGrad.addColorStop(0.68, 'rgba(190, 24, 93, 0.38)');   // 暮色玫瑰
    sunsetGrad.addColorStop(0.85, 'rgba(88, 28, 135, 0.12)');   // 暮紫流霞
    sunsetGrad.addColorStop(1.0, 'rgba(3, 7, 20, 0.0)');
    ctx.fillStyle = sunsetGrad;
    ctx.fillRect(0, 0, 1600, 2048);

    // 地平線柔金霞光帶
    const horizonGrad = ctx.createLinearGradient(0, 1040, 0, 1320);
    horizonGrad.addColorStop(0.0, 'rgba(255, 240, 190, 0.85)');
    horizonGrad.addColorStop(0.4, 'rgba(251, 146, 60, 0.6)');
    horizonGrad.addColorStop(1.0, 'rgba(251, 146, 60, 0.0)');
    ctx.fillStyle = horizonGrad;
    ctx.fillRect(0, 1000, 1300, 320);

    // 金色夕陽晚霞卷雲 (Wispy Clouds)
    ctx.save();
    ctx.filter = 'blur(14px)';
    ctx.fillStyle = 'rgba(254, 215, 170, 0.42)';
    [
      [420, 920, 420, 36], [720, 860, 520, 42], [980, 900, 460, 38],
      [580, 980, 380, 32], [880, 960, 420, 35]
    ].forEach(([cx, cy, cw, ch]) => {
      ctx.beginPath();
      ctx.ellipse(cx, cy, cw, ch, -0.04, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();

    // 夕陽中的黑色飛鳥剪影群 (Flock of silhouette birds)
    ctx.fillStyle = '#18181b';
    [
      [860, 880, 1.2], [905, 865, 0.95], [830, 900, 0.85], [955, 895, 1.1],
      [990, 870, 0.8], [800, 920, 0.75], [925, 920, 0.9], [880, 850, 0.7]
    ].forEach(([bx, by, s]) => {
      ctx.beginPath();
      ctx.moveTo(bx - 14 * s, by - 6 * s);
      ctx.quadraticCurveTo(bx - 7 * s, by + 4 * s, bx, by);
      ctx.quadraticCurveTo(bx + 7 * s, by + 4 * s, bx + 14 * s, by - 6 * s);
      ctx.quadraticCurveTo(bx + 7 * s, by + 1 * s, bx, by + 2 * s);
      ctx.quadraticCurveTo(bx - 7 * s, by + 1 * s, bx - 14 * s, by - 6 * s);
      ctx.fill();
    });

    // 3. 右側：壯麗高密度銀河系星雲帶 (中心斜貫 x = 1380)
    ctx.save();
    ctx.translate(1380, 960);
    ctx.rotate(-0.52);

    const nebulaGrad1 = ctx.createLinearGradient(-800, 0, 800, 0);
    nebulaGrad1.addColorStop(0.0, 'rgba(147, 51, 234, 0.0)');
    nebulaGrad1.addColorStop(0.35, 'rgba(168, 85, 247, 0.32)');
    nebulaGrad1.addColorStop(0.5, 'rgba(236, 72, 153, 0.38)');
    nebulaGrad1.addColorStop(0.65, 'rgba(96, 165, 250, 0.28)');
    nebulaGrad1.addColorStop(1.0, 'rgba(59, 130, 246, 0.0)');

    ctx.filter = 'blur(45px)';
    ctx.fillStyle = nebulaGrad1;
    ctx.fillRect(-800, -180, 1600, 360);

    const nebulaGrad2 = ctx.createLinearGradient(-600, 0, 600, 0);
    nebulaGrad2.addColorStop(0.2, 'rgba(255, 255, 255, 0.0)');
    nebulaGrad2.addColorStop(0.5, 'rgba(255, 240, 255, 0.45)');
    nebulaGrad2.addColorStop(0.8, 'rgba(255, 255, 255, 0.0)');
    ctx.filter = 'blur(26px)';
    ctx.fillStyle = nebulaGrad2;
    ctx.fillRect(-600, -80, 1200, 160);
    ctx.restore();

    // 4. 右側浩瀚繁星 (1,800+ 顆集中在 x = 1150 ~ 1750)
    const seed = 42;
    let rnd = seed;
    function pseudoRandom() {
      rnd = (rnd * 9301 + 49297) % 233280;
      return rnd / 233280;
    }

    for (let i = 0; i < 2200; i++) {
      const sx = 1050 + pseudoRandom() * 950;
      const sy = pseudoRandom() * 1250;
      const sr = pseudoRandom() * 1.8 + 0.4;
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

      if (sr > 1.8 && pseudoRandom() < 0.28) {
        ctx.strokeStyle = `rgba(255, 255, 255, ${op * 0.75})`;
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.moveTo(sx - sr * 3.5, sy); ctx.lineTo(sx + sr * 3.5, sy);
        ctx.moveTo(sx, sy - sr * 3.5); ctx.lineTo(sx, sy + sr * 3.5);
        ctx.stroke();
      }
    }

    // 5. 右上方立體逼真皎潔滿月 (精準落在 x = 1460, y = 350)
    const mx = 1460, my = 350, mr = 82;

    // 月亮外圍幽藍銀白月光暈輪 (Lunar Halo)
    const haloGrad = ctx.createRadialGradient(mx, my, mr * 0.8, mx, my, mr * 3.8);
    haloGrad.addColorStop(0.0, 'rgba(219, 234, 254, 0.75)');
    haloGrad.addColorStop(0.35, 'rgba(147, 197, 253, 0.38)');
    haloGrad.addColorStop(0.7, 'rgba(96, 165, 250, 0.15)');
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
      [mx - 20, my - 14, 24], [mx + 16, my - 20, 20], [mx - 28, my + 13, 26],
      [mx + 5, my + 24, 22], [mx + 30, my + 7, 18], [mx - 5, my - 34, 15]
    ].forEach(([cx, cy, cr]) => {
      ctx.beginPath();
      ctx.arc(cx, cy, cr, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();

    // 建立 Three.js Texture
    const skyTex = new THREE.CanvasTexture(canvas);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyTex.wrapS = THREE.RepeatWrapping;
    skyTex.wrapT = THREE.ClampToEdgeWrapping;

    const skyGeo = new THREE.SphereGeometry(220, 64, 32);
    const skyMat = new THREE.MeshBasicMaterial({
      map: skyTex,
      side: THREE.BackSide,
      depthWrite: false
    });

    skyDomeMesh = new THREE.Mesh(skyGeo, skyMat);
    // 旋轉微調：讓中心 (x=1120) 剛好正對鏡頭視野中心！
    skyDomeMesh.rotation.y = Math.PI * 0.95;
    scene.add(skyDomeMesh);
  }"""

code = re.sub(
    r"// 繪製 4096x2048 頂級全景雙景天幕[\s\S]*?scene\.add\(skyDomeMesh\);\s*\}",
    perfect_split_sky,
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied perfect co-located split sky dome!")
