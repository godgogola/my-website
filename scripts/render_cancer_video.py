import os
import sys
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_NAME = "十大癌症中屬於消化系癌症的個別分析"
BASE_DIR = os.path.abspath(r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工")
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
FFMPEG_BIN = os.path.join(BASE_DIR, "ffmpeg.exe") if os.path.exists(os.path.join(BASE_DIR, "ffmpeg.exe")) else "ffmpeg"
FONT_PATH = os.path.join(BASE_DIR, "jf-openhuninn-2.0.ttf")
LOGO_SRC = os.path.join(BASE_DIR, "turtle_logo.png")

def step1_generate_srt():
    print("【步驟 1】生成毫秒級繁體中文字幕 (output.srt)...")
    subtitles = [
        # 鏡頭 1: 癌登總覽與大腸癌榜首 (Part 1, 0s ~ 10.01s)
        ("00:00:00,000", "00:00:02,100", "國人最新癌登報告中"),
        ("00:00:02,200", "00:00:04,800", "消化系統占比極高"),
        ("00:00:04,900", "00:00:09,000", "大腸癌更蟬聯男性榜首14年！"),

        # 鏡頭 2: 糞便潛血篩檢與存活率 (Part 2, 10.01s ~ 20.02s)
        ("00:00:09,690", "00:00:12,650", "兩年一次糞便潛血篩檢"),
        ("00:00:12,700", "00:00:15,770", "能抓出過半早期大腸癌"),
        ("00:00:15,800", "00:00:18,600", "五年存活率高達九成以上！"),

        # 鏡頭 3: 肝癌發生率連續下降 (Part 3, 20.02s ~ 30.03s)
        ("00:00:19,700", "00:00:21,700", "排名第四的肝癌"),
        ("00:00:22,000", "00:00:26,000", "受惠於B肝篩檢與抗病毒藥物普及"),
        ("00:00:26,100", "00:00:28,500", "發生率已連降14年！"),

        # 鏡頭 4: 胃癌與幽門桿菌除菌 (Part 4, 30.03s ~ 40.04s)
        ("00:00:29,740", "00:00:31,700", "位居第九的胃癌"),
        ("00:00:31,740", "00:00:35,700", "隨幽門桿菌除菌與飲食改變"),
        ("00:00:35,800", "00:00:38,500", "發生率正穩定下降！"),

        # 鏡頭 5: 食道癌與菸酒檳榔警訊 (Part 5, 40.04s ~ 50.05s)
        ("00:00:39,940", "00:00:42,400", "食道癌居男性第六名"),
        ("00:00:42,550", "00:00:45,400", "發生率高達女性十二倍"),
        ("00:00:45,800", "00:00:48,100", "務必遠離菸酒與檳榔！"),

        # 鏡頭 6: 綜合篩檢與定期追蹤 (Part 6, 50.05s ~ 60.06s)
        ("00:00:50,240", "00:00:52,900", "善用公費篩檢與除菌治療"),
        ("00:00:52,980", "00:00:56,600", "定期接受內視鏡與超音波追蹤"),
        ("00:00:56,700", "00:00:59,400", "全面守住腸胃肝膽健康！")
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

    lines = ["十大癌症", "消化系癌症個別分析"]
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
        ("00:00:04.500", "preview_cancer_01_crc.jpg"),
        ("00:00:15.000", "preview_cancer_02_screening.jpg"),
        ("00:00:25.000", "preview_cancer_03_liver.jpg"),
        ("00:00:35.000", "preview_cancer_04_gastric.jpg"),
        ("00:00:45.000", "preview_cancer_05_esophagus.jpg"),
        ("00:00:55.000", "preview_cancer_06_prevention.jpg"),
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
    desc_text = """在衛福部最新公布的 112 年國人癌症登記報告中，屬於「腸胃消化系統（GI／肝膽胰）」範疇的癌症占比高得驚人！大腸癌、肝癌、胃癌、食道癌與胰臟癌，無一不是威脅國人健康的沈重隱形殺手。

然而，消化系癌症絕非不可預防，許多癌症正是「早期篩檢邊際效益最高」的典範：
1. 大腸癌（全癌第2名、男性第1名）：大腸癌已蟬聯男性癌症榜首長達 14 年！國健署推動每 2 年 1 次糞便潛血檢查（FIT），經篩檢發現的大腸癌有高達 55.4% 為早期（0期與1期），其 5 年相對存活率高達 9 成以上；反之未篩檢者確診時早期僅佔 28.3%。
2. 肝及肝內膽管癌（全癌第4名、男性第5名）：受惠於 B/C 型肝炎公費篩檢普及、抗病毒口服藥物治療與新生兒疫苗政策，肝癌發生率已連續 14 年穩定下降、死亡率連降 13 年，是公衛防癌的最佳見證！
3. 胃癌（全癌第9名）：隨著幽門螺旋桿菌（H. pylori）根除治療的普及化與飲食保鮮習慣改善，胃癌標準化發生率與死亡率長期呈現平穩下降趨勢。
4. 食道癌（男性第6名）：具有極高的性別不對稱性，男性發生率高達女性的 12.8 倍！主因與長期抽菸、過量飲酒、嚼食檳榔等黏膜刺激物高度相關，及早戒除壞習慣並定期胃鏡檢查是保命核心。
5. 善用國家公費篩檢資源，搭配定期無痛消化道內視鏡（胃鏡、大腸鏡）與腹部超音波檢查，及早截斷息肉與慢性發炎病灶，全面守住腸胃肝膽健康！

📖 閱讀本集完整深入衛教專文：
https://drhuanggi.vercel.app/posts/十大癌症中屬於消化系癌症的個別分析

⏱️ 影片時間軸重點：
00:00 最新癌登總覽：消化系統癌症占比極高，大腸癌蟬聯男性榜首14年
00:10 大腸癌黃金篩檢：每兩年糞便潛血篩檢，早期抓出存活率破九成
00:20 肝癌防治成果：B/C肝篩檢與抗病毒藥普及，發生率連降14年
00:30 胃癌防線解析：幽門桿菌積極除菌與飲食改善，發生率穩定下降
00:40 食道癌警訊：男性發生率高達女性12倍，務必遠離菸酒檳榔
00:50 綜合防癌處方：善用公費篩檢，定期內視鏡與腹部超音波追蹤

👨‍⚕️ 關於黃冠智醫師：
現任豐田診所院長、肝膽腸胃科專科醫師。致力於將嚴謹醫學實證轉化為溫暖生動的衛教筆記。
🌐 個人官方網站：https://drhuanggi.vercel.app

#十大癌症 #消化系癌症 #大腸癌 #肝癌 #胃癌 #食道癌 #糞便潛血檢查 #幽門桿菌 #腸胃科 #豐田診所 #黃冠智醫師 #診間說書房
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
    print("🎉【十大癌症中屬於消化系癌症的個別分析】6 分鏡短影音後製與渲染全部完成！")
    print("="*50)
