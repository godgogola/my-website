import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

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

// 1. 讀取 Google Drive「衛教文章圖片」真實圖片清單
const realImagesMap = new Map(); // normalizedName -> originalImgFileName

if (fs.existsSync(DRIVE_IMAGES_DIR)) {
  const driveFiles = fs.readdirSync(DRIVE_IMAGES_DIR);
  for (const file of driveFiles) {
    const ext = path.extname(file).toLowerCase();
    if (['.png', '.jpg', '.jpeg', '.webp'].includes(ext)) {
      // 複製到 public/images, public/og-images, src/assets/images
      const srcPath = path.join(DRIVE_IMAGES_DIR, file);
      fs.copyFileSync(srcPath, path.join(PUBLIC_IMAGES_DIR, file));
      fs.copyFileSync(srcPath, path.join(OG_IMAGES_DIR, file));
      fs.copyFileSync(srcPath, path.join(ASSETS_IMAGES_DIR, file));

      const baseName = path.basename(file, ext);
      realImagesMap.set(baseName.toLowerCase().trim(), file);
      realImagesMap.set(baseName.replace(/\s+/g, '').toLowerCase(), file);
    }
  }
}

// 2. 檢查 src/content/posts/ 所有文章，僅保留真實配對的圖片，刪除假的/預設湊數的圖片
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
    // 寫入/更新正確的 coverImage
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
    // 若沒有真正匹配的圖片，則把之前的假 coverImage 移除！
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
