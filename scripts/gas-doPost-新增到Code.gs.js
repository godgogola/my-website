// ============================================
// Code.gs - 豐田診所衛教專欄 (雙層快取極速版 v2)
// UI/UX Pro Max — 後端優化 + 安全同步機制
// ============================================

const SHEET_ID = '1zqiRJw2hp0vGqthOo4p9F1aUFk24dDBDgKHWV3bDR2U';
const CACHE_KEY = 'fengtien_clinic_data_v2';
const CACHE_TTL = 600; // 快取存活時間：600秒 (10分鐘)

function doGet(e) {
  var output = (e && e.parameter && e.parameter.output) || '';
  
  if (output === 'json') {
    var data = getCategoriesData();
    return ContentService.createTextOutput(JSON.stringify(data))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
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
// 【新增】doPost — 接收新網站同步請求 (安全版)
// 規則：1. 絕對不改寫已有內容的欄位 2. 只填空白 3. 不自動新增新列
// ============================================

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    if (data.action !== 'updateArticleUrl') {
      return jsonResponse({ success: false, error: '不支援的 action' });
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

    // 只在找到對應列時處理（找不到直接忽略，不自動 appendRow）
    if (rowIndex > 0) {
      var existingImgUrl     = String(subSheet.getRange(rowIndex, 5).getValue()).trim();
      var existingArticleUrl = String(subSheet.getRange(rowIndex, 6).getValue()).trim();

      var updated = false;

      // 🔒 只有欄位「完全空白」時才寫入新網址，絕對不覆蓋原本已有資料
      if (!existingImgUrl && data.imgUrl) {
        subSheet.getRange(rowIndex, 5).setValue(data.imgUrl);
        updated = true;
      }
      if (!existingArticleUrl && data.articleUrl) {
        subSheet.getRange(rowIndex, 6).setValue(data.articleUrl);
        updated = true;
      }

      if (updated) {
        CacheService.getScriptCache().remove(CACHE_KEY);
        return jsonResponse({ success: true, action: '僅填補空白欄位', title: data.title });
      } else {
        return jsonResponse({ success: true, action: '已有資料略過', title: data.title });
      }
    } else {
      // 找不到標題，直接略過，不新增列
      return jsonResponse({ success: true, action: '未匹配略過', title: data.title });
    }

  } catch (err) {
    return jsonResponse({ success: false, error: err.toString() });
  }
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
