import re

with open("public/2026暑假.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS style
style_old = """        body {
            font-family: 'Inter', 'Noto Sans TC', sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
        }"""

style_new = """        body {
            font-family: 'Inter', 'Noto Sans TC', sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            font-size: 16px;
            line-height: 1.65;
        }"""

content = content.replace(style_old, style_new)

# 2. Header
content = re.sub(
    r'<h1 class="font-bold text-lg sm:text-xl text-slate-800 leading-tight">墨爾本 12 天親子遊</h1>\s*<p class="text-xs text-slate-500 font-medium">8/15 \(六\) ➔ 8/26 \(三\) 完整接駁與景點導航</p>',
    '<h1 class="font-black text-xl sm:text-2xl text-slate-900 leading-tight">墨爾本 12 天親子遊</h1>\n                    <p class="text-sm sm:text-base text-slate-600 font-medium">8/15 (六) ➔ 8/26 (三) 完整接駁與景點導航</p>',
    content
)

# Header buttons
content = content.replace('class="px-3 py-2 text-xs sm:text-sm font-semibold', 'class="px-4 py-2.5 text-sm sm:text-base font-bold')

# 3. Main container max-w-7xl -> max-w-5xl
content = content.replace('max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6', 'max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8')

# 4. Banner
content = content.replace('text-2xl sm:text-3xl font-extrabold tracking-tight leading-snug', 'text-3xl sm:text-4xl font-black tracking-tight leading-tight')
content = content.replace('text-slate-300 text-xs sm:text-sm leading-relaxed max-w-2xl', 'text-slate-200 text-base sm:text-lg leading-relaxed max-w-2xl')
content = content.replace('class="px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs flex items-center gap-1"', 'class="px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-sm sm:text-base font-semibold flex items-center gap-1.5"')
content = content.replace('class="px-2.5 py-1 rounded-md bg-sky-500/20 text-sky-300 border border-sky-500/30 text-xs flex items-center gap-1"', 'class="px-3 py-1.5 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/30 text-sm sm:text-base font-semibold flex items-center gap-1.5"')

# Quick info panel
content = content.replace('text-xs font-semibold text-sky-200 tracking-wider uppercase', 'text-sm sm:text-base font-bold text-sky-200 tracking-wider uppercase')
content = content.replace('text-xs space-y-1.5 text-slate-200', 'text-sm sm:text-base space-y-2 text-slate-100 font-medium')
content = content.replace('w-full py-2 bg-sky-500 hover:bg-sky-400 text-white font-semibold text-xs rounded-xl shadow transition text-center flex items-center justify-center gap-2', 'w-full py-3 bg-sky-500 hover:bg-sky-400 text-white font-bold text-sm sm:text-base rounded-xl shadow transition text-center flex items-center justify-center gap-2')

# 5. Search input & Filter Chips
content = content.replace('text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500', 'text-sm sm:text-base py-2.5 focus:outline-none focus:ring-2 focus:ring-brand-500')
content = content.replace('px-3 py-1.5 text-xs font-medium rounded-xl whitespace-nowrap transition bg-brand-600', 'px-4 py-2 text-sm sm:text-base font-bold rounded-xl whitespace-nowrap transition bg-brand-600')
content = content.replace('px-3 py-1.5 text-xs font-medium rounded-xl whitespace-nowrap transition bg-slate-100', 'px-4 py-2 text-sm sm:text-base font-bold rounded-xl whitespace-nowrap transition bg-slate-100')
content = content.replace('day-tab px-3 py-1.5 rounded-lg bg-slate-800 text-white text-xs font-semibold', 'day-tab px-4 py-2 rounded-xl bg-slate-800 text-white text-sm sm:text-base font-bold')
content = content.replace('text-xs font-medium whitespace-nowrap hover:bg-brand-50', 'text-sm sm:text-base font-bold whitespace-nowrap hover:bg-brand-50')
content = content.replace('px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700', 'px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700')

# 6. Day Cards
# Badge D1..D12
content = content.replace('w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center font-black text-sm', 'w-12 h-12 rounded-2xl bg-sky-100 text-sky-800 flex items-center justify-center font-black text-base sm:text-lg shrink-0')

# Day title
content = content.replace('font-bold text-base sm:text-lg text-slate-800', 'font-black text-xl sm:text-2xl text-slate-900')
# Day subtitle
content = content.replace('class="text-xs text-slate-500"', 'class="text-sm sm:text-base text-slate-600 font-medium mt-0.5"')
# Day badge (e.g. 飛行起航)
content = content.replace('text-[10px] font-semibold', 'text-xs sm:text-sm font-bold')

# Checkbox
content = content.replace('text-xs font-medium text-slate-500 cursor-pointer', 'text-sm sm:text-base font-bold text-slate-600 cursor-pointer')
content = content.replace('class="w-4 h-4 rounded text-brand-600', 'class="w-5 h-5 rounded text-brand-600')

# Inner event cards
content = content.replace('p-3.5 rounded-xl bg-slate-50 border border-slate-100 space-y-1.5', 'p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-2.5')

# Time tags & reference badges
content = content.replace('text-xs font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded', 'text-sm sm:text-base font-extrabold text-brand-800 bg-brand-100/70 px-3 py-1 rounded-lg')
content = content.replace('text-xs text-amber-700 font-semibold bg-amber-50 px-2 py-0.5 rounded border border-amber-200', 'text-sm sm:text-base text-amber-800 font-bold bg-amber-50 px-3 py-1 rounded-lg border border-amber-200')
content = content.replace('text-xs text-indigo-700 font-semibold bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200', 'text-sm sm:text-base text-indigo-800 font-bold bg-indigo-50 px-3 py-1 rounded-lg border border-indigo-200')
content = content.replace('text-xs text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200', 'text-sm sm:text-base text-emerald-800 font-bold bg-emerald-50 px-3 py-1 rounded-lg border border-emerald-200')
content = content.replace('text-xs text-rose-700 font-semibold bg-rose-50 px-2 py-0.5 rounded border border-rose-200', 'text-sm sm:text-base text-rose-800 font-bold bg-rose-50 px-3 py-1 rounded-lg border border-rose-200')
content = content.replace('text-xs text-sky-700 font-semibold bg-sky-50 px-2 py-0.5 rounded border border-sky-200', 'text-sm sm:text-base text-sky-800 font-bold bg-sky-50 px-3 py-1 rounded-lg border border-sky-200')

# Event titles
content = content.replace('font-bold text-sm text-slate-800', 'font-black text-lg sm:text-xl text-slate-900')

# Event paragraph text
content = content.replace('class="text-xs text-slate-600"', 'class="text-base sm:text-lg text-slate-700 leading-relaxed"')

# Links
content = content.replace('text-[11px] font-medium text-brand-600 hover:underline', 'text-sm sm:text-base font-bold text-brand-600 hover:underline inline-flex items-center gap-1.5')

# Alert boxes inside events
content = content.replace('p-2.5 rounded-lg bg-sky-50 border border-sky-100 text-xs text-sky-800 space-y-1', 'p-4 rounded-xl bg-sky-50 border border-sky-200 text-sm sm:text-base text-sky-900 space-y-1.5')
content = content.replace('p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-800 space-y-1', 'p-4 rounded-xl bg-amber-50 border border-amber-200 text-sm sm:text-base text-amber-900 space-y-1.5')
content = content.replace('p-2.5 rounded-lg bg-emerald-50 border border-emerald-100 text-xs text-emerald-800 space-y-1', 'p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-sm sm:text-base text-emerald-900 space-y-1.5')

content = content.replace('text-[11px] space-y-0.5', 'text-sm sm:text-base space-y-1')
content = content.replace('text-xs space-y-1', 'text-sm sm:text-base space-y-1.5')

# Floating back button
content = content.replace('px-4 py-2.5 rounded-full bg-slate-900/90 hover:bg-slate-900 text-white text-xs font-semibold', 'px-5 py-3 rounded-full bg-slate-900/90 hover:bg-slate-900 text-white text-sm sm:text-base font-bold')

with open("public/2026暑假.html", "w", encoding="utf-8") as f:
    f.write(content)

with open("public/2026暑假/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Upgraded 2026暑假.html successfully!")
