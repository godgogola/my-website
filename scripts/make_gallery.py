import os

def create_gallery():
    base = r'c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工'
    html = ['<html><body style="background:#222;color:#eee;font-family:sans-serif;">']
    
    for cf in ['補足片段1_切分', '補足片段2_切分', '補足片段3_切分']:
        p = os.path.join(base, cf)
        if not os.path.exists(p):
            continue
        html.append(f'<h2>{cf}</h2><div style="display:flex;flex-wrap:wrap;gap:10px;">')
        jpgs = sorted([f for f in os.listdir(p) if f.endswith('.jpg')])
        for j in jpgs:
            full_p = os.path.join(p, j).replace('\\', '/')
            name = j.replace('.jpg', '')
            html.append(f'<div style="text-align:center;"><img src="file:///{full_p}" width="160" height="284" style="border-radius:6px;object-fit:cover;"/><br><small>{name}</small></div>')
        html.append('</div>')
    html.append('</body></html>')
    
    out_p = os.path.join(base, 'clips_gallery.html')
    with open(out_p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))
    print(f'Gallery written to: {out_p}')

create_gallery()
