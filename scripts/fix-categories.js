/**
 * fix-categories.js
 * 
 * 讀取所有 Markdown 文章的 category 欄位，
 * 自動批次呼叫 GAS 修正 Google Sheet 次分類工作表 A 欄（主分類名稱）。
 * 
 * 使用方式：node scripts/fix-categories.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const POSTS_DIR = path.join(__dirname, '../src/content/posts');
const GAS_URL   = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';

// 讀取所有文章的 title 和 category
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
const articles = [];

for (const f of mdFiles) {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const titleMatch    = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const categoryMatch = content.match(/^category:\s*["']?(.+?)["']?\s*$/m);
  const draftMatch    = content.match(/^draft:\s*(.+)$/m);

  if (!titleMatch) continue;
  if (draftMatch && draftMatch[1].trim() === 'true') continue;

  articles.push({
    title:    titleMatch[1].trim(),
    category: categoryMatch ? categoryMatch[1].trim() : '',
  });
}

console.log(`\n📋 共讀取 ${articles.length} 篇文章，開始修正 Google Sheet 分類...\n`);

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

(async () => {
  let fixedCount   = 0;
  let correctCount = 0;
  let notFound     = 0;

  const BATCH_SIZE = 5;
  for (let i = 0; i < articles.length; i += BATCH_SIZE) {
    const batch = articles.slice(i, i + BATCH_SIZE);
    await Promise.all(
      batch.map(async (article) => {
        if (!article.category) return;
        const result = await postToGAS({
          action:   'fixCategory',
          title:    article.title,
          category: article.category,
        });

        if (result.action === '分類已修正') {
          console.log(`✅ 已修正「${article.title}」: ${result.from} → ${result.to}`);
          fixedCount++;
        } else if (result.action === '分類正確無需修正') {
          console.log(`⭕ 正確「${article.title}」: ${article.category}`);
          correctCount++;
        } else if (result.action === '未找到標題') {
          console.log(`⚠️  找不到「${article.title}」（可能標題不一致）`);
          notFound++;
        } else {
          console.log(`❌ 錯誤「${article.title}」: ${JSON.stringify(result)}`);
        }
      })
    );
  }

  console.log('\n' + '='.repeat(60));
  console.log(`✅ 已修正：${fixedCount} 筆`);
  console.log(`⭕ 原本正確：${correctCount} 筆`);
  console.log(`⚠️  找不到標題（標題不一致）：${notFound} 筆`);
  console.log('\n🌐 請重新開啟 Google Sheet 確認分類是否已更正！');
})();
