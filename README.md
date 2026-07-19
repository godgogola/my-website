# 個人網站 — 文章發布 SOP

🌐 **網站網址：[https://drhuanggi.vercel.app](https://drhuanggi.vercel.app)**

---

## ⚡ 最簡單的方法 — 雙擊一鍵執行

> 不想記指令？專案根目錄有兩個 `.bat` 檔案，雙擊即可自動執行！

```
📁 個人網站/
   ├── 更新文章.bat  ← 同步圖片 + 文章 + 配對封面圖（Step 0~3）
   └── 發布網站.bat  ← 一鍵打包並發布至網頁 (drhuanggi.vercel.app)
```

**使用方式：**
1. 雙擊 **`更新文章.bat`**：自動完成 Google Drive 圖片同步、Obsidian 文章同步、封面圖配對。
2. （選做）在 VS Code 輸入 `npm run dev` 在本機預覽確認。
3. 雙擊 **`發布網站.bat`**：一鍵完成打包 + 自動更新上線！

---

## 🖼️ Google Drive 圖片同步流程（新功能）

> 在診所電腦製作好圖片後，不需要手動複製，只要放入 Google Drive 即可！

### 完整作業流程

```
① 在診所電腦製作圖片
   → 存成正確檔名（例如：痛風常發作的部位.png）
           ↓
② 上傳到 Google Drive
   → G:\我的雲端硬碟\衛教文章圖片\
           ↓
③ 回到家，等 Google Drive 自動同步完成
           ↓
④ 雙擊「更新文章.bat」
   [0/3] 自動從 Google Drive 複製圖片到 src/assets/images/
         + 配對同名草稿文章 → coverImage 寫入、draft 改為 false
   [1/3] 同步 Obsidian 文章
   [2/3] 比對封面圖
   [3/3] 更新 Google Sheet 網址欄位
           ↓
⑤ 雙擊「發布網站.bat」→ 上線！🚀
```

### 📌 圖片命名規則

圖片的**檔名（不含副檔名）必須與文章 title 完全一致**：

| 文章 title | 圖片檔名 |
|-----------|---------|
| `痛風常發作的部位` | `痛風常發作的部位.png` |
| `食道裂孔疝氣的原因` | `食道裂孔疝氣的原因.jpg` |
| `為什麼會有墨綠色大便` | `為什麼會有墨綠色大便.png` |

支援格式：`.png` `.jpg` `.jpeg` `.webp`

---

## 📝 草稿機制（draft: true）

> 文章還在修改中，或圖片尚未製作好時，加上 `draft: true` 保護它不被自動處理。

### 設定草稿

在文章的 frontmatter 加上：
```yaml
---
title: "食道裂孔疝氣的原因"
draft: true
slug: "食道裂孔疝氣的原因"
---
```

### 草稿的行為
- ✅ 文章頁面正常存在，可在網站上瀏覽
- ⏭ `auto-cover-image-v2.js` **跳過**，不會自動配錯誤的封面圖
- ⏭ `sync-sheet.js` **跳過**，不會更新 Google Sheet 網址欄位

### 圖片製作好後，手動解除草稿

把 `.md` 裡的 frontmatter 改成：
```yaml
---
title: "食道裂孔疝氣的原因"
draft: false
coverImage: "食道裂孔疝氣的原因.png"
slug: "食道裂孔疝氣的原因"
---
```
然後執行 `更新文章.bat` → 自動同步到 Google Sheet。

> 💡 **更快的方法**：把圖片上傳到 Google Drive 的「衛教文章圖片」資料夾，
> `更新文章.bat` 會自動幫您把 `draft: true` 改成 `false` 並寫入 `coverImage`！

---

## 📋 完整手動流程（進階參考）

> 所有指令都在 **VS Code 終端機**（專案根目錄）執行。

### Step 0｜同步 Google Drive 圖片（新）
```sh
node scripts/sync-drive-images.js
```
- 從 `G:\我的雲端硬碟\衛教文章圖片\` 自動複製圖片到 `src/assets/images/`。
- 自動配對同名草稿文章，寫入 `coverImage` 並將 `draft: true` 改為 `draft: false`。

---

### Step 1｜在 Obsidian 撰寫文章
- 將 `.md` 檔案放入 Google 雲端硬碟的**分類資料夾**中。
- 資料夾名稱 = 網站上的文章分類（例如：`肝膽胃腸`、`糖尿病` 等）。
- 不需要寫 YAML，純內文即可。

> **選擇性：** 可在文章最上方手動加入 frontmatter 指定標題或日期：
> ```yaml
> ---
> title: "你的文章標題"
> publishDate: "2026-07-15"
> draft: false
> ---
> ```

---

### Step 2｜同步 Obsidian → 網站
```sh
node scripts/sync-obsidian.js
```
- 自動讀取 Google 雲端硬碟並生成文章的 frontmatter。
- 將文章同步複製到本專案的 `src/content/posts/` 資料夾。

---

### Step 3｜自動配對封面圖片
```sh
node scripts/auto-cover-image-v2.js
```
- 根據文章標題，自動去比對 `src/assets/images/` 底下的圖片。
- 比對成功後，會自動在文章中寫入 `coverImage: "圖片名稱.png"`。
- **已配對過封面圖的文章會自動跳過**，不會重複比對。
- **草稿文章（`draft: true`）會自動跳過**，等圖片備妥再手動解除。

---

### Step 4｜本地預覽確認
```sh
npm run dev
```
> **💡 備用方案：** 如果在 VS Code 終端機無法輸入或沒有反應，請改用：
> ```sh
> node start-dev-scratch.js
> ```

啟動後，打開瀏覽器確認：👉 **[http://localhost:4321](http://localhost:4321)**

- ✅ 確認最新衛教文章有出現在首頁。
- ✅ 確認文章標題、分類正確。
- ✅ 點進去確認封面圖片是否正常顯示，排版是否無誤。

---

### Step 5｜建置並上線 🚀

**① 先打包建置：**
```sh
npm run build
```
- Astro 壓縮引擎會自動把 `src/assets/images/` 裡的大圖壓縮為超輕量 `.webp` 格式（節省 95% 以上流量！）。
- 自動生成最新 `sitemap-index.xml` 提供給 Google 搜尋引擎。

**② 上傳至 Vercel（正式上線）：**
```sh
npx vercel dist --prod --yes
```
- 將打包好的 `dist/` 資料夾直接上傳到 Vercel 雲端。
- 完成後網站立即更新：👉 **https://drhuanggi.vercel.app**

**③ 備份到 GitHub（建議每次都做）：**
```sh
git add .
git commit -m "新增文章：文章名稱"
git push origin main
```

---

## 🗺️ 完整流程圖

```
[診所] 製作圖片 → 上傳到 Google Drive「衛教文章圖片」資料夾
                            ↓（Google Drive 自動同步到家裡電腦）
node scripts/sync-drive-images.js  （複製圖片、解除草稿）
                            ↓
node scripts/sync-obsidian.js      （同步 Obsidian 文章）
                            ↓
node scripts/auto-cover-image-v2.js（模糊比對封面圖）
                            ↓
npm run dev → 瀏覽器 localhost:4321 確認
                            ↓
npm run build → 打包壓縮所有圖片與頁面
                            ↓
npx vercel dist --prod --yes → 上傳至 Vercel，網站立即更新 🚀
                            ↓
git add . && git commit -m "..." && git push origin main → GitHub 備份
```

---

## 🗑️ 刪除文章流程

為了避免下次同步時舊文章又跑回來，刪除文章時請遵照以下步驟：
```
1. 刪除 Google 雲端硬碟（Obsidian）資料夾裡的原始 .md 檔
         ↓
2. 刪除專案中 src/content/posts/ 裡對應的 .md 檔
         ↓
3. 執行 npm run build → npx vercel dist --prod --yes → 重新部署
```

---

## ⚙️ 環境設定

設定在專案根目錄的 `.env` 檔案：
```env
# Obsidian 文章來源（Google Drive）
OBSIDIAN_VAULT_PATH=G:/我的雲端硬碟/Wix衛教文章

# Google Drive 圖片資料夾（sync-drive-images.js 使用）
# 路徑已寫死在 scripts/sync-drive-images.js 的 DRIVE_IMAGES_DIR 變數
# 預設：G:\我的雲端硬碟\衛教文章圖片
```

---

## ⚠️ 常見問題與排除

| 狀況 | 處理方式 |
|---|---|
| 圖片無法從 Google Drive 複製 | 確認 Google Drive 已掛載（G 槽），且「衛教文章圖片」資料夾存在 |
| 圖片複製後草稿沒有自動解除 | 確認圖片檔名（不含副檔名）與文章 title **完全一致** |
| 封面圖片找不到 | 手動在文章 frontmatter 加上 `coverImage: "圖片名稱.png"` |
| 文章分類錯誤 | 確認 Google 雲端硬碟中的文章，是否有放在正確的分類資料夾中 |
| 根目錄文章不同步 | 腳本只會處理分類資料夾內的文章，請務必將文章歸類 |
| 終端機不能輸入 | 請改用 `node start-dev-scratch.js` 來啟動開發伺服器 |

---

## 🧞 常用指令速查表

| 指令 | 說明 |
|---|---|
| `node scripts/sync-drive-images.js` | **🖼️ 從 Google Drive 同步圖片並自動配對草稿文章** |
| `node scripts/sync-obsidian.js` | 同步 Obsidian 最新文章 |
| `node scripts/auto-cover-image-v2.js` | 自動配對封面圖片 |
| `node scripts/sync-sheet.js` | 更新 Google Sheet 網址欄位 |
| `npm run dev` | 啟動開發伺服器（預設） |
| `node start-dev-scratch.js` | **備用** 啟動開發伺服器（終端機卡住時用） |
| `npm run build` | 建置正式發布版本（自動壓縮圖片並生成 Sitemap） |
| `npx vercel dist --prod --yes` | **🚀 上傳至 Vercel，立即更新網站** |
| `npm run preview` | 本地預覽正式建置結果 |
| `git add . && git commit -m "說明" && git push origin main` | 備份到 GitHub |
