import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '..', 'src', 'content', 'posts');
const DRIVE_DIR = 'G:/我的雲端硬碟/衛教文章圖片';

// 1. 列出 Drive 圖片清單
const driveImages = new Set(fs.readdirSync(DRIVE_DIR).filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f)));
console.log(`\n=== Google Drive 圖片資料夾 (共 ${driveImages.size} 張) ===`);
console.log([...driveImages].join('\n'));

// 2. 列出每篇文章的 coverImage 及是否真的存在於 Drive
console.log('\n=== 文章封面圖現況 ===');
const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md')).sort();
let noImage = [];
let wrongImage = [];
let correct = [];

for (const file of files) {
  const content = fs.readFileSync(path.join(POSTS_DIR, file), 'utf8');
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const coverMatch = content.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);
  const title = titleMatch ? titleMatch[1].trim() : file;
  const cover = coverMatch ? coverMatch[1].trim() : null;

  if (!cover) {
    noImage.push({ file, title });
  } else if (!driveImages.has(cover)) {
    wrongImage.push({ file, title, cover });
  } else {
    correct.push({ file, title, cover });
  }
}

console.log('\n[有圖且圖檔存在 Drive]');
correct.forEach(x => console.log(`  ${x.title} -> ${x.cover}`));
console.log('\n[有 coverImage 但 Drive 沒有該圖！]');
wrongImage.forEach(x => console.log(`  ${x.title} -> 找不到: ${x.cover}`));
console.log('\n[沒有 coverImage]');
noImage.forEach(x => console.log(`  ${x.title}`));

console.log(`\n=== 摘要 ===`);
console.log(`正確配對: ${correct.length} 篇`);
console.log(`圖檔不存在: ${wrongImage.length} 篇`);
console.log(`無封面圖: ${noImage.length} 篇`);
