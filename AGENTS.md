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
3. **WebP 轉檔發布**：將 16:9 圖片轉檔為高品質 WebP 存入 `public/images/<Title>.webp`。
4. **綁定與驗證**：更新 Markdown 的 `coverImage` 欄位並執行 `npm run build` 驗證。
