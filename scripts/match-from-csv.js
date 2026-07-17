/**
 * match-from-csv.js
 * 從 posts.csv 讀取文章標題→圖片名稱的對應，
 * 找出還沒有 coverImage 的文章並補上
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CSV_PATH = 'C:\\Users\\X1 Yoga Gen7\\Desktop\\wix-temp\\posts.csv';
const IMAGES_DIR = path.join(__dirname, '../public/images');
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

// ── 1. 讀取 CSV，建立「Wix文章標題 → 本地圖片檔名」的對照表 ──
const csvContent = fs.readFileSync(CSV_PATH, 'utf-8');
const lines = csvContent.split('\n').filter(l => l.trim());

// 取得所有實際存在的圖片
const imageFiles = new Set(fs.readdirSync(IMAGES_DIR));

// CSV 格式：類別,序號,文章標題,分類,圖片網址,文章連結,是否公開
// 建立：Wix文章標題（小寫去空格）→ 圖片檔名
const wixTitleToImage = new Map();

for (const line of lines.slice(1)) {
  // 簡單 CSV 解析（欄位沒有逗號問題）
  const parts = line.split(',');
  if (parts.length < 3) continue;
  const wixTitle = parts[2]?.trim();
  if (!wixTitle) continue;
  
  // 找出對應的本地圖片
  // 圖片是用 wixTitle.png 命名的
  const possibleNames = [
    `${wixTitle}.png`,
    `${wixTitle}.jpg`,
    `${wixTitle}.jpeg`,
  ];
  
  for (const name of possibleNames) {
    if (imageFiles.has(name)) {
      wixTitleToImage.set(wixTitle.toLowerCase().replace(/\s/g, ''), name);
      wixTitleToImage.set(wixTitle, name);
      break;
    }
  }
}

console.log(`📋 CSV 中找到 ${wixTitleToImage.size} 個圖片對應`);

// ── 2. 正規化函數 ──
function normalize(str) {
  return str
    .toLowerCase()
    .replace(/[【】\[\]（）()\s\-_「」『』：:，,。.？?！!\/\\]/g, '')
    .trim();
}

// ── 3. 讀取 CSV 的所有 Wix 標題（正規化版本）→ 圖片 ──
const normalizedWixMap = new Map();
for (const [k, v] of wixTitleToImage) {
  normalizedWixMap.set(normalize(k), v);
}

// ── 4. 處理每篇 Markdown ──
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
let matched = 0, skipped = 0;

for (const mdFile of mdFiles) {
  const filePath = path.join(POSTS_DIR, mdFile);
  const content = fs.readFileSync(filePath, 'utf-8');
  
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;
  const frontmatter = fmMatch[1];
  if (frontmatter.includes('coverImage:')) continue;
  
  const titleMatch = frontmatter.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;
  const title = titleMatch[1].trim();
  const normalizedTitle = normalize(title);
  
  // 嘗試對應
  let foundImage = normalizedWixMap.get(normalizedTitle);
  
  // 如果還找不到，嘗試部分比對
  if (!foundImage) {
    for (const [wixNorm, imgFile] of normalizedWixMap) {
      // 至少有 8 個字元重疊，且重疊比例 > 80%
      const shorter = Math.min(wixNorm.length, normalizedTitle.length);
      const longer = Math.max(wixNorm.length, normalizedTitle.length);
      if (shorter >= 6 && wixNorm.startsWith(normalizedTitle.slice(0, shorter)) && shorter / longer > 0.8) {
        foundImage = imgFile;
        break;
      }
      if (shorter >= 6 && normalizedTitle.startsWith(wixNorm.slice(0, shorter)) && shorter / longer > 0.8) {
        foundImage = imgFile;
        break;
      }
    }
  }
  
  if (foundImage) {
    const newFrontmatter = frontmatter.replace(
      /(^title:.*$)/m,
      `$1\ncoverImage: "${foundImage}"`
    );
    const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf-8');
    console.log(`✅ "${title}"`);
    console.log(`   → ${foundImage}`);
    matched++;
  } else {
    console.log(`❌ 仍找不到: "${title}"`);
    skipped++;
  }
}

console.log(`\n${'='.repeat(50)}`);
console.log(`✅ 新增配對: ${matched} 篇`);
console.log(`❌ 仍找不到: ${skipped} 篇（這些文章 Wix 可能沒有封面圖）`);
