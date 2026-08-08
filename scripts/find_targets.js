import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

const items = [
  { text: "【糖化血色素】空腹血糖高但是糖化血色素正常是什麼原因", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，手持放大鏡觀察著一個跳躍不安的高個子黃色糖顆粒娃娃（代表即時高血糖），旁邊擺放著一個沉睡且平靜的彩色毛線甜甜圈娃娃（代表正常的3個月平均糖化血色素）。" },
  { text: "【糖化血色素】空腹血糖正常但是糖化血色素高是什麼原因", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，指著一個頭戴紅皇冠、體型龐大的糖化血色素毛線娃娃，而前方的小黃色血糖顆粒娃娃正乖乖排隊坐著（代表空腹血糖正常）。" },
  { text: "【糖化血色素】糖化血色素升高的原因_非飲食因素", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，正從一個抱頭困惑的紅血球娃娃身邊，搬走代表非飲食干擾（如血球壽命改變）的紫色毛線小怪獸，周圍完全沒有甜食或食物毛線玩偶。" },
  { text: "【尿蛋白】輕微尿蛋白怎麼辦", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，拿著一隻溫柔的軟毛刷，幫一個有點緊張、正微微冒出少許白色毛線泡沫的腎臟娃娃進行清潔與護理。" },
  { text: "【尿潛血】輕微尿潛血怎麼辦", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，手持小巧的毛線手電筒，輕柔檢視一個帶著微小紅色毛線斑點的腎臟與膀胱娃娃，並給予撫慰。" },
  { text: "【貧血】小球性與大球性貧血", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃站立在中央，兩邊分別站著一個超小號的緊實紅色毛線球娃娃（小球）與一個巨大膨脹的淡紅色毛線球娃娃（大球），呈現鮮明對比。" },
  { text: "【胃癌】胃癌的危險因子", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，張開一個藍色毛線防護盾牌，保護著一個有點不適的粉紅胃娃娃，擋下外圍的幽門桿菌小怪獸、香煙毛線玩偶和醃漬罐毛線玩偶。" },
  { text: "【腎功能】高齡肌少症與腎功能誤判", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃拿著天平，一端是一個體型消瘦的長者手臂毛線娃娃（肌少症），另一端是一個表情困惑的腎臟娃娃，呈現肌肉量影響數據判讀的意象。" },
  { text: "【慢性腎臟病】慢性腎臟病各分期保腎措施", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，在五座由低到高的彩虹毛線台階上，為不同健康狀態的腎臟娃娃分別戴上保護頭盔、提供優質水滴和健康餐盒毛線玩偶。" },
  { text: "【膽紅素】單純膽紅素偏高", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，微笑撫摸著一個身上泛著溫和黃色光芒、但表情非常健康愉悅的肝臟娃娃，旁邊擺放著標示安全的綠色毛線氣球。" },
  { text: "長期血壓控制不良的併發症", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，張開雙臂保護著被緊繃紅色橡皮筋圈住的心臟、大腦與腎臟三個毛線器官娃娃。" },
  { text: "S-ABCDE 高血壓生活型態調整", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，帶領著心臟娃娃做運動，周圍圍繞著少鹽罐、球鞋、蔬菜籃和戒菸符號等五彩毛線配件。" },
  { text: "【ALT AST】肝功能上升", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，拿著冰敷袋，溫柔地貼在一個臉頰紅彤彤、泛著微熱發炎狀態的綠色肝臟娃娃頭上。" },
  { text: "【Albumin】白蛋白的合成與低下原因", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，看著一個健康的肝臟娃娃像工廠般編織出白色小毛線球（白蛋白），並幫另一個白蛋白不足、顯得有些虛弱的毛線血管娃娃編織補充織網。" },
  { text: "【Globulin】球蛋白", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，指揮著一群身穿防衛盔甲、造型可愛的藍色球蛋白毛線士兵娃娃，築起防禦屏障。" },
  { text: "【AG ratio】", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，正站在一座毛線翹翹板旁，調整左邊的白色白蛋白球與右邊的藍色球蛋白球，使其達到完美平衡。" },
  { text: "【Cystatin C】血清胱蛋白 C", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，拿著極精密的毛線透視鏡，精準捕捉從肌肉與腎臟經過的粉紫色 Cystatin C 毛線小精靈。" },
  { text: "【HDL】HDL太高是好事嗎", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，看著一個巨大的金黃色 HDL 英雄毛線娃娃，正好奇地用放大鏡確認它是否還在正常執行清掃血管垃圾的工作。" },
  { text: "【胃輕癱】胃輕癱飲食調整與治療", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，正輕輕推著一個圓滾滾、肚子塞滿食物毛線團而走不動的懶洋洋胃娃娃，並遞給它易消化的液體毛線瓶。" },
  { text: "【胃輕癱】胃輕癱臨床診斷標準", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃拿著沙漏，觀察一個胃娃娃消化食物毛線球的速度，沙漏裡的毛線顆粒滴落得非常緩慢。" },
  { text: "【胃輕癱】胃輕癱與消化不良有何不同", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃站立在中間，左邊是動力停滯、昏昏欲睡的胃輕癱娃娃，右邊是正冒著酸氣波浪、表情急躁的消化不良胃娃娃。" },
  { text: "碳水化合物造成脂肪堆積的機制", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，看著米飯/麵包造型的碳水毛線小精靈進入身體後，轉化為一顆顆黃色脂肪毛線球堆疊在腰際。" },
  { text: "【代謝異常脂肪肝】逆轉代謝異常脂肪肝", prompt: "身材纖瘦、鵝蛋臉且穿著短裙的漂亮女醫師娃娃，拉著一個原本裹滿黃色脂肪毛線團的肝臟娃娃一起在跑步機上運動，幫助它脫下脂肪外衣、變回健康的粉綠色。" }
];

const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
const mdData = mdFiles.map(f => {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  let title = f.replace('.md', '');
  let coverImage = '';
  if (fmMatch) {
    const titleMatch = fmMatch[1].match(/^title:\s*["']?(.+?)["']?\s*$/m);
    if (titleMatch) title = titleMatch[1];
    const coverMatch = fmMatch[1].match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);
    if (coverMatch) coverImage = coverMatch[1];
  }
  return { filename: f, title, coverImage, path: path.join(POSTS_DIR, f) };
});

function clean(str) {
  return str.replace(/[【】\[\]（）()\s\-_「」『』：:，,。.？?！!]/g, '').toLowerCase();
}

console.log('Total items:', items.length);
items.forEach((item, index) => {
  const cText = clean(item.text);
  let match = mdData.find(m => clean(m.title) === cText || clean(m.filename) === cText);
  if (!match) {
    match = mdData.find(m => clean(m.title).includes(cText) || cText.includes(clean(m.title)) || clean(m.filename).includes(cText) || cText.includes(clean(m.filename)));
  }
  if (!match) {
    // try key terms
    const keywords = item.text.replace(/[【】\[\]]/g, ' ').split(/\s+/).filter(Boolean);
    match = mdData.find(m => keywords.every(kw => clean(m.title).includes(clean(kw)) || clean(m.filename).includes(clean(kw))));
  }
  console.log(`[${index + 1}] ${item.text}`);
  if (match) {
    console.log(`   -> FOUND: File="${match.filename}", Title="${match.title}", Cover="${match.coverImage}"`);
  } else {
    console.log(`   -> NOT FOUND!`);
  }
});
