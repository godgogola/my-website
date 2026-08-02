# 個人網站 — 文章發布 SOP

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

## 🖼️ 新增文章圖片的流程

### 方式一：自己製作圖片（手動）

```
① 製作好圖片（PNG / JPG / WebP）
   → 檔名必須與文章 title 欄位完全一致（詳見下方命名規則）
          ↓
② 上傳到 Google Drive：
   G:\我的雲端硬碟\衛教文章圖片\
          ↓
③ 等 Google Drive 自動同步到家裡電腦
          ↓
④ 雙擊「一鍵更新發布」→ 全部自動完成 🚀
```

### 方式二：請 Antigravity AI 批次生圖（自動，推薦）

不需要手動製作圖片！只需在 Antigravity 對話框輸入：

> 「請幫我用毛線風格生成這幾篇文章的封面圖：[貼上標題清單]」

Antigravity 會自動：
1. 套用**毛線編織（Amigurumi）風格**提示詞，生成 16:9 封面圖
2. 存到 `G:\我的雲端硬碟\衛教文章圖片\`（檔名 = 文章標題）
3. 執行同步，轉為 WebP 並更新文章封面

之後再按「一鍵更新發布」即可上線。

---

### 📌 圖片命名規則（重要！）

圖片的**檔名（不含副檔名）必須與文章 frontmatter 的 `title` 欄位完全一致**：

| 文章 `title` | 圖片檔名 |
|-------------|---------|
| `【大腸癌】大腸癌危險因子` | `【大腸癌】大腸癌危險因子.png` |
| `【地雷食物】高三酸甘油脂地雷食物` | `【地雷食物】高三酸甘油脂地雷食物.png` |
| `痛風常發作的部位` | `痛風常發作的部位.png` |

支援格式：`.png` `.jpg` `.jpeg` `.webp`

---

## ✏️ 改了文章標題怎麼辦？

> ⚠️ 改標題後，Drive 圖片名稱也必須跟著改，否則同步時封面會被自動清除！

### 自己手動處理：
1. 在 Obsidian 改好文章的 `title:` 欄位
2. 去 `G:\我的雲端硬碟\衛教文章圖片\`，找到舊圖，**重新命名成新標題**
3. 按「一鍵更新發布」

### 請 Antigravity 幫你處理（推薦）：
直接在對話框說：
> 「文章『舊標題』改標題成『新標題』，請幫我更新圖片檔名」

Antigravity 會自動幫你重新命名 Drive 圖片、更新設定檔，全部搞定。

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
| 圖片沒有顯示 | 確認圖片已上傳到 Drive，且**檔名與 title 完全一致** |
| 改了文章標題後圖片消失 | 需同步**重新命名 Drive 上的圖片**，或請 Antigravity 幫你處理 |
| 文章分類錯誤 | 確認 Obsidian 文章有放在正確的分類子資料夾 |
| 網站改動後沒更新 | 等 10~15 分鐘後再看，Vercel 在雲端 build 需要時間 |
| Google Sheet 圖片沒更新 | 重新執行 `node scripts/sync-sheet.js` |
| 編譯失敗 | 請截圖黑色視窗的錯誤訊息給 Antigravity 排查 |
| 點了兩次 Update-Website | 只要點一次！多次點擊會讓程序互相衝突。若誤點，聯絡 Antigravity 排查 |
| Vercel 部署出現「檔案被佔用」 | OneDrive 或防毒軟體鎖住 dist/ 資料夾，不影響部署，再跑一次即可 |

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

> 📌 如果 Google Drive 掛載磁碟機字母不是 `G:`，請修改 `.env` 的路徑。
