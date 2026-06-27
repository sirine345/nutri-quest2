"""
PATCH 39 — Corrige l'apostrophe ligne 339 (l'activité dans IntroScreen)
Usage: python patch_39_fix_l339.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

fixes = 0

# Fix 1: l'activité physique in JSX text (L339)
old = "Il promeut une alimentation équilibrée, l'activité physique régulière, et la prévention des maladies liées à la nutrition."
new = "Il promeut une alimentation équilibrée, l&apos;activité physique régulière, et la prévention des maladies liées à la nutrition."
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("✅ L339 - l'activité corrigée")

# Fix 2: Check for any other raw apostrophes in JSX text
# "Commencer l'aventure →" in button text
old2 = "Commencer l'aventure →"
new2 = "Commencer l&apos;aventure →"
if old2 in content:
    content = content.replace(old2, new2)
    fixes += 1
    print("✅ Commencer l'aventure corrigée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{fixes} correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
