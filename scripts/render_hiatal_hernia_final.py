import os
import sys
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工"
PROJ_NAME = "食道裂孔疝氣的原因"
PROJ_DIR = os.path.join(BASE_DIR, PROJ_NAME)
FFMPEG = os.path.join(BASE_DIR, "ffmpeg.exe")
FONT_PATH = os.path.join(BASE_DIR, "jf-openhuninn-2.0.ttf")
LOGO_SRC = os.path.join(BASE_DIR, "turtle_logo.png")

os.makedirs(PROJ_DIR, exist_ok=True)

# 1. 產生 3D 立體字卡 dynamic_title.png
def generate_title_card():
    output_png = os.path.join(PROJ_DIR, "dynamic_title.png")
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_size = 60
    font = ImageFont.truetype(FONT_PATH, font_size)

    stroke_width = 8
    fill_color = (255, 90, 180, 255)       # 亮桃紅主色
    stroke_color = (60, 20, 90, 255)       # 深紫外框
    x0, y0 = 140, 80
    line_spacing = 16

    lines = ["食道裂孔疝氣", "胃部滑脫移位常見成因"]
    cur_y = y0
    for line in lines:
        for ox, oy in [(4, 4), (5, 5), (6, 6)]:
            draw.text((x0 + ox, cur_y + oy), line, font=font, fill=stroke_color, stroke_width=stroke_width, stroke_fill=stroke_color)
        draw.text((x0, cur_y), line, font=font, fill=fill_color, stroke_width=stroke_width, stroke_fill=stroke_color)
        bbox = draw.textbbox((x0, cur_y), line, font=font, stroke_width=stroke_width)
        cur_y += (bbox[3] - bbox[1]) + line_spacing

    img.save(output_png, "PNG")
    print(f"✅ 3D字卡生成成功: {output_png}")
    return output_png

# 2. 產生精確字幕檔 output.srt
def generate_srt():
    srt_path = os.path.join(PROJ_DIR, "output.srt")
    transcript_path = os.path.join(PROJ_DIR, "transcript.txt")

    subtitles = [
        # Part 1 (0.00s ~ 10.01s): 火燒心、胃藥不靈、胃滑脫警訊
        ("00:00:00,000", "00:00:03,100", "吃飽經常火燒心還一直打嗝"),
        ("00:00:03,160", "00:00:05,400", "胃藥吃了總好不徹底"),
        ("00:00:05,600", "00:00:08,200", "小心是胃滑進胸腔了！"),

        # Part 2 (10.01s ~ 20.02s): 裂孔韌帶老化、腹壓推擠機制
        ("00:00:10,040", "00:00:13,200", "橫膈膜裂孔韌帶老化鬆弛"),
        ("00:00:13,800", "00:00:16,200", "肚子壓力大往上擠"),
        ("00:00:16,400", "00:00:18,800", "胃頂端就會滑進胸口！"),

        # Part 3 (20.02s ~ 30.03s): 內視鏡確診與阻斷逆流藥物
        ("00:00:19,820", "00:00:22,800", "做無痛胃鏡能精準確診"),
        ("00:00:23,040", "00:00:25,800", "搭配消脹與抑制胃酸藥物"),
        ("00:00:25,900", "00:00:28,500", "迅速封閉酸水逆流！"),

        # Part 4 (30.03s ~ 40.04s): 減輕腹部負擔、生活保護指引
        ("00:00:30,400", "00:00:32,200", "減輕腹部脂肪"),
        ("00:00:32,400", "00:00:34,200", "少用力搬重物"),
        ("00:00:34,680", "00:00:38,500", "吃飽別躺下，守護橫膈膜讓逆流不再來！")
    ]

    srt_lines = []
    txt_lines = []
    for idx, (s, e, text) in enumerate(subtitles, 1):
        srt_lines.append(f"{idx}\n{s} --> {e}\n{text}\n")
        txt_lines.append(f"[{s} -> {e}] {text}")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"✅ 字幕與文稿已生成: {srt_path} (共 {len(subtitles)} 條)")
    return srt_path

