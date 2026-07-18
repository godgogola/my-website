# 個人網站 — 文章發布 SOP

🌐 **網站網址：[https://drhuanggi.vercel.app](https://drhuanggi.vercel.app)**

---

## ⚡ 最簡單的方法 — 雙擊一鍵執行

> 不想記指令？專案根目錄有一個 **`更新文章.bat`** 檔案，雙擊它就會自動完成 Step 2 + Step 3！

```
📁 個人網站/
   └── 更新文章.bat  ← 雙擊這個！
```

雙擊後會自動依序執行：
- ✅ 同步 Obsidian 文章（sync-obsidian.js）
- ✅ 自動配對封面圖片（auto-cover-image-v2.js）

完成後再回到 VS Code 執行 `npm run dev` 預覽，確認沒問題就執行 Step 5 上線！

---

## 📋 完整手動流程（進階參考）

> 所有指令都在 **VS Code 終端機**（專案根目錄）執行。如果終端機無法輸入或沒反應，請參考下方【常見問題】使用備用指令。

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
- 根據文章標題，自動去比對 `src/assets/images/` 底下的圖片（新版壓縮引擎路徑）。
- 比對成功後，會自動在文章中寫入 `coverImage: "圖片名稱.png"`。
- **已配對過封面圖的文章會自動跳過**，不會重複比對。

---

### Step 4｜本地預覽確認
在終端機輸入：
```sh
npm run dev
```
> **💡 備用方案：** 如果在 VS Code 終端機無法輸入或沒有反應，請改用以下指令啟動：
> ```sh
> node start-dev-scratch.js
> ```

啟動後，打開瀏覽器進入以下網址確認：
👉 **[http://localhost:4321](http://localhost:4321)**

- ✅ 確認最新衛教文章有出現在首頁。
- ✅ 確認文章標題、分類正確。
- ✅ 點進去確認封面圖片是否正常顯示，排版是否無誤。

---

### Step 5｜建置並上線 🚀（每次更新都要做）

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
- 完成後網站立即更新，可到以下網址查看：
  👉 **https://drhuanggi.vercel.app**

**③ 備份到 GitHub（建議每次都做）：**
```sh
git add .
git commit -m "新增文章：文章名稱"
git push origin main
```

---

## 🗺️ 流程圖

```
Obsidian 文章移入分類資料夾
           ↓
node scripts/sync-obsidian.js  （同步 Obsidian 文章）
           ↓
node scripts/auto-cover-image-v2.js （模糊比對 src/assets/images 圖片）
           ↓
npm run dev（或 node start-dev-scratch.js）→ 瀏覽器 localhost:4321 確認
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

Obsidian 來源路徑設定在專案根目錄的 `.env` 檔案中：
```env
OBSIDIAN_VAULT_PATH=G:/我的雲端硬碟/Wix衛教文章
```

---

## ⚠️ 常見問題與排除

| 狀況 | 處理方式 |
|---|---|
| 封面圖片找不到 | 手動在文章最上方的 frontmatter 加上 `coverImage: "圖片名稱.png"`（注意：圖片需存在 `src/assets/images/` 中）。 |
| 文章分類錯誤 | 確認 Google 雲端硬碟中的文章，是否有放在正確的分類資料夾中。 |
| 根目錄文章不同步 | 腳本只會處理分類資料夾內的文章，請務必將文章歸類。 |
| 終端機不能輸入 | 請改用 `node start-dev-scratch.js` 來啟動開發伺服器。 |

---

## 🧞 常用指令速查表

| 指令 | 說明 |
|---|---|
| `node scripts/sync-obsidian.js` | 同步 Obsidian 最新文章 |
| `node scripts/auto-cover-image-v2.js` | 自動配對封面圖片 (比對 `src/assets/images/`) |
| `npm run dev` | 啟動開發伺服器 (預設) |
| `node start-dev-scratch.js` | **備用** 啟動開發伺服器 (當終端機卡住時使用) |
| `npm run build` | 建置正式發布版本 (自動壓縮圖片並生成 Sitemap) |
| `npx vercel dist --prod --yes` | **🚀 上傳至 Vercel，立即更新網站** |
| `npm run preview` | 本地預覽正式建置結果 |
| `git add . && git commit -m "說明" && git push origin main` | 備份到 GitHub |
