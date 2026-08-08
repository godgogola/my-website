import os
import sys
from PIL import Image

artifact_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d0bbff17-1170-46fc-a3b2-5bf2112488d8"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")

# 重新定義重繪清單 (微型袖珍場景 Miniature Chibi Diorama，保證上下各有 30% 留白)
PROMPT_SPECS = {
    "AG ratio": {
        "title": "【AG ratio】",
        "file": "ag-ratio.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll with short skirt and white coat sits or stands small (occupying only 35% vertical height on the right), with 30% empty background wall above her head and 30% carpet floor below her boots. On the left, she gently adjusts a cute miniature wooden-and-yarn seesaw balance with a white albumin yarn ball on one side and a blue globulin yarn ball on the other in perfect horizontal balance. 16:9 widescreen diorama, 100% complete body intact."
    },
    "Albumin": {
        "title": "【Albumin】白蛋白的合成與低下原因",
        "file": "albumin白蛋白的合成與低下原因.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background above her hair and floor below her boots. In the center and left, a cute round liver amigurumi doll sits on a low wooden stool knitting tiny white yarn balls like a mini craft factory, while the doctor helps a weak blood vessel doll by weaving a supplementary mesh. 16:9 widescreen diorama, 100% complete body intact."
    },
    "Cystatin C": {
        "title": "【Cystatin C】血清胱蛋白 C",
        "file": "cystatin-c血清胱蛋白-c.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background above her hair and floor below her boots. In the center and left on a low platform, a cute kidney doll and muscle arm doll sit together while tiny glowing pink-purple Cystatin C yarn fairies float gently between them, observed by the doctor with a tiny yarn lens. 16:9 widescreen diorama, 100% complete body intact."
    },
    "Bilirubin": {
        "title": "【膽紅素】單純膽紅素偏高",
        "file": "膽紅素單純膽紅素偏高.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background above her hair and floor below her boots. On the left, a cute smiling liver amigurumi doll rests happily on a soft floor cushion glowing with gentle yellow light, holding a bouquet of low-floating safe green yarn balloons. 16:9 widescreen diorama, 100% complete body intact."
    },
    "Globulin": {
        "title": "【Globulin】球蛋白",
        "file": "globulin球蛋白.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background above her hair and floor below her boots. In the center and left, a cute miniature squad of blue globulin soldier dolls in soft yarn armor build and carry soft foam blocks to form a defensive wall. 16:9 widescreen diorama, 100% complete body intact."
    },
    "HDL": {
        "title": "【HDL】HDL太高是好事嗎",
        "file": "hdlhdl太高是好事嗎.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background above her hair and floor below her boots. On the left, a cute chubby golden-yellow HDL hero doll with a blue cape holds a tiny yarn broom, curiously inspected by the doctor through a magnifying glass. 16:9 widescreen diorama, 100% complete body intact."
    },
    "Carbs": {
        "title": "碳水化合物造成脂肪堆積的機制",
        "file": "碳水化合物造成脂肪堆積的機制.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background above her hair and floor below her boots. On the left, miniature rice-bowl and bread-slice yarn sprites enter and playfully transform into small yellow fat yarn balls arranged on a low shelf. 16:9 widescreen diorama, 100% complete body intact."
    },
    "S-ABCDE": {
        "title": "S-ABCDE 高血壓生活型態調整",
        "file": "s-abcde-高血壓生活型態調整.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS ON PROPS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background above her hair and floor below her boots. On the left and center, a happy red heart doll does gentle exercises next to a plain woven yarn salt shaker (no letters or labels), miniature sneakers, a tiny vegetable basket, and a no-smoking circle. 16:9 widescreen diorama, 100% complete body intact."
    },
    "Gastroparesis_Diagnostic": {
        "title": "【胃輕癱】胃輕癱臨床診斷標準",
        "file": "胃輕癱胃輕癱臨床診斷標準.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with massive empty background wall taking up the top 35% and carpet taking up the bottom 30%. On the left on a low wooden bench, a cute sleepy pink stomach doll rests peacefully next to a miniature wooden hourglass as food yarn particles digest very slowly. 16:9 widescreen diorama, 100% complete body head-to-toe intact."
    },
    "Gastroparesis_vs_Dyspepsia": {
        "title": "【胃輕癱】胃輕癱與消化不良有何不同",
        "file": "胃輕癱胃輕癱與消化不良有何不同.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small in the center-right (occupying only 35% vertical height), with generous 35% empty wall above her hair and wide floor below her boots. On the left rests a sluggish sleepy pale-green gastroparesis stomach doll lying down, while next to it sits an irritable active orange dyspepsia doll puffing gentle yarn waves. 16:9 widescreen diorama, 100% complete body intact."
    },
    "Gastroparesis_Diet": {
        "title": "【胃輕癱】胃輕癱飲食調整與治療",
        "file": "胃輕癱胃輕癱飲食調整與治療.md",
        "prompt": "Cute 3D knitted crochet amigurumi plush doll style, hand-crafted yarn texture, soft wool thread details, cozy felt background, warm soft studio lighting. ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS. Miniature tabletop diorama wide horizontal scene: A tiny cute chibi female doctor amigurumi doll stands small on the right (occupying only 35% vertical height), with generous 35% empty wall above her hair and wide carpet below her boots. On the left, she gently offers a warm bottle of easily digestible liquid yarn broth to a chubby round lazy pink stomach doll whose tummy is full of colorful yarn balls. 16:9 widescreen diorama, 100% complete body intact."
    }
}

def crop_and_deploy(png_path, title, md_file):
    img = Image.open(png_path)
    w, h = img.size
    target_ratio = 16.0 / 9.0
    new_h = int(w / target_ratio)
    left = 0
    top = (h - new_h) // 2
    right = w
    bottom = top + new_h

    cropped = img.crop((left, top, right, bottom))

    # Save to Drive 16:9 PNG
    drive_path = os.path.join(drive_dir, f"{title}.png")
    cropped.save(drive_path, format="PNG")

    # Save to public 16:9 WebP
    webp_name = f"{title}.webp"
    webp_path = os.path.join(public_images_dir, webp_name)
    cropped.save(webp_path, format="WEBP", quality=95)

    print(f"Successfully cropped & deployed 16:9: {title}")

if __name__ == '__main__':
    print(f"Registered {len(PROMPT_SPECS)} target specs for flawless miniature diorama re-generation.")
