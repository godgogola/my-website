/**
 * fix-missing-covers.js
 * 手動配對：因文章標題變更導致圖片消失的文章，直接指定正確圖檔名
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');
const IMAGES_DIR = path.join(__dirname, '../public/images');

// 手動配對表：slug（檔名去掉.md） → 圖片檔名
const MANUAL_MAP = {
  '大腸息肉分類':                         '大腸息肉的分類.webp',
  '大腸息肉各種息肉常用的切除方式':         '各種大腸息肉的切除方式.webp',
  '大腸息肉困難息肉切除':                  '診所也可以做困難息肉切除.webp',
  '幽門桿菌兒童防治與治療':               '兒童幽門桿菌防治與治療.webp',
  '幽門桿菌幽門桿菌是怎麼來的':           '幽門桿菌怎麼來的.webp',
  '幽門桿菌幽門桿菌的治療方式':           '幽門螺旋桿菌的各種殺菌治療方式.webp',
  '幽門桿菌難治性幽門桿菌':               '難治性幽門桿菌治療_二次治療失敗.webp',
  '腸鏡前準備低渣飲食':                  '大腸鏡檢查前的低渣飲食指南.webp',
  '腸鏡前準備保可淨':                    '大腸鏡前清腸準備(保可淨).webp',
  '腸鏡前準備清腸劑比較保可淨及耐福力散':  '清腸劑比較(保可淨及耐福力散).webp',
  '腸鏡前準備耐福利散':                  '大腸鏡前清腸準備(耐福利散).webp',
  '豐田診所內視鏡介紹':                  '豐田診所使用的內視鏡系統-ELUXEO™ Lite 6000 影像系統 — 三大觀察模式介紹.webp',
};


let fixed = 0;
let skipped = 0;

for (const [slug, imageFile] of Object.entries(MANUAL_MAP)) {
  const mdPath = path.join(POSTS_DIR, `${slug}.md`);
  const imgPath = path.join(IMAGES_DIR, imageFile);

  if (!fs.existsSync(mdPath)) {
    console.log(`⚠️  找不到文章: ${slug}.md`);
    skipped++;
    continue;
  }

  if (!fs.existsSync(imgPath)) {
    console.log(`⚠️  找不到圖片: ${imageFile}`);
    skipped++;
    continue;
  }

  const content = fs.readFileSync(mdPath, 'utf8');
  if (content.includes('coverImage:')) {
    console.log(`⏭️  已有封面圖，跳過: ${slug}`);
    skipped++;
    continue;
  }

  // 在 title 那行後面插入 coverImage
  const updated = content.replace(
    /(^title:.*$)/m,
    `$1\ncoverImage: "${imageFile}"`
  );
  fs.writeFileSync(mdPath, updated, 'utf8');
  console.log(`✅ 修復: ${slug} → ${imageFile}`);
  fixed++;
}

console.log(`\n${'='.repeat(50)}`);
console.log(`✅ 修復: ${fixed} 篇`);
console.log(`⏭️  跳過: ${skipped} 篇`);
