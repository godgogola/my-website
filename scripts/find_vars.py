with open(r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Occurrences of skyDomeMesh:")
for idx, l in enumerate(lines):
    if "skyDomeMesh" in l:
        print(f"  Line {idx+1}: {repr(l)}")

print("\nOccurrences of lighthouseBeamMesh:")
for idx, l in enumerate(lines):
    if "lighthouseBeamMesh" in l:
        print(f"  Line {idx+1}: {repr(l)}")
