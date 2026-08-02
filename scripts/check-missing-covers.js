import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');
const DRIVE_DIR = 'G:\\我的雲端硬碟\\衛教文章圖片';

const targets = [
  '地雷食物胃食道逆流地雷食物.md',
  '地雷食物腸躁症-fodmap.md',
  '地雷食物高三酸甘油脂地雷食物.md',
  '地雷食物高壞膽固醇地雷食物.md',
  '地雷食物高尿酸地雷食物.md',
  '大腸息肉分類.md',
  '大腸息肉切除術後出血.md',
  '大腸息肉各種息肉常用的切除方式.md',
  '大腸息肉困難息肉切除.md',
  '幽門桿菌兒童防治與治療.md',
  '幽門桿菌幽門桿菌是怎麼來的.md',
  '幽門桿菌幽門桿菌的治療方式.md',
  '幽門桿菌難治性幽門桿菌.md',
  '胰島素的控糖新觀念.md',
  '腸鏡前準備低渣飲食.md',
  '腸鏡前準備保可淨.md',
  '腸鏡前準備清腸劑比較保可淨及耐福力散.md',
  '腸鏡前準備耐福利散.md',
  '豐田診所內視鏡介紹.md',
];

const driveFiles = fs.existsSync(DRIVE_DIR)
  ? fs.readdirSync(DRIVE_DIR).filter(f => ['.png','.jpg','.jpeg','.webp'].includes(path.extname(f).toLowerCase()))
  : [];

console.log('=== 文章目前標題 & coverImage ===');
for (const f of targets) {
  const fp = path.join(POSTS_DIR, f);
  if (!fs.existsSync(fp)) { console.log('NOT FOUND:', f); continue; }
  const content = fs.readFileSync(fp, 'utf8');
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const coverMatch = content.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);
  const title = titleMatch ? titleMatch[1].trim() : '(no title)';
  const cover = coverMatch ? coverMatch[1].trim() : '(MISSING)';
  
  // 目前 Drive 中同名圖片是否存在
  const driveMatch = driveFiles.find(df => path.basename(df, path.extname(df)) === path.basename(cover, path.extname(cover)));
  
  console.log(`
  檔案: ${f}
  標題: ${title}
  coverImage: ${cover}
  Drive 有對應圖: ${driveMatch ? '✅ ' + driveMatch : '❌ 不存在'}`);
}
