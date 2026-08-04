# 個人網站 — 文章發布與維護 SOP

🌐 **網站網址：[https://drhuanggi.vercel.app](https://drhuanggi.vercel.app)**

---

## ⚡ 日常更新只需一個動作

> 在 Obsidian 新增、修改、刪除文章，或在 Google Drive 上傳圖片之後：

**雙擊桌面上的「Update-Website」捷徑**

它會自動完成以下所有步驟，完成後視窗顯示「完成！」按任意鍵關閉，
約 **10~15 分鐘後** [drhuanggi.vercel.app](https://drhuanggi.vercel.app) 就會更新。

```
一鍵更新發布.bat  （位於：個人網站/ 資料夾內，桌面有捷徑）

  [1/7] 同步 Obsidian 文章（新增 / 刪除 / 改標題 / 改排序）
  [2/7] 同步 Google Drive 圖片到網站（PNG → WebP 壓縮）
  [3/7] 套用手動封面圖對應表（cover-mapping.json）
  [4/7] 自動模糊配對剩餘封面圖
  [5/7] 重新編譯網站（本機確認格式正確）
  [6/7] 將文章網址與圖片寫回 Google Sheet
  [7/7] 上傳到 Vercel，網站立即更新 🚀
```

> 📌 Vercel 在美國伺服器重新編譯 150+ 頁 + 100+ 張圖，需要約 10 分鐘，這是正常的。

---

## 🖼️ 新增或更換文章圖片 SOP

### 方式一：請 Antigravity AI 批次生圖 / 一條龍處理（最推薦、最省力 ⭐）

**無論是「寫新文章做新圖」還是「舊文章替換新圖」，操作完全一樣！**

只需要在 Antigravity 對話框輸入：

> 「請幫我為以下這幾篇文章生成全新封面圖：[貼上標題清單]」

Antigravity 會自動完成一條龍作業：
1. **AI 視覺生成**：繪製高品質專屬封面圖。
2. **高畫質原圖備份**：備份 PNG 高畫質原圖至 `G:\我的雲端硬碟\衛教文章圖片\`。
3. **網頁最佳化轉檔**：自動轉為輕量 WebP 檔存入網站圖片庫，確保開啟速度快。
4. **自動綁定與編譯驗證**：更新文章 `coverImage` 欄位並通過本機 build 測試。

---

### 方式二：自己製作圖片上傳（手動）

```
① 製作好圖片（PNG / JPG / WebP）
   → 檔名建議與文章 title 欄位一致
          ↓
② 上傳到 Google Drive：
   G:\我的雲端硬碟\衛教文章圖片\
          ↓
③ 等 Google Drive 自動同步到家裡電腦
          ↓
④ 雙擊「一鍵更新發布」→ 全部自動完成 🚀
```

---

## ✏️ 改了文章標題怎麼辦？

> **在 Obsidian 修改文章標題時，您完全不需要手動改圖片檔名！**

1. 直接在 Obsidian 放心修改文章檔名或 `title:` 欄位。
2. 累積一陣子或覺得有需要時，在對話框跟我說一聲：
   > **「幫我檢查/補齊封面圖片」**
3. AI 會有自動化修復腳本，一次幫您抓出所有改名文章並自動配對綁定封面。

---

## 📌 文章排序規則說明

- **衛教專欄「全部」分類**：
  - 文章排序**純粹依據發布日期 (`publishDate`) 由新到舊**排列（最新發布的文章會在最上面）。
- **特定主題分類（如：內視鏡檢查、肝病特區...）**：
  - 優先依自訂 `order` 序號 (由小到大) 排序，次要依發布日期由新到舊排序。

---

## 🔍 Google 搜尋標題與圖示 (SEO & Favicon)

- **首頁標題**：`黃冠智醫師｜肝膽腸胃科·豐田診所院長｜衛教專區與健康筆記`
- **衛教專欄頁標題**：`衛教專欄｜胃腸鏡、減重與三高控制筆記 - 黃冠智醫師`
- **個別文章頁標題**：`[文章題目] | 黃冠智醫師`
- **Google 搜尋圖示 (Favicon)**：
  - **動態湖水藍·內視鏡海龜專屬徽章**
  - 包含 Google 搜尋規範 48x48px PNG、192x192px PNG、Apple Touch Icon 與 favicon.ico。
- **Google 醫師結構化標籤 (Schema.org JSON-LD)**：
  - 已嵌入 `Physician` 專用結構化數據，幫助 Google 建立醫師專業知識卡片。

---

## 🗑️ 刪除或修改文章

1. 直接在 **Obsidian** 裡刪除或修改
2. 雙擊「**Update-Website**」捷徑

腳本會自動偵測 Obsidian 的變動（刪除、改標題、改排序）並同步到網站。

> ⚠️ 注意：Obsidian 文章必須放在**分類子資料夾**裡，根目錄的 `.md` 不會被同步。

---

## ⚙️ 環境設定

設定在專案根目錄的 `.env` 檔案：
```env
OBSIDIAN_VAULT_PATH=G:/我的雲端硬碟/Wix衛教文章
```

圖片資料夾路徑（固定寫在腳本裡）：
```
G:\我的雲端硬碟\衛教文章圖片\
```

---

## ⚠️ 常見問題

| 狀況 | 處理方式 |
|------|--------|
| 文章刪了但網站還有 | 確認是否在 Obsidian 分類資料夾內刪除，然後執行「Update-Website」 |
| 圖片沒有顯示 | 確認圖片已上傳到 Drive，且檔名與 title 一致，或請 AI 執行自動配對 |
| 改了文章標題後圖片沒對上 | 在對話中請 AI 執行「檢查/補齊封面圖片」自動完成對應 |
| 文章分類錯誤 | 確認 Obsidian 文章有放在正確的分類子資料夾 |
| 網站改動後沒更新 | 等 10~15 分鐘後再看，Vercel 在雲端 build 需要時間 |
| Google Sheet 圖片沒更新 | 重新執行 `node scripts/sync-sheet.js` |
| Google 搜尋圖示還沒變 | Google 爬蟲需數天至一週重新索引，上線後會自動替換 |
| 編譯失敗 | 請截圖黑色視窗的錯誤訊息給 Antigravity 排查 |
| 點了兩次 Update-Website | 只要點一次！多次點擊會讓程序互相衝突。若誤點，聯絡 Antigravity 排查 |

---

## 🧞 進階：手動指令速查

> 平常不需要用到，只有 bat 出錯或需要單獨執行某步驟時使用。

| 指令 | 說明 |
|------|------|
| `node scripts/sync-obsidian.js` | 同步 Obsidian 文章（新增 / 刪除 / 排序） |
| `node scripts/sync-drive-images.js` | 從 Google Drive 同步圖片到網站（PNG → WebP） |
| `node scripts/apply-mapping.js` | 套用 cover-mapping.json 封面對應表 |
| `node scripts/auto-cover-image-v2.js` | 自動模糊配對封面圖到文章 |
| `node scripts/rename-drive-images.js` | 批次重新命名 Drive 圖片（改標題後使用） |
| `node scripts/update-cover-mapping.js` | 更新 cover-mapping.json 圖片名稱 |
| `node scripts/sync-sheet.js` | 更新 Google Sheet 網址欄位 |
| `npm run dev` | 本機預覽（http://localhost:4321） |
| `npm run build` | 重新編譯網站 |
| `npx vercel --prod --yes` | 直接部署到 Vercel（緊急時使用） |

---

## 💻 換電腦 / 電腦壞掉的恢復步驟

> ✅ **網站不會下線** — 網站跑在 Vercel 上，和本機無關。

### 資料備份在哪裡？

| 資料 | 備份位置 |
|------|--------|
| 程式碼 + 文章 + 圖片 | ✅ GitHub（每次一鍵更新都會自動同步） |
| 原始 PNG 圖片 | ✅ Google Drive → `衛教文章圖片/` |
| Obsidian 文章原稿 | ✅ Google Drive → `Wix衛教文章/` |
| 已上線網站 | ✅ Vercel（持續運作中） |

### 換機清單（依序執行）

```
① 安裝軟體：
   - Node.js (https://nodejs.org)
   - Git (https://git-scm.com)
   - Google Drive 桌面版（等待雲端資料同步完成）

② Clone 專案：
   git clone https://github.com/godgogola/my-website.git
   cd my-website

③ 安裝套件：
   npm install

④ 建立 .env 檔（在專案根目錄新建 .env 檔，貼入以下內容）：
   OBSIDIAN_VAULT_PATH=G:/我的雲端硬碟/Wix衛教文章

⑤ 登入 Vercel：
   npx vercel login

⑥ 建立桌面捷徑：
   node scripts/_make_shortcuts.js

⑦ 完成！雙擊「Update-Website」捷徑即可正常使用 🚀
```
