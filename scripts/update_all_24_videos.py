import os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

# 1. Video metadata dictionary
new_videos = [
    # --- 漫步華爾街 Ep 03 ---
    {
        "id": "9njkkBBiDkg",
        "title": "破爛唱片行改名「電子」暴漲七倍？漂亮五十與投機泡沫血淚史！｜《漫步華爾街》Ep.03",
        "description": "別以為只有散戶會盲目！六零年代只要名字加上「電子」，連連年虧損的破公司股價都能翻七倍！企業更玩起造詞遊戲，將造船廠包裝成「海洋系統」大搞虛假併購；隨後機構法人狂炒「漂亮五十」藍籌股與日本資產泡沫，最終在金融萬有引力下慘烈崩盤！",
        "category": "漫步華爾街",
        "duration": "0:40",
        "featured": True,
        "thumbnail": "/images/03、投機泡沫史.webp",
        "articleSlug": "/books/漫步華爾街/03-投機泡沫史",
        "articleTitle": "03、投機泡沫史",
    },
    # --- 醫學短影音 (最新批次) ---
    {
        "id": "zhBtKjibzkM",
        "title": "台灣十大癌症近半數在腸胃肝膽！大腸癌蟬聯男性榜首14年，早期篩檢存活率破9成全攻略｜黃冠智醫師",
        "description": "最新癌登報告出爐！全台十大癌症中，消化道癌症佔據半壁江山，男性大腸癌更高居榜首長達 14 年！但你知道早期大腸癌篩檢發現治療，五年存活率超過 9 成嗎？掌握糞便潛血與高品質無痛大腸鏡，及早攔截息肉病變！",
        "category": "消化道癌症專區",
        "duration": "1:00",
        "featured": True,
        "thumbnail": "/images/112年臺灣癌症登記報告.webp",
        "articleSlug": "112年臺灣癌症登記報告",
        "articleTitle": "112年臺灣癌症登記報告",
    },
    {
        "id": "VGBp9EIMLLE",
        "title": "血糖穩就不會洗腎？忽略「尿白蛋白 uACR」腎臟照樣受損！2026 ADA 護腎組合拳全解析｜黃冠智醫師",
        "description": "糖尿病患者血糖控制良好，為什麼腎臟還是悄悄受損？2026 ADA 最新指引強調：單看抽血腎功能（eGFR）不夠，必須定期驗「尿白蛋白肌酸酐比值（uACR）」！早期發現微量白蛋白尿，及早啟用 SGLT2i 與非類固醇 MRA 護腎組合拳，逆轉洗腎危機！",
        "category": "糖尿病",
        "duration": "1:00",
        "featured": True,
        "thumbnail": "/images/糖尿病腎病變-uacr-處置.webp",
        "articleSlug": "糖尿病腎病變-uacr-處置",
        "articleTitle": "糖尿病腎病變-uacr-處置",
    },
    {
        "id": "3Q9je5AmbEc",
        "title": "吃白稀飯比吃白飯更飆血糖？一次搞懂「升糖指數 GI vs 升糖負荷 GL」與不發胖進食順序｜黃冠智醫師",
        "description": "為什麼清淡的白稀飯比乾飯更容易引發血糖海嘯？關鍵在於烹煮澱粉完全糊化！一次搞懂升糖指數（GI）與升糖負荷（GL）的差異，並學會「肉、菜、飯」科學進食順序，讓胰島素不再疲於奔命，告別飯後昏睡與脂肪囤積！",
        "category": "健康飲食",
        "duration": "1:00",
        "featured": True,
        "thumbnail": "/images/GI 值大解密.webp",
        "articleSlug": "gi-值大解密",
        "articleTitle": "GI 值大解密",
    },
    {
        "id": "upRugOtf4rI",
        "title": "胃悶脹痛、胃食道逆流可以吃什麼？腸胃科醫師點名「天然黏膜保護層」溫和護胃食物清單｜黃冠智醫師",
        "description": "胃痛胃脹、火燒心反覆發作，到底該吃什麼才能修復胃黏膜？腸胃科醫師親自整理溫和護胃食材清單：山藥、秋葵富含黏蛋白，高麗菜含天然抗潰瘍維生素U，木瓜與燕麥溫和好消化。遠離刺激酸辣與地雷甜食，吃出健康保護屏障！",
        "category": "胃部疾病",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/護胃食物.webp",
        "articleSlug": "護胃食物",
        "articleTitle": "護胃食物",
    },
    {
        "id": "ETbc0F7G35U",
        "title": "腹部超音波照出「膽囊息肉」會變癌症嗎？8成是良性膽固醇沉積！記住「1公分」關鍵警戒線｜黃冠智醫師",
        "description": "健檢超音波報告寫著「膽囊息肉」，會不會惡化成膽囊癌？別慌！臨床上超過八成都是良性的「膽固醇息肉」，不需開刀。關鍵在於記住「1公分（10mm）」警戒線與生長速度，定期超音波追蹤，安心掌握膽囊健康！",
        "category": "肝膽胰疾病",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/膽囊息肉.webp",
        "articleSlug": "膽囊息肉",
        "articleTitle": "膽囊息肉",
    },
    {
        "id": "vJDWppSFYyI",
        "title": "睡再飽還是莫名疲倦、肚子悶鼓？小心肝臟正在變粗硬！抓緊「早期肝纖維化」逆轉黃金期｜黃冠智醫師",
        "description": "肝臟沒有痛覺神經，當你感到莫名慢性疲勞、右上腹悶脹時，肝臟可能已經在默默纖維化變粗糙！從脂肪肝到肝硬化只要四部曲，幸運的是「早期肝纖維化（F1-F2）」完全可逆！及早進行超音波與 FIB-4 評估，守護肝臟健康！",
        "category": "肝膽胰疾病",
        "duration": "1:00",
        "featured": True,
        "thumbnail": "/images/腹部超音波肝纖維化.webp",
        "articleSlug": "腹部超音波肝纖維化",
        "articleTitle": "腹部超音波肝纖維化",
    },
    {
        "id": "GEarPGa3Wso",
        "title": "每天蛋白質到底吃夠沒？不用帶磅秤！醫師教你「1顆蛋＝1杯豆漿＝三指肉」7克代換秒懂法｜黃冠智醫師",
        "description": "減重想留住肌肉、維持免疫力與飽足感，但每天蛋白質到底吃夠了嗎？教你最實用的「7克蛋白質代換法」：1顆雞蛋＝1盒嫩豆腐＝1杯無糖豆漿＝女性三指大小肉片！免磅秤輕鬆湊齊每日所需，吃出易瘦緊實好體質！",
        "category": "健康飲食",
        "duration": "1:00",
        "featured": True,
        "thumbnail": "/images/一份蛋白質要怎麼吃.webp",
        "articleSlug": "一份蛋白質要怎麼吃",
        "articleTitle": "一份蛋白質要怎麼吃",
    },
    {
        "id": "_MFumV4dbgs",
        "title": "健檢「糞便潛血陽性」就等於得大腸癌？8萬人大數據揭曉真實罹癌率：做對1件事直接拆彈｜黃冠智醫師",
        "description": "收到健檢通知「糞便潛血陽性」先別自己嚇自己！臨床大數據顯示，潛血陽性患者中真正是大腸癌的僅約 3-5%，絕大多數是息肉、痔瘡或黏膜發炎。關鍵是「儘速安排無痛大腸鏡」，在息肉轉變成惡性前直接切除，一勞永逸拆除不定時炸彈！",
        "category": "內視鏡檢查",
        "duration": "1:00",
        "featured": True,
        "thumbnail": "/images/糞便潛血陽性就一定是大腸癌嗎.webp",
        "articleSlug": "糞便潛血陽性就一定是大腸癌嗎",
        "articleTitle": "糞便潛血陽性就一定是大腸癌嗎",
    },
    {
        "id": "HKeYzNAzvLE",
        "title": "每次跑步都喘到快斷氣卻瘦不下來？醫師解析「Zone 1～Zone 5 五大心率區間」：練對2區最燃脂護心｜黃冠智醫師",
        "description": "跑步總是氣喘吁吁、練得痛苦萬分卻體重不降？因為你跑錯心率區間了！了解 Zone 1 到 Zone 5 的運動生理學意義，特別是能大量燃燒脂肪、鍛鍊粒線體的「Zone 2 有氧基礎區」！用能輕鬆說話的節奏運動，護心抗老又燃脂！",
        "category": "要活就要動",
        "duration": "1:00",
        "featured": True,
        "thumbnail": "/images/跑步五大心率區間.webp",
        "articleSlug": "跑步五大心率區間",
        "articleTitle": "跑步五大心率區間",
    },
    {
        "id": "PZHOyX4llGI",
        "title": "吃飽總像懷孕脹氣、火燒心又絞痛？腸胃科醫師揭密「無糖代糖、牛奶洋蔥」4大隱形傷胃地雷｜黃冠智醫師",
        "description": "明明吃得很清淡，肚子卻脹成皮球、狂打嗝放屁又胃酸逆流？小心踩中高 FODMAP 食物陷阱！無糖口香糖的糖醇代糖、乳糖不耐的牛奶、以及洋蔥大蒜等產氣食材，在腸道發酵產生大量氣體。揪出脹氣隱形兇手，恢復平坦舒適好腸胃！",
        "category": "胃部疾病",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/護胃食物.webp",
        "articleSlug": "護胃食物",
        "articleTitle": "護胃食物",
    },
    {
        "id": "Q-meLPVXDv4",
        "title": "降血壓藥別再一顆一顆慢慢加！最新指引：單錠複方與心腎共病量身選藥全攻略｜黃冠智醫師",
        "description": "高血壓降壓藥別再一顆一顆慢慢試、慢慢加！最新指引強調「早期單錠複方 (SPC)」與「依共病量身訂做」。無共病首選 A+C 或 A+D；心衰竭與心梗必備乙型阻斷劑；腎病蛋白尿首選 ACEI/ARB；高齡長輩採溫和調控，全方位保護心腦腎！",
        "category": "高血壓",
        "duration": "1:01",
        "featured": True,
        "thumbnail": "/images/高血壓藥物在一般族群及共病族群的選擇.webp",
        "articleSlug": "高血壓藥物在一般族群及共病族群的選擇",
        "articleTitle": "高血壓藥物在一般族群及共病族群的選擇",
    },
    {
        "id": "GqRSeWBpCR8",
        "title": "喉嚨卡卡想咳咳不出、吃東西卻沒事？揭密「咽喉異物感」5大真兇與必做檢查警訊｜黃冠智醫師",
        "description": "喉嚨總是有異物感卡卡的、想咳咳不出來，吞口水特別明顯，但吃大餐喝水卻完全沒事？門診極為常見的「咽喉異物感（Globus Pharyngeus）」！成因涵蓋咽喉逆流 (LPR)、鼻涕倒流、自律神經與壓力、異位性胃黏膜及甲狀腺壓迫，找出病因對症下藥！",
        "category": "胃部疾病",
        "duration": "1:01",
        "featured": True,
        "thumbnail": "/images/咽喉異物感.webp",
        "articleSlug": "咽喉異物感",
        "articleTitle": "咽喉異物感",
    },
    {
        "id": "zp7aeqpjGyw",
        "title": "吃飽狂打嗝火燒心、胃藥總吃不好？小心是胃滑進胸腔！「食道裂孔疝氣」成因與自救法｜黃冠智醫師",
        "description": "吃飽經常火燒心、胃藥總吃不好？小心是胃部悄悄滑進胸腔了！橫膈膜裂孔韌帶因老化鬆弛，加上長期腹壓推擠，使得胃頂端滑入胸口。無痛胃鏡精準診斷，搭配制酸與促動力藥物封閉逆流；生活中減輕腹重、吃飽別躺下，守護橫膈膜！",
        "category": "胃部疾病",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/食道裂孔疝氣的原因.webp",
        "articleSlug": "食道裂孔疝氣的原因",
        "articleTitle": "食道裂孔疝氣的原因",
    },
    {
        "id": "Dr2M5Yvwlbs",
        "title": "健檢空腹血糖及格，糖化血色素卻亮紅字？揪出飯後飆糖與「泡芙人」3大隱形元兇｜黃冠智醫師",
        "description": "體檢空腹血糖 95 及格，糖化血色素卻亮紅字？因為空腹只是單張快照，糖化血色素才是三個月錄影帶！亞洲人泡芙人體質肌肉少，精緻澱粉吃進來消化不掉；加上熬夜高壓皮質醇偷放糖。掌握 211 餐盤順序與飯後散步 15 分鐘，完全可逆！",
        "category": "糖尿病",
        "duration": "1:01",
        "featured": True,
        "thumbnail": "/images/空腹血糖正常但是糖化血色素高是什麼原因_video_thumb.webp",
        "articleSlug": "糖化血色素空腹血糖正常但是糖化血色素高是什麼原因",
        "articleTitle": "【糖化血色素】空腹血糖正常但是糖化血色素高是什麼原因",
    },
    {
        "id": "tXlbdUwahMQ",
        "title": "胃藥吃好幾個月火燒心還沒好？PPI 胃藥一定要「飯前30分鐘空腹吃」的關鍵真相｜黃冠智醫師",
        "description": "胃藥吃了好幾個月，胸口還是反覆火燒心、泛酸水好不了？門診中最常見的原因往往不是藥效不夠強，而是第一步「服藥時間」就吃錯了！氫離子幫浦阻斷劑（PPI）必須在餐前 30 到 60 分鐘空腹吃，才能精準封閉胃壁產酸通道！",
        "category": "胃部疾病",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/ppi為什麼要空腹吃.webp",
        "articleSlug": "ppi為什麼要空腹吃",
        "articleTitle": "ppi為什麼要空腹吃",
    },
    # --- 你的人生，他們六個說了算！全系列 ---
    {
        "id": "-19NNKlOX8o",
        "title": "打造身心強大生化花園！掌握睡眠、前驅營養、運動與迷走神經四大物理基底｜黃冠智醫師",
        "description": "大腦是一座精密生化花園，若缺乏四大物理基底，再高明的心智調節都將淪為無米之炊！深層睡眠修復腦脊液、優質蛋白質補足神經原料、Zone 2 有氧刺激 BDNF 生長，結合腹式呼吸激活用迷走神經，築起抵禦憂鬱與焦慮的堅實壁壘！",
        "category": "你的人生，他們六個說了算!",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/08、大腦的天使特調四大生活基底.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/08-大腦的天使特調四大生活基底",
        "articleTitle": "08、大腦的天使特調四大生活基底",
    },
    {
        "id": "Y3G6w7l9Nwg",
        "title": "別把睪固酮當猛男專利！男女皆需的「勝利荷爾蒙」：累積小勝挺胸兩分鐘啟動贏家模式｜黃冠智醫師",
        "description": "睪固酮絕非男性的專屬激素，女性同樣維持著關鍵基線！它是兩性體內最重要的「增幅與勝利荷爾蒙」，強化自信、決斷力與抗壓專注。史丹佛研究揭示：挺起胸膛展現開放姿態兩分鐘，就能拉升睪固酮並壓制皮質醇，啟動大腦的贏家模式！",
        "category": "你的人生，他們六個說了算!",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/07、睪固酮_自信心與行為傾向的增幅器.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/07-睪固酮_自信心與行為傾向的增幅器",
        "articleTitle": "07、睪固酮_自信心與行為傾向的增幅器",
    },
    {
        "id": "ibMKsMPdBDg",
        "title": "長期慢性壓力燒毀大腦？皮質醇應變生存指南：劃定壓力地圖與生理性嘆息秒速重啟｜黃冠智醫師",
        "description": "皮質醇不是純毒素，而是人體應對危機不可或缺的「首席動員官」，能迅速釋放血糖、提升警覺與專注力！但長期慢性暴雨會燒毀海馬迴、引發焦慮萎縮。學會劃定控制圈壓力地圖，運用「兩次深吸、一次長吐」的生理性嘆息秒速關閉警報！",
        "category": "你的人生，他們六個說了算!",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/06、皮質醇_應變挑戰與警覺的雙面刃.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/06-皮質醇_應變挑戰與警覺的雙面刃",
        "articleTitle": "06、皮質醇_應變挑戰與警覺的雙面刃",
    },
    {
        "id": "IgjzEfNrgFk",
        "title": "滑社群越看越自卑？九成血清素竟由腸道製造！告別虛擬地位焦慮的日照快走自癒法｜黃冠智醫師",
        "description": "為什麼滑社群媒體看到別人的光鮮亮麗，心裡卻越來越焦慮自卑？因為無止盡的虛擬向上比較會引發大腦地位焦慮，讓穩定情緒的基石「血清素」極速驟降！高達九成血清素由腸道製造，走出戶外曬太陽、快走散步並照顧腸道微生態，重拾平靜幸福感！",
        "category": "你的人生，他們六個說了算!",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/05、血清素_滿足感與穩定情緒的基石.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/05-血清素_滿足感與穩定情緒的基石",
        "articleTitle": "05、血清素_滿足感與穩定情緒的基石",
    },
    {
        "id": "582aiZM_MeA",
        "title": "秒降焦慮的神奇荷爾蒙！20秒擁抱釋放「催產素」：平息杏仁核警報的深層安全感防線｜黃冠智醫師",
        "description": "提到催產素，多數人只聯想到分娩或熱戀，其實它是大腦在現代焦慮生活中最強大的修復配方！當焦慮來襲時，催產素能直接平息杏仁核警報、切換副交感神經。每天 20 秒真誠擁抱、撫摸寵物、或向他人表達感謝，築起深層安全感防線！",
        "category": "你的人生，他們六個說了算!",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/04、催產素_信任與歸屬感的愛的荷爾蒙.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/04-催產素_信任與歸屬感的愛的荷爾蒙",
        "articleTitle": "04、催產素_信任與歸屬感的愛的荷爾蒙",
    },
    {
        "id": "YnIuwXuu-MY",
        "title": "痛苦之後才是至福！人體自建天然止痛劑「腦內啡」：安全爆發協議遠離成癮陷阱｜黃冠智醫師",
        "description": "為什麼跑步汗流浹背、或大笑一場之後，全身會湧現一段難以言喻的輕鬆與幸福感？這正是人體自建的天然嗎啡——「腦內啡」在發揮神奇的止痛與愉悅效應！解析成癮心理機制，掌握深蹲、冷水浴與開懷大笑等安全爆發協議，健康享受登頂快感！",
        "category": "你的人生，他們六個說了算!",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/03、腦內啡_天然止痛劑與極致愉悅感.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/03-腦內啡_天然止痛劑與極致愉悅感",
        "articleTitle": "03、腦內啡_天然止痛劑與極致愉悅感",
    },
    {
        "id": "fGJFtUTxvC4",
        "title": "越滑手機越空虛？多巴胺不是快樂分子！揭密渴望引擎與戒斷宿醉的「緩效多巴胺」法則｜黃冠智醫師",
        "description": "為什麼短影音越刷越空虛、手搖甜點吃完更焦慮？因為多巴胺不是快樂分子，而是喊著「我還要更多」的渴望引擎！速效多巴胺會帶來耐受性與多巴胺宿醉；學會戒斷循環，重拾閱讀、運動與微習慣等「緩效多巴胺」，建立源源不絕的專注行動力！",
        "category": "你的人生，他們六個說了算!",
        "duration": "0:41",
        "featured": True,
        "thumbnail": "/images/02、多巴胺_動機與渴望的動力引擎.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/02-多巴胺_動機與渴望的動力引擎",
        "articleTitle": "02、多巴胺_動機與渴望的動力引擎",
    },
    {
        "id": "sGHNkCItIL8",
        "title": "疲憊焦慮提不起勁？大腦的天使特調：六大神經傳導物質解密，找回身心掌控力！｜黃冠智醫師",
        "description": "明明沒做什麼體力活，卻總是感到疲憊、焦慮、提不起勁？每天的情緒與行動力不是單靠意志力，而是由大腦頂級調酒櫃裡的多巴胺、催產素、血清素、皮質醇、腦內啡與睪固酮決定！解開六大天使特調生化密碼，調配出屬於自己的活力特調！",
        "category": "你的人生，他們六個說了算!",
        "duration": "1:01",
        "featured": True,
        "thumbnail": "/images/01、六大神經傳導物質簡介.webp",
        "articleSlug": "/books/你的人生-他們六個說了算/01-六大神經傳導物質簡介",
        "articleTitle": "01、六大神經傳導物質簡介",
    },
]

