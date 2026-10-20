import os
import sys
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_NAME = "112年臺灣癌症登記報告"
BASE_DIR = os.path.abspath(r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工")
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
FFMPEG_BIN = os.path.join(BASE_DIR, "ffmpeg.exe") if os.path.exists(os.path.join(BASE_DIR, "ffmpeg.exe")) else "ffmpeg"
FONT_PATH = os.path.join(BASE_DIR, "jf-openhuninn-2.0.ttf")
LOGO_SRC = os.path.join(BASE_DIR, "turtle_logo.png")

os.makedirs(PROJECT_DIR, exist_ok=True)

def step1_generate_srt():
    print("【步驟 1】生成毫秒級繁體中文字幕 (output.srt)...")
    subtitles = [
        # 鏡頭 1: 國人十大癌症總覽 (Part 1, 0.000s ~ 10.005s)
        ("00:00:00,000", "00:00:03,750", "國人十大癌症由肺癌連三年居冠！"),
        ("00:00:03,800", "00:00:06,900", "大腸癌與乳癌緊追在後"),
        ("00:00:06,950", "00:00:09,200", "再來是肝癌！"),

        # 鏡頭 2: 男女頭號殺手差異 (Part 2, 10.005s ~ 20.032s)
        ("00:00:10,010", "00:00:11,950", "男女頭號殺手大不同！"),
        ("00:00:11,980", "00:00:15,350", "男性大腸癌蟬聯14年第一"),
        ("00:00:15,390", "00:00:18,500", "女性乳癌則連霸21年！"),

        # 鏡頭 3: 男性危險因子與性別落差 (Part 3, 20.032s ~ 30.037s)
        ("00:00:20,030", "00:00:22,010", "男性食道與口腔癌"),
        ("00:00:22,050", "00:00:23,910", "高出女性十倍以上！"),
        ("00:00:23,950", "00:00:26,350", "主因是菸酒檳榔"),
        ("00:00:26,400", "00:00:29,500", "女性則多為婦科與甲狀腺！"),

        # 鏡頭 4: 罹癌年齡高度集中 (Part 4, 30.037s ~ 40.042s)
        ("00:00:30,040", "00:00:33,420", "超過八成四患者集中在50歲以上！"),
        ("00:00:33,500", "00:00:36,500", "全癌症發生年齡中位數"),
        ("00:00:36,550", "00:00:38,800", "落在六十五歲！"),

        # 鏡頭 5: 年齡層增減消長 (Part 5, 40.042s ~ 50.047s)
        ("00:00:40,040", "00:00:43,180", "六十到六十九歲罹癌人數最多！"),
        ("00:00:43,200", "00:00:46,680", "六、七十歲族群增幅最明顯"),
        ("00:00:46,700", "00:00:49,400", "四十歲以下罹癌微幅遞減！"),

        # 鏡頭 6: 防癌行動與早期篩檢處方 (Part 6, 50.047s ~ 60.052s)
        ("00:00:50,050", "00:00:54,250", "四、五十歲後務必落實定期癌症篩檢！"),
        ("00:00:54,300", "00:00:56,300", "戒除菸酒檳榔"),
        ("00:00:56,350", "00:00:59,200", "早期發現就能及早治療！")
    ]

    srt_path = os.path.join(PROJECT_DIR, "output.srt")
    transcript_path = os.path.join(PROJECT_DIR, "transcript.txt")

    srt_lines = []
    txt_lines = []
    for idx, (s, e, text) in enumerate(subtitles, 1):
        srt_lines.append(f"{idx}\n{s} --> {e}\n{text}\n")
        txt_lines.append(f"[{s} -> {e}] {text}")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"字幕生成完畢: {srt_path} (共 {len(subtitles)} 條)")
    return srt_path

def step2_generate_title():
    print("【步驟 2】生成專屬 3D 立體字卡 (dynamic_title.png)...")
    output_png = os.path.join(PROJECT_DIR, "dynamic_title.png")

    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_size = 60
    font = ImageFont.truetype(FONT_PATH, font_size)

    stroke_width = 8
    fill_color = (255, 90, 180, 255)       # 亮桃紅主色
    stroke_color = (60, 20, 90, 255)       # 深紫外框
    x0, y0 = 140, 80
    line_spacing = 16

    lines = ["112年國人", "臺灣癌症登記報告"]
    cur_y = y0

    for line in lines:
        for ox, oy in [(4, 4), (5, 5), (6, 6)]:
            draw.text(
                (x0 + ox, cur_y + oy),
                line,
                font=font,
                fill=stroke_color,
                stroke_width=stroke_width,
                stroke_fill=stroke_color
            )
        draw.text(
            (x0, cur_y),
            line,
            font=font,
            fill=fill_color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color
        )
        bbox = draw.textbbox((x0, cur_y), line, font=font, stroke_width=stroke_width)
        cur_y += (bbox[3] - bbox[1]) + line_spacing

    img.save(output_png, "PNG")
    print(f"字卡生成完畢: {output_png} (標題佔用高度至 y={cur_y})")
    return output_png

