/**
 * auto-sync-service.js
 * 
 * 自動監控 Obsidian 衛教文章庫與讀書筆記庫：
 * 當偵測到有新文章或章節移入/修改時，自動同步至本地專案並將標題新增至 Google Sheet！
 * 
 * 支援兩種模式：
 * 1. node scripts/auto-sync-service.js --check   (單次檢查，適合 Windows 工作排程器)
 * 2. node scripts/auto-sync-service.js --watch   (常駐背景監聽，每 60 秒或即時偵測變更)
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

// 讀取 .env
const envPath = path.join(projectRoot, '.env');
let obsidianPath = 'G:/我的雲端硬碟/衛教文章庫/衛教文章庫';
let booksPath = 'G:/我的雲端硬碟/讀書筆記庫/讀書筆記';

if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  const m1 = envContent.match(/^OBSIDIAN_VAULT_PATH\s*=\s*(.+)$/m);
  if (m1) obsidianPath = m1[1].trim().replace(/['"]/g, '');
  const m2 = envContent.match(/^BOOKS_VAULT_PATH\s*=\s*(.+)$/m);
  if (m2) booksPath = m2[1].trim().replace(/['"]/g, '');
}

const stateFile = path.join(__dirname, '.sync-state.json');
const logFile = path.join('C:/Users/X1 Yoga Gen7/Desktop', 'auto-sync.log');

function log(msg) {
  const line = `[${new Date().toLocaleString('zh-TW')}] ${msg}`;
  console.log(line);
  try {
    fs.appendFileSync(logFile, line + '\n', 'utf8');
  } catch (e) {}
}

// 遞迴取得所有 .md 檔案及其修改時間
function getFolderSnapshot(dir) {
  const snapshot = {};
  if (!fs.existsSync(dir)) return snapshot;

  function walk(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name.startsWith('.')) continue;
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        try {
          const stat = fs.statSync(fullPath);
          const relPath = path.relative(dir, fullPath).replace(/\\/g, '/');
          snapshot[relPath] = stat.mtimeMs;
        } catch (e) {}
      }
    }
  }

  walk(dir);
  return snapshot;
}

function hasChanges(prev, curr) {
  const prevKeys = Object.keys(prev);
  const currKeys = Object.keys(curr);
  if (prevKeys.length !== currKeys.length) return true;
  for (const k of currKeys) {
    if (!prev[k] || prev[k] !== curr[k]) return true;
  }
  return false;
}

export async function runCheck() {
  let state = { medical: {}, books: {} };
  if (fs.existsSync(stateFile)) {
    try {
      state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
    } catch (e) {}
  }

  const currMedical = getFolderSnapshot(obsidianPath);
  const currBooks = getFolderSnapshot(booksPath);

  const medicalChanged = hasChanges(state.medical || {}, currMedical);
  const booksChanged = hasChanges(state.books || {}, currBooks);

  if (!medicalChanged && !booksChanged) {
    return false;
  }

  log('⚡ 偵測到文章或讀書筆記目錄有變動，啟動自動同步管線...');

  if (booksChanged) {
    const prevCount = Object.keys(state.books || {}).length;
    const currCount = Object.keys(currBooks).length;
    log(`📚 讀書筆記變更 (前次 ${prevCount} 篇 ➜ 目前 ${currCount} 篇)，執行同步...`);
    try {
      execSync('node scripts/sync-books-content.js', { cwd: projectRoot, stdio: 'inherit' });
      execSync('node scripts/sync-books.js', { cwd: projectRoot, stdio: 'inherit' });
      log('✅ 讀書筆記已成功同步並新增至 Google Sheet！');
    } catch (err) {
      log('❌ 讀書筆記同步出錯: ' + err.message);
    }
  }

  if (medicalChanged) {
    const prevCount = Object.keys(state.medical || {}).length;
    const currCount = Object.keys(currMedical).length;
    log(`🩺 衛教文章變更 (前次 ${prevCount} 篇 ➜ 目前 ${currCount} 篇)，執行同步...`);
    try {
      execSync('node scripts/sync-obsidian.js', { cwd: projectRoot, stdio: 'inherit' });
      execSync('node scripts/add-missing-to-sheet.js', { cwd: projectRoot, stdio: 'inherit' });
      log('✅ 衛教文章已成功同步並新增至 Google Sheet！');
    } catch (err) {
      log('❌ 衛教文章同步出錯: ' + err.message);
    }
  }

  // 儲存狀態
  fs.writeFileSync(stateFile, JSON.stringify({
    medical: currMedical,
    books: currBooks,
    lastSync: new Date().toISOString()
  }, null, 2), 'utf8');

  log('🎉 自動同步程序完成！\n');
  return true;
}

// 主執行進入點
const isWatch = process.argv.includes('--watch');

if (isWatch) {
  log('🚀 啟動自動同步常駐監聽服務（每 60 秒巡檢 Google Drive 目錄）...');
  // 啟動先執行一次記錄或同步
  runCheck().catch(console.error);

  setInterval(() => {
    runCheck().catch(console.error);
  }, 60 * 1000);
} else {
  runCheck().catch(console.error);
}