print(f"Total new/updated video definitions: {len(new_videos)}")

# 2. Update src/data/videos.ts
with open('src/data/videos.ts', 'r', encoding='utf-8') as f:
    orig = f.read()

# Collect old IDs that are being replaced to remove duplicates
old_ids_to_replace = {
    'G0PAfeJwS4w', 'IwFh90jcMvg', 'TJ5mJQRNY3Y', 'HF5rHh3Df4I', 
    'Mq6Ndlq3G7E', 'qy6YD2DZots', 'jyOxM3nfrso', 'IpNvepoi-E4',
    'jh99G9JS4-U', 'dJoBaaJizFs', 'XDXe2YEdm4U'
}
for v in new_videos:
    old_ids_to_replace.add(v['id'])

# Read existing videos list by parsing or string manipulation
# Let's format the new video objects as TypeScript code
ts_entries = []
for i, v in enumerate(new_videos, 1):
    entry = f"""  {{
    id: '{v["id"]}',
    title: '{v["title"]}',
    description: '{v["description"]}',
    category: '{v["category"]}',
    duration: '{v["duration"]}',
    url: 'https://www.youtube.com/watch?v={v["id"]}',
    featured: {str(v["featured"]).lower()},
    order: {i},
    thumbnail: '{v["thumbnail"]}',
    articleSlug: '{v["articleSlug"]}',
    articleTitle: '{v["articleTitle"]}',
  }},"""
    ts_entries.append(entry)

