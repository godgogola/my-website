import fetch from 'node-fetch'; // or global fetch in Node 18+

async function check() {
  const GAS_URL = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';
  const res = await fetch(GAS_URL + '?output=json&_t=' + Date.now(), { redirect: 'follow' });
  const data = await res.json();
  
  const emptyImg = [];
  const emptyUrl = [];
  const emptyBoth = [];
  
  let total = 0;
  for (const cat of data) {
    for (const item of cat.items) {
      total++;
      const hasImg = !!(item.img && String(item.img).trim());
      const hasUrl = !!(item.url && String(item.url).trim());
      if (!hasImg && !hasUrl) {
        emptyBoth.push({ cat: cat.title, ...item });
      } else if (!hasImg) {
        emptyImg.push({ cat: cat.title, ...item });
      } else if (!hasUrl) {
        emptyUrl.push({ cat: cat.title, ...item });
      }
    }
  }
  
  console.log('Total items in GAS:', total);
  console.log('\n--- 1. 圖片與連結皆無 (' + emptyBoth.length + ' 篇) ---');
  emptyBoth.forEach(i => console.log(`[${i.cat}] (排序:${i.sort}) ${i.title}`));
  
  console.log('\n--- 2. 只有沒有圖片 (有連結) (' + emptyImg.length + ' 篇) ---');
  emptyImg.forEach(i => console.log(`[${i.cat}] (排序:${i.sort}) ${i.title} | 網址: ${i.url}`));
  
  console.log('\n--- 3. 只有沒有連結 (有圖片) (' + emptyUrl.length + ' 篇) ---');
  emptyUrl.forEach(i => console.log(`[${i.cat}] (排序:${i.sort}) ${i.title} | 圖片: ${i.img}`));
}

check().catch(console.error);