def step3_render_final_video():
    print("【步驟 3】執行 6 分鏡無縫拼接與多軌合成渲染...")
    local_logo = os.path.join(PROJECT_DIR, "turtle_logo.png")
    if not os.path.exists(local_logo) and os.path.exists(LOGO_SRC):
        shutil.copy2(LOGO_SRC, local_logo)

    clips = [os.path.join(PROJECT_DIR, "input_clips", f"part{i}.mp4") for i in range(1, 7)]
    title_png = os.path.join(PROJECT_DIR, "dynamic_title.png")
    srt_file = os.path.join(PROJECT_DIR, "output.srt")
    final_output = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}.mp4")

    srt_escaped = srt_file.replace("\\", "/").replace(":", "\\:")
    fonts_dir = os.path.dirname(FONT_PATH).replace("\\", "/").replace(":", "\\:")

    filter_complex = (
        "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a][5:v][5:a]concat=n=6:v=1:a=1[v_raw][a_raw];"
        "[v_raw]scale=1920:1080:flags=lanczos[base];"
        "[base][6:v]overlay=0:0[v_title];"
        "[v_title][7:v]overlay=180:270[v_logo];"
        f"[v_logo]subtitles='{srt_escaped}':fontsdir='{fonts_dir}':force_style='"
        "Fontname=jf-openhuninn-2.0,FontSize=24,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,Outline=2.5,Alignment=2,MarginV=35'[v_out]"
    )

    cmd = [
        FFMPEG_BIN,
        "-i", clips[0],
        "-i", clips[1],
        "-i", clips[2],
        "-i", clips[3],
        "-i", clips[4],
        "-i", clips[5],
        "-i", title_png,
        "-i", local_logo,
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_raw]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        final_output, "-y"
    ]

    print("執行 FFmpeg 合成指令...")
    subprocess.run(cmd, check=True)
    print(f"成片渲染成功: {final_output}")
    return final_output

def step4_extract_previews():
    print("【步驟 4】截取 6 大分鏡預覽畫面驗證畫質與字卡/字幕效果...")
    final_output = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}.mp4")
    timestamps = [
        ("00:00:04.500", "preview_112_01_top_cancers.jpg"),
        ("00:00:15.000", "preview_112_02_gender_diff.jpg"),
        ("00:00:25.000", "preview_112_03_male_risk.jpg"),
        ("00:00:35.000", "preview_112_04_age_median.jpg"),
        ("00:00:45.000", "preview_112_05_peak_age.jpg"),
        ("00:00:55.000", "preview_112_06_prevention.jpg"),
    ]
    for ts, filename in timestamps:
        out_img = os.path.join(PROJECT_DIR, filename)
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", ts,
            "-i", final_output,
            "-vframes", "1",
            "-q:v", "2",
            out_img
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"截圖已生成: {out_img} (時間點: {ts})")

def step5_generate_description():
    print("【步驟 5】生成 YouTube 專屬發布說明文案 (新增說明.txt)...")
    desc_text = """衛生福利部最新公布「112年國人癌症登記報告」！在全癌發生人數中，肺癌已連續 3 年位居榜首，大腸癌與女性乳癌緊追在後。然而深入剖析數據，男女之間的罹癌版圖與危險因子呈現極為懸殊的性別不對稱！

掌握最新癌登 4 大關鍵警訊與實證防線：
1. 男女頭號殺手迥異：男性發生率第 1 名由大腸癌已蟬聯長達 14 年，女性則由乳癌連霸 21 年榜首。大腸癌每 2 年一次公費糞便潛血（FIT）篩檢能及早攔截半數以上早期病灶，存活率破九成！
2. 男性上消化呼吸道癌症差距驚人：男性食道癌與口腔癌標準化發生率分別高達女性的 12.8 倍與 10.2 倍！長期抽菸、飲酒與嚼食檳榔是黏膜反覆受創、細胞癌變的關鍵元兇。
3. 罹癌高度高齡化集中：國人高達 84% 癌症集中在 50 歲以上族群，發生年齡中位數落在 65 歲（較前一年延後 1 歲），其中 60～69 歲為確診人數最高峰（高達 3.9 萬人）。
4. 預防勝於治療的實證行動：善用政府公費 5 大癌症篩檢（大腸癌、子宮頸癌、乳癌、口腔癌、肺癌 LDCT），戒除菸酒檳榔，並配合定期無痛胃鏡、大腸鏡與腹部超音波追蹤，守護自身與家人健康！

📖 閱讀本集完整深入衛教專文：
https://drhuanggi.vercel.app/posts/112年臺灣癌症登記報告

⏱️ 影片時間軸重點：
00:00 最新癌登總覽：國人十大癌症由肺癌連三年居冠，大腸癌與乳癌緊追在後，再來是肝癌
00:10 男女殺手差異：男性大腸癌蟬聯榜首14年第一，女性乳癌連霸21年
00:20 男性風險警訊：男性食道與口腔癌高出女性十倍以上，主因是菸酒檳榔，女性則多為婦科與甲狀腺
00:30 年齡分佈解析：超過八成四患者集中在50歲以上，全癌症發生年齡中位數65歲
00:40 年齡層消長：60至69歲罹癌人數最多，60-79歲增幅最顯著，40歲以下微減
00:50 綜合防癌處方：四、五十歲後務必落實定期癌症篩檢，戒除菸酒檳榔，早期發現及早治療

👨‍⚕️ 關於黃冠智醫師：
現任豐田診所院長、肝膽腸胃科專科醫師。致力於將嚴謹醫學實證轉化為溫暖生動的衛教筆記。
🌐 個人官方網站：https://drhuanggi.vercel.app

#癌症登記報告 #112年癌症登記 #十大癌症 #大腸癌 #肺癌 #乳癌 #食道癌 #口腔癌 #癌症篩檢 #糞便潛血檢查 #黃冠智醫師 #豐田診所 #診間說書房
"""
    desc_path = os.path.join(PROJECT_DIR, "新增說明.txt")
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write(desc_text.strip() + "\n")
    print(f"說明文案已生成: {desc_path}")

if __name__ == "__main__":
    step1_generate_srt()
    step2_generate_title()
    step3_render_final_video()
    step4_extract_previews()
    step5_generate_description()
    print("\n" + "="*50)
    print("🎉【112年臺灣癌症登記報告】6 分鏡短影音後製與渲染全部完成！")
    print("="*50)
