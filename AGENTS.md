# 專案規範與 AI 記憶設定 (AGENTS.md)

## 🎨 文章封面圖生成規範 (Cover Image Prompt Rule)

當使用者要求「生成文章封面圖」或「批次生成文章封面圖」時，**依文章類型（讀書筆記 vs. 醫療衛教筆記）嚴格套用以下專屬最高標準規格**，徹底達到原生 16:9 的豐富橫向構圖與生動微縮立體世界觀：

---

### 📚 體系 A：【讀書筆記】巨型羊毛書本立體微縮舞台 (Giant Open Wool Book Diorama)

所有讀書筆記（如《漫步華爾街》、《貨幣失能》、《21世紀的21堂課》等所有書籍章節）**100% 統一套用此「攤開的巨型粗羊毛書本舞台」架構**：

* **視覺風格**：可愛手作 3D 針織毛線娃娃微縮景觀 (Handcrafted amigurumi crochet miniature book-world diorama)。
* **核心基底（必備世界觀）**：
  * **以「攤開的巨型粗羊毛編織書本（空白米白羊毛書頁）」作為整體立體舞台** (`On top of a giant open knitted book with blank cream wool pages`)。
  * 背景為溫馨柔和的圖書館書房、層疊的毛線書堆、溫暖閱讀燈散景 (`cozy blurred library study with soft stacked wool books and warm reading lamp bokeh`)。
* **角色與情境動態**：
  * 角色為可愛的小小探索者人偶（男生/女生隨機可愛人偶）或智慧動物夥伴（貓頭鷹、小狐狸、小貓咪、小松鼠等）。
  * **角色必須有互動動作或沉浸於事件中**（如手持放大鏡探索、攜手合作、在三叉路口思考、在壁爐旁交談、在天秤兩端衡量），**絕非呆立或證件照擺拍**。
  * **嚴格禁忌**：**讀書筆記絕對不出現醫師、白袍、聽診器！**
* **攝影與光影**：微距攝影、移軸微縮景觀（Tilt-shift miniature effect）、柔和淺景深、溫暖柔和的晨光/黃金光斑（Floating warm light motes）、原生 16:9 橫向構圖、四周保留呼吸留白。
* **嚴格禁止文字與字母 (ABSOLUTELY NO TEXT / LETTERS)**：純視覺敘事，畫面上與任何道具絕不出現文字、數字、圖表或標籤。

#### 📝 讀書筆記標準通用 Prompt 範本 (Book Master Template)
```text
Generate a blog post cover image with an aspect ratio of 16:9 (landscape). Subject: On top of a giant open knitted book with blank cream wool pages, a charming and intricate miniature diorama exploring [章節核心主題與故事隱喻]. In the center, [可愛小小毛線人偶/動物夥伴正在進行的生動互動與探索動作], closely surrounded by a rich cluster of miniature wool architectural structures, stylized props, and landscape elements: [具體高低錯落的微型造景道具，如微型石板路、小建築、奇幻機關、天秤、燈火等]. Art Style: Rendered in a realistic, cute, handcrafted amigurumi knitted style (crochet wool texture) miniature book-world diorama. Texture: High-quality soft yarn texture, visible knit stitches, fuzzy wool and felt details. Characters: Cute, miniature chibi-style knitted explorer dolls or wise animal dolls, button-like eyes, warm and curious expressions (NO doctors, NO white coats, NO stethoscopes). Colors: Rich, warm, and inviting harmonious palette (cream wool, warm amber, glowing golds, soft pastels, cozy earth tones). Composition: Central focus on the giant open knitted book stage with generous breathing margins on all 4 sides (top, bottom, left, right). 100% completely intact diorama. Background: Cozy blurred library study with soft stacked wool books and warm reading lamp bokeh. Technical: High quality, 3D render, macro photography, tilt-shift miniature effect, photorealistic warm lighting, soft depth of field, wide shot. Constraints: ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO WATERMARKS, NO LABELS, NO TYPOGRAPHY, NO CHARTS, NO INFOGRAPHICS, NO UI ELEMENTS, NO MEDICAL ATTIRE. Full bleed framing.
```

---

### 🏥 體系 B：【醫療衛教筆記】微型醫學探索舞台 (Medical Mini-World Diorama)

未來新生成的醫學衛教文章封面圖，全面升級為**「具備生動情境、互動故事感與豐富立體空間」的高階微縮景觀**：

* **核心基底**：
  * 跳脫過去呆板的單一桌面，轉向**「立體多層次微縮醫學探索景觀」**（如立體人體微縮公園、巨型醫學知識百科舞台、溫馨治癒系微型診間/實驗室工坊）。
