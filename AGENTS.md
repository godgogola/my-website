# 專案規範與 AI 記憶設定 (AGENTS.md)

## 🎨 文章封面圖生成規範 (Cover Image Prompt Rule)

當使用者要求「生成文章封面圖」或「批次生成文章封面圖」時，**必須 100% 統一使用以下微型袖珍場景規格與裁切 SOP，杜絕任何切頭切腳問題**：

---

### 核心風格與微型袖珍構圖 (Miniature Tabletop Diorama)
* **視覺風格**：可愛手作 3D 針織毛線娃娃 (Cute 3D knitted crochet amigurumi plush doll)。
* **材質與質感**：細緻手作毛線紋理、羊毛質感、溫馨柔和的工作室燈光 (Hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft lighting)。
* **黃金防切構圖規格（以《慢性腎臟病》為最高標準）**：
  1. **袖珍人偶比例 (Miniature Chibi Scale 35%~40%)**：
     * 女醫師娃娃與主要器官角色**必須縮小為微型袖珍人偶**，整體人物高度**僅佔畫面中央 35%~40% 的垂直高度**。
  2. **上下 30% 巨大留白空間 (30% Top & Bottom Empty Felt Margin)**：
     * 畫面頂部必須保留 **30%~35% 的空白毛氈工作室背景牆**。
     * 畫面底部必須保留 **25%~30% 的毛氈地毯與木質桌面**。
     * 目的：進行 16:9 中心裁切時，女醫師的蓬鬆頭髮、頭頂、手部道具、雙腳靴子與地墊**完全落在安全區正中央，100% 絕不貼邊、絕不切除**。
  3. **橫向展開故事佈局 (Horizontal Storytelling)**：
     * 主體與道具橫向展開：左側與中央為多個器官或情境道具（如彩虹台階、沙漏、小推車、防禦牆等），右側為小巧站立的女醫師娃娃。
  4. **嚴格禁止文字與字母 (ABSOLUTELY NO TEXT / LETTERS)**：
     * 所有道具（如少鹽罐、藥瓶、餐盒）一律維持純毛線編織紋理，**絕對不能出現任何英文字母或標籤 (No text, no words, no letters on any props)**。
* **畫面比例**：最終輸出必須為橫向 16:9 比例 (1024x576)。

---

### 📝 標準通用 Prompt 範本 (Master Prompt Template)

未來生成任何封面圖時，直接套用此範本填入主題：

```text
Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS ON ANY PROPS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll with short skirt and white coat stands small on the right (occupying only 35% to 40% vertical height), with massive 30% empty background wall above her hair and wide cozy carpet floor below her boots. Spanning horizontally across the left and center is a rich horizontal scene of [主題道具與可愛器官玩偶描述]. 16:9 widescreen diorama composition, 100% complete body head-to-toe fully intact with generous breathing margins.
```

---

### 生成、裁切與轉檔 SOP (自動化處理)
1. **生圖 (袖珍微型 35% 高度 Prompt)**：依主題生成符合上述「上下 30% 留白、角色佔中央 35% 高度」的 1:1 方形圖片。
2. **16:9 中心裁切**：透過 Python Pillow 將生成的圖片進行**中心 16:9 比例裁切 (1024x576)**。
3. **原圖備份**：將裁切後的 16:9 PNG 備份至 `G:\我的雲端硬碟\衛教文章圖片\<Title>.png`。
4. **WebP 轉檔發布**：將裁切後的 16:9 圖片轉檔為高品質 WebP 存入 `public/images/<Title>.webp`。
5. **綁定與驗證**：更新 Markdown 的 `coverImage` 欄位並執行 `npm run build` 驗證。
