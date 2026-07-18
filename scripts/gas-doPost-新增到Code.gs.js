// ============================================
// Code.gs - 豐田診所衛教專欄 (雙層快取極速版 v2)
// UI/UX Pro Max — 後端優化
// ============================================

const SHEET_ID = '1zqiRJw2hp0vGqthOo4p9F1aUFk24dDBDgKHWV3bDR2U';
const CACHE_KEY = 'fengtien_clinic_data_v2';
const CACHE_TTL = 600; // 快取存活時間：600秒 (10分鐘)

function doGet(e) {
  // 支援 ?output=json 參數，回傳純 JSON（供跨域 fetch 使用）
  var output = (e && e.parameter && e.parameter.output) || '';
  
  if (output === 'json') {
    var data = getCategoriesData();
    return ContentService.createTextOutput(JSON.stringify(data))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  // 預設：回傳 HTML 頁面（直接開 URL 時使用）
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('衛教專欄 | 豐田診所')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getCategoriesData() {
  var cache = CacheService.getScriptCache();
  var cachedData = cache.get(CACHE_KEY);
  
  if (cachedData) {
    return JSON.parse(cachedData);
  }

  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
    
    var mainSheet = ss.getSheetByName('主分類');
    var mainData = mainSheet.getDataRange().getValues();
    var mainRows = mainData.slice(1);

    var subSheet = ss.getSheetByName('次分類');
    var subData = subSheet.getDataRange().getValues();
    var subRows = subData.slice(1);

    var subMap = {};
    subRows.forEach(function(sub) {
      var subMainName = sub[0]; 
      var subSort     = sub[1]; 
      var subTitle    = sub[2]; 
      var subType     = sub[3]; 
      var subImg      = sub[4]; 
      var subUrl      = sub[5]; 
      var subVisible  = sub[6] === true || String(sub[6]).toUpperCase() === 'TRUE'; 

      if (subVisible && subMainName) {
        if (!subMap[subMainName]) subMap[subMainName] = [];
        subMap[subMainName].push({
          sort: subSort || 999,
          title: subTitle,
          type: subType,
          img: subImg,
          url: subUrl
        });
      }
    });

    var categories = [];

    mainRows.forEach(function(row) {
      var sortOrder = row[0]; 
      var name      = row[1]; 
      var desc      = row[2]; 
      var icon      = row[3]; 
      var visible   = row[4] === true || String(row[4]).toUpperCase() === 'TRUE'; 

      if (!visible || !name) return;

      var items = (subMap[name] || []).slice();
      items.sort(function(a, b) { return a.sort - b.sort; });

      categories.push({
        sort: sortOrder || 999,
        title: name,
        subtitle: desc,
        icon: icon,
        items: items
      });
    });

    categories.sort(function(a, b) { return a.sort - b.sort; });

    try {
      cache.put(CACHE_KEY, JSON.stringify(categories), CACHE_TTL);
    } catch (cacheError) {
      Logger.log('快取寫入失敗（可能超過 100KB）：' + cacheError.toString());
    }

    return categories;

  } catch (error) {
    throw new Error("資料讀取失敗：" + error.toString());
  }
}

// ============================================
// 【新增】doPost — 接收新網站同步請求
// 自動將「文章網址」與「圖片網址」更新至次分類工作表
// ============================================

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    if (data.action !== 'updateArticleUrl') {
      return jsonResponse({ success: false, error: '不支援的 action: ' + data.action });
    }

    var ss       = SpreadsheetApp.openById(SHEET_ID);
    var subSheet = ss.getSheetByName('次分類');
    var subData  = subSheet.getDataRange().getValues();

    // 依「標題」尋找對應列（欄位 C = index 2）
    var rowIndex = -1;
    for (var i = 1; i < subData.length; i++) {
      if (String(subData[i][2]).trim() === String(data.title).trim()) {
        rowIndex = i + 1; // Google Sheet 1-indexed
        break;
      }
    }

    if (rowIndex > 0) {
      // ── 更新現有列的圖片網址（欄 E）和文章網址（欄 F）──
      if (data.imgUrl)     subSheet.getRange(rowIndex, 5).setValue(data.imgUrl);
      if (data.articleUrl) subSheet.getRange(rowIndex, 6).setValue(data.articleUrl);

      // 清除快取，讓診所網站下次立即讀到最新資料
      CacheService.getScriptCache().remove(CACHE_KEY);

      return jsonResponse({ success: true, action: '更新', title: data.title });

    } else {
      // ── 文章不在 Sheet 裡，自動新增一列 ──
      var category = data.category || '';

      // 計算同分類中最大排序號，新文章排在最後
      var maxSort = 0;
      for (var j = 1; j < subData.length; j++) {
        if (String(subData[j][0]).trim() === category) {
          var sortVal = Number(subData[j][1]);
          if (!isNaN(sortVal)) maxSort = Math.max(maxSort, sortVal);
        }
      }

      subSheet.appendRow([
        category,
        maxSort + 1,
        data.title,
        '圖片卡片',
        data.imgUrl || '',
        data.articleUrl || '',
        true
      ]);

      CacheService.getScriptCache().remove(CACHE_KEY);

      return jsonResponse({ success: true, action: '新增', title: data.title });
    }

  } catch (err) {
    return jsonResponse({ success: false, error: err.toString() });
  }
}

// 工具函數：統一回傳 JSON 格式
function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