new_entries_block = "\n".join(ts_entries)

# In videos.ts, replace or insert at start of `export const videos: VideoItem[] = [`
prefix = "export const videos: VideoItem[] = ["
if prefix in orig:
    # First, let's remove any existing objects that have IDs in old_ids_to_replace
    # Let's split by `{` and `},` carefully or use regex
    # A cleaner approach: filter out blocks containing `id: '<old_id>'`
    parts = orig.split(prefix)
    header = parts[0] + prefix + "\n"
    rest = parts[1]
    
    # We will filter out video objects from `rest`
    # Let's match all `{ ... }` blocks
    pattern = re.compile(r'(\s*\{[^{}]*?id:\s*\'([^\']+)\'[^{}]*?\},?)', re.DOTALL)
    
    removed_count = [0]
    def replacer(match):
        vid_id = match.group(2)
        if vid_id in old_ids_to_replace:
            removed_count[0] += 1
            return ""
        return match.group(1)
        
    cleaned_rest = pattern.sub(replacer, rest)
    print(f"Removed {removed_count[0]} old/duplicated entries from videos.ts")
    
    updated_videos_ts = header + new_entries_block + "\n" + cleaned_rest.lstrip()
    with open('src/data/videos.ts', 'w', encoding='utf-8') as f:
        f.write(updated_videos_ts)
    print("Successfully updated src/data/videos.ts with all 24 videos!")
