/**
 * auto-cover-image.js
 * 自動比對文章標題與圖片檔名，並在 frontmatter 中加入 coverImage 欄位
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const IMAGES_DIR = path.join(__dirname, '../public/images');
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

// 1. 取得所有圖片檔名（不含副檔名）
const imageFiles = fs.readdirSync(IMAGES_DIR);
const imageMap = new Map();

for (const file of imageFiles) {
  const ext = path.extname(file).toLowerCase();
  if (ext === '.png' || ext === '.jpg' || ext === '.jpeg' || ext === '.webp') {
    const nameWithoutExt = path.basename(file, ext);
    imageMap.set(nameWithoutExt, file);
    imageMap.set(nameWithoutExt.toLowerCase(), file);
    imageMap.set(nameWithoutExt.replace(/\s/g, ''), file);
    imageMap.set(nameWithoutExt.toLowerCase().replace(/\s/g, ''), file);
  }
}

console.log(`📁 找到 ${imageFiles.length} 張圖片`);

// 2. 讀取所有 Markdown 文章
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
console.log(`📝 找到 ${mdFiles.length} 篇文章\n`);

let matched = 0;
let skipped = 0;
let alreadyHas = 0;

for (const mdFile of mdFiles) {
  const filePath = path.join(POSTS_DIR, mdFile);
  const content = fs.readFileSync(filePath, 'utf-8');

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;

  const frontmatter = fmMatch[1];

  if (frontmatter.includes('coverImage:')) {
    alreadyHas++;
    continue;
  }

  const titleMatch = frontmatter.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;

  const title = titleMatch[1].trim();

  const lookups = [
    title,
    title.toLowerCase(),
    title.replace(/\s/g, ''),
    title.toLowerCase().replace(/\s/g, ''),
    title.replace(/[【\[（(].+?[】\]）)]\s*/g, '').trim(),
  ];

  let foundImage = null;
  for (const lookup of lookups) {
    if (imageMap.has(lookup)) {
      foundImage = imageMap.get(lookup);
      break;
    }
  }

  if (foundImage) {
    const newFrontmatter = frontmatter.replace(
      /(^title:.*$)/m,
      `$1\ncoverImage: "${foundImage}"`
    );
    const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf-8');
    console.log(`✅ ${title} → ${foundImage}`);
    matched++;
  } else {
    console.log(`❌ 找不到圖片: "${title}"`);
    skipped++;
  }
}

console.log('\n' + '='.repeat(50));
console.log(`✅ 成功配對: ${matched} 篇`);
console.log(`⚠️  已有圖片: ${alreadyHas} 篇`);
console.log(`❌ 找不到圖片: ${skipped} 篇`);
