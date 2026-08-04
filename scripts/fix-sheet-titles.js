/**
 * fix-sheet-titles.js
 * 
 * 把 Google Sheet 次分類 C 欄（標題）從舊標題更新為 Markdown 的新標題
 * 以 Obsidian/Markdown 的 title 為準
 * 
 * 使用方式：node scripts/fix-sheet-titles.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GAS_URL = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';

// 舊標題（Sheet C 欄）→ 新標題（Markdown title）對照表
const TITLE_MAP = {
  '上消化性潰瘍':                         '上消化道潰瘍',
  '巴瑞特氏食道炎':                        '巴瑞氏食道炎',
  '平穩血糖飲食策略':                      '平穩血糖上升的飲食與生活策略',
  '常見胃藥':                              '常見胃藥作機轉與服用建議',
  '常見止瀉劑':                            '常見止瀉藥',
  '常見軟便劑':                            '常見軟便藥',
  '懷孕期腸胃藥':                          '懷孕期間可使用的腸胃藥',
  '泌乳期腸胃藥':                          '泌乳期間可使用的腸胃藥物',
  '小兒腸胃用藥':                          '小兒常見腸胃用藥',
  '【P-CABs】鉀離子競爭性酸阻滯劑_新時代的胃藥': '【P-CABs】鉀離子競爭性酸阻滯劑',
  '合法減重藥':                            '台灣合法減重藥物',
  '目前合法減重藥物介紹':                  '台灣合法減重藥物',
  '胃內縫合術':                            '胃內縫合手術',
  '胃內肉毒注射':                          '胃肉毒減重',
  '糖尿病治療最新觀念-個人化治療與器官保護': '糖尿病治療新觀念-個人化治療與器官保護',
  '降糖血藥物之介紹':                       '降血糖藥物之機轉，優點及缺點',
  '降血糖藥物效果':                         '降血糖藥物療效與降幅',
  '腎功能':                                '心血管及腎功能檢查',
  '肝膽功能':                              '肝膽功能檢查',
  '血球檢查':                              '血液檢查',
  '內分泌及代謝':                           '內分泌及新陳代謝',
  '防治胃癌':                              '要如何防治胃癌，根除幽門桿菌',
  '【腸鏡前準備】保可淨':                   '【腸鏡前準備】(保可淨)',
  '【腸鏡前準備】耐福利散':                 '【腸鏡前準備】(耐福利散)',
};

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

console.log(`\n📋 共 ${Object.keys(TITLE_MAP).length} 筆標題需要修正，開始更新...\n`);

let fixed = 0, failed = 0;

for (const [oldTitle, newTitle] of Object.entries(TITLE_MAP)) {
  const result = await postToGAS({
    action:    'fixSheetTitle',
    oldTitle,
    newTitle,
  });

  if (result.action === '標題已更新') {
    console.log(`✅ 「${oldTitle}」→「${newTitle}」`);
    fixed++;
  } else if (result.action === '標題相同無需修改') {
    console.log(`⭕ 「${oldTitle}」已是新標題，略過`);
  } else if (result.action === '找不到舊標題') {
    console.log(`⚠️  找不到「${oldTitle}」，可能已修正`);
  } else {
    console.log(`❌ 失敗「${oldTitle}」: ${JSON.stringify(result)}`);
    failed++;
  }
}

console.log('\n' + '='.repeat(60));
console.log(`✅ 成功修正：${fixed} 筆`);
console.log(`❌ 失敗：${failed} 筆`);
console.log('\n🌐 請重新開啟 Google Sheet 確認 C 欄標題是否已更新！');
console.log('⚡ 接著執行 node scripts/fix-categories.js 修正剩餘文章的分類！');
