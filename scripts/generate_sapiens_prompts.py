import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

prompts_data = [
    {
        'chapter': '04',
        'title': '04、毀天滅地的人類洪水',
        'file': '04-毀天滅地的人類洪水.md',
        'imageName': 'sapiens_04_flood',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a miniature dramatic prehistoric voyage and ecological diorama. A tiny cute crocheted prehistoric explorer doll wearing fur-stitched wool garments steers a simple woven reed boat across sparkling blue yarn ocean waves, arriving at an untouched island savanna populated by gentle, majestic wool megafauna plushies (a giant cute diprotodon, a woolly mammoth, and a friendly saber-toothed cat resting among yarn ferns), depicting the early human migration across the sea and the dawn of prehistoric encounters.'
    },
    {
        'chapter': '05',
        'title': '05、史上最大騙局',
        'file': '05-史上最大騙局.md',
        'imageName': 'sapiens_05_wheat_fraud',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a charming miniature scene depicting the Agricultural Revolution paradox. In the center, a tiny cute crocheted farmer doll wearing a straw hat bends down tending golden yarn wheat stalks with a tiny wooden hoe, while a giant, proud golden wheat-head plush doll stands tall above the fields smiling playfully, surrounded by woven yarn grain baskets and a cute miniature stone mill, illustrating how wheat domesticated humanity.'
    },
    {
        'chapter': '06',
        'title': '06、蓋起監獄高牆',
        'file': '06-蓋起監獄高牆.md',
        'imageName': 'sapiens_06_pyramids_walls',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a miniature ancient city built on shared imagined order. A majestic stepped ziggurat pyramid made of soft sandstone-colored yarn blocks rises at the center, surrounded by safe miniature city walls. Tiny cute crocheted citizens and a miniature scribe doll hold hands around a grand blank stone tablet standing on a pedestal, illuminated by warm glowing braziers, symbolizing how shared myths unite millions.'
    },
    {
        'chapter': '07',
        'title': '07、大腦記憶過載',
        'file': '07-大腦記憶過載.md',
        'imageName': 'sapiens_07_memory_writing',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, an endearing miniature ancient bureaucratic archive. A tiny cute crocheted scribe doll wearing round glasses sits before a small wooden desk, pressing a stylus into a miniature clay-colored yarn tablet. Behind him stand neat wooden shelves stacked with tiny sealed clay scrolls and colorful knotted wool tally strings (quipu), alongside small woven sacks of grain marked with abstract woven tally patterns, depicting the birth of writing to overcome brain memory overload.'
    },
    {
        'chapter': '08',
        'title': '08、歷史從無正義',
        'file': '08-歷史從無正義.md',
        'imageName': 'sapiens_08_social_hierarchy',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a miniature philosophical scene exploring social hierarchy. A stepped wooden and wool podium displays several charming crocheted figurines on different tier steps, while a cute crocheted philosopher explorer doll wearing round glasses and an owl companion examine the artificial staircase with a magnifying glass, revealing that all the figurines are woven from the exact same warm golden yarn, symbolizing the imagined nature of historical castes and inequality.'
    },
    {
        'chapter': '09',
        'title': '09、歷史的方向',
        'file': '09-歷史的方向.md',
        'imageName': 'sapiens_09_unification',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a breathtaking miniature global convergence scene. At the center stands a large, beautifully knitted spherical globe made of colorful patchwork continents. Three flowing braided yarn ribbons (golden for commerce, royal purple for law, and starry sky-blue for faith) spiral inward, uniting miniature villages from around the book into one cohesive world community, watched over by a tiny cute crocheted explorer doll.'
    },
    {
        'chapter': '10',
        'title': '10、金錢的氣味',
        'file': '10-金錢的氣味.md',
        'imageName': 'sapiens_10_money_trust',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a magical miniature marketplace of universal trust. In the center, a tiny cute crocheted merchant doll happily trades with another traveler across a polished wooden counter: on one side are colorful sea shells and barley grains, and on the other are shiny golden yarn coins and stamped silver ingots. A gentle glowing golden aura surrounds the coins, representing universal mutual trust that transcends all borders.'
    },
    {
        'chapter': '11',
        'title': '11、帝國的願景',
        'file': '11-帝國的願景.md',
        'imageName': 'sapiens_11_empire_vision',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a grand miniature cultural fusion diorama. Under a splendid classical knitted triumphal archway and marble-like wool columns, diverse cute crocheted figures in various traditional woven garments (Roman robes, Persian silks, and Han tunics) gather peacefully around a large round table sharing bread and tea, illustrating how imperial order forged universal culture.'
    },
    {
        'chapter': '12',
        'title': '12、宗教的法則',
        'file': '12-宗教的法則.md',
        'imageName': 'sapiens_12_universal_religion',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a serene and sacred miniature spiritual sanctuary. In the center rests a blooming golden-and-white yarn lotus flower glowing with soft divine light, flanked by a miniature tranquil bell pavilion and gentle incense smoke ribbons made of translucent gossamer wool. A tiny cute crocheted monk doll sits in peaceful meditation alongside a forest deer plushie, depicting the universal spiritual laws that brought harmony to diverse peoples.'
    },
    {
        'chapter': '13',
        'title': '13、成敗的祕密',
        'file': '13-成敗的祕密.md',
        'imageName': 'sapiens_13_historical_blindness',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, an intriguing miniature game of historical contingency. In the center, a whimsical giant wooden and brass clockwork kaleidoscope turns, casting colorful yarn patterns across the stage. A tiny cute crocheted explorer doll wearing round glasses stands at a fork in a winding cobblestone yarn path, pondering a fluttering golden butterfly resting on a brass balance scale, illustrating the unpredictable dynamics of historical choices.'
    },
    {
        'chapter': '14',
        'title': '14、發現自己的無知',
        'file': '14-發現自己的無知.md',
        'imageName': 'sapiens_14_ignorance_science',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, an inspiring dawn of the Scientific Revolution. A tiny cute crocheted astronomer explorer doll wearing round glasses stands on a small wooden library ladder, peering through a sleek brass telescope toward an open window filled with glowing yarn star constellations and a crescent moon. Beside him lies a world globe with large blank unexplored areas, proudly embracing the unknown.'
    },
    {
        'chapter': '15',
        'title': '15、科學與帝國的聯姻',
        'file': '15-科學與帝國的聯姻.md',
        'imageName': 'sapiens_15_science_and_empire',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a grand miniature Age of Discovery voyage. A handsome three-masted wooden sailing ship with knitted white wool sails glides across deep blue yarn waves. On the ship deck, a tiny cute crocheted captain and an explorer naturalist doll study a large parchment navigation chart with brass calipers, surrounded by miniature glass jars containing exotic knitted plant specimens and a brass sextant.'
    },
    {
        'chapter': '16',
        'title': '16、資本主義的教條',
        'file': '16-資本主義的教條.md',
        'imageName': 'sapiens_16_capitalist_creed',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, an enchanting miniature grove of credit and enterprise. At the center stands a magical growing money tree with shimmering golden wool coins and green leaf pom-poms. A tiny cute crocheted entrepreneur doll waters the tree with a golden watering can fed by a bubbling spring labeled with a bright spark of faith in the future, while miniature joint-venture ships set sail from a tiny harbor.'
    },
    {
        'chapter': '17',
        'title': '17、工業的巨輪',
        'file': '17-工業的巨輪.md',
        'imageName': 'sapiens_17_industrial_wheels',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a fascinating miniature Industrial Revolution workshop. At the center, an intricate miniature steam engine with rotating brass-and-yarn cogwheels and a puff of white cotton steam powers a glowing electric bulb and a small woven textile loom. A tiny cute crocheted engineer doll holding a miniature wrench smiles proudly next to a steady mechanical clockwork tower, symbolizing the transformation of energy into limitless power.'
    },
    {
        'chapter': '18',
        'title': '18、一場永遠的革命',
        'file': '18-一場永遠的革命.md',
        'imageName': 'sapiens_18_permanent_revolution',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a bustling miniature modern life transition. In the center, a charming miniature railway station with a gleaming steam train stands beneath a large, synchronized vintage clock tower. A tiny cute crocheted traveler doll with a small suitcase checks a neat miniature departure timetable, while cozy streetlamps illuminate organized modern avenues, representing the precise schedules and societal shifts of the modern era.'
    },
    {
        'chapter': '19',
        'title': '19、從此過著幸福快樂的日子',
        'file': '19-從此過著幸福快樂的日子.md',
        'imageName': 'sapiens_19_happiness_meaning',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a heartwarming miniature philosophy of happiness. Beside a warm glowing knitted hearth, a tiny cute crocheted explorer doll sits in a plush armchair drinking hot cocoa, holding a glowing golden heart-shaped yarn ball that radiates tranquil light. On a small wooden table nearby rests a balanced scale weighing a heap of gold coins against a simple bouquet of wildflowers and a loving family portrait, symbolizing that true happiness comes from inner meaning and connection.'
    },
    {
        'chapter': '20',
        'title': '20、智人末日',
        'file': '20-智人末日.md',
        'imageName': 'sapiens_20_end_of_sapiens',
        'subject': 'On top of a giant open knitted book with blank cream wool pages, a breathtaking sci-fi and philosophical miniature future. In the center stands a whimsical, futuristic cute crocheted humanoid cyborg doll with one delicate mechanical clockwork arm and luminescent fiber-optic yarn hair, gently holding a shimmering double-helix DNA strand woven from glowing rainbow wool. Flanked by starry nebula bokeh and miniature floating cybernetic butterfly plushies, gazing toward the infinite horizon of intelligent design.'
    }
]

