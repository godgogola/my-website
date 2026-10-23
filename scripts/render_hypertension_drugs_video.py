import os
import sys
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_NAME = "高血壓藥物在一般族群及共病族群的選擇"
BASE_DIR = os.path.abspath(r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工")
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
FFMPEG_BIN = os.path.join(BASE_DIR, "ffmpeg.exe") if os.path.exists(os.path.join(BASE_DIR, "ffmpeg.exe")) else "ffmpeg"
FONT_PATH = os.path.join(BASE_DIR, "jf-openhuninn-2.0.ttf")
LOGO_SRC = os.path.join(BASE_DIR, "turtle_logo.png")

os.makedirs(PROJECT_DIR, exist_ok=True)

def step1_generate_srt():
    print("【步驟 1】生成毫秒級繁體中文字幕 (output.srt)...")
    subtitles = [
        # 鏡頭 1: 單錠複方與量身訂做 (Part 1, 0.000s ~ 10.010s)
        ("00:00:00,000", "00:00:03,120", "高血壓治療已不再單藥慢慢加量"),
        ("00:00:03,340", "00:00:07,140", "最新指引強調早期使用單錠複方"),
        ("00:00:07,300", "00:00:09,420", "並依共病量身訂做！"),

        # 鏡頭 2: 一般族群標準階梯 (Part 2, 10.010s ~ 20.020s)
        ("00:00:09,700", "00:00:13,360", "無共病患者優先選 ACEI 或 ARB"),
        ("00:00:13,460", "00:00:15,660", "搭配 CCB 或利尿劑"),
        ("00:00:15,920", "00:00:19,000", "頑固型高血壓再優先加上 MRA！"),

        # 鏡頭 3: 冠心病與心衰竭 (Part 3, 20.020s ~ 30.030s)
        ("00:00:19,760", "00:00:24,880", "冠心病與心衰竭，首選乙型阻斷劑搭配 ACEI 或 ARB"),
        ("00:00:24,880", "00:00:29,840", "射出率減少型心衰竭，更需結合 MRA 與 SGLT2 抑制劑！"),

        # 鏡頭 4: 慢性腎病與糖尿病護腎 (Part 4, 30.030s ~ 40.040s)
        ("00:00:29,940", "00:00:33,980", "慢性腎病與糖尿病，首選 ACEI 或 ARB"),
        ("00:00:34,080", "00:00:36,920", "並可搭配 SGLT2 抑制劑護腎"),
        ("00:00:37,420", "00:00:40,060", "切記，ACEI 與 ARB 嚴禁混用！"),

        # 鏡頭 5: 中風預防與孕婦禁忌 (Part 5, 40.040s ~ 50.050s)
        ("00:00:40,120", "00:00:43,820", "預防中風復發，首選 ACEI 或 ARB 搭配利尿劑"),
        ("00:00:43,920", "00:00:47,680", "但孕婦絕對禁用 ACEI、ARB 與 MRA"),
        ("00:00:47,940", "00:00:49,780", "需改用安全降壓藥！"),

        # 鏡頭 6: 高齡長者慢調防跌倒 (Part 6, 50.050s ~ 60.050s)
        ("00:00:50,520", "00:00:53,320", "高齡長者優先選 CCB 或利尿劑"),
        ("00:00:53,320", "00:00:55,600", "應避免起始使用單錠複方"),
        ("00:00:55,720", "00:00:57,320", "採單藥緩慢調整"),
        ("00:00:57,500", "00:01:00,000", "預防低血壓跌倒，安全穩血壓！")
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

    lines = ["高血壓降壓藥", "一般與共病族群用藥選擇"]
    cur_y = y0

    for line in lines:
        # 多層立體厚度浮雕效果
        for ox, oy in [(4, 4), (5, 5), (6, 6)]:
            draw.text(
                (x0 + ox, cur_y + oy),
                line,
                font=font,
                fill=stroke_color,
                stroke_width=stroke_width,
                stroke_fill=stroke_color
            )
        # 主文字
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
        ("00:00:04.500", "preview_01_intro_spc.jpg"),
        ("00:00:14.500", "preview_02_acd_ladder.jpg"),
        ("00:00:24.500", "preview_03_cad_hfref.jpg"),
        ("00:00:34.500", "preview_04_ckd_diabetes.jpg"),
        ("00:00:44.500", "preview_05_stroke_pregnancy.jpg"),
        ("00:00:54.500", "preview_06_elderly_stepped.jpg"),
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
    desc_text = """高血壓降壓藥別再一顆一顆慢慢加！最新國際高血壓治療指引（包含 2022 台灣 TSOC/THS、2024 歐洲 ESC 與 2025 美國 AHA/ACC）已全面革新：高血壓用藥的核心策略在於「早期單錠複方 (SPC)」與「依據共病量身訂做」！

📌 高血壓用藥關鍵指引解析：
1. 一般高血壓標準階梯（無特殊共病）：
   - 第一步（起始治療）：優先雙藥起始，首選 A (ACEI/ARB) + C (CCB) 或 D (Thiazide 類利尿劑)。
   - 第二步（未達標）：升級低劑量三藥聯合（A + C + D）。
   - 第三步：調升至足量或最大耐受劑量。
   - 第四步（頑固型高血壓）：優先加上保鉀利尿劑／礦物皮質素受體拮抗劑（MRA，如 Spironolactone）。
2. 特定臨床共病族群優先選擇：
   - 心臟衰竭 (HFrEF)：首選 ACEI/ARB + 乙型阻斷劑 (Beta-blocker) + MRA + SGLT2 抑制劑！絕對避免非 DHP 鈣離子阻斷劑（如 Verapamil、Diltiazem）。
   - 冠狀動脈疾病 (CAD) / 心肌梗塞後：必備乙型阻斷劑 + ACEI/ARB，降低心肌耗氧量並預防心室重塑。
   - 慢性腎臟病 (CKD) 與蛋白尿：首選 ACEI 或 ARB 降低腎絲球內壓、減少蛋白尿；但【切記 ACEI 與 ARB 嚴禁混用】，防急性腎衰與高血鉀！
   - 糖尿病：首選 ACEI 或 ARB 護腎，可搭配 SGLT2 抑制劑；慎用乙型阻斷劑避免掩蓋低血糖。
   - 預防腦中風復發：首選 ACEI/ARB 搭配 Thiazide 類利尿劑。
3. 特殊族群重大安全叮嚀：
   - 孕婦高血壓：【絕對禁用 ACEI、ARB 與 MRA】（具嚴重胎兒毒性），改選 Labetalol、Methyldopa 或長效 Nifedipine。
   - 高齡長者 / 單純收縮期高血壓：首選 CCB 或利尿劑，應避免一開始使用單錠複方，建議「單藥緩慢滴定」，以防降壓過快引發姿勢性低血壓與跌倒！

📖 閱讀本集完整深入衛教專文：
https://drhuanggi.vercel.app/posts/高血壓藥物在一般族群及共病族群的選擇

⏱️ 影片時間軸重點：
00:00 告別單藥慢慢加：最新指引推動早期單錠複方與量身訂做
00:10 一般族群階梯治療：A+C 或 A+D 起始，頑固型升級 MRA
00:20 心臟共病首選：心衰竭與心梗必備乙型阻斷劑，結合 MRA 與排糖藥
00:30 腎病蛋白尿與糖尿病：ACEI/ARB 護腎第一線，切記兩者嚴禁混搭
00:40 中風預防與孕婦禁忌：中風搭配利尿劑，孕婦嚴禁使用 ACEI/ARB
00:50 高齡長輩用藥安全：避免一開始複方，單藥慢調預防低血壓跌倒

👨‍⚕️ 關於黃冠智醫師：
現任豐田診所院長、肝膽腸胃科專科醫師。致力於將嚴謹醫學實證轉化為溫暖生動的衛教筆記。
🌐 個人官方網站：https://drhuanggi.vercel.app

#高血壓 #高血壓藥物 #降壓藥 #心臟衰竭 #心肌梗塞 #慢性腎臟病 #蛋白尿 #糖尿病 #單錠複方 #豐田診所 #黃冠智醫師 #診間說書房
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
    print(f"🎉【{PROJECT_NAME}】6 分鏡短影音後製與 1080p 壓制渲染全部完成！")
    print("="*50)
