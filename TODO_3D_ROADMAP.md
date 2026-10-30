# 3D 互動模型未來功能擴充規劃 (3D Feature Roadmap)

> **建立時間**：2026-10-28  
> **專案背景**：個人網站 3D 人體解剖系列（胃、大腸、肝膽胰、腹痛九宮格）與 3D 衛教群島（Island）之後續升級儲備清單。待日後需要時隨時啟動實作。

---

## 🎯 優先實作建議清單

### 1. 【解剖衛教】疾病進展滑桿 (Disease Progression Slider) 🥇
* **適用頁面**：`src/pages/anatomy/stomach.astro`、`liver.astro`
* **功能細節**：
  * **胃部黏膜時序演變**：正常黏膜 ➔ 慢性表淺性胃炎 ➔ 萎縮性胃炎 / 腸上皮化生 ➔ 早期胃癌。
  * **肝臟脂肪時序演變**：正常肝臟 ➔ 輕度脂肪肝 ➔ 脂肪性肝炎 (NASH) ➔ 肝硬化結節。
  * 拉動滑桿即時動態改變 3D 模型的材質表面、粗糙度、顏色與凹凸結節。

### 2. 【診間溝通】一鍵生成 3D 衛教圖卡 / 手機同步 QR Code 🥈
* **適用頁面**：所有 `src/pages/anatomy/*.astro`
* **功能細節**：
  * 醫師於診間旋轉至特定角度並標記病灶後，點擊「生成衛教卡」，系統將當前 3D Canvas 截圖結合診所衛教重點排版，病患可掃描 QR Code 帶回家於手機上旋轉查看。

### 3. 【沉浸體驗】虛擬內視鏡腔內飛行巡航 (Fly-through Mode) 🥉
* **適用頁面**：`src/pages/anatomy/stomach.astro`、`colon.astro`
* **功能細節**：
  * 沿著胃腔/腸腔中心曲線（Three.js `CatmullRomCurve3`）平滑前進的第一人稱內視鏡視野。
  * 模擬胃鏡著名的倒轉檢查（J-turn / Inversion），迴轉 180 度回看賁門。

### 4. 【深層病理解剖】器官壁斷面 4 層結構剖開 (Clipping Plane)
* **適用頁面**：`src/pages/anatomy/stomach.astro`、`colon.astro`
* **功能細節**：
  * 切開胃壁/腸壁展示 4 層結構（黏膜層 Mucosa ➔ 黏膜下層 Submucosa ➔ 固有肌層 Muscularis ➔ 漿膜層 Serosa）。
  * 標記息肉生長層位與內視鏡切除（EMR / ESD）深度。

### 5. 【病患自我評估】腹痛 3D 智慧導引 (Interactive Pain Locator)
* **適用頁面**：`src/pages/anatomy/abdominal-pain.astro`
* **功能細節**：
  * 病患直接在 3D 人體軀幹上點選痛點與痛感類型，動態透視高亮深層臟器並產出鑑別診斷引導。

### 6. 【3D 衛教群島】閱讀進度解鎖與健康錦囊 (Island Gamification)
* **適用頁面**：`src/pages/island.astro`
* **功能細節**：
  * 閱讀特定分類專欄文章累積進度，解鎖島上健康燈塔點亮或新小動物。
  * 每日健康盲盒：點擊寶箱抽取黃醫師今日護胃防癌叮嚀。
  * 手機陀螺儀視差（Parallax Effect）。