base_template = (
    "Generate a blog post cover image with an aspect ratio of 16:9 (landscape). "
    "Subject: {subject} "
    "Art Style: Rendered in a realistic, cute, handcrafted amigurumi knitted style (crochet wool texture) miniature book-world diorama. "
    "Texture: High-quality soft yarn texture, visible knit stitches, fuzzy wool and felt details. "
    "Characters: Cute, miniature chibi-style knitted explorer dolls and wise animal dolls, button-like eyes, warm and curious expressions (NO doctors, NO white coats, NO stethoscopes). "
    "Colors: Rich, warm, and inviting harmonious palette (cream wool, warm amber, glowing golds, soft pastels, cozy earth tones). "
    "Composition: Central focus on the giant open knitted book stage with balanced negative space on the sides. "
    "Background: Cozy blurred library study with soft stacked wool books and warm reading lamp bokeh. "
    "Technical: High quality, 3D render, macro photography, tilt-shift miniature effect, photorealistic warm lighting, soft depth of field, wide shot. "
    "Constraints: NO TEXT, no letters, no numbers, no watermarks, no labels, no typography, no charts, no infographics, no UI elements, no medical attire. Full bleed framing."
)

output = []
for p in prompts_data:
    full_prompt = base_template.format(subject=p['subject'])
    output.append({
        'chapter': p['chapter'],
        'title': p['title'],
        'file': p['file'],
        'imageName': p['imageName'],
        'prompt': full_prompt
    })

output_path = 'scripts/sapiens_17_prompts.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(output)} prompts to {output_path}")