* **角色與器官互動**：
  * 男醫師/女醫師毛線玩偶不再只是站樁拍照，而是與**可愛的微型器官玩偶（胃部、心臟、肝臟、血管水管、胰島素小精靈）進行生動的醫療互動**（例如：醫師手拿柔軟毛線聽診器為微笑胃玩偶看診、合力修復微型血管水管、拿著放大鏡研究發光的細胞晶體、在天秤前平衡地雷食物與健康食材）。
* **視覺與光影**：維持親切療癒的毛線質感（Amigurumi crochet）、溫暖柔和的工作室燈光、微距移軸景深、原生 16:9 留白防貼邊。
* **嚴格禁止文字與字母**：所有藥罐、醫療器材、飲食道具維持純編織紋理，嚴禁出現任何英文字母或標籤。

#### 📝 醫療筆記標準通用 Prompt 範本 (Medical Master Template)
```text
Generate a blog post cover image with an aspect ratio of 16:9 (landscape). Subject: On top of a warm wooden workbench or an open giant medical journal, a whimsical, heartwarming miniature diorama exploring [醫學病理/治療主題]. In the center, a cute chibi doctor amigurumi plush doll (sitting or actively interacting) is tenderly examining or working alongside a cute, anthropomorphic smiling [主題器官/細胞/微生物毛線玩偶], surrounded by a rich, creative horizontal cluster of handcrafted felt props: [具體醫療比喻道具，如毛線聽診器、微型針筒、水管管線、健康食物、藥箱模型等，生動高低錯落陳列]. Art Style: Realistic, cute, handcrafted amigurumi knitted style (crochet wool texture) miniature diorama. Texture: High-quality soft yarn texture, visible stitches, warm felt accents. Colors: Comforting, bright, warm clinical palette (mint green, gentle pastel blues, soft coral, warm amber). Composition: Dynamic tabletop diorama wide horizontal 16:9 scene, centered comfortably with generous breathing margins on all 4 sides (top, bottom, left, right). Background: Cozy softly blurred clinic studio with warm glowing fairy lights or stacked medical books bokeh. Technical: High quality 3D render, macro photography, tilt-shift miniature effect, soft depth of field. Constraints: ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO LABELS, NO CHARTS, NO WATERMARKS. Full bleed framing.
```

---

### 生成與發布 SOP (自動化處理)
1. **生圖 (符合體系 A/B 規格)**：依主題生成符合上述「巨型立體舞台、生動動作情境、四周充足留白」的原生 16:9 圖片。
2. **原圖備份**：將 16:9 PNG 備份至 `G:\我的雲端硬碟\衛教文章圖片\<Title>.png`。
3. **WebP 轉檔發布**：將 16:9 圖片轉檔為高品質 WebP，**同時存入 `public/images/<Title>.webp` 與 `public/og-images/<Title>.webp`**（確保 Google Sheet 次分類工作表之圖片與網站自動無縫更新為最新版）。
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

## 🚀 全自動發布交班 SOP (Master Release Pipeline)

> **Antigravity 2.0 最高發布守則**：
> 1. **平時編輯輕量模式（極重要，避免等待）**：平常進行局部修改（例如生圖、修改文章、增加一兩個影片 ID、調整文案等），**只在本地端完成檔案修改與儲存，嚴禁自動執行耗時的發布管線（禁止自動跑 `sync-sheet.js`、`sync-books.js`、`build` 與 `vercel --prod`）**，確保能光速回應進行下一個任務！
> 2. **觸發完整發布時機**：只有當使用者**明確給出指示**（例如「發布網站」、「同步更新」、「全部做完了發布上線」或定時交班任務觸發）時，才嚴格依照以下 7 個步驟一次性完成發布。

### 📋 標準發布 7 步驟 (SOP Execution Order)

1. **[1/7] 同步 Obsidian 文章與讀書筆記**：
   - 執行 `node scripts/sync-obsidian.js`（同步衛教專欄筆記）
   - 執行 `node scripts/sync-books-content.js`（同步人類大歷史等讀書筆記內文）
2. **[2/7] 套用自訂封面對應**：
   - 執行 `node scripts/apply-mapping.js`（套用已登記的手動封面對應表）
3. **[3/7] 自動比對剩餘封面**：
   - 執行 `node scripts/auto-cover-image-v2.js`（自動比對圖庫與未配對的文章）
