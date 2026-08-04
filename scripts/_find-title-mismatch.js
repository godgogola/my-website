/**
 * 找出 Markdown title 和 Google Sheet C 欄標題不一致的文章
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');
const GAS_URL = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';

// 讀取所有 md 文章 title
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
const mdTitles = new Map(); // title -> category
for (const f of mdFiles) {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const t = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const c = content.match(/^category:\s*["']?(.+?)["']?\s*$/m);
  const d = content.match(/^draft:\s*(.+)$/m);
  if (!t) continue;
  if (d && d[1].trim() === 'true') continue;
  mdTitles.set(t[1].trim(), c ? c[1].trim() : '');
}

// 從 GAS 拿 Sheet 所有 items 的 title
const res = await fetch(`${GAS_URL}?output=json`);
const categories = await res.json();

const sheetTitles = new Set();
for (const cat of categories) {
  for (const item of cat.items) {
    sheetTitles.add(item.title.trim());
  }
}

console.log('\n=== Markdown 有但 Sheet 找不到 (md title → 請在 Sheet C 欄確認) ===\n');
let count = 0;
for (const [title, category] of mdTitles) {
  if (!sheetTitles.has(title)) {
    console.log(`[${category}] ${title}`);
    count++;
  }
}
console.log(`\n共 ${count} 筆`);

console.log('\n=== Sheet 有但 Markdown 找不到 (sheet title → 可能已刪除或改名) ===\n');
let count2 = 0;
for (const t of sheetTitles) {
  if (!mdTitles.has(t)) {
    console.log(`  ${t}`);
    count2++;
  }
}
console.log(`\n共 ${count2} 筆`);
