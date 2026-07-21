import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..');

const DRIVE_IMAGES_DIR = 'G:\\我的雲端硬碟\\衛教文章圖片';
const PUBLIC_IMAGES_DIR = path.join(PROJECT_ROOT, 'public', 'images');
const OG_IMAGES_DIR     = path.join(PROJECT_ROOT, 'public', 'og-images');
const ASSETS_IMAGES_DIR = path.join(PROJECT_ROOT, 'src', 'assets', 'images');
const POSTS_DIR         = path.join(PROJECT_ROOT, 'src', 'content', 'posts');

if (!fs.existsSync(PUBLIC_IMAGES_DIR)) fs.mkdirSync(PUBLIC_IMAGES_DIR, { recursive: true });
if (!fs.existsSync(OG_IMAGES_DIR)) fs.mkdirSync(OG_IMAGES_DIR, { recursive: true });
if (!fs.existsSync(ASSETS_IMAGES_DIR)) fs.mkdirSync(ASSETS_IMAGES_DIR, { recursive: true });

// 壓縮圖片並存到目的地（轉 WebP，最大 1400px 寬）
async function compressAndCopy(srcPath, destPath) {
  const ext = path.extname(destPath).toLowerCase();
  // 如果目的地已是 webp 檔，先刪除同名的舊 png/jpg（如果有）
  try {
    await sharp(srcPath)
      .resize({ width: 1400, withoutEnlargement: true }) // 超過 1400px 才縮小
      .webp({ quality: 82 })
      .toFile(destPath);
  } catch (err) {
    // 壓縮失敗就直接複製原檔
    fs.copyFileSync(srcPath, destPath);
    console.warn(`[壓縮失敗，直接複製] ${path.basename(srcPath)}: ${err.message}`);
  }
}

// 1. 讀取 Google Drive「衛教文章圖片」真實圖片清單
const realImagesMap = new Map(); // normalizedName -> webp 檔名

if (fs.existsSync(DRIVE_IMAGES_DIR)) {
  const driveFiles = fs.readdirSync(DRIVE_IMAGES_DIR);
  const imgFiles = driveFiles.filter(f => ['.png', '.jpg', '.jpeg', '.webp'].includes(path.extname(f).toLowerCase()));

  console.log(`[圖片] 找到 ${imgFiles.length} 張圖片，檢查是否需要壓縮...`);

  let compressedCount = 0;
  let skippedCount = 0;

  for (const file of imgFiles) {
    const ext = path.extname(file).toLowerCase();
    const baseName = path.basename(file, ext);
    const webpName = baseName + '.webp'; // 統一輸出為 .webp

    const srcPath = path.join(DRIVE_IMAGES_DIR, file);
    const destPath = path.join(PUBLIC_IMAGES_DIR, webpName);

    // ✅ 跳過：目的地已存在 且 來源沒有比目的地新
    if (fs.existsSync(destPath)) {
      const srcMtime = fs.statSync(srcPath).mtimeMs;
      const destMtime = fs.statSync(destPath).mtimeMs;
      if (srcMtime <= destMtime) {
        // 來源沒有更新，只需確保其他兩個目錄也有同步
        const ogPath = path.join(OG_IMAGES_DIR, webpName);
        const assetsPath = path.join(ASSETS_IMAGES_DIR, webpName);
        if (!fs.existsSync(ogPath)) fs.copyFileSync(destPath, ogPath);
        if (!fs.existsSync(assetsPath)) fs.copyFileSync(destPath, assetsPath);
        skippedCount++;
        realImagesMap.set(baseName.toLowerCase().trim(), webpName);
        realImagesMap.set(baseName.replace(/\s+/g, '').toLowerCase(), webpName);
        continue;
      }
    }

    // 需要壓縮（新圖 或 圖片已更新）
    await compressAndCopy(srcPath, path.join(PUBLIC_IMAGES_DIR, webpName));
    await compressAndCopy(srcPath, path.join(OG_IMAGES_DIR, webpName));
    await compressAndCopy(srcPath, path.join(ASSETS_IMAGES_DIR, webpName));

    // 刪除三個目錄中同名的舊 png/jpg（如果有）
    for (const oldExt of ['.png', '.jpg', '.jpeg']) {
      if (oldExt === ext && ext !== '.webp') {
        const oldFile = baseName + oldExt;
        for (const dir of [PUBLIC_IMAGES_DIR, OG_IMAGES_DIR, ASSETS_IMAGES_DIR]) {
          const oldPath = path.join(dir, oldFile);
          if (fs.existsSync(oldPath)) fs.unlinkSync(oldPath);
        }
      }
    }

    const sizeBefore = Math.round(fs.statSync(srcPath).size / 1024);
    const sizeAfter = Math.round(fs.statSync(path.join(PUBLIC_IMAGES_DIR, webpName)).size / 1024);
    console.log(`  ✅ ${baseName}  ${sizeBefore}KB → ${sizeAfter}KB`);
    compressedCount++;

    realImagesMap.set(baseName.toLowerCase().trim(), webpName);
    realImagesMap.set(baseName.replace(/\s+/g, '').toLowerCase(), webpName);
  }

  console.log(`[圖片] 壓縮：${compressedCount} 張 ／ 跳過（未更新）：${skippedCount} 張`);

} else {
  console.warn(`[警告] 找不到 Google Drive 圖片資料夾：${DRIVE_IMAGES_DIR}`);
}

