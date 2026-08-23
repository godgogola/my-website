import re
import os

def upgrade_2026_summer():
    path = "public/2026暑假.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update CSS style block
    css_standard = """    <style>
        body {
            font-family: 'Inter', 'Noto Sans TC', sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            font-size: 16px;
            line-height: 1.65;
            -webkit-text-size-adjust: 100%;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 232, 240, 0.85);
        }
        .hide-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .hide-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        @media (max-width: 640px) {
            body {
                font-size: 16px;
            }
            .day-card {
                padding: 0.85rem !important;
            }
            .event-box {
                padding: 0.85rem !important;
            }
        }
        @media print {
            .no-print { display: none !important; }
            .print-break-inside { break-inside: avoid; }
            body { background: white !important; color: black !important; }
            .glass-card { border: 1px solid #ccc !important; box-shadow: none !important; }
        }
    </style>"""

    content = re.sub(r'<style>.*?</style>', css_standard, content, flags=re.DOTALL)

    # 2. Update Header
    content = content.replace(
        'class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16',
        'class="max-w-5xl mx-auto px-2.5 sm:px-6 lg:px-8 h-16'
    )

    # 3. Main container: decrease mobile padding from px-4 to px-2 (maximum reading width on mobile)
    content = re.sub(
        r'<main class="flex-grow max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-\d+ space-y-\d+"',
        '<main class="flex-grow max-w-5xl w-full mx-auto px-2 sm:px-4 lg:px-6 py-4 sm:py-8 space-y-4 sm:space-y-6"',
        content
    )

    # 4. Banner padding
    content = content.replace('p-6 sm:p-8 shadow-xl', 'p-4 sm:p-7 shadow-xl')
    
    # 5. Search bar padding
    content = content.replace('p-4 rounded-2xl shadow-sm border border-slate-200', 'p-3 sm:p-4 rounded-xl sm:rounded-2xl shadow-sm border border-slate-200')

    # 6. Day Card padding: replace p-5 sm:p-6 with p-3 sm:p-5 sm:p-6
    content = content.replace(
        'day-card glass-card rounded-2xl p-5 sm:p-6',
        'day-card glass-card rounded-2xl p-3 sm:p-5 sm:p-6'
    )

    # 7. Inner event cards: replace p-5 rounded-2xl with event-box p-3.5 sm:p-5 rounded-xl sm:rounded-2xl
    content = content.replace(
        'p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-2.5',
        'event-box p-3.5 sm:p-5 rounded-xl sm:rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-2 sm:space-y-2.5'
    )

    # 8. Clean up lists: replace list-inside and small font sizes with standard text-base
    content = content.replace('list-disc list-inside text-sm sm:text-base text-slate-700 space-y-2 leading-relaxed', 'list-disc pl-5 text-base leading-relaxed text-slate-700 space-y-2')
    content = content.replace('list-disc list-inside text-xs text-slate-600 space-y-1', 'list-disc pl-5 text-base leading-relaxed text-slate-700 space-y-2')
    content = content.replace('list-disc list-inside text-sm sm:text-base space-y-1 text-sky-900', 'list-disc pl-5 text-base leading-relaxed space-y-1 text-sky-900')
    content = content.replace('list-disc list-inside text-xs text-slate-600', 'list-disc pl-5 text-base leading-relaxed text-slate-700 space-y-2')
    content = content.replace('list-disc list-inside', 'list-disc pl-5')

    # 9. Clean up any remaining tiny text classes
    content = content.replace('class="text-xs text-slate-600"', 'class="text-base leading-relaxed text-slate-700"')
    content = content.replace('class="text-xs text-slate-500"', 'class="text-sm text-slate-500"')
    content = content.replace('class="text-[11px] leading-relaxed"', 'class="text-sm sm:text-base leading-relaxed"')
    content = content.replace('text-[11px]', 'text-sm')
    content = content.replace('text-[10px]', 'text-xs')

    # Save to both 2026暑假.html and 2026暑假/index.html
    with open("public/2026暑假.html", "w", encoding="utf-8") as f:
        f.write(content)
    with open("public/2026暑假/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: 2026 summer (Melbourne) updated successfully!")

