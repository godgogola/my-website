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

  [1/6] 同步 Obsidian 文章（新增 / 刪除 / 改標題 / 改排序）
  [2/6] 同步 Google Drive 圖片到網站
  [3/6] 自動配對封面圖（依圖片檔名對應文章）
  [4/6] 重新編譯網站（本機確認格式正確）
  [5/6] 將文章網址與圖片寫回 Google Sheet
  [6/6] 上傳到 Vercel，網站立即更新 🚀
```

> 📌 Vercel 在美國伺服器重新編譯 144 頁 + 100+ 張圖，需要約 10 分鐘，這是正常的。

---

## 🖼️ 新增文章圖片的流程

```
① 在診所製作好圖片（PNG / JPG / WebP）
   → 檔名必須與文章 title 完全一致
   → 例：文章 title 是「痛風常發作的部位」
          圖片檔名就是「痛風常發作的部位.png」
          ↓
② 上傳到 Google Drive：
   G:\我的雲端硬碟\衛教文章圖片\
          ↓
③ 等 Google Drive 自動同步到家裡電腦
          ↓
④ 雙擊「一鍵更新發布」→ 全部自動完成 🚀
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

## 🗑️ 刪除或修改文章

1. 直接在 **Obsidian** 裡刪除或修改
2. 雙擊「**Update-Website**」捷徑

腳本會自動偵測 Obsidian 的變動（刪除、改標題、改排序）並同步到網站。

> ⚠️ 注意：Obsidian 文章必須放在**分類子資料夾**裡，根目錄的 `.md` 不會被同步。

> 📌 **改了文章標題不用擔心圖片消失**：腳本會自動用舊標題找回原本的封面圖並繼承。

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
| 圖片沒有顯示 | 確認圖片已上傳到 `G:\我的雲端硬碟\衛教文章圖片\`，且檔名與 title 完全一致 |
| 改了文章標題後圖片消失 | 重新執行「Update-Website」即可，腳本會自動找回封面圖 |
| 文章分類錯誤 | 確認 Obsidian 文章有放在正確的分類子資料夾 |
| 網站改動後沒更新 | 等 10~15 分鐘後再看，Vercel 在雲端 build 需要時間 |
| Google Sheet 圖片沒更新 | 重新執行 `node scripts/sync-sheet.js` |
| 編譯失敗 | 請截圖黑色視窗的錯誤訊息給 AI 排查 |
| 點了兩次 Update-Website | 只要點一次！多次點擊會讓程序互相衝突。若誤點，聯絡 AI 排查 |

---

## 🧞 進階：手動指令速查

> 平常不需要用到，只有 bat 出錯或需要單獨執行某步驟時使用。

| 指令 | 說明 |
|------|------|
| `node scripts/sync-obsidian.js` | 同步 Obsidian 文章（新增 / 刪除 / 排序） |
| `node scripts/sync-drive-images.js` | 從 Google Drive 同步圖片到網站 |
| `node scripts/auto-cover-image-v2.js` | 自動配對封面圖到文章（依檔名比對） |
| `node scripts/sync-sheet.js` | 更新 Google Sheet 網址欄位 |
| `npm run dev` | 本機預覽（http://localhost:4321） |
| `npm run build` | 重新編譯網站 |
| `npx vercel --prod --yes` | 直接部署到 Vercel（緊急時使用） |
