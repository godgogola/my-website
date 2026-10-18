// ============================================
// Code.gs - 豐田診所衛教專欄 & 讀書筆記 (雙庫架構極速版 v3)
// 徹底移除主分類依賴，全面支援【衛教文章】與【讀書筆記】雙分頁
// ============================================

const SHEET_ID = '1zqiRJw2hp0vGqthOo4p9F1aUFk24dDBDgKHWV3bDR2U';
const CACHE_KEY = 'fengtien_clinic_data_v3';
const CACHE_TTL = 600; // 快取存活時間：600秒 (10分鐘)

// 取得目標工作表（支援舊名相容自動 fallback）
function getTargetSheet(ss, sheetName) {
  if (sheetName === '讀書筆記' || sheetName === 'books') {
    return ss.getSheetByName('讀書筆記');
  }
  // 衛教文章：優先抓「衛教文章」，找不到則自動抓舊名「次分類」
  return ss.getSheetByName('衛教文章') || ss.getSheetByName('次分類');
}

function doGet(e) {
  var output = (e && e.parameter && e.parameter.output) || '';
  var sheetParam = (e && e.parameter && e.parameter.sheet) || '';
  
  if (output === 'json') {
    var data;
    if (sheetParam === 'books' || sheetParam === '讀書筆記') {
      data = getSheetDataGrouped('讀書筆記');
    } else if (sheetParam === 'all') {
      data = {
        articles: getSheetDataGrouped('衛教文章'),
        books: getSheetDataGrouped('讀書筆記')
      };
    } else {
      // 預設回傳衛教文章
      data = getSheetDataGrouped('衛教文章');
    }
    return ContentService.createTextOutput(JSON.stringify(data))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('衛教專欄 | 豐田診所')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// 依指定工作表讀取並依 A 欄自動分組，不再需要「主分類」工作表
function getSheetDataGrouped(targetName) {
  var cache = CacheService.getScriptCache();
  var cacheKey = CACHE_KEY + '_' + targetName;
  var cachedData = cache.get(cacheKey);
  
  if (cachedData) {
    try { return JSON.parse(cachedData); } catch(e) {}
  }

  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var targetSheet = getTargetSheet(ss, targetName);
    if (!targetSheet) return [];

    var rows = targetSheet.getDataRange().getValues().slice(1);
    var groupMap = {};
    var groupOrder = [];

    rows.forEach(function(r) {
      var groupName = String(r[0] || '').trim(); // A欄：主分類 或 書名
      var sortVal   = r[1] || 999;               // B欄：排序
      var title     = String(r[2] || '').trim(); // C欄：標題 或 章節
      var type      = r[3] || '圖片卡片';         // D欄：類型
      var img       = r[4] || '';                // E欄：圖片網址
      var url       = r[5] || '';                // F欄：文章網址
      var visible   = r[6] === true || String(r[6]).toUpperCase() === 'TRUE'; // G欄：是否公開

      if (visible && groupName && title) {
        if (!groupMap[groupName]) {
          groupMap[groupName] = [];
          groupOrder.push(groupName);
        }
        groupMap[groupName].push({
          sort: sortVal,
          title: title,
          type: type,
          img: img,
          url: url
        });
      }
    });

    var result = [];
    groupOrder.forEach(function(name, idx) {
      var items = (groupMap[name] || []).slice();
      items.sort(function(a, b) { return a.sort - b.sort; });
      result.push({
        sort: idx + 1,
        title: name,
        items: items
      });
    });

    try {
      cache.put(cacheKey, JSON.stringify(result), CACHE_TTL);
    } catch (cacheError) {
      Logger.log('快取寫入略過：' + cacheError.toString());
    }

    return result;

  } catch (error) {
    throw new Error("資料讀取失敗：" + error.toString());
  }
}

// ============================================
// doPost — 支援【衛教文章】與【讀書筆記】雙分頁操作：
//   updateArticleUrl：更新圖片/文章網址
//   appendRow：新增不存在的文章列或章節列
//   fixCategory：修正 A 欄分類或書名
//   fixSheetTitle：修正 C 欄標題（舊→新）
// ============================================

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.openById(SHEET_ID);
    
    // 依參數決定操作「衛教文章」或「讀書筆記」分頁（預設為衛教文章）
    var targetSheetName = data.sheet || data.targetSheet || '衛教文章';
    var sheet = getTargetSheet(ss, targetSheetName);

    if (!sheet) {
      return jsonResponse({ success: false, error: '找不到目標工作表：' + targetSheetName });
    }

    var sheetRows = sheet.getDataRange().getValues();

    // ── 1. fixCategory：修正 A 欄主分類或書名 ──
    if (data.action === 'fixCategory') {
      for (var j = 1; j < sheetRows.length; j++) {
        if (String(sheetRows[j][2]).trim() === String(data.title).trim()) {
          var cur = String(sheetRows[j][0]).trim();
          if (cur !== String(data.category).trim()) {
            sheet.getRange(j + 1, 1).setValue(data.category);
            clearAllCache();
            return jsonResponse({ success: true, action: '分類已修正', title: data.title, from: cur, to: data.category });
          }
          return jsonResponse({ success: true, action: '分類正確無需修正', title: data.title });
        }
      }
      return jsonResponse({ success: true, action: '未找到標題', title: data.title });
    }

    // ── 2. fixSheetTitle：修正 C 欄標題 ──
    if (data.action === 'fixSheetTitle') {
      for (var k = 1; k < sheetRows.length; k++) {
        if (String(sheetRows[k][2]).trim() === String(data.oldTitle).trim()) {
          if (String(data.newTitle).trim() === String(data.oldTitle).trim()) {
            return jsonResponse({ success: true, action: '標題相同無需修改', title: data.oldTitle });
          }
          sheet.getRange(k + 1, 3).setValue(data.newTitle);
          clearAllCache();
          return jsonResponse({ success: true, action: '標題已更新', oldTitle: data.oldTitle, newTitle: data.newTitle });
        }
      }
      return jsonResponse({ success: true, action: '找不到舊標題', oldTitle: data.oldTitle });
    }

    // ── 3. appendRow：新增不存在的文章列或讀書筆記列 ──
    if (data.action === 'appendRow') {
      for (var m = 1; m < sheetRows.length; m++) {
        if (String(sheetRows[m][2]).trim() === String(data.title).trim()) {
          return jsonResponse({ success: true, action: '已存在略過', title: data.title });
        }
      }

      // 自動從該分類/書名目前最大序號接續往下遞增（防止產生 999 暫存值）
      var assignedSort = Number(data.sort);
      if (!assignedSort || isNaN(assignedSort) || assignedSort >= 900) {
        var groupKey = String(data.category || data.bookTitle || '').trim();
        var maxS = 0;
        for (var r = 1; r < sheetRows.length; r++) {
          if (String(sheetRows[r][0]).trim() === groupKey) {
            var sVal = Number(sheetRows[r][1]);
            if (!isNaN(sVal) && sVal < 900 && sVal > maxS) {
              maxS = sVal;
            }
          }
        }
        assignedSort = maxS + 1;
      }

      sheet.appendRow([
        data.category || data.bookTitle || '', // A欄：分類或書名
        assignedSort,                          // B欄：排序（自動接續遞增）
        data.title || '',                      // C欄：標題或章節名
        data.type || '圖片卡片',                // D欄：類型
        data.imgUrl || '',                     // E欄：圖片網址
        data.articleUrl || '',                 // F欄：文章網址
        data.visible !== undefined ? (data.visible ? 'TRUE' : 'FALSE') : 'TRUE' // G欄：是否公開
      ]);
      clearAllCache();
      return jsonResponse({ success: true, action: '新增成功', title: data.title, sort: assignedSort, sheet: targetSheetName });
    }

    // ── 4. updateArticleUrl：更新圖片/文章網址 ──
    if (data.action === 'updateArticleUrl' || data.action === 'updateBookNote') {
      var rowIndex = -1;
      for (var i = 1; i < sheetRows.length; i++) {
        if (String(sheetRows[i][2]).trim() === String(data.title).trim()) {
          rowIndex = i + 1;
          break;
        }
      }

      if (rowIndex > 0) {
        var existUrl = String(sheet.getRange(rowIndex, 6).getValue()).trim();
        var updated = false;

        // 圖片網址：永遠覆蓋最新版
        if (data.imgUrl) {
          sheet.getRange(rowIndex, 5).setValue(data.imgUrl);
          updated = true;
        }
        // 文章網址：空白時寫入
        if (!existUrl && data.articleUrl) {
          sheet.getRange(rowIndex, 6).setValue(data.articleUrl);
          updated = true;
        }
        // 排序序號 (B欄)：若有傳入且非 999 則更新
        if (data.sort !== undefined && data.sort !== null && data.sort !== '' && Number(data.sort) !== 999) {
          sheet.getRange(rowIndex, 2).setValue(Number(data.sort));
          updated = true;
        }
        // 類型 (D欄)：若有傳入則更新為指定類型（如「圖片卡片」）
        if (data.type) {
          sheet.getRange(rowIndex, 4).setValue(data.type);
          updated = true;
        }

        if (updated) {
          clearAllCache();
          return jsonResponse({ success: true, action: '更新成功', title: data.title, sheet: targetSheetName });
        }
        return jsonResponse({ success: true, action: '已有資料略過', title: data.title });
      }
      return jsonResponse({ success: true, action: '未匹配略過', title: data.title });
    }

    // ── 5. updateSort：單獨更新指定標題的排序序號 ──
    if (data.action === 'updateSort') {
      var targetTitle = String(data.title || '').trim();
      var targetSort = Number(data.sort);
      if (isNaN(targetSort)) {
        return jsonResponse({ success: false, error: '無效的排序數值' });
      }
      for (var sIdx = 1; sIdx < sheetRows.length; sIdx++) {
        if (String(sheetRows[sIdx][2]).trim() === targetTitle) {
          sheet.getRange(sIdx + 1, 2).setValue(targetSort);
          clearAllCache();
          return jsonResponse({ success: true, action: '排序更新成功', title: targetTitle, sort: targetSort, sheet: targetSheetName });
        }
      }
      return jsonResponse({ success: false, error: '找不到該標題', title: targetTitle });
    }

    return jsonResponse({ success: false, error: '不支援的 action' });

  } catch (err) {
    return jsonResponse({ success: false, error: err.toString() });
  }
}

function clearAllCache() {
  var cache = CacheService.getScriptCache();
  cache.remove(CACHE_KEY + '_衛教文章');
  cache.remove(CACHE_KEY + '_讀書筆記');
  cache.remove(CACHE_KEY);
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