def upgrade_2026_winter():
    path = "public/2026寒假.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update CSS style block
    css_standard = """    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');

        body {
            font-family: 'Noto Sans TC', sans-serif;
            background-color: #f0f4f8;
            scroll-behavior: smooth;
            font-size: 16px;
            line-height: 1.65;
            -webkit-text-size-adjust: 100%;
        }

        /* Hide scrollbar */
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .no-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }

        /* Timeline adjustments for larger circles */
        .timeline-line {
            position: absolute;
            left: 27px;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: #cbd5e1;
            z-index: 0;
        }

        .hotel-card {
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .hotel-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }

        /* Sticky Nav Active State */
        .nav-btn.active {
            background-color: #2563eb;
            color: white;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Place Link Style */
        .place-link {
            color: #2563eb;
            text-decoration: none;
            transition: all 0.2s;
            border-bottom: 1px dotted transparent;
        }
        .place-link:hover {
            color: #1e40af;
            text-decoration: underline;
            text-underline-offset: 4px;
        }
        
        /* Time Circle Text Shadow for better readability */
        .time-text {
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }

        @media (max-width: 640px) {
            body {
                font-size: 16px;
            }
            .timeline-card {
                padding: 0.75rem !important;
            }
        }
    </style>"""

    content = re.sub(r'<style>.*?</style>', css_standard, content, flags=re.DOTALL)

    # 2. Main container
    content = content.replace('max-w-3xl mx-auto px-2 sm:px-4 py-6 space-y-12 pb-24', 'max-w-3xl mx-auto px-2 sm:px-4 py-4 sm:py-6 space-y-8 sm:space-y-10 pb-24')

    # 3. Upgrade text sizes across events
    content = content.replace('text-sm text-gray-600 mt-1', 'text-base text-gray-700 leading-relaxed mt-1')
    content = content.replace('text-sm text-gray-600', 'text-base text-gray-700 leading-relaxed')
    content = content.replace('text-xs text-gray-400 mt-2', 'text-sm text-gray-500 mt-1.5')
    content = content.replace('text-xs text-gray-400', 'text-sm text-gray-500')
    content = content.replace('list-disc list-inside', 'list-disc pl-5')

    # 4. Event boxes
    content = content.replace(
        'ml-3 sm:ml-4 bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex-1',
        'ml-2.5 sm:ml-4 bg-white timeline-card p-3.5 sm:p-4 rounded-xl shadow-sm border border-gray-100 flex-1'
    )
    content = content.replace(
        'h-16 w-16 flex items-center justify-center text-white shrink-0 border-4 border-white shadow-md',
        'h-14 w-14 sm:h-16 sm:w-16 flex items-center justify-center text-white shrink-0 border-3 sm:border-4 border-white shadow-md'
    )

    # Save to both 2026寒假.html and 2026寒假/index.html
    with open("public/2026寒假.html", "w", encoding="utf-8") as f:
        f.write(content)
    with open("public/2026寒假/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: 2026 winter (Queensland) updated successfully!")

def upgrade_2025_summer():
    path = "public/2025暑假.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure 16px base font size & responsive mobile padding
    content = re.sub(
        r'body\s*\{\s*font-family:[^;]+;\s*line-height:[^;]+;\s*color:[^;]+;\s*background-color:[^;]+;\s*margin:[^;]+;\s*padding:[^;]+;\s*\}',
        """body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.65;
            color: #333;
            background-color: #f4f7f6;
            margin: 0;
            padding: 20px;
            font-size: 16px;
            -webkit-text-size-adjust: 100%;
        }""",
        content
    )

    # Save to both 2025暑假.html and 2025暑假/index.html
    with open("public/2025暑假.html", "w", encoding="utf-8") as f:
        f.write(content)
    with open("public/2025暑假/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: 2025 summer (Sydney) updated successfully!")

if __name__ == "__main__":
    upgrade_2026_summer()
    upgrade_2026_winter()
    upgrade_2025_summer()
