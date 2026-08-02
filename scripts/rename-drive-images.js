/**
 * rename-drive-images.js
 * 將 Google Drive 圖片重新命名成符合文章新標題，解決 coverImage 對應問題
 */

import fs from 'fs';
import path from 'path';

const DRIVE_DIR = 'G:\\我的雲端硬碟\\衛教文章圖片';
const PUBLIC_IMAGES_DIR = 'public/images';

// 舊圖檔名（不含副檔名）→ 新標題（= 文章 title = 新圖檔名）
// 格式：'Drive 上的舊檔名（不含.png）': '文章 title（不含副檔名）'
const RENAME_MAP = {
  '胃食道逆流患者的地雷飲食':
    '【地雷食物】胃食道逆流地雷食物',

  'FODMAP 食物指南-腸躁症':
    '【地雷食物】腸躁症 FODMAP',

  '哪些食物會讓三酸甘油脂升高':
    '【地雷食物】高三酸甘油脂地雷食物',

  '哪些食物會讓壞膽固醇（LDL）升高':
    '【地雷食物】高壞膽固醇地雷食物',

  '哪些食物會讓尿酸升高':
    '【地雷食物】高尿酸地雷食物',

  '大腸息肉的分類':
    '【大腸息肉】分類',

  '大腸息肉切除術後出血':
    '【大腸息肉】切除術後出血',

  '各種大腸息肉的切除方式':
    '【大腸息肉】各種息肉常用的切除方式',

  '診所也可以做困難息肉切除':
    '【大腸息肉】困難息肉切除',

  '兒童幽門桿菌防治與治療':
    '【幽門桿菌】兒童防治與治療',

  '幽門桿菌怎麼來的':
    '【幽門桿菌】幽門桿菌是怎麼來的',

  '幽門螺旋桿菌的各種殺菌治療方式':
    '【幽門桿菌】幽門桿菌的治療方式',

  '難治性幽門桿菌治療_二次治療失敗':
    '【幽門桿菌】難治性幽門桿菌',

  '胰島素的控糖新觀念--擺脫定時定量的束縛！':
    '胰島素的控糖新觀念',

  '大腸鏡檢查前的低渣飲食指南':
    '【腸鏡前準備】低渣飲食',

  '大腸鏡前清腸準備(保可淨)':
    '【腸鏡前準備】(保可淨)',

  '清腸劑比較(保可淨及耐福力散)':
    '【腸鏡前準備】清腸劑比較(保可淨及耐福力散)',

  '大腸鏡前清腸準備(耐福利散)':
    '【腸鏡前準備】(耐福利散)',

  '豐田診所使用的內視鏡系統-ELUXEO™ Lite 6000 影像系統 — 三大觀察模式介紹':
    '豐田診所內視鏡介紹',
};

let renamed = 0;
let skipped = 0;

console.log('=== 開始重新命名 Drive 圖片 ===\n');

for (const [oldBase, newTitle] of Object.entries(RENAME_MAP)) {
  // 找出 Drive 中的舊圖（可能是 .png 或 .webp）
  const exts = ['.png', '.jpg', '.jpeg', '.webp'];
  let oldFile = null;
  let ext = null;
  for (const e of exts) {
    const candidate = path.join(DRIVE_DIR, oldBase + e);
    if (fs.existsSync(candidate)) { oldFile = candidate; ext = e; break; }
  }

  if (!oldFile) {
    console.log(`⚠️  找不到舊圖: ${oldBase}.*`);
    skipped++;
    continue;
  }

  const newFile = path.join(DRIVE_DIR, newTitle + ext);

  if (fs.existsSync(newFile)) {
    console.log(`⏭️  新名稱已存在，跳過: ${newTitle}${ext}`);
    skipped++;
    continue;
  }

  fs.renameSync(oldFile, newFile);
  console.log(`✅ 重新命名:\n   舊: ${oldBase}${ext}\n   新: ${newTitle}${ext}\n`);
  renamed++;

  // 同步清除 public/images 中的舊 webp（若存在）
  const oldWebp = path.join(PUBLIC_IMAGES_DIR, oldBase + '.webp');
  if (fs.existsSync(oldWebp)) {
    fs.unlinkSync(oldWebp);
    console.log(`   🗑️  刪除舊 public/images: ${oldBase}.webp`);
  }
}

console.log(`\n${'='.repeat(50)}`);
console.log(`✅ 成功重新命名: ${renamed} 張`);
console.log(`⏭️  跳過: ${skipped} 張`);
console.log(`\n接下來請執行 sync-drive-images.js 完成同步！`);