4. **[4/7] 雲端硬碟圖片同步（最終權威）**：
   - 執行 `node scripts/sync-drive-images.js`（確保 `G:\我的雲端硬碟\衛教文章圖片\` 之最新圖片全數同步至 `public/images/` 與 `public/og-images/`）
5. **[5/7] Astro 建置檢查與自癒**：
   - 執行 `npm run build` 進行全站編譯驗證。
   - **自癒協議**：若建置報錯（如 YAML frontmatter 缺少引號、冒號衝突或破圖），AI 必須讀取報錯日誌，主動定位並修復該 `.md` 檔案，修復後重新執行 `npm run build` 直到完全成功（Exit Code 0）。
6. **[6/7] Google Sheet 次分類工作表同步**：
   - 執行 `node scripts/sync-sheet.js`（更新最新文章 URL 與圖片 URL 至次分類工作表，自動排除指數投資）
   - 執行 `node scripts/sync-books.js`（更新書籍工作表資料）
7. **[7/7] Git 提交與 Vercel 生產部署**：
   - 執行 `git add -A`
   - 檢查是否有更動，若有變更則執行 `git commit -m "auto: release sync YYYY-MM-DD HH:mm"`
   - 執行 `git push origin main`
   - 執行 `npx vercel --prod --yes` 確保線上網站即時發布

### 🛡️ 缺封面圖之應變機制 (Missing Cover Image Handling)
在執行發布過程中，若偵測到有新文章缺少 `coverImage` 或本機無圖檔：
1. **絕不破圖上線**。
2. 依據上方【地雷食物系列 16:9 黃金規範】，分析文章醫療核心，調用生圖工具生成原生 16:9 毛線娃娃圖。
3. 原圖存入 `G:\我的雲端硬碟\衛教文章圖片\<Title>.png`，轉 WebP 存入 `public/images/` 與 `public/og-images/`，並回填 frontmatter 後再繼續執行發布管線。

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

---

## 💼 非醫學個人專欄分流規範 (Personal vs. Clinic Separation)

- **情境說明**：院長在 Obsidian 會撰寫非醫學個人專欄（例如資料夾命名為「指數投資」或「投資理財」）。
- **個人網站展示**：在個人網站 (`/health-column`) 正常展示，並自動排在分類標籤列最末端。
- **診所官網與 Google Sheet 隔離**：
  1. `src/pages/health-column/embed.astro` 與 `src/pages/column/embed.astro` 已設置 `CLINIC_EXCLUDED_CATEGORIES = ['指數投資', '投資理財']`，確保豐田診所官網嵌入專區絕不出現任何投資理財文章。
  2. `scripts/sync-sheet.js` 已設置 `EXCLUDED_CATEGORIES`，確保投資理財文章不會同步至診所 Google Sheet。
  3. `src/pages/index.astro` 首頁「最新醫學筆記」區塊已設置排除過濾，確保首頁維持純粹醫學專業。

---

## 🎬 衛教與知識短影音前置檢查鐵律 (Video Footage Safety Rule)

> **Antigravity 影片後製第一鐵律（嚴禁雙層字幕重疊）**：
> 1. **前置檢查素材純淨度**：在啟動任何短影音後製壓制管線前，AI **必須首先檢驗素材來源是否為「100% 無字幕純淨原始片段（Clean Footage）」**。
> 2. **嚴格禁止硬蓋字幕**：絕對禁止拿已經燒錄過舊字幕的成品 MP4 疊加新字幕。
> 3. **缺失立即回報協議**：若在 `Downloads/`、本機或專案目錄中找不到乾淨無字幕的原始分段（例如找不到 `1.mp4`, `2.mp4` 或未加字幕母帶），**必須第一時間停下來主動向院長報告詢問，絕不可自行拿含舊字幕之影片硬蓋壓制**！

---

## 🎙️ 短影音男女配音分流鐵律 (Voice Identity Rule)

> **Antigravity 影片後製聲音規範（男女分流鐵律）**：
> 1. **醫學筆記 / 衛教專欄短影音**：配音**一律使用微軟台灣女聲 (`zh-TW-HsiaoChenNeural`)**。
>    - 形象設定：專業、親切、溫暖的女醫師衛教旁白。
>    - 製作鐵律：嚴禁保留生片工具自帶之劣質語音或同音錯字原聲，必須一律使用 `zh-TW-HsiaoChenNeural` 重新合成純淨醫學配音，並嚴密校對醫學專有名詞（如「糖化血色素」、「瘦瘦針」等）。
> 2. **讀書筆記短影音 (如《漫步華爾街》等財經與閱讀系列)**：配音**一律使用微軟台灣男聲 (`zh-TW-YunJheNeural`)**。
>    - 形象設定：知性、大氣、沉穩的說書人旁白，嚴格維持 1.0x 原速與每鏡頭結尾約 1.0 秒呼吸留白。

---

## 🎬 醫學筆記短影音後製標準（Lip-Sync 音畫同步、抑揚頓挫與字音一字不差鐵律）

> **Antigravity 醫學影片第一準則（絕不露出無聲動嘴穿幫、絕不平淡死板拖音）**：
> 1. **字音 100% 同步**：口播台詞與畫面上出現的字幕必須出自單一文本來源（`tts_to_sub`，僅隱藏 `——` 與 `「」`），一字不差！
> 2. **抑揚頓挫韻律工程 (Prosody Engineering)**：
>    - 核心專有名詞加 `「」` 引號（如 `「多巴胺」`、`「動力引擎」`），微軟神經女聲會**自動加重音階、音調微幅上揚**，營造層次豐富的醫學權威感。
>    - 句中轉折加逗號 `，` 或破折號 `——` 創造自然頓挫，句末肯定句加入 `！` 讓收音俐落乾脆。
>    - 合成參數帶入 `pitch="+2Hz", rate="+1%"`，提升親切、溫暖、有朝氣的女醫師診間質感。
> 3. **敏捷自然語速（嚴禁 atempo < 0.95 拖音死板）**：
>    - 嚴格鎖定語速在 **`0.95x ~ 1.06x`（推薦 1.00x 原速）**。
>    - **嚴禁使用 `atempo < 0.95`（如 0.85x）強行拖慢**！降速會磨平共振峰，產生有氣無力、拖沓死板的機器朗讀感。
> 4. **真人自然呼吸換氣留白 (Cadence Gap)**：
>    - 句與句之間精準留出 **`0.22s ~ 0.28s`（標準推薦 `0.24s`）**換氣空隙，重現「說完重點 ➔ 微頓換氣 ➔ 引出下句」的真實說話節奏。
> 5. **台詞飽滿度鐵律（Lip-Sync 全程覆蓋鐵律）**：
>    - 原生動嘴模型（Talking Head）嘴喙／口形開闔往往延伸至 **8.5 ~ 9.5 秒**。
>    - 每個 10 秒分鏡由 3 句台詞構成，第 3 句收尾時間必須精準銜接動物閉嘴瞬間（允許微幅 0.95x ~ 1.05x 貼合），絕不露出動物「無聲動嘴」穿幫！
> 6. **版面安全區**：左上角 3D 浮雕雙行字卡緊湊收斂在安全區 `(52, 42, 350, 46)`，防擋嘴喙、耳朵與角色道具；小烏龜徽章置於 `(85, 165)`。
> 7. **成片輸出與禁角括號鐵律**：1080p Lanczos 壓制，檔案直出 YouTube 爆款長標題，並同步產生時間軸章節 `新增說明.txt` 與預覽截圖。**YouTube 標題與 `新增說明.txt` 嚴格禁止出現任何角括號 `<`、`>`（及 `＜`、`＞`、`〈`、`〉`）**——醫學數值（如 `<30`、`>80`）一律改寫為中文 `低於 30`、`超過 80`、`小於`、`以上／以下`，並在腳本寫檔前強制 `assert` 攔截，避免 YouTube Studio 報錯「不得使用角括號」！

---

## 🎬 讀書筆記 3D 羊毛針氈定格短影音 SOP (Book Video Pipeline)

當使用者指示「製作讀書筆記短影音」、「漫步華爾街影片後製」或處理書籍分鏡時，嚴格遵循 `BOOK_VIDEO_SOP.md` 規範：
1. **視覺風格**：純視覺羊毛針氈定格偶動畫（Needle-Felted Wool Stop-Motion）＋ 巨型粗羊毛書本舞台，隨機可愛人偶＋動物夥伴，純視覺無文字圖表，**人偶專注動作不張嘴說話（Narrator 旁白說書風格）**。
2. **分鏡架構與 1.0x 沉穩說書鐵律**：
   - 標準 4 分鏡（40 秒，每鏡 10.027s）。
   - **台詞控制每鏡 32~38 字（方案 B 飽滿版）**。
   - **100% 維持 1.0x 原速（不加速、不趕話）**，發聲約 **8.8~9.0 秒**，結尾精準保留 **約 1.0 秒（0.9~1.1s）純定格呼吸留白**，避免冷場拖沓。
3. **自動後製**：微軟神經語音 `zh-TW-YunJheNeural` 1.0x ＋ Faster-Whisper 毫秒字幕對齊（零重疊） ＋ 3D 浮雕字卡與小烏龜 Logo ＋ 1080p Lanczos 壓制。
4. **輸出命名**：MP4 成品直接命名為 YouTube 爆款全名（如 `蒙眼猴子射飛鏢贏過九成經理人？磐石理論 vs 空中樓閣！｜《漫步華爾街》Ep.01.mp4`），上傳 YouTube Studio 一秒自動帶入標題，並自動產出包含章節時間軸與 `#Shorts` 之 `新增說明.txt`。
5. **網站雙向串聯**：
   - 登記至 `src/data/videos.ts`（分類為書名，如 `'漫步華爾街'`）。
   - 在讀書筆記 Markdown（Obsidian 與 `src/content/books/`）frontmatter 加入 `videoId: "YouTube_ID"`，由網站自動在文章標題下方渲染 16:9 播放器。
