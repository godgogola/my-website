import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

const [,, srcPath, title] = process.argv;

if (!srcPath || !title) {
  console.error('Usage: node scripts/process-cover-image.js <srcPath> <title>');
  process.exit(1);
}

const DRIVE_DIR = 'G:\\我的雲端硬碟\\衛教文章圖片';
const PUBLIC_IMG_DIR = path.resolve('public/images');
const PUBLIC_OG_DIR = path.resolve('public/og-images');

async function main() {
  console.log(`Processing cover for: ${title}`);

  // 1. 備份 PNG 至 Google Drive (如果存在)
  try {
    if (fs.existsSync(DRIVE_DIR)) {
      const drivePngPath = path.join(DRIVE_DIR, `${title}.png`);
      await sharp(srcPath).png({ quality: 100 }).toFile(drivePngPath);
      console.log(`✓ Backup PNG to Drive: ${drivePngPath}`);
    } else {
      console.log(`ℹ Drive path not found, skipping Drive backup`);
    }
  } catch (err) {
    console.warn(`Warning: Could not save to Drive: ${err.message}`);
  }

  // 2. 轉 WebP 存入 public/images
  if (!fs.existsSync(PUBLIC_IMG_DIR)) fs.mkdirSync(PUBLIC_IMG_DIR, { recursive: true });
  const publicWebpPath = path.join(PUBLIC_IMG_DIR, `${title}.webp`);
  await sharp(srcPath).webp({ quality: 90 }).toFile(publicWebpPath);
  console.log(`✓ Saved WebP to: ${publicWebpPath}`);

  // 3. 轉 WebP 存入 public/og-images
  if (!fs.existsSync(PUBLIC_OG_DIR)) fs.mkdirSync(PUBLIC_OG_DIR, { recursive: true });
  const publicOgPath = path.join(PUBLIC_OG_DIR, `${title}.webp`);
  await sharp(srcPath).webp({ quality: 90 }).toFile(publicOgPath);
  console.log(`✓ Saved WebP to: ${publicOgPath}`);

  // 4. 更新對應的 Markdown 檔案
  const contentDirs = [path.resolve('src/content/books'), path.resolve('src/content/posts')];
  let updatedFile = null;

  function scanDir(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        scanDir(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        const base = path.basename(entry.name, '.md');
        // 比對檔名、數字前綴或標題
        const cleanTitle = title.replace(/^[0-9]+[、\-_\s]*/, '').trim();
        const cleanBase = base.replace(/^[0-9]+[、\-_\s]*/, '').trim();
        if (base === title || cleanBase === cleanTitle || base.includes(cleanTitle) || cleanTitle.includes(cleanBase)) {
          updateFrontmatter(fullPath);
          updatedFile = fullPath;
        }
      }
    }
  }

  function updateFrontmatter(filePath) {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const coverImageLine = `coverImage: "${title}.webp"`;
    let newContent = '';
    if (raw.includes('coverImage:')) {
      newContent = raw.replace(/coverImage:\s*["'][^"']*["']/g, coverImageLine);
    } else {
      newContent = raw.replace(/---\r?\n([\s\S]*?)\r?\n---/, (match, fm) => {
        return `---\n${fm.trim()}\n${coverImageLine}\n---`;
      });
    }
    fs.writeFileSync(filePath, newContent, 'utf-8');
    console.log(`✓ Updated coverImage in Markdown: ${filePath}`);
  }

  for (const cDir of contentDirs) {
    scanDir(cDir);
  }

  if (!updatedFile) {
    console.log(`ℹ Note: No direct matching markdown found for title "${title}"`);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
