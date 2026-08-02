/**
 * update-cover-mapping.js
 * 將 cover-mapping.json 裡的舊圖檔名更新成與文章標題一致的新名稱
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MAPPING_FILE = path.join(__dirname, 'cover-mapping.json');
const PUBLIC_IMAGES_DIR = path.join(__dirname, '../public/images');

// 舊圖檔名 → 新圖檔名（對應 rename-drive-images.js 的重新命名）
const RENAME_MAP = {
  '胃食道逆流患者的地雷飲食.webp':           '【地雷食物】胃食道逆流地雷食物.webp',
  '胃食道逆流的地雷飲食.webp':               '【地雷食物】胃食道逆流地雷食物.webp',
  'FODMAP 食物指南-腸躁症.webp':            '【地雷食物】腸躁症 FODMAP.webp',
  '腸躁症 FODMAP.webp':                    '【地雷食物】腸躁症 FODMAP.webp',
  '三酸甘油脂食物地雷.webp':                 '【地雷食物】高三酸甘油脂地雷食物.webp',
  '哪些食物會讓三酸甘油脂升高.webp':          '【地雷食物】高三酸甘油脂地雷食物.webp',
  '壞膽固醇食物地雷.webp':                  '【地雷食物】高壞膽固醇地雷食物.webp',
  '哪些食物會讓壞膽固醇（LDL）升高.webp':     '【地雷食物】高壞膽固醇地雷食物.webp',
  '尿酸食物地雷.webp':                      '【地雷食物】高尿酸地雷食物.webp',
  '哪些食物會讓尿酸升高.webp':               '【地雷食物】高尿酸地雷食物.webp',
  '大腸息肉的分類.webp':                    '【大腸息肉】分類.webp',
  '大腸息肉切除術後出血.webp':               '【大腸息肉】切除術後出血.webp',
  '各種大腸息肉的切除方式.webp':              '【大腸息肉】各種息肉常用的切除方式.webp',
  '困難息肉切除.webp':                      '【大腸息肉】困難息肉切除.webp',
  '診所也可以做困難息肉切除.webp':            '【大腸息肉】困難息肉切除.webp',
  '兒童幽門桿菌防治與治療.webp':             '【幽門桿菌】兒童防治與治療.webp',
  '幽門桿菌怎麼來的.webp':                  '【幽門桿菌】幽門桿菌是怎麼來的.webp',
  '幽門螺旋桿菌的各種殺菌治療方式.webp':      '【幽門桿菌】幽門桿菌的治療方式.webp',
  '幽門桿菌除菌.webp':                      '【幽門桿菌】幽門桿菌的治療方式.webp',
  '難治性幽門桿菌治療_二次治療失敗.webp':     '【幽門桿菌】難治性幽門桿菌.webp',
  '難治性幽門桿菌治療.webp':                 '【幽門桿菌】難治性幽門桿菌.webp',
  '胰島素的控糖新觀念--擺脫定時定量的束縛！.webp': '胰島素的控糖新觀念.webp',
  '大腸鏡檢查前的低渣飲食指南.webp':         '【腸鏡前準備】低渣飲食.webp',
  '低渣飲食.webp':                          '【腸鏡前準備】低渣飲食.webp',
  '大腸鏡前清腸準備(保可淨).webp':           '【腸鏡前準備】(保可淨).webp',
  '清腸準備(保可淨).webp':                  '【腸鏡前準備】(保可淨).webp',
  '清腸劑比較(保可淨及耐福力散).webp':        '【腸鏡前準備】清腸劑比較(保可淨及耐福力散).webp',
  '清腸劑比較.webp':                        '【腸鏡前準備】清腸劑比較(保可淨及耐福力散).webp',
  '大腸鏡前清腸準備(耐福利散).webp':         '【腸鏡前準備】(耐福利散).webp',
  '清腸準備(耐福利散).webp':                '【腸鏡前準備】(耐福利散).webp',
  '豐田診所使用的內視鏡系統-ELUXEO™ Lite 6000 影像系統 — 三大觀察模式介紹.webp': '豐田診所內視鏡介紹.webp',
  'Fugifilm 6000 介紹.webp':               '豐田診所內視鏡介紹.webp',
};

const mapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));
let updated = 0;
let skipped = 0;

const newMapping = mapping.map(entry => {
  const oldImage = entry.coverImage;
  if (RENAME_MAP[oldImage]) {
    const newImage = RENAME_MAP[oldImage];
    // 只更新如果新圖片真的存在於 public/images
    const newImagePath = path.join(PUBLIC_IMAGES_DIR, newImage);
    if (fs.existsSync(newImagePath)) {
      console.log(`✅ 更新: "${oldImage}" → "${newImage}" (${entry.title})`);
      updated++;
      return { ...entry, coverImage: newImage };
    } else {
      console.log(`⚠️  新圖不存在於 public/images，保留舊值: "${oldImage}" (${entry.title})`);
      skipped++;
    }
  }
  return entry;
});

fs.writeFileSync(MAPPING_FILE, JSON.stringify(newMapping, null, 4), 'utf8');

console.log(`\n${'='.repeat(50)}`);
console.log(`✅ 已更新 cover-mapping.json: ${updated} 筆`);
console.log(`⏭️  跳過（新圖不存在）: ${skipped} 筆`);
