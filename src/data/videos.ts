/**
 * 衛教短影音資料集
 * 集中管理 YouTube 頻道 @godgogola 最新衛教影片
 */

export interface VideoItem {
  id: string;             // YouTube Video ID
  title: string;          // 影片標題
  description: string;    // 影片重點衛教簡述
  category: '肝膽胰疾病' | '胃部疾病' | '腸道健康' | '檢查衛教' | '代謝慢病'; // 分類標籤
  duration: string;       // 影片長度
  url: string;            // YouTube 觀看連結
  featured: boolean;      // 是否列為首頁精選（展示於首頁影音專區）
  order: number;          // 排序序號
}

export const videoCategories = [
  '全部',
  '肝膽胰疾病',
  '胃部疾病',
  '腸道健康',
  '檢查衛教',
  '代謝慢病',
] as const;

export const videos: VideoItem[] = [
  {
    id: 'iFDd1LTER_I',
    title: '急性胰臟炎',
    description: '上腹劇痛穿透後背小心自體消化！認識急性胰臟炎三大導火線、疼痛特徵警訊與臨床緊急處置原則。',
    category: '肝膽胰疾病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=iFDd1LTER_I',
    featured: true,
    order: 1,
  },
  {
    id: '4j84jWlgqlY',
    title: '巴瑞式食道炎',
    description: '火燒心久治不癒小心食道癌前病變！認識巴瑞特氏食道炎成因、腸化生細胞特徵與定期內視鏡追蹤防癌關鍵。',
    category: '胃部疾病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=4j84jWlgqlY',
    featured: true,
    order: 2,
  },
  {
    id: 'Z63MSpIm87o',
    title: '結腸激躁症',
    description: '一緊張壓力大就肚子痛、腹瀉或便秘？搞懂大腸激躁症（IBS）成因、常見分型與低 FODMAP 飲食日常調理。',
    category: '腸道健康',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=Z63MSpIm87o',
    featured: true,
    order: 3,
  },
  {
    id: 'GmdlJWoGZEA',
    title: '藥物性食道潰瘍',
    description: '吞藥沒喝夠水小心食道黏膜被灼傷！一顆藥丸引發胸口劇痛與吞嚥困難，認識藥物性食道潰瘍預防與照護重點。',
    category: '胃部疾病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=GmdlJWoGZEA',
    featured: true,
    order: 4,
  },
  {
    id: '1zkY0lUePRo',
    title: '膽結石',
    description: '右上腹悶痛、飯後脹氣小心膽結石！認識膽結石成因、高危險群、症狀警訊與微創手術治療時機。',
    category: '肝膽胰疾病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=1zkY0lUePRo',
    featured: false,
    order: 5,
  },
  {
    id: 'rW2WJlv-6u8',
    title: '打瘦瘦針也要健康',
    description: '打瘦瘦針快速減重也要守護肌肉與代謝！腸胃專科醫師解析 GLP-1 瘦瘦筆正確用藥原則、常見副作用照護與預防復胖關鍵。',
    category: '代謝慢病',
    duration: '1:11',
    url: 'https://www.youtube.com/watch?v=rW2WJlv-6u8',
    featured: false,
    order: 6,
  },
  {
    id: '41WgFILCHtM',
    title: '代謝症候群',
    description: '一分鐘快速掌握代謝症候群 5 大關鍵指標，提早防範心血管與三高慢性病風險。',
    category: '代謝慢病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=41WgFILCHtM',
    featured: false,
    order: 7,
  },
  {
    id: 'kbVjl-HOKr4',
    title: '大腸息肉',
    description: '息肉是大腸癌前身！認識常見大腸息肉種類、癌變機率與無痛內視鏡切除預防關鍵。',
    category: '腸道健康',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=kbVjl-HOKr4',
    featured: false,
    order: 8,
  },
  {
    id: 'lywTekvOC1k',
    title: '胃食道逆流',
    description: '火燒心、喉嚨異物感？帶您了解胃食道逆流成因、生活飲食調整與最新整合用藥觀念。',
    category: '胃部疾病',
    duration: '0:51',
    url: 'https://www.youtube.com/watch?v=lywTekvOC1k',
    featured: false,
    order: 9,
  },
  {
    id: 'w3L4lQW7HKU',
    title: '血糖平穩的好習慣',
    description: '遠離血糖雲霄飛車！腸胃專科醫師分享控糖好習慣、日常進食順序與穩糖關鍵心法。',
    category: '代謝慢病',
    duration: '1:11',
    url: 'https://www.youtube.com/watch?v=w3L4lQW7HKU',
    featured: false,
    order: 10,
  },
  {
    id: '-Nfxr0NGDQ0',
    title: '無痛腸胃鏡',
    description: '無痛舒眠內視鏡到底會不會痛？一次了解專業麻醉照護流程、安全性與檢查優勢。',
    category: '檢查衛教',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=-Nfxr0NGDQ0',
    featured: false,
    order: 11,
  },
  {
    id: 'omtvd71Inwc',
    title: '上消化道潰瘍',
    description: '胃潰瘍與十二指腸潰瘍有何不同？搞懂疼痛發作時間點、致病因素與黃金治療期。',
    category: '胃部疾病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=omtvd71Inwc',
    featured: false,
    order: 12,
  },
  {
    id: 'cBAGeNQeMP8',
    title: '一次做完腸胃篩檢',
    description: '為什麼醫師常建議胃鏡、大腸鏡同時做？一次舒眠準備、省時安心、全消化道完整把關。',
    category: '檢查衛教',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=cBAGeNQeMP8',
    featured: false,
    order: 13,
  },
  {
    id: 'S2QcETFlIxI',
    title: '低渣飲食',
    description: '大腸鏡檢查前最關鍵的清腸環節！低渣飲食原則、地雷食物與常見誤區全攻略。',
    category: '檢查衛教',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=S2QcETFlIxI',
    featured: false,
    order: 14,
  },
  {
    id: 'lxOZ1KRJDDE',
    title: '胃幽門桿菌',
    description: '胃癌與消化道潰瘍的頭號隱形殺手！什麼是幽門螺旋桿菌？為什麼感染務必殺菌？',
    category: '胃部疾病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=lxOZ1KRJDDE',
    featured: false,
    order: 15,
  },
  {
    id: 'wCFG_s-ToXA',
    title: '幽門桿菌檢驗方法',
    description: '碳13吹氣試驗、糞便抗原快篩、胃鏡切片怎麼選？各項檢查原理與適合對象評估。',
    category: '檢查衛教',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=wCFG_s-ToXA',
    featured: false,
    order: 16,
  },
  {
    id: '7yhAnDnFC60',
    title: '急性腸胃炎',
    description: '上吐下瀉虛脫無力？急性腸胃炎黃金照護守則、補充電解質要點與危險就醫警訊。',
    category: '胃部疾病',
    duration: '0:41',
    url: 'https://www.youtube.com/watch?v=7yhAnDnFC60',
    featured: false,
    order: 17,
  },
];

/**
 * 取得 YouTube 高畫質縮圖網址
 */
export function getYouTubeThumbnail(videoId: string): string {
  return `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;
}

/**
 * 取得 YouTube 嵌入連結（支援自動播放參數）
 */
export function getYouTubeEmbedUrl(videoId: string, autoplay = true): string {
  return `https://www.youtube.com/embed/${videoId}?rel=0&showinfo=0&autoplay=${autoplay ? 1 : 0}`;
}
