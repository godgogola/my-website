/**
 * add-missing-to-sheet.js
 * 
 * 把 Markdown 有但 Google Sheet 完全沒有的文章，自動新增到次分類工作表
 * 使用方式：node scripts/add-missing-to-sheet.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR         = path.join(__dirname, '../src/content/posts');
const PUBLIC_IMAGES_DIR = path.join(__dirname, '../public/images');
const ASSETS_IMAGES_DIR = path.join(__dirname, '../src/assets/images');
const SITE_URL          = 'https://drhuanggi.vercel.app';
const GAS_URL           = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';

// 從 GAS 取得目前 Sheet 所有標題
const res = await fetch(`${GAS_URL}?output=json`);
const categories = await res.json();
const sheetTitles = new Set();
for (const cat of categories) {
  for (const item of cat.items) {
    sheetTitles.add(item.title.trim());
  }
}

// 讀取所有 md 文章
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
const missing = [];

for (const f of mdFiles) {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const t = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const c = content.match(/^category:\s*["']?(.+?)["']?\s*$/m);
  const d = content.match(/^draft:\s*(.+)$/m);
  const slugM = content.match(/^slug:\s*["']?(.+?)["']?\s*$/m);
  const coverM = content.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);

  if (!t) continue;
  if (d && d[1].trim() === 'true') continue;

  const title = t[1].trim();
  if (sheetTitles.has(title)) continue; // 已存在，略過

  const category   = c ? c[1].trim() : '';
  const slug       = slugM ? slugM[1].trim() : path.basename(f, '.md');
  const cover      = coverM ? coverM[1].trim() : '';
  const articleUrl = `${SITE_URL}/posts/${slug}`;

  // 找封面圖
  let imgUrl = '';
  if (cover) {
    let srcImg = path.join(PUBLIC_IMAGES_DIR, cover);
    if (!fs.existsSync(srcImg)) srcImg = path.join(ASSETS_IMAGES_DIR, cover);
    if (fs.existsSync(srcImg)) {
      imgUrl = `${SITE_URL}/og-images/${encodeURIComponent(cover)}`;
    }
  }

  missing.push({ title, category, slug, articleUrl, imgUrl });
}

if (missing.length === 0) {
  console.log('\n✅ 所有文章都已在 Google Sheet，無需新增！');
  process.exit(0);
}

console.log(`\n📋 共找到 ${missing.length} 篇文章需要新增到 Sheet：\n`);
for (const a of missing) {
  console.log(`  [${a.category}] ${a.title}`);
}
console.log();

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

let added = 0, failed = 0;

// 逐一新增（避免並行衝突）
for (const article of missing) {
  const result = await postToGAS({
    action:     'appendRow',
    title:      article.title,
    category:   article.category,
    articleUrl: article.articleUrl,
    imgUrl:     article.imgUrl,
    sort:       999,
    type:       'article',
  });

  if (result.action === '新增成功') {
    console.log(`✅ 已新增「${article.title}」→ 分類：${article.category}`);
    added++;
  } else if (result.action === '已存在略過') {
    console.log(`⭕ 已存在「${article.title}」，略過`);
  } else {
    console.log(`❌ 新增失敗「${article.title}」: ${JSON.stringify(result)}`);
    failed++;
  }

  // 每筆間隔 500ms，避免 GAS 超時
  await new Promise(r => setTimeout(r, 500));
}

console.log('\n' + '='.repeat(60));
console.log(`✅ 成功新增：${added} 筆`);
console.log(`❌ 失敗：${failed} 筆`);
console.log('\n🌐 請重新開啟 Google Sheet 確認新增列是否出現！');
