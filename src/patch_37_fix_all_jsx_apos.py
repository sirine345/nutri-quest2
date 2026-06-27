"""
PATCH 37 — Corrige TOUTES les apostrophes dans les textes JSX directs
Usage: python patch_37_fix_all_jsx_apos.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

fixes = 0

REPLACEMENTS = {
    339: (
        "Le <strong style={{ color:\"#333\" }}>Programme National Nutrition Santé</strong> est une initiative française visant à améliorer la santé publique à travers des actions nutritionnelles. Il promeut une alimentation équilibrée, l\\'activité physique régulière, et la prévention des maladies liées à la nutrition.",
        "Le <strong style={{ color:\"#333\" }}>Programme National Nutrition Santé</strong> est une initiative française visant à améliorer la santé publique à travers des actions nutritionnelles. Il promeut une alimentation équilibrée, l&apos;activité physique régulière, et la prévention des maladies liées à la nutrition."
    ),
    1504: (
        "Le PNNS fixe des objectifs de consommation pour chaque groupe alimentaire. Le trait noir sur chaque barre indique l'objectif à atteindre.",
        "Le PNNS fixe des objectifs de consommation pour chaque groupe alimentaire. Le trait noir sur chaque barre indique l&apos;objectif à atteindre."
    ),
    1542: (
        "maximum (classée cancérigène groupe 1 par l'OMS).",
        "maximum (classée cancérigène groupe 1 par l&apos;OMS)."
    ),
    2050: (
        'viens {\\"t\'amuser\\"} en',
        "viens {\"t'amuser\"} en"
    ),
    3631: (
        "n'est nécessaire.",
        "n&apos;est nécessaire."
    ),
    4381: (
        "c'est pour toi !",
        "c&apos;est pour toi !"
    ),
}

for linenum, (old, new) in REPLACEMENTS.items():
    line = lines[linenum-1]
    if old in line:
        lines[linenum-1] = line.replace(old, new)
        fixes += 1
        print(f"✅ Ligne {linenum} corrigée")
    else:
        print(f"⚠️  Ligne {linenum} non trouvée: {old[:50]}")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n{fixes}/6 correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