// 2. 更新文章 frontmatter 的 coverImage（改成 .webp 副檔名）
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

let validCoverCount = 0;
let removedCoverCount = 0;

for (const file of mdFiles) {
  const filePath = path.join(POSTS_DIR, file);
  const content = fs.readFileSync(filePath, 'utf8');

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;

  const frontmatter = fmMatch[1];
  const titleMatch = frontmatter.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;

  const title = titleMatch[1].trim();
  const titleClean = title.replace(/[【\[（(].+?[】\]）)]\s*/g, '').trim();

  // 嘗試比對標題是否有真正的圖檔
  let matchedImage = null;
  if (realImagesMap.has(title.toLowerCase())) matchedImage = realImagesMap.get(title.toLowerCase());
  else if (realImagesMap.has(titleClean.toLowerCase())) matchedImage = realImagesMap.get(titleClean.toLowerCase());
  else if (realImagesMap.has(title.replace(/\s+/g, '').toLowerCase())) matchedImage = realImagesMap.get(title.replace(/\s+/g, '').toLowerCase());
  else if (realImagesMap.has(titleClean.replace(/\s+/g, '').toLowerCase())) matchedImage = realImagesMap.get(titleClean.replace(/\s+/g, '').toLowerCase());

  // 特殊檔名映射修正
  if (!matchedImage && title === '大腸息肉切除術後的出血機率' && realImagesMap.has('大腸息肉切除術後出血')) {
    matchedImage = realImagesMap.get('大腸息肉切除術後出血');
  }

  let newFrontmatter = frontmatter;
  const hasCoverInFM = frontmatter.includes('coverImage:');

  if (matchedImage) {
    if (hasCoverInFM) {
      newFrontmatter = newFrontmatter.replace(
        /^coverImage:\s*["']?.*?["']?\s*$/m,
        `coverImage: "${matchedImage}"`
      );
    } else {
      newFrontmatter = newFrontmatter.replace(
        /(^title:.*$)/m,
        `$1\ncoverImage: "${matchedImage}"`
      );
    }
    validCoverCount++;
  } else {
    if (hasCoverInFM) {
      newFrontmatter = newFrontmatter.replace(/^coverImage:.*$\n?/m, '');
      removedCoverCount++;
      console.log(`[移除無對應圖片的封面網址] ${title}`);
    }
  }

  if (newFrontmatter !== frontmatter) {
    const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf8');
  }
}

console.log('\n' + '='.repeat(50));
console.log(`✅ 保留/設定真實圖檔文章：${validCoverCount} 篇`);
console.log(`🗑️  清除湊數無圖檔文章封面：${removedCoverCount} 篇`);
console.log('='.repeat(50) + '\n');