# 3. 執行壓制渲染
def render_video():
    generate_title_card()
    srt_file = generate_srt()

    local_logo = os.path.join(PROJ_DIR, "turtle_logo.png")
    if not os.path.exists(local_logo) and os.path.exists(LOGO_SRC):
        shutil.copy2(LOGO_SRC, local_logo)

    merged_raw = os.path.join(PROJ_DIR, "merged_raw.mp4")
    final_output = os.path.join(PROJ_DIR, "食道裂孔疝氣的原因.mp4")
    srt_ffmpeg = srt_file.replace("\\", "/").replace(":", "\\:")
    font_ffmpeg = FONT_PATH.replace("\\", "/").replace(":", "\\:")

    # 濾鏡鏈：Lanczos 升頻至 1080p + 疊加 3D 字卡 + 疊加小烏龜 + 燒錄字幕
    filter_complex = (
        "[0:v]scale=1920:1080:flags=lanczos[v0];"
        "[1:v]scale=1920:1080[vtitle];"
        "[2:v]scale=90:90[vlogo];"
        "[v0][vtitle]overlay=0:0[v1];"
        "[v1][vlogo]overlay=140:270[v2];"
        f"[v2]subtitles='{srt_ffmpeg}':force_style='Fontname=jf-openhuninn-2.0,Fontsize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,MarginV=38,Alignment=2'[vout]"
    )

    cmd = [
        FFMPEG,
        "-i", merged_raw,
        "-i", os.path.join(PROJ_DIR, "dynamic_title.png"),
        "-i", local_logo,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        final_output, "-y"
    ]

    print("🚀 開始執行 1080p Lanczos 壓制渲染 (CRF 18)...")
    subprocess.run(cmd, check=True)
    print(f"🎉 影片渲染大成功: {final_output} ({os.path.getsize(final_output)} bytes)")

    # 4. 截取分鏡視覺預覽圖
    previews = [
        ("00:00:03.500", "preview_01_hernia_symptoms.jpg"),
        ("00:00:13.500", "preview_02_ligament_laxity.jpg"),
        ("00:00:23.500", "preview_03_endoscopy_meds.jpg"),
        ("00:00:33.500", "preview_04_lifestyle_habits.jpg"),
    ]
    for ts, fname in previews:
        out_jpg = os.path.join(PROJ_DIR, fname)
        subprocess.run([
            FFMPEG, "-ss", ts, "-i", final_output,
            "-vframes", "1", "-q:v", "2", out_jpg, "-y"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"📸 分鏡截圖成功: {fname}")

    # 5. 輸出 YouTube 專屬發布文案 新增說明.txt
    desc_content = """吃飽經常火燒心、喉嚨湧上酸水，吞了胃藥還是反覆發作？小心這可能不只是單純胃酸過多，而是「食道裂孔疝氣（橫膈膜疝氣）」在作怪！

許多長年飽受胃食道逆流所苦的朋友，往往在接受無痛胃鏡檢查時，才發現胃的頂端（賁門部）竟然悄悄「滑」進了胸腔！當橫膈膜上的食道裂孔因老化退化、膠原蛋白流失，或是長期腹壓過大（肥胖、久咳、便秘用力、搬重物），這扇原本緊閉的「活門」鬆弛被撐開，胃酸與食物便暢通無阻地逆流而上。

掌握黃金保護原則：及早透過高品質內視鏡精準評估裂孔大小，搭配抑制胃酸與消脹促動力藥物；在生活中減輕腹部負擔、避免飯後立刻平躺，徹底守護橫膈膜，重獲舒暢清爽的日常！

📖 閱讀本集完整深入衛教專文：
https://drhuanggi.vercel.app/posts/食道裂孔疝氣的原因

⏱️ 影片時間軸重點：
00:00 鏡頭1：火燒心打嗝好不了？小心胃部滑進胸腔
00:10 鏡頭2：橫膈膜裂孔韌帶鬆弛與腹壓推擠成因
00:20 鏡頭3：無痛胃鏡精準診斷與制酸封閉逆流
00:30 鏡頭4：減輕腹重、守護橫膈膜之生活處方

👨‍⚕️ 關於黃冠智醫師：
現任豐田診所院長、肝膽腸胃科專科醫師。致力於將嚴謹醫學實證轉化為溫暖生動的衛教筆記。
🌐 個人官方網站：https://drhuanggi.vercel.app

#食道裂孔疝氣 #橫膈膜疝氣 #胃食道逆流 #火燒心 #無痛胃鏡 #腸胃健康 #黃冠智醫師 #豐田診所"""

    desc_path = os.path.join(PROJ_DIR, "新增說明.txt")
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write(desc_content.strip())
    print(f"📝 YouTube 發布文案已生成: {desc_path}")

if __name__ == "__main__":
    render_video()
