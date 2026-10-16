#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
衛教短影音自動化後製 Agent - 專屬專案管線
專案名稱：糖尿病腎病變 uACR 處置
工作目錄：c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/糖尿病腎病變 uACR 處置
成片輸出：c:/Users/X1 Yoga Gen7/Desktop/Antigravity_Projects/影片加工/糖尿病腎病變 uACR 處置/糖尿病腎病變 uACR 處置.mp4
"""

import os
import sys
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_NAME = "糖尿病腎病變 uACR 處置"
BASE_DIR = os.path.abspath(r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工")
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
FFMPEG_BIN = os.path.join(BASE_DIR, "ffmpeg.exe") if os.path.exists(os.path.join(BASE_DIR, "ffmpeg.exe")) else "ffmpeg"
FONT_PATH = os.path.join(BASE_DIR, "jf-openhuninn-2.0.ttf")
LOGO_SRC = os.path.join(BASE_DIR, "turtle_logo.png")

def step1_generate_srt():
    print("【步驟 1】生成毫秒級繁體中文字幕 (output.srt)...")
    subtitles = [
        # 鏡頭 1: 核心指標與分級標準 (Part 1, 0s ~ 10.010s)
        ("00:00:00,000", "00:00:03,600", "檢測尿白蛋白比值是護腎核心關鍵"),
        ("00:00:03,740", "00:00:06,100", "30 以下屬於正常標準"),
        ("00:00:06,200", "00:00:08,700", "30 與 300 是分級界限！"),

        # 鏡頭 2: 正常值與定期篩檢 (Part 2, 10.010s ~ 20.020s)
        ("00:00:09,660", "00:00:12,500", "別以為數值正常就能大意"),
        ("00:00:13,760", "00:00:16,000", "每年至少定期篩檢一次"),
        ("00:00:16,220", "00:00:19,600", "高風險群更要及早護心護腎！"),

        # 鏡頭 3: 中度白蛋白尿處置 (Part 3, 20.020s ~ 30.030s)
        ("00:00:19,680", "00:00:23,000", "比值 30 到 300 屬早期腎損傷"),
        ("00:00:23,360", "00:00:24,750", "調足基礎防線"),
        ("00:00:24,820", "00:00:27,500", "再及早疊加排糖藥與腸泌素！"),

        # 鏡頭 4: 2026 ADA 最新強推方案 (Part 4, 30.030s ~ 40.040s)
        ("00:00:29,710", "00:00:32,000", "比值破百除了 ARB"),
        ("00:00:32,050", "00:00:36,400", "同步加上 SGLT2 抑制劑和 nsMRA"),
        ("00:00:36,550", "00:00:39,000", "尿白蛋白大降 52%！"),

        # 鏡頭 5: 重度白蛋白尿多重組合 (Part 5, 40.040s ~ 50.050s)
        ("00:00:39,630", "00:00:43,000", "比值破 300 屬於高風險群"),
        ("00:00:43,050", "00:00:45,500", "必須採取多重保護"),
        ("00:00:45,610", "00:00:48,300", "並及早會診腎臟專科！"),

        # 鏡頭 6: 綜合管理與血壓控制 (Part 6, 50.050s ~ 60.060s)
        ("00:00:49,760", "00:00:53,000", "別因初期腎功能微降就緊張"),
        ("00:00:53,560", "00:00:55,600", "波動三成內屬正常"),
        ("00:00:55,780", "00:00:58,200", "收縮壓控制在 120 內！")
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

    lines = ["糖尿病腎病變", "uACR 篩檢與臨床處置"]
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

    # 濾鏡圖層鏈：
    # 1. 6 段影音無縫串聯 concat
    # 2. 升頻至 1080p Lanczos
    # 3. 疊加 3D 左上字卡 (0:0)
    # 4. 疊加小烏龜徽章 (180:270，雙行標題下方舒適呼吸區)
    # 5. 燒錄粉圓體高畫質字幕 (白字黑描邊，底部 35px 邊距)
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
        ("00:00:04.500", "preview_uacr_01_classification.jpg"),
        ("00:00:15.000", "preview_uacr_02_screening.jpg"),
        ("00:00:25.000", "preview_uacr_03_moderate.jpg"),
        ("00:00:35.000", "preview_uacr_04_confidence_combo.jpg"),
        ("00:00:45.000", "preview_uacr_05_severe_multitarget.jpg"),
        ("00:00:55.000", "preview_uacr_06_egfr_bp_control.jpg"),
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
    desc_text = """在糖尿病照護中，許多糖友往往只緊盯著飯前血糖與糖化血色素（HbA1c），卻忽略了腎臟微血管正在悄悄承受壓力！根據 2026 美國糖尿病學會（ADA）與國際腎臟病指引，尿液白蛋白與肌酸酐比值（uACR）是評估早期腎臟微血管損傷與未來心血管事件的最核心敏感指標！

臨床上以 30 與 300 mg/g 作為關鍵分級防線：
1. uACR < 30 mg/g（正常至輕度）：每年至少規律篩檢一次 uACR 與 eGFR；若合併高心腎風險，及早部署器官保護藥物。
2. uACR 30–300 mg/g（中度微量白蛋白尿）：代表腎絲球微血管早期受損，首選滴定至最大耐受劑量 ACEi/ARB，並及早疊加 SGLT2 抑制劑或 GLP-1 受體激動劑。
3. 2026 ADA 最新實證強推：若 uACR ≥ 100 mg/g，建議同步聯合啟動「SGLT2 抑制劑 + 非類固醇礦物皮質素受體拮抗劑（nsMRA，如 Finerenone）」，可帶來高達 52% 的顯著蛋白尿降幅！
4. uACR > 300 mg/g（重度白蛋白尿）：屬於心腎事件極高危險群，需採取多重藥物組合拳阻斷，並及早轉診腎臟專科共同照護。
5. 剛啟動器官保護藥物時，若血清肌酸酐或 eGFR 波動在 30% 以內屬於正常的腎血流動力學調節效應，切勿驚慌停藥；收縮壓控制達到 < 120 mmHg，穩健守護腎臟與心血管！

📖 閱讀本集完整深入衛教專文：
https://drhuanggi.vercel.app/posts/糖尿病腎病變-uacr-處置

⏱️ 影片時間軸重點：
00:00 核心指標與分級標準：uACR 30 與 300 mg/g 關鍵防線
00:10 正常值與篩檢頻率：每年至少篩檢一次，心腎高風險及早預防
00:20 中度微量白蛋白尿：調足 ACEi/ARB 基礎，疊加排糖藥與腸泌素
00:30 2026 ADA 最新方案：uACR ≥ 100 同步聯合 SGLT2i + nsMRA 降 52%
00:40 重度白蛋白尿處置：多重組合拳保護，及早會診腎臟專科
00:50 綜合管理與血壓目標：預期 eGFR 波動正常範圍，收縮壓 < 120 mmHg

👨‍⚕️ 關於黃冠智醫師：
現任豐田診所院長、肝膽腸胃科專科醫師。致力於將嚴謹醫學實證轉化為溫暖生動的衛教筆記。
🌐 個人官方網站：https://drhuanggi.vercel.app

#糖尿病 #糖尿病腎病變 #uACR #微量白蛋白尿 #慢性腎臟病 #SGLT2抑制劑 #Finerenone #心腎保護 #豐田診所 #黃冠智醫師 #診間說書房
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
    print("🎉【糖尿病腎病變 uACR 處置】6 分鏡短影音後製與渲染全部完成！")
    print("="*50)
