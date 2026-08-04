/**
 * add-2-missing.js
 * 只新增 2 篇確定缺少的文章到 Google Sheet 次分類
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR         = path.join(__dirname, '../src/content/posts');
const PUBLIC_IMAGES_DIR = path.join(__dirname, '../public/images');
const ASSETS_IMAGES_DIR = path.join(__dirname, '../src/assets/images');
const SITE_URL = 'https://drhuanggi.vercel.app';
const GAS_URL  = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';

// 只需要新增這 2 篇
const TARGET_TITLES = [
  '想減重，要有氧還是重訓',
  '為什麼體重較重InBody肌肉量卻很高',
];

async function postToGAS(payload) {
  try {
    const res = await fetch(GAS_URL, {
      method: 'POST',
      redirect: 'follow',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload),
    });
    const text = await res.text();
    try { return JSON.parse(text); } catch { return { success: res.ok, raw: text }; }
  } catch (err) {
    return { success: false, error: err.message };
  }
}

const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
console.log('\n📋 準備新增 2 篇缺少的文章...\n');

for (const targetTitle of TARGET_TITLES) {
  // 找到對應的 md 檔
  let found = false;
  for (const f of mdFiles) {
    const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
    const t = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
    if (!t || t[1].trim() !== targetTitle) continue;

    found = true;
    const c       = content.match(/^category:\s*["']?(.+?)["']?\s*$/m);
    const slugM   = content.match(/^slug:\s*["']?(.+?)["']?\s*$/m);
    const coverM  = content.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);

    const category   = c ? c[1].trim() : '';
    const slug       = slugM ? slugM[1].trim() : path.basename(f, '.md');
    const cover      = coverM ? coverM[1].trim() : '';
    const articleUrl = `${SITE_URL}/posts/${slug}`;

    let imgUrl = '';
    if (cover) {
      let srcImg = path.join(PUBLIC_IMAGES_DIR, cover);
      if (!fs.existsSync(srcImg)) srcImg = path.join(ASSETS_IMAGES_DIR, cover);
      if (fs.existsSync(srcImg)) imgUrl = `${SITE_URL}/og-images/${encodeURIComponent(cover)}`;
    }

    console.log(`➡️  處理「${targetTitle}」`);
    console.log(`   分類：${category}`);
    console.log(`   網址：${articleUrl}`);

    const result = await postToGAS({
      action:     'appendRow',
      title:      targetTitle,
      category,
      articleUrl,
      imgUrl,
      sort:       999,
      type:       'article',
    });

    if (result.action === '新增成功') {
      console.log(`✅ 新增成功！\n`);
    } else if (result.action === '已存在略過') {
      console.log(`⭕ 已存在，略過\n`);
    } else {
      console.log(`❌ 失敗：${JSON.stringify(result)}\n`);
    }
    break;
  }
  if (!found) console.log(`⚠️  找不到「${targetTitle}」的 md 檔\n`);
}

console.log('='.repeat(50));
console.log('🌐 請開啟 Google Sheet 確認 2 篇是否已新增！');
