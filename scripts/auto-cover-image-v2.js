/**
 * auto-cover-image-v2.js
 * 進階模糊比對，處理剩餘找不到圖片的文章
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const IMAGES_DIR = path.join(__dirname, '../src/assets/images');
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

// 標準化字串：移除所有括號、標點、空格，只保留核心中英文
function normalize(str) {
  return str
    .replace(/[【】\[\]（）()\s\-_「」『』：:，,。.？?！!]/g, '')
    .replace(/[A-Z]/g, c => c.toLowerCase())
    .trim();
}

// 1. 建立圖片索引
const imageFiles = fs.readdirSync(IMAGES_DIR);
const images = [];
for (const file of imageFiles) {
  const ext = path.extname(file).toLowerCase();
  if (['.png', '.jpg', '.jpeg', '.webp'].includes(ext)) {
    const nameWithoutExt = path.basename(file, ext);
    images.push({
      filename: file,
      name: nameWithoutExt,
      normalized: normalize(nameWithoutExt),
    });
  }
}

// 2. 讀取所有 Markdown（只處理還沒有 coverImage 的）
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

let matched = 0;
let skipped = 0;

for (const mdFile of mdFiles) {
  const filePath = path.join(POSTS_DIR, mdFile);
  const content = fs.readFileSync(filePath, 'utf-8');

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;

  const frontmatter = fmMatch[1];
  if (frontmatter.includes('coverImage:')) continue; // 已有圖片，跳過

  const titleMatch = frontmatter.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;

  const title = titleMatch[1].trim();
  const normalizedTitle = normalize(title);

  // 嘗試模糊比對
  let best = null;
  let bestScore = 0;

  for (const img of images) {
    // 完全相符
    if (img.normalized === normalizedTitle) {
      best = img;
      bestScore = 100;
      break;
    }
    // 圖片名是文章標題的子集（或反之）
    if (img.normalized.length > 3 && normalizedTitle.includes(img.normalized)) {
      const score = img.normalized.length / normalizedTitle.length * 90;
      if (score > bestScore) { bestScore = score; best = img; }
    }
    if (normalizedTitle.length > 3 && img.normalized.includes(normalizedTitle)) {
      const score = normalizedTitle.length / img.normalized.length * 90;
      if (score > bestScore) { bestScore = score; best = img; }
    }
    // 開頭相符（至少 6 個字）
    const minLen = Math.min(img.normalized.length, normalizedTitle.length, 6);
    if (minLen >= 6 && img.normalized.slice(0, minLen) === normalizedTitle.slice(0, minLen)) {
      const score = minLen / Math.max(img.normalized.length, normalizedTitle.length) * 85;
      if (score > bestScore) { bestScore = score; best = img; }
    }
  }

  // 只有信心度夠高才採用（避免亂配對）
  if (best && bestScore >= 70) {
    const newFrontmatter = frontmatter.replace(
      /(^title:.*$)/m,
      `$1\ncoverImage: "${best.filename}"`
    );
    const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf-8');
    console.log(`✅ [${Math.round(bestScore)}%] "${title}"`);
    console.log(`   → ${best.filename}\n`);
    matched++;
  } else {
    console.log(`❌ 找不到合適圖片: "${title}"`);
    skipped++;
  }
}

console.log('\n' + '='.repeat(50));
console.log(`✅ 新增配對: ${matched} 篇`);
console.log(`❌ 仍找不到: ${skipped} 篇`);