else:
    print("Error: prefix not found in videos.ts")

# 3. Update Markdown frontmatter `videoId` for reading notes
book_mapping = [
    # 漫步華爾街
    ("src/content/books/漫步華爾街/03-投機泡沫史.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\03、投機泡沫史.md", "9njkkBBiDkg"),
    # 你的人生，他們六個說了算!
    ("src/content/books/你的人生，他們六個說了算!/01-六大神經傳導物質簡介.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\01、六大神經傳導物質簡介.md", "sGHNkCItIL8"),
    ("src/content/books/你的人生，他們六個說了算!/02-多巴胺_動機與渴望的動力引擎.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\02、多巴胺_動機與渴望的動力引擎.md", "fGJFtUTxvC4"),
    ("src/content/books/你的人生，他們六個說了算!/03-腦內啡_天然止痛劑與極致愉悅感.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\03、腦內啡_天然止痛劑與極致愉悅感.md", "YnIuwXuu-MY"),
    ("src/content/books/你的人生，他們六個說了算!/04-催產素_信任與歸屬感的愛的荷爾蒙.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\04、催產素_信任與歸屬感的愛的荷爾蒙.md", "582aiZM_MeA"),
    ("src/content/books/你的人生，他們六個說了算!/05-血清素_滿足感與穩定情緒的基石.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\05、血清素_滿足感與穩定情緒的基石.md", "IgjzEfNrgFk"),
    ("src/content/books/你的人生，他們六個說了算!/06-皮質醇_應變挑戰與警覺的雙面刃.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\06、皮質醇_應變挑戰與警覺的雙面刃.md", "ibMKsMPdBDg"),
    ("src/content/books/你的人生，他們六個說了算!/07-睪固酮_自信心與行為傾向的增幅器.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\07、睪固酮_自信心與行為傾向的增幅器.md", "Y3G6w7l9Nwg"),
    ("src/content/books/你的人生，他們六個說了算!/08-大腦的天使特調四大生活基底.md", r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了算!\08、大腦的天使特調四大生活基底.md", "-19NNKlOX8o"),
]

def update_frontmatter_videoid(filepath, video_id):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        fm = parts[1]
        body = parts[2]
        if 'videoId:' in fm:
            fm = re.sub(r'videoId:\s*["\']?[^"\s\n]+["\']?', f'videoId: "{video_id}"', fm)
        else:
            fm = fm.rstrip() + f'\nvideoId: "{video_id}"\n'
        new_content = f"---{fm}---{body}"
    else:
        new_content = f'---\nvideoId: "{video_id}"\n---\n{content}'
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated videoId in {os.path.basename(filepath)} -> {video_id}")

for local_path, obsidian_path, vid in book_mapping:
    update_frontmatter_videoid(local_path, vid)
    if os.path.exists(obsidian_path):
        update_frontmatter_videoid(obsidian_path, vid)

print("All frontmatter videoId updates completed!")
