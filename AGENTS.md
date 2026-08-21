# 專案規範與 AI 記憶設定 (AGENTS.md)

## 🎨 文章封面圖生成規範 (Cover Image Prompt Rule)

當使用者要求「生成文章封面圖」或「批次生成文章封面圖」時，**必須 100% 統一使用以下【地雷食物系列】最高標準規格，徹底達到原生 16:9 的豐富橫向構圖**：

---

### 🌟 滿分黃金範本：【地雷食物系列】(1400x781 / 16:9)
* **視覺風格**：可愛手作 3D 針織毛線娃娃 (Cute 3D knitted crochet amigurumi plush doll)。
* **材質與質感**：細緻手作毛線紋理、羊毛質感、溫馨柔和的工作室燈光 (Hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft lighting)。
* **原生 16:9 構圖核心規範**：
  1. **女醫師採「坐姿 / 半身 / 緊密置中」**：
     * 女醫師娃娃為坐姿、半身或小巧微型人偶，**身旁緊密圍繞主題器官玩偶與情境道具**。
     * 絕不全身筆直高高站立貫穿上下邊界，人物高度舒適維持在畫面中央。
  2. **橫向豐富桌面陳列 (Rich Horizontal Tabletop Cluster)**：
     * 主體與道具緊密聚集在木質桌面/毛氈地毯正中央，左右橫向展開（如食物玩偶排開、天秤、台階、藥盒等），畫面豐富、飽滿又有故事性。
  3. **四周均勻呼吸留白 (Generous 4-Side Margins)**：
     * 畫面頂部保留寬闊的空白毛氈背景牆。
     * 畫面底部保留充足的毛氈地毯與木質桌面。
     * 整體畫面呈現原生 16:9 的精緻橫向陳列，頭頂、頭髮、手部道具與桌面**完全在畫面正中央，100% 絕不貼邊**。
  4. **嚴格禁止文字與字母 (ABSOLUTELY NO TEXT / LETTERS)**：
     * 所有道具（如少鹽罐、藥瓶、牛奶盒、餐盒）一律維持純毛線編織紋理，**絕對不能出現任何英文字母或標籤 (No text, no words, no letters on any props)**。

---

### 📝 標準通用 Prompt 範本 (Master Prompt Template)

未來生成任何封面圖時，直接套用此範本填入主題：

```text
Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS ON ANY PROPS. Rich tabletop diorama wide horizontal 16:9 scene matching the food series: A cute chibi female doctor amigurumi doll (sitting or half-body, centered comfortably) is closely surrounded by a rich, cute horizontal cluster of [主題道具與可愛器官/食物玩偶描述]. Positioned in the middle with generous breathing margins on all 4 sides (top, bottom, left, right). 16:9 widescreen diorama composition, 100% completely intact.
```

---

### 生成與發布 SOP (自動化處理)
1. **生圖 (地雷食物系列 16:9 規格)**：依主題生成符合上述「坐姿/半身、豐富桌面橫向陳列、四周充足留白」的 16:9 圖片。
2. **原圖備份**：將 16:9 PNG 備份至 `G:\我的雲端硬碟\衛教文章圖片\<Title>.png`。
3. **WebP 轉檔發布**：將 16:9 圖片轉檔為高品質 WebP，**同時存入 `public/images/<Title>.webp` 與 `public/og-images/<Title>.webp`**（確保 Google Sheet / LINE 官方帳號圖文選單之圖片自動無縫更新為最新版）。
4. **綁定與驗證**：更新 Markdown 的 `coverImage` 欄位並執行 `npm run build` 驗證。

---

## 🔄 自動化管線架構說明 (Automation Pipeline)

> **AI 必讀**：在修改任何 Obsidian 筆記、`.md` 檔案、或 scripts/ 內的腳本前，務必先理解以下架構，避免破壞自動化流程。

### 核心流程
```
Obsidian Vault (.md 筆記)
    ↓  node scripts/sync-obsidian.js
src/content/posts/ (處理後的 .md)
    ↓  npm run build (Astro)
網站上線
```

### sync-obsidian.js 的運作邏輯
- **來源**：從 `.env` 中的 `OBSIDIAN_VAULT_PATH` 讀取 Obsidian 資料庫路徑
- **分類規則**：**以資料夾名稱為分類**（例如放在「胃部疾病」資料夾 → `category: "胃部疾病"`）
- **跳過規則**：根目錄文章、`.obsidian/`、`.git/`、`node_modules/` 資料夾一律跳過
- **封面圖保護**：sync 時會保留現有 `coverImage` 欄位，不會覆蓋已設定的封面圖
- **刪除同步**：Obsidian 中刪除的文章，下次 sync 後網站也會自動刪除

### 網站 Frontmatter 必要欄位 (content.config.ts)
```yaml
---
title: "文章標題"
category: "分類名稱"      # 必填，由資料夾名稱自動決定
publishDate: "2026-01-01" # 必填
draft: false              # true = 草稿不上線
slug: "url-slug"          # 自動由標題產生
coverImage: "xxx.webp"    # 選填，封面圖檔名
order: 1                  # 選填，排序序號
---
```

---

## 🛡️ Obsidian 外掛安全規則 (Plugin Safety Rules)

> **AI 必讀**：建議安裝 Obsidian 外掛前，必須確認該外掛是否會修改 `.md` 檔案內容，因為 `sync-obsidian.js` 會直接讀取這些檔案並推送至網站。

### ✅ 絕對安全的外掛（不修改 .md 檔案）
- **主題類**：AnuPpuccin、Minimal Theme、Style Settings、Hider
- **視覺工具**：Graph Analysis、Strange New Worlds
- **獨立檔案類**：Excalidraw（存成 `.excalidraw`，不影響 `.md`）
- **看板**：Kanban（獨立 `.md` 檔，不在衛教文章內）

### ⚠️ 需注意使用場合的外掛
| 外掛 | 風險 | 安全使用方式 |
|------|------|------------|
| **Dataview** | 在 `.md` 正文插入 ` ```dataview ``` ` 區塊，會原封不動出現在網站文章中 | **只在索引筆記、草稿筆記使用，衛教文章正文禁止使用** |
| **Templater** | 若模板語法 `<% ... %>` 未執行完就存檔，會帶進網站 | 確認模板語法已被替換成實際內容再存檔 |
| **Spaced Repetition** | 在文章末尾插入 `<!--SR:...-->` 復習標記 | 衛教文章不做閃卡；只在個人學習筆記使用 |
| **Folder Notes** | 在每個資料夾建立同名 `.md` 索引檔 | 安全，sync-obsidian.js 的分類判斷不受影響 |

### 🚫 AI 操作禁止事項
1. **禁止**直接修改 `src/content/posts/` 內的 `.md` 檔案（這些是自動生成的，手改會被下次 sync 覆蓋）
2. **禁止**修改 Obsidian 文章的 frontmatter `category` 欄位（分類由資料夾決定，sync 會覆蓋）
3. **禁止**在衛教文章正文插入 Dataview、Templater 等外掛語法
4. **修改 `sync-obsidian.js` 前**，必須先確認改動不影響 frontmatter 欄位的繼承邏輯（特別是 `coverImage` 和 `order`）
